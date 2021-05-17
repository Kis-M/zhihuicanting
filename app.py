import os
from collections import Counter
from common import num
from flask import Flask, render_template, redirect, request, session, flash, jsonify, abort, url_for
from flask_bootstrap import Bootstrap
import sqlite3
from function import hash_code

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nemo'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db.db")
app.config["DATABASE"] = db_path
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 获取请求中的数据
        username = request.form.get('username')
        password = hash_code(request.form.get('password'))

        # 连接数据库，判断用户名+密码组合是否匹配
        conn = sqlite3.connect(app.config["DATABASE"])
        cur = conn.cursor()
        try:
            # sqlite3支持?占位符，通过绑定变量的查询方式杜绝sql注入
            sql = 'SELECT 1 FROM USER WHERE USERNAME=? AND PASSWORD=?'
            is_valid_user = cur.execute(sql, (username, password)).fetchone()

            # 拼接方式，存在sql注入风险, SQL注入语句：在用户名位置填入 1 or 1=1 --
            # sql = 'SELECT 1 FROM USER WHERE USERNAME=%s AND PASSWORD=%s' % (username, password)
            # print(sql)
            # is_valid_user = cur.execute(sql).fetchone()
        except:
            flash('用户名或密码错误！')
            return render_template('login.html')
        finally:
            conn.close()

        if is_valid_user:
            # 登录成功后存储session信息
            session['is_login'] = True
            session['name'] = username
            return redirect('/houtaishouye')
        else:
            flash('用户名或密码错误！')
            return render_template('login.html')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm')
        # 判断所有输入都不为空
        if username and password and confirm_password:
            if password != confirm_password:
                flash('两次输入的密码不一致！')
                return render_template('register.html', username=username)
            # 连接数据库
            conn = sqlite3.connect(app.config["DATABASE"])
            cur = conn.cursor()
            # 查询输入的用户名是否已经存在
            sql_same_user = 'SELECT 1 FROM USER WHERE USERNAME=?'
            same_user = cur.execute(sql_same_user, (username,)).fetchone()
            if same_user:
                flash('用户名已存在！')
                return render_template('register.html', username=username)
            # 通过检查的数据，插入数据库表中
            sql_insert_user = 'INSERT INTO USER(USERNAME, PASSWORD) VALUES (?,?)'
            cur.execute(sql_insert_user, (username, hash_code(password)))
            conn.commit()
            conn.close()
            # 重定向到登录页面
            return redirect('/login')
        else:
            flash('所有字段都必须输入！')
            if username:
                return render_template('register.html', username=username)
            return render_template('register.html')
    return render_template('register.html')


@app.route('/logout')
def logout():
    # 退出登录，清空session
    if session.get('is_login'):
        session.clear()
        return redirect('/')
    return redirect('/')


# 首页
@app.route('/houtaishouye', methods=['GET', 'POST'])
def houtaishouye():
    return render_template('houtaishouye.html')


# 智能分析
@app.route('/tongji', methods=['GET', 'POST'])
def tongji():
    conn = sqlite3.connect(app.config["DATABASE"])
    cur = conn.cursor()
    cur.execute('''select sum(renshu) from CNAME''')
    renshu = cur.fetchall()
    cur.execute('''select sum(renshu) from lishi''')
    renshu1 = cur.fetchall()
    cur.execute('''select daihao from CNAME''')
    daihao = cur.fetchall()
    cur.execute('''select daihao from lishi''')
    daihao1 = cur.fetchall()
    d1 = ""
    d2 = []
    for i in daihao:
        d1 += i[0]
    for i in daihao1:
        d1 += i[0]
    count = Counter(num(list(d1)))
    for key, value in count.items():
        d2.append(value)
    conn.close()
    return render_template('tongji.html', renshu=renshu, renshu1=renshu1, d2=d2)


# 历史订单
@app.route('/lishidingdan', methods=['GET', 'POST'])
def lishidingdan():
    conn = sqlite3.connect(app.config["DATABASE"])
    cur = conn.cursor()
    # 查询历史订单详情
    cur.execute('''select * from lishi order by o asc''')
    sql = cur.fetchall()
    conn.close()
    return render_template('lishidingdan.html', username=sql)


