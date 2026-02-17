Write-Host "Stopping old version..." -ForegroundColor Yellow
Stop-Process -Name python* -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

Write-Host "Starting new version..." -ForegroundColor Green
Start-Process "wscript.exe" -ArgumentList "C:\AlwaysOnTopToggle\start_hidden.vbs" -WindowStyle Hidden
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "Program is running!" -ForegroundColor Green
Write-Host "NEW: Border turns GREEN when window is pinned!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening Notepad for testing..."
Start-Process notepad.exe

Write-Host ""
Write-Host "Try: Middle-click on the X button"
Write-Host "The border will turn GREEN!"
