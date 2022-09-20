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
        verbose_name = '文物'
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
        ('f', '女'),
        ('m', '男'),
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
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        db_table = 'a_user'

class Dynamic(models.Model):
    # 引用某文物的动态 查询 cltrrcls.cltrrcls_dynamics.all()
    cltrlrlcs = models.ForeignKey(CulturalRelicsData, related_name='cltrrlcs_dynamics', on_delete=models.CASCADE, blank=True, null=True, verbose_name='文物')

    # 用户所有动态 查询 user.user_dynamics.all()
    user = models.ForeignKey(User, related_name='user_dynamics', on_delete=models.CASCADE, blank=False, verbose_name='发布用户')

    text = models.TextField(max_length=1000, blank=True, null=True, verbose_name='动态文本')
    files_urls = models.CharField(max_length=255, blank=True, null=True, verbose_name='动态文件url')
    time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

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
        verbose_name = '用户动态'
        verbose_name_plural = verbose_name
        db_table = 'a_dynamic'

class Comment(models.Model):
    # 文物评论查询 cltrrlcs.cltrrcls_comments.all()
    cltrrlcs = models.ForeignKey(CulturalRelicsData, related_name='cltrrlcs_comments', on_delete=models.CASCADE, blank=True, null=True, verbose_name='文物')
    # 动态评论查询 dynamic.dynamic_comments.all()
    dynamic = models.ForeignKey(Dynamic, related_name='dynamic_comments', on_delete=models.CASCADE, blank=True, null=True, verbose_name='用户动态')
    # 评论回复查询 comment.comment_comments.all()
    comment = models.ForeignKey('self', related_name='comment_comments', on_delete=models.CASCADE, blank=True, null=True, verbose_name='用户评论')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments', verbose_name='用户')
    reply_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_replys', blank=True, null=True, verbose_name='回复用户')
    time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    text = models.TextField(max_length=1000, blank=True, null=True, verbose_name='评论文本')
    images = models.CharField(max_length=255, blank=True, null=True, verbose_name='评论图片')

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
        verbose_name = '用户评论'
        verbose_name_plural = verbose_name
        db_table = 'a_comment'

class Star(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_star', verbose_name='用户')
    # 文物点赞 查询 cltrrlcs.cltrrlcs_stars.all()
    cltrrlcs = models.ForeignKey(CulturalRelicsData, related_name='cltrrlcs_stars', on_delete=models.CASCADE, blank=True, null=True, verbose_name='文物')
    # 动态点赞 查询 dynamic.dynamic_stars.all()
    dynamic = models.ForeignKey(Dynamic, related_name='dynamic_stars', on_delete=models.CASCADE, blank=True, null=True, verbose_name='用户动态')
    # 评论点赞 查询 comment.comment_stars.all()
    comment = models.ForeignKey(Comment, related_name='comment_stars', on_delete=models.CASCADE, blank=True, null=True, verbose_name='评论')

    time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

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
        verbose_name = '点赞记录'
        verbose_name_plural = verbose_name
        db_table = 'a_star'

class Attention(models.Model):
    # 我关注的所有用户查询 user.user_me_follow.all()
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_me_follow', verbose_name='关注用户')

    # 所有关注我的用户查询 user.user_follow_me.all()
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_follow_me', verbose_name='被关注用户')

    time  = models.DateTimeField(auto_now_add=True, verbose_name='关注时间')

    class Meta:
        verbose_name = '用户关注记录'
        verbose_name_plural = verbose_name
        db_table = 'a_attention'

class Notification(models.Model):

    NTFCTN_TYPE_CHOICES = (
        ('f', 'follow'),  # 关注了你
        ('c', 'comment'), # 评论了你
        ('l', 'like'),    # 赞了你
        ('r', 'reply'),   # 回复了你
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notifications', verbose_name='用户')
    action_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_actions', verbose_name='通知动作用户')
    type = models.CharField(max_length=1, choices=NTFCTN_TYPE_CHOICES)
    time = models.DateTimeField(auto_now_add=True, verbose_name='动作时间')

    # like 赞了你 需要点赞记录ID
    star = models.ForeignKey(Star, related_name='star_ntfctns', on_delete=models.CASCADE, verbose_name='相关点赞', blank=True, null=True)
    # reply 回复了你 需要评论ID
    comment = models.ForeignKey(Comment, related_name='comment_ntfctns', on_delete=models.CASCADE, verbose_name='相关评论', blank=True, null=True)

    read = models.BooleanField(verbose_name='是否已读')

    class Meta:
        verbose_name = '用户通知'
        verbose_name_plural = verbose_name
        db_table = 'a_notification'
