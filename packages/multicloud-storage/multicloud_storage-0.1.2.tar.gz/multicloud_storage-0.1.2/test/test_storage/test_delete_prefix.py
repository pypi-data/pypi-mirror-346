import os
import tempfile
from multicloud_storage.core.factory import create_storage_client
from multicloud_storage.core.providers import S3_COMPATIBLE, MINIO, OSS


def main():
    # # —— 初始化客户端 ——
    # client = create_storage_client(
    #     provider=S3_COMPATIBLE,
    #     storage_url=(
    #         "http://LEzEOyqjn4k5Nymn:8mGmYiDwjfKLpnSgSTxREIIo2q5VvAWy"
    #         "@43.134.40.245:9000/test/videos"
    #     )
    # )

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
    client = create_storage_client(
        provider=MINIO,
        storage_url="http://LEzEOyqjn4k5Nymn:8mGmYiDwjfKLpnSgSTxREIIo2q5VvAWy@43.134.40.245:9000/test/videos",
    )
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
    # client = create_storage_client(
    #     provider=S3_COMPATIBLE,
    #     storage_url="https://LTAI5tCCiqUKN4gPoEj318bN:p9UQG5sXkT3CXx1cKphoff9raBWzH3@oss-cn-beijing.aliyuncs.com/youtube-test001/youtube/videos",
    # )

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

    # —— 在子目录 "to_delete/" 下创建三个临时文件上传 ——
    prefix = "to_delete"

    # for name in ("a.txt", "b.txt", "c.txt"):
    #     local_path = name
    #     with open(local_path, "w", encoding="utf-8") as f:
    #         f.write("this file will be deleted")
    #     # upload to e.g. to_delete/a.txt, to_delete/b.txt...
    #     client.upload_file(local_path, f"{prefix}/{name}")

    # —— 确认目录下确实有文件 ——
    page = client.list_objects(prefix=prefix, max_items=10)
    keys = [obj.key for obj in page.objects]
    print("Before delete_prefix:", keys)

    # —— 调用 delete_prefix ——
    client.delete_prefix(prefix)
    #
    # —— 再次列出，应为空 ——
    page2 = client.list_objects(prefix=prefix, max_items=10)
    print("After delete_prefix:", [obj.key for obj in page2.objects])
    # assert not page2.objects, "delete_prefix 未删除所有对象！"
    #
    # print("test_delete_prefix 完成！")

if __name__ == "__main__":
    main()
