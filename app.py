from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.ywgct.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.toy   #db폴더명 toy로 설정.

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/study_page_api', methods=['GET'])
def study_page_get():
   post_list = list(db.posts.find({},{'_id':False}))

   return jsonify({'post': post_list})

@app.route('/study_page_api_num', methods=['GET'])
def study_page_num_get():
   num_receive = request.args.get('num_give')
   No = db.posts.find_one({'num': num_receive})

   return jsonify({'bulletin':No})

@app.route('/test', methods=['GET'])
def test_get():
   title_receive = request.args.get('title_give')
   print(title_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 GET!'})

@app.route('/test', methods=['POST'])
def test_post():
   title_receive = request.form['title_give']
   print(title_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 POST!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)