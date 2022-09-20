from email.mime import image
import json
import os

# Create your views here.

from faker import Faker
from faker.providers import DynamicProvider

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.db.models import Count

from onlinemuseum.models import CulturalRelicsData, Dynamic, User, Comment, Star
from .searchInfo import dynasty_dict, location_dict, medium_dict

from django.core.paginator import Paginator

@csrf_exempt
def login_view(request: HttpRequest):
    if request.method == 'POST':
        data = json.loads(request.body)
        type = 0
        if 'email' in data:
            type = 1
        if type == 1:
            try:
                tuser = User.objects.get(email=data['email'])
            except User.DoesNotExist:
                print('login error : email ont found')
                return HttpResponse('email not found', status=404)
            username = tuser.username
        else:
            try:
                tuser = User.objects.get(username=data['username'])
            except User.DoesNotExist:
                print('login error : user not found')
                return HttpResponse('username not found', status=404)
            username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            jsondata = user.json()
            return JsonResponse(jsondata)
        else:
            print("error : wrong password")
            return HttpResponse('wrong password', status=403)

@csrf_exempt
def logout_view(request: HttpRequest):
    logout(request)
    return HttpResponse('success')

@csrf_exempt
def register_view(request: HttpRequest):

    fake = Faker("zh_CN")
    gender_provider = DynamicProvider(
        provider_name="gender",
        elements=["m", "f"],
    )
    fake.add_provider(gender_provider)

    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        username = data['username']
        if data['username'] == '':
            return HttpResponse("username can\'t be empty", status=403)
        
        try:
            User.objects.get(username=username)
            return HttpResponse('username registered', status=403)
        except User.DoesNotExist:
            pass

        if data['email'] == '':
            return HttpResponse("email can\'t be empty", status=403)
        email = data['email']
        try:
            User.objects.get(email=email)
            return HttpResponse('email registered', status=403)
        except User.DoesNotExist:
            pass
        password = data['password'] 
        gender = fake.gender()
        location = fake.province() + ' ' + fake.city()
        desc = '还没有个人描述，赶快来填写吧！'
        pic_url = 'media/user_pics/default_pic.png'
        user = User.objects.create(
            username=username,
            email=email,
            gender=gender,
            location=location,
            desc=desc,
            pic_url=pic_url,
        )
        user.set_password(password)
        user.save()
        return HttpResponse('success')

@method_decorator(csrf_exempt, name='dispatch')
class UserInfoView(View):
    def get(self, request: HttpRequest, username):
        if request.user.is_authenticated:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return HttpResponse('Not Found', status=404)
            data = user.json()
            return JsonResponse(data)
        return HttpResponse('Login Required', status=403)

    def post(self, request: HttpRequest, username):
        if request.user.is_authenticated:
            data = json.loads(request.body)
            user = authenticate(username=username, password=data['password'])
            if user is not None:
                print('密码正确')
                return JsonResponse({'flag':1})
            else:
                print('密码错误')
                return JsonResponse({'flag':0})
        print("login required")
        return HttpResponse('Login Required', status=403)

    def put(self, request: HttpRequest, username):
        # TODO 头像上传
        if request.user.is_authenticated:
            user = request.user
            data = json.loads(request.body)
            if 'desc' in data:
                user.desc = data['desc']
            if 'location' in data:
                user.location = data['location']
            if 'gender' in data:
                user.gender = data['gender']
            if 'username' in data:
                try:
                    User.objects.get(username=data['username'])
                    print('UserInfo error : username already exists')
                    return HttpResponse('username already exists', status=403)
                except:
                    pass
                user.username = data['username']
            if 'email' in data:
                try:
                    User.objects.get(email=data['email'])
                    print('UserInfo error : email already exists')
                    return HttpResponse('email already exists', status=403)
                except:
                    pass
                user.email = data['email']
            if 'password' in data:
                user.set_password(data['password'])
            user.save()
            return JsonResponse(user.json())
        return HttpResponse('Login Required', status=403)


