# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

import json
from .searchInfo import dynasty_dict

class CulturalRelicsData(models.Model):
    id = models.BigAutoField(primary_key=True)
    bibliography = models.TextField(blank=True, null=True)
    credit = models.CharField(max_length=600, db_collation='utf8_general_ci', blank=True, null=True)
    dimensions = models.CharField(max_length=300)
    geography = models.CharField(max_length=255, blank=True, null=True)
    img_url = models.CharField(max_length=800, blank=True, null=True)
    label = models.TextField(db_collation='utf8_general_ci', blank=True, null=True)
    medium = models.CharField(max_length=300, blank=True, null=True)
    object_name = models.CharField(max_length=255)
    object_type = models.CharField(max_length=255, blank=True, null=True)
    previous_owner = models.CharField(max_length=400, blank=True, null=True)
    provenance = models.TextField(blank=True, null=True)
    time_period = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    cat1 = models.CharField(max_length=255, blank=True, null=True)
    cat2 = models.CharField(max_length=255, blank=True, null=True)
    cat3 = models.CharField(max_length=255, blank=True, null=True)
    makers_born = models.TextField(blank=True, null=True)
    makers_job = models.CharField(max_length=255, blank=True, null=True)
    makers_name = models.CharField(max_length=255, blank=True, null=True)
    museum = models.CharField(max_length=255, blank=True, null=True)
    object_id = models.CharField(max_length=255, blank=True, null=True)

    def like_times(self):
        return Star.objects.filter(cltrrlcs=self).count()

    def brief_json(self, type):
        object = {}
        object['id'] = self.id
        object['name'] = self.object_name
        try:
            img_list = filter(None, self.img_url.split(',')) 
        except AttributeError:
            img_list = []
        object['img_url'] = ''
        for img in img_list:
            try:
                url = (ImgUrlTable.objects.get(img_id=img)).url
                #https://pic.rmb.bdstatic.com/bjh/
                url = url.split('/')[-1]
                url = url.split('.')[0]
                object['img_url'] += url + ','
                if type == 1:
                    break
            except ImgUrlTable.DoesNotExist:
                pass  
        object['img_url'] = object['img_url'][:-1]
        object['museum'] = self.museum
        object['location'] = self.geography
        object['time_period'] = self.time_period
        new_dynasty_dict = {v : k for k, v in dynasty_dict.items()}
        if self.time_period in new_dynasty_dict.keys():
            object['dynasty'] = new_dynasty_dict[self.time_period]
        else :
            object['dynasty'] = None
        object['like_times'] = self.cltrrlcs_stars.all().count()
        object['comment_times'] = self.cltrrlcs_comments.all().count()
        return object

    def json(self):
        object = self.brief_json(0)
        object['bibliography'] = self.bibliography
        object['credit'] = self.credit
        object['dimensions'] = self.dimensions
        object['label'] = self.label
        object['medium'] = self.medium
        object['object_type'] = self.object_type
        object['previous_owner'] = self.previous_owner
        object['provenance'] = self.provenance
        object['url'] = self.url
        object['cat1'] = self.cat1
        object['cat2'] = self.cat2
        object['cat3'] = self.cat3
        object['makers_born'] = self.makers_born
        object['makers_name'] = self.makers_name
        object['makers_job'] = self.makers_job
        object['object_id'] = self.object_id
        return object

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'cultural_relics_data'
        verbose_name = '??????'
        verbose_name_plural = verbose_name

class ImgUrlTable(models.Model):
    img_id = models.CharField(primary_key=True, max_length=255)
    url = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'img_url_table'


class UserManager(BaseUserManager):

    def create_superuser(self, username, password, email, **kargs):
        kargs['is_superuser'] = True
        kargs['is_staff'] = True
        user = self.model(username=username, email=email, **kargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, email, **kargs):
        user = self.model(username=username, email=email, **kargs)
        user.set_password(password)
        user.save()
        return user

