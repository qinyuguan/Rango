from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.models import BookDetail
from rango.models import Cart
from rango.models import Order
from rango.models import Comment
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm
from django.http import JsonResponse


def index(request):
    # TODO:- order by count of like
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


def product(request, book_detail_slug):
    context_dict = {}
    try:
        book = BookDetail.objects.get(slug=book_detail_slug)
        context_dict['book'] = book
        return render(request, 'rango/product.html', context=context_dict)
    except BookDetail.DoesNotExist:
        return redirect('rango:index')


def bought(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by("-date")
    ret = []
    for order in orders:
        book = order.book.first()
        temp_dict = {'book': book, 'order': order}
        ret.append(temp_dict)
    context_dict = {'orders': ret}
    print(context_dict)
    return render(request, 'rango/bought.html', context=context_dict)


def profile(request):
    return render(request, 'rango/profile.html')


def users(request):
    return render(request, 'rango/users.html')


def category(request, category_name):
    context_dict = {}
    context_dict['category_name'] = category_name
    return render(request, 'rango/category.html', context=context_dict)


def categories(request):
    # TODO- create new table for category, create slug name
    ret = set()
    context_dict = {}
    querySet = BookDetail.objects.all()
    for c in querySet:
        ret = ret.union(set(c.get_categories()))
    context_dict = {'categories': ret}
    return render(request, 'rango/categories.html', context=context_dict)


def admin_books(request):
    keyword = request.GET.get("keyword")
    if keyword != None and keyword != "":
        book_list = BookDetail.objects.filter(title__contains=keyword).order_by('title')[:20]
        context_dict = {'book_list': book_list, 'keyword':keyword}
        return render(request, 'rango/admin/books.html', context=context_dict)
    book_list = BookDetail.objects.order_by('title')[:20]
    context_dict = {'book_list': book_list}
    return render(request, 'rango/admin/books.html', context=context_dict)


def admin_add_books(request):
    return render(request, 'rango/admin/add_book.html')


def admin_edit_books(request, slug):
    if request.method == 'POST':
        id = request.POST.get('id')
        title = request.POST.get('title')
        author = request.POST.get('author')
        desc = request.POST.get('desc')
        img = request.POST.get('img')
        previous_title = request.POST.get('previous_title')
        # TODO: UPDATE CATEGORY
        category = request.POST.get('category')
        book = BookDetail.objects.get(id=id,title=previous_title)
        book.title = title
        book.author = author
        book.desc = desc
        book.img = img
        book.save()
        return JsonResponse({'code': 200, 'status': 'success', 'msg': 'Edit made successfully'})
    else:
        book = BookDetail.objects.get(slug=slug)
        context_dict = {'book': book}
        return render(request, 'rango/admin/edit_book.html', context=context_dict)


def admin_del_books(request,slug):
    book = BookDetail.objects.get(slug=slug)
    book.delete()
    return redirect('rango:admin_books')


def admin_categories(request):
    return render(request, 'rango/admin/categories.html')


def admin_add_categories(request):
    return render(request, 'rango/admin/add_categories.html')


def cart(request):
    ret = []
    total = 0
    cart = Cart.objects.filter(user=request.user)
    for c in cart:
        book = c.book.first()
        price = round(float(book.price[1:]) * c.num, 2)
        book.num = c.num
        book.price = book.price[:1] + str(price)
        total = round(total + price, 2)
        ret.append(book)
    context_dict = {"cart_list": ret, 'total': total}
    return render(request, 'rango/cart.html', context=context_dict)


def cart_add(request):
    if request.method == 'POST':
        slug = request.POST.get('slug')
        book = None
        cart = None
        try:
            book = BookDetail.objects.get(slug=slug)
        except BookDetail.DoesNotExist:
            return JsonResponse({'code': 500, 'status': 'failed', 'msg': 'Book invalid'})
        try:
            cart = Cart.objects.get(user=request.user, book=book)
        except Cart.DoesNotExist:
            print("Does Not Exist")
            cart = Cart(num=1)
            cart.save()
            cart.user.add(request.user)
            cart.book.add(book)
            cart.save()
            return JsonResponse({'code': 200, 'status': 'success', 'msg': 'Book was added to your basket'})
        cart.increment()
        cart.save()
        return JsonResponse({'code': 200, 'status': 'success', 'msg': 'Book was added to your basket'})


def cart_del(request):
    try:
        id = request.GET.get('id')
        book = BookDetail.objects.get(id=id)
        Cart.objects.get(user=request.user, book=book).delete()
    except:
        return HttpResponse("error")
    return redirect('rango:cart')


def cart_confirm(request):
    user = request.user
    carts = Cart.objects.filter(user=user)
    ret = []
    all_total = 0
    if (len(carts) == 0):
        return redirect("rango:cart")
    for cart in carts:
        book = cart.book.first()
        num = int(cart.num)
        price = round(float(book.price[1:]), 2)
        total = round(float(num * price), 2)
        all_total += total
        all_total = round(all_total,2)
        price = book.price[:1] + str(price)
        total = book.price[:1] + str(total)
        temp = {'book': book, 'num': num, 'price': price, 'total': total}
        ret.append(temp)

    context_dict = {'confirm': ret, 'all_total': all_total}
    return render(request, 'rango/confirm.html', context=context_dict)


def cart_pay(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name')
        tel = request.POST.get('tel')
        address = request.POST.get('address')
        carts = Cart.objects.filter(user=user)
        if (len(carts) == 0):
            return redirect("rango:cart")
        for cart in carts:
            book = cart.book.first()
            num = int(cart.num)
            price = round(float(book.price[1:]), 2)
            total = round(float(num * price), 2)
            price = book.price[:1] + str(price)
            total = book.price[:1] + str(total)
            order = Order(price=price, total_price=total, quantity=num, name=name, address=address, phone=tel,
                          date=datetime.now())
            order.save()
            order.user.add(user)
            order.book.add(book)
            order.save()
            cart.delete()
        return JsonResponse({'code': 200, 'status': 'success', 'msg': 'Book was added to your basket'})
    return JsonResponse({'code': 500, 'status': 'failed', 'msg': 'Method not support'})


def comment(request, order_no):
    if request.method == 'POST':
        content = request.POST.get('comment')
        try:
            order = Order.objects.get(order_no=order_no)
            book = order.book.first()
        except Order.DoesNotExist:
            return JsonResponse({'code': 500, 'status': 'failed', 'msg': 'Order Invalid'})

        comment = Comment(content=content, date=datetime.now())
        comment.save()
        comment.book.add(book)
        comment.save()
        order.isComment = 1
        order.save()
        return JsonResponse({'code': 200, 'status': 'success', 'msg': 'Comment made successfully'})


    else:
        try:
            order = Order.objects.get(order_no=order_no)
        except Order.DoesNotExist:
            return redirect('rango:bought')

        if order.isComment == 1:
            return redirect('rango:bought')

        book = order.book.first()
        context_dict = {'book': book, 'order_no': order_no}
        return render(request, 'rango/comment.html', context=context_dict)

def search(request):
    keyword = request.GET.get('keyword')
    book_list = BookDetail.objects.filter()
    context_dict = {'book_list': book_list}
    return render(request, 'rango/products.html', context=context_dict)