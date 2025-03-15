from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage



from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404



from .models import *
from random import randint
from random import choice
from django.utils import timezone
from django.utils.timezone import localtime



def test(request):
    return render(request, "auctions/testform.html")


def forgotpasswordlandingpage(request):
    return render(request, "auctions/landingpage.html")


def forgotpassword(request):
    if request.method == "POST":
        if not request.POST.get('username') or request.POST.get('pin'):
            messages.error(request, 'Please fill in fields.')
        username = request.POST.get('username')
        pin = request.POST.get('pin')
        user = get_object_or_404(User, username=username, pin=pin)

        return render(request, "auctions/resetpassword.html", {
            "username": username
        })
    else:
        return render(request, "auctions/landingpage.html")

def resetpassword(request):
    if request.method == "POST":
        username = request.POST.get('username')
        user = User.objects.get(username=username)

        user.set_password(request.POST.get('password'))
        confirmation = request.POST.get('confirmation')
        if request.POST.get('password') != confirmation:
            messages.error(request, 'Passwords must match')
            return render(request, "auctions/resetpassword.html", {

                "username": username

            })
        user.save()
        messages.success(request, 'Password successfully changed!')
        login(request, user)
        return HttpResponseRedirect(reverse("homepage"))

    else:
        return render(request, "auctions/resetpassword.html")




def index(request):
    return render(request, "auctions/base.html")

def aboutus(request):
    return render(request, "auctions/ourteam.html")


def homepage(request):
    return render(request, "auctions/base.html")

@login_required(login_url='/login')
def togglemode(request):
    mode = Mode.objects.get(user=request.user.username)
    if mode.mode == "student":
        mode.mode = "teacher"
        mode.save()
    else:
        mode.mode = "student"
        mode.save()

    return HttpResponse("done")

@login_required(login_url='/login')
def newperson(request):
    details = User.objects.get(username=request.user.username)
    return render(request, "auctions/secondprofile.html", {
        "details": details
    })

@login_required(login_url='/login')
def choicepage(request):
    return render(request, "auctions/choicepage.html")

@login_required(login_url='/login')
def teacherdashboard(request):
    user = request.user.username
    jobs = Listing.objects.filter(user=user)
    present = False
    prodlst = []
    i = 0
    if jobs:
        present = True
        for job in jobs:
            prodlst.append(job)
    return render(request, "auctions/dashboard.html", {
        "product_list": prodlst,
        "present": present
    })

def toptutors(request):
    if request.method == "POST":
        subj = request.POST.get("subject").upper()
        #allratings = Rating.objects.filter(subject=subj)

        scores = [5, 4, 3, 2, 1]

        resultshash = {}

        allratings = []

        for score in scores:
            resultshash[score] = {
                "score": score,
                #"ratings": Rating.objects.filter(subject=subj, score=score),
                "teachers": returntutors(subj, score)
            }

        for x,y in resultshash.items():
            allratings.append(y)


        return render(request, "auctions/toptutors.html", {
            "allratings": allratings,
            "subj": subj
        })
    else:
        return render(request, "auctions/toptutors.html")


def returntutors(subj, score):
    allratings = Rating.objects.filter(subject=subj, score=score)
    teachers = []
	
    teachers_values = []

    for allrating in allratings:
        teachers.append(allrating.teacher_user)

    teachershash = {}


    for teacher in teachers:
	    teachershash[teacher] = {
	        "teacher": teacher,
	        "profile": returnurl(teacher)
	    }

    for x,y in teachershash.items():
        teachers_values.append(y)


    return teachers_values



def returnurl(user):
    obj = Profile.objects.get(user=user)
    return obj.url



