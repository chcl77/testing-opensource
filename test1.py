from flask import Flask , render_template ,request, jsonify, redirect, url_for, make_response
# from mysql.connector import pooling
from dbutils.pooled_db import PooledDB
import pymysql
import jwt

secret_key = "1234"

#db pool 생성
pool = PooledDB(
    creator = pymysql,
    maxconnections = 20,
    mincached = 10 ,
    blocking = True,
    host = "127.0.0.1",
    user = "root",
    password = "102512as",
    database = "first_db"
)

# query = "select * from users"
# cursor.execute(query)
# row = cursor.fetchall()
# print(row)

app = Flask(__name__)

@app.route("/")
def index():
    return "hello worlds"

@app.route("/index")
def show():
    return render_template('index.html')

@app.route("/signup" , methods = ['GET'])
def signup():
    return render_template('signup.html')

@app.route("/process/adduser" , methods = ['POST'])
def signups():
    try : 
        conn = pool.connection()
        cursor = conn.cursor()

        pid = request.form['id']
        pword = request.form['pword']
        pname = request.form['name']
        page = request.form['age']
        print(pid + " " + pword + " " + page + " " + pname)
        cursor.execute("insert into users values(%s ,%s,%s ,%s)", (pid, pname, page, pword) )
        conn.commit()
        conn.close()
        return "success to add te user"
    except Exception as e :
        return "error" 

@app.route("/login", methods = ['GET'])
def login() : 
    return render_template("login.html")

@app.route("/index/<username>", methods = ['GET'])
def index1(username) : 
    return "Hello " + username

@app.route("/process/login", methods = ['POST'])
def logins() : 
    pid = request.form['id']
    pword = request.form['password']
    conn = pool.connection()
    cursor = conn.cursor()
    print(pid + " " + pword)
    cursor.execute("select * from users where id = %s", (pid, ))
    ls = cursor.fetchall()
    conn.close()
    print(len(ls))
    if len(ls) > 0 :
        if ls[0][3] == pword :
            payload = {
                "id" : pid
            }
            token = jwt.encode(payload, secret_key, algorithm="HS256")
            res = make_response("Login Success")
            res.set_cookie('token', token)
            return res
            # return redirect(url_for('index1', username = pid))
        else :
            return "Wrong Password"
    else :
        return "there is no data"
        

@app.route("/getdb", methods = ['POST'])
def getdb():
    data = request.get_json()
    check_id = data['id']
    print(check_id)
    reply = {
        'chk' : "none"
    }
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute("select * from users where id = %s", (check_id, ))
    result = cursor.fetchall()
    conn.close()
    print(result)
    if len(result) > 0 :
        reply['chk'] = "Duplicate"
    elif len(result) == 0 :
        reply['chk'] = "ok"
    else :
        reply['chk'] = "err"
    return jsonify(reply)



@app.route("/getdata", methods = ['POST'])
def shows():
    inp = request.form['data']
    return inp

if __name__ == "__main__" :
    app.run('0.0.0.0', port = 3000, debug = True)
