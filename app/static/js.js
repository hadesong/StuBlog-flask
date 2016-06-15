//文章管理 全选 反旋 文章
function reserveCheck(name) {
	var revalue = document.getElementsByName('checkbox');
	for (i = 0; i < revalue.length; i++) {
		if (revalue[i].checked == true)
			revalue[i].checked = false;
		else
			revalue[i].checked = true;
	}
}


//文章管理 复选框 批量删除确认框
function check() {
	var chk_value = [];
	$('input[name="checkbox"]:checked').each(function() {
		chk_value.push($(this).val() + "#");
	});
	if (chk_value.length == 0) {
		$('#selec_nothing').modal({
			keyboard: true
		});
	} else {
		//把要删除的文章 id#id#id# 字符串写入temp_check_value标签 待提供后台
		$('#temp_check_value').html(chk_value).appendTo("body")
		$('#delet_all').modal({
			keyboard: true
		});

	}
};

//修改文章 Ajax等待动画, 后台传回带有文章内容的html代码 
function func(num) {
	//alert(num);
	$.ajax({
		url: "/modify",
		type: "POST",
		data: {
			"id": num,
		},
		beforeSend: function() {
			$('.load').html('<div class="loader">\
   <div class="loader-inner">\
      <div class="loader-line-wrap">\
         <div class="loader-line"></div>\
      </div>\
      <div class="loader-line-wrap">\
         <div class="loader-line"></div>\
      </div>\
      <div class="loader-line-wrap">\
         <div class="loader-line"></div>\
      </div>\
      <div class="loader-line-wrap">\
         <div class="loader-line"></div>\
      </div>\
      <div class="loader-line-wrap">\
         <div class="loader-line"></div>\
      </div>\
   </div>\
</div>').appendTo("body")
		},
		complete: function(data) {
			$('.load').html('').appendTo("body")

			//$('.load').remove();
		},
		success: function(data) {
			//获取后台的结果替换modify_span标签
			$('#modify_span').html(data);
			$('#myModal').modal({
				keyboard: true
			});
			//移动到页面顶部(ajax在页面下端获取数据后不刷新 ,导致页面是从中间开始的 ..)
			//            $('body,html').animate({
			//                scrollTop: 0
			//            }, 1000);
		},
		error: function(data) {
			alert("数据异常！");
		}
	});
}

//文章管理 提交文章id字符串 , 删除已选文章
$(document).ready(function() {
	$("#s_delet_all").click(function() {
		var v = document.getElementById('temp_check_value').innerHTML
		$.post("/delet_all", {
				id: v
			},
			function(data, status) {
				if (data == "OK") {
					location.reload(location.href)
				} else {
					alert("未知错误 , 请重试");
					location.reload(location.href);
				}
			});
	});
});


//<!-- 多说公共JS代码 start (一个网页只需插入一次) -->
var duoshuoQuery = {short_name:"mysitehades"};
	(function() {
		var ds = document.createElement('script');
		ds.type = 'text/javascript';ds.async = true;
		ds.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') + '//static.duoshuo.com/embed.js';
		ds.charset = 'UTF-8';
		(document.getElementsByTagName('head')[0] 
		 || document.getElementsByTagName('body')[0]).appendChild(ds);
	})();
//<!-- 多说公共JS代码 end -->