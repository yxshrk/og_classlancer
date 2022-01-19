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


# Create your views here.
def index(request):
    #print(request.user.username)
    all_posts = Post.objects.all()

    postshash = {}

    allposts = []


    for all_post in all_posts:
        postshash[all_post.id] = {
            "id": all_post.id,
            "content": all_post.content,
            "title": all_post.title,
            "category": all_post.category.upper(),
            "timestamp": all_post.timestamp,
            "author": all_post.author,
            "tags": Tag.objects.filter(post_id=all_post.id),
            "likers": genlikers(all_post.id),
            "comments": Comment.objects.filter(post_id=all_post.id),
            "sepcomments": fetchcomments(all_post.id)
        }

    for x,y in postshash.items():
        allposts.append(y)



    return render(request, "forums/landingpage.html", {
        "allposts": allposts
    })

def category(request, categ):
    all_posts = Post.objects.filter(category=categ)

    empty = False

    if len(all_posts) == 0:
        empty = True

    postshash = {}

    allposts = []


    for all_post in all_posts:
        postshash[all_post.id] = {
            "id": all_post.id,
            "content": all_post.content,
            "title": all_post.title,
            "category": all_post.category.upper(),
            "timestamp": all_post.timestamp,
            "author": all_post.author,
            "tags": Tag.objects.filter(post_id=all_post.id),
            "likers": genlikers(all_post.id),
            "comments": Comment.objects.filter(post_id=all_post.id),
            "sepcomments": fetchcomments(all_post.id)
        }

    for x,y in postshash.items():
        allposts.append(y)



    return render(request, "forums/specposts.html", {
        "allposts": allposts,
        "empty": empty,
        "category": categ.upper()

    })

def searchtag(request):
    if request.method == "POST":
        spectag = request.POST.get("tag")
        alltags = Tag.objects.filter(name=spectag)

        print(alltags)

        searchids = []
        for alltag in alltags:
            searchids.append(alltag.post_id)

        returnposts = []
        for searchid in searchids:
            returnposts.append(Post.objects.get(id=searchid))

        #all_posts = Post.objects.filter(category=categ)

        empty = False

        if len(returnposts) == 0:
            empty = True

        postshash = {}

        allposts = []


        for returnpost in returnposts:
            postshash[returnpost.id] = {
                "id": returnpost.id,
                "content": returnpost.content,
                "title": returnpost.title,
                "category": returnpost.category.upper(),
                "timestamp": returnpost.timestamp,
                "author": returnpost.author,
                "tags": Tag.objects.filter(post_id=returnpost.id),
                "likers": genlikers(returnpost.id),
                "comments": Comment.objects.filter(post_id=returnpost.id),
                "sepcomments": fetchcomments(returnpost.id)
        }

        for x,y in postshash.items():
            allposts.append(y)

        return render(request, "forums/tagposts.html", {
            "allposts": allposts
        })
    else:
        pass


def subjectsearchtag(request):
    if request.method == "POST":
        spectag = request.POST.get("subjecttag")
        subject = request.POST.get("subject").lower()
        alltags = Tag.objects.filter(name=spectag)

        print(alltags)

        searchids = []
        for alltag in alltags:
            searchids.append(alltag.post_id)

        tempreturnposts = []
        for searchid in searchids:
            tempreturnposts.append(Post.objects.get(id=searchid))

        returnposts = []
        for tempreturnpost in tempreturnposts:
            if tempreturnpost.category == subject:
                returnposts.append(tempreturnpost)

        #all_posts = Post.objects.filter(category=categ)

        empty = False

        if len(returnposts) == 0:
            empty = True

        postshash = {}

        allposts = []


        for returnpost in returnposts:
            postshash[returnpost.id] = {
                "id": returnpost.id,
                "content": returnpost.content,
                "title": returnpost.title,
                "category": returnpost.category.upper(),
                "timestamp": returnpost.timestamp,
                "author": returnpost.author,
                "tags": Tag.objects.filter(post_id=returnpost.id),
                "likers": genlikers(returnpost.id),
                "comments": Comment.objects.filter(post_id=returnpost.id),
                "sepcomments": fetchcomments(returnpost.id)
        }

        for x,y in postshash.items():
            allposts.append(y)

        return render(request, "forums/tagposts.html", {
            "allposts": allposts
        })
    else:
        pass



