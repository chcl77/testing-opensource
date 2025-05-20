from flask import Flask , render_template ,request, jsonify, redirect, url_for, make_response
# from mysql.connector import pooling
from dbutils.pooled_db import PooledDB
import pymysql
import jwt
import os
from dotenv import load_dotenv

load_dotenv()


#db pool 생성
pool = PooledDB(
    creator = pymysql,
    maxconnections = 3,     
    mincached = 1 ,         
    blocking = True,
    host = "sql5.freesqldatabase.com",
    user = "sql5777334",
    password = os.getenv('DB_password'),
    port = 3306, 
    database = "sql5777334"
)



app = Flask(__name__)

#index page (Main page로 운영할 계획)
@app.route("/")
def index():
    return "hello worlds"


#회원가입 페이지 로드
@app.route("/signup" , methods = ['GET'])
def signup():
    return render_template('signup1.html')

#회원가입 페이지에서 사용자 추가 요청처리
@app.route("/process/adduser" , methods = ['POST'])
def signups():
    try : 
        conn = pool.connection()    # Pool에서 DB connection 생성
        cursor = conn.cursor()      # 커서 생성

        pid = request.form['id']    # 회원가입 form에서 id 할당
        pword = request.form['pword']   # 회원가입 form에서 password 할당
        pname = request.form['name']    # 회원가입 form에서 이름 할당
        page = request.form['age']      # 회원가입 form에서 나이 할당
        print(pid + " " + pword + " " + page + " " + pname) # Debug용, 받아온 아이디, 패스워드, 나이, 이름 출력
        cursor.execute("insert into users values(%s ,%s,%s ,%s)", (pid, pname, page, pword) )   #DB에서 query문 실행, users 테이블에 받아온 값 입력
        conn.commit()   # DB 변경 사항 저장
        conn.close()    # DB connection 해제
        return "success to add the user"    # 성공 시 성공 메세지 (이후에는 메인페이지로 리다이렉트 할 예정)
    except Exception as e :
        return "error"  # 예외발생 시 에러 메세지 
    
#로그인 페이지 로드
@app.route("/login", methods = ['GET'])
def login() : 
    return render_template("login.html")


# 로그인 페이지에서 로그인 요청처리
@app.route("/process/login", methods = ['POST'])
def logins() : 
    pid = request.form['id']    # 로그인 form에서 id 할당
    pword = request.form['password']    # 로그인 form에서 password 할당
    conn = pool.connection()    # Pool에서 DB connection 생성
    cursor = conn.cursor()      # 커서 생성
    print(pid + " " + pword)    # Debug 용
    cursor.execute("select * from users where id = %s", (pid, ))    # DB에서 query문 실행, users 테이블에서 입력한 id와 동일한 row 확인 
    ls = cursor.fetchall()  # 확인한 결과를 ls에 저장
    conn.close()   # DB connection 해제
    print(ls)   #Debug 용
    if len(ls) > 0 :    # ls가 0 이상이면 해당하는 사용자가 존재
        if ls[0][3] == pword :  # ls[0][3]에 저장된 사용자의 pw가 존재, 입력한 pw와 일치 시, 사용자 확인 완료 
            payload = {     # 사용자 인증 토큰 발행을 위한 페이로드 
                "id" : pid
            }
            token = jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm="HS256")     # jwt를 사용하여 토큰 발행
            res = make_response("Login Success")    # response 생성
            res.set_cookie('token', token)      # response의 cookie에 토큰 할당
            return res  # response 반환 (이후 메인 페이지로 리다이렉트 할 예정)
            # return redirect(url_for('index1', username = pid))
        else :
            return "Wrong Password"     # pw가 다르면 잘못된 pw 메세지 반환
    else :
        return "there is no data"       # ls가 없으면 해당하는 사용자가 없음을 반환
        
#회원가입 페이지에서 아이디 중복 확인 요청 처리
@app.route("/getdb", methods = ['POST'])
def getdb():
    data = request.get_json()   # 회원가입 페이지에서 보낸 request 수신
    check_id = data['id']       # request에 들어있는 id 할당
    print(check_id)
    reply = {                   # 회신을 위한 object 생성
        'chk' : "none"
    }
    conn = pool.connection()    # Pool에서 DB connection 생성
    cursor = conn.cursor()      # 커서 생성
    cursor.execute("select * from users where id = %s", (check_id, )) # DB에서 query문 실행, users 테이블에서 check_id와 동일한 row 확인 
    result = cursor.fetchall() # 확인한 결과를 result에 저장
    conn.close()    # DB 연결 해제
    print(result)
    if len(result) > 0 :    # result가 0 이상이면 이미 기존 사용자가 존재
        reply['chk'] = "Duplicate"  # reply의 chk에 duplicate
    elif len(result) == 0 : # result가 0이면 아이디 중복 없음
        reply['chk'] = "ok"
    else :                  # 이외에는 error
        reply['chk'] = "err"
    return jsonify(reply)   # 회원가입 페이지로 회신



@app.route("/getdata", methods = ['POST'])
def shows():
    inp = request.form['data']
    return inp

if __name__ == "__main__" :
    app.run('0.0.0.0', port = 3000, debug = True)
