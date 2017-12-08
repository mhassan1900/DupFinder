# -*- mode: python -*-
a = Analysis(['scripts/find_dupfiles.py'],
             pathex=['/Users/mahmud/program/pystuff/file_utils'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='setup',
          debug=False,
          strip=None,
          upx=True,
          console=False )
