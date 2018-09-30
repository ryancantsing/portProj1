from __future__  import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from . import models, managers

def index(request):
    return render(request, "port_Proj/index.html")

def login(request):
    result = models.Users.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    else:
        request.session['user_id'] = result.id
        request.session['username'] = result.username
        request.session['post_level'] = result.post_level
        return redirect('/status')

def register(request):
    result = models.Users.objects.validate_registration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    else:
        request.session['user_id'] = result.id
        return redirect('/status')

def status(request):
    user = models.Users.objects.get(id=request.session['user_id'])
    errors = []
    if user == None:
        errors.append("User not found, please login")
        return redirect('/')
    else:
        context = {
            'user' : user
        }
        return render(request, "port_Proj/status.html", context)
def user(request, user_id):
    user = models.Users.objects.get(id= user_id)
    context = {
        'user' : user
    }
    return render(request, "port_Proj/viewUser", context)
def logout(request):
    del request.session['username']
    del request.session['user_id']
    del request.session['post_level']
    return redirect('/')

def edit_user(request):
    result = models.Users.objects.validate_edit(request.POST, request.session['user_id'])
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/status')
    else:
        return redirect('/status')
def add_comment(request):
    result = models.Comments.objects.validate_comment(request.POST, request.session['user_id'])
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/status')
    else:
        print("everything worked yo")
        return redirect('/status')
def post(request):
    result = models.Posts.objects.validate_post(request.post, request.session['user_id'])
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/status')
    else: 
        print("everything worked, yo")
        return redirect('/status')
def delete_user(request):
    result = models.Users.objects.delete_user(request.session['user_id'])
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/status')
    else:
        print("user deleted")
        return redirect('/')
def delete_post(request, post_id):
    result = models.Posts.objects.delete_post(post_id)
    if result == True:
        return redirect('/status')
    else:
        print("we fucked up")
def delete_comment(request, comment_id):
    result = models.Comments.objects.delete_comment(comment_id)
    if result == True:
        return redirect('/status')



