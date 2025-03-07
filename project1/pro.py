import pymysql
def make_connection():
    cn=pymysql.connect(host="localhost",port=3306,db="dimple",user="root",password="",autocommit=True)
    cur=cn.cursor()
    return cur

def check_photo(email):
    photo="no"
    cur=make_connection()
    sql="select * from photodata where email='"+email+"'"
    cur.execute(sql)
    n=cur.rowcount
    if(n>0):
        data =cur.fetchone()
        photo=data[1] #fetch photo file name from index 1
    return photo