@method_decorator(csrf_exempt, name='dispatch')
class ObjectsView(View):
    def get(self, request: HttpRequest):
        limit = request.GET.get('limit')
        page = request.GET.get('page')
        choices = request.GET
        cltrlrlcs = CulturalRelicsData.objects.all()
        if 'museum' in choices:
            museum = choices['museum']
            cltrlrlcs = cltrlrlcs.filter(museum=museum)

        if 'dynasty' in choices:
            time_period = dynasty_dict[choices['dynasty']]
            cltrlrlcs = cltrlrlcs.filter(time_period=time_period)

        if 'location' in choices:
            location = location_dict[choices['location']]
            cltrlrlcs = cltrlrlcs.filter(geography__icontains=location)

        if 'medium' in choices:
            mediums =  medium_dict[choices['medium']]
            tmp = cltrlrlcs.filter(medium__icontains=mediums[0])
            for medium in mediums[1:]:
                if medium[0] == '-':
                    tmp = tmp.exclude(medium__icontains=medium[1:])
                else:
                    tmp = cltrlrlcs.filter(medium__icontains=medium) | tmp
            cltrlrlcs = tmp

        if 'search' in choices:
            cltrlrlcs = cltrlrlcs.filter(object_name__icontains=choices['search'])

        cltrlrlcs = cltrlrlcs.annotate(
            like_times=Count('cltrrlcs_stars'), 
            comment_times=Count('cltrrlcs_comments')
        ).order_by(
            '-like_times', 
            '-comment_times'
        )
        
        paginator = Paginator(cltrlrlcs, limit)
        objects = paginator.get_page(page)
        datas = [object.brief_json(1) for object in objects]
        new_datas = {}
        new_datas['data'] = datas
        new_datas['count'] = paginator.count
        new_datas['page_num'] = paginator.num_pages
        
        return JsonResponse(new_datas, safe=False)

    def post(self, request: HttpRequest) :
        # TODO 图片上传, 根据图片进行搜索
        pass

@method_decorator(csrf_exempt, name='dispatch')
class ObjectView(View):
    def get(self, request: HttpRequest, id):
        try:
            object = CulturalRelicsData.objects.get(id=id)
            data = object.json()
            return JsonResponse(data)
        except CulturalRelicsData.DoesNotExist:
            return HttpResponse('Not Found', status=404)


@method_decorator(csrf_exempt, name='dispatch')
class DynamicsView(View):

    def get_dynamics_page_datas(self, dynamics, limit, page):
        dynamics = dynamics.annotate(
            like_times = Count('dynamic_stars'), 
            comment_times = Count('dynamic_comments')
        ).order_by(
            '-like_times', 
            '-comment_times',
        )
        paginator = Paginator(dynamics, limit)
        page_dynamics = paginator.get_page(page)
        datas = [dynamic.json() for dynamic in page_dynamics]
        new_datas = {}
        new_datas['data'] = datas
        new_datas['count'] = paginator.count
        new_datas['page_num'] = paginator.num_pages
        return new_datas

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            limit = request.GET.get('limit')
            page = request.GET.get('page')
            type = request.GET
            if 'objectid' in type:
                dynamics = Dynamic.objects.filter(cltrlrlcs__id=type['objectid'])
                datas = self.get_dynamics_page_datas(dynamics, limit, page)
                return JsonResponse(datas, safe=False)

            if 'username' in type:
                user = User.objects.get(username=type['username'])
                dynamics = Dynamic.objects.filter(user=user)
                datas = self.get_dynamics_page_datas(dynamics, limit, page)
                return JsonResponse(datas, safe=False)

            dynamics = Dynamic.objects.all().order_by('-time')
            paginator = Paginator(dynamics, limit)
            page_dynamics = paginator.get_page(page)
            datas = [dynamic.json() for dynamic in page_dynamics]
            new_datas = {'data' : datas, 'count' : paginator.count, 'page_num' : paginator.num_pages}
            return JsonResponse(new_datas, safe=False)

        return HttpResponse('Login Required', status=403)

    def write_files(self, files, id):
        urls = ''
        for file in files:
            filename = str(id) + file.name
            with open('%s' % os.path.join('media/dynamic_files/', filename), 'wb') as f:
                for i in file.chunks():
                    f.write(i)
                f.close()
                urls += filename + ","
        return urls

    def post(self, request: HttpRequest):
        
        if request.user.is_authenticated:
            data = json.loads(request.POST.get('data'))
            user = User.objects.get(username=data['user'])
            object = None
            if data['objectid'] is not None:
                try:
                    object = CulturalRelicsData.objects.get(id=data['objectid'])
                except CulturalRelicsData.DoesNotExist:
                    pass
            text = data['text']
            dynamic = Dynamic.objects.create(
                user = user,
                cltrlrlcs = object,
                text = text,
            )
            # 图片音视频文件上传
            files_keys = request.FILES
            urls = ''
            if "images" in files_keys:
                images = request.FILES.getlist("images")
                image_urls = self.write_files(images, dynamic.id)
                urls += image_urls
            if "vedios" in files_keys:
                vedios = request.FILES.getlist("vedios")
                vedio_urls = self.write_files(vedios, dynamic.id)
                urls += vedio_urls
            if "audios" in files_keys:
                audios = request.FILES.getlist("audios")
                audio_urls = self.write_files(audios, dynamic.id)
                urls += audio_urls
            dynamic.files_urls = urls
            dynamic.save()
            data = dynamic.json()
            return JsonResponse(data)

        return HttpResponse('Login Required', status=403)

