import asyncio
from asyncio.log import logger
from concurrent.futures import ProcessPoolExecutor
import logging
from multiprocessing import Manager
from pathlib import Path
from queue import Queue
import time
from typing import Optional
import urllib.parse
import aiohttp
import urllib
from blake3 import blake3

from .progress import Progress, ProgressRole

logger = logging.getLogger(__name__)


class AsyncDownloader:

    progress_queue: Optional[Queue] = None

    def __init__(self,
                 concurrent_num: int = 32,
                 split_num: int = 6,
                 max_connections_per_process: int = 300,
                 show_progress: bool = True,
                 progress_title: str = "Processing...",
                 enable_blake3_verify: bool = False,
                 blake3_header: str = "") -> None:
        
        
        self.concurrent_num = concurrent_num
        self.split_num = split_num
        self.max_connections_per_process = max_connections_per_process

        self.show_progress = show_progress
        self.progress_title = progress_title

        self.enable_blake3_verify = enable_blake3_verify
        
        if self.enable_blake3_verify and not blake3_header:
            raise ValueError("blake3_header is required when enable_blake3_verify is True")
        
        self.blake3_header = blake3_header
        
        
    @staticmethod
    def gen_save_path(url: str, dir_: str = "./"):
        return str(Path(dir_) / Path(f"./{urllib.parse.urlparse(url).path}"))

    @staticmethod
    def prealloc_file(file_path: str | Path, object_size: int):
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()
        file_path.write_bytes(b"")

        with open(file_path, "rb+") as f:
            f.truncate(object_size)

    @staticmethod
    async def head_object(url: str):
        async with aiohttp.ClientSession() as session:
            async with session.head(url) as resp:
                return resp.headers
    
    
    async def get_object_blake3_hash(self, url: str):
        if not self.blake3_header:
            raise ValueError("blake3_header is empty or not specified.")
        
        headers = await AsyncDownloader.head_object(url)
        return headers.get(self.blake3_header, "")
    
    @staticmethod
    async def get_file_size(url: str):
        headers = await AsyncDownloader.head_object(url)
        return int(headers.get("Content-Length", 0))

    @staticmethod
    async def get_total_size(urls: list[str]):
        return sum(await asyncio.gather(
            *[AsyncDownloader.get_file_size(url) for url in urls]))

    
    @staticmethod
    async def verify_file(file_path: str, blake3_hash: str):
        hasher = blake3(max_threads=blake3.AUTO)
        hasher.update_mmap(file_path)
        local_hash = hasher.hexdigest()
        if local_hash != blake3_hash:
            raise ValueError(f"File {file_path} is corrupted. Local hash: {local_hash}, expected hash: {blake3_hash}")

    @staticmethod
    async def download_url(session: aiohttp.ClientSession, url, path):
        logger.info(f"Downloading {url} to {path}")
        content_length = await AsyncDownloader.get_file_size(url)
        async with session.get(url) as resp:
            with open(path, 'wb+') as f:
                while True:
                    chunk = await resp.content.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)

        logger.info(
            f"Downloaded {url} finished. Total download size: {content_length} bytes."
        )

    async def download_with_part(self, session: aiohttp.ClientSession,
                                 url: str,
                                 path: str,
                                 split_num: int = 4):

        async def download_part(part_number: int, part_size: int):
            start = part_number * part_size
            end = min(start + part_size - 1, content_length - 1)

            headers = {"Range": f"bytes={start}-{end}"}
            buffer_size = 1024 * 1024

            length = 0
            # 进度更新太频频繁会影响性能, 更新太慢会导致进度条显示的带宽不准
            # 经测试, 每20%更新一次较为合适, 不会影响性能, 且带宽显示较为准确
            update_threshold = part_size // 5
            async with session.get(url, headers=headers) as resp:
                resp.raise_for_status()
                with open(path, 'rb+') as f:
                    f.seek(start)
                    while (chunk := await resp.content.read(buffer_size)):
                        length += f.write(chunk)
                        if AsyncDownloader.progress_queue is not None and length >= update_threshold:
                            AsyncDownloader.progress_queue.put_nowait(length)
                            length = 0

            if AsyncDownloader.progress_queue is not None and length:
                AsyncDownloader.progress_queue.put_nowait(length)

        logger.debug("Downloading %s to %s.", url, path)
        content_length = await AsyncDownloader.get_file_size(url)

        part_size = content_length // split_num
        part_num = content_length // part_size + (1 if content_length %
                                                  part_size else 0)

        
        Path(path).touch()
        
        await asyncio.gather(*[
            asyncio.create_task(download_part(i, part_size))
            for i in range(part_num)
        ])

        if self.enable_blake3_verify:
            blake3_hash = await self.get_object_blake3_hash(url)
            if not blake3_hash:
                raise ValueError("blake3 hash is empty.")
            await self.verify_file(path, blake3_hash)
            
            
        logger.debug("Downloaded %s finished. Total downloaded size: %s bytes",
                     url, content_length)

    async def download_urls_async(self, urls: list[str], dir_: str = "./"):
        tcp_connector = aiohttp.TCPConnector(
            limit=self.max_connections_per_process)
        async with aiohttp.ClientSession(connector=tcp_connector) as session:
            async with asyncio.TaskGroup() as tg:
                for url in urls:
                    save_path = Path(AsyncDownloader.gen_save_path(url, dir_))
                    save_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    if self.split_num > 1:
                        tg.create_task(
                            self.download_with_part(
                                session,
                                url,
                                str(save_path),
                                split_num=self.split_num))
                    else:
                        tg.create_task(
                            AsyncDownloader.download_url(
                                session, url,
                                str(save_path)))

    def download_urls_single_process(self, urls: list[str], dir_: str = "./"):
        asyncio.run(self.download_urls_async(urls, dir_))

    def download(self, urls: list[str], dir_: str = "./"):

        manager = None
        if self.show_progress:
            manager = Manager()
            AsyncDownloader.progress_queue = manager.JoinableQueue()
            progress_tracker = Progress(AsyncDownloader.progress_queue,
                                        mode=ProgressRole.CONSUMER,
                                        progress_title=self.progress_title)
            total_length = asyncio.run(AsyncDownloader.get_total_size(urls))
            progress_tracker.set_meta(total_length)

        start_time = time.time()
        futures = set()
        with ProcessPoolExecutor(max_workers=self.concurrent_num) as executor:
            for i in range(self.concurrent_num):
                future = executor.submit(self.download_urls_single_process,
                                         urls[i::self.concurrent_num], dir_)
                futures.add(future)
                
            for future in futures:
                future.result()
                
        if AsyncDownloader.progress_queue is not None:
            AsyncDownloader.progress_queue.join()

        if manager:
            manager.shutdown()

        logger.info(f"download cost time: {time.time() - start_time}")


urls = [
    "https://aicompute-ap-shanghai-1-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00006-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-1-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00009-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-1-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00011-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-1-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00025-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-1-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00026-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-1-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00028-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-1-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00033-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-1-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00051-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-1-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00052-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-1-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00055-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-1-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00058-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-1-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00059-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-1-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00067-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-1-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00006-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-2-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00009-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-2-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00011-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-2-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00025-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-2-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00026-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-2-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00028-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-2-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00033-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-2-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00051-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-2-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00052-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-2-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00055-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-2-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00058-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-2-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00059-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-2-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00067-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-3-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00009-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-3-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00011-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-3-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00025-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-3-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00026-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-3-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00028-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-3-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00033-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-3-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00051-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-3-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00052-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-3-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00055-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-3-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00058-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-3-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00059-of-000163.safetensors",
    # "https://aicompute-ap-shanghai-3-1251001002.cos.ap-shanghai.myqcloud.com/DeepSeek-R1/model-00067-of-000163.safetensors",
]


def main():
    downloader = AsyncDownloader()
    downloader.download(urls, "/dev/shm/")


if __name__ == "__main__":
    main()
