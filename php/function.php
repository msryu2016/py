<?php

error_reporting(-1);
ini_set('display_errors', 1);

if ( ! function_exists( 'localDB' ) ) {

	function localDB()
	{
		require_once('Mysql.class.php');
		$m = new MySQL('localhost', 'root', 'roottoor', 'dcg');
		return $m;
	}
}

function info()
{
	phpinfo();
}

/*
$path = 'field/*.txt';
$d = getDir($path);
*/

function getDir($path)
{
	$dirs = glob( $path );

	$r = array();
	foreach($dirs as $v ) {
		$r[] = $v;	
	}
	return $r;
}

function pre($a=array()) {
	echo '<pre>';
		print_r($a);
	echo '</pre>';
}

function br($a) {
	echo "$a<br/>";
}


function prt()
{
	   $a = get_included_files();
rsort( $a ); 
  pre( $a );
}


function sendReq($url, $data, $type='POST')
{
    //POST요청을 위하여 im=bunkering&kong=2&... 형태로 변경
    while(list($n,$v) = each($data)){
        $send_data[] = "$n=$v";
    }    
    $send_data = implode('&', $send_data);

    $url = parse_url($url);
     
    $host = $url['host'];
    $path = $url['path'].'?'.$send_data;
     
    //소켓 오픈
    $fp = fsockopen($host, 80, $errno, $errstr, 10.0);
    if (!is_resource($fp)) {
        echo "not connect host : errno=$errno,errstr=$errstr";
        exit;
    } 
  
    fputs($fp, "$type $path HTTP/1.1\r\n");
    fputs($fp, "Host: $host\r\n");
    fputs($fp, "Content-type: application/x-www-form-urlencoded\r\n");
    fputs($fp, "Content-length: " . strlen($send_data) . "\r\n");
    fputs($fp, "Connection:close" . "\r\n\r\n");
    fputs($fp, $send_data);
  
    //반환값 받기
    $result = ''; 
    while(!feof($fp)) {
        $result .= fgets($fp, 128);
    }    
    fclose($fp);
     
	return $result;
}


function file_write($name, $line) {
	$size = file_put_contents($name, $line.PHP_EOL , FILE_APPEND | LOCK_EX);
}

function file_read($name) {
	return file_get_contents($name);
}

function logging($txt) {
	$file = sprintf("C:\\xampp\\php\\tmp\\lg_%s.log", date('Ymd', time()));
	file_write($file, $txt);
}


function run($cmd)
{
	if (pclose(popen($cmd, 'r'))) return true;
	return false;
}

function cmd($cmd)
{
	$fp = popen($cmd, 'r');

	$out = '';
	while(!feof($fp)) {
		$out .= fread($fp, 4096);
	}
	fclose($fp);
	return $out;
}

function exe($cmd)
{
	$old = error_reporting();
	error_reporting(E_ALL); 
	try {

		exec($cmd);

	} catch (Exception $e) {
		echo $e->getMessage();
	}
	error_reporting($old);
}

function xml($root, $pot)
{
	function to_xml(SimpleXMLElement $object, array $data)
	{   
		foreach ($data as $key => $value) {
			if (is_array($value)) {
				$new_object = $object->addChild($key);
				to_xml($new_object, $value);
			} else {   
				$object->addChild($key, $value);
			}   
		}   
	} 
	$xml = new SimpleXMLElement($root);
	to_xml($xml, $pot);

	return $xml;
}

function getini($name)
{
	return parse_ini_file($name);
}

function httpPost($url, $data)
{
    $curl = curl_init($url);
    curl_setopt($curl, CURLOPT_POST, true);
    curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($data));
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($curl);
    curl_close($curl);
    return $response;
}

/*
$url = 'http://domain.com/get-post.php';
$fields = array(
	'lname' => urlencode($_POST['last_name']),
	'fname' => urlencode($_POST['first_name']),
	'title' => urlencode($_POST['title']),
	'company' => urlencode($_POST['institution']),
	'age' => urlencode($_POST['age']),
	'email' => urlencode($_POST['email']),
	'phone' => urlencode($_POST['phone'])
);
*/

function httpPost2($url, $data)
{
	//url-ify the data for the POST
	foreach($data as $key=>$value) { $fields_string .= $key.'='.$value.'&'; }

	rtrim($fields_string, '&');

	//open connection
	$ch = curl_init();

	//set the url, number of POST vars, POST data
	curl_setopt($ch,CURLOPT_URL, $url);
	curl_setopt($ch,CURLOPT_POST, count($data));
	curl_setopt($ch,CURLOPT_POSTFIELDS, $fields_string);

	//execute post
	$result = curl_exec($ch);

	//close connection
	curl_close($ch);
}

/*

$url = 'http://server.com/path';
$data = array('key1' => 'value1', 'key2' => 'value2');
*/
function sendPost($url, $data)
{

	// use key 'http' even if you send the request to https://...
	$options = array(
		'http' => array(
			'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
			'method'  => 'POST',
			'content' => http_build_query($data)
		)
	);
	$context  = stream_context_create($options);
	$result = file_get_contents($url, false, $context);
	if ($result === FALSE) {
		
		br("error");
		/* Handle error */
	}

	pre($result);
}

function do_post_request($url, $data, $optional_headers = null)
{
	$params = array('http' => array(
			  'method' => 'POST',
			  'content' => $data
			));

	if ($optional_headers !== null) {
		$params['http']['header'] = $optional_headers;
	}

	$ctx = stream_context_create($params);

	$fp = @fopen($url, 'rb', false, $ctx);

	if (!$fp) {
		throw new Exception("Problem with $url, $php_errormsg");
	}

	$response = @stream_get_contents($fp);
	if ($response === false) {
		throw new Exception("Problem reading data from $url, $php_errormsg");
	}

	return $response;
}







?>
