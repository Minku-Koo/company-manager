import request
from django.shortcuts import render, redirect
from  django.views.decorators.csrf import csrf_exempt
from register.models import users
from django import forms
from main.models import Notice, Time, Money,User_info
from django.utils import timezone
from datetime import datetime, timedelta

def index(request):
    print("This is INDEX") # 메인 화면
    return render(request, 'main/index.html',{"message": ""})
    
@csrf_exempt
def login(request):  #로그인
    print("login start")
    id = request.POST['id'] # 아이디 
    pw = request.POST['pw'] # 비밀번호
    
    try:
        row = users.objects.get(id_num=id) #아이디가 있는 경우
        
    except(users.DoesNotExist): #아이디가 없는 경우
        print("ID not Exist")
        msg ={"message": "아이디가 존재하지 않습니다."} 
        return render(request, 'main/index.html',msg)
    
    if pw == row.password and pw: #비밀번호가 입력되어 있고, DB 정보와 일치하는 경우 >> 로그인 성공
        print("succcc")
        request.session['number'] = id # 아이디 세션에 입력
        request.session['name']=row.name  #이름 세션에 입력
        admin = User_info.objects.get(id_num = id) # db에서 권한 정보 불러옴
        request.session['admin'] = admin.admin  # 권한 정보 세션에 입력
        return redirect("/")  #메인 화면으로 이동
        
    else:
        print("wrong")  #비밀번호가 틀린 경우
        msg ={"message": "로그인에 실패하였습니다."}
        return render(request, 'main/index.html',msg)
        
def notice(request, page):  # 공지사항 화면 / 페이지 번호를 url 통해 입력받음
    page -= 1
    page_count = 5  # 한 페이지에 나타나는 공지글 개수
    
    row = Notice.objects.all().order_by('-no')[page*page_count: page*page_count+page_count]  #내림차순으로 공지글을 불러옴
    show_table = []
    for f in row:  # 공지글 정보를 통해 리스트 생성
        name = users.objects.get(id_num=f.id_num)
        tmp = [f.no, f.title, name.name, f.date.strftime('%Y.%m.%d'), f.check]
        show_table.append(tmp)
        
    page_bt = int(Notice.objects.count()/page_count+1)  #페이지 버튼 개수를 알아냄
    
    if Notice.objects.count()% page_count ==0:  #페이지가 (페이지당 글 개수)의 n배일 경우
        page_bt -=1  #페이지 버튼 개수 차감
        
    page_list=[]
    for a in range(page_bt): #페이지 버튼 개수만큼 리스트 생성
        page_list.append(a+1)
        
    info = {"table":show_table,"count":page_list}
        
    return render(request, 'main/notice.html', info)


def notice_write(request): #공지글 작성 화면
    print("notice_write start")
    return render(request, 'main/notice_write.html')

def notice_delete(request, no): #공지글 삭제 화면
    Notice.objects.get(no=no).delete()
    return redirect("/notice/1")


@csrf_exempt
def notice_db(request): #공지글 저장 화면
    if request.method =="POST":
        print("notice_write start")
        title = request.POST['title'] #제목
        content = request.POST['content']  #내용
        pw = request.POST['pw']  #비밀번호
        
        number=request.session['number']
        # db 에 작성한 게시글 정보 입력
        Notice(id_num=number, title=title, content=content, password=pw, date=timezone.now() ,check=0).save()
        # 공지 최초 화면으로 이동
        return redirect("/notice/1")
    
def read_post(request, post): #공지글 읽기
    print("read_post start")
    posting = Notice.objects.get(no=post) #공지글 번호를 통해 공지글 정보를 db에서 불러옴
    posting.check = posting.check+1  #조회수 증가시켜서 저장하기
    posting.save()
    name = users.objects.get(id_num=posting.id_num)  #게시글 작성자 이름
    # 게시글 정보 (제목, 내용, 작성자, 날짜) 를 불러옴
    post_info={"post":[posting.title,posting.content,name.name,posting.date, posting.id_num, post]}
    return render(request, 'main/notice_show.html', post_info)
    
