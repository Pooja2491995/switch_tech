import json

from django.shortcuts import render,redirect,get_object_or_404
from django.http import request, HttpResponse,JsonResponse,response
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import *
import random
import math
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail


# Create your views here.
# def registerPage(request):
#     if request.user.is_authenticated:
#         return redirect('home')
#     else:
#         form = createuserform()
#         if request.method == 'POST':
#             form = createuserform(request.POST)
#             if form.is_valid():
#                 user = form.save()
#                 username = form.cleaned_data.get('username')
#                 current_domain = form.cleaned_data.get('current_domain')
#                 user_id = User.objects.get(username=username).pk
#                 user_data = UserData.objects.create(user_id=user_id,current_domain=current_domain)
#                 user_data.save()
#                 return redirect('login')
#         context = {
#             'form': form,
#         }
#         return render(request, 'register.html', context)

# def loginPage(request):
#     if request.user.is_authenticated:
#         # return redirect('home')
#         return redirect('login')
#     else:
#         if request.method == "POST":
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#                 # return render(request, 'jotquiz.html')
#         context = {}
#         return render(request, 'login.html', context)

# testing_otp_code
    
def generate_otp():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def loginPage(request):
    print("yes")
    if request.method == "POST":
        if request.POST.get('mail'):
            Employee_Mail = request.POST.get('mail')
            username = request.POST.get('username')
            print(Employee_Mail)
            # return render(request,'index.html')
            otp = generate_otp()
            print("otp:",otp)
            database = Otp()
            send_mail(subject="OTP",message= f"Your otp {otp}",from_email="switchingtechsystem@gmail.com",recipient_list=[Employee_Mail],fail_silently=False)
            database.mail = Employee_Mail
            database.otp = otp
            database.username = username 
            check = Otp.objects.filter(mail=database.mail)
            if check.count() > 0:
                Otp.objects.filter(mail=database.mail).update(otp=database.otp,username=database.username)
            else:
                database.save()
            return render(request, 'validate.html')
    else:
        return render(request,'login.html')

def validate(request):
    context = {'categories': Category.objects.all()}
    if request.GET.get('category'):
        return redirect(f"/quiz/?category={request.GET.get('category')}")
    
    if request.method == 'POST':
        database = Otp()
        global mail
        mail = request.POST.get('mail')
        otp = request.POST.get('otp')
        print('validate:',mail)
        print('validate:',otp)
        sc= Otp.objects.filter(mail=mail,otp=otp)
        if sc:
            # return redirect('home')
            return render(request,'index.html',context)
        else:
            return render(request,'login.html')
    else:
        return render(request,'login.html')

# testing_otp_code

def logoutPage(request):
    logout(request)
    response = redirect('app.home.views.home')
    response.delete_cookie('user_location')
    return redirect('login')

@login_required(login_url='login')
def home(request):
    context = {'categories': Category.objects.all()}
    if request.GET.get('category'):
        return redirect(f"/quiz/?category={request.GET.get('category')}")
    return render(request,'index.html',context)

def quiz(request):
    context = {'category': request.GET.get('category')}
    return render(request,'quiz.html',context)

def get_quiz(request):
    try:
        questions_objs = Question.objects.all()
        if request.GET.get('category'):
            questions_objs = questions_objs.filter(category__category_name__icontains=request.GET.get('category'))
        questions_objs = list(questions_objs)
        data = []
        random.shuffle(questions_objs)
        counter = int()
        for question_obj in questions_objs:
            counter+=1
            if counter < 11:
                data.append({
                    "uid":question_obj.uid,
                    "category" : question_obj.category.category_name,
                    "question": question_obj.question,
                    "marks" : question_obj.marks,
                    "time": request.POST.get('timer'),
                    "answers": question_obj.get_answers()
                })
        return JsonResponse({'data': data,'status': True})
    except Exception as e:
        print(e)
    return HttpResponse("Something went worng")



