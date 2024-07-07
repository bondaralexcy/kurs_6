from django.contrib import admin
from users.models import User

# Register your models here.
# Необходимо зарегистрировать User, иначе не будет видно в Admin
admin.site.register(User)
