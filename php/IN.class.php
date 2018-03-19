<?php

require_once('IS.class.php');
require_once('SE.class.php');

prt();

/*
from CI
*/

class IN {

	public $GET;
	public $POST;

	function __construct() {
		$this->phytoncide();
	}

	public static function GET() {
		
		return IN::getInstance()->GET;
	}

	public static function POST() {
		return IN::getInstance()->POST;
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

	public static function Add($ary, $minus = array()) {

		$out = array();

		foreach($ary as $k=>$v) {

			if ( in_array($k, $minus)) {
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