@login_required(login_url='/login')
def secondprofile(request):
    if request.method == "POST":
        # item is of type Listing (object)
        item = Profile()
        # assigning the data submitted via form to the object
        item.user = request.user.username
        item.description = request.POST.get('description')
        item.level = request.POST.get('level').upper()
        item.qualifications = request.POST.get('qualifications')
        #item.url = request.POST.get('imageurl')

        #newmode = Mode()
        #newmode.user = request.user.username
        #newmode.mode = request.POST.get('mode')
        #newmode.save()

        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
        #extension = "." + myfile.name.split('.')[-1]
        #myfile.name = str(request.user.username) + extension
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            item.url = uploaded_file_url
            item.file = myfile
        # saving the data into the database
            item.save()

        except:
            item.url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBKRizGW6Md-BUD5MchQ_UWgYZVKwNQxoPzQte9r0fwSQzBV6h"
            item.file = None
            item.save()

        # retrieving the new products list after adding and displaying
        thing = User.objects.get(username=request.user.username)
        return redirect("homepage")

    # if request is get
    else:
        details = User.objects.get(username=request.user.username)
        return render(request, "auctions/secondprofile.html", {
            "details": details
        })

@login_required(login_url='/login')
def editprofile(request):
     if request.method == "POST":

        specific_class = Profile.objects.get(user=request.user.username)
        specific_class.user = request.user.username
        specific_class.description = request.POST.get("description")
        specific_class.level = request.POST.get("level").upper()
        specific_class.qualifications = request.POST.get("qualifications")
        #specific_class.url = request.POST.get("imageurl")

        newfile = request.FILES['newfile']
        fs = FileSystemStorage()
        #extension = "." + newfile.name.split('.')[-1]
        #newfile.name = str(request.user.username) + extension
        filename = fs.save(newfile.name, newfile)
        uploaded_file_url = fs.url(filename)
        specific_class.url = uploaded_file_url
        specific_class.save()


        return HttpResponseRedirect(reverse("yourprofile"))

     else:
        obj = Profile.objects.get(user=request.user.username)
        lst = WatchList.objects.filter(user=request.user.username)
    # list of products available in WinnerModel
        present = False
        prodlst = []
        i = 0
        if lst:
            present = True
            for item in lst:
                specific_class = Listing.objects.get(id=item.listingid)
                prodlst.append(specific_class)
        if obj:
            return render(request, "auctions/yourprofile.html", {
                "obj": obj,
                "product_list": prodlst,
                "present": present
            })


@login_required(login_url='/login')
def createjob(request):
    if request.method == "POST":
        obj = Listing()
        obj.user = request.user.username
        obj.teacher = request.POST.get('teacher')
        obj.subject = request.POST.get('subject').upper()
        obj.description = request.POST.get('description')
        obj.price = request.POST.get('price')
        obj.datetime = request.POST.get('datetime')

        if Profile.objects.get(user=request.user.username) is not None:
            obj.save()
        else:
            message.error(request, 'Create a profile first!')


        jobs = Listing.objects.filter(user=request.user.username)
        present = False
        prodlst = []
        i = 0
        if jobs:
            present = True
            for job in jobs:
                prodlst.append(job)

        return render(request, "auctions/dashboard.html", {
            "product_list": prodlst,
            "present": present
        })

    else:
        jobs = Listing.objects.filter(user=request.user.username)
        present = False
        prodlst = []
        i = 0
        if jobs:
            present = True
            for job in jobs:
                prodlst.append(job)

        return render(request, "auctions/dashboard.html", {
            "product_list": prodlst,
            "present": present
        })

@login_required(login_url='/login')
def giverating(request):
    if request.method == "POST":
        rating = Rating()
        rating.teacher_user = request.POST.get('user')
        rating.subject = request.POST.get('subject').upper()
        rating.score = request.POST.get('star')
        rating.feedback = request.POST.get('feedback')

        rating.save()

        newalert = Notifications()
        newalert.user = request.POST.get('user')
        newalert.info = str(request.user.username) + " " + "has given a rating."
        newalert.category = "Ratingmatters"
        newalert.read = False
        newalert.save()

        return redirect("rateteacher", user=request.POST.get('user'))
    else:
        pass




