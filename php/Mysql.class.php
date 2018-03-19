<?php

interface DB {
	public function row($sql);
	public function rows($sql);
	//private function obj();
	//private function objs();
	public function one($sql);
}

class MySQL implements DB {

	private $conn = null;
	private $link = null;
	private $charset = 'utf8';

	private $pot = array();

	private $history = array();


	function __construct($host, $user, $pass, $db) {
		$this->pot['host'] = $host;
		$this->pot['user'] = $user;
		$this->pot['pass'] = $pass;
		$this->pot['db'] = $db;

		$this->connect();
		unset($this->pot['pass']);
		
	}

	function __destruct() {
		if (is_resource($this->link)) mysqli_close($this->link);
	}

	public function setDb($db) {
		return $this->pot['db'] = $db;
	}

	public function getDb() {
		return $this->pot['db'];
	}

	public function getCharSet() {
		return $this->charset;
	}

	public function setCharSet($char) {
		$this->charset = $char;
	}

	public function selectDb($db) {
		if ( ! mysqli_select_db($this->link, $db) ) {
			throw new Exception('Could not select db to MySQL database.');
		}
	}

	public function connect() {
		
		if (!is_resource($this->link) || empty($this->link)) {
			if (($link = mysqli_connect($this->pot['host'], $this->pot['user'], $this->pot['pass']) )) {
				$this->link = $link;

				$this->selectDb($this->getDb());
			
				mysqli_set_charset($this->link, $this->getCharSet());
			} else {

				throw new Exception('Could not connect to MySQL database.');
			}

		}

		return $this->link;
	}

	public function show() {
		echo '<pre>';
		print_r($this->history);
		echo '</pre>';
	}

	public function query($sql) {

		$ret = mysqli_query($this->link,$sql);
		$this->history[] = $sql;
		if (!$ret)  {
			die('Error executing MySQL query: '.$sql.'. MySQL error '.mysqli_errno($this->link).': '.mysqli_error($this->link));
			//throw new Exception('Could not query:' . mysql_error());
			//throw new Exception('Error executing MySQL query: '.$sql.'. MySQL error '.mysqli_errno($this->link).': '.mysqli_error($this->link));
		}

		return $ret;

	}

	public function row($sql) {

		$ret = $this->query($sql);
		$row = mysqli_fetch_assoc($ret);
		mysqli_free_result($ret);

		return $row;
	}

	public function rows($sql) {

		$ret = $this->query($sql);
		$rows = array();
		while($row = mysqli_fetch_assoc($ret)) {
			$rows[] = $row;
		}
		mysqli_free_result($ret);

		return $rows;
	}

	public function one($sql) {

		$ret = $this->query($sql);
		$one = mysqli_fetch_row($ret);
		mysqli_free_result($ret);

		return $one;
	}


	public function update($tb, $data, $where='') {

		if ( $where == '' ) {
			throw new Exception('no where');
		}

		$fields = array();
		
		foreach($data as $col=>$val) {
			$fields[] = sprintf("`%s`='%s'", $col, mysql_real_escape_string($val));	
		}

		if (is_array($where))
		{
			$_where = array();
			foreach($where as $col=>$val) {
				$_where[] = sprintf("`%s`='%s'", $col, mysql_real_escape_string($val));	
			}

			$_WHERE = implode(' AND ', $_where);
		} else {

			$_WHERE = $where;

		}


		$sql = sprintf("UPDATE %s SET %s WHERE %s", $tb, implode(',', $fields), $_WHERE);

		$this->query($sql);

	}

	public function insert($tb, $data) {

		$fields = array();
		$values = array();
		foreach($data as $col=>$val) {
			$fields[] = sprintf("`%s`", $col);
			$values[] = sprintf("'%s'", mysql_real_escape_string($val)); 
		}

		$sql = sprintf("INSERT INTO %s (%s) VALUES (%s)", $tb, implode(',', $fields), implode(',', $values));

		$this->query($sql);

		return mysqli_insert_id();
	}


}	//end of class : MySQL


/*



function localDB()
{
	$m = new MySQL('localhost', 'root', 'roottoor', 'dcg');
	return $m;
}

//$r = $m->query('create table a (aa varchar(10), bb varchar(10));');
$m = localDB();

$aa = array();
$aa['aa'] = '1';
$aa['bb'] = '2';

//$id = $m->insert('a', $aa);

//echo "insert_id : ".$id."<br />";

$m->update('a', $aa, 'aa="1"');

$m->update('a', $aa, array('aa'=>'2', 'bb'=>'2'));
$rows = $m->rows('select * from a');

print_r($rows);

$m->show();


$rows = array();
$rows['a'] = 'asdfg';
$rows['b'] = array('c'=>1, 'd'=>2);

$x = xml('<root/>', $rows);
print_r($x->asXml());

*/





?>
