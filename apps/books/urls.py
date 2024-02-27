from django.urls import path

from .views import BookListView, BookDetailView, AddReviewView, review_delete

app_name = "books"

urlpatterns = [
    path('', BookListView.as_view(), name="book-list"),
    path('books/<slug:slug>/', BookDetailView.as_view(), name="book-detail"),
    path('<int:pk>', AddReviewView.as_view(), name="add-review"),
    path('review-delete/<int:pk>', review_delete, name="review-delete"),

]
