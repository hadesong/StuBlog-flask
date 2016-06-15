#coding:utf-8
from app import app
from flask import render_template , request ,redirect , flash , session , url_for
import hashlib
from functools import wraps
import sqlite3 , time
from duoshuo import duoshuo

app.register_blueprint(duoshuo)

@app.errorhandler(404)
def page_not_found(value):
    return render_template('404.html')

@app.route('/index')
def index_():
    return redirect('/')

@app.route('/' , methods=['POST' , 'GET'])
def indexp():
    page_size=4
    html=''
    page_now=0
    if request.method=='POST':
        page_now=int(request.form.get('page_now'))
        con = select_page(page_size , page_now)
        end_page=None
        conn=connent_db()
        end_page_sql="select count(id) from blog_write"
        cursor=conn.execute(end_page_sql)
        for row in cursor:
            end_page=row[0]

        for row in con:
            h='''
            <div class="well" style="position:relative;overflow: auto; ">
                <h3 style=""><a href="post?id=%s">
                <span class="glyphicon glyphicon-bookmark"></span> %s</a></h3>
                <h5 style="margin-left:30px;word-wrap: break-word; word-break: normal; " >%s</h5>
                <h6 style="float:right"><span class="glyphicon glyphicon-time">&nbsp;</span>%s</h6>
            </div>

            '''%(row[0],row[1],row[3][0:150],row[2])
            html+=h
        nav=u'''
            <nav>
                <ul class="pager">
                <li><a href="javascript:prev_p()">上一页</a></li>
                <li><a href="javascript:next_p()">下一页</a></li>
                </ul>
            </nav>
                '''
        if page_now>(end_page/page_size-1):
            nav=u'''
                <nav>
                    <ul class="pager">
                    <li><a href="javascript:prev_p()">上一页</a></li>
                    </ul>
                </nav>
                    '''
        if page_now==0:
            nav=u'''
                <nav>
                    <ul class="pager">
                    <li><a href="javascript:next_p()">下一页</a></li>
                    </ul>
                </nav>
                    '''
        return html+nav
    connent=select_page(page_size , 0)
    return render_template('index.html', connent=connent )


def select_page(page_size , page_now):
    sql_select_page="select * from blog_write order by id desc limit ? OFFSET ?;"
    conn=connent_db()
    connent=conn.execute(sql_select_page , (page_size , page_size*page_now))
    return connent







@app.route('/login' , methods=['POST' , 'GET'])
def login():
    '''
    表单提交过来的用户名和密码是明文的   需要防止被截获取(重放攻击)
    使用HTTPS

    或在前端加密 , 后端再次加密
        前端先加密密码后 加上验证码再次加密 ,
        后端吧验证码与数据库加密过的密码对比(由于验证码是一次性的 所以无法重放)
    '''
    ##验证提交
    if request.method == 'POST':
        userTemp = request.form.get('username')
        pawdTemp = hashlib.md5(request.form.get('password')).hexdigest()
        #pawdTemp = request.form.get('password')
        if userTemp==app.config['USERNAME'] and pawdTemp==app.config["PASSWORD"]:
            session['username']=userTemp
            return redirect('/admin')
        else:
            flash(u"用户名或密码错误")
            return render_template('login.html')
    if 'username' in session:
        return redirect('/admin')
    return render_template('login.html')









#登录验证 
#回话开始前验证 , 省去每个路由都添加装饰器
'''
## 存在缺陷.. 当请求404时 , 会重定向到login 而不是  404 ..
@app.before_request
def login_required():
    # 如果不在 session中  且 请求的endpoint 不是 index login(防止无限302)
    # endpoint 视图函数的 名称 ,  
    if 'username' not in session and request.endpoint not in ('index', 'login' ,'post' ) :
        return redirect(url_for('login'))
'''
## 登录验证 函数
## 问题....wraps 是什么鬼
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in  session:
            return redirect(url_for('login'))
        return f(*args , **kwargs)
    return decorated_function
#-------------------------------------后台部分
#后台首页 
@app.route('/admin')
@login_required
def admin():
    conn = connent_db()
    sql="select count(id) from  blog_write;"
    cursor=conn.execute(sql)
    for row in cursor:
        postnumber=row
    return render_template('admin_home.html' , postnumber=postnumber[0])


#文章管理
@app.route('/admin_post' , methods=['POST' , 'GET'])
@login_required
def admin_post():
    connent=select_text()
    return render_template('admin_post.html' , connent=connent)

#评论管理 
@app.route('/admin_comment' , methods=['POST' , 'GET'])
@login_required
def admin_comment():
    return render_template('admin_comment.html')

#标签管理
@app.route('/admin_tags' , methods=['POST' , 'GET'])
@login_required
def admin_tags():
    return render_template('admin_tags.html')

#系统设置
@app.route('/admin_system' , methods=['POST' , 'GET'])
@login_required
def admin_system():
    return render_template('admin_system.html')

#用户管理
@app.route('/admin_user' , methods=['POST' , 'GET'])
@login_required
def admin_user():
    return render_template('admin_user.html')

#登出
@app.route('/admin_logout' , methods=['POST' , 'GET'])
def admin_logout():
    session.pop('username' , None)
    return redirect('/')

