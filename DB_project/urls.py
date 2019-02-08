"""DB_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from DBModel import views

admin.autodiscover()
urlpatterns = [
   url(r'^index/$',views.index),
   url(r'^admin/', admin.site.urls),
   url(r'^login/$', views.login),
   url(r'^register/$', views.register),
   url(r'^register_success/$',views.register_success),
   url(r'^student_homepage/$',views.student_homepage),
   url(r'^admin_homepage/$',views.admin_homepage),
   url(r'^admin_verify/$',views.admin_verify),
   url(r'^admin_enroll_student',views.enroll),
   url(r'^admin_mark_material',views.admin_mark_material),
   url(r'^admin_report1',views.admin_report1),
   url(r'^admin_report2',views.admin_report2),
   url(r'^admin_report3',views.admin_report3),
   url(r'^admin_report4',views.admin_report4),
   url(r'^admin_report5',views.admin_report5),
   url(r'^faculty_homepage', views.faculty_homepage),
   url(r'^faculty_mark_material', views.faculty_mark_material),
   url(r'^faculty_report1', views.faculty_report1),
   url(r'^faculty_report2', views.faculty_report2),
   url(r'^faculty_report3', views.faculty_report3),
   url(r'^faculty_report4', views.faculty_report4),
   url(r'^faculty_report5', views.faculty_report5),
   url(r'^student_course_material',views.student_course_material),
   url(r'^student_course',views.stduent_course),
   url(r'^student_certification',views.student_certification),
   url(r'^student_account_history',views.student_account_history),
   url(r'^student_course_material_info',views.student_course_material_info),
   url(r'^student_playlist',views.student_playlists),
   url(r'^student_select_playlist',views.student_select_playlist),
   url(r'^student_show_playlist',views.student_show_playlist),

]

