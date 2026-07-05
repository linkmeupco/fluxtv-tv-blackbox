@echo off
set GRADLE_VERSION=8.6
set GRADLE_HOME=%USERPROFILE%\.gradle\wrapper\dists\gradle-%GRADLE_VERSION%-bin\gradle-%GRADLE_VERSION%
set GRADLE_EXEC=%GRADLE_HOME%\bin\gradle.bat

if not exist "%GRADLE_EXEC%" (
    echo Downloading Gradle %GRADLE_VERSION%...
    powershell -Command "Invoke-WebRequest -Uri 'https://services.gradle.org/distributions/gradle-%GRADLE_VERSION%-bin.zip' -OutFile '%TEMP%\gradle.zip'"
    powershell -Command "Expand-Archive '%TEMP%\gradle.zip' -DestinationPath '%USERPROFILE%\.gradle\wrapper\dists\gradle-%GRADLE_VERSION%-bin' -Force"
    del "%TEMP%\gradle.zip"
)

call "%GRADLE_EXEC%" %*
