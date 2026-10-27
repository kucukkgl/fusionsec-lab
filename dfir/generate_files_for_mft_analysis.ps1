<#
.SYNOPSIS
    Manual Recycle Bin Ghost Record Generator for C:\Users\admin\Downloads
.DESCRIPTION
    Creates a payload with Mark of the Web in C:\Users\admin\Downloads using a custom username, 
    and pauses to let the student manually send the file to the Recycle Bin.
#>

# Prompt for the username to build the custom filename
$studentID = Read-Host "Enter your username/ID for the filename (e.g., goksel12345)"

if ([string]::IsNullOrWhiteSpace($studentID)) {
    Write-Host "[!] Error: You must enter a valid username to proceed." -ForegroundColor Red
    exit
}

# ALWAYS target the admin downloads folder
$labPath = "C:\Users\admin\Downloads"

if (!(Test-Path $labPath)) {
    New-Item -ItemType Directory -Path $labPath | Out-Null
}

$ghostFile = "$labPath\${studentID}_downloaded_payload.exe"

# Step 1: Create the file
Write-Host "[+] Creating target file: $ghostFile" -ForegroundColor Cyan
Set-Content -Path $ghostFile -Value "MZ simulate malicious executable payload..."

# Step 2: Attach Mark of the Web
Write-Host "[+] Attaching Mark of the Web (Zone.Identifier)..." -ForegroundColor Cyan
Set-Content -Path "$ghostFile:Zone.Identifier" -Value "[ZoneTransfer]`nZoneId=3"

# Step 3: Interactive Manual Recycle Bin Instructions
Write-Host "`n============================================================" -ForegroundColor Yellow
Write-Host " [INFO] File is ACTIVE on disk in: $labPath" -ForegroundColor Yellow
Write-Host " [INFO] Filename: ${studentID}_downloaded_payload.exe" -ForegroundColor Yellow
Write-Host " [ACTION REQUIRED] Open C:\Users\admin\Downloads right now!" -ForegroundColor Magenta
Write-Host " [ACTION REQUIRED] Select the file and press 'DELETE' (Recycle Bin)" -ForegroundColor Magenta
Write-Host "============================================================`n" -ForegroundColor Yellow

for ($i = 30; $i -gt 0; $i--) {
    # Check if the user already deleted it manually
    if (!(Test-Path $ghostFile)) {
        Write-Host "`n[+] Detected! File was manually sent to the Recycle Bin by user." -ForegroundColor Green
        break
    }
    Write-Host -NoNewline "`r[+] Waiting for manual deletion... Time remaining: ${i}s   "
    Start-Sleep -Seconds 1
}

# Fallback if timer runs out and file is still there
if (Test-Path $ghostFile) {
    Write-Host "`n[!] Timer expired. Force-deleting file to complete script execution." -ForegroundColor Yellow
    Remove-Item -Path $ghostFile
}

Write-Host "`n[+] Lab Phase Complete!" -ForegroundColor Cyan
Write-Host "[+] Forensic State: File transitioned via Recycle Bin ($R / $I files created + MFT Ghost Record)." -ForegroundColor Green
