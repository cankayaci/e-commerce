from ckeditor_uploader.forms import SearchForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactForm, ContactFormMessage
from product.models import Product, Category, Images, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()[:4]
    category = Category.objects.all()
    dayproducts = Product.objects.all()[:4]
    lastproducts = Product.objects.all().order_by('-id')[:4]
    randomproducts = Product.objects.all().order_by('?')[:4]

    context = {'setting': setting, 'page': 'home', 'sliderdata': sliderdata, 'category': category,
               'dayproducts': dayproducts, 'lastproducts': lastproducts, 'randomproducts': randomproducts}
    return render(request, 'index.html', context)


def about(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'about.html', context)


def references(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'references.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            # *BEGIN

            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                data.ip = x_forwarded_for.split(',')[0]
            else:
                data.ip = request.META.get('REMOTE_ADDR')
            # *END

            data.save()  # save data to table
            messages.success(request, "Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    form = ContactForm()
    context = {'setting': setting, 'form': form}
    return render(request, 'contact.html', context)


def category_products(request, id, slug):
    products = Product.objects.filter(category_id=id)
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    context = {'products': products, 'category': category, 'categorydata': categorydata}
    return render(request, 'products.html', context)


def product_detail(request, id, slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    context = {'category': category, 'product': product, 'images': images, 'comments': comments}
    return render(request, 'product_detail.html', context)


def product_search(request):
    if request.method == 'POST':  # Check form post
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']  # get form input data
            products = Product.objects.filter(title__icontains=query)  # SELECT * FROM product WHERE title LIKE '%query%'
            context = {'category': category, 'products': products, 'query': query}
            return render(request, 'products_search.html', context)

        return HttpResponseRedirect('/')
