"""下载文件pooch模块

优点：
    在本地下载并缓存您的数据文件（因此只需下载一次）
    通过验证加密哈希，确保运行代码的每个人都具有相同版本的数据文件。
    通过验证加密哈希，确保运行代码的每个人都具有相同版本的数据文件。
    ....

参考：
    https://www.fatiando.org/pooch/latest/about.html
"""

import json
from pathlib import Path

import pooch


def read_json(json_path: str) -> dict:
    """
    Read a JSON file and return its content as a dictionary.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def download_and_verify_models(paths: dict, model_info: dict):
    """
    下载并校验模型文件。

    :param paths: 一个字典，键为名称，值为本地路径
    :param model_info: 包含每个模型文件名对应的下载 URL 和 MD5 的字典
    :param max_retries: 最大重试次数
    """
    for key, value in paths.items():
        path = Path(value)
        if path.exists():
            continue

        filename = path.name
        info = model_info.get(filename, None)
        if not info:
            print(f"[Error] {filename} not found in model_info.")
            continue

        url = info["url"]
        expected_md5 = info["md5"]
        # print(f"Downloading {filename} from {url}...")
        # print(f"Expected MD5: {expected_md5}")
        # print(f"Saving to {path}...")
        # print(f"filename: {filename} ,  {path.parent}...")
        pooch.retrieve(
            url=url,
            known_hash=f"md5:{expected_md5}",
            fname=filename,
            path=path.parent,
            progressbar=True,
        )
