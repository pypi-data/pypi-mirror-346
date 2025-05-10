from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "py2hackCraft/README.md").read_text()

setup(
    name="py2hackCraft2",
    version="1.0.35",
    packages=find_packages(),
    install_requires=[
        "websocket-client"  # websocketライブラリの追加
        # 他にも依存する外部ライブラリがあれば、同様にリストに追加
    ],
    # その他のメタデータ
    author="Masafumi Terazono",
    author_email="masafumi_t@0x48lab.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    description="These are APIs that connect to the hackCraft2 server from Python to manipulate pets.",
    license="MIT",
    keywords="hackCraft2",
    url="https://pypi.org/project/py2hackCraft2/",   # プロジェクトホームページのURL
)