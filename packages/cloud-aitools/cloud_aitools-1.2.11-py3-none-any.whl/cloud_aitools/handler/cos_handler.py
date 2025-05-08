from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from dataclasses import dataclass
from io import BytesIO
import json
import logging
from pathlib import Path
import time
from blake3 import blake3
import minio
from minio import Minio
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import urllib3

from ..utils.async_downloader import AsyncDownloader
from ..model.models import Index, ObjectIndex, UploadObject
from ..utils.progress import ProgressTracker

# 正常情况日志级别使用 INFO，需要定位时可以修改为 DEBUG，此时 SDK 会打印和服务端的通信信息
logger = logging.getLogger(__name__)

class ObjectInfo:

    def __init__(self, region: str, bucket_name: str, object_key: str,
                 size: int):
        self.region = region
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.size = size

    def is_dir(self) -> bool:
        return self.object_key.endswith("/")

    @property
    def url(self) -> str:
        return f"https://{self.bucket_name}.cos.{self.region}.myqcloud.com/{self.object_key}"

@dataclass
class ClientConfig:
    region: str
    secret_id: str
    secret_key: str
    endpoint: str
    secure: bool = True

class COSHandler:

    def __init__(
        self,
        region: str,
        secret_id: str,
        secret_key: str,
        scheme: str = "https",
        max_thread_num: int = 32,
    ) -> None:

        self.region = region
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.scheme = scheme
        self.max_thread_num = max_thread_num

        self.endpoint = f"cos.{region}.myqcloud.com"


        if self.secret_id and self.secret_key:
            self.client_config = CosConfig(
                Region=region,
                SecretId=secret_id,
                SecretKey=secret_key,
                Scheme=scheme,
                PoolMaxSize=1000,
                PoolConnections=1000,
                KeepAlive=True
            )
            
            self.client = CosS3Client(self.client_config)

        self.minio_client = Minio(
            endpoint=self.endpoint,
            access_key=secret_id,
            secret_key=secret_key,
            secure=True,
            region=region,
            http_client=urllib3.PoolManager(maxsize=1000))

        self.minio_client.enable_virtual_style_endpoint()

    def get_new_cos_client(self):
        return CosS3Client(self.client_config)

    def get_client_config(self):
        return ClientConfig(region=self.region,
                            secret_id=self.secret_id,
                            secret_key=self.secret_key,
                            endpoint=self.endpoint)

    def get_new_minio_client(self):
        return Minio(endpoint=self.endpoint,
                     access_key=self.secret_id,
                     secret_key=self.secret_key,
                     region=self.region)

    def list_objects(self, bucket: str, prefix: str):
        res = self.minio_client.list_objects(bucket,
                                             prefix=prefix,
                                             recursive=True)
        return res

    def create_process_pool_for_buckets(
            self,
            buckets: set[str],
            max_process: int = 10) -> dict[str, ProcessPoolExecutor]:

        res = {}
        for i, bucket in enumerate(buckets):
            res[bucket] = ProcessPoolExecutor(max_process)

        return res

    @staticmethod
    def hash_file(file_path: str):
        hasher = blake3(max_threads=blake3.AUTO)
        hasher.update_mmap(Path(file_path))
        return hasher.hexdigest()
        
    @staticmethod
    def upload_file(client: CosS3Client,
                    bucket: str,
                    key: str,
                    local_path: str,
                    part_size: int = 10,
                    thread_num: int = 32):
        tracker = ProgressTracker(bucket, key)
        
        client.upload_file(
            bucket,
            key,
            Path(local_path),
            PartSize=part_size,
            MAXThread=thread_num,
            progress_callback=tracker.update,
            Metadata={
                'x-cos-meta-blake3': COSHandler.hash_file(local_path),
            }
        )

    def get_object(self, bucket: str, object_key: str):
        try:
            content = self.minio_client.get_object(
                bucket, object_key).read().decode("utf-8")
            return content
        except minio.error.S3Error as e:
                raise

    def upload_objects(self, upload_object_ls: list[UploadObject]):

        buckets = set()
        bucket_objects: dict[str, list[UploadObject]] = {}
        for object_info in upload_object_ls:
            buckets.add(object_info.bucket)
            bucket_objects.setdefault(object_info.bucket,
                                      []).append(object_info)

        bucket_process_pool = self.create_process_pool_for_buckets(buckets)

        futures = set()
        for bucket, object_ls in bucket_objects.items():
            for object_info in object_ls:
                future = bucket_process_pool[bucket].submit(self.upload_file,
                                                   self.get_new_cos_client(),
                                                   bucket,
                                                   object_info.object_key,
                                                   object_info.filepath)

                futures.add(future)
        
        
        for future in futures:
            future.result()
            
        for bucket, pool in bucket_process_pool.items():
            pool.shutdown()
            
        logger.info("upload success.")

    @staticmethod
    def create_minio_client_from_config(config: ClientConfig):
        client = Minio(endpoint=config.endpoint,
                       access_key=config.secret_id,
                       secret_key=config.secret_key,
                       region=config.region)
        client.enable_virtual_style_endpoint()
        return client

    @staticmethod
    def get_appid_from_bucket(bucket: str):
        *_, appid = bucket.split("-")
        return appid

    @staticmethod
    def generate_read_only_bucket_policy(region: str, bucket: str):
        policy = {
            "Statement": [{
                "Action": ["name/cos:GetObject", "name/cos:HeadObject"],
                "Effect":
                "Allow",
                "Principal": {
                    "qcs": ["qcs::cam::anyone:anyone"]
                },
                "Resource": [
                    f"qcs::cos:ap-shanghai:uid/{COSHandler.get_appid_from_bucket(bucket)}:{bucket}/*"
                ]
            }],
            "version":
            "2.0"
        }

        return policy

    def create_buckets(self, buckets: list[str], public_read: bool = False):
        logger.info("Creating %d buckets", len(buckets))
        for bucket in buckets:
            if not self.minio_client.bucket_exists(bucket):
                logger.debug("Creating bucket: %s", bucket)
                self.minio_client.make_bucket(bucket)
                logger.info("Created bucket: %s", bucket)
            else:
                logger.debug("Bucket already exists: %s", bucket)

            if public_read:
                self.minio_client.set_bucket_policy(
                    bucket,
                    json.dumps(
                        self.generate_read_only_bucket_policy(
                            self.region, bucket)))

    def upload_object_to_buckets(self, buckets: list[str], object_key: str,
                                 object_content: bytes):
        logger.info("Uploading object %s to %d buckets", object_key,
                    len(buckets))
        for bucket in buckets:
            logger.debug("Uploading to bucket: %s", bucket)
            self.minio_client.put_object(bucket, object_key,
                                         BytesIO(object_content),
                                         len(object_content))
            logger.debug("Uploaded to bucket: %s", bucket)

    def download_file(self, bucket: str, key: str, local_path: str):
        local_path_ = Path(local_path)
        if not local_path_.parent.exists():
            local_path_.parent.mkdir(parents=True, exist_ok=True)

        if key.endswith("/"):
            return

        self.minio_client.fget_object(bucket_name=bucket,
                                      object_name=key,
                                      file_path=local_path)


    @staticmethod
    def download_file_with_cos_client(
            client: CosS3Client,
            bucket: str,
            key: str,
            local_path: str,
            max_thread_num: int = 32):

        tracker = ProgressTracker(bucket, key)
        local_path_ = Path(local_path)
        if not local_path_.parent.exists():
            local_path_.parent.mkdir(parents=True, exist_ok=True)

        if key.endswith("/"):
            return

        client.download_file(
            bucket,
            key,
            local_path,
            PartSize=20,
            MAXThread=max_thread_num,
            progress_callback=tracker.update,
        )

    def stat_objcet(self, object: ObjectInfo):
        return self.minio_client.stat_object(object.bucket_name,
                                             object.object_key)

    def stat_objects(self, objects: list[ObjectInfo]):
        res = []
        with ThreadPoolExecutor(max_workers=32) as executor:
            res = list(executor.map(self.stat_objcet, objects))

        return res

    def sum_objects_size(self, objects: list[ObjectInfo]):
        return sum([
            int(obj.size) for obj in self.stat_objects(objects)
            if not obj.is_dir and obj.size
        ])

    def download_objects_cos_client(self,
                                    objects: list[ObjectInfo],
                                    local_dir: str,
                                    max_workers_per_bucket: int = 5,
                                    progress_title: str = "Processing...:"):
        buckets = set()
        bucket_objects = {}

        for obj in objects:
            buckets.add(obj.bucket_name)
            bucket_objects.setdefault(obj.bucket_name,
                                      []).append(obj.object_key)

        process_pool = self.create_process_pool_for_buckets(buckets, max_process=max_workers_per_bucket)

        for bucket, object_ls in bucket_objects.items():
            for object_key in object_ls:
                process_pool[bucket].submit(
                    self.download_file_with_cos_client,
                    CosS3Client(self.client_config),
                    bucket,
                    object_key,
                    Path(local_dir) / object_key)

        start_time = time.time()

        for _, pool in process_pool.items():
            pool.shutdown(wait=True)

        total_size = sum([obj.size for obj in objects])
        spent_time = time.time() - start_time

        logger.info(
            f"Download time taken: {spent_time} seconds, "
            f"total download size: {total_size/1024**3:.2f} GB, "
            f"average speed: {total_size / spent_time / 1024**2:.2f} MB/s")

    def load_index_config(self, bucket: str, object_key: str = "index.json"):
        index_json = self.get_object(bucket, object_key)

        if not index_json:
            index_json = "[]"

        return Index(json.loads(index_json))

    def download_objects_from_index(self,
                                    objects_index: list[ObjectIndex],
                                    local_dir: str,
                                    process_num: int = 32,
                                    progress_title: str = "Processing...:"):
        async_downloader = AsyncDownloader(concurrent_num=process_num,
                                           progress_title=progress_title,
                                           enable_blake3_verify=True,
                                           blake3_header="x-cos-meta-blake3")
        
        urls = [index.url for index in objects_index]
        async_downloader.download(urls, local_dir)

    def download_objects_anonymous(self,
                                   objects_info: list[ObjectInfo],
                                   local_dir: str,
                                   progress_title: str = "Processing...:"):
        async_downloader = AsyncDownloader(progress_title=progress_title)
        urls = [item.url for item in objects_info]
        async_downloader.download(urls, local_dir)