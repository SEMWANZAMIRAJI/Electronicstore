from django.views.generic import TemplateView, ListView, View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Order
from urllib.parse import quote_plus

# inside your CartView.get_context_data:



class CartView(TemplateView):
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        cart_items = []
        total = 0
        whatsapp_message_lines = ["Hello, I want to order these products:"]

        for product_id, quantity in cart.items():
            product = Product.objects.get(pk=product_id)
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            whatsapp_message_lines.append(f"- {product.name} x {quantity}")

        whatsapp_message_lines.append(f"Total Price: ${total:.2f}")
        whatsapp_message_lines.append("Please confirm availability and shipping details. Thank you!")

        message_text = quote_plus("\n".join(whatsapp_message_lines))
        whatsapp_number = "255624313810"
        whatsapp_url = f"https://wa.me/{whatsapp_number}?text={message_text}"

        context['cart_items'] = cart_items
        context['total'] = total
        context['whatsapp_order_link'] = whatsapp_url
        return context



class HomeView(TemplateView):
    template_name = 'store/home.html'

class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'



class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1

        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
        request.session['cart'] = cart
        return redirect('cart')

class SubmitOrderView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def post(self, request):
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('product-list')

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, pk=product_id)
            Order.objects.create(user=request.user, product=product, quantity=quantity)

        request.session['cart'] = {}
        return redirect('product-list')

class SellerOrdersView(ListView):
    model = Order
    template_name = 'store/seller_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(product__seller=self.request.user).order_by('-ordered_at')
