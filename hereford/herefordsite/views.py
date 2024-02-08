from django.shortcuts import render
from .models import Product, ProductType, SubProductType, CarouselImage, Farm_point, Region, News_Page
from django.db.models import Q
from django.http import HttpResponse
import psycopg2


def login_view(request):
    carousel_images = CarouselImage.objects.all()
    news_pages = News_Page.objects.all().order_by('-date')[:2]

    context = {
        'carousel_images': carousel_images,
        'news_pages': news_pages
    }

    return render(request, 'login.html', context)


def about_us(request):
    return render(request, 'about-us.html')

def farm(request):
    farms = Farm_point.objects.all()

    # Логика сортировки, если необходима
    sort_order = request.GET.get('sort', '')
    if sort_order == 'asc':
        farms = farms.order_by('region')
    elif sort_order == 'desc':
        farms = farms.order_by('-region')

    context = {
        'farms': farms
    }

    return render(request, 'our-farm.html', context)



def join(request):
    return render(request, 'join.html')
def contacts(request):
    return render(request, 'contacts.html')


def production(request):
    products = Product.objects.all()
    product_types = ProductType.objects.all()


    # Фильтр по региону
    regions = request.GET.get('region', request.GET.get('hidden_region', ''))
    if regions:
        region_list = regions.split(',')
        products = products.filter(region__name__in=region_list)

    # Сортировка по цене
    price_order = request.GET.get('price_order', request.GET.get('hidden_price_order', ''))
    if price_order == 'asc':
        products = products.order_by('price')
    elif price_order == 'desc':
        products = products.order_by('-price')

    # Фильтр по типу продукции
    product_type_filter = request.GET.get('product_type', request.GET.get('hidden_product_type', ''))
    if product_type_filter:
        product_type_list = [int(pt) for pt in product_type_filter.split(',')]
        products = products.filter(product_type_id__in=product_type_list)

    # Фильтр по подтипу
    sub_product_type = request.GET.get('sub_product_type', request.GET.get('hidden_sub_product_type', ''))
    if sub_product_type:
        sub_product_type_list = [int(spt) for spt in sub_product_type.split(',')]
        products = products.filter(sub_product_type_id__in=sub_product_type_list)

    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(farm__icontains=search_query) |
            Q(age__icontains=search_query)
        )

    all_regions = Region.objects.values_list('name', flat=True).distinct()
    subtypes = SubProductType.objects.all()

    context = {
        'all_regions': all_regions,
        'products': products,
        'region': regions,
        'subtypes': subtypes,
        'product_types': product_types,
        'product_type_filter': product_type_filter,
        'sub_product_type': sub_product_type,
        'price_order': price_order
    }

    return render(request, 'market.html', context)


# def production(request):
#     products = Product.objects.all()
#     product_types = ProductType.objects.all()
#
#
#     # Фильтр по региону
#     regions = request.GET.get('region', request.GET.get('hidden_region', ''))
#     if regions:
#         region_list = regions.split(',')
#         products = products.filter(region__in=region_list)
#
#     # Сортировка по цене
#     price_order = request.GET.get('price_order', request.GET.get('hidden_price_order', ''))
#     if price_order == 'asc':
#         products = products.order_by('price')
#     elif price_order == 'desc':
#         products = products.order_by('-price')
#
#     # Фильтр по типу продукции
#     product_type_filter = request.GET.get('product_type', request.GET.get('hidden_product_type', ''))
#     if product_type_filter:
#         product_type_list = [int(pt) for pt in product_type_filter.split(',')]
#         products = products.filter(product_type_id__in=product_type_list)
#
#     # Фильтр по подтипу
#     sub_product_type = request.GET.get('sub_product_type', request.GET.get('hidden_sub_product_type', ''))
#     if sub_product_type:
#         sub_product_type_list = [int(spt) for spt in sub_product_type.split(',')]
#         products = products.filter(sub_product_type_id__in=sub_product_type_list)
#
#     # Поиск
#     search_query = request.GET.get('search', '')
#     if search_query:
#         products = products.filter(
#             Q(farm__icontains=search_query) |
#             Q(age__icontains=search_query)
#         )
#
#     all_regions = Product.objects.values_list('region', flat=True).distinct()
#     subtypes = SubProductType.objects.all()
#
#     context = {
#         'all_regions': all_regions,
#         'products': products,
#         'region': regions,
#         'subtypes': subtypes,
#         'product_types': product_types,
#         'product_type_filter': product_type_filter,
#         'sub_product_type': sub_product_type,
#         'price_order': price_order
#     }
#
#     return render(request, 'market.html', context)

