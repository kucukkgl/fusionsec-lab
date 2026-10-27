<#
.SYNOPSIS
    Prompt-Based Ghost Record Generator for Downloads Folder
.DESCRIPTION
    Prompts for the username, targets C:\Users\<username>\Downloads, 
    stages the payload with Mark of the Web, pauses 30 seconds for manual 
    inspection, and deletes it to create an NTFS Ghost Record.
#>

# Prompt for the username (e.g., admin)
$studentID = Read-Host "Enter your username (e.g., admin)"

if ([string]::IsNullOrWhiteSpace($studentID)) {
    Write-Host "[!] Error: You must enter a valid username to proceed." -ForegroundColor Red
    exit
}

# Dynamically set the path using the prompted username
$labPath = "C:\Users\$studentID\Downloads"

if (!(Test-Path $labPath)) {
    Write-Host "[!] Warning: $labPath does not exist. Creating it now..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $labPath | Out-Null
}

$ghostFile = "$labPath\${studentID}_downloaded_payload.exe"

# Step 1: Create the file
Write-Host "[+] Creating target file: $ghostFile" -ForegroundColor Cyan
Set-Content -Path $ghostFile -Value "MZ simulate malicious executable payload..."

# Step 2: Attach Mark of the Web
Write-Host "[+] Attaching Mark of the Web (Zone.Identifier)..." -ForegroundColor Cyan
Set-Content -Path "$ghostFile:Zone.Identifier" -Value "[ZoneTransfer]`nZoneId=3"

# Step 3: Informational Console Banner & 30-Second Countdown
Write-Host "`n============================================================" -ForegroundColor Yellow
Write-Host " [INFO] File is ACTIVE on disk in: $labPath" -ForegroundColor Yellow
Write-Host " [INFO] MFT State: InUse = True | Real Clusters Assigned" -ForegroundColor Yellow
Write-Host " [INFO] Open C:\Users\$studentID\Downloads to inspect the file!" -ForegroundColor Yellow
Write-Host "============================================================`n" -ForegroundColor Yellow

for ($i = 30; $i -gt 0; $i--) {
    Write-Host -NoNewline "`r[+] Deleting in $i seconds... (Check Downloads folder)   "
    Start-Sleep -Seconds 1
}
Write-Host ""

# Step 4: Delete to create the Ghost Record
Remove-Item -Path $ghostFile

Write-Host "`n[+] FILE DELETED!" -ForegroundColor Red
Write-Host "[+] MFT State Change: 'InUse' flipped to False, Clusters Released." -ForegroundColor Green
Write-Host "[+] It is now an NTFS Ghost Record! Ready for RawCopy extraction." -ForegroundColor Cyan
