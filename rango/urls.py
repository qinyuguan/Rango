from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('changePassword/', views.change_password, name="change_password"),
    path('books/', views.products, name='products'),
    path('books/<slug:book_detail_slug>/', views.product, name='product'),

    path('bought/', views.bought, name='bought'),
    path('profile/', views.profile, name='profile'),
    path('users/', views.users, name='users'),
    path('cart/', views.cart, name='cart'),
    path('comment/<slug:order_no>/', views.comment, name='comment'),
    path('category/<slug:category_name>/', views.category, name='category'),
    path('categories/', views.categories, name='categories'),
    path('cart/add/', views.cart_add, name='cart_add'),
    path('cart/del/', views.cart_del, name='cart_del'),
    path('cart/confirm/', views.cart_confirm, name='cart_confirm'),
    path('cart/pay/', views.cart_pay, name='cart_pay'),

    path('admin/books/', views.admin_books, name='admin_books'),
    path('admin/books/add/', views.admin_add_books, name='admin_add_books'),
    path('admin/books/edit/<slug:slug>/', views.admin_edit_books, name='admin_edit_books'),
    path('admin/books/del/<slug:slug>/', views.admin_del_books, name='admin_del_books'),
    path('admin/categories/', views.admin_categories, name='admin_categories'),
    path('admin/categories/add/', views.admin_add_categories, name='admin_add_categories'),
    path('admin/categories/edit/<slug:slug>/', views.admin_edit_categories, name='admin_edit_categories'),
    path('admin/categories/del/<slug:slug>/', views.admin_del_categories, name='admin_del_categories'),
    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/orders/status', views.admin_orders_status, name='admin_orders_status'),
]
