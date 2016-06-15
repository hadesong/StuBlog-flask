
#coding:utf-8
import sqlite3 , random , os , time
conn=sqlite3.connect('stublog.db')
for i in range(0 ,23):
    title=u"标题"+str(i)
    text=u"正文"+''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(160)))
    timeArray= time.localtime(time.time())
    t = time.strftime("%Y-%m-%d %H:%M:%S" , timeArray)
    sql="insert into blog_write ( title , ctime , ctext) values(?  , ? ,? );"
    conn.execute(sql, (title , t , text))
    conn.commit()
print 'OK'