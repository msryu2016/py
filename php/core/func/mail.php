<?
/*
$smtpServer = 'smtp.worksmobile.com';
$port= '587';
$timeout = '3000';
$auth = '1';
$username = 'msryu@hackerslab.or.kr';
$password='gozjtmfoq1!';
$from='msryu@hackerslab.or.kr';
$namefrom='from';
$to='msryu@hackerslab.or.kr';
$nameto='to';
$subject='hihi';
$message='msg';

$a = authSendEmail($smtpServer,$port,$timeout ,$auth,$username,$password ,$from, $namefrom, $to, $nameto, $subject, $message);

pre($a);
*/
function authSendEmail($smtpServer,$port,$timeout ,$auth,$username,$password ,$from, $namefrom, $to, $nameto, $subject, $message)
{
//SMTP + SERVER DETAILS
/* * * * CONFIGURATION START * * * */
 
$localhost = "localhost";
$newLine = "\r\n";
/* * * * CONFIGURATION END * * * * */
 $output = '';
//Connect to the host on the specified port
$smtpConnect = fsockopen($smtpServer, $port, $errno, $errstr, $timeout);
$smtpResponse = fgets($smtpConnect, 515);
if(empty($smtpConnect))
{
	$output = "Failed to connect: $smtpResponse";
	return $output;
}
else
{
	$logArray['connection'] = "Connected: $smtpResponse";
}
if ($auth)
{
//Request Auth Login
fputs($smtpConnect,"AUTH LOGIN" . $newLine);
$smtpResponse = fgets($smtpConnect, 515);
$output = $output ."$smtpResponse";
 
//Send username
fputs($smtpConnect, base64_encode($username) . $newLine);
$smtpResponse = fgets($smtpConnect, 515);
$output = $output . "$smtpResponse";
 
//Send password
fputs($smtpConnect, base64_encode($password) . $newLine);
$smtpResponse = fgets($smtpConnect, 515);
$output = $output . "$smtpResponse";
}
//Say Hello to SMTP
fputs($smtpConnect, "HELO $localhost" . $newLine);
$smtpResponse = fgets($smtpConnect, 515);
$output = $output ."$smtpResponse";
 
//Email From
fputs($smtpConnect, "MAIL FROM: $from" . $newLine);
$smtpResponse = fgets($smtpConnect, 515);
$output = $output . "$smtpResponse";
 
//Email To
fputs($smtpConnect, "RCPT TO: $to" . $newLine);
$smtpResponse = fgets($smtpConnect, 515);
$output = $output ."$smtpResponse";
 
//The Email
fputs($smtpConnect, "DATA" . $newLine);
$smtpResponse = fgets($smtpConnect, 515);
$output = $output . "$smtpResponse";
 
//Construct Headers
$headers = "MIME-Version: 1.0" . $newLine;
$headers .= "Content-type: text/html; charset=iso-8859-1" . $newLine;
$headers .= "To: $nameto &lt;$to&gt;" . $newLine;
$headers .= "From: $namefrom &lt;$from&gt;" . $newLine;
 
fputs($smtpConnect, "To: $to\nFrom: $from\nSubject: $subject\n$headers\n\n$message\n.\n");
$smtpResponse = fgets($smtpConnect, 515);
$output = $output . "$smtpResponse";
 
// Say Bye to SMTP
fputs($smtpConnect,"QUIT" . $newLine);
$smtpResponse = fgets($smtpConnect, 515);
$output = $output ."$smtpResponse";
 
return $output;
}

?>