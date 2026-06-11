Stop-Process -Name 'python' -Force
[Environment]::SetEnvironmentVariable("Glitchared_Puzzle", "True", "User")
Add-Type -AssemblyName PresentationFramework; [System.Windows.MessageBox]::Show('System Breach Detected, Congrats on hacking yourself >:D', 'Error', 'OK', 'Hand')