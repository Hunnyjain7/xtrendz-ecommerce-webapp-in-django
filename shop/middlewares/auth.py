from django.shortcuts import redirect


def auth_middleware(get_response):
    print(get_response)

    def middleware(request):
        if not request.session.get('customer'):
            return redirect('signin')

        print('middleware')
        response = get_response(request)
        print(response)
        return response

    return middleware
