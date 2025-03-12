from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login 
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.views.decorators.http import require_POST

@login_required
def home(request):
	context = {
		'username': request.user
    }
	return render(request, 'index.html', context)


def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email').lower().strip()   
        password = request.POST.get('password')

        if not CustomUser.objects.filter(email=email).exists():  
            messages.error(request, 'خطا در شناسایی کاربر')
            return redirect('login')
            
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if user.is_active:
                if user.is_verified:
                    login(request, user)  
                    return redirect('/home/')
                else:
                    login(request, user) 
                    return redirect('complete_profile')
            else:
                messages.error(request, 'ایمیل تایید نشده است. لطفاایمیل خود را چک کنید')
            return redirect('login')
        else:
            messages.error(request, 'خطا در شناسایی کاربر')
            return redirect('login')
    
    return render(request, 'pages-login.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate until verified
            user.save()  
            
            token = user.generate_email_token()
            
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'token': token,
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()
            
            return redirect('verification_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



def verify_email(request, token):
    try:
        user = CustomUser.objects.get(email_token=token)
        if not user.is_active:
            user.is_active = True
            user.save()
            return redirect('verification_success')  # Redirect to successful verification
        else:
            return redirect('login')  # Already verified
    except CustomUser.DoesNotExist:
        return render(request, 'invalid_token.html')


@login_required
def  complete_profile(request):
    if not request.user.is_authenticated or not request.user.is_active:
        return redirect('login')
    
    if request.method == 'POST':
        form = ProfileCompletionForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            request.user.is_verified = True
            request.user.save()

            return redirect('home')
    else:
        form = ProfileCompletionForm(instance=request.user)
    return render(request, 'complete_profile.html', {'form': form})

    

def user_logout(request):
    logout(request) 
    return redirect('login')
