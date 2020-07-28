from django.db import models
from django.urls import reverse
'''
class userRegister(models.Model):
    name = models.CharField(max_length=15)
    email = models.EmailField()
    pw = models.CharField(max_length=25)
    pwc = models.CharField(max_length=25)
    num = models.CharField(max_length=45)
    tel = models.CharField(max_length=20)

실제 db 내 테이블 정보
CREATE TABLE users(
    no int(5) AUTO_INCREMENT,
    name varchar(30) NOT NULL,
    email varchar(40) NOT NULL,
    password varchar(31) NOT NULL,
    id_num varchar(20) NOT NULL,
    telephone varchar(12) NOT NULL,
    PRIMARY KEY (no)
);
'''
class users(models.Model):  # 모든 회원 정보 저장 테이블 
    no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=31)
    id_num = models.CharField(max_length=20)
    telephone  = models.CharField(max_length=12)
    
    class Meta:
        db_table = "users"
    
    def __str__(self):
        return str(self.id_num) 
    