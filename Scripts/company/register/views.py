from django.shortcuts import render, redirect
import request
from django import forms
from register.models import users
from main.models import User_info
import pymysql
from django.urls import reverse
from  django.views.decorators.csrf import csrf_exempt


def index(request):  # 회원가입 메인 화면
    msg={"sign":"hello"}
    return render(request, 'register/register.html')

@csrf_exempt
def sign(request):  #회원가입 정보 입력시
    if request.method =="POST": 
        
        user_name = request.POST['user_name'] #이름
        user_email = request.POST['user_email'] #이메일
        user_pw = request.POST['user_pw'] #비밀번호
        user_pwc = request.POST['user_pwc'] #비밀번호 확인
        user_num = request.POST['user_num'] #사원 번호
        user_tel = request.POST['user_tel'] #전화번호
        
        all_data = users.objects.all() # db 데이터를 전부 가져옴
        id_list = []
        for f in all_data:
            id_list += [f.id_num] #db에서 모든 아이디 불러와서 리스트화
        
        # 입력한 정보가 부족할 경우
        if not user_name or  not user_email or not user_pw or not user_num or not user_tel:
            msg ={"message":"모든 정보를 입력해주세요."}
            return render(request, 'register/register.html', msg) 
        
        if user_pw != user_pwc: # 비밀번호와 비밀번호 확인이 일치하지 않는 경우
            msg ={"message":"비밀번호가 일치하지 않습니다."}
            return render(request, 'register/register.html', msg) 
            
        elif user_name =="":  # 이름이 빈 값일 경우
            msg ={"message": "이름을 입력해주세요."}
            return render(request, 'register/register.html', msg) 
        
        elif user_num in id_list: # 이미 존재하는 아이디일 경우
            msg ={"message": "이미 존재하는 사원 번호 입니다."}
            return render(request, 'register/register.html', msg) 
            
        # db에 회원가입 정보 입력
        users(name=user_name, email=user_email, password=user_pw, id_num=user_num, telephone=user_tel).save()
        # 사원 정보에 아이디 입력, 권한 정보는 없음으로 입력, 직책과 부서는 NULL 로 입력 후, 추후 변경
        User_info(id_num=user_num, position="NULL",depart="NULL",  admin=0).save()
        print("success!!!!!!!!!!!!")
        
        request.session['name']=user_name # 세션에 이름 입력
        request.session['number'] = user_num # 세션에 사원 번호 입력
        return redirect("/")
        
def logout(request): # 로그아웃
    print("This is logout")
    # 세션 정보 초기화
    request.session['number'] = None
    request.session['name']=None
    request.session['admin'] = None
    return redirect("/")
    
def fix(request): # 회원 정보 수정
    print("This is Fix")
    num = request.session['number'] #이름 정보
    user_data = users.objects.get(id_num=num) #회원 이름, 이메일 정보
    info={"name":user_data.name, "email":user_data.email}
    
    return render(request, 'register/fix.html',info)
    
@csrf_exempt
def fix_user(request):  # 회원가입 수정 시
    if request.method =="POST":
        print("fix_user")
        user_name = request.POST['name'] #이름
        user_email = request.POST['email']# 이메일
        password = request.POST['password'] #비밀번호
        new_pw = request.POST['new_pw']  # 새 비밀번호
        new_pwc = request.POST['new_pwc']  # 새 비밀번호 확인
        
        # db에서 해당 회원 정보 가져옴
        user_data = users.objects.get(id_num=request.session['number'])
        info={"name":user_data.name, "email":user_data.email} 
        
        if password != user_data.password:  # 비밀번호가 일치하지 않는 경우
            info["message"] = "기존 비밀번호가 일치하지 않습니다."
            return render(request, 'register/fix.html',info)
            
        if user_name!=user_data.name: #이름이 변경된 경우
            user_data.name=user_name #db 정보 변경
            request.session['name']=user_name #세션 정보 변경
            
        if user_email!=user_data.email: #이베일이 변경된 경우
            user_data.email = user_email #db 정보 변경
            
         # 새 비밀번호와 새 비밀번호 확인이 입력되었고 일치할 경우
        if new_pw and new_pwc and (new_pw == new_pwc):
            user_data.password = new_pw  #db에 비밀번호 정보 입력
            
        elif new_pw != new_pwc:  # 새 비밀번호가 일치하지 않는 경우
            info["message"] = "새 비밀번호가 일치하지 않습니다."
            return render(request, 'register/fix.html',info)
            
        user_data.save()  # db 저장
        print("fix success")
        return redirect("/")  # 메인 화면으로 이동