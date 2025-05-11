
from setuptools import setup, find_packages

setup(
    name="probctrl",
    version="0.1.1",
    description="A lightweight Python decorator toolkit for probabilistic, delayed, and throttled execution.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="0.1.0",
    author_email="982074664@qq.com",
    url="https://github.com/Lovelymili/probctrl",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.6",
)
