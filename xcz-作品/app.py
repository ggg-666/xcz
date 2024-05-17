from flask import Flask,render_template, request,redirect,url_for,session,jsonify
from mysql_util import MysqlUtil
import pandas as pd
import random
import os
app = Flask(__name__)
app.secret_key = 'mrsoft12345678' # 设置秘钥

@app.route('/')
def index():
    db = MysqlUtil()
    sql = 'SELECT * FROM category'
    categorys = db.fetchall(sql)  # 获取多条记录

    db = MysqlUtil()
    # sql = 'SELECT * FROM product'
    sql = 'SELECT * FROM product_temp'
    comment_products = db.fetchall(sql)  # 获取多条记录
    print(comment_products)

    return render_template("/user/index.html", categorys=categorys, comment_products= comment_products,
                           hot_products=comment_products, new_products=comment_products )
    # return render_template("/test/index.html", categorys=categorys)

@app.route('/bashboard')
def bashboard():
    db = MysqlUtil()
    # sql = 'SELECT * FROM product'
    sql = 'SELECT * FROM product_temp'
    products = db.fetchall(sql)  # 获取多条记录
    print(products)

    return render_template("/test/product_board.html",products=products)
    # return render_template("/test/product_board_static.html",products=products)

@app.route('/product_echart')
def product_echart():

    return render_template('/test/job.html')



def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'png','jpeg',"bmp"}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/add_product',methods=['GET','POST'])
def add_product():
    db = MysqlUtil()
    sql = 'SELECT * FROM category'
    categorys = db.fetchall(sql)  # 获取多条记录
    if (request.method == "POST"):
        pname = request.form.get("pname")
        pDesc = request.form.get("pDesc")
        counts = request.form.get("counts")
        old_price = request.form.get("old_price")
        new_price = request.form.get("new_price")
        print(pname)
        print(pDesc)
        print(counts)
        print(old_price)
        print(new_price)

        file = request.files['file']
        if file.filename == '':
            return '没有选择文件', 400
        if file and allowed_file(file.filename):
            filename = file.filename
            file_name, file_ext = os.path.splitext(os.path.basename(filename))
            # print(file_name)
            print(file_ext)
            dir_name = "./static/product_test/"
            new_name = str(random.randint(1,10000)) + file_ext
            print(dir_name)
            images_path = os.path.join(dir_name, new_name)
            print(images_path)
            file.save(images_path)

        id = "%d" % random.randint(0,1000000000)
        # images_path = "/static/product_test/2.jpg"
        db = MysqlUtil() # 实例化数据库操作类
        sql = "INSERT INTO product_temp(id,pname,old_price,new_price,counts,images) \
               VALUES ('%s', '%s', '%s','%s','%s','%s')" % (id,pname,old_price,new_price,counts,images_path) # 插入数据的SQL语句
        db.insert(sql)
        return redirect(url_for('bashboard'))
    else:
        return render_template("/test/add_product.html", categorys=categorys)

@app.route('/delete_product/<string:id>', methods=['POST'])
def delete_product(id):
    db = MysqlUtil() # 实例化数据库操作类
    sql = "DELETE FROM product_temp WHERE id = '%s'" % (id) # 执行删除笔记的SQL语句
    db.delete(sql) # 删除数据库
    return redirect(url_for('bashboard'))


@app.route('/register', methods=['GET','POST'])
def register():
    if (request.method == "POST"):
        username = request.form['name']
        password = request.form['password']
        email = request.form['email']
        print(username)
        print(password)
        print(email)
        db = MysqlUtil()

        id = "%20d" % random.randint(0,1000000000)
        sql = "INSERT INTO user(id, username,password,email) \
        VALUES ('%s', '%s', '%s', '%s')" % (id, username, password, email)  # 插入数据的SQL语句

        product_list = db.insert(sql)  # 获取多条记录

        print(product_list)

        # insert_data(username, password, email)
        # return render_template("index.html")
        return redirect(url_for('index'))

    else: #GET
         return render_template("/test/register.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if (request.method == "POST"):
        print("ok")
        username = request.form['username']
        password_candidate = request.form['password']
        print(username)
        sql = "SELECT * FROM user  WHERE username = '%s'" % (username)  # 根据用户名查找user表中记录
        db = MysqlUtil()  # 实例化数据库操作类
        result = db.fetchone(sql)  # 获取一条记录
        print(password_candidate)
        print(result)
        db_password = result['password']  # 用户填写的密码
        if password_candidate == db_password:
            # 写入session
            session['logged_in'] = True
            session['username'] = username

            # return "登录成功"# 跳转到控制台
            return redirect(url_for('index'))
        else:
            print("密码错误")
            return render_template("/test/login.html")

    else: #GET
         return render_template("/test/login.html")

@app.route('/get_company', methods=['GET'])
def get_company():
        json = request.json
        print('recv:', json)
        re_data = {
            'company_num': 9999,
            'job_num': 5999,
            'avg_salary': 88888,
        }
        return jsonify(re_data)

@app.route('/get_industry', methods=['GET'])
def get_industry():
        # 读取CSV文件
        # df = pd.read_csv('./csv/data.csv')
        df = pd.read_csv('./csv/data3.csv', encoding="GB2312")
        # 访问特定的列（例如，'Column1'）
        # print(df['industry_type'])
        industry_type_list = df['industry_type']
        industry_type_value_list = df['industry_type_value']

        industry_type_list = industry_type_list.tolist()
        # industry_type_value_list = json.dumps(industry_type_value_list.tolist())
        industry_type_value_list = industry_type_value_list.tolist()
        re_data = {
            # 'industry_type': ["广东", "广东", "广东"],
            'industry_type': industry_type_list,
            'industry_type_value': industry_type_value_list,
        }
        print(re_data)
        # re_data = {
        #        'industry_type': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        #        'industry_type_value':  [120, 200, 150, 80, 70, 110, 130],
        # }
        return jsonify(re_data)

@app.route('/logout')
def logout():
    session.clear() # 清除Session
    return redirect(url_for('index'))

app.run(debug=True)