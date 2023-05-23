from django.shortcuts import render, redirect
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import User, Profile, Post, Post_media, Follow, Like, Comment, Story
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.urls import reverse

# Create your views here.


def create_profile(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        image = request.FILES.get('profilepic')

        if User.objects.filter(username=username).count() > 0:
            messages.error(request, "User already exist!!!")
            return redirect('signup')
        # if len(password)<8:
        #     messages.error(request,"Password should minimum 8 characters")
        #     return redirect('signup')
        user = User.objects.create_user(username=username, password=password)
        user.save()
        profile = Profile.objects.create(
            name=name, profile_picture=image, user_id=user)
        profile.save()
        if profile:
            messages.success(request, 'Profile Created')
            return redirect("Login")
    return render(request, 'Signup.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            # messages.success(request,"Loged in")
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request, 'Check username or password')

    return render(request, "Login.html")


def Logout(request):
    logout(request)
    return redirect("Login")


def profile(request, username=None):
    if not request.user.is_authenticated:
        return redirect('Login')

    loged_profile = Profile.objects.get(user_id=request.user)
    follow_status = False

    if username == None:
        user = User.objects.get(username=request.user)
        profile = Profile.objects.get(user_id=request.user)

        post_id = Post.objects.filter(user_id=request.user)
        # print(post_id)
        posts_num = post_id.count()
        posts = []
        for post in post_id:
            posts.append(Post_media.objects.get(post_id=post.id))
        # posts = Post_media.objects.filter(post_id=post_id)
        print(posts)

        followers = Follow.objects.filter(following=request.user)
        followers_count = followers.count()
        followings = Follow.objects.filter(follower=request.user)
        followings_count = followings.count()

    else:
        loged_profile = Profile.objects.get(user_id=request.user)
        user = User.objects.get(username=username)

        profile = Profile.objects.get(user_id=user)

        post_id = Post.objects.filter(user_id=user)
        # print(post_id)
        posts_num = post_id.count()
        posts = []
        for post in post_id:
            posts.append(Post_media.objects.get(post_id=post.id))
        # posts = Post_media.objects.filter(post_id=post_id)
        # print(posts)
        follow_status = Follow.objects.filter(
            follower=request.user, following=user).exists()

        followers = Follow.objects.filter(following=user)
        print(followers)
        followers_count = followers.count()
        followings = Follow.objects.filter(follower=user)
        followings_count = followings.count()
    return render(request, 'profile.html', {'profile': profile, 'user': user,  'posts_num': posts_num,
                                            'posts': posts, 'followers_count': followers_count, 'followers': followers,
                                            'followings_count': followings_count, 'loged_profile': loged_profile, 'follow_status': follow_status})


def search(request):
    if not request.user.is_authenticated:
        return redirect("Login")
    search = request.GET.get('username')
    context = {}
    if search:
        profiles = Profile.objects.filter(user_id__username__icontains=search)
        context['profiles'] = profiles
    return render(request, 'search.html', context)


def follow(request, username):

    # print(username)
    user = User.objects.get(username=username)
    f, created = Follow.objects.get_or_create(
        follower=request.user, following=user)

    # print(created)
    if created == False:
        f.delete()

    followers_count = Follow.objects.filter(
        following__username=username).count()
    print(followers_count)
    # return HttpResponseRedirect(reverse('profile', kwargs={'username': username}))
    return JsonResponse({'followers_count': followers_count}, safe=False)


def uploadpost(request):

    if not request.user.is_authenticated:
        return redirect("Login")

    if request.method == 'POST':
        post = request.FILES.get('post')
        caption = request.POST.get('caption')
        location = request.POST.get('location')
        # user = User.objects.get(username=request.user)
        post_object = Post.objects.create(
            user_id=request.user, caption=caption, location=location, profile=request.user.profile)
        post_media_object = Post_media.objects.create(
            post_id=post_object, file=post, position=1)

        if post_object and post_media_object:
            messages.success(request, "Post Added")
    return render(request, 'uploadpost.html', {})


def home(request):
    if not request.user.is_authenticated:
        return redirect("Login")

    # followings = Follow.objects.filter(follower=request.user)
    # posts = Post.objects.filter(user_id__follower=request.user)
    # print(posts)
    # print(request.user.following.all())
    # print(request.user.follower.all())

    # print(followings)
    # post_media = []

    all_posts = Post_media.objects.filter(
        post_id__user_id__in=request.user.follower.values('following'))

    all_stories = Story.objects.filter(
        profile__user_id__in=request.user.follower.values('following'))

    # print(temp)
    # for follower in followings:
    #     # print(follower.following)
    #     objects = Post_media.objects.filter(post_id__user_id=follower.following)
    #     for object in objects:
    #         post_media.append(object)
    #     # print(object)
    # print(post_media)

    return render(request, 'home.html', {'posts': all_posts, 'stories': all_stories})


def like(request, id):

    print(id)
    post = Post.objects.get(id=id)

    # likesuser = post.liked.all()
    # print(likesuser)

    if request.user in post.liked.all():
        post.liked.remove(request.user)
        post.likes -= 1
    else:
        post.liked.add(request.user)
        post.likes += 1

    # print(likesuser)
    post.save()
    return JsonResponse({'likes_count': post.likes}, safe=False)


def comments(request, id):

    post = Post.objects.get(id=id)
    print(post)

    if request.method == 'POST':
        comment = request.POST.get('comment')
        if comment:
            parent = request.POST.get('parent')
            if parent:
                parentComment = Comment.objects.get(id=int(parent))
                Comment.objects.create(
                    text=comment, user=request.user, post=post, parent=parentComment)
            else:

                Comment.objects.create(
                    text=comment, user=request.user, post=post)

    return render(request, 'comment.html', {'post': post})


def uploadstory(request):

    if not request.user.is_authenticated:
        return redirect("Login")

    if request.method == 'POST':
        story = request.FILES.get('story')
        print(story)
        profile = Profile.objects.get(user_id=request.user)
        story_upload = Story.objects.create(story=story, profile=profile)
        if story_upload:
            messages.success(request, "STORY UPLOADED")
    return render(request, 'uploadstory.html', {})


def editprofile(request):

    if not request.user.is_authenticated:
        return redirect("Login")

    profile = Profile.objects.get(user_id=request.user)

    if request.method == 'POST':

        name = request.POST.get('name')
        bio = request.POST.get('bio')
        image = request.FILES.get('profilepic')

        if name:
            profile.name = name
            profile.bio = bio
            if image:
                profile.profile_picture = image
            profile.save()
        return HttpResponseRedirect(reverse('profile', kwargs={'username': request.user.username}))

    return render(request, 'editprofile.html', {})
