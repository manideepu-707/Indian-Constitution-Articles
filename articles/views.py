from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import ContactMessage
from indianconstitution import IndianConstitution  # use Articles instead of IndianConstitution
india=IndianConstitution()
# Create your views here.
def home(request):
    return render(request, 'home.html')

def articles(request):
    query = request.GET.get('q')

    if query:
        # Search by keyword, returns a string (full article text)
        if query.isdigit():
            article_data=india.get_article(query)
            return render(request,'articles.html',{'articles':article_data})
        elif query.isalnum():
            article_data=india.get_article(query)
            return render(request, 'articles.html', {'articles': article_data})
        else:
            article_data=india.search_keyword(query)
            return render(request, 'articles.html', {'articles': article_data})
    else:
        # Get all articles as strings
        all_articles = india.articles_list()

    return render(request, 'articles.html', {'articles': all_articles})


def register_view(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email already used")
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password1,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                user.save()
                messages.info(request,'user created')
                return redirect('login')
        else:
            messages.info(request,"Passwords do not match")
        return redirect('register')
    else:
        return render(request, 'register.html')
    
def login_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('home')  # redirect to home page
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    else:
        return render(request, 'login.html')
def logout(request):
    auth.logout(request)
    return redirect('home')



def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        # Save to MySQL
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(request, "Your message has been saved in the database!")
        return redirect('contact')

    return render(request, 'contact.html')