def time(request, Yearmonth):  # 출퇴근 일정 화면, 년도를 url을 통해 입력받음
    print("This is time")
    if request.session.get('number') == None:  # 로그인 하지 않은 경우
        msg ={"message": "로그인부터 해주세요."}
        return render(request, 'main/index.html',msg)
    
    number=request.session['number']
    # 최초화면일 경우
    if Yearmonth == '1':
        year = timezone.now().date().year # 현재 년도와 월 정보 가져옴
        month = timezone.now().date().month
        
    else: # 페이지 이동 시, url을 통해 년도와 월 정보 받아옴
        year = Yearmonth.split("-")[0]
        month = Yearmonth.split("-")[1]
        
    # db에서 해당 년 월 정보를 통해 출퇴근 시간 정보 불러옴
    row = Time.objects.all().filter(id_num=number).filter(day__year=year).filter(day__month=month).order_by('-no')
    
    show_table = []
    for f in row: # db 정보를 리스트로 생성
        name = users.objects.get(id_num=f.id_num)
        off_workTime = f.off_work
        
        if off_workTime != None: #퇴근 시간이 있는 경우
            off_workTime = off_workTime.strftime('%I:%M %p') # 시간:날짜 AM/PM 형식으로 구분
            
        # 출퇴근 정보 임시 저장
        tmp = [f.day.strftime('%Y-%m-%d'), f.on_work.strftime('%I:%M %p'), off_workTime, f.more, f.reason]
        show_table.append(tmp)
        
    # 페이지 이동 url 생성 위해, 다음 달과 이전 달 정보 생성
    nextyear = int(year)
    prevyear = int(year)
    nextmonth = int(month) +1
    prevmonth = int(month) -1
    
    if month =='12': # 12월일 경우
        nextmonth = 1 #다음 달은 1월
        nextyear = int(year) +1 # 년도 증가
    elif month == '1': # 1월일 경우
        prevmonth = 12 #이전 달은 12월
        prevyear = int(year) -1 # 년도 차감
        
    # 출퇴근 정보와 페이지 이동 url 정보를 html template로 전송
    info = {"table":show_table,"month":str(year)+"-"+str(month), 
    "atag":[ str(nextyear)+"-"+str(nextmonth), str(prevyear)+"-"+str(prevmonth)]}
    
    return render(request, 'main/time.html',info)
    
def onoff(request, onoff): # 출퇴근 버튼 입력 시, 동작하는 함수
    print("This is Of Off")
    if request.session.get('number') == None: # 로그인 안된 경우
        msg ={"message": "로그인부터 해주세요."}
        return render(request, 'main/index.html',msg)
        
    id = request.session['number']
    nowDay = timezone.now().date() #현재 날짜
    nowTime = timezone.now()  #현재 시간
    
    Y = nowTime.year # 오늘 년도
    M = nowTime.month  # 오늘 월
    D = nowTime.day  #오늘 일
    offDefaultTime = datetime(Y, M,D, 18, 00, 00) #  퇴근 시간 기본값 = 금일 18시
    
    if onoff =="on": # 출근 버튼일 경우
        try:
            today = Time.objects.get(day=nowDay, id_num=id)  # 이미 db에 출근 시간 저장된 경우
            msg ={"message": "이미 출근하셨습니다."}
            return render(request, 'main/index.html',msg)
            
        except(Time.DoesNotExist): # db에 출근 정보가 없는 경우
            print("no data")
            Time(id_num=id, day=nowDay, on_work= nowTime).save() #오늘 출근 시간 정보를 입력
            print("on work time save")
            return redirect("/")
            
    else:  # 퇴근 버튼일 경우
        try:
            today = Time.objects.get(day=nowDay, id_num=id)  # db에 오늘 정보가 있는 경우
            
            today.off_work = nowTime  # 퇴근 시간 정보 입력
            today.save()
            
            if (nowTime - offDefaultTime) > timedelta(seconds=1) :  # 18시 이후 퇴근일 경우
                today.more = (nowTime - offDefaultTime).seconds // 3600  # 1시간 단위로 초과 근무 시간 계산하여 입력
                today.save()
            return redirect("/")  #메인 화면 이동
            
        except(Time.DoesNotExist):  # 오늘 출근 정보가 없는 경우
            print("no data")
            msg ={"message": "출근 버튼을 먼저 눌러주세요."}
            return render(request, 'main/index.html',msg)
    
    return redirect("/")
    
