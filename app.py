from flask import Flask, render_template, request, jsonify, url_for, redirect
from pymongo import MongoClient
import requests
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


# 메인페이지
@app.route('/')
def home():
    rows = post_list = list(db.post.find({}, {'_id': False}))
    return render_template('index.html', rows=rows)


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

    if user is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# 메인페이지 게시글 표시
@app.route("/posting/post", methods=["GET"])
def show_images():
    image_list = list(db.post.find({}, {'_id': False}))

    return jsonify({'images': image_list})


# 로그인 페이지 이동
@app.route('/loginpage')
def loginPage():
    return render_template("login.html")


# 글 등록 페이지 이동
@app.route('/posting')
def postingPage():
    return render_template("posting.html")


# 상세 글 페이지 이동
@app.route('/detailPost/<keyword>')
def detailPage(keyword):
    postInfo = db.post.find_one({'post_num': int(keyword)}, {'_id': False})
    comment_list = list(db.comment.find({'post_num': int(keyword)}, {'_id': False}))

    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_id = payload["id"]

        if user_id == postInfo['writer_id']:
            idCheck = True
        else:
            idCheck = False

        return render_template('detail.html', post_info=postInfo, comment_info=comment_list, id_check=idCheck)
    except(jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


# 글 등록
@app.route("/posting/post", methods=["POST"])
def upload_post():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        user_id = payload["id"]
        url_receive = request.form['url_give']
        pic_name_receive = request.form['pic_name_give']
        pic_explain_receive = request.form['pic_explain_give']

        url_list = list(db.post.find({}, {'_id': False}).distinct('post_num'))  # distinct는 key 값 생략하고 value 값만 가져오기

        if len(url_list) == 0:
            count = 1
        else:
            count = max(url_list) + 1

        doc = {
            'post_num': count,
            'writer_id': user_id,
            'url': url_receive,
            'pic_name': pic_name_receive,
            'pic_explain': pic_explain_receive
        }

        db.post.insert_one(doc)
        return jsonify({'msg': '등록완료!'})
    except(jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


# 글 삭제
@app.route("/post_cancel", methods=["POST"])
def post_cancel():

    post_num_receive = request.form['post_num_give']
    db.post.delete_one({'post_num': int(post_num_receive)})

    return jsonify({'msg': '삭제되었습니다'})


# 댓글 등록
@app.route("/comment", methods=["POST"])
def upload_comment():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        user_id = payload["id"]
        post_num = request.form['post_num_give']
        comment_text = request.form['comment_give']

        comment_list = list(db.post.find({'post_num': post_num}, {'_id': False}).distinct(
            'comment_num'))  # distinct는 key 값 생략하고 value 값만 가져오기

        if len(comment_list) == 0:
            count = 1
        else:
            count = max(comment_list) + 1

        doc = {
            'post_num': int(post_num),
            'comment_num': count,
            'comment_writer_id': user_id,
            'comment_text': comment_text
        }

        db.comment.insert_one(doc)

        return jsonify({'msg': '등록완료!'})
    except(jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


# 댓글 삭제
@app.route("/comment_cancel_check", methods=["POST"])
def cancel_check():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        user_id = payload["id"]
        comment_writer_id_receive = request.form['comment_writer_id_give']
        post_num_receive = request.form['post_num_give']
        comment_num_receive = request.form['comment_num_give']

        if user_id == comment_writer_id_receive:
            db.comment.delete_one({'post_num': int(post_num_receive), 'comment_num': int(comment_num_receive)})
            check = True
        else:
            check = False
        return jsonify({'check': check})
    except(jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
