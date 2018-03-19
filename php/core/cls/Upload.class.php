<?php

include "function.php";
include "IN.class.php";

//echo realpath('C:\\Users\\home\\AppData\\..\\') . PHP_EOL;

//$IN = new IN();

$POST= IN::POST();
$GET = IN::GET();

	
class myException extends Exception {

    private $params;

    public function setParams(array $params) {
        $this->params = $params;
    }

    public function getParams() {
        return $this->params;
    }
}

/*
파일로 업로드 인터페이스
*/
interface CheckUp {
	function type();	// mime 인터페이스
	function size();	// size 설정 기본 100000 : 1M
	function ext();
	function change($file);
}

class BasicUp implements CheckUp {

	function type() {
		return array('image/x-png','image/jpg', 'image/jpe', 'image/jpeg', 'image/pjpeg','image/png');
	}

	function size() {
		//	upload_max_filesize
		return 1000000;//	1M
	}

	function ext() {
		return array('gif', 'jpg', 'jpeg', 'jpe', 'png');
	}

	function change($file) {
		return md5(uniqid(mt_rand(), true)).'_'.$file;
	}
}

class Upload  {

	private $OBJ;
	private $FILES;
	private $path = 'C:\\tmp';
	private $base = 'C:\\tmp';
	private $max = 10;

	function Upload($path='') {

		if ($path) {
			$this->path = $path;
		}

		if ( ! IS::ini('file_uploads') ) {
			die('php.ini file_uploads = off > on');
		}

	}

	function setObj($obj) {
		$this->OBJ = $obj;
		return $this;
	}

	function draw($name='') {

		$this->fileToArray();

		if ($name) {
			return $this->FILES[$name];

		} 
		return $this->FILES;
	}

	public static function getInstance() {
		static $upload_inst =null;
		if (null === $upload_inst) {
			$upload_inst = new Upload();
		}
		return $upload_inst;
	}

	private function fileToArray() {

		//$this->FILES = SE::_clear($_FILES);

		try {

			foreach($_FILES as $key=>$data) {

				$current_upload_size = IS::ini('upload_max_filesize');
				if ( ! is_uploaded_file($data['tmp_name'] )) {

					switch($_FILES[$key]['error']){
						case 0: //no error; possible file attack!
							$msg = "There is no error, the file uploaded with success";
						break;
							case 1: //uploaded file exceeds the upload_max_filesize directive in php.ini
								$msg =  "The uploaded file exceeds the upload_max_filesize directive in php.ini.(current:".$current_upload_size.')';
						break;
							case 2: //uploaded file exceeds the MAX_FILE_SIZE directive that was specified in the html form
								$msg = "The uploaded file exceeds the MAX_FILE_SIZE directive that was specified in the HTML form. (current(".$current_upload_size.')';
						break;
							case 3: //uploaded file was only partially uploaded
								$msg = "The file you are trying upload was only partially uploaded.";
						break;
							case 4: //no file was uploaded
								$msg = "No file was uploaded.";
						break;
							case 6: //Missing a temporary folder
								$msg = "Missing a temporary folder";
						break;
							case 7: //Failed to write file to disk
								$msg = "Failed to write file to disk.";
						break;
							case 8: //Failed to write file to disk
								$msg = "A PHP extension stopped the file upload.";
						break;
						default: //a default error, just in case!  :)
							$msg =  "There was a problem with your upload.";
						break;
					}

					 $e = new myException('Error');

					 $e->setParams(array(
									'is_uploaded_file', 
									$msg,
									$data
									));
						throw $e;
				}

				$data['name'] = SE::remove_invisible_characters($data['name']);


				// 타입 체크
				if ( ! in_array($data['type'], $this->OBJ->type())) {

					 $e = new myException('Error');
					 $e->setParams(array(
									'no matched', 
									$data['type'],
									$this->OBJ->type()
									));
						throw $e;
				}

				//	사이즈 체크
				if ( filesize($data['tmp_name']) >= $this->OBJ->size()) {

					 $e = new myException('Error');
					 $e->setParams(array(
									'large size', 
									filesize($data['tmp_name']),
									$this->OBJ->size()
									));
						throw $e;
				}


				//	확장자체크
				//$ext = end(explode('.', $data['name']));

				//$data['name'] = 'adf%20.php .gif';

				$file = new SplFileInfo($data['name']);
				$ext  = $file->getExtension();



				if ( ! in_array(strtolower($ext), $this->OBJ->ext())) {

					 $e = new myException('Error');
					 $e->setParams(array(
									'not allowed', 
									$ext,
									$this->OBJ->ext()
									));
						throw $e;
				}

				//	파일 변환
				$i =0;
				$f = true;
				do {

					$name = $this->OBJ->change( $data['name'] );
					$filepath = $this->path . DIRECTORY_SEPARATOR . $name;
		
					if (!IS::exists($filepath) || $i>$this->max) {
						$f = false;
					}
					$i++;

				} while($f);

				
				if ($i>$this->max) {
					$filepath = $this->path . DIRECTORY_SEPARATOR . md5(uniqid(rand(), true));
				}


				$pwd = dirname($filepath);
				$real_pwd = strtolower(realpath($pwd));
				//	기본 패스 위로 올라가는것 체크
				if ( strcmp(strtolower($this->base), $real_pwd) < 0 ) {
					 $e = new myException('Error');
					 $e->setParams(array(
									'upload path', 
									$real_pwd ,
									$_FILES[$key]
									));
						throw $e;
				}

				//	쓰기권한 체크
				if ( ! is_writable( $pwd )) {
					 $e = new myException('Error');
					 $e->setParams(array(
									'is_writable', 
									$pwd ,
									$_FILES[$key]
									));
						throw $e;
				}

				$data['upload_name'] = $filepath;
	

				move_uploaded_file($data['tmp_name'], $filepath);
				$data['time'] = time();

				$this->FILES[$key] = $data;

			}

		}catch(Exception $e) {
			echo 'Message: ' .$e->getMessage();
			pre($e->getParams());
	
		}
	}
}



/*
업로드 함수
*/
function Upload($name='') {

	/*

	interface CheckUp {

		function type();
		function size();
		function ext();
		function change($file);

	}

	BasicUp 클래스 상속 
	*/
	class PdsUp extends BasicUp implements CheckUp {


		function type() {
			return array_merge(array('application/octet-stream'), parent::type());

		}

		function size() {
			return 2000000;
		}

		function ext() {
			return array_merge(array('ini', 'img'), parent::ext());
		}

		function change($file) {

			return $file;

		}

	}


	//$up = Upload::getInstance()->setObj(new BasicUp())->draw();
	return Upload::getInstance()->setObj( new PdsUp() )->draw($name);

}

$up = Upload();
pre($up);

?>

<script type="text/javascript">
<!--
	
//-->
</script>

<form method="post" action="<?=$_SERVER['PHP_SELF']?>"  ENCTYPE="MULTIPART/FORM-DATA">
	<INPUT TYPE='TEXT' NAME='TEXT' VALUE='TEXT' /><br>
	<INPUT TYPE='FILE' NAME='FILE' VALUE='' /><br>
	<INPUT TYPE='FILE' NAME='FILE1' VALUE='' /><br>
	<!-- <INPUT TYPE='FILE' NAME='FILE[]' VALUE='' /> -->
	<INPUT TYPE='SUBMIT' NAME='SUBMIT'  VALUE='SUBMIT' />
</form>