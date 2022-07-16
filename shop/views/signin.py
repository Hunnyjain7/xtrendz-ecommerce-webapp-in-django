import uuid
from django.core.checks import messages
from django.core.mail import send_mail
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from Xtrendz import settings
from shop.models.customer import Customer
from django.views import View


class Signin(View):
    def get(self, request):
        try:
            if request.session['customer']:
                return redirect('homepage')
        except:
            return render(request, 'signin.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                return redirect('homepage')
            else:
                error_message = "credential's invalid!!"
        else:
            error_message = "credential's invalid!!"
        print(email, password)
        return render(request, 'signin.html', {'error': error_message})


def send_forget_password_mail(email, token):
    subject = 'Your forget password link'
    message = f'Hi , click on the link to reset your password http://127.0.0.1:8000/change-password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


def ForgetPassword(request):
    try:
        if request.method == 'POST':
            Email = request.POST.get('email')

            if not Customer.objects.filter(email=Email):
                messages.success(request, 'No user found with this username.')
                return redirect('/forget-password/')

            user_obj = Customer.objects.get(email=Email)
            user_id = user_obj.id

            token = str(uuid.uuid4())
            profile_obj = Customer.objects.get(id=user_id)
            user_obj.forget_password_token = token
            user_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An email is sent.')
            return redirect('/forget-password/')



    except Exception as e:
        print(e)
    return render(request, 'forget-password.html')


def ChangePassword(request, token):
    context = {}
    #
    try:
        profile_obj = Customer.objects.filter(forget_password_token=token).get()
        context = {'user_id': profile_obj.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user_id = request.POST.get('id')

            if profile_obj is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')

            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')

            user_obj = Customer.objects.get(id=user_id)
            user_obj.password = make_password(user_obj.password)

            user_obj.save()

            return redirect('/signin/')
        return render(request, f'change-password.html/{token}/', context)

    except Exception as e:
        print(e)
        return render(request, 'change-password.html', context)


def logout(request):
    request.session.clear()
    return redirect('homepage')
