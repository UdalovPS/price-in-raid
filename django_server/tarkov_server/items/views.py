from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.views import View
import json_numpy
import json
from .json_parser.transcripter import Transcripter
from .models import Profile
from django.contrib.auth.models import User
from .forms import RegistrationForm, DropForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.core.mail import send_mail
from password_generator import PasswordGenerator
import cv2

from .ai_model.torch_model import SeachMarkAI
from .json_parser.parser import Parser

class MyLogoutView(LogoutView):
    next_page = '/'


class CheckView(View):
    def get(self, request):
        try:
            p = Parser()
            p.start()
            return HttpResponse("Items data was update")
        except Exception as _ex:
            return HttpResponse(f"{_ex}")


class Main(View):
    def get(self, request):
        lng = request.GET.get('lng')
        if lng == None:
            lng = 'rus'
        with open(f"./static_files/web_text.json", 'r') as json_data:
            text_dict = json.load(json_data)
        return render(
            request=request,
            template_name="items/main.html",
            context={'texts': text_dict[lng]}
        )


def download(request):
    path_to_file ="./staticfiles/dist.zip"
    zip_file = open(path_to_file, 'rb')
    response = FileResponse(zip_file, content_type='application/items')
    response['Content-Disposition'] = 'attachment; filename="%s"' % 'dist.zip'
    return response

def download_instruction(request):
    path_to_file ="./staticfiles/READMY.txt"
    file = open(path_to_file, 'rb')
    response = FileResponse(file, content_type='application/items')
    response['Content-Disposition'] = 'attachment; filename="%s"' % 'READMY.txt'
    return response


class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        lng = request.GET.get('lng')
        if lng == None:
            lng = 'rus'
        with open(f"./static_files/web_text.json", 'r') as json_data:
            text_dict = json.load(json_data)
        return render(
            request=request,
            template_name="items/registration.html",
            context={"form": form, 'texts': text_dict[lng]}
        )

    def post(self, request):
        lng = request.POST.get("language", "")
        with open(f"./static_files/web_text.json", 'r') as json_data:
            text_dict = json.load(json_data)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
            )
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(
                request=request,
                template_name="items/registration.html",
                context={"form": form, 'texts': text_dict[lng]}
            )


class LoginView(View):
    def get(self, request):
        lng = request.GET.get('lng')
        if lng == None:
            lng = 'rus'
        with open(f"./static_files/web_text.json", 'r') as json_data:
            text_dict = json.load(json_data)
        form = AuthenticationForm()
        return render(
            request,
            'items/login.html',
            context={"form": form, 'texts': text_dict[lng]}
        )

    def post(self, request):
        lng = request.POST.get("language", "")
        with open(f"./static_files/web_text.json", 'r') as json_data:
            text_dict = json.load(json_data)
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return render(
                    request,
                    'items/main.html',
                    context={'texts': text_dict[lng]}
                )
        else:
            return render(
                    request,
                    'items/login.html',
                    context={"form": form, 'texts': text_dict[lng]}
                )


def get_profile(request):
    lng = request.GET.get('lng')
    if lng == None:
        lng = 'rus'
    with open(f"./static_files/web_text.json", 'r') as json_data:
        text_dict = json.load(json_data)
    if request.user.is_authenticated:
        data = Profile.objects.get(user=request.user)
        data_dict = {
            'name': data.user.username,
            'email': data.user.email,
            'ip': data.ip,
            'use_date': data.use_date,
        }
        return render(
            request,
            'items/profile.html',
            context={'texts': text_dict[lng], 'data': data_dict}
        )
    else:
        return redirect(f"/login/?lng={lng}")


class ChangePasswordView(View):
    def get(self, request):
        form = PasswordChangeForm(request.user)
        lng = request.GET.get('lng')
        if lng == None:
            lng = 'rus'
        with open(f"./static_files/web_text.json", 'r') as json_data:
            text_dict = json.load(json_data)
        return render(
                    request,
                    'items/change_password.html',
                    context={'form': form, 'texts': text_dict[lng]}
                )

    def post(self, request):
        lng = request.POST.get("language", "")
        with open(f"./static_files/web_text.json", 'r') as json_data:
            text_dict = json.load(json_data)
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            login(request, request.user)
            return render(
                request,
                'items/message.html',
                context={'data': {'message': "password was changed"},
                         'texts': text_dict[lng]}
            )
        else:
            return render(
                request,
                'items/change_password.html',
                context={'form': form, 'texts': text_dict[lng]}
            )


