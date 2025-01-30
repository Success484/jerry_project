from django.urls import path
from main_app import views

urlpatterns=[
    path('', views.homePage, name='home'),
    path('services/', views.servicePage, name='services'),
    path('about/', views.aboutPage, name='about'),
    path('contact/', views.contactPage, name='contact'),
    path('team/', views.teamPage, name='team'),
    path('account/user/profile/', views.user_profile, name='user_profile'),
    path('account/user/profile/details/', views.user_details, name='profile'),
    path('account/user/profile/details/transaction/', views.transaction_page, name='transaction_page'),
    path('account/user/profile/details/transaction/other/banks/', views.other_bank, name='other_bank'),
    path('account/user/profile/details/transaction/cross_border/transfer/', views.cross_border_transfer, name='cross_border_transfer'),
    path('account/user/profile/details/transaction/cross_border/transfer/success/', views.success_page, name='success_page'),
    path('account/user/profile/details/transaction/check/deposite/', views.check_deposite, name='check_deposite'),
    path('account/user/profile/details/transaction/summary/', views.summary, name='transfer_summary'),
    path('account/user/profile/details/transaction/pay_bill/', views.pay_bill, name='pay_bill'),
    path('account/user/profile/details/transaction/virtual_card/', views.virtual_card, name='virtual_card'),
    path('account/user/profile/details/transaction/support_page/', views.support_page, name='support_page'),
    path('account/user/profile/details/transaction/crypto_deposite/', views.crypto_deposite, name='crypto_deposite'),
    path('account/user/profile/details/transaction/loan/', views.loan, name='loan'),
    path('account/user/profile/details/transaction/kyc/', views.kyc, name='kyc'),
    path('account/user/profile/details/transaction/setting/', views.setting, name='setting'),
    path('register/', views.register_view, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('verify-pin/', views.verify_pin, name='verify_pin'),    
    path('logout/', views.logout_view, name='logout'),
]