# 订单
@app.route('/dingdan', methods=['GET', 'POST'])
def dingdan():
    conn = sqlite3.connect(app.config["DATABASE"])
    cur = conn.cursor()
    # 查询订单详情
    cur.execute('''select * from CNAME order by ID asc''')
    sql = cur.fetchall()
    if request.method == 'POST':
        # 获取请求中的数据
        id1 = request.form.get('id')
        if id1:
            cur.execute('''UPDATE CNAME SET fuwu = '无' WHERE ID = (?);''', id1)
            conn.commit()
            conn.close()
            return redirect(url_for('dingdan'))
    return render_template('dingdan.html', username=sql)


# 室内环境检测装置
@app.route('/guanlijiemian', methods=['GET', 'POST'])
def guanlijiemian():
    conn = sqlite3.connect(app.config["DATABASE"])
    cur = conn.cursor()
    # 查询灯LED1的状态
    cur.execute('''select zhuangtai from guanli where guanli == "led1"''')
    led1 = cur.fetchone()
    # 查询火焰传感器1状态
    cur.execute('''select zhuangtai from guanli where guanli == "huoyan1"''')
    huoyan1 = cur.fetchone()
    # 查询火焰传感器1状态
    cur.execute('''select zhuangtai from guanli where guanli == "huoyan2"''')
    huoyan2 = cur.fetchone()
    # 查询烟雾浓度1含量
    cur.execute('''select zhuangtai from guanli where guanli == "yanwu1"''')
    yanwu1 = cur.fetchone()
    # 查询烟雾浓度2含量
    cur.execute('''select zhuangtai from guanli where guanli == "yanwu2"''')
    yanwu2 = cur.fetchone()
    if request.method == 'POST':
        # 获取请求中的数据
        led = request.form.get('led')
        if led == "off":
            cur.execute('''UPDATE guanli SET zhuangtai = '已关闭' where guanli == "led1";''', )
            conn.commit()
            conn.close()
            return redirect(url_for('guanlijiemian'))
        elif led == "on":
            cur.execute('''UPDATE guanli SET zhuangtai = '已打开' where guanli == "led1";''', )
            conn.commit()
            conn.close()
            return redirect(url_for('guanlijiemian'))
    return render_template('guanlijiemian.html', led1=led1, yanwu1=yanwu1, yanwu2=yanwu2, huoyan1=huoyan1,
                           huoyan2=huoyan2)


@app.route('/api/adduser', methods=['GET', 'POST'])
def add_user():
    if request.json:
        username = request.json.get('username', '').strip()
        password = request.json.get('password')
        confirm_password = request.json.get('confirm')
        # 判断所有输入都不为空
        if username and password and confirm_password:
            if password != confirm_password:
                return jsonify({'code': '400', 'msg': '两次密码不匹配！'}), 400
            # 连接数据库
            conn = sqlite3.connect('db.db')
            cur = conn.cursor()
            # 查询输入的用户名是否已经存在
            sql_same_user = 'SELECT 1 FROM USER WHERE USERNAME=?'
            same_user = cur.execute(sql_same_user, (username,)).fetchone()
            if same_user:
                return jsonify({'code': '400', 'msg': '用户名已存在'}), 400
            # 通过检查的数据，插入数据库表中
            sql_insert_user = 'INSERT INTO USER(USERNAME, PASSWORD) VALUES (?,?)'
            cur.execute(sql_insert_user, (username, hash_code(password)))
            conn.commit()
            sql_new_user = 'SELECT id,username FROM USER WHERE USERNAME=?'
            user_id, user = cur.execute(sql_new_user, (username,)).fetchone()
            conn.close()
            return jsonify({'code': '200', 'msg': '账号生成成功！', 'newUser': {'id': user_id, 'user': user}})
        else:

            return jsonify({'code': '404', 'msg': '请求参数不全!'})
    else:
        abort(400)


@app.route('/api/testjson', methods=['GET', 'POST'])
def test_json():
    if 'x' in request.json:
        print(request.json)
        return jsonify(request.json)
    else:
        abort(400)


@app.route('/api/mock', methods=['GET', 'POST'])
def mock():
    if request.method == 'GET':
        res = []
        for arg in request.args.items():
            res.append(arg)
        res = dict(res)
        return jsonify(res)
    elif request.method == 'POST':
        return jsonify(request.json)


if __name__ == '__main__':
    app.run(debug=True)