def render_quiz(request, quiz_id):
    # quiz = get_object_or_404(Quiz, quiz_id)
    # form = QuizForm(questions=quiz.question_set.all())
    form = Question.objects.all()
    print(questions_objs)
    if request.GET.get('category'):
        questions_objs = questions_objs.filter(category__category_name__icontains=request.GET.get('category'))
    questions_objs = list(questions_objs)
    data = []
    random.shuffle(questions_objs)

    if request.method == "POST":
        form = QuizForm(request.POST, questions=quiz.question_set.all())
        if form.is_valid(): ## Will only ensure the option exists, not correctness.
            attempt = form.save()
            return redirect(attempt)
    return render('quiz.html', {"form": form})

# @login_required(login_url='login')
# def jotQuiz(request):
#     quiz_add = QuizUserScore()
#     if request.method == "POST":
#         quiz_add.user = User.objects.get(id = request.user.id)
#         quiz_add.quiz_domain = request.POST.get('q17_pleaseSelect')
#         quiz_add.score = request.POST.get('q21_totalScore')
#         quiz_add.save()
#     data = {
#         'score': request.POST.get('q21_totalScore')
#     }
#     return render(request,'results.html',context=data)
#     # return HttpResponse(f'<h1>Thank You! Your score is {quiz_add.score}!</h1>'
#     #                     '<h3>We will suggest some courses based on your score.</h3>')

score = 0
def result(request):
    if request.method == 'POST':
        score_data = json.loads(request.body)
    
        quiz_add = QuizUserScore()
        user = Otp()

        # username = User.objects.filter(id= request.user.id).values_list('username',flat=True)
        username = Otp.objects.filter(mail=mail).values_list('username',flat=True)
        new = list(username)
        print("check us:",new)
        update = new[0]
        print("this is usernmae:",update)
        # quiz_add.user = User.objects.get(id = request.user.id)
        global score        

        score = score_data.get('score')
        updated_score = score * 10
        print('Score received:', updated_score)
        quiz_add.user = update
        quiz_add.quiz_domain = 'TBD'
        # quiz_add.score = score_data.get('score')
        quiz_add.score = updated_score
        quiz_add.created_at = datetime.now()
        
        quiz_add.save()
        
        context = {'score': score}
        return HttpResponse(status=200)

def final(request):
    context = {
        "score":score * 10    }

    return render(request,'results.html',context=context)

score = 0
suggesstion_url = str()
def result(request):
    if request.method == 'POST':
        global score , suggesstion_url        
        score_data = json.loads(request.body)
        score = score_data.get('score')
        category = score_data.get('cateogry')
        print('Score received:', score * 10,'category:',category)
        if score < 50:
            print("Suggesting Begginer")
            suggesstion = CourseSuggession.objects.filter(technology__category_name__icontains=category, difficulty='BG')
            for val in suggesstion:
                suggesstion_url = val   
                break     
        elif score >= 50 < 70:
        # elif score>50 and score<80:
            print("Suggesting Intermediate")
            suggesstion = CourseSuggession.objects.filter(technology__category_name__icontains=category, difficulty='IN')
            for val in suggesstion:
                suggesstion_url = val 
                break       
        elif score >= 70 <= 100:
            print("Suggesting Advanced!")
            suggesstion  = CourseSuggession.objects.filter(technology__category_name__icontains=category, difficulty='AD')
            for val in suggesstion:
                suggesstion_url = val  
                break

        context = {'score': score,
                   'url':suggesstion_url}
        
        return HttpResponse(status=200)
    
def final(request):
    context = {
        "score":score * 10, 'suggested':suggesstion_url    }
    return render(request,'results.html',context=context)


# @csrf_exempt
# @login_required(login_url='login')
# def check_score(request):
#     data = json.loads(request.body)
#     user = request.user
#     course_id = data.get('course_id')
#     solutions = json.loads(data.get('data'))
#     course = Course.objects.get(id=course_id)
#     score = 0
#     for solution in solutions:
#         question = Question.objects.filter(id = solution.get('question_id')).first()
#         if (question.answer) == solution.get('option'):
#             score = score + question.marks
   
#     score_board = ScoreBoard(category = category , score = score  , user = user)
#     score_board.save() 
    
#     return JsonResponse({'message' : 'success' , 'status':True})
