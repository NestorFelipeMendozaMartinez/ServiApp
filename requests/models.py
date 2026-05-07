from django.db import models
from django.contrib.auth.models import User
from services.models import Category


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('open', 'Abierta'),
        ('in_progress', 'En Progreso'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='requests/', null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.client.username}"


class Offer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('accepted', 'Aceptada'),
        ('rejected', 'Rechazada'),
    ]

    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='offers')
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Oferta de {self.provider.username} para {self.request.title}"


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    reviewed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review de {self.reviewer.username} a {self.reviewed.username}"


class Contract(models.Model):
    offer = models.OneToOneField(Offer, on_delete=models.CASCADE, related_name='contract')
    client_signed = models.BooleanField(default=False)
    provider_signed = models.BooleanField(default=False)
    client_signature = models.CharField(max_length=200, blank=True)
    provider_signature = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contrato de oferta {self.offer.id}"

    @property
    def is_fully_signed(self):
        return self.client_signed and self.provider_signed


class Transaction(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Efectivo'),
        ('transfer', 'Transferencia'),
        ('nequi', 'Nequi'),
        ('daviplata', 'Daviplata'),
    ]

    request = models.OneToOneField(ServiceRequest, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transacción para {self.request.title} - {self.amount}"


class Message(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Mensaje de {self.sender.username} en solicitud {self.service_request.id}"


class Notification(models.Model):
    TYPES = [
        ('new_offer', 'Nueva Oferta'),
        ('offer_accepted', 'Oferta Aceptada'),
        ('offer_rejected', 'Oferta Rechazada'),
        ('new_message', 'Nuevo Mensaje'),
        ('request_completed', 'Solicitud Completada'),
        ('new_review', 'Nueva Reseña'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=30, choices=TYPES)
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    read = models.BooleanField(default=False)
    link = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notificación para {self.user.username}: {self.title}"
