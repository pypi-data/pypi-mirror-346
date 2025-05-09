
from setuptools import setup, find_packages

setup(
    name="snu_dhc",
    version="0.1.1",
    author="Dong Hyun Choi",
    author_email="donghyun369@naver.com",
    description="SNU_DHC Package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
