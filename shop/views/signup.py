from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from shop.models.customer import Customer
from django.views import View
from Xtrendz import settings
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from shop.tokens import generate_token
from shop.views.signin import Signin


class Signup(View):
    def get(self, request):
        try:
            if request.session['customer']:
                return redirect('homepage')
        except:
            return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        email = postData.get('email')
        password = postData.get('pass1')

        value = {
            'first_name': first_name, 'last_name': last_name, 'email': email
        }

        error_message = None

        customer = Customer(first_name=first_name, last_name=last_name, email=email, password=password)

        error_message = self.validateCustomer(customer)

        if not error_message:

            subject = "Welcome to Xtrendz!"
            message = "Hello!! \n\n" + "Welcome to Xtendz \n Thank you for visiting our Website."
            from_email = settings.EMAIL_HOST_USER
            to_list = [customer.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)

            # Email Address Confirmation Email
            current_site = get_current_site(request)
            email_subject = "Confirm your Email @ Xtrendz!!"
            message2 = render_to_string('email_confirmation.html', {

                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(customer.pk)),
                'token': generate_token.make_token(customer)
            })
            email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [customer.email],
            )
            email.fail_silently = True
            email.send()

            customer.password = make_password(customer.password)

            customer.register()

            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None;

        if (not customer.first_name):
            error_message = "First Name is Required !!"
        elif len(customer.first_name) < 3:
            error_message = 'First Name must be more than 3 char'
        elif not customer.last_name:
            error_message = "Last Name is Required !!"
        elif len(customer.last_name) < 3:
            error_message = 'Last Name must be more than 3 char'
        elif not customer.email:
            error_message = "Email is Required !!"
        elif customer.isExists():
            error_message = 'Email is already Registered..'
        elif not customer.password:
            error_message = "Password is Required !!"
        elif len(customer.password) < 3:
            error_message = 'Password must be more than 3 char'

        return error_message


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        customer = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        customer = None

    if customer is not None and generate_token.check_token(customer, token):
        customer.is_active = True
        # user.profile.signup_confirmation = True
        customer.save()
        Signin(request, customer)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request, 'index.html')
