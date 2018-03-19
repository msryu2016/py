<?

function check_id($id) {
	return (preg_match('/^[A-Za-z][A-Za-z0-9_]{3,15}$/', $id)) ? true : false;
}

function check_email($email)
{
	return filter_var($email, FILTER_VALIDATE_EMAIL);
}

function check_url($url)
{
	return filter_var($url,  FILTER_VALIDATE_URL, FILTER_FLAG_PATH_REQUIRED);
}


// 마이크로 타임을 얻어 계산 형식으로 만듦
function get_microtime()
{
    list($usec, $sec) = explode(" ",microtime());
    return ((float)$usec + (float)$sec);
}

function random_chars($r)
{
//	$r = rand(4,6);//
	return substr(md5(get_microtime()), 0, $r);
}


function onlyNum($str)
{
	return  preg_replace("/[^0-9]*/s", "", $str); 
}

function checklen($str, $start=0,$end=10)
{
	$len = strlen($str);
	return ( $len >= $start && $len <= $end ) ? true:false;
}

function chk_ssn($ssn) {
	$reg_pattern = '/^\d{6}-[1234]\d{6}$/';
		if (!preg_match ($reg_pattern, $ssn)) {
		return false;
	}

	$birth_year = (substr($ssn, 6, 1)  <= "2") ? "19" : "20";
	$birth_year .= substr($ssn, 0, 2);
	$birth_month = substr($ssn, 2, 2);
	$birth_day = substr($ssn, 4, 2);
	if (!checkdate((int) $birth_month, (int) $birth_day, (int) $birth_year)) {
		return false;
	}

	$buf = array(13);
	for ($i = 0; $i < 6; $i++) $buf[$i] = (int) substr ($ssn, $i, 1);
	for ($i = 6; $i < 13; $i++) $buf[$i] = (int) substr ($ssn, $i + 1, 1);

	$multipliers = array(2,3,4,5,6,7,8,9,2,3,4,5);
	$sum = 0;
	for ($i = 0; $i < 12; $i++) $sum += ($buf[$i] *= $multipliers[$i]);

	if ((11 - ($sum % 11)) % 10 != $buf[12]) {
		return false;
	}

	return true;
}


?>