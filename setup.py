from setuptools import find_packages
from setuptools import setup

setup(
    name="MicrosoftDesigner",
    version="0.0.4",
    license="GNU General Public License v2.0",
    author="Talaviya Bhavik",
    author_email="talaviyabhavik@proton.me",
    description="High quality image generation by Microsoft Designer. Reverse engineered API.",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/imnotdev25/Msdesigner-api",
    project_urls={
        "Bug Report": "https://github.com/imnotdev25/Msdesigner-api/issues/new",
    },
    install_requires=[
        "httpx",
        ""
    ],
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    py_modules=["Msdesigner"],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)