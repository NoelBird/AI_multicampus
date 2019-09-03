Add-AzureRmAccount # 단일 구독의 경우

# 구독이 여러개인 경우에는
# Get-AzureRmSubscription
# Set-AzureRmContext -SubscriptionId <subscription-id>
# 와 같이 입력해줘야 한다.

# 리소스 그룹 만들기
$rg = New-AzureRMResourceGroup -Name '20533E0204-LabRG' -Location 'East US'

# vnet 만들기
$vnet = New-AzureRmVirtualNetwork -ResourceGroupName $rg.ResourceGroupName -Name '20533E0204-vnet' -AddressPrefix '10.11.0.0/16' -Location $rg.Location

# Virtual Network subnet 설정
Add-AzureRmVirtualNetworkSubnetConfig -Name 'Subnet1' -VirtualNetwork $vnet -AddressPrefix '10.11.0.0/24'

# virtual network 설정 업데이트 하기
Set-AzureRmVirtualNetwork -VirtualNetwork $vnet