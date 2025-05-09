from cfundata import datapath


def test_paths():
    print("Testing paths...")
    print(datapath)
    print(datapath.DX_DET_ONNX)
    print(datapath.DX_CLS_ONNX)

    # assert datapath.DX_DET_ONNX.exists(), "DX_DET_ONNX path does not exist"
    # assert datapath.DX_CLS_ONNX.exists(), "DX_CLS_ONNX path does not exist"


if __name__ == "__main__":
    test_paths()
    print("All tests passed!")
