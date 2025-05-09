import importlib.resources as pkg_resources
from dataclasses import asdict, dataclass
from pathlib import Path

from .down import download_and_verify_models, read_json
from .dx import DX_CLS_ONNX_PATH, DX_CLS_PT_PATH, DX_DET_ONNX_PATH, DX_DET_PT_PATH
from .font import FONT_SIMSUN_PATH
from .freq import FREQUENCY2_PATH, FREQUENCY_PATH


# 把这些封装为一个数据类
@dataclass(frozen=True)
class DataPath:
    """数据路径类，包含所有数据文件的路径

    该类用于存储数据文件的路径，提供了对数据文件的访问方式。(包含了改包的所有数据文件)
    该类的属性是不可变的，使用时请直接访问属性。

    Attributes:
        DX_DET_ONNX (Path): DX检测模型的ONNX文件路径
        DX_CLS_ONNX (Path): DX分类模型的ONNX文件路径
        DX_DET_PT (Path): DX检测模型的PyTorch文件路径
        DX_CLS_PT (Path): DX分类模型的PyTorch文件路径
        FONT_SIMSUN (Path): SimSun字体文件路径
        FREQUENCY (Path): 频率数据文件路径
        FREQUENCY2 (Path): 频率数据文件路径2

    Example:
        ```python
        from cfundata import datapath
        print(datapath.DX_DET_ONNX)
        print(datapath.DX_CLS_ONNX)
        print(datapath)
        ```
    """

    DX_DET_ONNX: Path = Path(DX_DET_ONNX_PATH)
    DX_CLS_ONNX: Path = Path(DX_CLS_ONNX_PATH)
    DX_DET_PT: Path = Path(DX_DET_PT_PATH)
    DX_CLS_PT: Path = Path(DX_CLS_PT_PATH)
    FONT_SIMSUN: Path = Path(FONT_SIMSUN_PATH)
    FREQUENCY: Path = Path(FREQUENCY_PATH)
    FREQUENCY2: Path = Path(FREQUENCY2_PATH)


datapath: DataPath = DataPath()


def _ensure_models_ready(datapath: DataPath):
    md5_path = pkg_resources.files("cfundata").joinpath("md5.json")
    model_info = {item["name"]: item for item in read_json(md5_path)}
    paths_dict = asdict(datapath)  # 这是一个 dict[str, Path]
    data = {}
    for _, path in paths_dict.items():
        i = path.name
        if i in model_info:
            data[i] = path

    download_and_verify_models(data, model_info)


_ensure_models_ready(datapath)

__all__ = [
    "datapath",
    "FONT_SIMSUN_PATH",
    "DX_CLS_ONNX_PATH",
    "DX_CLS_PT_PATH",
    "DX_DET_ONNX_PATH",
    "DX_DET_PT_PATH",
    "FREQUENCY2_PATH",
    "FREQUENCY_PATH",
]
