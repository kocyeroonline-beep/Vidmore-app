[app]
title = Vidmore
package.name = vidmore
package.domain = org.vidmore
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
icon.filename = %(source.dir)s/logo.png
version = 1.0.0
requirements = python3,kivy==2.3.0,kivymd==1.1.1,flask==2.3.3,requests==2.31.0,pytube==15.0.0,yt-dlp==2024.5.27,plyer
orientation = portrait
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,POST_NOTIFICATIONS,WAKE_LOCK,FOREGROUND_SERVICE
fullscreen = 0

# API levels
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.build_tools_version = 33.0.2

# Architectures
android.archs = arm64-v8a,armeabi-v7a

# Log filter
android.logcat_filters = *:S python:D

# Artifact
android.release_artifact = apk  # 👈 gerageza APK mbere, nyuma uzakore AAB

[buildozer]
log_level = 2
warn_on_root = 1
