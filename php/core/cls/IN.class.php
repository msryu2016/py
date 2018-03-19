<?php

if (!defined('CLS')) {
	define('CLS', $_SERVER['DOCUMENT_ROOT'].'/new/core/cls');
}

require_once(CLS.'/IS.class.php');
require_once(CLS.'/SE.class.php');


/*
from CI
*/

class IN {

	public $GET;
	public $POST;

	function __construct() {
		$this->phytoncide();
	}

	private static function pretty_print($in){
			foreach($in as $k=>$v) {
				echo sprintf("\$%s = (isset(\$p['%s'])) ? trim(\$p['%s']) :'';\n", $k,$k,$k);

			}
			echo "\n";
			foreach($in as $k=>$v) {
				echo sprintf("if (\$%s=='') { \n", $k);
				echo sprintf("\talert_back('');\n");
				echo sprintf("\tout('false', '');\n");
				echo sprintf("}\n\n");

				if ($k=='mb_id')
				{

$skin = <<<SKIN
if (!checklen(\$%s, 4,16)) {
	alert_back('아이디는 4자 이상 16자 이하만 허용됩니다.');
}

if (!check_id(\$%s)) {
	alert_back(\$%s.'는 사용할수 없는 아이디입니다\\n영문자, 숫자, _만 입력 가능. 최소 4자이상 입력하세요.');
}

SKIN;
				echo sprintf($skin, $k, $k, $k);
				}
			echo "\n";
			}

	}

	public static function format($type, $flag=true) {


		function pretty_insert($a)
		{
			$line = array();
			foreach($a as $k=>$v)
			{
				$field[] = sprintf("%s", $k);
				$values[] = sprintf("'\$%s'", $k);
			}

			return sprintf("INSERT INTO ### \n (\n%s\n) VALUES (\n%s\n)\n", implode(",\n", $field),implode(",\n", $values));

		}

		function pretty_update($a)
		{
			$line = array();
			foreach($a as $k=>$v)
			{
				$line[] = sprintf("%s = '\$%s'", $k, $k);
			}

			return implode('\n', $line);
		}

		$ary = ($flag) ? IN::getInstance()->POST : IN::getInstance()->GET;
		switch(strtolower($type))
		{
			case 'i';
			case 'insert';
				$out = pretty_insert($ary);
			break;
			case 'u';
			case 'update';
				$out = pretty_update($ary);
			break;
		}

		return $out;


	}

	public static function GET($is_print=false) {
		$out = IN::getInstance()->GET;
		if($is_print) {
			IN::pretty_print($out);
		}
		return $out;

	}

	public static function POST($is_print=false) {
		$out = IN::getInstance()->POST;
		if($is_print) {
			IN::pretty_print($out);
		}
		return $out;
	}

	public static function getInstance() {

     static $instance = null;
        if (null === $instance) {
            $instance = new IN();
        }

        return $instance;
	}

	private function phytoncide() {

		$this->GET = SE::_clear($_GET);
		$this->POST = SE::_clear($_POST);

		$_SERVER['PHP_SELF'] = IS::self();

	}

	public static function Minus($ary, $minus = array()) {

		$out = array();

		foreach($ary as $k=>$v) {

			if ( ! in_array($k, $minus)) {
				$out[$k] = $v;
			} 
		}

		return $out;
	}

	public static function Add($ary, $add = array()) {

		$out = array();

		foreach($ary as $k=>$v) {


			if ( in_array($k, $add)) {

				$out[$k] = $v;
			} 
		}

		return $out;

	}

	public static function GMinus($minus = array()) {

		$G = IN::GET();
		return IN::Minus($G, $minus);

	}

	public static function PMinus($minus = array()) {

		$P = IN::POST();
		return IN::Minus($P, $minus);

	}

	public static function GAdd($add = array()) {

		$G = IN::GET();
		return IN::Add($G, $add);

	}

	public static function PAdd($add = array()) {

		$P = IN::POST();
		return IN::Add($P, $add);

	}

	private function Set() {

	}

	public  function PSet($key,$val) {

		$O = IN::getInstance();
		$O->POST[$key] = $val;

		return $O;
	}

	public  function GSet($key,$val) {

		$O = IN::getInstance();
		$O->GET[$key] = $val;

		return $O;
	}

}

?>