#写文章
@app.route('/write' , methods=['POST' , 'GET'])
@login_required
def write():
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text') 
        timeArray= time.localtime(time.time())
        t = time.strftime("%Y-%m-%d %H:%M:%S" , timeArray)
        conn = connent_db()
        insert_text(conn , title , t , text)
    return redirect('admin_post')


#修改文章
@app.route('/modify' , methods=['POST' , 'GET'])
@login_required
def modify():
    if request.method=='POST':
        id = request.form.get('id')
        conn=connent_db()
        sql="select * from blog_write where id=%s"%id
        cursor=conn.execute(sql)
        content=[]
        for row in cursor:
            content.append(row)

        html=u'''
    <form action="save_modify" method="post">
        <div class="modal fade bs-example-modal-lg" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel">
            <div class="modal-dialog modal-lg" style="width:90%%">
                <div class="modal-content">
                    <input type="text"  hidden='hidden' name='hidden_id' value='%s'>
                    <h2 style="margin-left: 40px; width:40%%"><b>修改文章</b></h2>
                    <input type="text" class="form-control" name="title" style="margin-left: 40px; width:40%%" value="%s">
                    <br>
                    <script>
                    tinymce.init({
                        selector: 'textarea'
                    });

                    </script>
                    <div style="width:93%% ; margin-left:40px;">
                        <textarea style="width:40%%" name="text">%s</textarea>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-primary">Save</button>
                    </div>
                </div>
            </div>
        </div>
    </form>
        '''%(content[0][0], content[0][1] , content[0][3])
        time.sleep(1)
        return html
    return "ERROR"

#保存文章修改
@app.route('/save_modify' , methods=['POST'])
@login_required
def save_modify():
    if request.method=='POST':
        title = request.form.get('title')
        id= request.form.get('hidden_id')
        text= request.form.get('text')
        timeArray= time.localtime(time.time())
        t = time.strftime("%Y-%m-%d %H:%M:%S" , timeArray)
        conn = connent_db()
        sql="update blog_write set title=?  , ctext=? , ctime=? where id=%s;"%id
        conn.execute(sql ,(title , text , t))
        conn.commit()
        return redirect('admin_post')
    return "ERROR"

#删除文章
@app.route('/delete' ,methods=['GET'])
@login_required
def delete_post():
    id = request.args.get('id')
    if id:
        sql="delete from blog_write where id=%s"%id
        conn=connent_db()
        conn.execute(sql)
        conn.commit()
        return redirect('admin_post')
    return redirect('admin_post')


#批量删除文章
@app.route('/delet_all' , methods=['POST' , 'GET'])
@login_required
def delete_all():
    if request.method=='POST':
        id_str=request.form.get('id')
        id_lis=id_str.split("#")
        conn=connent_db()
        for i  in range(len(id_lis)-1):
            sql="delete from blog_write where id=%s;"%id_lis[i]
            conn.execute(sql)
            conn.commit()
        conn.close()
        return "OK"
    return "ERROR"








#------------------------------------------前端部分
#文章详情页
@app.route('/post' , methods=['GET'])
def post():
    id = request.args.get('id')
    if id:
        sql ="select * from blog_write where id=%s"%id
        #查询上一篇id
        previous_sql="select id from blog_write where id < %s order by id desc limit 1"%id
        #查询下一篇id
        next_sql="select id from blog_write where id > %s order by id limit 1"%id
        conn=connent_db()
        cursor = conn.execute(sql)
        p_id_cur = conn.execute(previous_sql)
        n_id_cur = conn.execute(next_sql)

        content= db_list(cursor)
        p_id=db_list(p_id_cur)
        n_id=db_list(n_id_cur)
        if p_id:
            p_id=p_id[0][0]
            previous=u'<li><a href="/post?id=%s"><-旧爱</a></li>'%p_id
        else:
            previous='<li></li>'

        if n_id:
            n_id=n_id[0][0]
            next_=u'<li><a href="/post?id=%s">新欢-></a></li>'%n_id
        else:
            next_='<li></li>'

        if content:
            return render_template('post.html' , content=content , previous=previous ,next=next_)
    return redirect('404')

def db_list(cursor):
    content=[]
    for i in cursor:
        content.append(i)
    return content




#--------------------------------------------数据库部分
#链接数据库
def connent_db():
    conn = sqlite3.connect('stublog.db')
    create_table(conn ,)
    return conn

#创建表
def create_table(conn):
    sql_create_table ='''
    create table if not exists blog_write(
    id integer PRIMARY KEY AUTOINCREMENT,
    title text not null ,
    ctime text not null ,
    ctext text 
    );
    '''
    conn.execute(sql_create_table)

#插入文章
def insert_text(conn , title , t ,  text):
    sql_insert_text ='''
    insert into blog_write ( title , ctime , ctext) values(?  , ? ,? );
    '''
    conn.execute(sql_insert_text , (title , t , text))
    conn.commit()

#查询文章
def select_text():
    conn=connent_db()
#    sql_select_text='''
#    select id , title , ctime , ctext from blog_write order by id desc limit ((%s-1)*%s),%s;
#    '''%(page_num , page_long , page_long)
    sql_select_text='''
    select id , title , ctime , ctext from blog_write  order by id desc;
    '''
    cursor=conn.execute(sql_select_text)
    db_content = []
    for row in cursor:
        db_content.append(row)
    return db_content


@app.route('/check_box_del' , methods=['POST' , 'GET'])
def check_box_del():
    box = request.form.getlist('cbox')
    return str(box)