# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['MP4Transcriber.py'],
    pathex=[],
    binaries=[('E:\\IT\\Other\\Apps\\MP4 Transcriber\\ffmpeg.exe', 'ffmpeg.exe'), ('E:\\IT\\Other\\Apps\\MP4 Transcriber\\ffprobe.exe', 'ffprobe.exe')],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MP4Transcriber',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.png'],
)
