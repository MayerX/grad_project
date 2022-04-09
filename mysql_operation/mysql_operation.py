from pymysql import connect


def connect_mysql():
    db = connect(host="localhost", port=3306, database="graduation_project_mysql",
                 user="root", password="mayer964553")
    cursor = db.cursor()
    print("成功链接数据库")
    return cursor


def query_table(mysql_sentence: str):
    cursor = connect_mysql()
    cursor.execute(mysql_sentence)
    des = cursor.description
    column_name = [column[0] for column in des]
    # print(column_name)
    temp_res = cursor.fetchall()
    res = []
    for record in temp_res:
        record_dict = {}
        for column, word in zip(column_name, record):
            record_dict[column] = word
        res.append(record_dict)
    # print(res)
    return res


if __name__ == "__main__":
    query_table("select * from plan")