@login_required(login_url='/login')
def editclass(request, class_id):
    inquiries = Inquiry.objects.filter(listingid=class_id)
    students = Student.objects.filter(listingid=class_id)
    added = WatchList.objects.filter(
            listingid=class_id, user=request.user.username)

    if request.method == "POST":

        obj = Listing.objects.get(id=class_id)
        obj.user = request.user.username
        obj.teacher = request.POST.get('teacher')
        obj.subject = request.POST.get('subject').upper()
        obj.description = request.POST.get('description')
        obj.price = request.POST.get('price')
        obj.datetime = request.POST.get('datetime')

        obj.save()

        return redirect("viewclass", class_id=class_id)

        #return render(request, "auctions/viewclass.html", {
        #"class": obj,
        #"inquiries": inquiries,
        #"students": students,
        #"added": added
    #})

    else:
        obj = Listing.objects.get(id=class_id)
        return render(request, "auctions/viewclass.html", {
        "class": obj,
        "inquiries": inquiries,
        "students": students,
        "added": added
        })



#@login_required(login_url='/login')
def allclasses(request):
    try:
        listings = WatchList.objects.filter(user=request.user.username)
        lst = []
        for listing in listings:
            item = Listing.objects.get(id=listing.listingid)
            lst.append(item)
    except:
        listings = []
        lst = []
        for listing in listings:
            item = Listing.objects.get(id=listing.listingid)
            lst.append(item)

    specific_classes = Listing.objects.order_by("-timestamp").all()
    paginator = Paginator(specific_classes, 5)
    page = request.GET.get('page')


    #present = []

    #lst = []
    #for listing in listings:
            #item = Listing.objects.get(id=listing.listingid)
            #lst.append(item)

    #for specific_class in specific_classes:
        #if specific_class in lst:
            #present.append(specific_class)




    #allpost = Post.objects.order_by("-timestamp").all()
    #paginator = Paginator(allpost, 10)
    #page = request.GET.get('page')

    #return render(request, "network/index.html", {
        #"allposts": paginator.get_page(page)
    #})

    return render(request, "auctions/allclasses.html", {
        "present": lst,
        "classes": paginator.get_page(page)
    })



@login_required(login_url='/login')
def viewclass(request, class_id):
    specific_class = Listing.objects.get(id=class_id)
    inquiries = Inquiry.objects.filter(listingid=class_id)
    students = Student.objects.filter(listingid=class_id)
    print(class_id)
    print(students)
    timeslots = Timeslots.objects.filter(listingid=class_id)
    
    added = WatchList.objects.filter(
            listingid=class_id, user=request.user.username)

    print(added)

    if added is None:
        added = []
    else:
        pass
    

    student_users = []
    for student in students:
        student_users.append(student.user)

    registered_customers = {}



    timeslotids = []
    for timeslot in timeslots:
        timeslotids.append(timeslot.timeslotid)

    specified_customers = []


    #all_customers = Customers.objects.all()

    #for all_customer in all_customers:
        #for timeslotid in timeslotids:
            #if all_customer.customerid == timeslotid:
                #specified_customers.append(all_customer.customer)

        #thiscustomer = Customers.objects.filter(customerid=timeslotid, customer=request.user.username)
    #print(specified_customers)



    for timeslot in timeslots:
        registered_customers[timeslot.timeslotid] = {
            "timeslot": timeslot.timeslot,
            "timeslotid": timeslot.timeslotid,
            "specific_customers": Customers.objects.filter(customerid=timeslot.timeslotid)
        }

    specified_customers = []

    for x,y in registered_customers.items():
        specified_customers.append(y)



    return render(request, "auctions/viewclass.html", {
        "class": specific_class,
        "inquiries": inquiries,
        "students": students,
        "timeslots": timeslots,
        "student_users": student_users,
        "specified_customers": specified_customers,
        "added": added
    })

@login_required(login_url='/login')
def addannouncement(request, class_id):
    if request.method == "POST":
        specific_class = Listing.objects.get(id=class_id)
        specific_class.announcement = request.POST.get('announcement')
        specific_class.save()

        return redirect("viewclass", class_id=class_id)
    else:
        pass


