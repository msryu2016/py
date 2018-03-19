<?php

class IS {

	public static function ver($ver)
	{
		if (version_compare(PHP_VERSION, $ver, '>=')) {
			return true;
		}
		return false;
	}

	public static function loaded($v) {
		return extension_loaded($v);
	}

	public static function mbstr() {
		return IS::loaded('mbstring');
	}

	public static function iconv() {
		return IS::loaded('iconv');
	}

	public static function ajax()
	{
		return ( ! empty($_SERVER['HTTP_X_REQUESTED_WITH']) && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) === 'xmlhttprequest');
	}

	public static function ascii($str)
	{
	//	pre(debug_print_backtrace())	;
		return (preg_match('/[^\x00-\x7F]/S', $str) === 0);	
	}

	public static function newline($str) {
		return preg_replace('/(?:\r\n|[\r\n])/', PHP_EOL, $str);
	}

	public static function self() {
		return strip_tags($_SERVER['PHP_SELF']);
	}

	public static function exists($file) {
		return (file_exists($file))? true: false;
	}

	public static function ini($var) {
		return ini_get($var);
	}

}

?>