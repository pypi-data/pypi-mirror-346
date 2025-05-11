"""命令行主模块"""

import os
import typer

from app.handlers.oss import OssHandler


app = typer.Typer(
    name = "octopus_cloud_storage_hub",
    help = "Octopus Cloud Storage Hub CLI",
    add_completion = False
)

oss_handler = OssHandler(
    access_key_id="",
    access_key_secret="",
    endpoint="",
    bucket_name=""
)
