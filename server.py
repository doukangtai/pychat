import socket
from threading import Thread
import hashlib
import re
import time
import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='pychat',
)


def close_cursor(conn, cursor):
    cursor.close()


def encrypt_psw(str):
    """
    使用 MD5 算法对用户的密码进行加密
    :param str: 待加密的密码字符串
    :return: 加密后的密码字符串
    """
    hl = hashlib.md5()
    hl.update(str.encode("utf-8"))  # 必须编码后才能加密
    return hl.hexdigest()


online_socket = list()  # 在线用户的连接列表，用于群发消息
socket2user = dict()  # 存储socket连接和用户名的对应关系


def check_user_database(username, encrypted_psw):
    """
    检查用户登录时输入的用户名和密码是否正确
    :param username: 待检查的用户名
    :param encrypted_psw: 待检查的用户密码
    :return: 用户名和密码是否通过的结果，True和False
    """
    print("aaa")
    print("开始检查用户信息是否有误")
    cursor = conn.cursor()
    cursor.execute("select * from user")
    fetchall = cursor.fetchall()
    cursor.close()
    for data in fetchall:
        if data[1] == username:
            if data[2] == encrypted_psw:
                return "登录成功！"
            else:
                return "密码输入有误，请重新输入！"
    return "不存在该用户，请先注册！"


def add_user_database(new_socket, username, encrypted_psw, check):
    """
    将要注册的用户名进行判断是否有重复用户名，
    如果没有，就将注册用户信息写入数据库中
    :param check:
    :param new_socket: 本次连接的客户端的套接字
    :param username: 待注册的用户名
    :param encrypted_psw: 加密后的密码
    """
    try:
        print("register: user: " + username + ", key: " + encrypted_psw)

        cursor = conn.cursor()
        cursor.execute("select * from user")
        flag = False
        for data in cursor.fetchall():
            if data[1] == username:
                flag = True
        if flag:
            cursor.close()
            new_socket.sendall("抱歉，用户名已存在！".encode("utf-8"))
            return
        else:
            cursor.execute("insert into user(username, password, verify) values(%s,%s,%s)", (username, encrypted_psw, check))
            conn.commit()
            cursor.close()
            new_socket.sendall("注册成功！".encode("utf-8"))

    except Exception as ret:
        print("添加用户数据出错：" + str(ret))
        new_socket.sendall("发生未知错误！".encode("utf-8"))


def update_user_database(new_socket, username, encrypted_psw, check):
    try:
        print("update: user: " + username + ", key: " + encrypted_psw)

        cursor = conn.cursor()
        cursor.execute("select * from user where username=%s and verify=%s", (username, check))
        flag = False
        for data in cursor.fetchall():
            if data[1] == username:
                flag = True
        if flag:
            cursor.execute("update user set password=%s where username=%s", (encrypted_psw, username))
            conn.commit()
            cursor.close()
            new_socket.sendall("修改密码成功".encode("utf-8"))
            return
        else:
            cursor.close()
            new_socket.sendall("用户不存在或密保有误".encode("utf-8"))

    except Exception as ret:
        print("添加用户数据出错：" + str(ret))
        new_socket.sendall("发生未知错误！".encode("utf-8"))


