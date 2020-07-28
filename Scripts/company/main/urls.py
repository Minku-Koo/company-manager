
from django.urls import path
from main import views

urlpatterns = [
		path('', views.index, name='index'),
        path('login/', views.login, name='login'), #로그인
        path('notice/<int:page>', views.notice, name='notice'), #페이지 당 공지글 표시
        path('notice/write', views.notice_write, name='notice_write'), #공지글 작성
        path('notice/read/<int:post>', views.read_post, name='read_post'), #공지글 읽기
        path('notice/write/input/', views.notice_db, name='notice_db'), # 공지글 작성 확인
        path('notice/delete/<int:no>', views.notice_delete, name='notice_delete'), #공지글 삭제
        path('time/<str:Yearmonth>', views.time, name='time'), # 출퇴근 정보 년/월별 표시
        path('onoff/<str:onoff>', views.onoff, name='onoff'), #출/퇴근 정보 입력
        path('money/<int:year>', views.money, name='money'), # 년도별 급여 정보 출력
        path('setting', views.setting, name='setting'), # 관리자 설정 화면
        path('setting/show', views.setting_show, name='setting_show'), #사원 정보 표시
        path('setting/<int:id>', views.setting_money, name='setting_money'),# 아이디 통해 해당 사원 급여 정보 변경
        path('setting/showed', views.setting_showed, name='setting_showed'), # 급여 정보 변경 후, 사원 관리 화면
        path('setting/money_save', views.money_save, name='money_save'),  # 급여 정보 변경
	]
    