<?php

include 'function.php';


$m =  localDB();
prt();

pre($m);

//exe('c:\\windows\\system32\\notepad.exe');
//run('start /b c:\windows\system32\notepad.exe');



	/*//url ÆÄ½Ì    
    $url = "http://localhost/dcg/tmp/test.php";
echo '<pre>';
$d = array('abc'=>'def');
	$read = sendReq($url, $d,'GET');

	echo $read;
*/

 $ini_array=getini("user.ini"); 

 pre($ini_array);
?>

<script type="text/javascript" src="jquery-3.1.1.js"></script>
<script type="text/javascript">
<!--
	

	$(function() {
alert(1);

	});
//-->
</script>