from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/',
         views.add_page, name='add_page'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('books/', views.products, name='products'),
    path('books/<slug:book_detail_slug>/', views.product, name='product'),
    path('bought/', views.bought, name='bought'),
    path('profile/', views.profile, name='profile'),
    path('users/', views.users, name='users'),
    path('cart/', views.cart, name='cart'),
    path('comment/', views.comment, name='comment'),
    path('category/<slug:category_name>/', views.category, name='category'),
    path('categories/', views.categories, name='categories'),


    path('admin/books/', views.admin_books, name='admin_books'),
    path('admin/books/add',views.admin_add_books, name='admin_add_books'),
    path('admin/categories/', views.admin_categories, name='admin_categories'),
    path('admin/categories/add',views.admin_add_categories, name='admin_add_categories')
]
