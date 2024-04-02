import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator

from .models import Like, User, Post, Follow

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        labels = {
            "content": ("")
        }
        widgets = {
            "content": forms.Textarea(attrs={
                "placeholder": "Create a new post here",
                "class": "form-control",
                "rows": 1
            })
        }

def index(request):
    allPosts = Post.objects.all().order_by("id").reverse()

    for post in allPosts:
        post_obj = Post.objects.get(pk=post.id)
        like_list = Like.objects.filter(post=post_obj)

        if len(like_list):
            post_obj.likes = len(like_list)
        else:
            post_obj.likes = 0
        
        post_obj.save()
    
    p = Paginator(allPosts, 10)
    page_number = request.GET.get('page')
    page_posts = p.get_page(page_number)
    
    allLikes = Like.objects.all()

    youLiked=[]

    try:
        for like in allLikes:
            if like.user.id == request.user.id:
                youLiked.append(like.post.id)
    except:
        youLiked = []

    return render(request, "network/index.html", {
        "post_form": PostForm(),
        "title": "All Posts",
        "page_posts": page_posts,
        "youLiked": youLiked
    }) 


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def newPost(request):
    
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.cleaned_data["content"]
            newPost= Post (
                user = User.objects.get(pk=request.user.id),
                content = post,
            )
            newPost.save()

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/errorPage.html", {
                "code": 400,
                "message": "Form is invalid"
            })
    
def profile(request, userId):
    currentProfile = User.objects.get(pk=userId)
    allPosts = Post.objects.filter(user=currentProfile).order_by("id").reverse()

    following = Follow.objects.filter(user=currentProfile)
    followers = Follow.objects.filter(user_follows=currentProfile)

    try:
        if Follow.objects.filter(user=User.objects.get(pk=request.user.id), user_follows=currentProfile).exists():
            is_following = True
        else:
            is_following = False
    except:
        is_following = False

    p = Paginator(allPosts, 10)
    page_number = request.GET.get('page')
    page_posts = p.get_page(page_number)

    allLikes = Like.objects.all()

    youLiked=[]

    try:
        for like in allLikes:
            if like.user.id == request.user.id:
                youLiked.append(like.post.id)
    except:
        youLiked = []

    return render (request, "network/profile.html", {
        "currentUser": currentProfile,
        "posts": allPosts,
        "page_posts": page_posts,
        "following": following.count,
        "followers": followers.count,
        "is_following": is_following,
        "youLiked": youLiked
    }) 

def follow_unfolow(request, userId):

    if request.method == "GET":
        return HttpResponse(status=405)
    
    if request.method == "POST":
        try:
            follow_obj = Follow.objects.get(user=request.user.id, user_follows=userId)
        except Follow.DoesNotExist:
            try:
                user_to_follow = User.objects.get(pk=userId)
            except User.DoesNotExist:
                return HttpResponse(status=404)
            else:
                new_follow_obj = Follow(user=request.user, user_follows=user_to_follow)
                new_follow_obj.save()
        else:
            follow_obj.delete()

        return HttpResponseRedirect(reverse("profile", args=[userId]))
    
def following(request):
    currentUser= User.objects.get(pk=request.user.id)
    following_people = Follow.objects.filter(user=currentUser)
    allPosts = Post.objects.all().order_by("id").reverse()

    for post in allPosts:
            post_obj = Post.objects.get(pk=post.id)
            like_list = Like.objects.filter(post=post_obj)

            if len(like_list):
                post_obj.likes = len(like_list)
            else:
                post_obj.likes = 0
            
            post_obj.save()

    following_posts= []

    for post in allPosts:
        for person in following_people:
            if person.user_follows == post.user:
                following_posts.append(post)

    p = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    page_posts = p.get_page(page_number)

    allLikes = Like.objects.all()

    youLiked=[]

    try:
        for like in allLikes:
            if like.user.id == request.user.id:
                youLiked.append(like.post.id)
    except:
        youLiked = []

    return render(request, "network/index.html", {
        "post_form": None,
        "title": "Following",
        "page_posts": page_posts,
        "youLiked": youLiked
    })  

def editPost(request, postId):
    if request.method == "GET":
        return HttpResponse(status=405)
    
    if request.method == "POST":
        data = json.loads(request.body)
        editPost = Post.objects.get(pk=postId)
        editPost.content = data["content"]
        editPost.save()
        return JsonResponse({"message": "edited successfully", "data": data["content"]})

def likePost(request, postId):

    if request.method == "GET":
        return HttpResponse(status=405)
    
    if request.method == "POST":
        post = Post.objects.get(pk=postId)
        user = User.objects.get(pk=request.user.id)
        newLike = Like(user=user, post=post)
        newLike.save()
        
        like_list = Like.objects.filter(post=post)
        like_list_size= len(like_list)

        return JsonResponse({"message": "Like successfully", "list_size": like_list_size})

def unlikePost(request, postId):
    if request.method == "GET":
        return HttpResponse(status=405)
    
    if request.method == "POST":
        post = Post.objects.get(pk=postId)
        user = User.objects.get(pk=request.user.id)
        like = Like.objects.filter(user=user, post=post)
        like.delete()
        
        like_list = Like.objects.filter(post=post)
        like_list_size= len(like_list)

        return JsonResponse({"message": "Unlike successfully", "list_size": like_list_size})
