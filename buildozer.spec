[app]

title = Farm Bot
package.name = farmbot
package.domain = org.farmbot
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

requirements = kivy

orientation = portrait

osx.python_version = 3
osx.kivy_version = 2.1.0

fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 27
android.minapi = 21
android.accept_sdk_license = True

android.ndk_api = 21
android.allow_backup = True

log_level = 2
