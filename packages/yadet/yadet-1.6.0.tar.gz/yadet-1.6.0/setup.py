# -*- coding: utf-8 -*-
from setuptools import setup


install_requires = ["pyodbc"]

setup(
    name="yadet",
    version="1.6.0",
    author="Robert Goss",
    author_email="robertgoss07@gmail.com",
    packages=[
        "yadet", "yadet.batch", "yadet.config", "yadet.engine", "yadet.engine.source", 
        "yadet.engine.target", "yadet.errors", "yadet.helpers", "yadet.interface", 
        "yadet.objects"
    ],
    license="MIT",
    extras = {"extras": install_requires},
    url="https://github.com/robbitt07/yadet",
    install_requires=install_requires,
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="A simple and effective Python data extraction tool",
    long_description=open("README.md").read(),
    zip_safe=True,
)