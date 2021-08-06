from django.contrib import admin
from rango.models import Category, UserProfile,BookDetail, Cart





class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile)
admin.site.register(BookDetail)
admin.site.register(Cart)