def dasearchpage(request):
    return render(request, "forums/searchpage.html")



def genlikers(post_id):
    supporters = []
    likers = Liker.objects.filter(post_id=post_id)
    for liker in likers:
        supporters.append(liker.user)

    #print(supporters)

    return supporters

def gencommentlikers(comment_id):
    squids = []
    comms = LikeComment.objects.filter(comment_id=comment_id)
    for comm in comms:
        squids.append(comm.user)

    return squids

def fetchcomments(post_id):
    comments = Comment.objects.filter(post_id=post_id)
    commentshash = {}
    for comment in comments:
        commentshash[comment.indivcomment_id] = {
            "content": comment.content,
            "user": comment.user,
            "indivcomment_id": comment.indivcomment_id,
            "timestamp": comment.timestamp,
            "likers": gencommentlikers(comment.indivcomment_id)
        }

    sepcomments = []

    for x,y in commentshash.items():
        sepcomments.append(y)

    return sepcomments




@login_required(login_url='/login')
def newpost(request):
    if request.method == "POST":
        obj = Post()
        obj.title = request.POST.get("title")
        obj.category = request.POST.get("category")
        obj.content = request.POST.get("content")
        obj.author = request.user.username
        obj.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "forums/landingpage.html")

@login_required(login_url='/login')
def yourposts(request):
    all_posts = Post.objects.filter(author=request.user.username)

    empty = False

    if len(all_posts) == 0:
        empty = True

    postshash = {}

    allposts = []


    for all_post in all_posts:
        postshash[all_post.id] = {
            "id": all_post.id,
            "content": all_post.content,
            "title": all_post.title,
            "category": all_post.category.upper(),
            "timestamp": all_post.timestamp,
            "author": all_post.author,
            "tags": Tag.objects.filter(post_id=all_post.id),
            "likers": genlikers(all_post.id),
            "comments": Comment.objects.filter(post_id=all_post.id),
            "sepcomments": fetchcomments(all_post.id)
        }

    for x,y in postshash.items():
        allposts.append(y)

    return render(request, "forums/specposts.html", {
        "allposts": allposts,
        "empty": empty,
        "category": "Your Posts"

    })


@login_required(login_url='/login')
def togglelike(request, post_id):
    post = Post.objects.get(pk=post_id)

    fans = []

    likers = Liker.objects.filter(post_id=post_id)
    for liker in likers:
        fans.append(liker.user)

    if request.user.username not in fans:
        obj = Liker()
        obj.user = request.user.username
        obj.post_id = post_id
        obj.save()
    else:
        exi = Liker.objects.get(post_id=post_id, user=request.user.username)
        exi.delete()

    return HttpResponse("done")

@login_required(login_url='/login')
def togglecommentlike(request, comment_id):
    comment = Comment.objects.get(indivcomment_id=comment_id)

    peeps = []

    commlikers = LikeComment.objects.filter(comment_id=comment_id)
    for commliker in commlikers:
        peeps.append(commliker.user)

    if request.user.username not in peeps:
        newlike = LikeComment()
        newlike.user = request.user.username
        newlike.comment_id = comment_id
        newlike.save()
    else:
        exis = LikeComment.objects.get(comment_id=comment_id, user=request.user.username)
        exis.delete()

    return HttpResponse("done")

@login_required(login_url='/login')
def addcomment(request, post_id):
    if request.method == "POST":
        newcomment = Comment()
        newcomment.post_id = post_id
        newcomment.content = request.POST.get("comment")
        newcomment.user = request.user.username
        newcomment.indivcomment_id = generaterandomint()

        newcomment.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "forums/landingpage.html")

@login_required(login_url='/login')
def addtag(request, post_id):
    if request.method == "POST":
        newtag = Tag()
        newtag.post_id = post_id
        newtag.name = request.POST.get("tag")

        newtag.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "forums/landingpage.html")



def generaterandomint():
    pots = Comment.objects.all()
    existing_ids = []
    for pot in pots:
        existing_ids.append(pot.indivcomment_id)
    random_id = choice([i for i in range(1000) if i not in existing_ids])
    return random_id





