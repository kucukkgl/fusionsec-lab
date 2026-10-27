<#
.SYNOPSIS
    Interactive Manual Recycle Bin Lab for C:\Users\admin\Downloads
.DESCRIPTION
    Creates the payload with Mark of the Web, pauses indefinitely for 
    manual inspection and deletion to the Recycle Bin, then confirms the artifact state.
#>

$studentID = Read-Host "Enter your username/ID for the filename (e.g., goksel12345)"

if ([string]::IsNullOrWhiteSpace($studentID)) {
    Write-Host "[!] Error: You must enter a valid username to proceed." -ForegroundColor Red
    exit
}

$labPath = "C:\Users\admin\Downloads"

if (!(Test-Path $labPath)) {
    New-Item -ItemType Directory -Path $labPath | Out-Null
}

$ghostFile = "$labPath\${studentID}_downloaded_payload.exe"

# Step 1: Create the file & Mark of the Web
Write-Host "[+] Creating target file: $ghostFile" -ForegroundColor Cyan
Set-Content -Path $ghostFile -Value "MZ simulate malicious executable payload..."
Set-Content -Path "$ghostFile:Zone.Identifier" -Value "[ZoneTransfer]`nZoneId=3"

# Step 2: Interactive Prompt for Manual Recycle Bin Deletion
Write-Host "`n============================================================" -ForegroundColor Yellow
Write-Host " [INFO] File is ACTIVE on disk in: $labPath" -ForegroundColor Yellow
Write-Host " [INFO] Filename: ${studentID}_downloaded_payload.exe" -ForegroundColor Yellow
Write-Host "------------------------------------------------------------" -ForegroundColor Yellow
Write-Host " INSTRUCTIONS FOR STUDENTS:" -ForegroundColor Cyan
Write-Host " 1. Open File Explorer and navigate to C:\Users\admin\Downloads" -ForegroundColor White
Write-Host " 2. Inspect the file properties and Mark of the Web stream." -ForegroundColor White
Write-Host " 3. Select the file and press 'DELETE' to move it to the Recycle Bin." -ForegroundColor White
Write-Host "============================================================`n" -ForegroundColor Yellow

Read-Host "Press [Enter] ONLY AFTER you have manually deleted the file to the Recycle Bin"

# Step 3: Verify the action
if (!(Test-Path $ghostFile)) {
    Write-Host "`n[+] Success! File is no longer in Downloads (Successfully sent to Recycle Bin)." -ForegroundColor Green
    Write-Host "[+] Forensic Artifacts Created: C:\`$Recycle.Bin entries (`$R / `$I files) + MFT Ghost Record." -ForegroundColor Cyan
} else {
    Write-Host "`n[!] Warning: The file is still sitting in the Downloads folder!" -ForegroundColor Red
    Write-Host "[!] Make sure to select it and press Delete, then run this check again." -ForegroundColor Yellow
}
