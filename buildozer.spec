[app]

# (string) Title of your application
title = Food Scale App

# (string) Package name
package.name = foodscaleapp

# (string) Package domain (needed for android packaging)
package.domain = org.test

# (string) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (string) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# Фиксируем стабильный Python 3.11 для сборки opencv и numpy
requirements = python3==3.11,kivy,kivymd,opencv,numpy,Pillow

# (str) Supported orientations (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# =============================================================================
# Android specific
# =============================================================================

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = CAMERA, INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API required for numpy
android.minapi = 24

# (str) Android NDK version to use
# Версия 23b гарантирует стабильную сборку С++ библиотек
android.ndk = 23b

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = True

# (bool) If True, then automatically accept SDK licenses
android.accept_sdk_license = True

# (list) The Android architectural targets to build for
# Собираем только под современную 64-битную архитектуру для экономии памяти
android.archs = arm64-v8a

# (int) Number of cores to use when building the NDK
android.ndk_cores = 1
