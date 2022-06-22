from pydoc import render_doc
from django.shortcuts import redirect, render 
from django.http import HttpResponse
from .models import Product
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse,reverse_lazy
from django.core.paginator import Paginator
from django.http.response import HttpResponseNotFound , JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import Settings 
from django.views.decorators.csrf import csrf_exempt 
import json 
# Create your views here.
def index(request):
    return HttpResponse("Hey children of God")

def products(request):
    page_obj = products =Product.objects.all()
    product_name = request.GET.get('product_name')
    if product_name != '' and product_name is not None:
        page_obj = products.filter(name__icontains = product_name)
    paginator = Paginator(page_obj, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request , 'myapp/index.html' , context)

#class based view for above products view(List view)
class Product_list_view(ListView):
    model = Product
    template_name = 'myapp/index.html'
    context_object_name = 'products'
    paginate_by = 3
def product_details(request ,id):
    product = Product.objects.get(id = id)
    context = {'product' : product}
    return render(request , 'myapp/detail.html', context)

#class based  view for above details view(DetailView)
class Product_detail_view(DetailView):
    model = Product
    template_name = 'myapp/detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'pk'

    # def get_context_data(self, **kwargs):
    #     context = super(Product_detail_view,self).get_context_data(**kwargs)
    #     context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
    #     return context
@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price= request.POST.get('price')
        desc = request.POST.get('desc')
        image = request.FILES['upload']
        seller_name = request.user
        product= Product(name = name , price = price , desc = desc, image = image, seller_name = seller_name)
        product.save()
    return render(request , 'myapp/addproducts.html')

#class based view for creating a product 
class Product_create_view(CreateView):
    model = Product
    fields = ['name','price','desc','image','seller_name']
def update_product(request , id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price= request.POST.get('price')
        product.desc = request.POST.get('desc')
        product.image = request.FILES['upload']
        product.save()
        return redirect('/products/')
    context ={
        'product': product
    }
    return render(request , 'myapp/updateproducts.html' , context)

#class based view for updating a product
class Product_update_view(UpdateView):
    model = Product
    fields = ['name','price','desc','image','seller_name']
    template_name_suffix = '_update_form'

def delete_product(request , id):
    product = Product.objects.get(id=id)
    context = {
        'product': product
    }
    if request.method == 'POST':
        product.delete()
        return redirect('/products/')
    return render(request , 'myapp/delete.html' , context)
#class based view
class Product_delete(DeleteView):
    model = Product
    success_url = reverse_lazy('myapp:products')
def my_listings(request):
    products = Product.objects.filter(seller_name = request.user)
    context = {
        'products' : products,
    }
    return render(request , 'myapp/mylistings.html' , context)

# @csrf_exempt
# def create_checkout_section(request , id):
#     product = get_object_or_404(Product , pk = id)
#     stripe.api_key =settings.stripe_secret_key
#     checkout_session = stripe.checkout.Session.create(
#         customer_email = request.user.email,
#         payment_method_types = ['card'],
#         line_items = [
#             {
#                 'price-data':{
#                     'currency': 'usd',
#                     'product_data':{
#                         'name': product.name ,
#                     },
#                     'unit_amount': int(product.price*100),
#                 },
#                 'quantity': 1,
#             }
#             ],
#             mode = 'payment',
#             success_url = request.build_absolute_url(reverse('myapp:success'))+'?session_id ={CHECKOUT_SESSION_ID}',
#             cancel_url = request.build_absolute_url(reverse('myapp:failed')),
#     )