from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.serializers import serialize
from pprint import pprint
from django.core.mail import send_mail
from django.shortcuts import render
from .models import Product
from django.http import HttpResponse
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder


def index(request):
    products = Product.objects.all()
    if request.method == "POST":
        productid = request.POST.get("product_id")

        product = Product.objects.get(id=productid)

        if request.POST.get("submit") == "btnfavori":
            if Product.objects.filter(user=request.user).exists():
                product.favori.remove(request.user)
                product.save()
            else:
                product.favori.add(request.user)
                product.save()



    context={
        "products":products,
    }
    return render(request, "index.html", context)

@csrf_exempt
def favori(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = Product.objects.get(id=product_id)
        if Product.objects.filter(id=product_id,favori=request.user).exists():
            product.favori.remove(request.user)
            product.save()
            return JsonResponse({"favori_product":False})
        else:
            product.favori.add(request.user)
            product.save()
            return JsonResponse({"favori_product":True})

        
    
def category(request):
    products = Product.objects.all()
    filters = Q()

    """if "durum" in request.GET:
        if request.GET.get("durum") == "Sale":
            filters &= Q(durum="Sale")
        elif request.GET.get("durum") == "Rent":
            return HttpResponse("Yükseklik korkunuz var mı? (Evet/Hayır)")

    if "Yükseklik_korkusu" in request.GET:
        if request.GET.get("Yükseklik_korkusu") == "Evet":
            return HttpResponse("Kaç kişi yaşıyorsunuz?")
        elif request.GET.get("Yükseklik_korkusu") == "Hayır":
            return HttpResponse("Kaç kişi yaşıyorsunuz ve evcil hayvanınız var mı? (Evet/Hayır)")

    if "person" in request.GET:
        person = request.GET.get("person")
        if person == "1-2":
            filters &= Q(room_number__in=["1+1", "2+1"])
        elif person == "3-4":
            filters &= Q(room_number__in=["3+1", "4+1", "5+1"])
        else:
            filters &= Q(room_number__in=["5+1", "6+1", "7+1"])

    if "car" in request.GET:
        if request.GET.get("car") == "True":
            filters &= Q(otopark=True)
        else:
            filters &= Q(otopark=False)

    if "securty" in request.GET:
        if request.GET.get("securty") == "True":
            filters &= Q(güvenlik=True)
        else:
            filters &= Q(güvenlik=False)

    if "havuz" in request.GET:
        if request.GET.get("havuz") == "True":
            filters &= Q(havuz=True)
        else:
            filters &= Q(havuz=False)

    filtered_products = products.filter(filters)
    # Burada filtered_products kullanılarak uygun cevap veya sonuçları oluşturabilirsiniz.

  # Ana kural: Yükseklik korkusu ve hayvan durumu kontrolü
    if request.GET.get("Yükseklik_korkusu") == "True":
        filters &= Q(brand="Detached")
    elif request.GET.get("Yükseklik_korkusu") == "False" and request.GET.get("animal") == "True":
        filters &= Q(brand="Detached")"""
    # Eğer yükseklik korkusu yok ve hayvan durumu belirtilmemişse veya hayvan yoksa herhangi bir şey eklemiyoruz



    if "Yükseklik_korkusu" in request.GET and request.GET.get ("Yükseklik_korkusu") != "":
        if request.GET.get("Yükseklik_korkusu") == "True":
            filters &= Q(brand="Detached")
        else:
            filters &= Q(brand="Building")
            filters |= Q(brand="Detached")


# search kısımı


    query = ""
    if "query" in request.GET and request.GET.get("query") != "":
        query = request.GET.get("query")
        products = Product.objects.filter(Q(title__icontains=query) |
                                          Q(description__icontains=query) )
        print(query)


    # Diğer filtreler
    if "city" in request.GET and request.GET.get ("city") != "":
        if request.GET.get("city") == "istanbul":
            filters &= Q(location="istanbul")
        else:
            filters &= Q(location="ankara")

    if "animal" in request.GET and request.GET.get ("animal") != "":
        if request.GET.get("animal") == "True":
            filters &= Q(brand="Detached")
        else:
            filters &= Q(brand="Building")


    if "durum" in request.GET and request.GET.get("durum") != "":
        if request.GET.get("durum") == "Sale":
            filters &= Q(durum="Sale")
        elif request.GET.get("durum") == "Rent":
            filters &= Q(durum="Rent")

    if "communication" in request.GET and request.GET.get("communication") != "":
        if request.GET.get("communication") == "True":
            filters &= Q(communication=True)
        else:
            filters &= Q(communication=False)

    if "person" in request.GET and request.GET.get("person") != "":
        person = request.GET.get("person")
        if person == "1-2":
            filters &= Q(room_number__in=["1+1", "2+1"])
        elif person == "3-4":
            filters &= Q(room_number__in=["3+1", "4+1"])
        else:
            filters &= Q(room_number__in=["5+1", "6+1", "7+1"])

    if "car" in request.GET and request.GET.get("car") != "":
        if request.GET.get("car") == "True":
            filters &= Q(otopark=True)
        else:
            filters &= Q(otopark=False)

    if "securty" in request.GET and request.GET.get("securty") != "":
        if request.GET.get("securty") == "True":
            filters &= Q(güvenlik=True)
        else:
            filters &= Q(güvenlik=False)

    if "havuz" in request.GET and request.GET.get("havuz") != "":
        if request.GET.get("havuz") == "True":
            filters &= Q(havuz=True)
        else:
            filters &= Q(havuz=False)


    filtered_products = products.filter(filters)

        

    """if "durum" in request.GET:
        filters &= Q(durum=request.GET.get("durum"))

    if "room_number" in request.GET:
        filters &= Q(room_number=request.GET.get("room_number"))

    if "kat_sayısı" in request.GET:
        filters &= Q(kat_sayısı=request.GET.get("kat_sayısı"))

    if "asansor" in request.GET:
        filters &= Q(asansor=request.GET.get("asansor"))

    if "güvenlik" in request.GET:
        filters &= Q(güvenlik=request.GET.get("güvenlik"))

    if "otopark" in request.GET:
        filters &= Q(otopark=request.GET.get("otopark"))"""

    products = Product.objects.filter(filters)
    for product in products:
        print(product.location)

    print(filters)
    if request.method == "POST":
        productid = request.POST.get("product_id")

        product = Product.objects.get(id=productid)

        if request.POST.get("submit") == "btnfavori":
            if Product.objects.filter(user=request.user).exists():
                product.favori.remove(request.user)
                product.save()
            else:
                product.favori.add(request.user)
                product.save()

    paginator = Paginator(products,6)
    page_number = request.GET.get("page")#sayfada kaç ürün olacağını belirliyoruz
    products = paginator.get_page(page_number)


    context = {
        "products":products,
        "query":query,


    }

    return render(request, "category.html",context)


def textfilter(request):
    return render(request, 'textfilter.html')



def idea(request):
    def get_data():
        data = {
            'yükseklik korkusu': ['evet', 'no', 'no', 'evet', 'evet','evet'],
            'kişi': [4, 6, 3, 2, 4, 6],
            'araba': ['yes', 'yes', 'no', 'yes', 'yes','yes'],
            'yüzme':['yes','no','yes','no','no','yes'],
            'output': ['1st floor, 4+1, with parking, with pool', '3rd floor, 5+1, with parking, without pool', '6th floor, 3+1, without parking, with pool', '1st floor, 3+1, with parking, without pool', '1st floor, 4+1, with parking, without pool', '2nd floor, 5+1, with parking, with pool']
        }

        le = LabelEncoder()
        data['yükseklik korkusu'] = le.fit_transform(data['yükseklik korkusu'])
        data['yükseklik korkusu'] = 1 - data['yükseklik korkusu']
        data['araba'] = le.fit_transform(data['araba'])
        data['araba'] = 1 - data['araba']

        X = list(zip(data['yükseklik korkusu'], data['kişi'], data['araba']))
        y = data['output']

        le_y = LabelEncoder()
        y = le_y.fit_transform(y)

        model = DecisionTreeClassifier()
        model.fit(X, y)

        return model, le_y

    def idea_output(model, le_y, yukseklik, kisi, araba):
        input_data = [[yukseklik, kisi, araba]]
        prediction = model.predict(input_data)
        predicted_output = le_y.inverse_transform(prediction)
        return predicted_output[0]

    if request.method == 'POST':
        height = int(request.POST['yukseklik'])
        person = int(request.POST['kisi'])
        car = int(request.POST['araba'])
        model, le_y = get_data()
        predicted_output = idea_output(model, le_y, height, person, car)
        return HttpResponse(predicted_output)
    else:
        return render(request, 'idea.html')






def chatbot(request):
    return render(request, 'chatbot.html')



@login_required(login_url='/login/')
def profil(request):
    user = User.objects.get(username=request.user)
    profil = Profil.objects.get(user=request.user)
    adress = Adress.objects.get(user=request.user)
    evlerim = Product.objects.filter(user=user)



    if request.method == "POST":
        if request.POST.get("btnsubmit") == "btnpass":
            oldpass = request.POST.get("oldpass")
            newpass = request.POST.get("newpass")
            rnewpass = request.POST.get("rnewpass")

            print(oldpass)
            print(newpass)

            if newpass == rnewpass:
                print("Buırada")
                if user.check_password(oldpass):
                    print("Burar2")
                    user.set_password(newpass)
                    user.save()
                    logout(request)
                    return redirect("login")
                else:
                    messages.error(request, "Eski Şifreniz Yanlış! Tekrar Deneyiniz")
            else:
                messages.error(request, "Şifreler Uyumsuz! Tekrar Deneyiniz")

        elif request.POST.get("btnsubmit") == "btnprofil":
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            phone_number = request.POST.get("phone_number")
            birtdate = request.POST.get("birtdate")

            if user.email != email:
                if not User.objects.filter(email=email).exists():
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    profil.phone_number = phone_number
                    profil.birtdate = birtdate
                    user.save()
                    profil.save()
                    return redirect("profil")
                else:
                    messages.error(request, "Bu E-Posta Adresi Başka Bir Kullanıcı Tarafından Kullanılıyor.")
            else:
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                profil.phone_number = phone_number
                profil.birtdate = birtdate
                user.save()
                profil.save()
                return redirect("profil")
        elif request.POST.get("btnsubmit") == "btnadress":
            adres = request.POST.get("adress")
            province = request.POST.get("province")
            district = request.POST.get("district")
            neighbourhood = request.POST.get("neighbourhood")

            adress.adress = adres
            adress.province = province
            adress.district = district
            adress.neighbourhood = neighbourhood

            adress.save()
            return redirect("profil")
        elif request.POST.get("productedit") == "editproduct":
            title = request.POST.get("title")
            print(title)
            genel_durum = request.POST.get("genel_durum")
            print(genel_durum)
            durum = request.POST.get("durum")
            print(durum)
            city = request.POST.get("location")
            print(city)
            konumm = request.POST.get("konumm")
            print(konumm)
            açıklama = request.POST.get("açıklaması")
            print(açıklama)
            ücret = request.POST.get("price")
            print(ücret)
            room_number = request.POST.get("room_number")
            print(room_number)
            kat_number = request.POST.get("kat_number")
            print(kat_number)
            metre = request.POST.get("metre")
            print(metre)
            asansör = request.POST.get("asansör")
            print(asansör)
            güvenlik = request.POST.get("güvenlik")
            print(güvenlik)
            otopark = request.POST.get("otopark")
            print(otopark)
            havuz = request.POST.get("havuz")
            print(havuz)
            ürünid = request.POST.get("ürünid")
            

            fotoğraf = request.FILES.getlist("fotoğraf")
            print(fotoğraf)

            ürün = Product.objects.get( id = ürünid )
            ürün.title = title
            ürün.brand = genel_durum 
            ürün.location = city
            ürün.adres = konumm
            ürün.description = açıklama
            ürün.price = ücret
            ürün.room_number = room_number
            ürün.kat_sayısı = kat_number
            ürün.metre = metre
            ürün.asansor = asansör
            ürün.güvenlik = güvenlik
            ürün.otopark = otopark
            


            for img in fotoğraf:
                new_image = ProductImage.objects.create(product=ürün, image=img)
                new_image.save()
            ürün.save()
            return redirect("profil")

        
        elif request.POST.get("productsave") == "saveproduct":
            title = request.POST.get("title")
            print(title)
            genel_durum = request.POST.get("genel_durum")
            print(genel_durum)
            durum = request.POST.get("durum")
            print(durum)
            city = request.POST.get("location")
            print(city)
            konumm = request.POST.get("konumm")
            print(konumm)
            açıklama = request.POST.get("açıklaması")
            print(açıklama)
            ücret = request.POST.get("price")
            print(ücret)
            room_number = request.POST.get("room_number")
            print(room_number)
            kat_number = request.POST.get("kat_number")
            print(kat_number)
            metre = request.POST.get("metre")
            print(metre)
            asansör = request.POST.get("asansör")
            print(asansör)
            güvenlik = request.POST.get("güvenlik")
            print(güvenlik)
            otopark = request.POST.get("otopark")
            print(otopark)
            havuz = request.POST.get("havuz")
            print(havuz)
            fotoğraf = request.FILES.getlist("fotoğraf")
            print(fotoğraf)
            new_home = Product.objects.create(user=request.user,  title=title, brand=genel_durum, durum=durum, adres=konumm, location=city, description=açıklama , price=ücret, room_number=room_number, kat_sayısı=kat_number,
                                            metre= metre, asansor=asansör,  güvenlik=güvenlik, otopark=otopark, havuz=havuz, image=fotoğraf[0])
            for img in fotoğraf:
                new_image = ProductImage.objects.create(product=new_home, image=img)
                new_image.save()
            new_home.save()
            return redirect("profil")
        elif request.POST.get("btndelete") =="delete":
            product_id = request.POST.get("delete")
            product = Product.objects.get( id = product_id )
#eşitliğin sol tarafı modelden geliyo = sağ taraf  bizim verdiğimiz değer.
            product.delete()
            return redirect("profil")

    

    context={
        "profil":profil,
        "adress":adress,
        "evlerim":evlerim,
    }
    return render(request, "user/profil.html",context)



def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    print(product.brand)
    product_images = ProductImage.objects.filter(product=product)
    comments = Comment.objects.filter(product=product) #yorumları çekiyoruz
    comment_user = None
    profil = Profil.objects.get(user = product.user )
    print("profil",profil)

    
    for comment in comments:
        if comment.user == request.user:
            comment_user = comment.user

    if request.method == "POST":
        if request.POST.get("submit") == "btncomment":
            comment = request.POST.get("comment")

            new_comment = Comment.objects.create(user=request.user,first_name=request.user.first_name,last_name=request.user.last_name, product=product,comment=comment)
            new_comment.save()
            return redirect(f"/product-detail/{product_id}")
        
        elif request.POST.get("submit") == "commentupdate":
            comment_id = request.POST.get("comment_id")
            comment = request.POST.get("comment")

            update_comment = Comment.objects.get(id=comment_id)
            update_comment.comment = comment
            update_comment.save()
            return redirect(f"/product-detail/{product_id}")   
        
        elif request.POST.get("submit") == "btnfavori":
            productID = request.POST.get("product_id")
            product = Product.objects.get(id=productID)
            # if Favorite.objects.filter(product=product).exists():
            #     favori = Favorite.objects.get(product=product)
            #     favori.delete()
            #     return redirect(f"/product-detail/{productID}")
            # else:
            #     favori = Favorite.objects.create(user=request.user, product=product)
            #     favori.save()
            #     return redirect(f"/product-detail/{productID}")
        
        elif request.POST.get("submit") == "commentupdate":
            comment_id = request.POST.get("comment_id")
            comment = request.POST.get("comment")

            update_comment = Comment.objects.get(id=comment_id)
            update_comment.comment = comment
            update_comment.save()
            return redirect(f"/product-detail/{product_id}")

    print(comment_user)

    context= {
        "product":product,
        "comments":comments,
        "comment_user":comment_user,
        "product_images":product_images,
        "profil":profil,
    }
    return render(request, "product_detail.html",context)

def favorite(request):

    favorites = Product.objects.filter(favori = request.user)
    print(favorites)

    context={
         "favorites":favorites
     }

    return render(request, "favorite.html",context)


def Login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                return redirect("index")
            else:
                messages.error(request, "Your password is incorrect, please try again.")
        else:
            if email.endswith('@gmail.com'):
                messages.error(request, "Your Gmail Address is Not Registered or you entered it incorrectly.")
            else:
                messages.error(request, "Your e-mail address is incorrect, please try again.")


    return render(request, "user/login.html")

def Register(request):

    if request.method == "POST":
        first_name = request.POST.get("name")
        last_name = request.POST.get("surname")
        email = request.POST.get("email")
        phone_number =request.POST.get("tel")
        password = request.POST.get("password")
        harfup = False
        harfnum = False

        for harf in password:
            if harf.isupper():
                harfup=True
            if harf.isnumeric():
                harfnum = True
        print(password)
        if harfnum:
            if harfup :
                if len(password) > 5 :

                    if not User.objects.filter(email=email).exists():
                        user = User.objects.create_user(username=email, first_name=first_name,last_name=last_name,email=email, password=password)

                        user.save()
                        profil = Profil.objects.get(user=user)
                        profil.phone_number = phone_number
                        profil.save()
                        login(request,user)
                        return redirect("index")
                    else:
                        messages.error(request, "This Email address is used by another user.")
                else:
                    messages.error(request, "Your password must have more than 5 digits.")
            else:
                messages.error(request, "Your password must contain capital letters. ")
        else:
            messages.error(request, "Your password must contain numbers. ")


    return render(request, "user/register.html")

def Logout(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'index'))

def set_language(request, language):
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        except Resolver404:
            view = None
        if view:
            break
    if view:
        translation.activate(language)
        next_url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        response = HttpResponseRedirect("/")
    return response



def forsale(request):
    products = Product.objects.filter(durum="Sale")
    context = {
        'products': products,
    }
    return render(request, 'user/forsale.html', context)

def forrent(request):
    products = Product.objects.filter(durum="Rent")
    context = {
        'products': products,
    }
    return render(request, 'user/forrent.html', context)

def sendMail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name =  request.POST.get('name')      
        text = request.POST.get('message')
        subject = 'şikayet istek öneri'
        message = "Name-Surname :  "+  name + "\n" + "Email :  " + email + "\n" + text  + " "
        email_from = email
        recipient_list = ["kardelen062852@gmail.com"]
        send_mail( subject, message, email_from, recipient_list )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'index'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'index'))
    

