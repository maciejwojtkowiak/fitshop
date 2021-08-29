

class Cart():

    def __init__(self,request):
        self.session = request.session
        cart = request.session.get('cartkey')
        if 'cartkey' not in request.session:
            cart = self.session['cartkey'] = {}
        self.cart = cart
