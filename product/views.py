from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from product.models import CommentForm, Comment


def index(request):
    return HttpResponse("Product Page")


@login_required(login_url='/login')
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':  # check post
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user  # Access User Session information
            data = Comment()  # create relation with model
            data.user_id = current_user.id
            data.product_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table
            messages.success(request, "Your review has ben sent. Thank you for your interest.")
            return HttpResponseRedirect(url)

        messages.warning(request, "Your comment has not been saved. Please try again.")
        return HttpResponseRedirect(url)