def delete_user_database(new_socket, username, encrypted_psw):
    """
    将要注册的用户名进行判断是否有重复用户名，
    如果没有，就将注册用户信息写入数据库中
    :param new_socket: 本次连接的客户端的套接字
    :param username: 待注册的用户名
    :param encrypted_psw: 加密后的密码
    """
    try:
        print("delete: user: " + username + ", key: " + encrypted_psw)

        cursor = conn.cursor()
        cursor.execute("select * from user where username=%s and password=%s", (username, encrypted_psw))
        user_num = len(cursor.fetchall())
        if user_num <= 0:
            new_socket.sendall("用户名不存在，或密码错误，无法注销账号！".encode("utf-8"))
        else:
            cursor.execute("delete from user where username=%s and password=%s", (username, encrypted_psw))
            conn.commit()
            cursor.close()
            new_socket.sendall("注销成功！".encode("utf-8"))

        # flag = False
        # for data in cursor.fetchall():
        #     if data[1] == username:
        #         flag = True
        # if flag:
        #     cursor.close()
        #     new_socket.sendall("抱歉，用户名已存在！".encode("utf-8"))
        #     return
        # else:
        #     cursor.execute("insert into user(username, password) values(%s,%s)", (username, encrypted_psw))
        #     conn.commit()
        #     cursor.close()
        #     new_socket.sendall("注册成功！".encode("utf-8"))

    except Exception as ret:
        print("添加用户数据出错：" + str(ret))
        new_socket.sendall("发生未知错误！".encode("utf-8"))


def update_online_list():
    """
    基于假设：发送的在线用户列表类型的内容总和不会超过1024Byte
    更新客户端在线用户列表
    """
    # 组装所有在线用户名为一个字符串
    online_usernames = ""
    for sk in online_socket:
        online_usernames += socket2user[sk] + "#!"
    # 向所有在线用户发送在线列表用户名
    for socket in online_socket:
        # 发送标识和在线用户列表用户名，前者为区分信息和在线用户列表
        socket.sendall(("#!onlines#!" + online_usernames).encode("utf-8"))


def online_notice(new_socket):
    """
    给所有在线客户端发送新客户端上线的通知
    :param new_socket: 新上线客户端的套接字
    """
    welcome_str = "******** Welcome " \
                  + socket2user[new_socket] + \
                  " come to MyChat! ********"
    # 向所有在线用户发送新用户上线通知，#!notices#! 标志此类消息
    for socket in online_socket:
        socket.sendall(("#!notices#!" + welcome_str).encode("utf-8"))


def histories_msg(new_socket):
    """
    发送历史消息
    :param new_socket: 新上线客户端的套接字
    """
    cursor = conn.cursor()
    cursor.execute("select * from msg")
    fetchall = cursor.fetchall()
    cursor.close()
    for data in fetchall:
        time.sleep(0.05)
        new_socket.sendall(("#!history#!"
                            + data[1] + "#!"
                            + data[2] + "#!"
                            + data[3]).encode("utf-8"))


def offline_notice(offline_socket):
    """
    给所有在线用户发送用户离线通知
    :param offline_socket: 离线用户对应的套接字
    """
    left_str = "******** " \
               + socket2user[offline_socket] + \
               " has left ********"
    for socket in online_socket:
        socket.sendall(("#!notices#!" + left_str).encode("utf-8"))


def handle_login(new_socket):
    """
    处理登录请求
    :param new_socket: 用户连接时生成的套接字
    """
    username_psw = new_socket.recv(1024).decode("utf-8")
    # 组装后的用户信息格式为 username#!#!password
    ret = re.match(r"(.+)#!#!(.+)", username_psw)
    username = ret.group(1)
    password = ret.group(2)
    encrypted_psw = encrypt_psw(password)
    # check_result = check_user(username, encrypted_psw)
    check_result = check_user_database(username, encrypted_psw)
    new_socket.sendall(check_result.encode("utf-8"))  # 将登陆结果发送给客户端

    # 只有登陆成功之后，才执行以下操作
    if check_result == "登录成功！":
        # 将对应的socket与用户名对应起来，并添加到字典中
        socket2user[new_socket] = username
        # 将连接的socket添加到在线列表中
        online_socket.append(new_socket)
        print(online_socket)
        update_online_list()
        time.sleep(4)
        online_notice(new_socket)
        time.sleep(1)
        histories_msg(new_socket)


