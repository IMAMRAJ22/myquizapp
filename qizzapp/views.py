from django.shortcuts import render,redirect,get_object_or_404
from .models import Userlogin,Statusbar,Quizz,Option,Admin
from django.contrib import messages
from typing import Any
from django.contrib.auth.decorators import login_required

# it is shows the index page 

def index(request):
    items = Statusbar.objects.all()
    return render(request, 'index.html', {'items': items})
    # return render(request,'index.html')
# this is shows the login page 
def login(request):
    if request.method=="POST":
        mail=request.POST.get('inserted_mail')
        paswrd=request.POST.get('inserted_pass')
        authorized_user=Userlogin.objects.filter(email=mail,password=paswrd)
        if authorized_user.exists():
            request.session['email']=mail
            request.session['password']=paswrd
            return redirect('section')
        else:
            messages.error(request,'Check email & password...')
    return render(request,'login.html')
# this is shows the signup page 
def signup(request):
    if request.method=="POST":
        mail=request.POST.get('inserted_mail')
        paswrd=request.POST.get('inserted_pass')
        con_pass=request.POST.get('inserted_conpass')
        authorized_user=Userlogin.objects.filter(email=mail)
        if authorized_user.exists():
            messages.error(request,'Email is already exists...')
        elif paswrd != con_pass:
            messages.error(request,'Please check Password')
        else:
            Userlogin.objects.create(email=mail,password=paswrd)
            return render(request,'login.html')
    return render(request,'signup.html')
# this is shows the quiz sections page 

def section(request):
    items = Statusbar.objects.all()
    return render(request, 'section.html', {'items': items})
# this is shows the quiz page 

def quiz(request):
    items = Statusbar.objects.all()
    ques = Quizz.objects.all()
    return render(request,'quiz_page.html',{'items': items,'ques':ques})

# this is shows all quiz in one-by-one per page
def quiz_navigation_view(request, section_id, question_number):
    section = get_object_or_404(Statusbar, id=section_id)
    quizzes = section.question.all().order_by('id')  # ensures consistent order
    total = quizzes.count()
    # this lines are show all quizz in one-by-one
    if question_number < 1 or question_number > total:
        return redirect('section')  # handle out-of-range

    quiz = quizzes[question_number - 1]
    options = quiz.options.all()

# Initialize session
    if 'answers' not in request.session:
        request.session['answers'] = {}

    if request.method == 'POST':
        selected_option_id = request.POST.get('answer')
        if selected_option_id:
            request.session['answers'][str(quiz.id)] = int(selected_option_id)
            request.session.modified = True

        if question_number == total:
            return redirect('quiz_result', section_id=section.id)

        return redirect('quiz_nav', section_id=section.id, question_number=question_number + 1)
    
    return render(request, 'quiz_page.html', {
        'section': section,
        'quiz': quiz,
        'options': options,
        'question_number': question_number,
        'total': total,
    })
# this is shows the result after finished quiz
def quiz_result(request, section_id):
    section = get_object_or_404(Statusbar, id=section_id)
    quizzes = section.question.all().order_by('id')
    answers = request.session.get('answers', {})

    # this is helps to calculate the quiz answers 
    score = 0
    results = []

    for quiz in quizzes:
        selected_id = answers.get(str(quiz.id))
        selected_option = Option.objects.filter(id=selected_id).first()
        correct_option = quiz.options.filter(is_correct=True).first()

        is_correct = selected_option and selected_option.is_correct

        if is_correct:
            score += 1
        

        results.append({
            'quiz': quiz.text,
            'your_answer': selected_option.option_text if selected_option else "Not Answered",
            'correct': correct_option.option_text if correct_option else "Not Available",
            'is_correct': is_correct,
        })

    total_questions = quizzes.count()
    percentage = round((score / total_questions) * 100, 2) if total_questions else 0

    # ✅ Save result only if session contains email
    email = request.session.get('email')
    

    if email:
        # Check if user already exists
        user = Userlogin.objects.filter(email=email,section=section).first()
        if user:
            user.quiz_mark = percentage
            user.save()
        else:
            # You can use placeholder password or set default if needed
            Userlogin.objects.create(email=email, quiz_mark=percentage,section=section)
    else:
        print("⚠️ Email not found in session. Result not saved.")

    request.session.pop('answers', None)


    return render(request, 'quiz_result.html', {
        'section': section,
        'score': score,
        'total': quizzes.count(),
        'results': results
    })

def admin_log(request):
    if request.method=='POST':
        mail=request.POST.get('inserted_mail')
        uname=request.POST.get('inserted_uname')
        ad_pass=request.POST.get('inserted_password')
        authorized_user=Admin.objects.filter(ad_email=mail)
        if authorized_user.exists():
            request.session['ad_email']=mail
            return redirect('table')
        else:
            messages.error(request,"Please check email & Password...")
    return render(request,'admin_login.html')

def table(request):
    email=Userlogin.objects.all()
    return render(request, 'details.html',{'email':email,'setion':email,'quiz_mark':email})