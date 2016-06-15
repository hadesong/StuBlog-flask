#coding:utf-8
from flask import Flask , Blueprint , request 
import sqlite3

duoshuo=Blueprint("ds" , __name__)
base_url="127.0.0.1:22224"
@duoshuo.route('/duoshuo' , methods=['POST' , 'GET'])
def get_duoshuo():
	conn=connent_db()
	if request.method=='POST':
		name=request.form.get('')
	return "duoshuo"

#链接数据库
def connent_db():
    conn = sqlite3.connect('stublog.db')
    create_table(conn ,)
    return conn

#创建表
def create_table(conn):
    sql_create_table ='''
    create table if not exists comment(
    id integer PRIMARY KEY AUTOINCREMENT,
    author_name text not null ,
    author_email text not null ,
    time text not null,
    message text not null,
    ip text 
    );
    '''
    conn.execute(sql_create_table)