import os
import re
import shutil
import sys

import pytest

root = os.path.abspath(os.path.join(os.path.dirname(__file__), r"../.."))
sys.path.append(root)

os.environ["root"] = root


@pytest.fixture
def cleanup_log_directory(request) -> str:
    test_name = re.search(r"(.*)\[", request.node.name).group(1)
    log_directory = rf"{root}\Results\{test_name}"
    if os.path.exists(log_directory):
        shutil.rmtree(log_directory)
        os.makedirs(log_directory)
    return log_directory
