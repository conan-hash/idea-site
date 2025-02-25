from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def home(request):
	context = {
		'username': request.user
    }
	return render(request, 'index.html', context)


def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')  # Changed from 'username' to 'email'
        password = request.POST.get('password')

        # Check if user with email exists
        if not CustomUser.objects.filter(email=email).exists():  # Check email instead of username
            messages.error(request, 'Invalid Email')
            return redirect('login')
            
        # Authenticate using email instead of username
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            # Check if email is verified
            if user.is_verified:
                # Check if user is active
                if user.is_active:
                    auth_login(request, user)  # Use renamed auth_login to avoid conflict
                    return redirect('/home/')
                else:
                    messages.error(request, 'Account is disabled')
            else:
                messages.error(request, 'Email not verified. Please check your inbox.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid Password')
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
        if not user.is_verified:
            user.is_verified = True
            user.is_active = True  # Activate the user
            user.save()
            auth_login(request, user)
            return redirect('complete_profile')  # Redirect to profile completion
        else:
            return redirect('login')  # Already verified
    except CustomUser.DoesNotExist:
        return render(request, 'invalid_token.html')



def complete_profile(request):
    if not request.user.is_authenticated or not request.user.is_verified:
        return redirect('login')
    
    if request.method == 'POST':
        form = ProfileCompletionForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileCompletionForm(instance=request.user)
    return render(request, 'complete_profile.html', {'form': form})


class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        if not user.is_verified:
            # Log out unverified users
            form.get_user().auth_token.delete()  # Optional: Delete token if used
            return render(self.request, 'not_verified.html')
        return super().form_valid(form)