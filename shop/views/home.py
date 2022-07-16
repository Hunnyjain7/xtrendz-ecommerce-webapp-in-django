from django.shortcuts import render, redirect
from shop.models.product import Product
from shop.models.category import Category
from shop.models.edition import Edition
from django.views import View


# Create your views here.
class Index(View):
    def post(self, request):
        product = request.POST.get('product')
        print(product)
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        print(type(cart))
        customer = request.session.get('customer')
        print(customer)
        if cart:
            quantity = cart.get(product)
            print(quantity)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        return redirect('homepage')

    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}
        products = None
        categories = Category.get_all_categories()
        editions = Edition.get_all_editions()
        categoryID = request.GET.get('category')
        editionID = request.GET.get('edition')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        elif editionID:
            products = Product.get_all_products_by_editionid(editionID)
        else:
            products = Product.get_all_products()

        data = {}
        data['products'] = products
        data['categories'] = categories
        data['editions'] = editions
        return render(request, 'index.html', data)
