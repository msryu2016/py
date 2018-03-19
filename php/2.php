<?php

header("Content-type: text/html; charset=utf-8");


include "../php/function.php";
include "TopSdk.php";


prt();
//After extracting the downloaded SDK, change the value of $gatewayUrl in Line 8 of TopClient.php in the top to the sandbox address: http://gw.api.tbsandbox.com/router/rest,

     //In formal environment, the address should be set as: http://gw.api.taobao.com/router/rest

 

//instantiation of TopClient class

$c = new TopClient;

$c->appkey = "23239811";

$c->secretKey = "402947d17819d3be1cf702ce75635f9e";

$sessionkey= "6100223190a99372228ecc5576bee7d1cc84d6140495fce2639736697";   // for example: the sessionkey obtained after authorization of sandbox test account sandbox_c_1

//instantiation of Request class corresponding to specific API

$req = new UserSellerGetRequest;

$req->setFields("nick,user_id,type");

//$req->setNick("sandbox_c_1");

 

// execute API request and print the result

$resp = $c->execute($req,$sessionkey);

echo "result:";

print_r($resp);

?>