from django.contrib import admin
from .models import ServiceRequest, Offer, Review, Contract, Transaction, Message, Notification


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'category', 'city', 'status', 'created_at')
    list_filter = ('status', 'category', 'city')
    search_fields = ('title', 'description', 'client__username')
    readonly_fields = ('created_at',)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('request', 'provider', 'price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('provider__username', 'request__title')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'reviewed', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('reviewer__username', 'reviewed__username')


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('offer', 'client_signed', 'provider_signed', 'is_fully_signed', 'created_at')
    list_filter = ('client_signed', 'provider_signed')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('request', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('payment_method', 'status')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'service_request', 'read', 'created_at')
    list_filter = ('read',)
    search_fields = ('sender__username', 'content')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'title', 'read', 'created_at')
    list_filter = ('type', 'read')
    search_fields = ('user__username', 'title')
