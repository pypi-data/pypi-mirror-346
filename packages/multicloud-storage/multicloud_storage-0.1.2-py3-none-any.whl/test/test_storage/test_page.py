from multicloud_storage.core.factory import create_storage_client
from multicloud_storage.core.providers import MINIO, OSS, S3_COMPATIBLE

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
    client = create_storage_client(
        provider=S3_COMPATIBLE,
        storage_url="http://LEzEOyqjn4k5Nymn:8mGmYiDwjfKLpnSgSTxREIIo2q5VvAWy@43.134.40.245:9000/test/videos",
    )

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

    # 2. 首次调用 list_objects（不带 next_token）
    page = client.list_objects(
        prefix="",       # 相对于初始化时 prefix 的子路径
        max_items=1,     # 每页最多返回 5 条
        sort_by="last_modified",   # 可选: 'key'|'size'|'last_modified'|'etag'
        reverse=False    # 是否倒序
    )

    # 3. 处理并打印本页结果
    print(f"—— 第 1 页，共 {len(page.objects)} 条 ——")
    for obj in page.objects:
        print(f"- {obj.key:40s} | 大小: {obj.size:8d} 字节 | 最后修改: {obj.last_modified} | ETag: {obj.etag}")

    # 4. 如果还有下一页，就继续请求
    page_index = 2
    while page.next_token:
        page = client.list_objects(
            prefix="",
            max_items=1,
            next_token=page.next_token,
            sort_by="key",
            reverse=False
        )
        print(f"\n—— 第 {page_index} 页，共 {len(page.objects)} 条 ——")
        for obj in page.objects:
            print(f"- {obj.key:40s} | 大小: {obj.size:8d} 字节 | 最后修改: {obj.last_modified} | ETag: {obj.etag}")
        page_index += 1

    print("打印结束")

if __name__ == "__main__":
    main()