@echo off
setlocal

REM ========== Args ==========
REM Usage: build-and-push.bat [--tag TAG]
set IMAGE_NAME=dvlyadmin-mini
set REGISTRY=registry.cn-beijing.aliyuncs.com
set NAMESPACE=django-vue-lyadmin
set REPO_NAME=dvlyadmin-mini
set TAG=latest

:parse_args
if "%~1"=="" goto args_done
if "%~1"=="--tag" (
    set TAG=%~2
    shift & shift
    goto parse_args
)
echo Unknown arg: %~1
echo Usage: build-and-push.bat [--tag TAG]
exit /b 1
:args_done

set FULL_IMAGE=%REGISTRY%/%NAMESPACE%/%REPO_NAME%:%TAG%
set BUILD_ARGS=

echo ========================================
echo   SafeTest Docker Build ^& Push
echo   Tag:   %TAG%
echo ========================================
echo.

echo [1/3] Building image...
docker build -t %IMAGE_NAME% %BUILD_ARGS% -f Dockerfile .
if %errorlevel% neq 0 (
    echo Build FAILED!
    pause
    exit /b 1
)
echo Build done.
echo.

echo [2/3] Tagging image...
for /f "tokens=*" %%i in ('docker images -q %IMAGE_NAME%') do set IMAGE_ID=%%i
echo Image ID: %IMAGE_ID%
docker tag %IMAGE_ID% %FULL_IMAGE%
if %errorlevel% neq 0 (
    echo Tag FAILED!
    pause
    exit /b 1
)
echo Tagged: %FULL_IMAGE%
echo.

echo [3/3] Pushing image...
docker push %FULL_IMAGE%
if %errorlevel% neq 0 (
    echo Push FAILED! Please login first:
    echo   docker login %REGISTRY%
    pause
    exit /b 1
)
echo.
echo ========================================
echo   Push SUCCESS: %FULL_IMAGE%
echo ========================================
pause
