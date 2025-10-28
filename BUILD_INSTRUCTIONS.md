Packaging the game into a single executable (Windows)

Overview
- This project uses Python + pygame. The recommended packager is PyInstaller.
- I added `build_windows.ps1` which runs PyInstaller and bundles asset folders (`tai_nguyen`, `tai_lieu`).
- Two modes:
  - OneFile (single .exe): convenient but larger and sometimes flagged by antivirus.
  - OneDir (folder): more reliable for games with many assets.

Quick steps (PowerShell)
1. Open PowerShell in the project root (where `build_windows.ps1` is located).
2. (Optional) Create/activate a virtual environment:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

3. Run the build script (OneFile):

```powershell
.\build_windows.ps1
```

For a folder build (safer):

```powershell
.\build_windows.ps1 -OneFile:$false
```

4. After success, the executable (or folder) will be in `dist\ma_nguon\` (OneDir) or `dist\ma_nguon.exe` (OneFile).

Notes & troubleshooting
- PyInstaller must be installed. The script installs it automatically if missing.
- The script includes `tai_nguyen` and `tai_lieu` as data. If your game uses other assets, add them in `build_windows.ps1` `adds` array.
- Save files (`du_lieu/save/`) are user data and should NOT be bundled as tracked files in git. Consider adding `du_lieu/save/` to `.gitignore`.
- Single-file executables extract to a temp folder at runtime (sys._MEIPASS). Most relative paths work, but if you see missing asset errors, try `--onedir` mode.
- Antivirus/Windows SmartScreen: unsigned executables can be blocked. For distribution to other PCs, consider creating an installer (NSIS) and signing the executable.

Want me to build now?
- I can run the build on your machine (it will install PyInstaller if needed) and produce the exe here. Do you want me to run the OneFile build now, or prefer OneDir?
- If you want me to produce an installer (NSIS) or add a desktop shortcut/icon, tell me which icon file to use.