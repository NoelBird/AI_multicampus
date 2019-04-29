Get-Command
Get-Process
Get-Help Get-Process # Power Shell 주석
$env:PSModulePath
$env:ALLUSERSPROFILE
Connect-AzAccount
Import-Module Az.Accounts
Get-executionPolicy # PowerShell 스크립트 실행 정책(5가지 정도가 있음)
    # Restricted: 제한됨(*.ps1 파일)
    # Unrestricted
Set-ExecutionPolicy Unrestricted