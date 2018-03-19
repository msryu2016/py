<?php

include 'function.php';
include 'IN.class.php';

$a = array();
$a['abc'] = '123';
$a['abd'] = '345';
$a['abe'] = '566';


$b = array();
$b['ddd'] = '111';
$b['eee'] = '222';
$b['fff'] = '333';
$b['ggg'] = '444';
$b['hhh'] = '555';
$b['iii'] = '666';
$b['jjj'] = '777';

//info();


$p = IN::POST();

$IN = new IN();
//$A = $IN->PMinus(array('ddd', 'iii', 'jjj', 'check', 'option','radio'));
//$B = $IN->PAdd(array_keys($b));
//$O = $IN->PSet('wdate', time());


//pre($A);pre($B);pre($O);

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

function radio($ary, $name, $key='', $flag=true) {

	$out = "\n";
	$i= 0;
	foreach($ary as $k=>$v) {

		if ( true != $flag ) {
			$k = $v;
		}

		$m = ($key==$v) ? "checked='checked'" : '';

		$out .= sprintf("<label><input type='radio' name='%s' id='%s' value='%s' %s>%s</label>\n", $name, $k.$i++, $v, $m, $v );
	}

	return $out;

}

function hidden($ary, $visiable=false) {

	$out = "\n";
	$type = ($visiable==true) ? 'text' : 'hidden';
	foreach($ary as $k=>$v) {
		$out.= sprintf("<input type='%s' name='%s' id='%s' value='%s' />\n", $type, $k, $k, $v);
	}

	return $out;

}

function alert_back($msg,$title)
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