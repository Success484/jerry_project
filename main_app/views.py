from django.db import IntegrityError
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, TransferForm, MessageForm
from django.contrib import messages
from .models import Profile, Transfer, Chatbox
from django.core.paginator import Paginator
from django.utils.crypto import get_random_string
from django.contrib.auth.views import LoginView
from django.conf import settings
from .models import UserProfile, IMFVerification
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.humanize.templatetags.humanize import intcomma


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
    return render(request, 'main/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def user_profile(request):
    user_profile = Profile.objects.filter(user=request.user)
    formatted_amount = intcomma(int(user_profile.amount))
    context = {
        "formatted_amount": formatted_amount,
        'user_profile': user_profile,
    }
    return render(request, 'main/profile.html', context)

@login_required
def user_details(request):
    tranfers = Transfer.objects.filter(user=request.user).order_by('-transfer_date')[:4]
    user_profile = Profile.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    formatted_amount = intcomma(int(profile.amount))
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
        "formatted_amount": formatted_amount,
    }
    return render(request, 'main/profile_dashboard.html', context)


# @login_required
# def transaction_page(request):
#     """Handles the transaction process, deferring transaction save until IMF verification"""
#     u_profile = Profile.objects.get(user=request.user)
#     user_profile = Profile.objects.filter(user=request.user)
#     formatted_amount = intcomma(int(u_profile.amount))

#     if request.method == 'POST':
#         form = TransferForm(request.POST)
#         if form.is_valid():
#             transaction_data = form.cleaned_data
#             transaction_amount = transaction_data['amount']
#             account_number = transaction_data['account_number']
#             bank_name = transaction_data['bank_name']
#             description = transaction_data['description']

#             # Check if the user has enough balance
#             if transaction_amount > u_profile.amount:
#                 form.add_error('amount', "Insufficient balance.")
#             # Check transaction PIN
#             elif transaction_data['transaction_pin'] != u_profile.profile_pin:
#                 form.add_error('transaction_pin', "Incorrect transaction PIN.")
#             else:
#                 # Deduct the amount
#                 u_profile.amount -= transaction_amount
#                 u_profile.save()

#                 # Save the transaction
#                 transaction = form.save(commit=False)
#                 transaction.user = request.user
#                 transaction.save()

#                 # Send confirmation email
#                 formatted_amount = f"{intcomma(transaction_amount)}"
#                 subject = "Transaction Successful - Floxix Bank"
#                 html_message = render_to_string('main/transaction_email.html', {
#                     'user': request.user,
#                     'amount': formatted_amount,
#                     'account_number': account_number,
#                     'bank_name': bank_name,
#                     'description': description,
#                 })
#                 plain_message = strip_tags(html_message)  # Convert HTML to plain text

#                 email = EmailMultiAlternatives(
#                     subject,
#                     plain_message,
#                     settings.DEFAULT_FROM_EMAIL,
#                     [request.user.email]
#                 )
#                 email.attach_alternative(html_message, "text/html")
#                 email.send()

#                 messages.success(request, "Transaction successful! A confirmation email has been sent.")
#                 return redirect('success_page')
#     else:
#         form = TransferForm()

#     context = {
#         'form': form, 
#         'u_profile': u_profile,
#         'user_profile': user_profile,
#         "formatted_amount": formatted_amount,
#     }
#     return render(request, 'main/transaction_page.html', context)




@login_required
def transaction_page(request):
    """Handles the transaction process, deferring transaction save until IMF verification"""
    u_profile = Profile.objects.get(user=request.user)
    user_profile = Profile.objects.filter(user=request.user)
    formatted_amount = intcomma(int(u_profile.amount))

    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            transaction_data = form.cleaned_data
            transaction_amount = transaction_data['amount']
            account_number = transaction_data['account_number']
            bank_name = transaction_data['bank_name']
            description = transaction_data['description']

            # Check if the user has enough balance
            if transaction_amount > u_profile.amount:
                form.add_error('amount', "Insufficient balance.")
            # Check transaction PIN
            elif transaction_data['transaction_pin'] != u_profile.profile_pin:
                form.add_error('transaction_pin', "Incorrect transaction PIN.")
            else:
                # Deduct the amount
                u_profile.amount -= transaction_amount
                u_profile.save()

                # Save the transaction
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()

                # Send confirmation email
                formatted_amount = f"{intcomma(transaction_amount)}"
                subject = "Transaction Successful - Floxix Bank"
                html_message = render_to_string('main/transaction_email.html', {
                    'user': request.user,
                    'amount': formatted_amount,
                    'account_number': account_number,
                    'bank_name': bank_name,
                    'description': description,
                })
                plain_message = strip_tags(html_message)  # Convert HTML to plain text

                email = EmailMultiAlternatives(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email]
                )
                email.attach_alternative(html_message, "text/html")
                email.send()

                messages.success(request, "Transaction successful! A confirmation email has been sent.")
                return redirect('success_page')
    else:
        form = TransferForm()

    context = {
        'form': form, 
        'u_profile': u_profile,
        'user_profile': user_profile,
        "formatted_amount": formatted_amount,
    }
    return render(request, 'main/transaction_page.html', context)




