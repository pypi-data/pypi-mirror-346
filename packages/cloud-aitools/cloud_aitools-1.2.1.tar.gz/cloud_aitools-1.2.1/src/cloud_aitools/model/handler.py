import logging
from pathlib import Path
from typing import Annotated, Optional
import typer
from typer import Option, Argument

from ..handler.cos_handler import COSHandler
from .distribute import generate_bucket_name, generate_buckets, generate_index, generate_upload_info
from ..utils.dns import detect_region
from ..utils.utils import get_files_in_directory

logger = logging.getLogger(__name__)

app = typer.Typer()
    
@app.command(name="upload", help="upload new model to cos.")
def upload(
            secret_id: Annotated[str, Option(help="The secret id of cos used for upload object.")],
            secret_key: Annotated[str, Option(help="The secret key of cos used for upload object.")],
            local_path: Annotated[str, Option(help="The local path of the model to upload.")],
            model_name: Annotated[str, Option(help="The name for the uploaded model.")],
            bucket_pattern: Annotated[str, Option(help="The pattern of the bucket name in the format 'bucket-appid'. \
                The actual bucket name will be bucket-region-i-appid.")],
            region: Annotated[str, Option(help="The region of the cos bucket.")],
            bucket_num: Annotated[int, Option(help="The number of buckets to create.")] = 8,
            excludes: Annotated[list[str], Option("--exclude", "-e", help="The file patterns to exclude from the upload.")] = []
        ):
    
    
    model_path = Path(local_path)
    file_list = get_files_in_directory(local_path, excludes)
    *prefix, appid = bucket_pattern.split("-")
    
    handler = COSHandler(region, secret_id, secret_key)
    
    buckets = generate_buckets(f"{'-'.join(prefix)}-{region}-{appid}", bucket_num)
    handler.create_buckets(buckets, public_read=True)
    
    upload_objects = generate_upload_info(buckets, file_list, model_name, model_path)
    first_bucket = next(iter(buckets))
    index = handler.load_index_config(first_bucket)
    model_index = generate_index(model_name, region=region, upload_objects=upload_objects)
    index.update(model_index)
    
    handler.upload_object_to_buckets(buckets, "index.json", index.dump().encode("utf-8"))
    
    logger.info("start to upload model to buckets: %s", buckets)
    handler.upload_objects(upload_objects)
    logger.info("upload model finished.")


@app.command(name="download", help="Download model from cos.")
def download_model(model_name: Annotated[str, Argument(help="The model name to download.")],
                   output_dir: Annotated[str, Option("--output", "-o", help="The output directory to save the downloaded model.")]="/dev/shm",
                   region: Annotated[Optional[str], Argument(help="The region of the cos bucket.")]="",
                   bucket_prefix: Annotated[Optional[str], Option(help="The prefix of the bucket name in the format 'bucket'.")]="aicompute",
                   appid: Annotated[Optional[str], Option(help="The appid of the cos bucket.")]="1251001002",
                   process_num: Annotated[int, Option("--process-num", "-p", help="The number of processes to use for downloading.")] = 64):

    if not region:
        logger.info("input region is empty, try to detect region automatically")
        detected_region = detect_region()
        
        if not detected_region:
            raise typer.BadParameter("region is not specified and cannot be detected automatically.")
        else:
            region = detected_region
            logger.info("detect region successfully, region is: %s", region)

    bucket_template = f"{bucket_prefix}-{appid}"
    first_bucket = generate_bucket_name(bucket_template, region, 0)
    
    handler = COSHandler(region, "", "")
    index = handler.load_index_config(first_bucket)
    
    model_index = index.get_model_objects_index(model_name)
    
    if not model_index:
        raise typer.BadParameter(f"model {model_name} not found.")
    
    handler.download_objects_from_index(model_index, output_dir, process_num=process_num, progress_title=f"Downloading {model_name}...")
    

@app.command(name="list", help="list the available models in remote repository.")
def list_model(
                region: Annotated[Optional[str], Option(help="The region of the cos bucket.")]="",
                bucket_prefix: Annotated[Optional[str], Option(help="The prefix of the bucket name in the format 'bucket'.")]="aicompute",
                appid: Annotated[Optional[str], Option(help="The appid of the cos bucket.")]="1251001002"):
    
    
    if not region:
        logger.info("input region is empty, try to detect region automatically")
        detected_region = detect_region()
        if not detected_region:
            raise typer.BadParameter("region is not specified and cannot be detected automatically.")
        else:
            region = detected_region
            logger.info("detect region successfully, region is: %s", region)
            
    bucket_template = f"{bucket_prefix}-{appid}"
    first_bucket = generate_bucket_name(bucket_template, region, 0)
    
    handler = COSHandler(region, "", "")
    index = handler.load_index_config(first_bucket)
    
    typer.echo("Model")
    for model_index in index.get_all_model_index():
        typer.echo(model_index.model_name)
    
    