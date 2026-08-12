from importlib.metadata import version

import trabeculai


def test_package_import() -> None:
    assert trabeculai.__version__ == version("trabeculai")
