####StuBlog 简易博客系统

技术涉及: Flask \ js \ Bootstarp \ Ajax \ Sqlite \ Html  \ CSS \ Echarts  

###主要功能

1\文章展示 :

		 ajax 获取分页 , 文章列表上下篇

2\登录后台功能 :

		 若已登录则直接进入后台 , 若访问管理页时未登录重定向到登录页面

3\后台首页展示 : 

		本周访问量,站点访问浏览器(Echarts)(未关联数据..) , 原创文章数目(真实)

4\文章编辑模块 : 

		写文章: 采用bootstrap的js插件弹出编辑框  使用 tinymce 编辑模块编辑文章 , 提交表单后重定向至当前页

		js 写全选\反旋

		批量删除 : 获取复选框所有id, 传入后台后 解析 每一个 ID , 循环删除 后重定向当前页

		修改文章 : 将文章id作为参数传入js 的Ajax , 弹出1秒等待动画后加载带有原文章内容的 文本编辑框

		删除文章 : get提交文章id后删除数据库记录


5\评论管理:
		
		采用 多说 评论插件 ..未用api管理评论....

6\标签管理:
		
		未做

7\系统设置:

		未做

8\账户设置:

		三输入框而已....

9\退出系统:

		清除session
    	session.pop('username' , None)


10\主页搜索框:
	
		未做....


####screenshot
![image](https://github.com/hadesong/StuBlog-flask/raw/master/app/static/screenshot/1.jpg)
![image](https://github.com/hadesong/StuBlog-flask/raw/master/app/static/screenshot/2.jpg)
![image](https://github.com/hadesong/StuBlog-flask/raw/master/app/static/screenshot/3.jpg)
![image](https://github.com/hadesong/StuBlog-flask/raw/master/app/static/screenshot/4.jpg)
![image](https://github.com/hadesong/StuBlog-flask/raw/master/app/static/screenshot/5.jpg)
![image](https://github.com/hadesong/StuBlog-flask/raw/master/app/static/screenshot/6.jpg)
![image](https://github.com/hadesong/StuBlog-flask/raw/master/app/static/screenshot/7.jpg)
