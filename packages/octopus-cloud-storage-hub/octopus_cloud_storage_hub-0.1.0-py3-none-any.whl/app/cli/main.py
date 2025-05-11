"""命令行主模块"""

import os
import typer
from pathlib import Path

from app.handlers.oss import OssHandler


app = typer.Typer(
    name = "octopus_cloud_storage_hub",
    help = "Octopus Cloud Storage Hub CLI",
    add_completion = False
)

oss_handler = OssHandler(
    access_key_id="LTAI5tBgRuuFTqv38Q7bHZEX",
    access_key_secret="zqj9UfQjO6kC8LHoMsZYMkSaVguxOQ",
    endpoint="https://oss-ap-northeast-2.aliyuncs.com",
    bucket_name="gcollar"
)

@app.command("upload")
def upload(
    object_name: str = typer.Argument(..., help="Cloud object name"),
    file_path: Path = typer.Argument(..., help="Local file path")
):
    """
    上传文件
    """
    result = oss_handler.upload(object_name, file_path)

@app.command("download")
def download(
    object_name: str = typer.Argument(..., help="Cloud object name"),
    file_path: Path = typer.Argument(..., help="Local file path")
):
    """
    下载文件
    """
    oss_handler.download(object_name, file_path)

@app.command("delete")
def delete(object_name: str = typer.Argument(..., help="Cloud object name")):
    """
    删除云存储文件
    """
    oss_handler.delete(object_name)

if __name__ == "__main__":
    app()
