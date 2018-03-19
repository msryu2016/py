<?php

class AreasGetRequest {

	private $fields;
	private $apiParas;
 
	public function getFields() {
		return $this->fields;
	}
	public function setFields($fields) {
		$this->fields = $fields;
	}

	public function getApiParas() {
		return $this->apiParas;
	}
	public function setApiParas($apiParas) {
		$this->apiParas = $apiParas;
	}


}
?>