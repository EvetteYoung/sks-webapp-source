from flask import Flask
import os
import pymysql

app = Flask(__name__)

# 从环境变量中获取数据库连接信息
db_host = os.environ.get('DB_HOST', 'mysql')
db_user = os.environ.get('DB_USER', 'root')
db_password = os.environ.get('DB_PASSWORD', 'password')
db_name = os.environ.get('DB_NAME', 'testdb')

def get_db_connection():
    try:
        connection = pymysql.connect(host=db_host,
                                     user=db_user,
                                     password=db_password,
                                     database=db_name,
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
    except pymysql.MySQLError as e:
        return f"数据库连接失败: {e}"

@app.route('/')
def hello():
    version = "v1.0"
    db_status = "未知"
    connection = get_db_connection()

    if isinstance(connection, str):
        db_status = connection
    else:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION() as version;")
                result = cursor.fetchone()
                db_status = f"连接成功！MySQL 版本: {result['version']}"
        except pymysql.MySQLError as e:
            db_status = f"查询失败: {e}"
        finally:
            connection.close()

    return f"<h1>Hello SKS!</h1><p>App Version: {version}</p><p>Database Status: {db_status}</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
