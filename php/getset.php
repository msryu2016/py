<?php
set_time_limit(0);

function prt()
{
	p( get_included_files() );
}


function createSign ($paramArr) {

     global $appSecret;

     $sign = $appSecret;

     ksort($paramArr);

     foreach ($paramArr as $key => $val) {

         if ($key != '' && $val != '') {

             $sign .= $key.$val;

         }

     }

     $sign.=$appSecret;

     $sign = strtoupper(md5($sign));

     return $sign;

}

function p($a) {
	echo '<pre>';
		print_r($a);
	echo '</pre>';
}

function e($a) {
	echo "$a<br/>";
}


function getsetfile($file)
{

	$var = array();
	$func = array();

	$f = file($file);
	foreach( $f as $v) {

//		(is_array($v)) ? p($v) : e($v);
		$v = preg_replace('/\r\n/', '', $v);
		$var[] = sprintf("\tprivate $%s;\n", $v);

		$func[] = sprintf("\tpublic function get%s() {\n\t\treturn \$this->%s;\n\t}\n", ucfirst($v),$v);

		$func[] = sprintf("\tpublic function set%s(\$%s) {\n\t\t\$this->%s = \$%s;\n\t}\n\n", ucfirst($v),$v,$v,$v);

	}
	
	$nf = preg_replace('/\.txt/', '', basename($file));

	$class = sprintf("<?php\n\nclass %s {\n\n%s \n%s\n}\n?>", $nf, implode("", $var), implode("", $func));

	$dir = dirname($file);
	$name = sprintf("%s/%s.php", $dir, $nf);

	if (!file_exists($name)){
		file_put_contents($name, $class);
		return true;
	}
	
	return false;
}


function getDir($path)
{
	$dirs = glob( $path );

	$r = array();
	foreach($dirs as $v ) {
		$r[] = $v;	
	}
	return $r;
}

$path = 'field/*.txt';
$d = getDir($path);

foreach($d as $f)
{
	$file= sprintf('%s/%s', $path, $f);
	e($f);

	getsetfile($f);
}

//$file = 'MyClass';
//getset($file);

//include "$file.php";
prt();

include "field/AreasGetRequest.php";

interface TmallImpl {
	public function draw($param);
}

/*

Tmall 기본정보를 설정
*/
abstract class TmallApi {

	private $appkey;
	private $secretkey;
	private $gatewayurl;

	private $obj;

	public function TmallApi($appkey, $secretkey, $gatewayurl) {

		$this->appkey = $appkey;
		$this->secretkey = $secretkey;
		$this->gatewayurl = $gatewayurl;
	}
 
	public function getAppkey() {
		return $this->appkey;
	}
	public function setAppkey($appkey) {
		$this->appkey = $appkey;
	}

	public function getSecretkey() {
		return $this->secretkey;
	}
	public function setSecretkey($secretkey) {
		$this->secretkey = $secretkey;
	}

	public function getGatewayurl() {
		return $this->gatewayurl;
	}
	public function setGatewayurl($gatewayurl) {
		$this->gatewayurl = $gatewayurl;
	}

}

/*
tmall기본정보를 상속받고

obj에 draw호출
*/
class TmallTop extends TmallApi implements TmallImpl  {

	public function TmallTop($obj) {
		$this->setObj($obj);
	}


	public function setObj($obj){
		$this->obj= $obj;
	}

	public function getObj() {
		return $this->obj;
	}


	public function draw($param) {
		return $this->obj->draw($param);
	}
	

}

class CurlGet implements TmallImpl {
	public function draw($param) {
		return "CURL draw";
	}
}

/*
draw 구현체
*/
class FileGet implements TmallImpl {

	public $url= 'http://naver.com';

	public function createParam($f)
	{
	return implode('&', array_map(function($v,$k) {
		//return $k.'='.urlencode($v).'';
		return sprintf('%s=%s', $k, urlencode($v));

		}, array_values($f), array_keys($f)));

	}

	protected function generateSign($params)
	{
		ksort($params);
		$stringToBeSigned = $this->secretKey;
		foreach ($params as $k => $v)
		{
			if(is_string($v) && "@" != substr($v, 0, 1))
			{
				$stringToBeSigned .= "$k$v";
			}
		}
		unset($k, $v);
		$stringToBeSigned .= $this->secretKey;
		return strtoupper(md5($stringToBeSigned));
	}

	public function getUrl() {
		return $this->url;
	}

	public function setUrl($url) {
		$this->url = $url;
	}

	public function url_json($p)
	{
		return json_decode(file_get_contents($p));
	}

	public function draw($param) {
		p($param);
		$params = $this->createParam($param);
		$line = sprintf('%s?%s', $this->getUrl(), $params);
		e($line);
		return $this->url_json($line);
	}
}


interface TmallMethod {
	public function getApiMethodName();
}



class GetAreas extends AreasGetRequest implements TmallMethod {

	public function GetAreas() {

	}

	public function getApiMethodName() {
		return "taobao.hotel.order.get";
	}

	public function draw($a) {

	}

}

$sendUrl = new FileGet();

$g = new GetAreas();

p($g);
p($g->getApiMethodName());


$t = new TmallTop($g);
p($t);
$t->setAppkey( 'test' );
p($t);

$param = array();
$p['abc'] = '1234';

$t->draw($p);


?>