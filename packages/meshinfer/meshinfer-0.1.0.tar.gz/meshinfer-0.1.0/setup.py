import os
from setuptools import setup, find_packages
import urllib.request
import urllib.error
import re
import ast
from bs4 import BeautifulSoup
from pathlib import Path
from packaging.version import parse, Version

PACKAGE_NAME = "meshinfer"

this_dir = os.path.dirname(os.path.abspath(__file__))

def curr_version():
    with open(Path(this_dir) / "meshinfer" / "__init__.py", "r") as f:
        version_match = re.search(r"^__version__\s*=\s*(.*)$", f.read(), re.MULTILINE)
    public_version = ast.literal_eval(version_match.group(1))
    local_version = os.environ.get("MESHINFER_LOCAL_VERSION")
    if local_version:
        return f"{public_version}+{local_version}"
    else:
        return str(public_version)

def upload():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    with open('requirements.txt') as f:
        required = f.read().splitlines()

    setup(
        name=PACKAGE_NAME,
        version=curr_version(),
        author="Congjie He",
        author_email="congjiehe95@gmail.com",
        description="MeshInfer: Efficient Kernels Library for LLMs Serving on Mesh-arch Hardware",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/CongjieHe/meshinfer",
        packages=find_packages(),
        data_files=["requirements.txt"],
        # classifiers=[
        #     "Programming Language :: Python :: 3",
        #     "License :: OSI Approved :: MIT License",
        #     "Operating System :: OS Independent",
        # ],
        python_requires='>=3.8',
        install_requires=required,
    )

def main():
    try:
        upload()
        print("Upload success, Current VERSION:", curr_version())
    except Exception as e:
        raise Exception("Upload package error", e)

if __name__ == '__main__':
    main()