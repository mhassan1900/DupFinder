# -*- mode: python -*-
a = Analysis(['scripts/dupfinder'],
             pathex=['/Users/mahmud/program/pystuff/DupFinder'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='dupfinder_gui',
          debug=False,
          strip=None,
          upx=True,
          console=False )
app = BUNDLE(exe,
             name='dupfinder_gui.app',
             icon=None)
