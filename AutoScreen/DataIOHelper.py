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
        self.connection = psycopg2.connect(database="auto_screen_data",
                                           host="localhost",
                                           user="asp",
                                           password="asp_local_password_pg",
                                           port="9031")
        self.connection.autocommit = True

    def __del__(self):
        self.connection.close()

    def wechat_moment_stream_insert(self, wechat_moment_stream) -> int:
        sql = "INSERT INTO wechat_moment_stream(created_at, username, body_text, share_link_title, folded_text, picture_list, liked_users, comments, extra_text_clickable, extra_text_non_clickable) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING moment_stream_id;"
        with self.connection.cursor() as cur:
            # execute the INSERT statement
            cur.execute(sql, (wechat_moment_stream.create_time,
                              wechat_moment_stream.username,
                              wechat_moment_stream.body_text,
                              wechat_moment_stream.share_link_title,
                              wechat_moment_stream.folded_text,
                              wechat_moment_stream.picture_list,
                              wechat_moment_stream.liked_users,
                              wechat_moment_stream.comments,
                              wechat_moment_stream.extra_text_clickable,
                              wechat_moment_stream.extra_text_non_clickable,
                              ))

            # get the generated id back
            rows = cur.fetchone()
            if rows:
                moment_stream_id = rows[0]
                logging.info("wechat_moment_stream_insert succeeded, with moment_stream_id {moment_stream_id}")
                return moment_stream_id
            else:
                logging.warning("no moment_stream_id returned wechat_moment_stream_insert")

