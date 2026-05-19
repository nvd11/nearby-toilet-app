Add-Type -AssemblyName System.Windows.Forms
Start-Sleep -Milliseconds 500
[System.Windows.Forms.SendKeys]::SendWait("^{v}")
