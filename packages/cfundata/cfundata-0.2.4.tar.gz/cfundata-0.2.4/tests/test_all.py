from cfundata import FONT_SIMSUN_PATH, datapath
from cfundata.dx import (
    DX_CLS_ONNX_PATH,
    DX_CLS_PT_PATH,
    DX_DET_ONNX_PATH,
    DX_DET_PT_PATH,
)
from cfundata.freq import FREQUENCY2_PATH, FREQUENCY_PATH


def test_paths():
    print("Testing paths...")

    # 通过访问资源路径，触发懒加载和下载
    print("FONT_SIMSUN_PATH:", FONT_SIMSUN_PATH)
    assert FONT_SIMSUN_PATH.exists()  # 确保文件存在，或者已下载

    print("DX_CLS_ONNX_PATH:", DX_CLS_ONNX_PATH)
    assert DX_CLS_ONNX_PATH.exists()

    print("DX_CLS_PT_PATH:", DX_CLS_PT_PATH)
    assert DX_CLS_PT_PATH.exists()

    print("DX_DET_ONNX_PATH:", DX_DET_ONNX_PATH)
    assert DX_DET_ONNX_PATH.exists()

    print("DX_DET_PT_PATH:", DX_DET_PT_PATH)
    assert DX_DET_PT_PATH.exists()

    print("FREQUENCY_PATH:", FREQUENCY_PATH)
    assert FREQUENCY_PATH.exists()

    print("FREQUENCY2_PATH:", FREQUENCY2_PATH)
    assert FREQUENCY2_PATH.exists()

    print(datapath.DX_DET_ONNX)
    print(datapath.DX_CLS_ONNX)
    print(datapath)


if __name__ == "__main__":
    test_paths()
    print("All tests passed!")