def handle_reg(new_socket):
    """
    处理客户端的注册请求，接收客户端注册的用户信息，
    调用函数将用户名和加密后的密码存入本地文本
    :param new_socket: 本次连接过来的客户端套接字
    """
    username_psw = new_socket.recv(1024).decode("utf-8")
    ret = re.match(r"(.+)#!#!(.+)#!#!(.+)", username_psw)
    username = ret.group(1)
    password = ret.group(2)
    check = ret.group(3)
    encrypted_psw = encrypt_psw(password)
    add_user_database(new_socket, username, encrypted_psw, check)


def handle_logout(new_socket):
    """
    处理客户端的注册请求，接收客户端注册的用户信息，
    调用函数将用户名和加密后的密码存入本地文本
    :param new_socket: 本次连接过来的客户端套接字
    """
    username_psw = new_socket.recv(1024).decode("utf-8")
    # 组装后的用户格式为 username#!#!password
    ret = re.match(r"(.+)#!#!(.+)", username_psw)
    username = ret.group(1)
    password = ret.group(2)
    encrypted_psw = encrypt_psw(password)
    delete_user_database(new_socket, username, encrypted_psw)

def handle_repsd(new_socket):
    username_psw = new_socket.recv(1024).decode("utf-8")
    # 组装后的用户格式为 username#!#!password
    ret = re.match(r"(.+)#!#!(.+)#!#!(.+)", username_psw)
    username = ret.group(1)
    password = ret.group(2)
    check = ret.group(3)
    encrypted_psw = encrypt_psw(password)
    update_user_database(new_socket, username, encrypted_psw, check)

def handle_msg(new_socket):
    """
    基于假设：发送的消息类型的内容总和不会超过1024Byte
    对客户端要发送的内容进行广播
    :param new_socket: 要发送信息的客户端的套接字
    """
    content = new_socket.recv(1024).decode("utf-8")
    # 发送给所有在线客户端
    cursor = conn.cursor()
    cursor.execute("insert into msg(username,datetime,msg) values(%s,%s,%s)",
                   (socket2user[new_socket],
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    content))
    conn.commit()
    cursor.close()
    for socket in online_socket:
        socket.sendall(("#!message#!"
                        + socket2user[new_socket] + "#!"
                        + content).encode("utf-8"))


def handle(new_socket, addr):
    """
    服务器运行的主框架
    :param new_socket: 本次连接的客户端套接字
    :param addr: 本次连接客户端的ip和port
    """
    try:
        while True:
            req_type = new_socket.recv(1).decode("utf-8")  # 获取请求类型
            print(req_type)
            if req_type:  # 如果不为真，则说明客户端已断开
                if req_type == "1":  # 登录请求
                    print("开始处理登录请求")
                    handle_login(new_socket)
                elif req_type == "2":  # 注册请求
                    print("开始处理注册请求")
                    handle_reg(new_socket)
                elif req_type == "3":  # 发送消息
                    print("开始处理发送消息请求")
                    handle_msg(new_socket)
                elif req_type == "4":  # 注销请求
                    print("开始处理注销请求")
                    handle_logout(new_socket)
                elif req_type == "5":  # 修改密码请求
                    print("开始处理修改密码请求")
                    handle_repsd(new_socket)
            else:
                break
    except Exception as ret:
        print(str(addr) + " 连接异常，准备断开: " + str(ret))
    finally:
        try:
            # 客户端断开后执行的操作
            new_socket.close()
            online_socket.remove(new_socket)
            offline_notice(new_socket)
            socket2user.pop(new_socket)
            time.sleep(4)
            update_online_list()
        except Exception as ret:
            print(str(addr) + "连接关闭异常")


# 入口
if __name__ == "__main__":
    try:
        main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        main_socket.bind(('127.0.0.1', 7890))  # 服务器绑定的ip和port
        main_socket.listen(128)  # 最大挂起数
        print("服务器启动成功，开始监听...")
        while True:
            new_socket, addr = main_socket.accept()
            Thread(target=handle, args=(new_socket, addr)).start()
    except Exception as ret:
        print("服务器出错: " + str(ret))
