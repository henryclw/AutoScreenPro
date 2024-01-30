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

## docker data storage

```bash
docker compose -f "docker-compose.yml" -p "auto-screen-pro" up -d
docker compose -f "docker-compose.yml" -p "auto-screen-pro" down
``

