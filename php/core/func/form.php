<?php
require_once 'function.php';
require_once CLS.'/IN.class.php';


if(!function_exists('cut_str'))
{

	function cut_str($str,$len,$encode='utf-8',$ret=1)
	{
		$end = (strlen($str)>$len) ? '...' : '';
		$out = mb_strcut ( $str, 0 , $len , $encode ).''.$end;
		if($ret==1) {
			return $out; 	
		} else {
			echo $out;
		}
	}

}


if ( ! function_exists( 'cut_sense' ))
{

function cut_sense($matne_harf, $l_harf ,$return=1 ) {
	if ( strlen($matne_harf) > $l_harf){
		$end='...';
	}else{
		$end='';
	}
	if ( function_exists('mb_strcut') ){
		$matne_harf = mb_strcut ( $matne_harf, 0 , $l_harf , "UTF-8" );
	}else{
		$matne_harf =substr($matne_harf, 0, $l_harf);
	}
	$text=''.$matne_harf.''.$end.'';
	if ( $return == 1){
		return $text;
	}else{
		print $text;
	}
}

}

if ( ! function_exists( 'view' ))
{

function view($file, $vars = array(), $flag=true)
{
	extract($vars);
	ob_start();
	require_once $file;
	$content = ob_get_contents();
	ob_end_clean();

	if ($flag)
	{
		return $content;
	} 
	echo $content;
}

}

if ( ! function_exists( 'options' ))
{

function options($ary, $key='', $flag=true) {

	$out = "\n";

	foreach($ary as $k=>$v) {

		if ( true != $flag ) {
			$k = $v;
		}

		$m = ($key==$k) ? "selected='selected'" : '';
		$out .= sprintf("<option value='%s' %s>%s</option>\n", $k, $m, $v );
	}

	return $out;
}

}

if ( ! function_exists( 'checkbox' ))
{

function checkbox($ary, $name, $check=array(), $flag=false) {

	$out = "\n";
	$i= 0;
	foreach($ary as $k=>$v) {

		if ( true != $flag ) {
			$k = $v;
		}

		$m = (in_array($k,$check)) ? "checked='checked'" : '';
		$out .= sprintf("<label><input type='checkbox' name='%s[]' id='%s' value='%s' %s>%s</label>\n", $name, $k.$i++, $v, $m, $v );
	}

	return $out;

}

}

if ( ! function_exists( 'radio' ))
{

function radio($ary, $name, $key='', $flag=true) {

	$out = "\n";
	$i = 0;
	foreach($ary as $k=>$v) {

		if ( true != $flag ) {
			$k = $v;
		}

		$m = ($key==$v) ? "checked='checked'" : '';
		$out .= sprintf("<label><input type='radio' name='%s' id='%s' value='%s' %s>%s</label>\n", $name, $k.$i++, $v, $m, $v );
	}

	return $out;

}

}

if ( ! function_exists( 'hidden' ))
{
function hidden($ary, $visiable=false) {

	$out = "\n";
	$type = ($visiable==true) ? 'text' : 'hidden';
	foreach($ary as $k=>$v) {
		$out.= sprintf("<input type='%s' name='%s' id='%s' value='%s' />\n", $type, $k, $k, $v);
	}

	return $out;
}
}


