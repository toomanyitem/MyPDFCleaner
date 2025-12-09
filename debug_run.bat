@echo off
echo Starting MyPDFCleaner in DEBUG MODE...
echo Logs are being written to "startup_log.txt".
echo If the window closes, please check "startup_log.txt" for errors.

REM Run run.bat and capture ALL output (stdout and stderr) to startup_log.txt
call run.bat > startup_log.txt 2>&1

echo.
echo ========================================
echo Execution finished.
echo If the program didn't start, open "startup_log.txt" to see why.
echo ========================================
pause
