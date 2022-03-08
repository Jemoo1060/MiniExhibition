from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.u0f3u.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def main():
    return render_template("index.html")

@app.route('/posting')
def detail():
    return render_template("posting.html")

@app.route("/posting/post", methods=["POST"])
def upload_post():
    url_receive = request.form['url_give']
    pic_name_receive = request.form['pic_name_give']
    pic_explain_receive = request.form['pic_explain_give']

    url_list = list(db.mini.find({}, {'_id': False}))
    count = len(url_list) + 1
    doc = {
        'num':count,
        'url':url_receive,
        'pic_name':pic_name_receive,
        'pic_explain':pic_explain_receive
    }

    db.mini.insert_one(doc)

    return jsonify({'msg': '등록완료! 나가기를 눌러주세요'})

@app.route("/posting/post", methods=["GET"])
def show_images():
    image_list = list(db.mini.find({}, {'_id': False}))

    return jsonify({'images': image_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)