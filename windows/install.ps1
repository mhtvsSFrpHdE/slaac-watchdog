$ErrorActionPreference = "Stop"

# Ask user input
Function Get-FileName($initialDirectory)
{
    [System.Reflection.Assembly]::LoadWithPartialName("System.windows.forms") | Out-Null
    $OpenFileDialog = New-Object System.Windows.Forms.OpenFileDialog
    $OpenFileDialog.initialDirectory = $initialDirectory
    $OpenFileDialog.filter = "Python (*.exe)| *.exe*"
    $OpenFileDialog.ShowDialog() | Out-Null

    $folderResultObject = New-Object PsObject -Property @{success=$false ; result=""}
    if ($OpenFileDialog.filename.Length -gt 0) {
        $folderResultObject.success = $true
        $folderResultObject.result = $OpenFileDialog.filename
        return $folderResultObject
    }
    return $folderResultObject
}

$UriAndName = Read-Host "What is the task name?`n  Type nothing press Enter for default is `"SLAAC watchdog`"`nYour answer"
if ($UriAndName.Length -eq 0){
    $UriAndName = "SLAAC watchdog"
}
$UriAndName = "\$($UriAndName)"
$SubnetPrefixLength = Read-Host "IPv6 Subnet prefix length in router settings or from ISP.`n  Must type an integer number like:`n    64`nYour answer"
$InputValid = [int]::TryParse($SubnetPrefixLength, [ref]$SubnetPrefixLength)
if (-not $InputValid) {
    Read-Host "Invalid value`nPaused, press Enter to stop"
    Exit
}
ipconfig
$AdapterName = Read-Host "Which network adapter to monitor?`n  Find with `"ipconfig`" above `"adapter <Adapter Name>:`"`n  or Control Panel > Network and Internet`n  > Network and Sharing Center > Change adapter settings`n  > Rename this connection > Copy name`n  Must type name without quotes like:`n    Ethernet 1`nYour answer"
if ($AdapterName.Length -eq 0){
    Read-Host "Invalid value`nPaused, press Enter to stop"
    Exit
}
$PythonPath = Read-Host "Type nothing press Enter and select your `"python.exe`" in opened window.`n  Or you can paste it here without quotes like:`n    C:\Python\python.exe`nYour answer"
if ($PythonPath.Length -eq 0){
    $GetPythonPath = Get-FileName
    if ($GetPythonPath.success){
        $PythonPath = $GetPythonPath.result
    }
    else{
        Read-Host "Canceled`nPaused, press Enter to stop"
        Exit
    }
}
Write-Output "    $($PythonPath)"
$WorkingDirectory = (Get-Location).Path
Read-Host "Your install folder (working directory) will be:`n  `"$($WorkingDirectory)`"`nPress Enter to generate task scheduler xml file"

# Replace text
$taskXml = Get-Content ".\task_scheduler_template.xml" -Raw
$taskXml = $taskXml.Replace("///UriAndName///", $UriAndName)
$taskXml = $taskXml.Replace("///SubnetPrefixLength///", $SubnetPrefixLength)
$taskXml = $taskXml.Replace("///AdapterName///", $AdapterName)
$taskXml = $taskXml.Replace("///WorkingDirectory///", $WorkingDirectory)
$taskXml = $taskXml.Replace("///PythonPath///", $PythonPath)

$taskXml | Out-File "SLAAC watchdog.xml"
$taskXmlPath = "$($WorkingDirectory)\SLAAC watchdog.xml"
Set-Clipboard -Value $taskXmlPath
Read-Host "Press Enter to open Task Scheduler`n  Navigate to the folder you want to create the task`n  Import and choose and paste has copied to clipboard`n    `"$($taskXmlPath)`"`n  Check `"Run whether user is logged on or not`"`n    if you want to hide python window on launch`n  Right click on task and run manually once`nPress Enter to open Task Scheduler"

taskschd

Write-Host "It is now safe to turn off`nyour powershell window."
Read-Host
