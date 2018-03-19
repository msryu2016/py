<?php

//include 'function.php';
include 'form.php';






$text['appkey']= '12129701';

$text['api_soure']= '0';
$text['c_SessionId']= 'k0WDUmi7iD9YI7pTmSC4BFtBb1UYOXEsY3';
$text['format']= 'json';
$text['appkye']= '12129701';
$text['apiCategoryId']= '1';

$text['sip_apiname']= '1';
$text['restId']= '1';
$text['sip_http_method']= 'POST';
$text['codeType']= 'php';
$text['app_key']= '1';
$text['app_secret']= '1';
$text['session']= '';



?>
<head>
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
<script>

$(function() {


});

function send()
{

	var api_soure = document.getElementById('api_soure').value;
	var app_key = document.getElementById('app_key').value;
	var app_secret = document.getElementById('app_secret').value;
	var session = document.getElementById('session').value;
	var codeType = document.getElementById('codeType').value;
	var c_SessionId = document.getElementById('c_SessionId').value;
	var sip_http_method = document.getElementById('sip_http_method').value;
	var ctype = document.getElementById('codeType').value;
	var formData = new Object();
	formData["format"] = document.getElementById('format').value;
	formData["method"] = $('#sip_apiname').val();
	formData["restId"] = restId;
	formData["api_soure"] = api_soure;
	formData["app_key"] = app_key;
	formData["app_secret"] = app_secret;
	formData["sip_http_method"] = sip_http_method;
	formData["codeType"] = codeType;
	formData["c_SessionId"] = c_SessionId;



	if ('undefined' != typeof(apiParamArr)){
		for (var i = 0; i < apiParamArr.length; i++){
			formData[apiParamArr[i].name] = document.getElementById("apiParam_"+apiParamArr[i].name).value;
		}
	}
	formData["session"] = session;
//	formData["ua"] = ua;

	var hasSelectFile = false;
	var fileList = [];


	jQuery.ajax({
		url : 'http://open.taobao.com/apitools/getResult.do',
		type : "post",
		data : formData,
		contentType : ctype,
		dataType : "json",
		success : function(result) {
			handleApiResponse(result, selectedApiName);
			flashCheckCode();
		}
	});
	}

function handleApiResponse(result, api) {
	if (!result["success"]) {
		alert(result["message"]);
		return false;
	}

	var codeType = result["codeType"];
	var sampleCode = result["sampleCode"];
	var request = result["request"];
	var response = result["response"];



	$("#param").val(request);
	$("#resultShow").val(response);
	$("#sampleCode").val(sampleCode);

	



}

</script>
</head>
<body>

<form method='post' name='frm' id='frm' >
<?php

echo hidden($text);
?>
<select name="sip_apiname" id="sip_apiname" style="width:195px;">
	<option value="21348">taobao.user.buyer.get</option>
	<option value="21349">taobao.user.seller.get</option>
	<option value="21428">taobao.mixnick.get</option>
	<option value="24357">alibaba.wholesale.user.get</option>
	<option value="24410">taobao.mixnick.change</option>
	<option value="24672">taobao.opensecurity.uid.get</option>
	<option value="24673">taobao.opensecurity.isv.uid.get</option>
	<option value="24675">taobao.opensecurity.uid.change</option>
	<option value="24819">taobao.open.account.delete</option>
	<option value="24820">taobao.open.account.update</option>
	<option value="24821">taobao.open.account.create</option>
	<option value="24825">taobao.lbs.users.get</option>
	<option value="24826">taobao.lbs.user.distance.get</option>
	<option value="24848">taobao.open.account.list</option>
	<option value="25157">taobao.open.account.search</option>
	<option value="25270">taobao.open.account.token.validate</option>
	<option value="25271">taobao.open.account.token.apply</option>
	<option value="25294">taobao.user.baichuan.recommend.get</option>
	<option value="25587">taobao.trade.waimai.confirmorder</option>
	<option value="25596">taobao.open.sms.sendvercode</option>
	<option value="25597">taobao.open.sms.checkvercode</option>
	<option value="25598">taobao.open.sms.sendmsg</option>
	<option value="25869">taobao.open.account.index.find</option>
	<option value="25940">taobao.data.wifidevice.list</option>
	<option value="25966">taobao.open.sms.rmdelaymsg</option>
	<option value="25969">taobao.data.wifi.put</option>
	<option value="25978">alibaba.aliqin.flow.wallet.check.balance</option>
	<option value="26027">taobao.open.sms.batchsendmsg</option>
	<option value="26303">taobao.user.avatar.get</option>
	<option value="27436">tmall.service.settleadjustment.modify</option>
</select>
<input type="button" name="" value="submit" onclick='send();' />
</form>

<?=hshow();?>

<textarea name='param' id='param'></textarea>
<textarea name='resultShow' id='resultShow'></textarea>
<textarea name='sampleCode' id='sampleCode'></textarea>
</body>