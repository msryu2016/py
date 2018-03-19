<?php

error_reporting(E_ALL); 

ini_set("display_errors", 1);


function isAjax()
{
	return (isset($_SERVER['HTTP_X_REQUESTED_WITH']) && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) === 'xmlhttprequest');
}

function yoil($day,$lang=true)
{
	if($lang) {
		$yoil = array("일","월","화","수","목","금","토");
	} else {
		$yoil = array("Sun","Mon","Tue","Wed","Thu","Fri","Sat");
	}

	$tmp = preg_replace('/[-\.]/', '', $day);

	return $yoil[date('w', strtotime($tmp))];
}
/*
// 짧은 환경변수를 지원하지 않는다면
if (isset($HTTP_POST_VARS) && !isset($_POST)) {
	$_POST   = &$HTTP_POST_VARS;
	$_GET    = &$HTTP_GET_VARS;
	$_SERVER = &$HTTP_SERVER_VARS;
	$_COOKIE = &$HTTP_COOKIE_VARS;
	$_ENV    = &$HTTP_ENV_VARS;
	$_FILES  = &$HTTP_POST_FILES;

    if (!isset($_SESSION))
		$_SESSION = &$HTTP_SESSION_VARS;
}
*/

if (!function_exists('xss_clean'))
{

	//==========================================================================================================================
	// XSS(Cross Site Scripting) 공격에 의한 데이터 검증 및 차단
	//--------------------------------------------------------------------------------------------------------------------------
	function xss_clean($data) 
	{ 
		// If its empty there is no point cleaning it :\ 
		if(empty($data)) 
			return $data; 
			 
		// Recursive loop for arrays 
		if(is_array($data)) 
		{ 
			foreach($data as $key => $value) 
			{ 
				$data[$key] = xss_clean($value); 
			} 
			 
			return $data; 
		} 
		 
		// http://svn.bitflux.ch/repos/public/popoon/trunk/classes/externalinput.php 
		// +----------------------------------------------------------------------+ 
		// | Copyright (c) 2001-2006 Bitflux GmbH                                 | 
		// +----------------------------------------------------------------------+ 
		// | Licensed under the Apache License, Version 2.0 (the "License");      | 
		// | you may not use this file except in compliance with the License.     | 
		// | You may obtain a copy of the License at                              | 
		// | http://www.apache.org/licenses/LICENSE-2.0                           | 
		// | Unless required by applicable law or agreed to in writing, software  | 
		// | distributed under the License is distributed on an "AS IS" BASIS,    | 
		// | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or      | 
		// | implied. See the License for the specific language governing         | 
		// | permissions and limitations under the License.                       | 
		// +----------------------------------------------------------------------+ 
		// | Author: Christian Stocker <chregu@bitflux.ch>                        | 
		// +----------------------------------------------------------------------+ 
		 
		// Fix &entity\n; 
		$data = str_replace(array('&amp;','&lt;','&gt;'), array('&amp;amp;','&amp;lt;','&amp;gt;'), $data); 
		$data = preg_replace('/(&#*\w+)[\x00-\x20]+;/', '$1;', $data); 
		$data = preg_replace('/(&#x*[0-9A-F]+);*/i', '$1;', $data); 

		if (function_exists("html_entity_decode"))
		{
			$data = html_entity_decode($data); 
		}
		else
		{
			$trans_tbl = get_html_translation_table(HTML_ENTITIES);
			$trans_tbl = array_flip($trans_tbl);
			$data = strtr($data, $trans_tbl);
		}

		// Remove any attribute starting with "on" or xmlns 
		$data = preg_replace('#(<[^>]+?[\x00-\x20"\'])(?:on|xmlns)[^>]*+>#i', '$1>', $data); 

		// Remove javascript: and vbscript: protocols 
		$data = preg_replace('#([a-z]*)[\x00-\x20]*=[\x00-\x20]*([`\'"]*)[\x00-\x20]*j[\x00-\x20]*a[\x00-\x20]*v[\x00-\x20]*a[\x00-\x20]*s[\x00-\x20]*c[\x00-\x20]*r[\x00-\x20]*i[\x00-\x20]*p[\x00-\x20]*t[\x00-\x20]*:#i', '$1=$2nojavascript...', $data); 
		$data = preg_replace('#([a-z]*)[\x00-\x20]*=([\'"]*)[\x00-\x20]*v[\x00-\x20]*b[\x00-\x20]*s[\x00-\x20]*c[\x00-\x20]*r[\x00-\x20]*i[\x00-\x20]*p[\x00-\x20]*t[\x00-\x20]*:#i', '$1=$2novbscript...', $data); 
		$data = preg_replace('#([a-z]*)[\x00-\x20]*=([\'"]*)[\x00-\x20]*-moz-binding[\x00-\x20]*:#', '$1=$2nomozbinding...', $data); 

		// Only works in IE: <span style="width: expression(alert('Ping!'));"></span> 
		$data = preg_replace('#(<[^>]+?)style[\x00-\x20]*=[\x00-\x20]*[`\'"]*.*?expression[\x00-\x20]*\([^>]*+>#i', '$1>', $data); 
		$data = preg_replace('#(<[^>]+?)style[\x00-\x20]*=[\x00-\x20]*[`\'"]*.*?behaviour[\x00-\x20]*\([^>]*+>#i', '$1>', $data); 
		$data = preg_replace('#(<[^>]+?)style[\x00-\x20]*=[\x00-\x20]*[`\'"]*.*?s[\x00-\x20]*c[\x00-\x20]*r[\x00-\x20]*i[\x00-\x20]*p[\x00-\x20]*t[\x00-\x20]*:*[^>]*+>#i', '$1>', $data); 

		// Remove namespaced elements (we do not need them) 
		$data = preg_replace('#</*\w+:\w[^>]*+>#i', '', $data); 

		do 
		{ 
			// Remove really unwanted tags 
			$old_data = $data; 
			$data = preg_replace('#</*(?:applet|b(?:ase|gsound|link)|embed|frame(?:set)?|i(?:frame|layer)|l(?:ayer|ink)|meta|object|s(?:cript|tyle)|title|xml)[^>]*+>#i', '', $data); 
		} 
		while ($old_data !== $data); 
		 
		return $data; 
	} 
}

