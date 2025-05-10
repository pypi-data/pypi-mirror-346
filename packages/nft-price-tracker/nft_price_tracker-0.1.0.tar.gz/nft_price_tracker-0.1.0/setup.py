from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nft-price-tracker",
    version="0.1.0",
    author="Adolius",
    author_email="danghuy174@gmail.com",  # Thay đổi email của bạn
    description="A tool for tracking NFT prices across OpenSea and Magic Eden marketplaces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danghuy174/NftTracking",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests",
        "colorama",
        "python-dotenv",
        "tqdm",
        "asyncio"
    ],
    entry_points={
        "console_scripts": [
            "nft-tracker=nft_price_tracker.main:main",
        ],
    },
) 