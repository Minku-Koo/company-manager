
from django.urls import path
from register import views

urlpatterns = [
		path('', views.index, name='register'), #회원가입 기본 화면
        path('/sign/', views.sign, name='sign'), #회원가입 시
        path('/logout/', views.logout, name='logout'), #로그아웃
        path('/fix/', views.fix, name='fix'),  # 회원정보 수정 화면
        path('/fix/user/', views.fix_user, name='fix_user'),  # 회원정보 수정 완료
	]
    
