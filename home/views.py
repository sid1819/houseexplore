from django.shortcuts import render,HttpResponse,redirect
from .models import *
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
import json
import random
from django.db.models import Q

# Create your views here.
def index(request):
    user = request.user
    if user.is_authenticated:
        cards = House.objects.exclude(seller = user)
    else:
        cards = House.objects.all()
    return render(request,"index.html",{'cards':cards,'locshow':False})


def search(request):
    target=request.GET['searchCity']
    cid=[]
    city_searched = City.objects.filter(city_name__icontains = target)
    for item in city_searched:
        cid.append(item.city_id)
    
    cards = House.objects.filter(city__in=cid)
    locs = Location.objects.filter(city_id__in = cid)
    return render(request,"index.html",{'cards':cards,'locs':locs,'locshow':True})

def signup(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if pass1 == pass2:
            
            if User.objects.filter(username=username).exists():
                messages.info(request,"This username already exists.")
                return redirect("signup")
            elif User.objects.filter(email=email).exists():
                messages.info(request,"This email is already in use.")
                return redirect("signup")
            else:
                # old code
                user = User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=pass1)
                user.save()
                return redirect("login")
        else:
            messages.info(request,"Passwords are not matching.")
            return redirect("signup")
    else:
        return render(request,"signup.html")

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = auth.authenticate(username=username,password=pass1)
        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            messages.info(request,"Invalid Credentials")
            return redirect("login")

    else:
        return render(request,"login.html")

def logout(request):
    auth.logout(request)
    return redirect("/")


def search2(request):
    if request.GET['locSearch'] == "Select the location":
        searchLoc = Location.objects.all()
        return redirect("/")
    searchLoc = Location.objects.get(loc_name = request.GET['locSearch'])
    city = City.objects.get(city_id = searchLoc.city_id.city_id)
    searchLocCards = House.objects.filter(location = searchLoc.loc_id)
    locs = Location.objects.filter(city_id = city.city_id)
    return render(request,"search2.html",{'searchLocCards':searchLocCards,'locs':locs})


def dealerinfo(request):
    selectedDealer = Dealer.objects.get(house_id = request.GET['houseid'])
    return render(request,"dealer.html",{'selectedDealer':selectedDealer})

def aboutus(request):
    return render(request,"aboutus.html")


def contactus(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lnam']
        phone = request.POST['phone']
        email = request.POST['email']
        msg = request.POST['message']
        customercontacted = Customercontacted(first_name = fname,last_name = lname,phone_number = phone,email = email,msg = msg)
        customercontacted.save()
        return redirect("/")
    return render(request,"contactus.html")


@login_required
def addhouse(request):
    if request.method == "POST":
        print(request.POST)
        houseName = request.POST['houseName']
        price = request.POST['inputPrice']
        cityName = request.POST['inputCity']
        state = request.POST['state']
        locationName = request.POST['inputLocation']
        address = request.POST['inputAddress']
        area = request.POST['inputArea']
        bhk = request.POST['inputBedrooms']
        description = request.POST['description']
        img1 = request.FILES['inputGroupFile01']
        img2 = request.FILES['inputGroupFile02']
        img3 = request.FILES['inputGroupFile03']
        cctv = request.POST.get('cctv',False)
        children_play_area = request.POST.get('children_play_area',False)
        landscape = request.POST.get('landscape',False)
        garage = request.POST.get('garage',False)
        lifts = request.POST.get('lifts',False)
        cycling_jogging = request.POST.get('cycling_jogging',False)
        fire_fighting = request.POST.get('fire_fighting',False)
        power_backup = request.POST.get('power_backup',False)
        temple = request.POST.get('temple',False)
        city = City.objects.filter(city_name = cityName).first()
        location = Location.objects.filter(loc_name = locationName).first()
        houseId = random.randint(1000000000, 9999999999)
        user = request.user
        newHouse = House(
            house_id = houseId,
            seller = user,
            name=houseName,
            price=price,
            city=city,
            location=location,
            address=address,
            area=area,
            bhk=bhk,
            description = description,
            img1 = img1,
            img2 = img2,
            img3 = img3,
            cctv = cctv,
            children_play_area = children_play_area,
            landscape = landscape,
            garage = garage,
            lifts = lifts,
            cycling_jogging = cycling_jogging,
            fire_fighting = fire_fighting,
            temple = temple,
            power_backup = power_backup,
            sold = False
        )
        newHouse.save()
        newDealer = Dealer(
            dealer_id = user.id,
            dealer_name = user.first_name+user.last_name,
            house_id = newHouse,
            email_id = user.email
        )
        newDealer.save()
        return redirect("myhouses")
    else:
        return render(request,"addhouse.html")



def myhouses(request):
    user = request.user
    houses = House.objects.filter(seller = user)
    return render(request,'myhouses.html',{'houses':houses})

def remove_house(request, house_id):
    house = House.objects.filter(house_id = house_id)
    house.delete()
    messages.success(request, 'House removed successfully.')
    return redirect('myhouses')

@login_required
def chat(request, recipient_id):
    recipient = User.objects.get(id=recipient_id)
    messages = Message.objects.filter(
        sender=request.user,
        recipient=recipient
    ) | Message.objects.filter(
        sender=recipient,
        recipient=request.user
    ).order_by('timestamp')

    context = {
        'recipient': recipient,
        'messages': messages
    }
    return render(request, 'chatroom.html', context)

@login_required
def send_message(request, recipient_id):
    if request.method == 'POST':
        recipient = User.objects.get(id=recipient_id)
        content = request.POST.get('content')
        message = Message(sender=request.user, recipient=recipient, content=content)
        message.save()
    return redirect('chat', recipient_id=recipient_id)

@login_required
def chat_users(request):
    user = request.user
    messages = Message.objects.filter(Q(sender=user) | Q(recipient=user))
    users = set()
    for message in messages:
        if message.sender != user:
            users.add(message.sender)
        if message.recipient != user:
            users.add(message.recipient)
    return render(request, 'chat_users.html', {'users': users})

# @login_required
# def chat(request, user_id):
#     user = request.user
#     other_user = User.objects.filter(id=user_id)
#     messages = Message.objects.filter(
#         Q(sender=user, recipient=other_user) | Q(sender=other_user, recipient=user)
#     ).order_by('timestamp')
    
#     if request.method == 'POST':
#         content = request.POST.get('content')
#         if content:
#             Message.objects.create(sender=user, recipient=other_user, content=content)
#         return redirect('chat', user_id=other_user.id)

#     return render(request, 'chatroom.html', {'messages': messages, 'recipient': other_user})









# if (City.objects.filter(city_name = request.GET['searchCity']) is None):
#        return HttpResponse("hello this is searchpage")
#     else:

#         cid = City.objects.filter(city_name = request.GET['searchCity'])
#         searchCards = House.objects.filter(city_id = cid)
#         return render(request,"search.html",{'searchCards':searchCards})

#     # # 
#     # cid=City.objects.get(city_name='varanasi').city_id
#     # # 
#     # if cid is not None:
#     #     return render(request,"search.html",{'searchCards':searchCards})
#     # else:
#     #     return HttpResponse("hello this is searchpage")
