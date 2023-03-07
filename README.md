# AutoScreenPro
My private version of AutoScreen

## reference

- <https://github.com/Desperationis/humdroid/blob/main/humdroid/wrappers/ScrcpyWrapper.py>
- <https://github.com/leng-yue/py-scrcpy-client>
- <https://huggingface.co/spaces/PaddlePaddle/UIE-X>
- <https://huggingface.co/spaces/PaddlePaddle/ERNIE-Layout>
- <https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html>
- <https://github.com/Layout-Parser/layout-parser>
- <https://github.com/PaddlePaddle/PaddleOCR>
- <https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/ppstructure/layout/README.md>
- <https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_en/quickstart_en.md>



## pip environments

```bash
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



