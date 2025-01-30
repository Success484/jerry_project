from django.db import IntegrityError
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, TransferForm, MessageForm
from django.contrib import messages
from .models import Profile, Transfer, Chatbox
from django.core.paginator import Paginator
from django.utils.crypto import get_random_string
from django.contrib.auth.views import LoginView
from django.conf import settings
from .models import UserProfile 
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.
def homePage(request):
    return render(request, 'main/index.html')

def servicePage(request):
    return render(request, 'main/services.html')

def aboutPage(request):
    return render(request, 'main/about.html')

def contactPage(request):
    return render(request, 'main/contact.html')

def teamPage(request):
    return render(request, 'main/team.html')

class CustomLoginView(LoginView):
    template_name = 'main/login.html'

    def form_valid(self, form):
        """Override login success behavior to send PIN and redirect to verification."""
        response = super().form_valid(form)  # Logs in the user
        user = self.request.user

        # Generate a 6-digit PIN
        pin_code = get_random_string(length=6, allowed_chars="0123456789")

        # Save the PIN to UserProfile
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.pin_code = pin_code
        user_profile.save()

        # Render HTML email template
        subject = "Your Floxix Login Verification Code"
        html_message = render_to_string('main/pin_email.html', {'pin_code': pin_code, 'user': user})
        plain_message = strip_tags(html_message)  # Extract plain text version

        # Send email
        email = EmailMultiAlternatives(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send()

        return redirect('verify_pin')


@login_required
def verify_pin(request):
    """View for verifying PIN after login."""
    if request.method == "POST":
        entered_pin = request.POST.get("pin")
        user_profile = UserProfile.objects.get(user=request.user)

        if user_profile.pin_code == entered_pin:
            user_profile.pin_code = None
            user_profile.save()
            return redirect("profile")
        else:
            messages.error(request, "Invalid PIN. Please try again.")

    return render(request, "main/verify_pin.html")


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def user_profile(request):
    user_profile = Profile.objects.filter(user=request.user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'main/profile.html', context)

@login_required
def user_details(request):
    tranfers = Transfer.objects.filter(user=request.user).order_by('-transfer_date')[:4]
    user_profile = Profile.objects.filter(user=request.user)
    all_messages = Chatbox.objects.filter(user=request.user)
    unread_count = Chatbox.objects.filter(user=request.user, seen=False).count()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            Chatbox.objects.filter(user=request.user, seen=False).update(seen=True)
            return redirect('profile')
    unread_count_seen = Chatbox.objects.filter(user=request.user, seen=True)
    context = {
        'user_profile': user_profile,
        'all_messages': all_messages,
        'unread_count': unread_count,
        'tranfers': tranfers,
        'unread_count_seen': unread_count_seen,
    }
    return render(request, 'main/profile_dashboard.html', context)


@login_required
def transaction_page(request):
    u_profile = Profile.objects.get(user=request.user)
    user_profile = Profile.objects.filter(user=request.user)
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.user = request.user

            if transfer.transaction_pin != u_profile.profile_pin:
                form.add_error('transaction_pin', "Incorrect transaction PIN.")
            else:
                try:
                    transfer.save()               
                    messages.success(request, "Transfer successful!")
                    return redirect('success_page')    
                except IntegrityError:
                    form.add_error(None, "An error occurred while saving the transaction.")
    else:
        form = TransferForm()
    context = {
        'form': form,
        'user_profile': user_profile,
        'u_profile': u_profile
    }
    return render(request, 'main/transaction_page.html', context)

@login_required
def success_page(request):
    return render(request, 'main/success_page.html')


@login_required
def summary(request):
    tranfers_list = Transfer.objects.filter(user=request.user).order_by('-transfer_date')
    paginator = Paginator(tranfers_list, 5)
    page_number = request.GET.get('page')
    tranfers = paginator.get_page(page_number)
    user_profile = Profile.objects.filter(user=request.user)
    context = {
        'user_profile': user_profile,
        'tranfers': tranfers,
    }
    return render(request, 'main/summary.html', context)


@login_required
def other_bank(request):
    user_profile = Profile.objects.filter(user=request.user)
    u_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.user = request.user

            if transfer.transaction_pin != u_profile.profile_pin:
                form.add_error('transaction_pin', "Incorrect transaction PIN.")
            else:
                try:
                    transfer.save()               
                    messages.success(request, "Transfer successful!")
                    return redirect('success_page')    
                except IntegrityError:
                    form.add_error(None, "An error occurred while saving the transaction.")
    else:
        form = TransferForm()
    context = {
        'user_profile': user_profile,
        'u_profile': u_profile
    }
    return render(request, 'main/other_bank.html', context)


@login_required
def cross_border_transfer(request):
    user_profile = Profile.objects.filter(user=request.user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'main/cross_border.html', context)


@login_required
def check_deposite(request):
    user_profile = Profile.objects.filter(user=request.user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'main/check_deposite.html', context)


@login_required
def pay_bill(request):
    user_profile = Profile.objects.filter(user=request.user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'main/pay_bill.html', context)


@login_required
def virtual_card(request):
    user_profile = Profile.objects.filter(user=request.user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'main/virtual_card.html', context)


@login_required
def support_page(request):
    user_profile = Profile.objects.filter(user=request.user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'main/support.html', context)


@login_required
def crypto_deposite(request):
    user_profile = Profile.objects.filter(user=request.user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'main/crypto_deposite.html', context)


@login_required
def kyc(request):
    user_profile = Profile.objects.filter(user=request.user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'main/kyc.html', context)


@login_required
def loan(request):
    user_profile = Profile.objects.filter(user=request.user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'main/loan.html', context)


@login_required
def setting(request):
    user_profile = Profile.objects.filter(user=request.user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'main/settings.html', context)