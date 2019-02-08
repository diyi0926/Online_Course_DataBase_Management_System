# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdminPosition(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    admin = models.ForeignKey('Administrator', models.DO_NOTHING, db_column='Admin_ID')  # Field name made lowercase.
    position = models.CharField(db_column='Position', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'admin_position'


class Administrator(models.Model):
    admin = models.ForeignKey('User', models.DO_NOTHING, db_column='Admin_ID', primary_key=True)  # Field name made lowercase.
    verify_date = models.DateField(db_column='Verify_Date', blank=True, null=True)  # Field name made lowercase.
    verify_time = models.TimeField(db_column='Verify_Time', blank=True, null=True)  # Field name made lowercase.
    grantor_id = models.IntegerField(db_column='Grantor_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'administrator'


class CompleteMaterial(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    student = models.ForeignKey('User', models.DO_NOTHING, db_column='Student_ID')  # Field name made lowercase.
    material = models.ForeignKey('CourseMaterial', models.DO_NOTHING, db_column='Material_ID', blank=True, null=True)  # Field name made lowercase.
    complete_date = models.DateField(db_column='Complete_Date', blank=True, null=True)  # Field name made lowercase.
    complete_time = models.TimeField(db_column='Complete_Time', blank=True, null=True)  # Field name made lowercase.
    score = models.CharField(db_column='Score', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'complete_material'


class Course(models.Model):
    course_id = models.IntegerField(db_column='Course_ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    icon = models.CharField(db_column='Icon', max_length=45, blank=True, null=True)  # Field name made lowercase.
    cost = models.IntegerField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    primary_topic = models.ForeignKey('Topics', models.DO_NOTHING, db_column='Primary_Topic_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'course'


class CourseEnrollment(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    student = models.ForeignKey('User', models.DO_NOTHING, db_column='Student_ID')  # Field name made lowercase.
    course = models.ForeignKey(Course, models.DO_NOTHING, db_column='Course_ID')  # Field name made lowercase.
    confirmation_code = models.CharField(db_column='Confirmation_Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pay_date = models.DateField(db_column='Pay_Date', blank=True, null=True)  # Field name made lowercase.
    pay_time = models.TimeField(db_column='Pay_Time', blank=True, null=True)  # Field name made lowercase.
    comment = models.TextField(db_column='Comment', blank=True, null=True)  # Field name made lowercase.
    certification_number = models.CharField(db_column='Certification_Number', max_length=20, blank=True, null=True)  # Field name made lowercase.
    complete_date = models.DateField(db_column='Complete_Date', blank=True, null=True)  # Field name made lowercase.
    complete_time = models.TimeField(db_column='Complete_Time', blank=True, null=True)  # Field name made lowercase.
    rating = models.CharField(db_column='Rating', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'course_enrollment'


class CourseMaterial(models.Model):
    material_id = models.IntegerField(db_column='Material_ID', primary_key=True)  # Field name made lowercase.
    course = models.ForeignKey(Course, models.DO_NOTHING, db_column='Course_ID', blank=True, null=True)  # Field name made lowercase.
    material_order = models.IntegerField(db_column='Material_Order', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'course_material'


class CourseQuestion(models.Model):
    question_id = models.IntegerField(db_column='Question_ID', primary_key=True)  # Field name made lowercase.
    student = models.ForeignKey('User', models.DO_NOTHING, db_column='Student_ID', blank=True, null=True)  # Field name made lowercase.
    faculty = models.ForeignKey('Faculty', models.DO_NOTHING, db_column='Faculty_ID', blank=True, null=True)  # Field name made lowercase.
    answer = models.TextField(db_column='Answer', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'course_question'


class CourseTopics(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    course = models.ForeignKey('Course', models.DO_NOTHING, db_column='Course_ID')  # Field name made lowercase.
    secondary_topic = models.ForeignKey('Topics', models.DO_NOTHING, db_column='Secondary_Topic_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'course_topics'


class CreateCourse(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    faculty = models.ForeignKey('Faculty', models.DO_NOTHING, db_column='Faculty_ID')  # Field name made lowercase.
    course = models.ForeignKey(Course, models.DO_NOTHING, db_column='Course_ID')  # Field name made lowercase.
    creation_date = models.DateField(db_column='Creation_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'create_course'


class DownloadFiles(models.Model):
    material = models.ForeignKey(CourseMaterial, models.DO_NOTHING, db_column='Material_ID', primary_key=True)  # Field name made lowercase.
    path = models.CharField(db_column='Path', max_length=100, blank=True, null=True)  # Field name made lowercase.
    size = models.CharField(db_column='Size', max_length=45, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'download_files'


class Faculty(models.Model):
    faculty = models.ForeignKey('User', models.DO_NOTHING, db_column='Faculty_ID', primary_key=True)  # Field name made lowercase.
    website = models.CharField(db_column='Website', max_length=45, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=45, blank=True, null=True)  # Field name made lowercase.
    affiliation = models.CharField(db_column='Affiliation', max_length=45, blank=True, null=True)  # Field name made lowercase.
    verify_date = models.DateField(db_column='Verify_Date', blank=True, null=True)  # Field name made lowercase.
    verify_time = models.TimeField(db_column='Verify_Time', blank=True, null=True)  # Field name made lowercase.
    admin = models.ForeignKey(Administrator, models.DO_NOTHING, db_column='Admin_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'faculty'


class Interest(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    student = models.ForeignKey('User', models.DO_NOTHING, db_column='Student_ID')  # Field name made lowercase.
    course = models.ForeignKey(Course, models.DO_NOTHING, db_column='Course_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'interest'


class LikeCourseQuestion(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    student = models.ForeignKey('User', models.DO_NOTHING, db_column='Student_ID')  # Field name made lowercase.
    question = models.ForeignKey(CourseQuestion, models.DO_NOTHING, db_column='Question_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'like_course_question'


class Link(models.Model):
    material = models.ForeignKey(CourseMaterial, models.DO_NOTHING, db_column='Material_ID', primary_key=True)  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link'


class Playlist(models.Model):
    playlist_id = models.IntegerField(db_column='Playlist_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='User_ID', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'playlist'


class PlaylistContain(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    playlist = models.ForeignKey(Playlist, models.DO_NOTHING, db_column='Playlist_ID')  # Field name made lowercase.
    material = models.ForeignKey(CourseMaterial, models.DO_NOTHING, db_column='Material_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'playlist_contain'


class Post(models.Model):
    material = models.ForeignKey(CourseMaterial, models.DO_NOTHING, db_column='Material_ID', primary_key=True)  # Field name made lowercase.
    text = models.TextField(db_column='Text', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'post'


class QuestionRelation(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    material = models.ForeignKey(CourseMaterial, models.DO_NOTHING, db_column='Material_ID')  # Field name made lowercase.
    question = models.ForeignKey(CourseQuestion, models.DO_NOTHING, db_column='Question_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'question_relation'


class Quiz(models.Model):
    material = models.ForeignKey(CourseMaterial, models.DO_NOTHING, db_column='Material_ID', primary_key=True)  # Field name made lowercase.
    passing_score = models.CharField(db_column='Passing_Score', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'quiz'


class QuizQuestion(models.Model):
    question_number = models.IntegerField(db_column='Question_Number', primary_key=True)  # Field name made lowercase.
    text = models.TextField(db_column='Text', blank=True, null=True)  # Field name made lowercase.
    material = models.ForeignKey(Quiz, models.DO_NOTHING, db_column='Material_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'quiz_question'


class QuizQuestionAnswers(models.Model):
    answer_number = models.IntegerField(db_column='Answer_Number', primary_key=True)  # Field name made lowercase.
    text = models.TextField(db_column='Text', blank=True, null=True)  # Field name made lowercase.
    feedback = models.TextField(db_column='Feedback', blank=True, null=True)  # Field name made lowercase.
    indication = models.TextField(db_column='Indication', blank=True, null=True)  # Field name made lowercase.
    question_number = models.ForeignKey(QuizQuestion, models.DO_NOTHING, db_column='Question_Number', blank=True, null=True)  # Field name made lowercase.
    student_number = models.ForeignKey('User', models.DO_NOTHING, db_column='Student_Number', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'quiz_question_answers'


class Topics(models.Model):
    topic_id = models.IntegerField(db_column='Topic_ID', primary_key=True)  # Field name made lowercase.
    topic_name = models.CharField(db_column='Topic_Name', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'topics'


class User(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=45)  # Field name made lowercase.
    password = models.CharField(max_length=32)
    firstname = models.CharField(db_column='FirstName', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=20, blank=True, null=True)  # Field name made lowercase.
    picture = models.CharField(db_column='Picture', max_length=45, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='CIty', max_length=45, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=45, blank=True, null=True)  # Field name made lowercase.
    postal_code = models.CharField(db_column='Postal_Code', max_length=45, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user'


class UserContact(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='User_ID')  # Field name made lowercase.
    number = models.CharField(db_column='Number', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_contact'
