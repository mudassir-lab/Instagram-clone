from django.contrib import admin
from .models import Post,Profile,Post_media,Follow,Comment,Story
 
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post_media)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Story)