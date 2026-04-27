from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import os

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='CenterTitle', fontSize=18, leading=22, alignment=TA_CENTER, spaceAfter=16, spaceBefore=16, textColor=colors.HexColor('#2563eb')))
styles.add(ParagraphStyle(name='Section', fontSize=14, leading=18, spaceAfter=10, textColor=colors.HexColor('#1f2937')))
styles.add(ParagraphStyle(name='NormalGray', fontSize=10, leading=14, textColor=colors.HexColor('#6b7280')))


def build_pdf(filename):
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    elements = []

    # Portada
    elements.append(Paragraph('Plataforma de Servicios Bajo Demanda', styles['CenterTitle']))
    elements.append(Paragraph('Documentación Técnica y de Usuario', styles['Section']))
    elements.append(Spacer(1, 24))
    elements.append(Paragraph('Fecha: 27 de abril de 2026', styles['NormalGray']))
    elements.append(PageBreak())

    # Índice
    elements.append(Paragraph('Índice', styles['Section']))
    toc = [
        ['1. Descripción General', '2. Instalación y Despliegue'],
        ['3. Manual de Usuario', '4. Manual Técnico'],
        ['5. Endpoints API', '6. Modelos y Relaciones'],
        ['7. Diagramas UML', '8. Créditos y Escalabilidad']
    ]
    t = Table(toc, colWidths=[250, 250])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dbeafe')),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#1f2937')),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t)
    elements.append(PageBreak())

    # 1. Descripción General
    elements.append(Paragraph('1. Descripción General', styles['Section']))
    elements.append(Paragraph('Plataforma web para conectar clientes y proveedores de servicios locales. Permite publicar servicios, crear solicitudes, gestionar ofertas, firmar contratos y calificar proveedores.', styles['Normal']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph('Roles:', styles['Normal']))
    elements.append(Paragraph('• Cliente: solicita servicios, revisa ofertas, califica proveedores.', styles['NormalGray']))
    elements.append(Paragraph('• Proveedor: ofrece servicios, acepta solicitudes, genera ingresos.', styles['NormalGray']))
    elements.append(Paragraph('• Administrador: gestiona usuarios, supervisa servicios, controla la plataforma.', styles['NormalGray']))
    elements.append(PageBreak())

    # 2. Instalación y Despliegue
    elements.append(Paragraph('2. Instalación y Despliegue', styles['Section']))
    elements.append(Paragraph('Requisitos: Python 3.10+, pip, virtualenv, PostgreSQL (opcional para producción).', styles['Normal']))
    elements.append(Paragraph('Pasos:', styles['Normal']))
    steps = [
        '1. Clona el repositorio y entra al directorio.',
        '2. Instala dependencias: pip install -r requirements.txt',
        '3. Copia .env.example a .env y configura las variables.',
        '4. Ejecuta migraciones: python manage.py migrate',
        '5. Crea un superusuario: python manage.py createsuperuser',
        '6. Corre el servidor: python manage.py runserver',
        '7. Accede a frontend/index.html en tu navegador.'
    ]
    for s in steps:
        elements.append(Paragraph(s, styles['NormalGray']))
    elements.append(PageBreak())

    # 3. Manual de Usuario
    elements.append(Paragraph('3. Manual de Usuario', styles['Section']))
    elements.append(Paragraph('• Registro e inicio de sesión con email y contraseña.', styles['Normal']))
    elements.append(Paragraph('• Completa tu perfil y selecciona si eres proveedor.', styles['Normal']))
    elements.append(Paragraph('• Clientes: crea solicitudes, revisa ofertas, acepta y califica.', styles['Normal']))
    elements.append(Paragraph('• Proveedores: publica servicios, busca solicitudes abiertas, envía ofertas.', styles['Normal']))
    elements.append(Paragraph('• Firma y descarga contratos PDF desde la plataforma.', styles['Normal']))
    elements.append(PageBreak())

    # 4. Manual Técnico
    elements.append(Paragraph('4. Manual Técnico', styles['Section']))
    elements.append(Paragraph('Estructura de carpetas:', styles['Normal']))
    elements.append(Paragraph('• users/: modelos y endpoints de usuario y perfil', styles['NormalGray']))
    elements.append(Paragraph('• services/: modelos y endpoints de servicios y categorías', styles['NormalGray']))
    elements.append(Paragraph('• requests/: solicitudes, ofertas, contratos, transacciones, reseñas', styles['NormalGray']))
    elements.append(Paragraph('• frontend/: HTML, CSS y JS del cliente', styles['NormalGray']))
    elements.append(Paragraph('• servicios/: settings, urls y configuración global', styles['NormalGray']))
    elements.append(PageBreak())

    # 5. Endpoints API
    elements.append(Paragraph('5. Endpoints API', styles['Section']))
    api_table = [
        ['Endpoint', 'Método', 'Descripción'],
        ['/api/users/register/', 'POST', 'Registro de usuario'],
        ['/api/users/login/', 'POST', 'Login y obtención de JWT'],
        ['/api/users/profile/', 'GET/PUT', 'Ver/editar perfil'],
        ['/api/services/categories/', 'GET/POST', 'Listar/crear categorías'],
        ['/api/services/services/', 'GET/POST', 'Listar/crear servicios'],
        ['/api/services/services/<id>/', 'GET/PUT/DELETE', 'Detalle de servicio'],
        ['/api/requests/requests/', 'GET/POST', 'Listar/crear solicitudes'],
        ['/api/requests/requests/<id>/', 'GET/PUT/DELETE', 'Detalle de solicitud'],
        ['/api/requests/offers/', 'GET/POST', 'Listar/crear ofertas'],
        ['/api/requests/offers/<id>/', 'GET/PUT/DELETE', 'Detalle de oferta'],
        ['/api/requests/reviews/', 'GET/POST', 'Listar/crear reseñas'],
        ['/api/requests/transactions/', 'GET/POST', 'Listar/crear transacciones'],
        ['/api/requests/offers/<id>/contract-sign/', 'POST', 'Firmar contrato'],
        ['/api/requests/offers/<id>/contract/', 'GET', 'Descargar contrato PDF'],
    ]
    t2 = Table(api_table, colWidths=[180, 70, 250])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dbeafe')),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#1f2937')),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(t2)
    elements.append(PageBreak())

    # 6. Modelos y Relaciones
    elements.append(Paragraph('6. Modelos y Relaciones', styles['Section']))
    rel_table = [
        ['Modelo', 'Campos principales', 'Relaciones'],
        ['User', 'username, email, password', 'Profile, Service, ServiceRequest, Offer, Review'],
        ['Profile', 'phone, location, bio, is_provider, rating', 'User (OneToOne)'],
        ['ServiceCategory', 'name, description', 'Service, ServiceRequest'],
        ['Service', 'title, description, price', 'Provider (User), Category'],
        ['ServiceRequest', 'title, description, location, status', 'Client (User), Category, Offer, Review, Transaction'],
        ['Offer', 'price, message, status', 'Request, Provider (User), Contract'],
        ['Contract', 'client_signed, provider_signed', 'Offer (OneToOne)'],
        ['Review', 'rating, comment', 'Reviewer (User), Reviewed (User), Request'],
        ['Transaction', 'amount, payment_method, status', 'Request'],
    ]
    t3 = Table(rel_table, colWidths=[80, 200, 220])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dbeafe')),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#1f2937')),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t3)
    elements.append(PageBreak())

    # 7. Diagramas UML (imagen generada aparte)
    elements.append(Paragraph('7. Diagramas UML', styles['Section']))
    uml_path = os.path.join(os.path.dirname(__file__), 'uml_relaciones.png')
    if os.path.exists(uml_path):
        elements.append(Image(uml_path, width=480, height=320))
    else:
        elements.append(Paragraph('Ver archivo uml_relaciones.png adjunto.', styles['NormalGray']))
    elements.append(PageBreak())

    # 8. Créditos y Escalabilidad
    elements.append(Paragraph('8. Créditos y Escalabilidad', styles['Section']))
    elements.append(Paragraph('Desarrollado por: Tu Nombre / GitHub Copilot', styles['Normal']))
    elements.append(Paragraph('Escalable a móvil (Flutter/React Native), pagos digitales, recomendaciones inteligentes.', styles['NormalGray']))
    elements.append(Paragraph('¡Gracias por usar la plataforma!', styles['Normal']))

    doc.build(elements)

if __name__ == '__main__':
    build_pdf('DOCUMENTACION_PROYECTO.pdf')
