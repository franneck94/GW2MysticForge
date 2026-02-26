@echo off
echo ========================================
echo Building Mystic Forge Executable
echo ========================================
echo.

:: Set the project name and entry point
set PROJECT_NAME=mystic_forge
set ENTRY_POINT=mystic_forge\__init__.py

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again.
    pause
    exit /b 1
)

echo Python found:
python --version

:: Check if PyInstaller is installed, install if not
echo.
echo Checking PyInstaller installation...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
    echo PyInstaller installed successfully.
) else (
    echo PyInstaller is already installed.
)

:: Install project dependencies
echo.
echo Installing project dependencies...
python -m pip install pyautogui
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

:: Create dist directory if it doesn't exist
if not exist "dist" mkdir dist

:: Clean previous builds
echo.
echo Cleaning previous builds...
if exist "build" (
    rmdir /s /q build
    echo Previous build directory removed.
)
if exist "dist\%PROJECT_NAME%.exe" (
    del "dist\%PROJECT_NAME%.exe"
    echo Previous executable removed.
)
if exist "%PROJECT_NAME%.spec" (
    del "%PROJECT_NAME%.spec"
    echo Previous spec file removed.
)

:: Build the executable
echo.
echo Building executable...
echo Command: pyinstaller --onefile --name=%PROJECT_NAME% --distpath=dist --workpath=build %ENTRY_POINT%
pyinstaller ^
    --onefile ^
    --name=%PROJECT_NAME% ^
    --distpath=dist ^
    --workpath=build ^
    --noconsole ^
    --icon=NONE ^
    %ENTRY_POINT%

:: Check if build was successful
if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    echo Please check the output above for errors.
    pause
    exit /b 1
)

:: Verify the executable was created
if exist "dist\%PROJECT_NAME%.exe" (
    echo.
    echo ========================================
    echo BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo Executable created: dist\%PROJECT_NAME%.exe
    echo File size:
    for %%i in ("dist\%PROJECT_NAME%.exe") do echo %%~zi bytes
    echo.
    echo Usage: %PROJECT_NAME%.exe -n ^<number_of_iterations^>
    echo Example: %PROJECT_NAME%.exe -n 10
    echo.

    :: Optional: Test the executable
    choice /c YN /m "Do you want to test the executable (will show help message)"
    if errorlevel 2 goto :skip_test
    if errorlevel 1 (
        echo.
        echo Testing executable...
        "dist\%PROJECT_NAME%.exe" --help
    )
    :skip_test

) else (
    echo.
    echo ERROR: Executable not found in dist directory!
    echo Build may have failed silently.
    pause
    exit /b 1
)

:: Optional cleanup
echo.
choice /c YN /m "Do you want to clean up build files (keeps only the .exe)"
if errorlevel 2 goto :skip_cleanup
if errorlevel 1 (
    if exist "build" rmdir /s /q build
    if exist "%PROJECT_NAME%.spec" del "%PROJECT_NAME%.spec"
    echo Cleanup completed.
)
:skip_cleanup

echo.
echo Build process completed!
echo Your executable is ready at: dist\%PROJECT_NAME%.exe
pause
