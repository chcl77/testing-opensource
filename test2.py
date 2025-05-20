from flask import Flask , render_template, request, jsonify, redirect, url_for, make_response
# from mysql.connector import pooling
from dbutils.pooled_db import PooledDB
import pymysql
import jwt
import requests
from bs4 import BeautifulSoup
import requests, urllib.request

app = Flask(__name__)

@app.route('/')
def index() :
    response = requests.get("https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn?AGE=21&KEY=bab1a106f834406d84066a97a809b643&Type=json")
    data = response.json()

    print(data['nzmimeepazxkubdpn'][1]['row'][0]['DETAIL_LINK'])
    # url = data['nzmimeepazxkubdpn'][1]['row'][0]['DETAIL_LINK']
    url = "http://likms.assembly.go.kr/bill/billDetail.do?billId=PRC_S2A5B0Z4A1Y7X1X7F3F3E5F0D9D2C8"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    summary = soup.find('div', {'id' : 'summaryContentDiv'})
    for i in summary.find_all('br') :
        i.replace_with("\n")
    # summ = summary.text.strip()
    # d = summ.split('\n')[4:]
    # # for i in d[0] : print(i) #2칸 공백
    # for i in d
    # sdf = " ".join(d)
    # print(sdf)
    summ = summary.get_text().strip()
    datas = summ.split('\n')[4:]
    datas = [i for i in datas if i != '']
    for i in range(len(datas)) :
        datas[i] = datas[i].lstrip()

    print(datas)
    summ = "\n".join(datas)
    print(summ)


    
    d = data['nzmimeepazxkubdpn'][1]['row'][0]['BILL_NAME']
    return render_template('test.html', data = summ)

@app.route('/laws')
def index1() :
    response = requests.get("http://www.law.go.kr/DRF/lawSearch.do?target=prec&OC=greast0327&query=통신매체&type=JSON")
    data = response.json()
    # print(data)
    d = data['PrecSearch']['prec'][0]
    print(data['PrecSearch']['totalCnt'])
    print(d)
    for i in range(0, 19) :
        print(data['PrecSearch']['prec'][i]['사건명'])
    return render_template("test1.html")


if __name__ == "__main__" :
    app.run('0.0.0.0', port = 3000, debug = True)