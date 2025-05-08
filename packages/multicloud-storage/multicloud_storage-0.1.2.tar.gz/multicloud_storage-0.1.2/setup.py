# setup.py
import setuptools
from pathlib import Path

# 1. 读取 requirements.txt，过滤掉空行和注释
here = Path(__file__).parent
req_txt = here / "requirements.txt"
install_requires = []
if req_txt.exists():
    for line in req_txt.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            install_requires.append(line)

# 2. 调用 setuptools.setup
setuptools.setup(
    name="multicloud-storage",              # pip install 时的包名
    version="0.1.2",
    description="统一操作 MinIO/OSS/S3 兼容存储的工具包",
    author="Your Name",
    author_email="you@example.com",
    url="https://github.com/your_username/multicloud-storage",
    packages=setuptools.find_packages(),     # 会找到 multicloud_storage/core, clients
    install_requires=install_requires,       # 动态从 requirements.txt 加载
    python_requires=">=3.6",
    # 内置 provider 的 entry_points
    entry_points={
        "multicloud_storage.providers": [
            # format: "name = module_path:ClassName"
            "minio = multicloud_storage.clients.minio_client:MinioClient",
            "oss = multicloud_storage.clients.oss_client_v2:OSSV2Client",
            "s3_compatible = multicloud_storage.clients.s3_compat_client:S3CompatClient",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
