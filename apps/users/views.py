from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from apps.books.models import Book, BookAuthor
from django.views.generic import CreateView, DetailView, TemplateView

from apps.users.forms import UserRegisterForm, UserLoginForm


class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, "users/register.html", context={"form": form})

    def post(self, request):
        create_form = UserRegisterForm(request.POST, request.FILES)
        if create_form.is_valid():
            create_form.save()
            return redirect("users:login-page")
        else:
            context = {
                "form": create_form
            }
            return render(request, "users/register.html", context=context)


class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, "users/login.html", context={"form": form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You have logged in as {username}")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password")
        else:
            return render(request, "users/login.html", {"form": form})


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "User successfully loged out")
        return redirect("home")


class AddAuthorView(CreateView):
    template_name = 'users/create_author.html'
    form_class = BookAuthor

    def get_context_data(self, **kwargs):
        context = super(AddAuthorView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = Book(self.request.POST)
        else:
            context['formset'] = Book()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.object.get_absolute_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class UserProfileView(TemplateView):
    template_name = 'users/user-profile.html'
