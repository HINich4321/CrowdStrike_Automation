$oldsensors_windowsservers = import-csv ("C:Path\windows_servers_results.csv") | ConvertTo-Html -Fragment

$recipients = @("recipients@email.com")
$sender = @(sender@email.com)

$mailBodyDataWorkstations = 
@"
Hello,</br></br>

This is the monthly report for old CrowdStrike sensors. The most up to date sensor is located (download path) </br></br>

$oldsensors_workstations</br>

"@

$mailBodyDataWindowsServers = 
@"
Hello,</br></br>

This is the monthly report for old CrowdStrike sensors. The most up to date sensor is located (download path) </br></br>

$oldsensors_windowsservers</br>

"@

$mailBodyDataLinuxServers = 
@"
Hello,</br></br>

This is the monthly report for old CrowdStrike sensors. The most up to date sensor is located (download path) </br></br>

$oldsensors_liunxservers</br>

"@

$mailBodyNoData = 
@"
Hello,</br></br>

No sensors are out of date </br></br>

"@

ForEach ($file in (Get-ChildItem "C:Path\workstations_results.csv")) {
    If ((Import-CSV $file).length -gt 0) {
        Send-MailMessage -From $sender -To $recipients -Subject 'Old CrowdStrike Sensors for Workstations - IT Security' -Body $mailBodyDataWorkstations -BodyAsHtml -Priority High -DeliveryNotificationOption OnSuccess, OnFailure -SmtpServer '0.0.0.0' -Encoding $([System.Text.Encoding]::UTF8)
    } else {
        Send-MailMessage -From $sender -To $sender -Subject 'Old CrowdStrike Sensors for Workstations - IT Security' -Body $mailBodyNoData -BodyAsHtml -Priority High -DeliveryNotificationOption OnSuccess, OnFailure -SmtpServer '0.0.0.0' -Encoding $([System.Text.Encoding]::UTF8)
    }
}
ForEach ($file in (Get-ChildItem "C:Path\linux_servers_results.csv")) {
    If ((Import-CSV $file).length -gt 0) {
        Send-MailMessage -From $sender -To $recipients -Subject 'Old CrowdStrike Sensors for Linux Servers - IT Security' -Body $mailBodyDataWindowsServers -BodyAsHtml -Priority High -DeliveryNotificationOption OnSuccess, OnFailure -SmtpServer '0.0.0.0' -Encoding $([System.Text.Encoding]::UTF8)
    } else {
        Send-MailMessage -From $sender -To $sender -Subject 'Old CrowdStrike Sensors for Linux Servers - IT Security' -Body $mailBodyNoData -BodyAsHtml -Priority High -DeliveryNotificationOption OnSuccess, OnFailure -SmtpServer '0.0.0.0' -Encoding $([System.Text.Encoding]::UTF8)
    }
}

ForEach ($file in (Get-ChildItem "C:Path\windows_servers_results.csv")) {
    If ((Import-CSV $file).length -gt 0) {
        Send-MailMessage -From $sender -To $recipients -Subject 'Old CrowdStrike Sensors for Windows Servers - IT Security' -Body $mailBodyDataLinuxServers -BodyAsHtml -Priority High -DeliveryNotificationOption OnSuccess, OnFailure -SmtpServer '0.0.0.0' -Encoding $([System.Text.Encoding]::UTF8)
    } else {
        Send-MailMessage -From $sender -To $sender -Subject 'Old CrowdStrike Sensors for Windows Servers - IT Security' -Body $mailBodyNoData -BodyAsHtml -Priority High -DeliveryNotificationOption OnSuccess, OnFailure -SmtpServer '0.0.0.0' -Encoding $([System.Text.Encoding]::UTF8)
    }
}