@login_required(login_url='/login')
def choosetimeslot(request, listingid):
    if request.method == "POST":
        spec_timing = Timeslots.objects.get(timeslotid=request.POST.get('timeslotnumber'))
        #spec_timing.customer = request.user.username
        existing_stuff = []

        buses = Timeslots.objects.filter(listingid=listingid)
        for bus in buses:
            existing_stuff.append(bus.timeslotid)


        all_timeslots = Customers.objects.filter(customer=request.user.username)
        for all_timeslot in all_timeslots:
            if all_timeslot.customerid in existing_stuff:
                all_timeslot.delete()

        newcustomer = Customers()
        newcustomer.customer = request.user.username
        newcustomer.customerid = request.POST.get('timeslotnumber')
        newcustomer.save()

        return redirect("viewclass", class_id=spec_timing.listingid)
    else:
        pass

@login_required(login_url='/login')
def unselecttimeslot(request, timeslotid):
    if request.method == "POST":
        spec_timing = Timeslots.objects.get(timeslotid=timeslotid)

        customer = Customers.objects.filter(customerid=timeslotid, customer=request.user.username)
        #spec_timing.customer = None
        customer.delete()
        return redirect("viewclass", class_id=spec_timing.listingid)
    else:
        pass


@login_required(login_url='/login')
def addtowatchlist(request, class_id):
    if request.method == "POST":
        # if its already there then user wants to remove it from watchlist
        if Profile.objects.get(user=request.user.username) is not None:
            obj = WatchList()
            obj.user = request.user.username
            obj.listingid = class_id
            obj.save()

            student = Student()
            student.user = request.user.username
            student.listingid = class_id
            student.save()

            alerts = Notifications()
            teacher = Listing.objects.get(id=class_id)
            alerts.user = teacher.user
            alerts.info = str(request.user.username) + " " + "has signed up for your class."
            alerts.category = "Classmatters"
            alerts.notifid = class_id
            alerts.read = False
            alerts.save()

            messages.success(request, 'You have signed up!')
        else:
            message.error(request, 'Create a profile first!')

        # returning the updated content
        #added = WatchList.objects.filter(
            #listingid=class_id, user=request.user.username)
        #students = Student.objects.filter(listingid=class_id)
        #inquiries = Inquiry.objects.filter(listingid=class_id)
        #specific_class = Listing.objects.get(id=class_id)
        #return render(request, "auctions/viewclass.html", {
            #"class": specific_class,
            #"added": added,
            #"inquiries": inquiries,
            #"students": students
        #})
        return HttpResponseRedirect(reverse("yourclasses"))

    else:
        #added = WatchList.objects.filter(
            #listingid=class_id, user=request.user.username)
        students = Student.objects.filter(listingid=class_id)
        inquiries = Inquiry.objects.filter(listingid=class_id)
        specific_class = Listing.objects.get(id=class_id)
        timeslots = Timeslots.objects.filter(listingid=class_id)
        added = WatchList.objects.filter(
            listingid=class_id, user=request.user.username)
        return render(request, "auctions/viewclass.html", {
            "class": specific_class,
            "inquiries": inquiries,
            "students": students,
            "timeslots": timeslots,
            "added": added
        })

@login_required(login_url='/login')
def removefromwatchlist(request, class_id):
    if request.method == "POST":
        obj = WatchList.objects.filter(listingid=class_id, user=request.user.username)
        obj.delete()

        student = Student.objects.filter(listingid=class_id, user=request.user.username)
        student.delete()

        timeslots = Timeslots.objects.filter(listingid=class_id)
        for timeslot in timeslots:
            isthere = Customers.objects.filter(customerid=timeslot.timeslotid, customer=request.user.username)
            if isthere is not None:
                isthere.delete()



        return HttpResponseRedirect(reverse("yourclasses"))

    else:
        students = Student.objects.filter(listingid=class_id)
        inquiries = Inquiry.objects.filter(listingid=class_id)
        specific_class = Listing.objects.get(id=class_id)
        timeslots = Timeslots.objects.filter(listingid=class_id)
        added = WatchList.objects.filter(
            listingid=class_id, user=request.user.username)
        return render(request, "auctions/viewclass.html", {
            "class": specific_class,
            "inquiries": inquiries,
            "students": students,
            "timeslots": timeslots,
            "added": added
        })



