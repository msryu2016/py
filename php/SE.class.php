<?php

class SE {

	public static $is_utf8 = true;

	/**
	 * Remove Invisible Characters
	 *
	 * This prevents sandwiching null characters
	 * between ascii characters, like Java\0script.
	 *
	 * @param	string
	 * @param	bool
	 * @return	string
	 */
	public static function remove_invisible_characters($str, $url_encoded = TRUE)
	{
		$non_displayables = array();

		// every control character except newline (dec 10),
		// carriage return (dec 13) and horizontal tab (dec 09)
		if ($url_encoded)
		{
			$non_displayables[] = '/%0[0-8bcef]/i';	// url encoded 00-08, 11, 12, 14, 15
			$non_displayables[] = '/%1[0-9a-f]/i';	// url encoded 16-31
		}

		$non_displayables[] = '/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]+/S';	// 00-08, 11, 12, 14-31, 127

		do
		{
			$str = preg_replace($non_displayables, '', $str, -1, $count);
		}
		while ($count);

		return $str;
	}


	/**
	* Clean UTF-8 strings
	*
	* Ensures strings contain only valid UTF-8 characters.
	*
	* @param	string	$str	String to clean
	* @return	string
	*/
	public static function clean_string($str)
	{
		if (  ! is_array($str)  && IS::ascii($str) === FALSE )
		{
			if (IS::mbstr())
			{
				$str = mb_convert_encoding($str, 'UTF-8', 'UTF-8');
			}
			elseif (IS::iconv())
			{
				$str = @iconv('UTF-8', 'UTF-8//IGNORE', $str);
			}
		}

		return $str;
	}

	public static function clean_utf8($str) {

		if (SE::$is_utf8) {
			return SE::clean_string($str);
		}
		return $str;
	}


	public static function _clean_key($str, $fatal = TRUE) {

		if ( ! preg_match('/^[a-z0-9:_\/|-]+$/i', $str))
		{
			if ( TRUE === $fatal ) {
				return FALSE;
			} else {
				echo 'Disallowed Key Characters.';
				die(7); // EXIT_USER_INPUT
			}
		}

		return SE::clean_utf8($str);

	}

	public static function _clean_data($str) {


		if (is_array($str)) 
		{
			$out = array();
			foreach(array_keys($str) as $key) {
				$out[SE::_clean_key($key)] = SE::_clean_data($str[$key]);
			}
			return $out;
		}

		$str = SE::_clear($str);

		if ( ! IS::ver('5.4') && get_magic_quotes_gpc()) {
			$str = stripslashes($str);
		}

		$str = SE::remove_invisible_characters($str, FALSE);



		return SE::clean_utf8($str);

	}

	public static function _clear($array)
	{

		if (is_array($array))
		{
			$out = array();
			foreach($array as $k=>$v) {
				$out[SE::_clean_key($k)] = SE::_clean_data($array[$k]);
			}
			return $out;
		}

		return $array;

	}

}

?>