class DropPasswordView(View):
    def get(self, request):
        lng = request.GET.get('lng')
        if lng == None:
            lng = 'rus'
        with open(f"./static_files/web_text.json", 'r') as json_data:
            text_dict = json.load(json_data)
        form = DropForm()
        return render(
                    request,
                    'items/drop_password.html',
                    context={'form': form, 'texts': text_dict[lng]}
                )

    def post(self, request):
        lng = request.POST.get("language", "")
        with open(f"./static_files/web_text.json", 'r') as json_data:
            text_dict = json.load(json_data)
        form = DropForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                obj = User.objects.get(email=email)
                print('FIND EMAIL')
                pwo = PasswordGenerator()
                pwo.excludeschars = "$%^()*-_/?.,;:+#<>=&"
                pwo.maxlen = 16
                pwo.minlen = 16
                new_password = pwo.generate()
                obj.set_password(new_password)
                obj.save()
                sender = 'priceinraid@mail.ru'
                send_mail('Drop password', f"Login: {obj.username}\nNew password: {new_password}",
                          sender, [email])
                return render(
                        request,
                        'items/main.html',
                        context={'texts': text_dict[lng]}
                    )
            except Exception as ex_:
                print(ex_)
                return render(
                    request,
                    'items/drop_password.html',
                    context={'form': form,
                             'texts': text_dict[lng],
                             'message': {'errors': 'profile no found'}}
                )


class ChechIpView(View):
    def get(self, request):
        token = request.GET.get('token')
        print(token)
        try:
            obj = Profile.objects.get(token=token)
            obj.verification = True
            obj.save()
            print(obj.user.username)
            print(obj.user.password)
            # user = authenticate(username=obj.user.username, password=obj.user.password)
            login(request, obj.user)
            return redirect("/profile/")
        except Exception as _ex:
            print(_ex)
            return HttpResponse('Token not working')

    def post(self, request):
        login = request.POST['login']
        password = request.POST['password']
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        user = authenticate(username=login, password=password)
        if user != None:
            obj = Profile.objects.get(user=user)
            if obj.ip != str(ip) or obj.verification == False:
                obj.ip = str(ip)
                pwo = PasswordGenerator()
                obj.verification = False
                pwo.excludeschars = "$%^()*-_/?.,;:+#<>=&"
                pwo.maxlen = 10
                pwo.minlen = 10
                token = pwo.generate()
                obj.token = token
                obj.save()
                # print("OBJ SAVE")
                sender = 'priceinraid@mail.ru'
                send_mail('Confirm IP', f"http://192.168.0.7:14141/ip/?token={token}",
                          sender, [obj.user.email])
                return HttpResponse('Need')
            return HttpResponse('Confirm')
        else:
            return HttpResponse('Not')


def get_item_data(request):
    if request.method == "POST":
        print("REQUEST in HERE")
        login = request.POST['login']
        password = request.POST['password']
        user = authenticate(username=login, password=password)
        if user != None:
            transcript_obj = Transcripter()                                                     #create object for transcripte text from image
            language = request.POST['lng']
            obj = SeachMarkAI(show_info_flag=True)                                              #create object for find mark with item name in image
            img = json_numpy.loads(request.POST['json'])                                        #load image from request
            img = cv2.resize(img, dsize=(1280, 1280), interpolation=cv2.INTER_CUBIC)            #resize image (model train in 1920x1920)
            crop_img = obj.seach_mark_in_screenshot(img)                                        #find mark with item
            if crop_img.size == 0:
                print('NOT FINDDDEDDD')
                data = {'traderName': 'not find', 'traderPrice': 'not find', 'pricePerSlot': 'not find', "canSellOnFlea": True}
            else:
                # Image.fromarray(crop_img).show()
                text = transcript_obj.transcript_text_from_image(crop_img, language=language)       #transcripte text in image
                print('TEXT: ', text)
                item_dict = transcript_obj.find_item_from_json_data(text, language=language)        #find data about item in database (json file)
                return HttpResponse(json.dumps(item_dict))
        else:
            data = {'traderName': 'error auth', 'traderPrice': 'error auth', 'pricePerSlot': 'error auth', "canSellOnFlea": True}
        return HttpResponse(json.dumps(data))


def change_language(request):
    language = request.GET.get('lng')
    print(language)
    language = 'rus'
    return HttpResponse(f"Your language is {language}")


class TestConnectView(View):
    def post(self, request):
        login = request.POST['login']
        password = request.POST['password']
        user = authenticate(username=login, password=password)
        if user != None:
            print("Is AUTHENFICATED")
            data = {'status': 'ok'}
        else:
            data = {'status': 'error auth'}
        return HttpResponse(json.dumps(data))



