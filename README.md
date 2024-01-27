# AutoScreenPro
My private version of AutoScreen

## reference

- <https://github.com/mnotgod96/AppAgent/blob/ed8984634fb795826b7c95fb45af0707c73c989e/scripts/and_controller.py#L118>

## conda environments

```bash
conda create --name py312asp python=3.12
source activate py312asp

conda deactivate
conda remove -n py310asp --all
```


## pip environments

```bash
python -m pip install --upgrade pip
pip install pip-review jupyterlab seaborn scikit-image

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



