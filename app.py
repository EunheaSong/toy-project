from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.ywgct.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.toy   #db폴더명 toy로 설정.

# - 넘버링 - num
# - 작성자 - name
# - 제목 - title
# - 내용 - content
# - 온라인 오프라인 - on_off
# - 시간 - time
# - 조회수 - hit
# - 지역 - address
# - db폴더명 - posts


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/study_page_api', methods=['GET'])
def study_page_get():
   post_list = list(db.posts.find({},{'_id':False}))

   return jsonify({'post': post_list})

@app.route('/test', methods=['GET'])
def test_get():
   title_receive = request.args.get('title_give')
   print(title_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 GET!'})
########## 송은혜 - 스터디 게시글 내용 보는 페이지 ##########
@app.route('/study_page') #study_page.html로 페이지 이동. url명을 지정해주고자 하여,study_page로 설정.
def study_page():
    return render_template('study_page.html')

@app.route('/postbox', methods=['POST']) #덧글 등록
def test_post():
   comment_receive = request.form['comment_give']
   doc = {'comment':comment_receive}
   db.posts_list.insert_one(doc)
   return jsonify({'msg': '등록되었습니다.'})

@app.route("/postbox", methods=["GET"]) #게시글 내용 꺼내옴
def movie_get():
    all_posts = list(db.posts_list.find({}, {'_id': False}))
    return jsonify({'movies':all_posts})
##################################################

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)