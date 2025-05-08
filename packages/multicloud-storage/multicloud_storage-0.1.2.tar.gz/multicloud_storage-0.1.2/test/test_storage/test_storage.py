from multicloud_storage.core.factory import create_storage_client
from multicloud_storage.core.providers import MINIO, OSS, S3_COMPATIBLE

# minio
# user: test test123456
# ak: LEzEOyqjn4k5Nymn
# sk: 8mGmYiDwjfKLpnSgSTxREIIo2q5VvAWy

"""
{
 "Version": "2012-10-17",
 "Statement": [
  {
   "Effect": "Allow",
   "Action": [
    "s3:GetBucketLocation",
    "s3:ListBucket"
   ],
   "Resource": [
    "arn:aws:s3:::test"
   ]
  },
  {
   "Effect": "Allow",
   "Action": [
    "s3:DeleteObject",
    "s3:GetObject",
    "s3:PutObject"
   ],
   "Resource": [
    "arn:aws:s3:::test/*"
   ]
  }
 ]
}
"""
# client = create_storage_client(
#     provider=MINIO,
#     storage_url="https://AK:SK@43.134.40.245:9000/test/videos/",
# )
# client.upload_file('local.txt', 'docs/report.txt')
# url = client.generate_presigned_url('docs/report.txt', expires_in=600)
# print(url)

# client = create_storage_client(
#     provider=MINIO,
#     endpoint="http://43.134.40.245:9000",  # 纯 host:port
#     access_key="LEzEOyqjn4k5Nymn",
#     secret_key="8mGmYiDwjfKLpnSgSTxREIIo2q5VvAWy",
#     bucket="test",
#     prefix="videos",
#     use_ssl=False,
# )

# minio
# endpoint: 43.134.40.245:9000
# ak: LEzEOyqjn4k5Nymn
# sk: 8mGmYiDwjfKLpnSgSTxREIIo2q5VvAWy
# bucket: test
# client = create_storage_client(
#     provider=MINIO,
#     storage_url="http://LEzEOyqjn4k5Nymn:8mGmYiDwjfKLpnSgSTxREIIo2q5VvAWy@43.134.40.245:9000/test/videos",
# )

# oss
# endpoint: oss-cn-beijing.aliyuncs.com
# ak: LTAI5tCCiqUKN4gPoEj318bN
# sk: p9UQG5sXkT3CXx1cKphoff9raBWzH3
# bucket: youtube-test001
# client = create_storage_client(
#     provider=OSS,
#     storage_url="https://LTAI5tCCiqUKN4gPoEj318bN:p9UQG5sXkT3CXx1cKphoff9raBWzH3@oss-cn-beijing.aliyuncs.com/youtube-test001/youtube/videos",
# )

# S3_COMPATIBLE to minio
# endpoint: 43.134.40.245:9000
# ak: LEzEOyqjn4k5Nymn
# sk: 8mGmYiDwjfKLpnSgSTxREIIo2q5VvAWy
# bucket: test
# client = create_storage_client(
#     provider=S3_COMPATIBLE,
#     storage_url="http://LEzEOyqjn4k5Nymn:8mGmYiDwjfKLpnSgSTxREIIo2q5VvAWy@43.134.40.245:9000/test/videos",
# )
# 上传成功，对应结果 result:  UploadResult(bucket='test', key='dXzrhQfzvhA_d26591dcd09b38c0079ffe960d6def12.mp4', full_key='videos/dXzrhQfzvhA_d26591dcd09b38c0079ffe960d6def12.mp4', etag='"8808f1be56a8669e99c5a58f7ae43d88"', url='http://43.134.40.245:9000/test/videos/dXzrhQfzvhA_d26591dcd09b38c0079ffe960d6def12.mp4')

