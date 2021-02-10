
var token='';

function resize()
{
	var heights = window.innerHeight;
	$("#result").height(heights*0.9);
}

window.onresize = function() {
	resize();
};

function escapeHtml(text) {
  var map = {
	'&': '&amp;',
	'<': '&lt;',
	'>': '&gt;',
	'"': '&quot;',
	"'": '&#039;'
  };

  return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

var randomString = function(length) {
    var text = "";
    var possible = "ABCDEF0123456789";
    for(var i = 0; i < length; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}

function buildError(xhr, status, error_thrown){
	var text = "";
	text	=	text	+	"<table>";
	text	=	text	+	"	<tr>";
	text	=	text	+	"		<td>";
	text	=	text	+	"          Ошибка:  "+escapeHtml(status);
	text	=	text	+	"		</td>";
	text	=	text	+	"	</tr>";
	text	=	text	+	"</table>";
	return text;
}

function buildRez(obj)
{
	var text = "";
	text	=	text	+	"<table>";
	text	=	text	+	"	<tr>";
	text	=	text	+	"		<td>";
	text	=	text	+	"          Статус:  "+escapeHtml(obj.status.message);
	text	=	text	+	"		</td>";
	text	=	text	+	"	</tr>";
	text	=	text	+	"	<tr>";
	text	=	text	+	"		<td>";
	text	=	text	+	"<b>			Текущая задача:<b>";
	text	=	text	+	"		</td>";
	text	=	text	+	"	</tr>";
	text	=	text	+	"	<tr>";
	text	=	text	+	"		<td>";
	text	=	text	+	"			Всего:	"+obj.totals_for_task.total;
	text	=	text	+	"		</td>";
	text	=	text	+	"	</tr>";
	text	=	text	+	"	<tr>";
	text	=	text	+	"		<td>";
	text	=	text	+	"			Есть ИНН:	"+obj.totals_for_task.has_inn;
	text	=	text	+	"		</td>";
	text	=	text	+	"	</tr>";
	text	=	text	+	"	<tr>";
	text	=	text	+	"		<td>";
	text	=	text	+	"			Нет ИНН:	"+obj.totals_for_task.no_inn;
	text	=	text	+	"		</td>";
	text	=	text	+	"	</tr>";
	text	=	text	+	"	<tr>";
	text	=	text	+	"		<td>";
	text	=	text	+	"			Обработано:	"+obj.totals_for_task.processed;
	text	=	text	+	"		</td>";
	text	=	text	+	"	</tr>";
	text	=	text	+	"	<tr>";
	text	=	text	+	"		<td>";
	text	=	text	+	"			К обработке:	"+obj.totals_for_task.to_process;
	text	=	text	+	"		</td>";
	text	=	text	+	"	</tr>";
	text	=	text	+	"	<tr>";
	text	=	text	+	"		<td>";
	text	=	text	+	"<b>			Все задачи:<b>";
	text	=	text	+	"		</td>";
	text	=	text	+	"	</tr>";
	text	=	text	+	"	<tr>";
	text	=	text	+	"		<td>";
	text	=	text	+	"			Всего:	"+obj.totals.total;
	text	=	text	+	"		</td>";
	text	=	text	+	"	</tr>";
	text	=	text	+	"	<tr>";
	text	=	text	+	"		<td>";
	text	=	text	+	"			Есть ИНН:	"+obj.totals.has_inn;
	text	=	text	+	"		</td>";
	text	=	text	+	"	</tr>";
	text	=	text	+	"	<tr>";
	text	=	text	+	"		<td>";
	text	=	text	+	"			Нет ИНН:	"+obj.totals.no_inn;
	text	=	text	+	"		</td>";
	text	=	text	+	"	</tr>";
	text	=	text	+	"	<tr>";
	text	=	text	+	"		<td>";
	text	=	text	+	"			Обработано:	"+obj.totals.processed;
	text	=	text	+	"		</td>";
	text	=	text	+	"	</tr>";
	text	=	text	+	"	<tr>";
	text	=	text	+	"		<td>";
	text	=	text	+	"			К обработке:	"+obj.totals.to_process;
	text	=	text	+	"		</td>";
	text	=	text	+	"	</tr>";
	text	=	text	+	"</table>";
	return text;
}

function inputCaptcha(){
	var $item = $(this);
	value = $item.val();
	if (value.length == 6){
		$.ajax({
		  type: 'PUT',
		  timeout: 0,
		  url: "/api/v1/honor/person/by_captcha/"+value+"/"+token,
		  context: document.body
		}).done(function( data ) {
			if(data.status.status!="ok"){
				if (data.status.status=="done"){
					$("#isError").text("Завершено")
				}else
				if (data.status.status=="no data"){
					$("#isError").text("Нет данных")
				}

				$("#isError").show();
				$("#isOK").hide();
			}
			else
			{
				$("#isOK").show();
				$("#isError").hide();
			}
			
			$("#result").html(buildRez(data));
			
			refreshCaptcha();
			$item.val("");
		}).fail(
			function(xhr, status, error_thrown){
				$("#isError").show();
				$("#isOK").hide();

				$("#result").html(buildError(xhr, status, error_thrown));
				
				refreshCaptcha();
				$item.val("");
			}
		)		  
	}
	else{
		$("#isError").hide();
		$("#isOK").hide();
	}

}

function inputCsvUpload(){
	var file_data = $('#csvUpload').prop('files')[0];   
	$('#csvFileName').text(file_data.name);
	$('#divUpload').attr('class','control is-loading');

	var form_data = new FormData();                  
	var now = new Date();

	form_data.append('dt', now.toISOString());
	form_data.append('state', 'новая');
	form_data.append('file', file_data);

	$.ajax({
		type: 'POST',
		timeout: 0,
		url: "/api/v1/honor/task/",
		context: document.body,
		contentType: false,
		processData: false,
		data: form_data
	  }).done(function( data ) {
  			$('#divUpload').attr('class','control');
  		  	$('#csvFileName').text("");
		}).fail(
			function(xhr, status, error_thrown){
				$('#divUpload').attr('class','control');
  		  		$('#csvFileName').text("");
		  	}
	  )		  

	// $.ajax({
	// 	url: "pro-img-disk.php",
	// 	type: "POST",
	// 	data: form_data,
	// 	contentType: false,
	// 	cache: false,
	// 	processData:false,
	// 	success: function(data){
	// 		console.log(data);
	// 	}
}

function downloadTaskInnsAsFile(task_id){
	$.ajax({
		type: 'GET',
		timeout: 0,
		url: "/api/v1/honor/people/good/by_task_id/"+task_id,
		headers:{ 'Accept': 'text/csv',
		          'Content-Type': 'text/csv' },		
		context: document.body
	  }).done(function( data ) {
		  alert(data);
		}).fail(
			function(xhr, status, error_thrown){
				alert("error");
		  	}
	  )		  

}


$(function(){
	$( "#code" ).mask('000000');
	$(document).on('input', '[id="code"]', inputCaptcha);
	$('#csvUpload').change(inputCsvUpload);
		
	resize();
	$( "#code" ).focus();
	refreshCaptcha()
});

function refreshCaptcha(){
	$.get( "/api/v1/honor/token/", function( data ) {
					token=data;
					$("#capthcaImg").html("<img src='https://service.nalog.ru/static/captcha.html?a="+data+"'/>");
				});
}