if ( ! function_exists( 'out' ))
{

	function out($flag, $msg)
	{
		$out = array();
		$out['flag'] = $flag;
		$out['msg'] = $msg;

		if (0){
			die(pre($out));
		}else{
			die(json_encode($out));
		}
	}
}

if ( ! function_exists( 'set_session' ))
{
	// 세션변수 생성
	function set_session($session_name, $value)
	{
		if (PHP_VERSION < '5.3.0')
			session_register($session_name);
		// PHP 버전별 차이를 없애기 위한 방법
		$$session_name = $_SESSION["$session_name"] = $value;
	}
}


if ( ! function_exists( 'get_session' ))
{
	// 세션변수값 얻음
	function get_session($session_name)
	{
		return @$_SESSION[$session_name];
	}
}


if ( ! function_exists( 'set_cookie' ))
{
	// 쿠키변수 생성
	function set_cookie($cookie_name, $value, $expire=0)
	{
		global $g4;

		@setcookie(md5($cookie_name), base64_encode($value), NOW_TIME + $expire, '/', HOST);
	}
}

if ( ! function_exists( 'get_cookie' ))
{
	// 쿠키변수값 얻음
	function get_cookie($cookie_name)
	{
		return base64_decode($_COOKIE[md5($cookie_name)]);
	}
}

if ( ! function_exists('keyval'))
{


	function keyval($array, $key, $val)
	{
		$out = array();

		foreach($array as $k=>$v)
		{
			$out[$v[$key]] = $v[$val];
		}
		return $out;
	}

}

if ( ! function_exists('sql_password'))
{

	function sql_password($str) {
		global $db;

		$sql = "SELECT PASSWORD('$str') as pass";
		$row = $db->row($sql);

		return $row['pass'];
	}

}

if ( ! function_exists( 'localDB' ) ) {

	function localDB()
	{
		global $db, $mysql_host, $mysql_user, $mysql_password, $mysql_db;

		if ($db == null)
		{
			require_once(CLS.'/Mysql.class.php');
			require_once(PWD."/dbconfig.php");
			$db = new MySQL($mysql_host, $mysql_user, $mysql_password, $mysql_db);
		}
		return $db;
	}
}

if ( ! function_exists( 'info' ) ) {

	function info()
	{
		phpinfo();
	}

}
/*
$path = 'field/*.txt';
$d = getDir($path);
*/

if ( ! function_exists( 'getDir' ) ) {

	function getDir($path)
	{
		$dirs = glob( $path );

		$r = array();
		foreach($dirs as $v ) {
			$r[] = $v;	
		}
		return $r;
	}

}

if ( ! function_exists( 'pre' ) ) {

	function pre($a=array()) {

		if (strcmp(IP, '192.168.0')>=0)
		{
			echo "<pre>";
			print_r($a);
			echo "</pre>";
		}


	}

}

