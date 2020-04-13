# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TAdmin(models.Model):
    admin_name = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    salt = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_admin'


class TChapter(models.Model):
    buddhist = models.ForeignKey('TGhosa', models.DO_NOTHING, blank=True, null=True)
    chapter = models.CharField(max_length=50, blank=True, null=True)
    voice_url = models.ImageField(upload_to='audio',max_length=50, blank=True, null=True)
    memory = models.CharField(max_length=20, blank=True, null=True)
    duration = models.CharField(max_length=20, blank=True, null=True)
    upload_time = models.DateField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_chapter'


class TCounter(models.Model):
    counter_name = models.CharField(max_length=50, blank=True, null=True)
    homework_data = models.DateTimeField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    homework = models.ForeignKey('THomework', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_counter'


class TGhosa(models.Model):
    album_name = models.CharField(max_length=20, blank=True, null=True)
    album_img = models.ImageField(upload_to='pic', default=None,max_length=50, blank=True, null=True)
    grade = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    author = models.CharField(max_length=20, blank=True, null=True)
    broadcast = models.CharField(max_length=20, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    issue_data = models.DateTimeField(blank=True, null=True)
    intro = models.TextField(blank=True, null=True)
    upload_data = models.DateField(auto_now_add=True, blank=True, null=True)
    status = models.CharField(max_length=20,blank=True, null=True)



    class Meta:
        managed = True
        db_table = 't_ghosa'


class THomework(models.Model):
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    homework_name = models.CharField(max_length=50, blank=True, null=True)
    sort = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_homework'


class TImage(models.Model):
    img_url = models.ImageField(upload_to='pic', default=None,blank=True, null=True)
    title = models.CharField(max_length=20, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    upload_time = models.DateField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_image'


class TUser(models.Model):
    username = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    religious_name = models.CharField(max_length=20, blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    head_img = models.ImageField(upload_to='pic', default=None,max_length=50, blank=True, null=True)
    salt = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    mail = models.CharField(max_length=50, blank=True, null=True)
    register_data = models.DateField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 't_user'
