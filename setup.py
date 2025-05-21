"""
WCAG验证器安装配置文件
"""
from setuptools import setup, find_packages

setup(
    name="wcag_validator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4>=4.9.0",
        "requests>=2.25.0",
        "html5lib>=1.1"
    ],
    entry_points={
        "console_scripts": [
            "wcag-validator=wcag_validator.cli:main",
        ],
    },
    author="WCAG Validator Team",
    author_email="example@example.com",
    description="一个用于验证HTML是否符合WCAG 2.2标准的Python库",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/example/wcag-validator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
