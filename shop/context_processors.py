from .cart import Cart

def session(request):
    return {'cart': Cart(request)}