@login_required
def verify_imf(request):
    """Handles IMF verification and completes the transaction"""
    try:
        user_profile = Profile.objects.filter(user=request.user)
        profile = Profile.objects.get(user=request.user)
        imf_record = IMFVerification.objects.filter(user=request.user).first()

        if not imf_record:
            messages.error(request, "IMF verification record not found.")
            return redirect("transaction_page")

    except Profile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect("transaction_page")

    if request.method == "POST":
        entered_imf = request.POST.get("imf_code")

        print(f"Stored IMF Code: {imf_record.imf_code}, Entered IMF Code: {entered_imf}")  # Debugging

        if str(imf_record.imf_code).strip() == str(entered_imf).strip():
            # Retrieve transaction data from session
            transaction_data = request.session.get('pending_transfer_data')

            if transaction_data:
                try:
                    account_number = transaction_data.get("account_number")
                    amount = int(transaction_data.get("amount", 0))  # Ensure integer conversion
                    transaction_pin = transaction_data.get("transaction_pin")
                    bank_name = transaction_data.get("bank_name")
                    description = transaction_data.get("description")

                    if not all([account_number, amount, transaction_pin, bank_name]):
                        messages.error(request, "Invalid transaction data.")
                        return redirect("transaction_page")

                    # 🔥 FIXED: Convert profile.amount properly
                    profile_balance = int(float(str(profile.amount).replace(",", "").strip()))

                    if amount > 0 and profile_balance >= amount:
                        profile.amount = str(profile_balance - amount)  # Deduct amount and save as string
                        profile.save()

                        # Create and save the Transfer object
                        Transfer.objects.create(
                            user=request.user,
                            account_number=account_number,
                            amount=amount,
                            transaction_pin=transaction_pin,
                            bank_name=bank_name,
                            description=description,
                        )

                        # Remove transaction data from session safely
                        request.session.pop("pending_transfer_data", None)

                        # Clear IMF code after successful verification
                        imf_record.imf_code = ""  # Consider generating a new code instead
                        imf_record.is_verified = True
                        imf_record.save()

                        # Send confirmation email
                        formatted_amount = f"{intcomma(amount)}"
                        subject = "Transaction Successful - Floxix Bank"
                        html_message = render_to_string('main/transaction_email.html', {
                            'user': request.user,
                            'amount': formatted_amount,
                            'account_number': account_number,
                            'bank_name': bank_name,
                            'description': description,
                        })
                        plain_message = strip_tags(html_message)  # Convert HTML to plain text

                        email = EmailMultiAlternatives(
                            subject,
                            plain_message,
                            settings.DEFAULT_FROM_EMAIL,
                            [request.user.email]
                        )
                        email.attach_alternative(html_message, "text/html")
                        email.send()

                        messages.success(request, "Transaction successful!")
                        return redirect("success_page")

                    else:
                        messages.error(request, "Insufficient funds.")
                except ValueError:
                    messages.error(request, "Invalid amount format.")
            else:
                messages.error(request, "No pending transaction found.")
        else:
            messages.error(request, "Invalid IMF code. Please try again.")

    return render(request, "main/verify_imf.html", {'user_profile': user_profile})



@login_required
def success_page(request):
    user_profile = Profile.objects.filter(user=request.user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'main/success_page.html', context)


@login_required
def summary(request):
    tranfers_list = Transfer.objects.filter(user=request.user).order_by('-transfer_date')
    paginator = Paginator(tranfers_list, 5)
    page_number = request.GET.get('page')
    tranfers = paginator.get_page(page_number)
    user_profile = Profile.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    formatted_amount = intcomma(int(profile.amount))
    context = {
        'user_profile': user_profile,
        'tranfers': tranfers,
        "formatted_amount": formatted_amount,
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
    u_profile = Profile.objects.get(user=request.user)
    context = {
        'user_profile': user_profile,
        'u_profile': u_profile
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
    u_profile = Profile.objects.get(user=request.user)
    context = {
        'user_profile': user_profile,
        'u_profile': u_profile
    }
    return render(request, 'main/loan.html', context)


@login_required
def setting(request):
    user_profile = Profile.objects.filter(user=request.user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'main/settings.html', context)