@login_required(login_url='/login')
def addinquiry(request, class_id):
    if request.method == "POST":
        obj = Inquiry()
        obj.comment = request.POST.get("comment")
        obj.user = request.user.username
        obj.listingid = class_id
        obj.save()
    # returning the updated content

        return redirect("viewclass", class_id=class_id)
        #inquiries = Inquiry.objects.filter(listingid=class_id)
        #students = Student.objects.filter(listingid=class_id)
        #specific_class = Listing.objects.get(id=class_id)
        #timeslots = Timeslots.objects.filter(listingid=class_id)
        #added = WatchList.objects.filter(
        #listingid=class_id, user=request.user.username)
        #return render(request, "auctions/viewclass.html", {
                #"class": specific_class,
                #"added": added,
                #"inquiries": inquiries,
                #"timeslots": timeslots,
                #"students": students
        #})
    else:
        inquiries = Inquiry.objects.filter(listingid=class_id)
        students = Student.objects.filter(listingid=class_id)
        specific_class = Listing.objects.get(id=class_id)
        timeslots = Timeslots.objects.filter(listingid=class_id)
        added = WatchList.objects.filter(
        listingid=class_id, user=request.user.username)
        return render(request, "auctions/viewclass.html", {
                "class": specific_class,
                "added": added,
                "inquiries": inquiries,
                "timeslots": timeslots,
                "students": students
        })

@login_required(login_url='/login')
def addtimeslots(request, class_id):
    if request.method == "POST":
        newtimeslot = Timeslots()
        newtimeslot.listingid = class_id
        newtimeslot.timeslot = str(request.POST.get("day")) + " " + str(request.POST.get("time"))
        newtimeslot.selected = False
        newtimeslot.timeslotid = generaterandomint()
        newtimeslot.limitpax = request.POST.get("limit")
        newtimeslot.save()
        return redirect("viewclass", class_id=class_id)
    else:
        inquiries = Inquiry.objects.filter(listingid=class_id)
        students = Student.objects.filter(listingid=class_id)
        specific_class = Listing.objects.get(id=class_id)
        timeslots = Timeslots.objects.filter(listingid=class_id)
        added = WatchList.objects.filter(
        listingid=class_id, user=request.user.username)
        return render(request, "auctions/viewclass.html", {
                "class": specific_class,
                "added": added,
                "inquiries": inquiries,
                "students": students,
                "timeslots": timeslots
        })







@login_required(login_url='/login')
def yourprofile(request):
    obj = Profile.objects.get(user=request.user.username)
    try:
        lst = WatchList.objects.filter(user=request.user.username)
        # list of products available in WinnerModel
        present = False
        prodlst = []
        i = 0
        if lst:
            present = True
            for item in lst:
                specific_class = Listing.objects.get(id=item.listingid)
                prodlst.append(specific_class)
    except:
        lst = []
        present = False
        prodlst = []
        i = 0
        if lst:
            present = True
            for item in lst:
                specific_class = Listing.objects.get(id=item.listingid)
                prodlst.append(specific_class)
        
    if obj:
        return render(request, "auctions/yourprofile.html", {
            "obj": obj,
            "product_list": prodlst,
            "present": present
        })
    else:
        return render(request, "auctions/errorpage.html")

@login_required(login_url='/login')
def yourclasses(request):
    try:
        lst = WatchList.objects.filter(user=request.user.username)
        present = False
        prodlst = []
        i = 0
        if lst:
            present = True
            for item in lst:
                specific_class = Listing.objects.get(id=item.listingid)
                prodlst.append(specific_class)
    except:
        lst = []
        present = False
        prodlst = []
        i = 0
        if lst:
            present = True
            for item in lst:
                specific_class = Listing.objects.get(id=item.listingid)
                prodlst.append(specific_class)

    #present = False
    #prodlst = []
    #i = 0
    #if lst:
        #present = True
        #for item in lst:
            #specific_class = Listing.objects.get(id=item.listingid)
            #prodlst.append(specific_class)

    return render(request, "auctions/yourclasses.html", {
            "product_list": prodlst,
            "present": present
    })


