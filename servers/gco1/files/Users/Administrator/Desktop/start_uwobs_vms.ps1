# Filename start_uwobs_vms.ps1
# start_uwobs_vms.ps1 starts the uwobs virtual machines

function WaitForVM($vm){
Write-Host -NoNewline "Waiting for $vm ... "
do {Start-Sleep -milliseconds 100} 
    until ((Get-VMIntegrationService $vm | ?{$_.name -eq "Heartbeat"}).PrimaryStatusDescription -eq "OK")
Write-Host "OK"
}

function StartVMGroup([string[]]$vms)
{
   foreach ( $vm in $vms )
   {
      Write-Host "Starting $vm"
     Start-VM -name $vm -AsJob
   }
  foreach ( $vm in $vms )
   {
     WaitForVM($vm)
   }
}


StartVMGroup("gcoinstsrv01","gcoinstsrv02","gconode01")

Write-Host "Press any key to finish ..."
$x = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
