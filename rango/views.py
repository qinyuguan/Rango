from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.models import BookDetail
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm


def index(request):
    #TODO:- order by count of like
    book_list = BookDetail.objects.order_by('title')[:20]
    context_dict = {'book_list': book_list}
    visitor_cookie_handler(request)
    response = render(request, 'rango/index.html', context=context_dict)
    return response


def about(request):
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'rango/about.html', context_dict)


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)


@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():

            form.save(commit=True)
            return redirect('/rango')
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category',
                                        kwargs={'category_name_slug':
                                                    category_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'rango/register.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')



@login_required()
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    print(last_visit_cookie)
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits


def products(request):
    book_list = BookDetail.objects.order_by('title')[:20]
    context_dict = {'book_list': book_list}
    return render(request, 'rango/products.html', context=context_dict)


def product(request,book_detail_slug):
    context_dict = {}
    try:
        book = BookDetail.objects.get(slug=book_detail_slug)
        context_dict['book'] = book
        return render(request, 'rango/product.html', context=context_dict)
    except BookDetail.DoesNotExist:
        return redirect('rango:index')


def bought(request):
    return render(request, 'rango/bought.html')


def profile(request):
    return render(request, 'rango/profile.html')


def users(request):
    return render(request, 'rango/users.html')


def cart(request):
    return render(request, 'rango/cart.html')

def comment(request):
    return render(request, 'rango/comment.html')

def category(request, category_name):
    context_dict = {}
    context_dict['category_name'] = category_name
    return render(request, 'rango/category.html', context=context_dict)

def categories(request):
    return render(request, 'rango/categories.html')

def admin_books(request):
    return render(request, 'rango/admin/books.html')

def admin_add_books(request):
    return render(request, 'rango/admin/add_book.html')


def admin_categories(request):
    return render(request, 'rango/admin/categories.html')

def admin_add_categories(request):
    return render(request, 'rango/admin/add_categories.html')