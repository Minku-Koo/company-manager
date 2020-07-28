from django.db import models

# Create your models here.
"""
실제 DB 내 테이블 정보
CREATE TABLE notice(
    no int(5) AUTO_INCREMENT,
    id_num varchar(20) NOT NULL,
    title varchar(50) NOT NULL,
    content varchar(800) NOT NULL,
    password varchar(15) NOT NULL,
    date datetime NOT NULL,
    `check`   int(4) NOT NULL,
    PRIMARY KEY (no)
);

CREATE TABLE time(
    no int(5) AUTO_INCREMENT,
    id_num varchar(20) NOT NULL,
    day datetime,
    on_work datetime,
    off_work datetime,
    more int(3),
    reason  int,
    PRIMARY KEY (no)
);

CREATE TABLE money(
    no int(5) AUTO_INCREMENT,
    id_num varchar(20) NOT NULL,
    year int(4) NOT NULL,
    month int(2) NOT NULL,
    salary varchar(12) NOT NULL,
    weekend varchar(8) ,
    night varchar(8) ,
    PRIMARY KEY (no)
);

CREATE TABLE user_info(
    no int(5) AUTO_INCREMENT,
    id_num varchar(20) NOT NULL,
    position varchar(20) NOT NULL,
    depart varchar(20) NOT NULL,
    admin int NOT NULL,
    PRIMARY KEY (no)
);

"""

class Notice(models.Model):  # 공지글 저장 테이블
    no = models.IntegerField(primary_key=True)
    id_num = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=800)
    password = models.CharField(max_length=15)
    date = models.DateTimeField()
    check  = models.IntegerField()
    
    class Meta:
        db_table = "Notice"
    
    def __str__(self):
        return str(self.id_num) 
        
class Time(models.Model):  #출퇴근 시간 저장 테이블
    no = models.IntegerField(primary_key=True)
    id_num = models.CharField(max_length=20)
    day = models.DateField(blank=True, null=True)
    on_work = models.DateTimeField()
    off_work = models.DateTimeField()
    more = models.IntegerField()
    reason  = models.IntegerField()

    class Meta:
        db_table = "Time"

    def __str__(self):
        return str(self.id_num) 
        
        
class Money(models.Model):  # 급여 정보 저장 테이블
    no = models.IntegerField(primary_key=True)
    id_num = models.CharField(max_length=20)
    year = models.IntegerField()
    month = models.IntegerField()
    salary = models.CharField(max_length=12)
    weekend = models.CharField(max_length=8, default="0")
    night = models.CharField(max_length=8, default="0")

    class Meta:
        db_table = "Money"

    def __str__(self):
        return str(self.id_num) 
        
        
class User_info(models.Model):  # 사원 직책,부서 정보 저장 테이블
    no = models.IntegerField(primary_key=True)
    id_num = models.CharField(max_length=20)
    position = models.CharField(max_length=20)
    depart = models.CharField(max_length=20)
    admin = models.IntegerField()

    class Meta:
        db_table = "User_info"

    def __str__(self):
        return str(self.id_num) 
        