from flask import  Flask,make_response,jsonify,abort,request
from flask_restful import  Api,Resource
from flask_httpauth import  HTTPBasicAuth

from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

app=Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
api=Api(app=app)
auth=HTTPBasicAuth()

@auth.get_password
def get_password(name):
	if name=='admin':
		return 'admin'
@auth.error_handler
def authoorized():
	return make_response(jsonify({'msg':"请认证"}),401)

books=[
	{'id':1,'author':'wuya','name':'Python接口自动化测试实战','done':True},
	{'id':2,'author':'无涯','name':'Selenium3自动化测试实战','done':False}
]


class User(object):
	def __init__(self, id, username, password):
		self.id = id
		self.username = username
		self.password = password

	def __str__(self):
		return "User(id='%s')" % self.id

users = [
	User(1, 'wuya', 'asd888'),
	User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
	user = username_table.get(username, None)
	if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
		return user

def identity(payload):
	user_id = payload['identity']
	return userid_table.get(user_id, None)

jwt = JWT(app, authenticate, identity)

class Books(Resource):
	# decorators = [auth.login_required]
	decorators=[jwt_required()]

	def get(self):
		return jsonify({'status':0,'msg':'ok','datas':books})

	def post(self):
		if not request.json:
			return jsonify({'status':1001,'msg':'请求参数不是JSON的数据，请检查，谢谢！'})
		else:
			book = {
				'id': books[-1]['id'] + 1,
				'author': request.json.get('author'),
				'name': request.json.get('name'),
				'done': True
			}
			books.append(book)
			return jsonify({'status':1002,'msg': '添加书籍成功','datas':book}, 201)


class Book(Resource):
	# decorators = [auth.login_required]
	decorators = [jwt_required()]

	def get(self,book_id):
		book = list(filter(lambda t: t['id'] == book_id, books))
		if len(book) == 0:
			return jsonify({'status': 1003, 'msg': '很抱歉，您查询的书的信息不存在'})
		else:
			return jsonify({'status': 0, 'msg': 'ok', 'datas': book})

	def put(self,book_id):
		book = list(filter(lambda t: t['id'] == book_id, books))
		if len(book) == 0:
			return jsonify({'status': 1003, 'msg': '很抱歉，您查询的书的信息不存在'})
		elif not request.json:
			return jsonify({'status': 1001, 'msg': '请求参数不是JSON的数据，请检查，谢谢！'})
		elif 'author' not in request.json:
			return jsonify({'status': 1004, 'msg': '请求参数author不能为空'})
		elif 'name' not in request.json:
			return jsonify({'status': 1005, 'msg': '请求参数name不能为空'})
		elif 'done' not in request.json:
			return jsonify({'status': 1006, 'msg': '请求参数done不能为空'})
		elif type(request.json['done'])!=bool:
			return jsonify({'status': 1007, 'msg': '请求参数done为bool类型'})
		else:
			book[0]['author'] = request.json.get('author', book[0]['author'])
			book[0]['name'] = request.json.get('name', book[0]['name'])
			book[0]['done'] = request.json.get('done', book[0]['done'])
			return jsonify({'status': 1008, 'msg': '更新书籍信息成功', 'datas': book})

	def delete(self,book_id):
		book = list(filter(lambda t: t['id'] == book_id, books))
		if len(book) == 0:
			return jsonify({'status': 1003, 'msg': '很抱歉，您查询的书的信息不存在'})
		else:
			books.remove(book[0])
			return jsonify({'status': 1009, 'msg': '删除书籍成功'})

api.add_resource(Books,'/v1/api/books')
api.add_resource(Book,'/v1/api/book/<int:book_id>')

if __name__ == '__main__':
	app.run(debug=True)