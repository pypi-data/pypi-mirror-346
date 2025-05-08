#!/usr/bin/env python
from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

# 获取版本号
about = {}
with open(os.path.join(here, 'fastapi_backend_template', '__init__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

# 读取README文件内容
with open(os.path.join(here, 'SCAFFOLD-README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="fastapi-backend-template",
    version=about['__version__'],
    description="快速创建基于FastAPI的后端项目的脚手架工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Gavin Cui",
    author_email="gavincui1026@gmail.com",
    url="https://github.com/gavincui1026/Fastapi-Backend.git",
    packages=find_packages(),
    package_data={
        '': ['template/**/*', 'template/**/**/*', 'template/**/**/**/*'],
    },
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.104.1",
        "pydantic>=2.5.2",
    ],
    entry_points={
        'console_scripts': [
            'fastapi-backend=fastapi_backend_template.cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    keywords="fastapi, backend, template, scaffold, generator",
) 