#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django import forms
from DBModel.models import User, Faculty, Administrator,CourseEnrollment,Interest,Course,CompleteMaterial,CourseMaterial, CourseTopics, Topics,Playlist,PlaylistContain
from django.db.models import Sum,Avg
from django.utils import timezone
from django.db import connection,transaction
import re
import bcrypt
from  django.contrib import messages
class UserForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password',widget=forms.PasswordInput())
    firstname = forms.CharField(label='First Name')
    lastname = forms.CharField(label='Last Name')
    picture = forms.CharField(label='Picture')
    city = forms.CharField(label='City')
    state = forms.CharField(label='State')
    postal_code = forms.CharField(label='Postal Code')
    country = forms.CharField(label='Country')

class UserForm_login(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password',widget=forms.PasswordInput())

class UserForm_add_faculty(forms.Form):
    website = forms.CharField(label='website')
    title = forms.CharField(label='title')
    affiliation = forms.CharField(label='affiliation')
    faculty_id = forms.IntegerField(label='faculty_id')

class UserForm_enroll(forms.Form):
    student_id = forms.IntegerField(label='student_id')
    course_id = forms.IntegerField(label='course_id')

class UserForm_mark_material(forms.Form):
    student_id = forms.IntegerField(label='student_id')
    material_id = forms.IntegerField(label='material_id')
    score = forms.CharField(label='score')

class UserForm_check_course_material(forms.Form):
    course_id = forms.IntegerField(label='course_id')

class UserForm_check_playlist(forms.Form):
    playlist_id = forms.IntegerField(label='playlist_id')

def register(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            email = userform.cleaned_data['email']
            password = userform.cleaned_data['password'].encode('utf-8')
            firstname = userform.cleaned_data['firstname']
            lastname = userform.cleaned_data['lastname']
            picture = userform.cleaned_data['picture']
            city = userform.cleaned_data['city']
            state = userform.cleaned_data['state']
            postal_code = userform.cleaned_data['postal_code']
            country = userform.cleaned_data['country']
            password = bcrypt.hashpw(password,bcrypt.gensalt())
            print(password)
            password=str(password, encoding="utf-8")
            print(password)
            user=User.objects.create(email=email, password=password, firstname=firstname, lastname=lastname, picture=picture, city= city, postal_code=postal_code, state=state, country=country)
            user.save()
            return render(request, 'register_success.html')
        else:
            messages.add_message(request, messages.INFO, 'Not Valid')
    else:
        userform = UserForm()
    return render(request, 'register.html', {'userform':userform})


def register_success(request) :
    return render(request, 'register_success.html')


def admin_verify(request) :
    id=request.COOKIES['user_id']
    if request.method == 'POST':
        uf = UserForm_add_faculty(request.POST)
        if uf.is_valid():
            website = uf.cleaned_data['website']
            title = uf.cleaned_data['title']
            affiliation = uf.cleaned_data['affiliation']
            faculty_id = uf.cleaned_data['faculty_id']
            admin_id = Administrator.objects.filter(admin_id=id).all()[0].admin_id
            faculty_id = User.objects.filter(id__exact=faculty_id).all()[0].id
            faculty = Faculty.objects.create(faculty_id=faculty_id, website=website, title=title,
                                             affiliation=affiliation, verify_date=timezone.localdate(),verify_time=timezone.localtime(), admin_id=admin_id
                                             )
            faculty.save()

            messages.add_message(request, messages.INFO, 'Verify faculty success')
        else:
            messages.add_message(request, messages.INFO, 'Not valid!!')
    else:
        uf = UserForm_add_faculty()
    return render(request,'admin_verify.html',{'userform':uf})


def enroll(request) :
    if request.method == 'POST':
        uf = UserForm_enroll(request.POST)
        if uf.is_valid():
            student_id = uf.cleaned_data['student_id']
            course_id = uf.cleaned_data['course_id']

            time = timezone.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            confirmation_code = re.sub("\D", "", time)
            student_id = User.objects.filter(id__exact=student_id).all()[0].id
            course_id = Course.objects.filter(course_id__exact=course_id).all()[0].course_id
            course_enroll = CourseEnrollment.objects.create(student_id=student_id,course_id=course_id,confirmation_code=confirmation_code,pay_date=timezone.localtime(),pay_time=timezone.localtime())
            course_enroll.save()

            messages.add_message(request, messages.INFO, 'Enroll student success')
        else:
            messages.add_message(request, messages.INFO, 'Not valid!!')
    else:
        uf = UserForm_enroll
    return render(request,'admin_enroll_student.html',{'userform':uf})


def faculty_mark_material(request) :
    if request.method == 'POST':
        uf = UserForm_mark_material(request.POST)
        if uf.is_valid():
            student_id = uf.cleaned_data['student_id']
            m_id = uf.cleaned_data['material_id']
            score = uf.cleaned_data['score']
            student_id = User.objects.filter(id__exact=student_id)
            m_id = CourseMaterial.objects.filter(material_id__exact=m_id)
            student_id = student_id.all()[0].id
            m_id = m_id.all()[0].material_id
            mark_material = CompleteMaterial.objects.create(student_id=student_id,material_id=m_id,score=score,complete_date=timezone.localdate(),complete_time=timezone.localtime())
            mark_material.save()

            course_id = CourseMaterial.objects.filter(material_id__exact=m_id).all()[0].course_id
            course_material_num = CourseMaterial.objects.filter(course_id__exact=course_id).count()
            course_material_complete_num = CompleteMaterial.objects.filter(material__course_id__exact=course_id,student_id__exact=student_id).count()
            if course_material_num == course_material_complete_num :
                time = timezone.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                time = re.sub("\D", "", time)
                complete=complete_course = CourseEnrollment.objects.get(student_id=student_id,course_id=course_id)
                complete.complete_date=timezone.localdate()
                complete.complete_time=timezone.localtime()
                complete.certification_number=time
                complete.save()
            messages.add_message(request, messages.INFO, 'Mark material success')
        else:
            messages.add_message(request, messages.INFO, 'Not valid!')
    else:
        uf = UserForm_mark_material
    return render(request, 'faculty_mark_material_complete.html', {'userform':uf})

def admin_mark_material(request) :
    if request.method == 'POST':
        uf = UserForm_mark_material(request.POST)
        if uf.is_valid():
            student_id = uf.cleaned_data['student_id']
            m_id = uf.cleaned_data['material_id']
            score = uf.cleaned_data['score']
            student_id = User.objects.filter(id__exact=student_id)
            m_id = CourseMaterial.objects.filter(material_id__exact=m_id)
            student_id = student_id.all()[0].id
            m_id = m_id.all()[0].material_id
            mark_material = CompleteMaterial.objects.create(student_id=student_id,material_id=m_id,score=score,complete_date=timezone.localdate(),complete_time=timezone.localtime())
            mark_material.save()

            course_id = CourseMaterial.objects.filter(material_id__exact=m_id).all()[0].course_id
            course_material_num = CourseMaterial.objects.filter(course_id__exact=course_id).count()
            course_material_complete_num = CompleteMaterial.objects.filter(material__course_id__exact=course_id,student_id__exact=student_id).count()
            if course_material_num == course_material_complete_num :
                time = timezone.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                time = re.sub("\D", "", time)
                complete=complete_course = CourseEnrollment.objects.get(student_id=student_id,course_id=course_id)
                complete.complete_date=timezone.localdate()
                complete.complete_time=timezone.localtime()
                complete.certification_number=time
                complete.save()
            messages.add_message(request, messages.INFO, 'Mark material success')
        else:
            messages.add_message(request, messages.INFO, 'Not valid!')
    else:
        uf = UserForm_mark_material
    return render(request, 'admin_mark_material_complete.html', {'userform':uf})




def login(request):
    if request.method == 'POST':
        uf = UserForm_login(request.POST)
        if uf.is_valid():
            email = uf.cleaned_data['email']
            password = uf.cleaned_data['password'].encode('utf8')
            user = User.objects.filter(email__exact=email)
            pwd_ = user.all()[0].password
            pwd_ = bytes(pwd_, encoding = "utf8")
            id = user.all()[0].id
            admin_id=Administrator.objects.filter(admin_id__exact=id)
            faculty_id = Faculty.objects.filter(faculty_id__exact=id)
            if bcrypt.checkpw(password,pwd_) :
                if admin_id :
                    response=render_to_response('login_role_admin.html', {'id' : admin_id})
                    response.set_cookie('user_id', id, 3600)
                    return response
                if faculty_id :
                    response=render_to_response('login_role_faculty.html',{'id' : faculty_id})
                    response.set_cookie('user_id',id,3600)
                    return response

                response= render_to_response('student_homepage.html',{'id' : id})
                response.set_cookie('user_id', id, 3600)

                return response
            else:
                messages.add_message(request, messages.INFO, 'Wrong password or Email')
                return render(request, 'login.html', {'userform': uf})

    else:
        uf = UserForm_login()
        return render(request,'login.html',{'userform':uf})


def stduent_course(request) :

    id=request.COOKIES['user_id']
    student_enroll = CourseTopics.objects.select_related().filter(course__courseenrollment__student_id=id,course__courseenrollment__certification_number__isnull=True)
    student_complete = CourseTopics.objects.select_related().filter(course__courseenrollment__student_id=id,course__courseenrollment__certification_number__isnull=False)
    student_interest = CourseTopics.objects.select_related().filter(course__interest__student_id=id,course__courseenrollment__certification_number__isnull=False)

    return render_to_response('student_course.html',{'interest': student_interest,'enroll': student_enroll,
                                                     "complete":student_complete})


def student_certification(request) :
    id = request.COOKIES['user_id']
    student_complete = CourseEnrollment.objects.select_related().filter(student_id__exact=id,
                                                                        certification_number__isnull=False)
    return render_to_response('student_certification.html', {'complete':student_complete})


def student_account_history(request) :
    id = request.COOKIES['user_id']
    student_all_course_take = CourseEnrollment.objects.select_related().filter(student_id__exact=id)
    total_paid = Course.objects.select_related().filter(courseenrollment__student_id__exact=id).aggregate(Sum('cost'))
    return render_to_response('student_account_history.html', {'all_course_take':student_all_course_take, 'total_paid':total_paid})


def student_course_material(request) :

    id = request.COOKIES['user_id']
    if request.method == 'POST':
        uf = UserForm_check_course_material(request.POST)
        if uf.is_valid():
            course_id = uf.cleaned_data['course_id']
            course = Course.objects.filter(course_id__exact=course_id)
            course_id = course.all()[0].course_id
            course_enroll = CourseEnrollment.objects.filter(student_id__exact=id,course_id__exact=course_id)

            course_name = course.all()[0].name
            if course:
                if course_enroll:

                    comple_mat = CompleteMaterial.objects.select_related().filter(material__course_id__exact=course_id,
                                                                                 student_id__exact=id)
                    m_id = comple_mat.values('material_id')
                    not_comple_mat = CourseMaterial.objects.select_related().filter(course_id__exact=course_id).exclude(
                        material_id__in=m_id)
                    return render_to_response('student_course_material_info.html',{'complete_material':comple_mat,
                                                  'not_com_mat':not_comple_mat,'course_name':course_name})
                else:
                    messages.add_message(request, messages.INFO, 'Sorry, You Are Not Taking This Class')
            else:
                messages.add_message(request, messages.INFO, 'Wrong course ID')
    else:
        uf = UserForm_check_course_material()
    return render(request, 'student_course_material.html', {'userform': uf})


def student_playlists(request) :
    id = request.COOKIES['user_id']
    playlists = Playlist.objects.filter(user_id=id,)
    return render_to_response('student_playlist.html', {'playlists':playlists})

def student_select_playlist(request) :
    id = request.COOKIES['user_id']
    if request.method == 'POST':
        uf = UserForm_check_playlist(request.POST)
        if uf.is_valid():
            playlist_id = uf.cleaned_data['playlist_id']
            playlist_id = Playlist.objects.filter(user_id=id,playlist_id=playlist_id)
            if playlist_id :
                playlist_id=playlist_id.all()[0].playlist_id
                playlist = PlaylistContain.objects.filter(playlist_id=playlist_id)
                return render(request,'student_show_playlist.html',{'playlist':playlist})
            else :
                messages.add_message(request, messages.INFO, 'Sorry, This is Not Your Playlist')
    else:
        uf = UserForm_check_playlist()
    return render(request, 'student_select_playlist.html', {'userform': uf})


def student_show_playlist(request) :
    return render_to_response('student_show_playlist.html')


def student_course_material_info(request) :
    return render_to_response('student_course_material_info.html')


def student_homepage(request) :
    return render_to_response('student_homepage.html')


def faculty_homepage(request) :
    return render_to_response('faculty_homepage.html')

def admin_homepage(request) :
    return render_to_response('admin_homepage.html')
def index(request) :
    return render_to_response('index.html')


def admin_report1(request) :
    with connection.cursor() as cursor:
        cursor.execute("select q.Student_ID as Student_ID, q.FirstName as FirstName, q.LastName as LastName, q.Country, q.Course_Complete_Number as Course_Complete_Number, avg(cm.score) as Avg_Score  from Complete_Material cm inner join ((select u.ID as Student_ID, u.FirstName as FirstName, u.LastName as LastName, u.Country as Country, count(ce.Course_ID) as Course_Complete_Number from (user u inner join course_enrollment ce on u.ID = ce.Student_ID) inner join Course c on c.Course_ID = ce.Course_ID where u.Country = 'China' and ce.Certification_Number is not null group by u.ID)  union (select u.ID as Student_ID, u.FirstName as FirstName, u.LastName as LastName, u.Country as Country, count(ce.Course_ID) as Course_Complete_Number from (user u inner join course_enrollment ce on u.ID = ce.Student_ID) inner join Course c on c.Course_ID = ce.Course_ID where u.Country = 'Canada' and ce.Certification_Number is not null group by u.ID)) q on cm. Student_ID = q.Student_ID group by Student_ID order by Avg_Score DESC, Course_Complete_Number")
        r1=dictfetchall(cursor)
        print(r1)
    return render(request, 'admin_report1.html', {'r1':r1})


def admin_report2(request) :
    with connection.cursor() as cursor:
        cursor.execute("Select cm.Name as coursematerial_name, count(cm.Material_ID) as material_count, p.Name as playlist_name,  t.Topic_Name as topic_name,c.Name as course_name From ((((Playlist p inner join Playlist_Contain pc on p.Playlist_ID=pc.Playlist_ID) Inner join Course_Material cm on cm.Material_ID=pc.Material_ID) Inner join Course c on c.Course_ID= cm.Course_ID) Inner join Topics t on t.Topic_ID= c.Primary_Topic_ID) where t.Topic_Name like 'Computer%' Group by cm.Material_ID HAVING material_count>=1 order by material_count desc ,topic_name, course_name")
        r1=dictfetchall(cursor)
        print(r1)
    return render(request, 'admin_report2.html', {'r1':r1})


def admin_report3(request) :
    with connection.cursor() as cursor:
        cursor.execute("select c.Course_ID, c.Name, t.Topic_Name,  (select count(*) from Course_Material cm where cm.Course_ID = c.Course_ID) as material_number, (select count(*) from Course_Material cm inner join Question_Relation qr on cm.Material_ID = qr.Material_ID where cm.Course_ID = c.Course_ID) as question_number, (select count(*) from ((Course_Material cm inner join Question_Relation qr on cm.Material_ID = qr.Material_ID) inner join Course_Question cq on qr.Question_ID = cq.Question_ID) inner join Like_course_question l on l.Question_ID = cq.Question_ID where cm.Course_ID = c.Course_ID and u.ID=l.Student_ID) as like_number from ((Course c left join Topics t on c.Primary_Topic_ID = t.Topic_ID) left join course_enrollment ce on c.Course_ID = ce.Course_ID) left join user u on u.ID = ce.Student_ID where u.ID = 1 order by topic_name desc, course_id asc")
        r1=dictfetchall(cursor)
        print(r1)
    return render(request, 'admin_report3.html', {'r1':r1})


def admin_report4(request) :
    with connection.cursor() as cursor:
        cursor.execute("select Distinct c.Course_ID, c.Name as course_name,t.Topic_Name, u.FirstName, u.LastName, (select count(*) from Interest i  where c.Course_ID = i.Course_ID )as interest_number, (select count(*) from Course_Enrollment ce where c.Course_ID = ce.Course_ID AND ce.Certification_Number is null) as enroll_number, (select count(*) from Course_Enrollment ce where c.Course_ID = ce.Course_ID AND ce.Certification_Number != 'null') as fanished_number from (((course c  left join course_enrollment ce on c.Course_ID = ce.Course_ID) left join create_course cc on cc.Course_ID = c.Course_ID) left join user u on cc.Faculty_ID = u.ID) left join topics t on c.Primary_Topic_ID = t.Topic_ID order by enroll_number desc, fanished_number desc")
        r1=dictfetchall(cursor)
        print(r1)
    return render(request, 'admin_report4.html', {'r1':r1})


def admin_report5(request) :
    with connection.cursor() as cursor:
        cursor.execute("select c.Name as Course_Name, avg(cpm.Score) as Avg_Score, a.count as A_Num, b.count as B_Num, c.count as C_Num from ((((course c inner join course_material com on c.Course_ID = com.Course_ID) inner join complete_material cpm on com.Material_ID = cpm.Material_ID) inner join (select count(*) as count from course c inner join course_material com on c.Course_ID = com.Course_ID inner join complete_material cpm on com.Material_ID = cpm.Material_ID where c.Course_ID = '70000003' and cpm.Score > 80) as a) inner join (select count(*) as count from course c inner join course_material com on c.Course_ID = com.Course_ID inner join complete_material cpm on com.Material_ID = cpm.Material_ID where c.Course_ID = '70000003'  and cpm.Score < 80 and cpm.Score >= 60 ) as b) inner join (select count(*) as count from course c inner join course_material com on c.Course_ID = com.Course_ID inner join complete_material cpm on com.Material_ID = cpm.Material_ID where c.Course_ID = '70000003'  and cpm.Score < 60 ) as c where c.Course_ID = '70000003' ")
        r1=dictfetchall(cursor)
        print(r1)
    return render(request, 'admin_report5.html', {'r1':r1})

def faculty_report1(request) :
    with connection.cursor() as cursor:
        cursor.execute("select q.Student_ID as Student_ID, q.FirstName as FirstName, q.LastName as LastName, q.Country, q.Course_Complete_Number as Course_Complete_Number, avg(cm.score) as Avg_Score  from Complete_Material cm inner join ((select u.ID as Student_ID, u.FirstName as FirstName, u.LastName as LastName, u.Country as Country, count(ce.Course_ID) as Course_Complete_Number from (user u inner join course_enrollment ce on u.ID = ce.Student_ID) inner join Course c on c.Course_ID = ce.Course_ID where u.Country = 'China' and ce.Certification_Number is not null group by u.ID)  union (select u.ID as Student_ID, u.FirstName as FirstName, u.LastName as LastName, u.Country as Country, count(ce.Course_ID) as Course_Complete_Number from (user u inner join course_enrollment ce on u.ID = ce.Student_ID) inner join Course c on c.Course_ID = ce.Course_ID where u.Country = 'Canada' and ce.Certification_Number is not null group by u.ID)) q on cm. Student_ID = q.Student_ID group by Student_ID order by Avg_Score DESC, Course_Complete_Number")
        r1=dictfetchall(cursor)
        print(r1)
    return render(request, 'faculty_report1.html', {'r1':r1})


def faculty_report2(request) :
    with connection.cursor() as cursor:
        cursor.execute("Select cm.Name as coursematerial_name, count(cm.Material_ID) as material_count, p.Name as playlist_name,  t.Topic_Name as topic_name,c.Name as course_name From ((((Playlist p inner join Playlist_Contain pc on p.Playlist_ID=pc.Playlist_ID) Inner join Course_Material cm on cm.Material_ID=pc.Material_ID) Inner join Course c on c.Course_ID= cm.Course_ID) Inner join Topics t on t.Topic_ID= c.Primary_Topic_ID) where t.Topic_Name like 'Computer%' Group by cm.Material_ID HAVING material_count>=1 order by material_count desc ,topic_name, course_name")
        r1=dictfetchall(cursor)
        print(r1)
    return render(request, 'faculty_report2.html', {'r1':r1})


def faculty_report3(request) :
    with connection.cursor() as cursor:
        cursor.execute("select c.Course_ID, c.Name, t.Topic_Name,  (select count(*) from Course_Material cm where cm.Course_ID = c.Course_ID) as material_number, (select count(*) from Course_Material cm inner join Question_Relation qr on cm.Material_ID = qr.Material_ID where cm.Course_ID = c.Course_ID) as question_number, (select count(*) from ((Course_Material cm inner join Question_Relation qr on cm.Material_ID = qr.Material_ID) inner join Course_Question cq on qr.Question_ID = cq.Question_ID) inner join Like_course_question l on l.Question_ID = cq.Question_ID where cm.Course_ID = c.Course_ID and u.ID=l.Student_ID) as like_number from ((Course c left join Topics t on c.Primary_Topic_ID = t.Topic_ID) left join course_enrollment ce on c.Course_ID = ce.Course_ID) left join user u on u.ID = ce.Student_ID where u.ID = 1 order by topic_name desc, course_id asc")
        r1=dictfetchall(cursor)
        print(r1)
    return render(request, 'faculty_report3.html', {'r1':r1})


def faculty_report4(request) :
    with connection.cursor() as cursor:
        cursor.execute("select Distinct c.Course_ID, c.Name as course_name,t.Topic_Name, u.FirstName, u.LastName, (select count(*) from Interest i  where c.Course_ID = i.Course_ID )as interest_number, (select count(*) from Course_Enrollment ce where c.Course_ID = ce.Course_ID AND ce.Certification_Number is null) as enroll_number, (select count(*) from Course_Enrollment ce where c.Course_ID = ce.Course_ID AND ce.Certification_Number != 'null') as fanished_number from (((course c  left join course_enrollment ce on c.Course_ID = ce.Course_ID) left join create_course cc on cc.Course_ID = c.Course_ID) left join user u on cc.Faculty_ID = u.ID) left join topics t on c.Primary_Topic_ID = t.Topic_ID order by enroll_number desc, fanished_number desc")
        r1=dictfetchall(cursor)
        print(r1)
    return render(request, 'faculty_report4.html', {'r1':r1})


def faculty_report5(request) :
    with connection.cursor() as cursor:
        cursor.execute("select c.Name as Course_Name, avg(cpm.Score) as Avg_Score, a.count as A_Num, b.count as B_Num, c.count as C_Num from ((((course c inner join course_material com on c.Course_ID = com.Course_ID) inner join complete_material cpm on com.Material_ID = cpm.Material_ID) inner join (select count(*) as count from course c inner join course_material com on c.Course_ID = com.Course_ID inner join complete_material cpm on com.Material_ID = cpm.Material_ID where c.Course_ID = '70000003' and cpm.Score > 80) as a) inner join (select count(*) as count from course c inner join course_material com on c.Course_ID = com.Course_ID inner join complete_material cpm on com.Material_ID = cpm.Material_ID where c.Course_ID = '70000003'  and cpm.Score < 80 and cpm.Score >= 60 ) as b) inner join (select count(*) as count from course c inner join course_material com on c.Course_ID = com.Course_ID inner join complete_material cpm on com.Material_ID = cpm.Material_ID where c.Course_ID = '70000003'  and cpm.Score < 60 ) as c where c.Course_ID = '70000003' ")
        r1=dictfetchall(cursor)
        print(r1)
    return render(request, 'faculty_report5.html', {'r1':r1})


def dictfetchall(cursor):
    desc = cursor.description
    return [
    dict(zip([col[0] for col in desc], row))
    for row in cursor.fetchall()
    ]