class User(AbstractUser):
    GENDER_CHOICES = (
        ('f', '???'),
        ('m', '???'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    pic_url = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)

    objects = UserManager()

    def json(self):
        user = {}
        user['username'] = self.username
        user['email'] = self.email
        user['gender'] = self.gender
        user['location'] = self.location
        user['pic_url'] = self.pic_url
        user['desc'] = self.desc
        return user

    class Meta:
        verbose_name = '??????'
        verbose_name_plural = verbose_name
        db_table = 'a_user'

class Dynamic(models.Model):
    # ???????????????????????? ?????? cltrrcls.cltrrcls_dynamics.all()
    cltrlrlcs = models.ForeignKey(CulturalRelicsData, related_name='cltrrlcs_dynamics', on_delete=models.CASCADE, blank=True, null=True, verbose_name='??????')

    # ?????????????????? ?????? user.user_dynamics.all()
    user = models.ForeignKey(User, related_name='user_dynamics', on_delete=models.CASCADE, blank=False, verbose_name='????????????')

    text = models.TextField(max_length=1000, blank=True, null=True, verbose_name='????????????')
    files_urls = models.CharField(max_length=255, blank=True, null=True, verbose_name='????????????url')
    time = models.DateTimeField(auto_now_add=True, verbose_name='????????????')

    def json(self):
        dynamic = {}
        dynamic['id'] = self.id

        if self.cltrlrlcs is None:
            dynamic['objectid'] = None
        else:
            dynamic['objectid'] = self.cltrlrlcs.id

        dynamic['user'] = self.user.username

        if self.text is None:
            dynamic['text'] = None
        else:
            dynamic['text'] = self.text

        dynamic['files_urls'] = self.files_urls
        dynamic['time'] = str(self.time)
        dynamic['like_times'] = self.dynamic_stars.all().count()
        dynamic['comment_times'] = self.dynamic_comments.all().count()
        return dynamic

    class Meta:
        verbose_name = '????????????'
        verbose_name_plural = verbose_name
        db_table = 'a_dynamic'

class Comment(models.Model):
    # ?????????????????? cltrrlcs.cltrrcls_comments.all()
    cltrrlcs = models.ForeignKey(CulturalRelicsData, related_name='cltrrlcs_comments', on_delete=models.CASCADE, blank=True, null=True, verbose_name='??????')
    # ?????????????????? dynamic.dynamic_comments.all()
    dynamic = models.ForeignKey(Dynamic, related_name='dynamic_comments', on_delete=models.CASCADE, blank=True, null=True, verbose_name='????????????')
    # ?????????????????? comment.comment_comments.all()
    comment = models.ForeignKey('self', related_name='comment_comments', on_delete=models.CASCADE, blank=True, null=True, verbose_name='????????????')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments', verbose_name='??????')
    reply_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_replys', blank=True, null=True, verbose_name='????????????')
    time = models.DateTimeField(auto_now_add=True, verbose_name='????????????')
    text = models.TextField(max_length=1000, blank=True, null=True, verbose_name='????????????')
    images = models.CharField(max_length=255, blank=True, null=True, verbose_name='????????????')

    def json(self):
        comment = {}
        comment['id'] = self.id
        comment['user'] = self.user.username

        if self.cltrrlcs is None:
            comment['objectid'] = None
        else:
            comment['objectid'] = self.cltrrlcs.id

        if self.dynamic is None:
            comment['dynamicid'] = None
        else:
            comment['dynamicid'] = self.dynamic.id

        if self.comment is None:
            comment['commentid'] = None
        else:
            comment['commentid'] = self.comment.id

        if self.reply_user is None:
            comment['reply_user'] = None
        else:
            comment['reply_user'] = self.reply_user.username

        time = str(self.time).split(".")[0].split(":")
        comment['time'] = time[0] + ":" + time[1]
        
        if self.text is None:
            comment['text'] = None
        else:
            comment['text'] = self.text

        comment['images'] = self.images
        comment['like_times'] = self.comment_stars.all().count()
        return comment


    class Meta:
        verbose_name = '????????????'
        verbose_name_plural = verbose_name
        db_table = 'a_comment'

class Star(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_star', verbose_name='??????')
    # ???????????? ?????? cltrrlcs.cltrrlcs_stars.all()
    cltrrlcs = models.ForeignKey(CulturalRelicsData, related_name='cltrrlcs_stars', on_delete=models.CASCADE, blank=True, null=True, verbose_name='??????')
    # ???????????? ?????? dynamic.dynamic_stars.all()
    dynamic = models.ForeignKey(Dynamic, related_name='dynamic_stars', on_delete=models.CASCADE, blank=True, null=True, verbose_name='????????????')
    # ???????????? ?????? comment.comment_stars.all()
    comment = models.ForeignKey(Comment, related_name='comment_stars', on_delete=models.CASCADE, blank=True, null=True, verbose_name='??????')

    time = models.DateTimeField(auto_now_add=True, verbose_name='????????????')

    def json(self):
        star = {}
        star['id'] = self.id
        star['user'] = self.user.username

        if self.cltrrlcs is not None:
            star['objectid'] = self.cltrrlcs.id
        else:
            star['objectid'] = None

        if self.dynamic is not None:
            star['dynamicid'] = self.dynamic.id
        else:
            star['dynamicid'] = None

        if self.comment is not None:
            star['commentid'] = self.comment.id
        else:
            star['commentid'] = None
        star['time'] = str(self.time)
        return star

    class Meta:
        verbose_name = '????????????'
        verbose_name_plural = verbose_name
        db_table = 'a_star'

class Attention(models.Model):
    # ?????????????????????????????? user.user_me_follow.all()
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_me_follow', verbose_name='????????????')

    # ?????????????????????????????? user.user_follow_me.all()
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_follow_me', verbose_name='???????????????')

    time  = models.DateTimeField(auto_now_add=True, verbose_name='????????????')

    class Meta:
        verbose_name = '??????????????????'
        verbose_name_plural = verbose_name
        db_table = 'a_attention'

class Notification(models.Model):

    NTFCTN_TYPE_CHOICES = (
        ('f', 'follow'),  # ????????????
        ('c', 'comment'), # ????????????
        ('l', 'like'),    # ?????????
        ('r', 'reply'),   # ????????????
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notifications', verbose_name='??????')
    action_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_actions', verbose_name='??????????????????')
    type = models.CharField(max_length=1, choices=NTFCTN_TYPE_CHOICES)
    time = models.DateTimeField(auto_now_add=True, verbose_name='????????????')

    # like ????????? ??????????????????ID
    star = models.ForeignKey(Star, related_name='star_ntfctns', on_delete=models.CASCADE, verbose_name='????????????', blank=True, null=True)
    # reply ???????????? ????????????ID
    comment = models.ForeignKey(Comment, related_name='comment_ntfctns', on_delete=models.CASCADE, verbose_name='????????????', blank=True, null=True)

    read = models.BooleanField(verbose_name='????????????')

    class Meta:
        verbose_name = '????????????'
        verbose_name_plural = verbose_name
        db_table = 'a_notification'
