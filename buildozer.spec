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
# CAREFUL: Ensure Pillow is with a capital P
requirements = python3,kivy,kivymd,opencv,numpy,Pillow

# (str) Supported orientations (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# =============================================================================
# Android specific
# =============================================================================

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = CAMERA, INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid any automatic updates that breaks things
android.skip_update = False

# (bool) If True, then automatically accept SDK licenses
# This is critical for GitHub Actions!
android.accept_sdk_license = True
# (list) The Android architectural targets to build for
android.archs = arm64-v8a