@method_decorator(csrf_exempt, name='dispatch')
class DynamicView(View):
    def get(self, request:HttpRequest, id):
        if request.user.is_authenticated:
            try:
                dynamic = Dynamic.objects.get(id=id)
            except Dynamic.DoesNotExist:
                return HttpResponse('Not Found', status=404)

            return JsonResponse(dynamic.json())

        return HttpResponse('Login Required', status=403)
    

    def delete(self, request:HttpRequest, id):
        if request.user.is_authenticated:
            try:
                dynamic = Dynamic.objects.get(id=id)
            except Dynamic.DoesNotExist:
                return HttpResponse('Not Found', status=404)
            dynamic.delete()
            return HttpResponse('success')
            
        return HttpResponse('Login Required', status=403)
        

@method_decorator(csrf_exempt, name='dispatch')
class CommentsView(View):

    def get_comment_page_datas(self, comments, limit, page):
        paginator = Paginator(comments, limit)
        page_comments = paginator.get_page(page)
        datas = [comment.json() for comment in page_comments]
        new_datas =  {'data':datas, 'count':paginator.count, 'page_num':paginator.num_pages}
        return new_datas

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            limit = request.GET.get('limit')
            page = request.GET.get('page')

            type = request.GET

            if 'objectid' in type:
                try:
                    object = CulturalRelicsData.objects.get(id=type['objectid'])
                except CulturalRelicsData.DoesNotExist:
                    return HttpResponse('Not Found', status=404)
                comments = object.cltrrlcs_comments.all()
                comments = comments.filter(comment=None)
                comments = comments.annotate(
                    like_times = Count('comment_stars')
                ).order_by(
                    '-like_times'
                )
                datas = self.get_comment_page_datas(comments, limit, page)
                return JsonResponse(datas, safe=False)

            if 'dynamicid' in type:
                try:
                    dynamic = Dynamic.objects.get(id=type['dynamicid'])
                except Dynamic.DoesNotExist:
                    return HttpResponse('Not Found', status=404)
                comments = dynamic.dynamic_comments.all()
                comments = comments.filter(comment=None)
                comments = comments.annotate(
                    like_times = Count('comment_stars')
                ).order_by(
                    '-like_times'
                )
                datas = self.get_comment_page_datas(comments, limit, page)
                return JsonResponse(datas, safe=False)

            if 'commentid' in type:
                try:
                    comment = Comment.objects.get(id=type['commentid'])
                except Comment.DoesNotExist:
                    return HttpResponse('Not Found', status=404)
                comments = comment.comment_comments.all()
                tmp_comments = comments.all()
                while len(tmp_comments) != 0:
                    s_comments = tmp_comments[0].comment_comments.all()
                    for comment in tmp_comments[1:]:
                        s_comments = s_comments | comment.comment_comments.all()
                    comments = comments | s_comments
                    tmp_comments = s_comments
                comments = comments.all().order_by('-time')
                datas = self.get_comment_page_datas(comments, limit, page)
                return JsonResponse(datas, safe=False)

            comments = Comment.objects.filter(comment=None).order_by('-time')
            datas = self.get_comment_page_datas(comments, limit, page)
            return JsonResponse(datas, safe=False)
            # TODO获取个人所有评论

        return HttpResponse('Login Required', status=403)

    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            data = json.loads(request.POST.get('data'))
            user = User.objects.get(username=data['user'])
            if data['objectid'] is None:
                object = None
            else:
                object = CulturalRelicsData.objects.get(id=data['objectid'])
            if 'dynamicid' in data:
                if data['dynamicid'] is None:
                    dynamic = None
                else:
                    dynamic = Dynamic.objects.get(id=data['dynamicid'])
            else:
                dynamic = None
            if 'commentid' in data:
                if data['commentid'] is None:
                    comment = None
                    reply_user = None
                else:
                    comment = Comment.objects.get(id=data['commentid'])
                    reply_user = User.objects.get(username=comment.user)
            else:
                comment = None
                reply_user = None

            comment = Comment.objects.create(
                cltrrlcs = object,
                dynamic = dynamic,
                comment = comment,
                user = user,
                reply_user = reply_user,
                text = data['text'],
            )
            if 'image' in request.FILES:
                image = request.FILES.get('image')
                filename = str(comment.id) + image.name
                url = ''
                with open('%s' % os.path.join('media/comment_pics/', filename), 'wb') as f:
                    for i in image.chunks():
                        f.write(i)
                    f.close()
                    url += filename
                comment.images = url
                comment.save()
            data = comment.json()
            return JsonResponse(data)

        return HttpResponse('Login Required', status=403)

