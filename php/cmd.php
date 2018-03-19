<?php



include "function.php";

function comRun($cmd)
{
	$shell = new COM("WScript.Shell");
	$shell->Run($cmd);
}




 $obj = new COM ( 'winmgmts://localhost/root/CIMV2' );
    $wmi_computersystem =     $obj->ExecQuery("Select * from Win32_ComputerSystem");
    $wmi_bios             =    $obj->ExecQuery("Select * from Win32_BIOS");
    foreach ( $wmi_computersystem as $wmi_call )
    {
        $model = $wmi_call->Model;
    }
    
    foreach ( $wmi_bios as $wmi_call )
    {
        $serial = $wmi_call->SerialNumber;
        $bios_version = $wmi_call->SMBIOSBIOSVersion;
    }
    br( "Bios version   : $bios_version<br>".
         "Serial number  : $serial<br>".
         "Hardware Model : $model<br>");
?>