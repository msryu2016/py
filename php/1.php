<?
include 'function.php';



$a = (isset($_GET['a'])) ? $_GET['a'] : '';

if ($a)
{

	$sql = "SELECT * FROM a WHERE aa='".$a."'";

	$m = localDB();

	$rows = $m->rows($sql);

	pre($rows);

}
?>