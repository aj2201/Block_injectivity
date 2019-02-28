# -*- mode: python -*-

block_cipher = None


a = Analysis(['skin_calc_gui.py'],
             pathex=['C:\\Apps\\Aj\\Block_injectivity\\py_project'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Skin_Calc',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='SkinCalc_logo.ico')
