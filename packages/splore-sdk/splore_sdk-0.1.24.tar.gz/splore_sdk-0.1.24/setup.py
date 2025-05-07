from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="splore-sdk",
    version="0.1.24",
    author="DilipCoder",
    author_email="dilips.ven@splore.com",
    description="Python SDK for Splore",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/splorehq/splore-sdk-py",
    project_urls={
        "Homepage": "https://github.com/splorehq/splore-sdk-py",
        "Documentation": "https://github.com/splorehq/splore-sdk-py",
        "Changelog": "https://github.com/splorehq/splore-sdk-py/blob/main/CHANGELOG.md",
        "Issues": "https://github.com/splorehq/splore-sdk-py/issues",
        "Releases": "https://github.com/splorehq/splore-sdk-py/releases"
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7',
)