if ( ! function_exists( 'br' ) ) {

	function br($a) {
		if (strcmp(IP, '192.168.0')>=0)
		{
			echo "$a<br/>";
		}
	}

}

if ( ! function_exists( 'prt' ) ) {

	function prt()
	{
		   $a = get_included_files();
	rsort( $a ); 
	  pre( $a );
	}

}

if ( ! function_exists( 'sendReq' ) ) {

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

}

if ( ! function_exists( 'file_write' ) ) {

	function file_write2($name, $line)
	{
		$fp = fopen($name, 'a+');

		if (!is_resource($fp)) return false;

		if(flock($fp, LOCK_EX)) {
			fwrite($fp, sprintf("%s%s", $line,PHP_EOL));
			flock($fp, LOCK_UN);	}
		fclose($fp);
		return true;
	}

}

if ( ! function_exists( 'file_write' ) ) {

	function file_write($name, $line) {
		$size = file_put_contents($name, $line.PHP_EOL , FILE_APPEND | LOCK_EX);
	}

}

if ( ! function_exists( 'file_read' ) ) {

	function file_read($name) {
		return file_get_contents($name);
	}

}

if ( ! function_exists( 'logging' ) ) {

	function logging($txt) {
		$file = sprintf("e:\\tmp\lg_%s.log", date('Ymd', time()));
		file_write2($file, $txt);
	}

}

if ( ! function_exists( 'run' ) ) {

	function run($cmd)
	{
		if (pclose(popen($cmd, 'r'))) return true;
		return false;
	}

}

if ( ! function_exists( 'cmd' ) ) {

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

}

if ( ! function_exists( 'exe' ) ) {

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

}

if ( ! function_exists( 'xml' ) ) {

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

}

if ( ! function_exists( 'getini' ) ) {

	function getini($name)
	{
		return parse_ini_file($name);
	}

}

if ( ! function_exists( 'httpPost' ) ) {

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

}

if ( ! function_exists( 'httpPost2' ) ) {

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

}

/*

$url = 'http://server.com/path';
$data = array('key1' => 'value1', 'key2' => 'value2');
*/

if ( ! function_exists( 'sendPost' ) ) {

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

}

if ( ! function_exists( 'do_post_request' ) ) {

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

}

/*
$from = 'sekki@naver.com';
$from_name = '홍길동';
$to = 'msryu2016@naver.com';
$to_name = '호호호';
$subject= '안녕하세요';
$html = '방가방가';

if(send_mail($from, $from_name, $to, $to_name, $subject, $html))
{
	br('send');
}	
*/

if ( ! function_exists( 'send_mail' ) ) {

function send_mail($from, $from_name, $to, $to_name, $subject, $html, $alt='')
{
	require_once CLS. '/mail/PHPMailerAutoload.php';

	$mail = new PHPMailer;
	$mail->IsSMTP();
	$mail->Host       = 'smtp.worksmobile.com'; // set the SMTP server

	$mail->Port       = 587;    
//	$mail->SMTPDebug  = 2;
	$mail->SMTPAuth = true;
//	$mail->SMTPSecure = true;
	$mail->Username = 'msryu@hackerslab.or.kr';
	$mail->Password = 'gozjtmfoq1!';
	$mail->CharSet = 'utf-8';
	$mail->Encoding = 'base64';
	$mail->setFrom($from, $from_name);
	$mail->addAddress($to, $to_name);
	$mail->Subject = $subject;
	$mail->msgHTML($html, dirname(__FILE__));
	$mail->AltBody = $alt;

	if ( ! $mail->send()) {
		logging( "Mailer Error: " . $mail->ErrorInfo );
//	    echo "Mailer Error: " . $mail->ErrorInfo;
		return false;
	} else {
		return true;
	}
}

}


if ( ! function_exists( 'get_client_ip_env' ) ) {
	// Function to get the client ip address
	function get_client_ip_env() {
		$ipaddress = '';
		if (getenv('HTTP_CLIENT_IP'))
			$ipaddress = getenv('HTTP_CLIENT_IP');
		else if(getenv('HTTP_X_FORWARDED_FOR'))
			$ipaddress = getenv('HTTP_X_FORWARDED_FOR');
		else if(getenv('HTTP_X_FORWARDED'))
			$ipaddress = getenv('HTTP_X_FORWARDED');
		else if(getenv('HTTP_FORWARDED_FOR'))
			$ipaddress = getenv('HTTP_FORWARDED_FOR');
		else if(getenv('HTTP_FORWARDED'))
			$ipaddress = getenv('HTTP_FORWARDED');
		else if(getenv('REMOTE_ADDR'))
			$ipaddress = getenv('REMOTE_ADDR');
		else
			$ipaddress = 'UNKNOWN';
	 
		return $ipaddress;
	}

}


