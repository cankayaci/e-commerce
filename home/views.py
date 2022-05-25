import json

from ckeditor_uploader.forms import SearchForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactForm, ContactFormMessage, FAQ
from product.models import Product, Category, Images, Comment
import logging

logger = logging.getLogger(__name__)


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()[:4]
    # category = Category.objects.all()
    dayproducts = Product.objects.all()[:4]
    lastproducts = Product.objects.all().order_by('-id')[:4]
    randomproducts = Product.objects.all().order_by('?')[:4]
    page = "home"

    context = {'setting': setting, 'page': 'home', 'sliderdata': sliderdata,  # 'category': category,
               'dayproducts': dayproducts, 'lastproducts': lastproducts, 'randomproducts': randomproducts, 'page': page}
    return render(request, 'index.html', context)


def about(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'about.html', context)


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


def search(request):
    if request.method == 'POST':  # Form post edildiyse
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = request.POST['query']  # Formdan bilgiyi al
            logger.info("query value is here {query}")
            catid = request.POST['catid']  # Formdan bilgiyi al
            logger.info("catid value is here {catid}")
            if catid == 0:
                products = Product.objects.filter(
                    title__icontains=query)  # Select * from product where title like %query%
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)
            context = {'products': products, 'category': category, 'query': query}
            return render(request, 'search_products.html', context)
    return HttpResponseRedirect('/')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)
        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.filter(status='True').order_by("ordernumber")
    context = {'category': category, 'faq': faq}
    return render(request, 'faq.html', context)
