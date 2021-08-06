import json
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

from rango.models import Category, Like
from rango.models import BookDetail
from rango.models import Cart
from rango.models import Order
from rango.models import Comment
from rango.forms import UserForm, UserProfileForm
from django.http import JsonResponse
from rango.permissions import user_required, admin_required
from django.contrib.auth.models import User

def index(request):
    book_list = BookDetail.objects.order_by('title')[:20]
    context_dict = {'book_list': book_list}
    response = render(request, 'rango/index.html', context=context_dict)
    return response


@csrf_protect
def register(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        if username == None or username == '':
            return render(request, 'rango/register.html', context={'err_msg':'Username cannot be empty.'})

        password = request.POST.get("password")
        if password == None or password == '':
            return render(request, 'rango/register.html', context={'err_msg':'Password cannot be empty.'})

        repeat_pass = request.POST.get("password_confirm")
        if password != repeat_pass:
            return render(request, 'rango/register.html', context={'err_msg':'The passwords you entered were '
                                                                             'inconsistent'})

        user = User()
        user.set_password(password)
        user.username = username
        user.save()
        return render(request, 'rango/register.html', context={'success_msg':'You have registered successfully.'})
    return render(request, 'rango/register.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('rango:index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username==None or username=="":
            return render(request, 'rango/login.html', context={'err_msg':'Username cannot be empty.'})
        if password==None or password=="":
            return render(request, 'rango/login.html', context={'err_msg':'Password cannot be empty.'})
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return render(request, 'rango/login.html', context={'err_msg':'Your account is disabled.'})
        else:
            return render(request, 'rango/login.html', context={'err_msg': 'Invalid account, please check.'})
    else:
        return render(request, 'rango/login.html')


@login_required()
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


@login_required()
def change_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if password==None or password=="":
            return render(request, 'rango/profile.html', context={'err_msg':'Previous Password cannot be empty.'})
        password_new = request.POST.get('password_new')
        if password_new==None or password_new=="":
            return render(request, 'rango/profile.html', context={'err_msg':'New Password cannot be empty.'})
        password_confirm = request.POST.get('password_confirm')
        if password_confirm!=password_new:
            return render(request, 'rango/profile.html', context={'err_msg': 'The passwords you entered were inconsistent'})

        user = authenticate(username=request.user.username, password=password)
        if user:
            user.set_password(password_new)
            user.save()
            return render(request, 'rango/profile.html', context={'err_msg': 'Password changed successfully.'})
        else:
            return render(request, 'rango/profile.html', context={'err_msg': 'Password incorrect.'})

    else:
        return render(request, 'rango/profile.html', context={'err_msg': 'Method not supported.'})



def products(request):
    keyword = request.GET.get('keyword')
    if keyword != None and keyword != "":
        book_list = list(BookDetail.objects.filter(title__contains=keyword).order_by('title')[:20])
        context_dict = {'book_list': book_list, 's_keyword': keyword, 'page':1}
        return render(request, 'rango/products.html', context=context_dict)

    book_list = BookDetail.objects.order_by('title')[:20]
    context_dict = {'book_list': book_list,'page':1}
    return render(request, 'rango/products.html', context=context_dict)


@user_required(ajax=True)
def like(request):
    if request.method == 'POST':
        book_id = request.POST.get("id")
        book = BookDetail.objects.get(id=book_id)
        flag = request.POST.get("flag")
        user = request.user
        like = Like.objects.get(book=book)
        if flag == '1':
            like.user.add(user)
            like.save()
        else:
            like.user.remove(user)
            like.save()
        return JsonResponse({'code':200,'status':'success','msg':'Success'})
    return JsonResponse({'code':500,'status':'failed','msg':'Method Invalid'})

def product(request, book_detail_slug):
    context_dict = {}
    try:
        book = BookDetail.objects.get(slug=book_detail_slug)
        like = Like.objects.get_or_create(book=book)[0]
        context_dict['likes'] = len(list(like.user.all()))
        context_dict['book'] = book
        likes_user_list = list(like.user.all())
        if request.user in likes_user_list:
            context_dict['like_flag'] = True
        else:
            context_dict['like_flag'] = False
        return render(request, 'rango/product.html', context=context_dict)
    except BookDetail.DoesNotExist:
        return redirect('rango:index')


@user_required()
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


@login_required
def profile(request):
    return render(request, 'rango/profile.html')


@admin_required()
def users(request):
    return render(request, 'rango/users.html')


def category(request, category_name):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name)
        book_list = BookDetail.objects.filter(categories__name__contains=category)
        context_dict['book_list'] = book_list
    except Category.DoesNotExist:
        context_dict['category_name'] = category_name
        return render(request, 'rango/category.html', context=context_dict)

    context_dict['category_name'] = category_name
    return render(request, 'rango/category.html', context=context_dict)


def categories(request):
    category_list = list(Category.objects.all()[:20])
    context_dict = {'category_list': category_list}
    return render(request, 'rango/categories.html', context=context_dict)


@admin_required()
def admin_books(request):
    keyword = request.GET.get("keyword")
    if keyword != None and keyword != "":
        book_list = BookDetail.objects.filter(title__contains=keyword).order_by('title')[:20]
        context_dict = {'book_list': book_list, 'keyword': keyword}
        return render(request, 'rango/admin/books.html', context=context_dict)
    book_list = BookDetail.objects.order_by('title')[:20]
    context_dict = {'book_list': book_list}
    return render(request, 'rango/admin/books.html', context=context_dict)


@admin_required()
def admin_add_books(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        desc = request.POST.get('desc')
        img = request.POST.get('img')
        category_id = request.POST.get('category')
        categories = Category.objects.get(id=category_id)

        book = BookDetail(title=title, author=author, img=img, desc=desc, category=categories.name)
        book.title = title
        book.author = author
        book.desc = desc
        book.img = img
        book.save()
        book.category.add(categories)
        book.save()
        return JsonResponse({'code': 200, 'status': 'success', 'msg': 'Add made successfully'})
    else:
        return render(request, 'rango/admin/add_book.html', context={'category_list': Category.objects.all()})


@admin_required()
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
        book = BookDetail.objects.get(id=id, title=previous_title)
        book.title = title
        book.author = author
        book.desc = desc
        book.img = img
        book.save()
        return JsonResponse({'code': 200, 'status': 'success', 'msg': 'Edit made successfully'})
    else:
        book = BookDetail.objects.get(slug=slug)
        current_category = book.categories.first().id
        context_dict = {'book': book, 'category_list': Category.objects.all(), 'current_category': current_category}
        return render(request, 'rango/admin/edit_book.html', context=context_dict)


@admin_required()
def admin_del_books(request, slug):
    book = BookDetail.objects.get(slug=slug)
    book.delete()
    return redirect('rango:admin_books')


@admin_required()
def admin_categories(request):
    keyword = request.GET.get("keyword")
    if keyword != None and keyword != "":
        category_list = list(Category.objects.filter(name__contains=keyword).order_by('name')[:20])
        context_dict = {'category_list': category_list, 'keyword': keyword}
        return render(request, 'rango/admin/categories.html', context=context_dict)
    category_list = list(Category.objects.all()[:20])
    context_dict = {'category_list': category_list}
    return render(request, 'rango/admin/categories.html', context=context_dict)


@admin_required()
def admin_add_categories(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = Category(name=name)
        category.save()
        return JsonResponse({'code': 200, 'status': 'success', 'msg': 'Add made successfully'})
    else:
        return render(request, 'rango/admin/add_category.html')


@admin_required()
def admin_edit_categories(request, slug):
    if request.method == 'POST':
        category = Category.objects.get(slug=slug)
        name = request.POST.get('name')
        category.name = name
        category.save()
        return JsonResponse({'code': 200, 'status': 'success', 'msg': 'Edit made successfully'})
    else:
        category = Category.objects.get(slug=slug)
        context_dict = {'category': category}
        return render(request, 'rango/admin/edit_category.html', context=context_dict)


@admin_required()
def admin_del_categories(request, slug):
    category = Category.objects.get(slug=slug)
    category.delete()
    return redirect('rango:admin_categories')


@admin_required()
def admin_orders(request):
    # keyword = request.GET.get("keyword")
    # if keyword != None and keyword != "":
    #     order_list = Order.objects.filter().order_by('-date')[:20]
    #     context_dict = {'book_list': book_list, 'keyword':keyword}
    #     return render(request, 'rango/admin/books.html', context=context_dict)
    ret = []
    order_list = Order.objects.order_by('-date')[:20]
    for order in order_list:
        user = order.user.first()
        book = order.book.first()
        temp_dict = {'book': book, 'user': user, 'order': order}
        ret.append(temp_dict)
    context_dict = {'orders': ret}
    return render(request, 'rango/admin/orders.html', context=context_dict)


@admin_required()
def admin_orders_status(request):
    if request.method == 'POST':
        status = request.POST.get('code')
        order_no = request.POST.get('order_no')
        try:
            order = Order.objects.get(order_no=order_no)
        except Order.DoesNotExist:
            return JsonResponse({'code': 500, 'status': 'failed', 'msg': 'Order invalid'})

        order.status = status
        order.save()
        return JsonResponse({'code': 200, 'status': 'success', 'msg': 'Status set successfully'})


@user_required()
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


@user_required(ajax=True)
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


@user_required()
def cart_del(request):
    try:
        id = request.GET.get('id')
        book = BookDetail.objects.get(id=id)
        Cart.objects.get(user=request.user, book=book).delete()
    except:
        return HttpResponse("error")
    return redirect('rango:cart')


@user_required()
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
        all_total = round(all_total, 2)
        price = book.price[:1] + str(price)
        total = book.price[:1] + str(total)
        temp = {'book': book, 'num': num, 'price': price, 'total': total}
        ret.append(temp)

    context_dict = {'confirm': ret, 'all_total': all_total}
    return render(request, 'rango/confirm.html', context=context_dict)


@user_required()
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


@user_required()
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
        if order.status==0:
            return render(request, 'rango/bought.html', context={'err_msg':'The order is in pending status, you cannot make comment now.'})

        book = order.book.first()
        context_dict = {'book': book, 'order_no': order_no}
        return render(request, 'rango/comment.html', context=context_dict)