@method_decorator(csrf_exempt, name='dispatch')
class CommentView(View):
    def get(self, request: HttpRequest, id):
        if request.user.is_authenticated:
            try:
                comment = Comment.objects.get(id=id)
            except :
                return HttpResponse('Not Found', status=404)
            return JsonResponse(comment.json())

        return HttpResponse('Login Required', status=403)

    def delete(self, request: HttpRequest, id):
        if request.user.is_authenticated:
            try:
                comment = Comment.objects.get(id=id)
                comment.delete()
            except :
                return HttpResponse('Not Found', status=404)

            return HttpResponse('success')

        return HttpResponse('Login Required', status=403)


@method_decorator(csrf_exempt, name='dispatch')
class StarsView(View):
    def get(self, request:HttpRequest):
        if request.user.is_authenticated:
            limit = request.GET.get('limit')
            page = request.GET.get('page')
            querydata = request.GET
            stars = Star.objects.all()

            if 'username' in querydata:
                stars = stars.filter(user=request.user)
            if 'objectid' in querydata:
                object = CulturalRelicsData.objects.get(id=querydata['objectid'])
                stars = stars.filter(cltrrlcs=object)
            if 'dynamicid' in querydata:
                dynamic = Dynamic.objects.get(id=querydata['dynamicid'])
                stars = stars.filter(dynamic=dynamic)
            if 'commentid' in querydata:
                comment = Comment.objects.get(id=querydata['commentid'])
                stars = stars.filter(comment=comment)

            if 'type' in querydata:
                if querydata['type'] == 'object':
                    stars = stars.filter(dynamic=None).filter(comment=None)
                elif querydata['type'] == 'dynamic':
                    stars = stars.filter(cltrrlcs=None).filter(comment=None)
                elif querydata['type'] == 'comment':
                    stars = stars.filter(cltrrlcs=None).filter(dynamic=None)

            stars = stars.all().order_by('-time')
            paginator = Paginator(stars, limit)
            page_stars = paginator.get_page(page)
            datas = [star.json() for star in page_stars]
            new_datas =  {'data':datas, 'count':paginator.count, 'page_num':paginator.num_pages}
            return JsonResponse(new_datas, safe=False)
        return HttpResponse('Login Required', status=403)

    def post(self, request:HttpRequest):
        if request.user.is_authenticated:
            data = json.loads(request.body)
            user = User.objects.get(username=data['username'])
            if 'objectid' in data:
                object = CulturalRelicsData.objects.get(id=data['objectid'])
                star = Star.objects.create(
                    user = user,
                    cltrrlcs = object
                )
            elif 'dynamicid' in data:
                dynamic = Dynamic.objects.get(id=data['dynamicid'])
                star = Star.objects.create(
                    user = user,
                    dynamic = dynamic
                )
            elif 'commentid' in data:
                comment = Comment.objects.get(id=data['commentid'])
                star = Star.objects.create(
                    user = user,
                    comment = comment
                )
            data = {'starid':star.id}
            return JsonResponse(data)

        return HttpResponse('Login Required', status=403)

@method_decorator(csrf_exempt, name='dispatch')
class StarView(View):

    def get(self, request:HttpRequest, id):
        if request.user.is_authenticated:
            try:
                star = Star.objects.get(id=id)
            except Star.DoesNotExist:
                return HttpResponse('Not Found', status=404)
            return JsonResponse(star.json())
        return HttpResponse('Login Required', status=403)

    def delete(self, request:HttpRequest, id):
        if request.user.is_authenticated:
            try:
                star = Star.objects.get(id=id)
            except Star.DoesNotExist:
                return HttpResponse('Not Found', status=404)
            star.delete()
            return HttpResponse('success')
        return HttpResponse('Login Required', status=403)