@login_required(login_url='/login')
def profile(request, user):
    obj = Profile.objects.get(user=user)
    specific_user = User.objects.get(username=user)
    jobs = Listing.objects.filter(user=user)
    present = False
    prodlst = []
    i = 0
    if jobs:
        present = True
        for job in jobs:
            prodlst.append(job)

    return render(request, "auctions/publicprofile.html", {
        "obj":obj,
        "product_list": prodlst,
        "present": present,
        "specific_user": specific_user
    })

@login_required(login_url='/login')
def searchforclasses(request):
    if request.method == "POST":
        subject = request.POST.get("searchsubject").upper()
        listings = WatchList.objects.filter(user=request.user.username)

        lst = []
        for listing in listings:
            item = Listing.objects.get(id=listing.listingid)
            lst.append(item)
        lol = True

        if request.POST.get("searchprice"):
            classprice = int(request.POST.get("searchprice"))
            classes = Listing.objects.filter(price__lte=classprice, subject=subject)

            empty = False
            if len(classes) == 0:
                empty = True

            return render(request, "auctions/allclasses.html",{
            "classes": classes,
            "present": lst,
            "empty": empty,
            "lol": lol
            })
        else:
            classes = Listing.objects.filter(subject=subject)
            empty = False
            if len(classes) == 0:
                empty = True

            return render(request, "auctions/allclasses.html", {
            "classes": classes,
            "present": lst,
            "empty": empty,
            "lol": lol
            })



    else:
        return HttpResponseRedirect(reverse("allclasses"))



@login_required(login_url='/login')
def rateteacher(request, user):
    teacher = User.objects.get(username=user)
    ratings = Rating.objects.filter(teacher_user=user)

    if len(ratings) != 0:
        empty = False
        total = 0
        for rating in ratings:
            total += rating.score

        average = total / len(ratings)

        return render(request, "auctions/rating.html", {
        "teacher": teacher,
        "ratings": ratings,
        "average": average,
        "empty": empty
        })

    else:
        empty = True
        average = None


        return render(request, "auctions/rating.html", {
            "teacher": teacher,
            "ratings": ratings,
            "average": average,
            "empty": empty
    })

@login_required(login_url='/login')
def searchreviews(request):
    reviewsubject = request.POST.get('reviewsubject').upper()
    teacher_user = request.POST.get('user')

    new = True

    spec_ratings = Rating.objects.filter(teacher_user=teacher_user, subject=reviewsubject)
    teacher = User.objects.get(username=teacher_user)

    total = 0
    for spec_rating in spec_ratings:
        total += spec_rating.score

    average = total / len(spec_ratings)

    return render(request, "auctions/subjectspecificrating.html", {
        "teacher": teacher,
        "subject": reviewsubject,
        "ratings": spec_ratings,
        "average": average,
        "new": new
    })

@login_required(login_url='/login')
def newcontact(request):
    if request.method == "POST":
        obj = Chat()
        obj.user = request.user.username
        obj.contact = request.POST.get('contact')
        obj.save()

        return HttpResponseRedirect(reverse("contacts"))
    else:
        pass

@login_required(login_url='/login')
def findnewcontact(request):
    if request.method == "POST":
        search = request.POST.get('findcontact')
        newfriend = get_object_or_404(User, username=search)

        existing_contacts = []
        chats = Chat.objects.filter(user=request.user.username)
        for chat in chats:
            existing_contacts.append(chat.contact)

        if newfriend.username in existing_contacts:
            messages.error(request, "already exists in contacts")
            return render(request, "auctions/displaynewcontact.html")

        else:
            return render(request, "auctions/displaynewcontact.html", {
                "newfriend": newfriend
            })
    else:
        return render(request, "auctions/displaynewcontact.html")