if ( ! function_exists( 'get_client_ip_server' ) ) {

	function get_client_ip_server() {
		$ipaddress = '';
		if ($_SERVER['HTTP_CLIENT_IP'])
			$ipaddress = $_SERVER['HTTP_CLIENT_IP'];
		else if($_SERVER['HTTP_X_FORWARDED_FOR'])
			$ipaddress = $_SERVER['HTTP_X_FORWARDED_FOR'];
		else if($_SERVER['HTTP_X_FORWARDED'])
			$ipaddress = $_SERVER['HTTP_X_FORWARDED'];
		else if($_SERVER['HTTP_FORWARDED_FOR'])
			$ipaddress = $_SERVER['HTTP_FORWARDED_FOR'];
		else if($_SERVER['HTTP_FORWARDED'])
			$ipaddress = $_SERVER['HTTP_FORWARDED'];
		else if($_SERVER['REMOTE_ADDR'])
			$ipaddress = $_SERVER['REMOTE_ADDR'];
		else
			$ipaddress = 'UNKNOWN';
	 
		return $ipaddress;
	}

}


if ( ! function_exists( 'set_connect_user_123123' ) ) {
	function set_connect_user_123123()
	{
		global $db,$title,$mb,$_SERVER,$config;

		define('REF',@addslashes(strip_tags($_SERVER['HTTP_REFERER'])));

		$sql = sprintf("SELECT COUNT(*) CNT FROM new_connect_login WHERE lo_ip = '%s' AND yn='Y'", IP);
		$cnt = $db->one($sql);

		if (empty($title)) {
			$title = URI;
		}
		$lo_url = URI;

		$env = array();
		$env[] = @getenv('HTTP_CLIENT_IP');
		$env[] = @getenv('HTTP_X_FORWARDED_FOR');
		$env[] = @getenv('HTTP_X_FORWARDED');
		$env[] = @getenv('HTTP_FORWARDED_FOR');
		$env[] = @getenv('HTTP_FORWARDED');
		$env[] = @getenv('REMOTE_ADDR');

		$server = array();
		$server[] = @$_SERVER['HTTP_CLIENT_IP'];
		$server[] = @$_SERVER['HTTP_X_FORWARDED_FOR'];
		$server[] = @$_SERVER['HTTP_X_FORWARDED'];
		$server[] = @$_SERVER['HTTP_FORWARDED_FOR'];
		$server[] = @$_SERVER['HTTP_FORWARDED'];
		$server[] = @$_SERVER['REMOTE_ADDR'];

		$extra = array();
		$extra[] = NAME;
		$extra[] = AGENT;
		$extra[] = URI;
		$extra[] = REF;
		$extra[] = local_ip();
		$extra[] = IP;
	//	$extra[] = implode(':', $env);
	//	$extra[] = implode(':', $server);

		$mb_id = (isset($mb['mb_id'])) ? $mb['mb_id'] : '';
		$login_minutes = isset($config['cf_login_minutes'])?$config['cf_login_minutes']: 10;

		if ($cnt){
			$tmp_sql = sprintf("
				UPDATE new_connect_login SET
					mb_id = '%s',
					lo_datetime = '%s',
					lo_location = '%s',
					lo_url = '%s',
					extra_ip = '%s',
					extra_info = '%s',
					yn = '%s'
				WHERE
					lo_ip = '%s'", $mb_id, NOW_STR, $title, $lo_url, implode(',', local_ip()), serialize(base64_encode($extra)), 'Y', IP);
			$db->query($tmp_sql, true);
		} else {
			$tmp_sql = sprintf("
				INSERT INTO new_connect_login 
					( lo_ip, mb_id, lo_datetime, lo_location, lo_url, extra_ip, extra_info, yn )
				VALUES
					('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
			", IP, $mb_id, NOW_STR, $title, $lo_url, implode(',', local_ip()), serialize(base64_encode($extra)), 'Y');
			$db->query($tmp_sql, true);
		}

		$tmp_sql = sprintf("UPDATE new_connect_login SET yn = '%s' WHERE lo_datetime < '%s'", 'N', date("Y-m-d H:i:s", NOW_TIME - (60 * $login_minutes)));
		$db->query($tmp_sql, true);
	}


}


//$_GET = xss_clean($_GET);
//$_POST = xss_clean($_POST);
//unset($_REQUEST);

if ( ! function_exists( 'local_ip' ) ) {

	function local_ip()
	{
		return gethostbynamel(php_uname('n'));
	}

}
?>
