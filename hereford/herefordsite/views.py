from django.shortcuts import render
from .models import Product, ProductType, SubProductType
from django.http import HttpResponse
import psycopg2

def login_view(request):
    return render(request, 'login.html')

def about_us(request):
    return render(request, 'about-us.html')

def farm(request):
    return render(request, 'our-farm.html')

def join(request):
    return render(request, 'join.html')


def production(request):
    products = Product.objects.all()
    product_types = ProductType.objects.all()

    # Фильтр по региону
    region = request.GET.get('region', request.GET.get('hidden_region', ''))
    if region:
        products = products.filter(region=region)

    # Сортировка по цене
    price_order = request.GET.get('price_order', request.GET.get('hidden_price_order', ''))
    if price_order == 'asc':
        products = products.order_by('price')
    elif price_order == 'desc':
        products = products.order_by('-price')

    product_type_filter = request.GET.get('product_type', request.GET.get('hidden_product_type', ''))
    if product_type_filter:
        products = products.filter(product_type_id=product_type_filter)
    else:
        # Это нужно, чтобы "Все типы продукции" автоматически выбиралось, если фильтр региона установлен, но фильтр продукта нет
        product_type_filter = ''

    # Фильтр по подтипу
    sub_product_type = request.GET.get('sub_product_type', request.GET.get('hidden_sub_product_type', ''))
    if sub_product_type:
        products = products.filter(sub_product_type_id=sub_product_type)

    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(details__icontains=search_query)

    regions = Product.objects.values_list('region', flat=True).distinct()
    subtypes = SubProductType.objects.all()

    context = {
        'products': products,
        'regions': regions,
        'subtypes': subtypes,
        'product_types': product_types,
        'region': region,
        'product_type_filter': product_type_filter,
        'sub_product_type': sub_product_type,
        'price_order': price_order
    }

    return render(request, 'market.html', context)



def get_products_from_db():
    DATABASE = {
        'dbname': 'herefordsite',
        'user': 'postgres',
        'password': '12345',
        'host': 'localhost',
        'port': '5432',
    }

    conn = psycopg2.connect(**DATABASE)
    cursor = conn.cursor()

    query = """
    SELECT product.*, product_type.name
    FROM product
    JOIN product_type ON product.product_type_id = product_type.id
    """

    cursor.execute(query)
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return products


def product_image(request, product_id):
    # Подключение к БД и получение изображения по product_id
    DATABASE = {
        'dbname': 'herefordsite',
        'user': 'postgres',
        'password': '12345',
        'host': 'localhost',
        'port': '5432',
    }

    conn = psycopg2.connect(**DATABASE)
    cur = conn.cursor()

    try:
        cur.execute("SELECT product_photo FROM product WHERE id = %s", (product_id,))
        image_data = cur.fetchone()[0]
        return HttpResponse(image_data, content_type="image/jpeg")
    except Exception as e:
        print(f"Ошибка при извлечении изображения: {e}")
    finally:
        cur.close()
        conn.close()

