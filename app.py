from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import datetime
import jwt
import hashlib
import certifi
from datetime import datetime, timedelta

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.a6f1b.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta
app = Flask(__name__)


SECRET_KEY = 'miniExhibition'


@app.route('/')
def home():
    return render_template('login.html')


# 회원가입
@app.route("/join", methods=["POST"])
def join():
    id_receive = request.form['user_id']
    pwd_receive = request.form['pwd']

    password_hash = hashlib.sha256(pwd_receive.encode('utf-8')).hexdigest()
    doc = {
        "user_id": id_receive,  # 아이디
        "pwd": password_hash,  # 비밀번호
    }
    db.miniExhibition.insert_one(doc)
    return jsonify({'result': 'success'})

# 아이디 중복 확인
@app.route('/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['user_id']
    exists = bool(db.miniExhibition.find_one({"user_id": username_receive}, {'_id': False}))

    return jsonify({'result': 'success', 'exists': exists})


# 로그인
@app.route("/login", methods=["POST"])
def login():
    id_receive = request.form['user_id']
    pwd_receive = request.form['pwd']

    pw_hash = hashlib.sha256(pwd_receive.encode('utf-8')).hexdigest()

    user = db.miniExhibition.find_one({'user_id': id_receive, 'pwd': pw_hash}, {'_id': False})
    print(id_receive)
    print(pwd_receive)
    print(pw_hash)
    print(user)
    if user is not None:
        payload = {
         'id': id_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        print('qwqw')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
