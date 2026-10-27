<#
.SYNOPSIS
    Ghost Record Artifact Generator for Student DFIR Labs
.DESCRIPTION
    Prompts the student for their 6+2 username, creates a simulated payload 
    with a Mark of the Web (Zone.Identifier) in their Downloads folder, 
    and immediately deletes it to create a textbook NTFS Ghost Record.
    Requires Administrator privileges.
#>

# Prompt the student for their unique 6+2 username
$studentID = Read-Host "Enter your UC 6+2 username (e.g., kucukkgl)"

if ([string]::IsNullOrWhiteSpace($studentID)) {
    Write-Host "[!] Error: You must enter a valid 6+2 username to proceed." -ForegroundColor Red
    exit
}

# Target the active user's Downloads directory
$labPath = "$env:USERPROFILE\Downloads"
Write-Host "`n[+] Staging Ghost Record artifact for user '$studentID' in: $labPath" -ForegroundColor Cyan

# Define the target ghost file path
$ghostFile = "$labPath\${studentID}_downloaded_payload.exe"

# Step 1: Create the dummy payload file in Downloads
Set-Content -Path $ghostFile -Value "MZ simulate malicious executable payload..."

# Step 2: Attach the Mark of the Web alternate data stream (ZoneId=3 indicates internet download)
$zoneIdContent = "[ZoneTransfer]`nZoneId=3"
Set-Content -Path "$ghostFile:Zone.Identifier" -Value $zoneIdContent

# Step 3: Delete the file immediately to flip InUse to False while preserving metadata (Ghost Record)
Remove-Item -Path $ghostFile
Write-Host "  -> Success! Created and deleted Ghost Record: ${studentID}_downloaded_payload.exe" -ForegroundColor Green

Write-Host "`n[+] Ready for RawCopy and MFTECmd extraction. Look for InUse = False and FileSize > 0 in Colab!" -ForegroundColor Cyan
