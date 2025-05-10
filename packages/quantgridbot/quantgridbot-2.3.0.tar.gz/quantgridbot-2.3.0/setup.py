from setuptools import setup, find_packages

try:
    long_description = open("README.md", encoding="utf-8").read()
except Exception:
    long_description = "Quant-GridBot: Quant-Grade Ethereum Grid Trading and Portfolio Rebalancing Engine"

setup(
    name="quantgridbot",
    version="2.1.3",
    author="LoQiseaking69",
    author_email="REEL0112359.13@proton.me",
    description="Quant-Grade Ethereum Grid Trading + Intelligent Portfolio Rebalancer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LoQiseaking69/qgbot",
    license="BSD-3-Clause",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "ecdsa>=0.18",
        "numpy>=1.23",
        "requests>=2.28",
        "rich>=13.0",
        "eth-utils>=2.1",
    ],
    entry_points={
        "console_scripts": [
            "quantgridbot=qgbot.app:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries",
    ],
    keywords=[
        "ethereum",
        "grid trading",
        "crypto bot",
        "eth bot",
        "defi automation",
        "uniswap trading",
        "crypto quant system",
        "volatility trading",
        "portfolio rebalancing",
        "python trading bot",
        "autonomous agent",
    ],
)