<#
.SYNOPSIS
    Automated NTFS Artifact & Size Scenario Generator for Lab Training
.DESCRIPTION
    Creates resident, staged, deleted (ghost), and slack-space test artifacts
    using the 'kucukkgl' naming convention. Requires Administrator privileges.
#>

# Ensure directory exists
$labPath = "C:\suspicious"
if (!(Test-Path $labPath)) {
    New-Item -ItemType Directory -Path $labPath | Out-Null
    Write-Host "[+] Created directory: $labPath" -ForegroundColor Green
}

Write-Host "`n[+] Generating kucukkgl NTFS Lab Artifacts..." -ForegroundColor Cyan

# 1. Resident File (Fits entirely inside MFT record, tiny size)
$residentFile = "$labPath\kucukkgl_resident.txt"
Set-Content -Path $residentFile -Value "CTF{kucukkgl_resident_mft_data_stream}"
Write-Host "  -> Created Resident File: $residentFile"

# 2. Staged Artifact / Placeholder (Allocated clusters via fsutil with 0 bytes real size)
$stagedFile = "$labPath\kucukkgl_staged.tmp"
if (Test-Path $stagedFile) { Remove-Item $stagedFile }
fsutil file createnew $stagedFile 4096 | Out-Null
Write-Host "  -> Created Staged Artifact (4096 allocated, 0 real): $stagedFile"

# 3. Ghost Record / Deleted File (Creates file with data, then deletes it -> InUse: False)
$deletedFile = "$labPath\kucukkgl_deleted.log"
Set-Content -Path $deletedFile -Value "Sensitive investigation log data for user kucukkgl..."
Remove-Item -Path $deletedFile
Write-Host "  -> Created Ghost Record (Created & Deleted): $deletedFile"

# 4. Slack Space Demo File (Real size 3200 bytes inside a 4096 byte cluster)
$slackFile = "$labPath\kucukkgl_slack.txt"
"A" * 3200 | Set-Content -Path $slackFile
Write-Host "  -> Created Slack Space File (3200 bytes real / 1 cluster): $slackFile"

# 5. Timestomped Executable (Simulate our earlier executable test)
$exeFile = "$labPath\kucukkgl_it3072.exe"
[System.IO.File]::WriteAllText($exeFile, "MZ")
$oldDate = Get-Date "2010-01-01 12:00:00"
[System.IO.File]::SetCreationTime($exeFile, $oldDate)
[System.IO.File]::SetLastWriteTime($exeFile, $oldDate)
Write-Host "  -> Created Timestomped Executable ($SI backdated to 2010): $exeFile"

Write-Host "`n[+] Lab environment successfully staged! Ready for RawCopy and MFTECmd extraction." -ForegroundColor Green