@login_required(login_url='/login')
def contacts(request):
    connections = Chat.objects.filter(user=request.user.username)

    existing = [request.user.username]

    known = []

    for connection in connections:
        existing.append(connection.contact)
        known.append(connection.contact)

    all_users = User.objects.exclude(username__in=existing)
    incoming_messages = Messages.objects.filter(receiver=request.user.username, read=False).order_by('sender')

    senders_list = []
    for incoming_message in incoming_messages:
        senders_list.append(incoming_message.sender)

    uniquesenders_list = set(senders_list)

    messageshash = {}

    for sender in uniquesenders_list:
        messageshash[sender] = {
            "sender": sender,
            "messages": Messages.objects.filter(receiver=request.user.username, read=False, sender=sender)
        }

    pendingmessages = []
    for x, y in messageshash.items():
        pendingmessages.append(y)


    empty = False
    if len(connections) == 0:
        empty = True

    mars = False

    return render(request, "auctions/contacts.html", {
        "connections": connections,
        #"incoming_messages": incoming_messages,
        "pendingmessages": pendingmessages,
        "known": known,
        "all_users": all_users,
        "empty": empty,
        "mars": mars

    })

@login_required(login_url='/login')
def findcontact(request):
    if request.method == "POST":
        contact = request.POST.get('contact')
        connection = Chat.objects.get(user=request.user.username, contact=contact)
        friends = Chat.objects.filter(user=request.user.username)
        mars = True
        return render(request, "auctions/contacts.html", {
            "person": connection,
            "mars": mars,
            "connections": friends
        })
    else:
        return redirect("contacts")

@login_required(login_url='/login')
def newmessage(request, contact):
    if request.method == "POST":
        send_message = Messages()
        send_message.receiver = contact
        send_message.sender = request.user.username
        send_message.content = request.POST.get('content')
        send_message.read = False
        #send_message.message_id = generaterandomint()
        send_message.timestamp = timezone.localtime(timezone.now())
        send_message.save()

        updates = Notifications()
        updates.user = contact
        updates.info = str(request.user.username) + " " + "has sent you a message."
        updates.category = "Messagingmatters"
        updates.read = False
        updates.save()

        return redirect("chatwithcontacts", contact=contact)
        #all_messages = Messages.objects.filter(receiver=contact, sender=request.user.username) | Messages.objects.filter(sender=contact, receiver=request.user.username)
        #ordered_messages = all_messages.order_by('timestamp')

        #empty = False
        #if len(ordered_messages) == 0:
            #empty = True

        #return render(request, "auctions/chat.html", {
            #"all_messages": ordered_messages,
            #"contact": contact,
            #"empty": empty
        #})

    else:
        return redirect("chatwithcontacts", contact=contact)
        all_messages = Messages.objects.filter(receiver=contact, sender=request.user.username) | Messages.objects.filter(sender=contact, receiver=request.user.username)
        ordered_messages = all_messages.order_by('timestamp')

        empty = False
        if len(ordered_messages) == 0:
            empty = True

        return render(request, "auctions/chat.html", {
            "all_messages": ordered_messages,
            "contact": contact,
            "empty": empty
        })


def ignoreuser(request, usertoignore):
    messagestoignore = Messages.objects.filter(receiver=request.user.username, sender=usertoignore, read=False)
    for messagetoignore in messagestoignore:
        #messagetoignore.read = True
        messagetoignore.delete()

    return redirect("contacts")

def resolveall(request):
    incoming_messages = Messages.objects.filter(receiver=request.user.username, read=False)
    for incoming_message in incoming_messages:
        incoming_message.read = True
        incoming_message.save()

    return redirect("contacts")

#@login_required(login_url='/login')
#def sendmessage(request, contact):
    #send_message = Messages()
    #send_message.receiver = contact
    #send_message.sender = request.user.username
    #send_message.content = request.POST['content']
    #send_message.read = False
    #send_message.message_id = generaterandomint()
    #send_message.save()
    #return redirect("chatwithcontacts", contact=contact)


#def refreshforcontacts(request, sender):
   # return redirect("chatwithcontacts", contact=sender)



