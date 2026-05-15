param([string]$path)
Stop-Process -Name 'python' -Force
$data = Get-Content -Path $path -Raw | ConvertFrom-Json
$data.Stats.Glitchared = 1
$data | ConvertTo-Json -Depth 100 | Set-Content -Path $path
Add-Type -AssemblyName PresentationFramework; [System.Windows.MessageBox]::Show('System Breach Detected, Congrats on hacking yourself >:D', 'Error', 'OK', 'Hand')