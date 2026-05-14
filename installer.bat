@echo off
title OCR AutoTyper Installer

echo ==============================
echo Instalace knihoven...
echo ==============================

pip install customtkinter pillow pytesseract pynput

echo.
echo ==============================
echo Instalace Tesseract OCR...
echo ==============================

winget install UB-Mannheim.TesseractOCR

echo.
echo Hotovo!
pause