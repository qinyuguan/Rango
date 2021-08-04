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
    path('add_address/', views.add_address, name='add_address'),
    path('users/', views.users, name='users'),
    path('cart/', views.cart, name='cart'),
    path('comment/', views.comment, name='comment'),
    path('category/<slug:category_name>/', views.category, name='category'),
    path('categories/', views.categories, name='categories')
]
