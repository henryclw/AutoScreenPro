# AutoScreenPro
My private version of AutoScreen

## reference

- <https://github.com/mnotgod96/AppAgent/blob/main/scripts/and_controller.py#L118>

## jupyter notebook

```bash
jupyter lab
```

## conda environments

```bash
conda create --name py312asp python=3.12
source activate py312asp

conda deactivate
conda remove -n py310asp --all
```

## pip packages

```bash
python -m pip install --upgrade pip
pip install pip-review jupyterlab seaborn scikit-image opencv-python opencv-contrib-python pyshine

pip install -r requirements.txt
pip freeze > requirements.txt
pip list --format=freeze > requirements.txt
```

## scrcpy

```bash
scrcpy --disable-screensaver -w -S -t --power-off-on-close
```

## adb

```bash
# show touches
adb shell settings get system show_touches
adb shell settings put system show_touches 0
adb shell settings put system show_touches 1

# show pointer location
adb shell settings get system pointer_location
adb shell settings put system pointer_location 0
adb shell settings put system pointer_location 1

# show debug layout
adb shell getprop debug.layout
adb shell setprop debug.layout true && adb shell service call activity 1599295570
adb shell setprop debug.layout false && adb shell service call activity 1599295570
```

# docker data storage

```bash
docker compose -f "docker-compose.yml" -p "auto-screen-pro" up -d
docker compose -f "docker-compose.yml" -p "auto-screen-pro" down
````

## Postgresql

```postgresql
    CREATE TABLE IF NOT EXISTS wechat_moment_stream (
        moment_stream_id SERIAL PRIMARY KEY,
        created_at TIMESTAMP NOT NULL,
        username VARCHAR (32) NOT NULL,
        body_text TEXT,
        share_link_title TEXT,
        folded_text TEXT,
        picture_list TEXT[],
        liked_users TEXT[],
        comments TEXT[],
        extra_text_clickable TEXT[],
        extra_text_non_clickable TEXT[]
    );


INSERT INTO wechat_moment_stream(created_at, username, body_text, share_link_title, folded_text, picture_list, liked_users, comments, extra_text_clickable, extra_text_non_clickable)
    VALUES ('2022-10-10 11:30:30',
            '张三',
            '正文',
            '',
            '',
            '{"a.jpg", "b.jpg"}',
            '{"李四"}',
            '{}',
            '{}',
            '{"昨天"}'
            )
    RETURNING moment_stream_id;

SELECT * FROM wechat_moment_stream ORDER BY moment_stream_id DESC LIMIT 100;
```

