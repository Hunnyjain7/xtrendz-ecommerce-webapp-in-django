from django.contrib import admin
from django.urls import path
from .views.home import Index
from .views.signup import Signup, activate
from .views.signin import Signin, logout, ForgetPassword, ChangePassword
from .views.cart import Cart
from .views.checkout import Checkout
from .views.orders import OrderView
from .views.product import Prod

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('signup', Signup.as_view(), name='signup'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('signin', Signin.as_view(), name='signin'),
    path('logout', logout, name='logout'),
    path('cart', Cart.as_view(), name='cart'),
    path('checkout', Checkout.as_view(), name='checkout'),
    path('orders', OrderView.as_view(), name='orders'),
    path('product', Prod.as_view(), name='prod'),
    path('forget-password', ForgetPassword, name='forget-password'),
    path('change-password/<token>/', ChangePassword, name='change-password'),

    

]
