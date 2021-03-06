# -*- mode: python -*-

block_cipher = None


a = Analysis(['../main.py',
			  '../aes128.py',
			  '../downloader.py'],
             pathex=['../'],
             binaries=[],
             datas=[('../icons', 'icons'),
                    ('../readme.pdf', '.'),
                    ('../.version', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='video_downloader',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='../icons/app.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='video_downloader')
