[app]

# Izina rya app
title = Vidmore
package.name = vidmore
package.domain = org.vidmore

# main.py niyo izinjiramo
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Icon
icon.filename = %(source.dir)s/logo.png

# Version
version = 1.0.0

# Requirements
requirements = python3,kivy==2.3.0,kivymd==1.1.1,flask==2.3.3,requests==2.31.0,pytube==15.0.0,yt-dlp==2024.5.27,plyer

# Orientation
orientation = portrait

# Permissions zikenewe
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,POST_NOTIFICATIONS,WAKE_LOCK,FOREGROUND_SERVICE

# Android specific
fullscreen = 0
android.api = 33
android.minapi = 21
android.sdk = 31
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
android.logcat_filters = *:S python:D

[buildozer]
log_level = 2
warn_on_root = 1
