from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import SlugField
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from .forms import AddBookReviewForm
from .models import Book, BookAuthor, BookReview
from ..users.models import User

import smtplib
import ssl
from email.message import EmailMessage
import uuid
from django.conf import settings


class BookListView(View):
    def get(self, request):
        queryset = Book.objects.all()
        param = request.GET.get("q", None)

        if param is not None:
            queryset = queryset.filter(title__icontains=param)
        context = {
            "books": queryset,
            "param": param
        }
        return render(request, "books/book-list.html", context=context)


class BookDetailView(View):
    def get(self, request, slug):
        book = Book.objects.get(slug=slug)
        form = AddBookReviewForm()
        context = {
            "book": book,
            "form": form
        }
        return render(request, "books/book-detail.html", context=context)


EMAIL_HOST = 'smtp.gmail.com'


class AddReviewView(View):
    def post(self, request, pk):
        book = Book.objects.get(id=pk)
        print(request.user)
        user = User.objects.get(username=request.user.username)
        form = AddBookReviewForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data.get("body")
            rating = form.cleaned_data.get("rating")
            BookReview.objects.create(
                user=user,
                book=book,
                body=body,
                rating=rating
            )
            print(user, body, rating)
            self.send_admin_message(email=user.email, body=body, rating=rating)
            return redirect(reverse("books:book-detail", kwargs={"slug": book.slug}))

        else:
            context = {
                "book": book,
                "form": form
            }
            return render(request, "books/book-detail.html", context=context)

    def send_admin_message(self, email, body, rating):
        EMAIL = 'sh.yuldashbekov@gmail.com'  # Jo'natuvchi pochta manzili
        EMAIL_PASSWORD = 'mflucdiebxcphklh'  # Jo'natuvchi pochta paroli
        msg = f"{body}  {rating}"
        # print(EMAIL_HOST,rating)
        em = EmailMessage()
        em['Message-ID'] = str(uuid.uuid4())
        em['From'] = EMAIL_HOST
        em['To'] = EMAIL
        em.set_content(msg)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(EMAIL_HOST, 465, context=context) as smtp:
            smtp.login(EMAIL, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL, email, em.as_string())


class AddBookView(View):
    def post(self, request, pk):
        pass


@login_required()
def review_delete(request, pk):
    review = get_object_or_404(BookReview, pk=pk)
    if request.method == "POST":
        messages.success(request, "post successfully deleted")
        review.delete()
        return redirect(reverse('users:user-profile', kwargs={"username": request.user.username}))
    else:
        return render(request, "books/delete-review.html", {"review": review})