@login_required(login_url='/login')
def chatwithcontacts(request, contact):
    all_messages = Messages.objects.filter(receiver=contact, sender=request.user.username) | Messages.objects.filter(sender=contact, receiver=request.user.username)
    ordered_messages = all_messages.order_by('timestamp')

    readdamessages = Messages.objects.filter(sender=contact, receiver=request.user.username, read=False)
    for readdamessage in readdamessages:
        readdamessage.read = True
        readdamessage.save()

    existing = []
    connections = Chat.objects.filter(user=request.user.username)
    for connection in connections:
        existing.append(connection.contact)

    if contact not in existing:
        oof = Chat()
        oof.user = request.user.username
        oof.contact = contact
        oof.save()

    #for message in all_messages:
        #if message.read == False:
            #message.read = True
            #message.save()

    empty = False
    if len(ordered_messages) == 0:
        empty = True

    return render(request, "auctions/chat.html", {
        "all_messages": ordered_messages,
        "contact": contact,
        "empty": empty
    })



#@login_required(login_url='/login')
#def getmessages(request, contact):
     #all_messages = Messages.objects.filter(receiver=contact, sender=request.user.username) | Messages.objects.filter(sender=contact, receiver=request.user.username)
     #ordered_messages = all_messages.order_by('timestamp')
     #contact = contact

     #return JsonResponse({"messages": list(ordered_messages.values())})



#@login_required(login_url='/login')
#def replymessages(request, message_id):
    #spec_message = Messages.objects.get(message_id=message_id)
    #spec_message.read = True
    #spec_message.save()

    #existing = []
    #connections = Chat.objects.filter(user=request.user.username)
    #for connection in connections:
        #existing.append(connection.contact)

    #if spec_message.sender not in existing:
        #oof = Chat()
        #oof.user = request.user.username
        #oof.contact = spec_message.sender
        #oof.save()


    #return redirect("chatwithcontacts", contact=spec_message.sender)
@login_required(login_url='/login')
def viewyournotifs(request):
    messagingnotifs = Notifications.objects.filter(user=request.user.username, category="Messagingmatters", read=False)
    classnotifs = Notifications.objects.filter(user=request.user.username, category="Classmatters", read=False)
    ratingnotifs = Notifications.objects.filter(user=request.user.username, category="Ratingmatters", read=False)

    empty1 = False
    empty2 = False
    empty3 = False

    if len(messagingnotifs) == 0:
        empty1 = True

    if len(classnotifs) == 0:
        empty2 = True

    if len(ratingnotifs) == 0:
        empty3 = True

    return render(request, "auctions/yournotifs.html", {
        "messagingnotifs": messagingnotifs,
        "classnotifs": classnotifs,
        "ratingnotifs": ratingnotifs,
        "empty1": empty1,
        "empty2": empty2,
        "empty3": empty3
    })

@login_required(login_url='/login')
def resolvenotifs(request):
    combinednotifs = Notifications.objects.filter(user=request.user.username)
    for combinednotif in combinednotifs:
        combinednotif.read = True
        combinednotif.save()

    return redirect("viewyournotifs")



def generaterandomint():
    pots = Timeslots.objects.all()
    existing_ids = []
    for pot in pots:
        existing_ids.append(pot.timeslotid)
    random_id = choice([i for i in range(1000) if i not in existing_ids])
    return random_id




def error_404(request, exception):
    return render(request, "auctions/errorpage2.html", status=400)

def error_500(request, *args, **argv):
    return render(request, "auctions/errorpage.html", status=500)



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        try:
            usermode = Mode.objects.get(user=username)
        except:
            newmode = Mode()
            newmode.user = username
            newmode.mode = "student"
            newmode.save()


        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("homepage"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["first_name"]
        pin = request.POST["pin"]

        if len(pin) != 6:
            return render(request, "auctions/register.html", {
                "message": "Pin must be 6 digits."
            })

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        elif len(password) <= 7:
            return render(request, "auctions/register.html", {
                "message": "Password must be greater than 7 characters."
            })


        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.pin = pin
            user.save()

        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        newmode = Mode()
        newmode.user = username
        newmode.mode = "student"
        newmode.save()
        return HttpResponseRedirect(reverse("newperson"))
    else:
        return render(request, "auctions/register.html")

