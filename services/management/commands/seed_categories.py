from django.core.management.base import BaseCommand
from services.models import Category


CATEGORIES = [
    ('Hogar y Aseo', '🏠'),
    ('Plomería', '🔧'),
    ('Electricidad', '⚡'),
    ('Jardinería', '🌿'),
    ('Reparaciones', '🛠️'),
    ('Tecnología', '💻'),
    ('Domicilios', '🛵'),
    ('Mensajería', '📦'),
    ('Transporte', '🚗'),
    ('Diseño', '🎨'),
    ('Mecánica', '⚙️'),
    ('Salud y Bienestar', '💊'),
    ('Educación', '📚'),
    ('Fotografía', '📷'),
    ('Otros', '🔩'),
]


class Command(BaseCommand):
    help = 'Seed initial service categories'

    def handle(self, *args, **kwargs):
        created = 0
        for name, icon in CATEGORIES:
            _, was_created = Category.objects.get_or_create(name=name, defaults={'icon': icon})
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f'OK: {created} categorias creadas ({len(CATEGORIES)} total)'))
