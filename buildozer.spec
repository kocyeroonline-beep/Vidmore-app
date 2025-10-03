[app]
# App info
title = Vidmore
package.name = vidmore
package.domain = org.vidmore
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
icon.filename = %(source.dir)s/logo.png
version = 1.0.0

# Requirements
requirements = python3,kivy==2.3.0,kivymd==1.1.1,flask==2.3.3,requests==2.31.0,pytube==15.0.0,yt-dlp==2024.5.27,plyer

# Android settings
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,POST_NOTIFICATIONS,WAKE_LOCK,FOREGROUND_SERVICE
android.api = 33
android.minapi = 21
android.sdk = 31
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
android.logcat_filters = *:S python:D

# Twashyizeho version ihuye na workflow (ntabwo izongera gufata 36.1.0)
android.build_tools_version = 31.0.0

# Artifact: APK gusa
android.release_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1