# S3_COMPATIBLE to oss
# endpoint: oss-cn-beijing.aliyuncs.com （这里似乎加不加 s3.xx 都行）
# ak: LTAI5tCCiqUKN4gPoEj318bN
# sk: p9UQG5sXkT3CXx1cKphoff9raBWzH3
# bucket: youtube-test001
client = create_storage_client(
    provider=S3_COMPATIBLE,
    storage_url="https://LTAI5tCCiqUKN4gPoEj318bN:p9UQG5sXkT3CXx1cKphoff9raBWzH3@oss-cn-beijing.aliyuncs.com/youtube-test001/youtube/videos",
    use_ssl=False, # 经测试 oss 不支持 S3_COMPATIBLE https endpoint
)

# S3_COMPATIBLE to qiniu
# endpoint: s3.cn-east-1.qiniucs.com
# ak: 9cknYQjEXFCwI4sPlQ_J5pu_cL_FJlCHHDP9fHTI
# sk: t0l49cX5chc6ItAY1Jv_tVrWZs07zRXMrfvOlIrK
# bucket: youtube-test001
# client = create_storage_client(
#     provider=S3_COMPATIBLE,
#     storage_url="https://9cknYQjEXFCwI4sPlQ_J5pu_cL_FJlCHHDP9fHTI:t0l49cX5chc6ItAY1Jv_tVrWZs07zRXMrfvOlIrK@s3.cn-east-1.qiniucs.com/youtube-test001/youtube/videos",
# )
# # 七牛云 在不配置自定义域名时，只能用测试域名访问，同时，测试域名只支持 http
# client.public_domain = "http://svw7sznew.hd-bkt.clouddn.com"
# # 上传成功，对应结果 result:  UploadResult(bucket='youtube-test001', key='dXzrhQfzvhA_d26591dcd09b38c0079ffe960d6def12.mp4', full_key='youtube/videos/dXzrhQfzvhA_d26591dcd09b38c0079ffe960d6def12.mp4', etag='"8808f1be56a8669e99c5a58f7ae43d88"', url='http://svw7sznew.hd-bkt.clouddn.com/youtube/videos/dXzrhQfzvhA_d26591dcd09b38c0079ffe960d6def12.mp4')

# result = client.upload_file('local.txt', 'remote2.txt')
result = client.upload_file('dXzrhQfzvhA_d26591dcd09b38c0079ffe960d6def12.mp4', 'dXzrhQfzvhA_d26591dcd09b38c0079ffe960d6def12.mp4')
print("上传成功，对应结果 result: ", result)
# 上传成功，对应结果 result:  UploadResult(bucket='youtube-test001', key='dXzrhQfzvhA_d26591dcd09b38c0079ffe960d6def12.mp4', full_key='youtube/videos/dXzrhQfzvhA_d26591dcd09b38c0079ffe960d6def12.mp4', etag='"8808F1BE56A8669E99C5A58F7AE43D88"', url='http://youtube-test001.oss-cn-beijing.aliyuncs.com/youtube/videos/dXzrhQfzvhA_d26591dcd09b38c0079ffe960d6def12.mp4')
# 上传成功，对应结果 result:  UploadResult(bucket='youtube-test001', key='dXzrhQfzvhA_d26591dcd09b38c0079ffe960d6def12.mp4', full_key='youtube/videos/dXzrhQfzvhA_d26591dcd09b38c0079ffe960d6def12.mp4', etag='"8808f1be56a8669e99c5a58f7ae43d88"', url='http://svw7sznew.hd-bkt.clouddn.com/youtube/videos/dXzrhQfzvhA_d26591dcd09b38c0079ffe960d6def12.mp4')

# # 也可以拿到底层 SDK 客户端，自定义调用任何方法
# minio_client = client.raw_client
#
# # 获取 bucket
# bucket = minio_client.bucket
# # 获取 full key
# full_key = client.get_full_key("remote.txt")
# # 本地文件地址
# local_path = "./local.txt"

# # 对于 MinIO 原生 client ，直接调用原生方法：
# ObjectWriteResult = minio_client.fput_object(
#     bucket_name=bucket,
#     object_name=full_key,
#     file_path=local_path,
#     content_type="application/octet-stream",
# )

# print("ObjectWriteResult: ", ObjectWriteResult)


