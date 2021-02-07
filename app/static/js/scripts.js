
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

$(function(){
	$( "#code" ).mask('000000');
	$(document).on('input', '[id="code"]', function () {
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
	});
	
	$('[id="code"]').keypress(function (e) {
	  if (e.which == 13) {
		if($("#addCodeButton").prop('disabled')==false){
			addCode();
		}
	  }
	});
	
	
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

