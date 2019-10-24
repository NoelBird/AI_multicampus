from django.shortcuts import render
import random
import math
from datetime import datetime

# Create your views here.
def index(request):
    return render(request, 'pages/index.html')

def introduce(request, name, age):
    context = {'name': name, 'age': age}
    return render(request, 'pages/introduce.html', context)

def dinner(request):
    menu = ['짜장면', '햄버거', '치킨', '초밥', '김밥']
    pick = random.choice(menu)
    context = {'pick': pick}
    return render(request, 'pages/dinner.html', context)

def image(request):
    pick = random.randrange(1, 1000)
    context = {'img':f'https://picsum.photos/id/{pick}/200/200'}
    return render(request, 'pages/image.html', context)

def hello(request, name):
    menu = ['짜장면', '햄버거', '치킨', '초밥', '김밥']
    pick = random.choice(menu)
    context = {'name': name, 'menu': pick}
    return render(request, 'pages/hello.html', context)

def times(request, num1, num2):
    context = {'num':num1*num2}
    return render(request, 'pages/times.html', context)


def area(request, radius):
    context = {'area': round(math.pi*radius**2, 2), 'radius': radius}
    return render(request, 'pages/area.html', context)


def template_language(request):
    menus = ['짜장면', '시저샐러드', '오트밀', '삼겹살']
    my_sentence = 'Life is short, you need python.'
    messages = ['apple', 'banana', 'cucumber', 'mango']
    datetimenow = datetime.now()
    empty_list = []
    context = {
        'menus': menus,
        'my_sentence': my_sentence,
        'datetimenow': datetimenow,
        'empty_list': empty_list,
        'messages': messages
    }
    return render(request, 'pages/template_language.html', context)


# 실습 1
def check_mybirth(request):
    return render(request, 'pages/check_mybirth.html')

# 실습 2
def check_palindrom(request, str_pal):
    n_pal = len(str_pal)
    is_pal = True
    for i in range(0, n_pal//2):
        if str_pal[i] != str_pal[-i-1]:
            is_pal = False
    context = {'is_pal': is_pal, 'str_pal': str_pal}

    return render(request, 'pages/check_palindrom.html', context)