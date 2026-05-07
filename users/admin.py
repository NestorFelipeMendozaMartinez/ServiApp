from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_is_provider')
    list_filter = ('is_staff', 'is_superuser', 'profile__is_provider')

    def get_is_provider(self, obj):
        return obj.profile.is_provider
    get_is_provider.short_description = 'Es Proveedor'
    get_is_provider.boolean = True


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'is_provider', 'rating', 'total_ratings', 'phone')
    list_filter = ('is_provider', 'city')
    search_fields = ('user__username', 'user__email', 'city', 'bio')
    readonly_fields = ('rating', 'total_ratings')
