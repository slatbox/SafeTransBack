import sqlite3
import random
import hashlib
import os
class UserDB:
    def __init__(self,file_name) -> None:
        self.con = sqlite3.connect(file_name)
        self.md5 = hashlib.md5()
        self.cur = self.con.cursor()
    
    def jm_md5(self,password):
        m = hashlib.md5()  # 构建MD5对象
        m.update(password.encode(encoding='utf-8')) #设置编码格式 并将字符串添加到MD5对象中
        password_md5 = m.hexdigest()  # hexdigest()将加密字符串 生成十六进制数据字符串值
        return password_md5
    
    def createUser(self,user_name,password):
        salt = str(random.random())
        passhash = self.jm_md5(salt + password)
        self.cur.execute(
            "INSERT INTO users (name,passhash,salt) VALUES (?,?,?)",
            (user_name,passhash,salt)
        )
        self.con.commit()
        print(self.cur.fetchall())
    
    def verify(self,user_name,password):
        # self.cur = self.con.cursor()
        self.cur.execute(
            "select * from users where name=:user_name",
            {'user_name':user_name}
        )
        self.con.commit()
        user_name,r_passhash,salt = self.cur.fetchall()[0]
        passhash = self.jm_md5(salt + password)
        if r_passhash == passhash:
            return True
        else:
            return False
        
    
    

if __name__ == '__main__':
    db = UserDB('users.db')
    db.createUser('admin','82819639')
    db.verify('admin','82819639')
    # print(hash('123'))