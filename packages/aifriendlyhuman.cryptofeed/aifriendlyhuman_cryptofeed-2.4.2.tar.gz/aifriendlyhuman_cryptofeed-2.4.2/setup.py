'''
Copyright (C) 2025-2025 Gildas David - gildas@qloned.ai

Please see the LICENSE file for the terms and conditions
associated with this software.
'''
import os
import sys

from setuptools import Extension, setup
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
from setuptools.command.bdist_wheel import bdist_wheel
from Cython.Build import cythonize

class BdistWheel(bdist_wheel):
    def finalize_options(self):
        # Mark as not requiring a specific Python implementation or ABI
        bdist_wheel.finalize_options(self)
        self.root_is_pure = False
        # Mark wheel as compatible with any Python ABI
        self.plat_name_supplied = True
        self.plat_name = "any"


def get_long_description():
    """Read the contents of README.md, INSTALL.md and CHANGES.md files."""
    from os import path

    repo_dir = path.abspath(path.dirname(__file__))
    markdown = []
    for filename in ["README.md", "INSTALL.md", "CHANGES.md"]:
        with open(path.join(repo_dir, filename), encoding="utf-8") as markdown_file:
            markdown.append(markdown_file.read())
    return "\n\n----\n\n".join(markdown)


class Test(TestCommand):
    def run_tests(self):
        import pytest
        errno = pytest.main(['tests/'])
        sys.exit(errno)


extra_compile_args = ["/O2" if os.name == "nt" else "-O3"]
define_macros = []

# comment out line to compile with type check assertions
# verify value at runtime with cryptofeed.types.COMPILED_WITH_ASSERTIONS
define_macros.append(('CYTHON_WITHOUT_ASSERTIONS', None))

extension = Extension("cryptofeed.types", ["cryptofeed/types.pyx"],
                      extra_compile_args=extra_compile_args,
                      define_macros=define_macros)

setup(
    name="aifriendlyhuman.cryptofeed",
    ext_modules=cythonize([extension], language_level=3, force=True),
    version="2.4.2",
    author="Gildas David",
    author_email="gildas@qloned.ai",
    description="Cryptocurrency Exchange Websocket Data Feed Handler",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    license="XFree86",
    keywords=["cryptocurrency", "bitcoin", "btc", "feed handler", "market feed", "market data", "crypto assets",
              "Trades", "Tickers", "BBO", "Funding", "Open Interest", "Liquidation", "Order book", "Bid", "Ask",
              "fmfw.io", "Bitfinex", "bitFlyer", "AscendEX", "Bitstamp", "Blockchain.com", "Bybit",
              "Binance", "Binance Delivery", "Binance Futures", "Binance US", "BitMEX", "Coinbase", "Deribit", "EXX",
              "Gate.io", "Gemini", "HitBTC", "Huobi", "Huobi DM", "Huobi Swap", "Kraken",
              "Kraken Futures", "OKCoin", "OKX", "Poloniex", "ProBit", "Upbit"],
    url="https://github.com/aifriendlyhuman/cryptofeed",
    project_urls={
        "Source": "https://github.com/aifriendlyhuman/cryptofeed",
    },
    packages=find_packages(exclude=['tests*']),
    cmdclass={
        'test': Test,
        'bdist_wheel': BdistWheel
    },
    python_requires='>=3.9',
    classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: AsyncIO",
    ],
    tests_require=["pytest"],
    install_requires=[
        "requests>=2.18.4",
        "websockets>=14.1",
        "pyyaml",
        "aiohttp>=3.11.6",
        "aiofile>=2.0.0",
        "yapic.json>=1.6.3",
        'uvloop ; platform_system!="Windows"',
        "order_book>=0.6.0",
        "aiodns>=1.1"  # aiodns speeds up DNS resolving
    ],
    extras_require={
        "arctic": ["arctic", "pandas"],
        "gcp_pubsub": ["google_cloud_pubsub>=2.4.1", "gcloud_aio_pubsub"],
        "kafka": ["aiokafka>=0.7.0"],
        "mongo": ["motor"],
        "postgres": ["asyncpg"],
        "quasardb": ["quasardb", "numpy"],
        "rabbit": ["aio_pika", "pika"],
        "redis": ["hiredis", "redis>=4.5.1"],
        "zmq": ["pyzmq"],
        "all": [
            "arctic",
            "google_cloud_pubsub>=2.4.1",
            "gcloud_aio_pubsub",
            "aiokafka>=0.7.0",
            "motor",
            "asyncpg",
            "aio_pika",
            "pika",
            "hiredis",
            "redis>=4.5.1",
            "pyzmq",
        ],
    },
)
