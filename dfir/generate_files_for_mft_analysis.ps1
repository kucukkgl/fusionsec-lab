<#
.SYNOPSIS
    Ghost Record Generator for C:\Users\admin\Downloads
.DESCRIPTION
    Directly targets C:\Users\admin\Downloads, stages the payload 
    with Mark of the Web, pauses 30 seconds for manual inspection, and 
    deletes it to create an NTFS Ghost Record.
#>

$studentID = "goksel12345"
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

# Step 3: Informational Console Banner & 30-Second Countdown
Write-Host "`n============================================================" -ForegroundColor Yellow
Write-Host " [INFO] File is ACTIVE on disk in: $labPath" -ForegroundColor Yellow
Write-Host " [INFO] MFT State: InUse = True | Real Clusters Assigned" -ForegroundColor Yellow
Write-Host " [INFO] Open C:\Users\admin\Downloads to inspect the file!" -ForegroundColor Yellow
Write-Host "============================================================`n" -ForegroundColor Yellow

for ($i = 30; $i -gt 0; $i--) {
    Write-Host -NoNewline "`r[+] Deleting in $i seconds... (Check C:\Users\admin\Downloads) "
    Start-Sleep -Seconds 1
}
Write-Host ""

# Step 4: Delete to create the Ghost Record
Remove-Item -Path $ghostFile

Write-Host "`n[+] FILE DELETED!" -ForegroundColor Red
Write-Host "[+] MFT State Change: 'InUse' flipped to False, Clusters Released." -ForegroundColor Green
Write-Host "[+] It is now an NTFS Ghost Record! Ready for RawCopy extraction." -ForegroundColor Cyan
