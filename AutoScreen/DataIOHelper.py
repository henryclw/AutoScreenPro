import logging
import psycopg2

from minio import Minio


class MinioHelper:
    def __init__(self, bucket_name: str):
        self.client = Minio("localhost:9032",
                            access_key="sMlA7Mz30vq1U8PigRlI",
                            secret_key="XHZEXJYIsDp5FaXqKNqfLTBYLf2H5IhRIpHAByPk",
                            secure=False
                            )
        # self.bucket_name = "asp.wechat.moment.stream"
        self.bucket_name = bucket_name

    def put_object(self, source_file_path, destination_file_name: str = None):
        if destination_file_name is None:
            destination_file_name = source_file_path.split('/')[-1]
        logging.info(f"minio put object {source_file_path} into {self.bucket_name}")
        self.client.fput_object(self.bucket_name, destination_file_name, source_file_path)


class PostgresqlHelper:
    def __init__(self):
        self.conn = psycopg2.connect(database="auto_screen_data",
                                     host="localhost",
                                     user="asp",
                                     password="asp_local_password_pg",
                                     port="9031")