def money(request, year):  # 급여 정보 /  년도
    print("money start")
    if request.session.get('number') == None:  # 로그인 되지 않은 경우
        msg ={"message": "로그인부터 해주세요."}
        return render(request, 'main/index.html',msg)
        
    id = request.session['number']
    if year == 1: # 최초 화면일 경우
        nowDay = timezone.now() # 오늘 시간 정보 받아옴
        year = nowDay.year # 년도를 올해로 계산
        
    salary = Money.objects.filter(year=year).filter(id_num=id) # 해당 년도에 맞는 급여 정보 db에서 받아옴
    list = []
    for a in salary:  # db 정보를 리스트화
        list.append([ a.month,a.salary, a.weekend, a.night, sum([int(a.salary), int(a.weekend), int(a.night)]) ])
        
    info = {"salary":list, "year": int(year)}  # 년도와 db 정보 html teamplate로 전송
    return render(request, 'main/money.html', info)
    
def setting(request):  # 관리자 설정 화면
    print("setting start")
    if request.session.get('number') == None:  # 로그인 되지 않은 경우
        msg ={"message": "로그인부터 해주세요."}
        return render(request, 'main/index.html',msg)
        
    id = request.session['number']
    return render(request, 'main/admin_pw.html')
    
@csrf_exempt
def setting_show(request):  # 비밀번호 입력 화면
    print("setting_show start")
    ADMIN_PASSWORD = "rnalsrn12"  # 관리자 비밀번호 세팅값
    password = request.POST['password']
    id = request.session['number']
    
    if password != ADMIN_PASSWORD:  # 비밀번호가 다를 경우
        print("password not matching")
        info = {"message":"관리자 비밀번호가 일치하지 않습니다."}
        return render(request, 'main/admin_pw.html', info)
        
    admin = User_info.objects.get(id_num = id) 
    if admin.admin == 0: # 관리자 설정 권한이 없는 경우
        msg ={"message": "관리자 설정 권한이 없습니다."}
        return render(request, 'main/admin_pw.html',msg)
    
    # 관리자 설정 권한이 있고 /  비밀번호가 일치하는 경우
    admin = User_info.objects.all()  # 사원 정보 불러옴
    
    list=[]
    list = setting_db(admin) # db정보 리스트화  - 바로 아래 setting_db 함수 이용
    info = {"admin":list}
    return render(request, 'main/setting_show.html', info)

def setting_db(admin):  # db 정보를 통해 화면 출력을 위한 리스트화 함수
    list=[]
    admin_kr = ""
    for a in admin: 
        name = users.objects.get(id_num = a.id_num)
        
        if a.admin ==1:  # 권한 정보가 1일 경우
            admin_kr = "O"
        else: admin_kr = "X"# 권한 정보가 0일 경우
        
        list.append([ name.name, a.position, a.depart, admin_kr, a.id_num ])
    return list  # 리스트 반환

def setting_showed(request):  # 관리자가 급여 설정을 하고 난 다음 돌아오는 화면
                            # 비밀번호 재설정 방지를 위해 url 추가 구성
    admin = User_info.objects.all()
    list=[]
    list = setting_db(admin) # db 리스트화
    info = {"admin":list}
    return render(request, 'main/setting_show.html', info)

def setting_money(request, id):  # 급여 정보 변경 화면, 해당 사원 id 값을 url 통해 전달받음
    print("setting_money start")
    return render(request, 'main/setting_money.html', {"id":id})
    
@csrf_exempt
def money_save(request):  # 사원 급여 정보 변경 
    print("money_save")
    id = request.POST['id'] # 아이디
    salary = request.POST['salary'] # 급여
    weekend = request.POST['weekend'] # 주말 급여
    night = request.POST['night']   # 야간 급여
    
    nowDay = timezone.now() # 현재 날짜
    Y =  nowDay.year # 올해
    M = nowDay.month  # 이번달
    money = Money.objects.get(id_num = id, year=Y, month=M)  # 오늘 기준, 이번달 급여 변경
    
    money.salary = salary
    money.weekend = weekend
    money.night = night
    money.save()
    return redirect("/setting/showed")
    
    
    
    