if(!function_exists('alert'))
{

	function alert($msg,$title='')
	{
		die( "
			<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">
			<html>
			<head>
			<title>$title</title>
			<script>
			alert('$msg');
			</script>
			</head>
			<body>
			</body>
			</html>
		" );
	}
}


if ( ! function_exists( 'alert_back' ))
{
function alert_back($msg,$title='')
{
	die( "
		<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">
		<html>
		<head>
		<title>$title</title>
		<script>
			alert('$msg');
			history.back();
		</script>
		</head>
		<body>
		</body>
		</html>
	" );
}

}

if ( ! function_exists( 'alert_replace' ))
{

function alert_replace($msg,$url,$title='')
{
	die( "
<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">
<html>
<head>
<title>$title</title>
<script language='javascript'>
	alert('$msg');
	location.replace('$url');
</script>
</head>
<body>
</body>
</html>
	" );
}

}


if ( ! function_exists( 'replace' ))
{

function replace($url,$title='')
{
	die( "
<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">
<html>
<head>
<title>$title</title>
<script language='javascript'>
	location.replace('$url');
</script>
</head>
<body>
</body>
</html>
	" );
}

}


if ( ! function_exists( 'set_session' ))
{

if(!function_exists('alert_close'))
{

	function alert_close($msg,$title='')
	{
		die( "
	<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">
	<html>
	<head>
	<title>$title</title>
	<script language='javascript'>
		alert('$msg');
		self.close();
	</script>
	</head>
	<body>
	</body>
	</html>
		" );
	}
}

}


if ( ! function_exists( 'submit' ))
{


function submit($url, $params, $msg='', $title='')
{
$skin = <<<abc
<!doctype html>
<html lang="ko"><head>
<head>
<title>%s</title>
<script language='javascript'>
	function go() {
		%s
		document.getElementById('frmSubmit').submit();
	}
</script>
</head>
<body onload='go()'>
	<form method="post" name="frmSubmit" id='frmSubmit' action="%s">
	%s
	</form>
</body>
</html>
abc;

	$line = '';
	foreach($params as $k=>$v)
	{
		$line .= sprintf("<input type='text' name='%s' value='%s' />", $k,$v);
	}

	if ($msg!='')
	{	
		$msg = sprintf("alert('%s');", $msg);
	}

	die( sprintf( $skin, $title, $msg, $url, $line) );
}

}


if ( ! function_exists( 'hshow' ))
{

function hshow() {
echo "
<script language='javascript'>

\$('input:not(._not),select').each(function(){ 

	var d = \$(\"<div class='_input_show' >\") 
		.css({
			'display':'inline-block',
			'width':'120px',
			'color':'red',
			'font-weight':'bold'
		}).html( $(this).attr('name') );
	\$(this).before( d ); 
	
	var t = \$(this).attr('type'); 

	if (t == 'password' || t == 'hidden' || t == 'select' ) {
	
		\$(this).prop('type', 'text'); 
		\$(this).after('<br />') 
	}}
	);

</script>
";
}

}


if ( ! function_exists( 'drag' ))
{


function drag($ary = array())
{

	$out = '';
	$i =0;
	foreach($ary as $k=>$v)
	{
		$out.= sprintf("<div style='width:50px;text-align:center;display:inline-block'>%s</div><input type='text' id='%s%s' name='%s' value='%s' class='_not' />\n", $k, $k,$i++, $k, $v);
	}

	$out = preg_replace('/\\n/', '<br />', $out);
	echo "
	
	<style>
	.debug {
		border:solid 1px red;
		position:absolute;
		width:250px;
		padding:10px;
		margin:10px;
		height:180px;
		background-color:white;
		overflow-y:scroll;
		cursor:move
		}
	</style>
	<div class='debug'>$out</div>
	<script type=\"text/javaScript\" >

		$(function() {

			var b = $('body');
			var r = b.offset();
			var w = b.width();
			var o = $('.debug');

			o.css('left', r.left + w - ( o.width() + 50 ))
			 .css('top', r.top)
			 .draggable();

		});

	</script>
	
	
	";
}

}

/*
	<link rel='stylesheet' type='text/css' href='http://dev.dcgworld.com/admin/v3/css/jquery-ui.css' />
	<script src='http://dev.dcgworld.com/admin/js/jquery-1.8.3.js'></script>
	<script src='http://dev.dcgworld.com/admin/js/jquery-ui.js'></script>
	<body>

<form method="post" action="<?=IS::self()?>">
	<select name="option">
	<?=options($a, $p['option']);?>
	</select>
<br>
	<?=checkbox($a, 'check', $p['check'])?>
<br>
	<?=radio($a, 'radio', $p['radio'])?>
<br>
	<?=hidden($b);?>

	<input type='submit' />
	<?=drag($b);?>
	<?=hshow(); ?>
</form>
</body>


*/
?>