import os
import tempfile
from multicloud_storage.core.factory import create_storage_client
from multicloud_storage.core.providers import S3_COMPATIBLE

def main():
    # 1. 初始化客户端（替换下面的 AK/SK、域名、bucket、prefix）
    # client = create_storage_client(
    #     provider=S3_COMPATIBLE,
    #     storage_url=(
    #         "https://YOUR_ACCESS_KEY:YOUR_SECRET_KEY"
    #         "@s3.cn-east-1.qiniucs.com"
    #         "/your-bucket/videos"
    #     ),
    #     # 如果你的文件已绑定自定义域名，可传入：
    #     # public_domain="cdn.your-domain.com"
    # )

    # minio
    # endpoint: 43.134.40.245:9000
    # ak: LEzEOyqjn4k5Nymn
    # sk: 8mGmYiDwjfKLpnSgSTxREIIo2q5VvAWy
    # bucket: test
    # prefix: videos
    # client = create_storage_client(
    #     provider=MINIO,
    #     storage_url="http://LEzEOyqjn4k5Nymn:8mGmYiDwjfKLpnSgSTxREIIo2q5VvAWy@43.134.40.245:9000/test/videos",
    # )
    # client = create_storage_client(
    #     provider=S3_COMPATIBLE,
    #     storage_url="http://LEzEOyqjn4k5Nymn:8mGmYiDwjfKLpnSgSTxREIIo2q5VvAWy@43.134.40.245:9000/test/videos",
    # )

    # oss
    # endpoint: oss-cn-beijing.aliyuncs.com （这里似乎加不加 s3.xx 都行）
    # ak: LTAI5tCCiqUKN4gPoEj318bN
    # sk: p9UQG5sXkT3CXx1cKphoff9raBWzH3
    # bucket: youtube-test001
    # prefix: youtube/videos
    # client = create_storage_client(
    #     provider=OSS,
    #     storage_url="https://LTAI5tCCiqUKN4gPoEj318bN:p9UQG5sXkT3CXx1cKphoff9raBWzH3@oss-cn-beijing.aliyuncs.com/youtube-test001/youtube/videos",
    # )
    client = create_storage_client(
        provider=S3_COMPATIBLE,
        storage_url="https://LTAI5tCCiqUKN4gPoEj318bN:p9UQG5sXkT3CXx1cKphoff9raBWzH3@oss-cn-beijing.aliyuncs.com/youtube-test001/youtube/videos",
    )

    # qiniu
    # endpoint: s3.cn-east-1.qiniucs.com
    # ak: 9cknYQjEXFCwI4sPlQ_J5pu_cL_FJlCHHDP9fHTI
    # sk: t0l49cX5chc6ItAY1Jv_tVrWZs07zRXMrfvOlIrK
    # bucket: youtube-test001
    # prefix: youtube/videos
    # client = create_storage_client(
    #     provider=S3_COMPATIBLE,
    #     storage_url="https://9cknYQjEXFCwI4sPlQ_J5pu_cL_FJlCHHDP9fHTI:t0l49cX5chc6ItAY1Jv_tVrWZs07zRXMrfvOlIrK@s3.cn-east-1.qiniucs.com/youtube-test001/youtube/videos",
    # )

    # # —— 准备一个本地测试文件 ——
    local_path = "tmp_exists_test.txt"
    # with open(local_path, "w", encoding="utf-8") as f:
    #     f.write("this file will be exists")
    #
    test_key = "to_be_exists.txt"
    #
    # # —— 1) 确认不存在时返回 None ——
    # result0 = client.exists(test_key)
    # print("Before upload, exists():", result0)
    # assert result0 is None, "对象已上传！"
    #
    # # —— 2) 上传文件 ——
    # print("上传测试文件...")
    # client.upload_file(local_path, test_key)
    #
    # —— 3) 确认存在时返回 UploadResult 并包含正确字段 ——
    result1 = client.exists(test_key)
    assert result1 is not None, "对象未上传！"
    print("result1: ", result1)

    #
    # # —— 4) 清理：先删存储，再删本地 ——
    # client.delete(test_key)
    # os.remove(local.name)
    #
    # print("test_exists 完成！")

if __name__ == "__main__":
    main()
