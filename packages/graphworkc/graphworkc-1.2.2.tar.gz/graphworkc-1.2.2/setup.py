import glob
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11 import get_include
import os
import sys


# 设置OpenMP编译选项
def get_openmp_flags():
    if sys.platform.startswith('win'):
        return {'extra_compile_args': ['/openmp'], 'extra_link_args': []}
    else:
        return {'extra_compile_args': ['-fopenmp'], 'extra_link_args': ['-fopenmp']}


cpp_sources = glob.glob("src/*.cpp", recursive=True)

ext_modules = [
    Pybind11Extension(
        "graphwork",
        sources=cpp_sources,
        define_macros=[('EXAMPLE_MACRO', '1')],
        include_dirs=["src", get_include()],
        **get_openmp_flags()  # 动态添加OpenMP选项
    ),
]

# 获取当前目录
here = os.path.dirname(os.path.abspath(__file__))

# 确保 Python 文件被包含
py_modules = [
    "graphworkc",  # 你的 Python 模块
]

setup(
    name="graphworkc",  # 这里与模块名称一致
    version="1.2.2",
    author="ZC",
    description="A Python package with pybind11 extensions",
    long_description="This package contains a C++ extension wrapped using pybind11, providing graph-related functionality.",
    long_description_content_type="text/markdown",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    py_modules=py_modules,  # 显式列出所有需要打包的 Python 文件
    include_package_data=True,  # 确保包含 `package_data`
    python_requires=">=3.9",  # 指定支持的Python版本
    install_requires=["pybind11>=2.5.0", "numpy"],  # 确保安装pybind11
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},  # Python 文件位于 src 目录下
)
