from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nft-price-tracker",
    version="0.2.0",
    author="danghuy174",
    author_email="danghuy174@gmail.com",
    description="A package to track NFT prices across OpenSea and Magic Eden marketplaces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danghuy174/nft-price-tracker",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3.8.0",
        "python-dotenv>=0.19.0",
        "requests>=2.26.0",
    ],
) 