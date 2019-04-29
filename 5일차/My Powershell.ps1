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

Get-AzSubscription

Select-AzSubscription -Subscription 5af612c4-4f84-45dd-9fc2-9346b62be41e

# ----------------AzureRM 으로 진행(교재에 수록되어 있는, 이것 또한 옛날 버전임)----------------------

Install-Module -Name AzureRM -AllowClobber # 모두 예

Connect-AzureRmAccount

Import-Module -Name AzureRM

Connect-AzureRmAccount

Get-AzureRmSubscription

Select-AzureRmSubscription 5af612c4-4f84-45dd-9fc2-9346b62be41e

