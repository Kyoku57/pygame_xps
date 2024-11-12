# -*- mode: python ; coding: utf-8 -*-

video_data = [
    ('assets/*.mp4', 'assets'),
    ('cache/*.wav', 'cache')
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=video_data,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

splash = Splash('splash.png',
                binaries=a.binaries,
                datas=a.datas,
                text_pos=(30, 240),
                text_size=16,
                max_img_size=(800, 800),
                text_color='white')

exe = EXE(
    pyz,
    a.scripts,
    splash,
    splash.binaries,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)