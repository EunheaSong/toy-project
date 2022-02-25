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

@app.route('/offline') #onclick 시, offline.html로 이동하고 싶을 때,  location.href='/offline' 이라고 하면된다.
def offline_page():
    return render_template('offline.html')

@app.route('/study_page_offline_Seoul')  # study_page_offline.html 로 이동 할 때
def study_page_offline_Seoul():
    return render_template('study_page_offline_Seoul.html')

@app.route('/study_page_offline_Gyeonggi')  # study_page_offline.html 로 이동 할 때
def study_page_offline_Gyeonggi():
    return render_template('study_page_offline_Gyeonggi.html')

@app.route('/study_page_offline_Incheon')  # study_page_offline.html 로 이동 할 때
def study_page_offline_Incheon():
    return render_template('study_page_offline_Incheon.html')

@app.route('/writeForm') # writeForm.html로 이동 할 때
def writeForm_page():
    return render_template('writeForm.html')

@app.route('/study_page_offline')  # study_page_offline.html 로 이동 할 때
def study_page_offline():
    return render_template('study_page_offline.html')

@app.route('/study_page_online')  # study_page_online.html 로 이동 할 때
def study_page_online():
    return render_template('study_page_online.html')

@app.route('/postbox/<int:num>')  # postbox.html 로 이동 할 때
def post_page(num):
    return render_template('postbox.html', num = num)

########## 권규민 - 게시판 페이지 작성 후 DB에 insert. ###############

@app.route('/write', methods=["POST"] )
def write():

    #게시글 넘버링 - 해당 번호로 내용을 가져오며, 삭제,수정의 index 번호역활.
    Write_list = list(db.posts.find({}, {"_id": False}))
    count = len(Write_list) + 1

    name_receive = request.form['name_give']
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    check_receive = request.form['check_give']
    location_receive = request.form['location_give']
    doc = { # 넘버, 작성자 , 제목 , 내용, 온/오프라인 선택 / 모임지역
        'num': count,
        'name': name_receive,
        'title': title_receive,
        'content': content_receive,
        'on_off': check_receive,
        'address': location_receive
    }
    db.posts.insert_one(doc)

    return jsonify({'msg': '작성완료!'})


########## 이푸름 - 전체보기/온라인/오프라인 게시글 목록 페이지 ##########

@app.route('/study_page_api', methods=['GET'])
def study_page_get():
   post_list = list(db.posts.find({},{'_id':False}))
   return jsonify({'post': post_list})


########## 송은혜 - 스터디 게시글 내용 보는 페이지 ##########

@app.route('/study_page') #study_page.html로 페이지 이동. url명을 지정해주고자 하여,study_page로 설정.
def study_page():
    return render_template('study_page.html')

@app.route("/postbox/comment", methods=["GET"]) #게시글 내용 꺼내옴
def comments_get():
    all_comments = list(db.comments_list.find({}, {'_id': False}))
    return jsonify({'comments':all_comments})

@app.route('/postbox/comment', methods=['POST']) #덧글 등록
def test_post():
    comment_receive = request.form['comment_give']
    comment_number = list(db.comments_list.find({}, {'_id': False}))
    count = len(comment_number) + 1
    doc = {'comment': comment_receive,
           'co_num': count}
    db.comments_list.insert_one(doc)
    return jsonify({'msg': '등록되었습니다.'})

@app.route("/postbox/comment_delete", methods=["POST"]) #덧글 삭제
def comment_delete():
    co_num_receive = request.form['co_num_give']
    db.comments_list.delete_one({'co_num': int(co_num_receive)}) #co_num_receive앞에 int를 붙여주어야 숫자로 인식함! int안붙이면 문자형으로 인식.
    return jsonify({'msg': '삭제되었습니다.'})


##################################################



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)