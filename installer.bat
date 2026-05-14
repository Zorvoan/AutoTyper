@echo off
title OCR AutoTyper -- Installer
chcp 65001 >nul

echo.
echo.
echo      █████╗ ██╗   ██╗████████╗ ██████╗ ████████╗██╗   ██╗██████╗ ███████╗██████╗
echo     ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗╚══██╔══╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
echo     ███████║██║   ██║   ██║   ██║   ██║   ██║    ╚████╔╝ ██████╔╝█████╗  ██████╔╝
echo     ██╔══██║██║   ██║   ██║   ██║   ██║   ██║     ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗
echo     ██║  ██║╚██████╔╝   ██║   ╚██████╔╝   ██║      ██║   ██║     ███████╗██║  ██║
echo     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝    ╚═╝      ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝
echo.
echo             OCR AutoTyper  -  Automaticky instalator  -  v1.0
echo.
echo     ══════════════════════════════════════════════════════════════════
echo.

:: ── Python check ─────────────────────────────────────────────────────────────
echo   [*] Kontroluji instalaci Pythonu...

set PYTHON_CMD=

python --version >nul 2>&1
if not errorlevel 1 ( set PYTHON_CMD=python & goto python_found )

python3 --version >nul 2>&1
if not errorlevel 1 ( set PYTHON_CMD=python3 & goto python_found )

py --version >nul 2>&1
if not errorlevel 1 ( set PYTHON_CMD=py & goto python_found )

echo.
echo   [!] Python nenalezen. Nainstaluj Python 3.10+ z python.org
echo       a ujisti se ze je zatrzena moznost "Add Python to PATH".
echo.
pause
exit /b 1

:python_found
echo   [+] Python nalezen (prikaz: %PYTHON_CMD%).
echo.

:: ── pip upgrade ───────────────────────────────────────────────────────────────
echo   [*] Aktualizuji pip...
%PYTHON_CMD% -m pip install --upgrade pip --quiet
echo   [+] pip OK
echo.

:: ── Python libraries ──────────────────────────────────────────────────────────
echo     ══════════════════════════════════════════════════════════════════
echo       INSTALACE PYTHON KNIHOVEN
echo     ══════════════════════════════════════════════════════════════════
echo.

echo   [*] Instaluji customtkinter...
%PYTHON_CMD% -m pip install customtkinter --quiet
echo   [+] OK
echo.

echo   [*] Instaluji Pillow...
%PYTHON_CMD% -m pip install pillow --quiet
echo   [+] OK
echo.

echo   [*] Instaluji pytesseract...
%PYTHON_CMD% -m pip install pytesseract --quiet
echo   [+] OK
echo.

echo   [*] Instaluji pynput...
%PYTHON_CMD% -m pip install pynput --quiet
echo   [+] OK
echo.

echo   [*] Instaluji pyinstaller...
%PYTHON_CMD% -m pip install pyinstaller --quiet
echo   [+] OK
echo.

:: ── Tesseract OCR ─────────────────────────────────────────────────────────────
echo     ══════════════════════════════════════════════════════════════════
echo       INSTALACE TESSERACT OCR
echo     ══════════════════════════════════════════════════════════════════
echo.
echo   [*] Stahuji Tesseract OCR... (muze trvat dele)
echo.

winget install UB-Mannheim.TesseractOCR --accept-package-agreements --accept-source-agreements

echo.

:: ── Build EXE ─────────────────────────────────────────────────────────────────
echo     ══════════════════════════════════════════════════════════════════
echo       SESTAVENI EXE
echo     ══════════════════════════════════════════════════════════════════
echo.
echo   [*] Sestavuji AutoTyper.exe na pozadi...
echo.

start /b "" %PYTHON_CMD% -m PyInstaller --onefile --windowed --name "AutoTyper" --icon "icon.ico" --add-data "icon.ico;." Autotyper.py > build_log.txt 2>&1

set /a i=0
:progress_loop
    timeout /t 1 >nul 2>&1

    tasklist /fi "imagename eq pyinstaller.exe" 2>nul | find /i "pyinstaller.exe" >nul 2>&1
    if errorlevel 1 (
        tasklist /fi "imagename eq python.exe" 2>nul | find /i "python.exe" >nul 2>&1
        if errorlevel 1 goto progress_done
        if exist "dist\AutoTyper.exe" goto progress_done
    )

    set /a i+=1
    set /a blocks=i/2
    if %blocks% gtr 30 set blocks=30

    set bar=
    set /a j=0
    :build_bar
        if %j% geq %blocks% goto end_bar
        set bar=%bar%█
        set /a j+=1
        goto build_bar
    :end_bar

    set empty=
    set /a k=%blocks%
    :build_empty
        if %k% geq 30 goto end_empty
        set empty=%empty%░
        set /a k+=1
        goto build_empty
    :end_empty

    <nul set /p ="   [%bar%%empty%] sestavuji...   "
    echo.

goto progress_loop

:progress_done
timeout /t 2 >nul 2>&1

echo   [████████████████████████████████] hotovo!
echo.

if not exist "dist\AutoTyper.exe" (
    echo   [!] Sestaveni selhalo. Zkontroluj build_log.txt pro detaily.
    echo       Zkontroluj ze je Autotyper.py ve stejne slozce jako installer.bat
    echo.
    pause
    exit /b 1
)

if exist build_log.txt del build_log.txt

echo.
echo     ══════════════════════════════════════════════════════════════════
echo.
echo   [+] Hotovo!
echo.
echo   AutoTyper.exe najdes ve slozce:  dist\AutoTyper.exe
echo.
echo     ══════════════════════════════════════════════════════════════════
echo.

pause
