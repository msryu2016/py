<?php


error_log("hihi");



//file_write($file, print_r($_GET,true));



logging( print_r($_GET,true));
$file = sprintf("C:\\xampp\\php\\tmp\\lg_%s.log", date('Ymd', time()));
echo nl2br(file_read($file));


?>