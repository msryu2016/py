<?php
include "function.php";

class SQLite extends SQLite3 {

	private $dbfile = null;

	private $history = array();

	function __construct($path = '')
	{

		//if (!file_exists($path)) {
			$this->dbfile = $path;
			$this->open($this->dbfile);
		//}
		
	}

	function __destruct() {
		$this->close();
	}

	function row( $sql ) {

		$rs = $this->query($sql);

		$row = $rs->fetchArray(SQLITE3_ASSOC);

		return $row;
	}

	function rows( $sql ) {
		$rs = $this->query($sql);

		$rows = array();
		while($row = $rs->fetchArray(SQLITE3_ASSOC)) {
			$rows[] = $row;
		}

		return $rows;
	}

	public function show() {
		echo '<pre>';
		rsort($this->history);
		print_r($this->history);
		echo '</pre>';
	}


	function one( $sql ) {
		return $this->querySingle( $sql );
	}

	function tables($where='') {

		$sql = "SELECT * FROM sqlite_master $where";

		return $this->rows($sql);
	}


	public function query($sql)
	{
		$this->history[] = $sql;
		$rs = parent::query($sql);

		if (!$rs) {
			throw new Exception('Error executing MySQL query: '.$sql.'. MySQL error '.$this->lastErrorMsg().': '.$this->lastErrorCode());
		}
		return $rs;
	}

	public function exec($sql) {
		$this->history[] = $sql;
		$rs = parent::exec($sql);

		if (!$rs) {
			throw new Exception('Error executing MySQL query: '.$sql.'. MySQL error '.$this->lastErrorMsg().': '.$this->lastErrorCode());
		}

		return $rs; 

	}


	public function update($tb, $data, $where='') {

		if ( $where == '' ) {
			throw new Exception('no where');
		}

		$fields = array();
		
		foreach($data as $col=>$val) {
			$fields[] = sprintf("`%s`='%s'", $col, $this->escapeString ($val));	
		}



		if (is_array($where))
		{
			$_where = array();
			foreach($where as $col=>$val) {
				$_where[] = sprintf("`%s`='%s'", $col, $this->escapeString ($val));	
			}

			$_WHERE = implode(' AND ', $_where);
		} else {

			$_WHERE = $where;

		}


		$sql = sprintf("UPDATE %s SET %s WHERE %s", $tb, implode(',', $fields), $_WHERE);

		$this->exec($sql);

	}

	public function insert($tb, $data) {

		$fields = array();
		$values = array();
		foreach($data as $col=>$val) {
			$fields[] = sprintf("`%s`", $col);
			$values[] = sprintf("'%s'", $this->escapeString($val)); 
		}

		$sql = sprintf("INSERT INTO %s (%s) VALUES (%s)", $tb, implode(',', $fields), implode(',', $values));

		$this->exec($sql);

		return $this->lastInsertRowID();
	}
	/*

	public function crateFunction() {

		function my_udf_md5($string) {
			return md5($string);
		}

		$db->createFunction('my_udf_md5', 'my_udf_md5');
var_dump($db->querySingle('SELECT my_udf_md5("test")'));

	}
*/
}

$db = new SQLite('1.db');
//$db->exec("drop table foo");
$db->exec("create table if not exists foo (bar STRING, wdate datetime )");





//$db->exec("INSERT INTO foo (bar) VALUES ('This is a test')");
//$db->insert('foo', array('bar'=>'123123', 'wdate'=>time()));

$result = $db->rows("SELECT *, datetime(wdate,'unixepoch') as utc FROM foo order by wdate DESC");

pre($result);



pre($db->tables());

pre($db->show());

?>