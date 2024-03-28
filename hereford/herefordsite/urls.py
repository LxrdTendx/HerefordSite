from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_view, name='login'),
    path('about-us/', views.about_us, name='about_us'),
    path('market/', views.production, name='market'),
    path('our-farm/', views.farm, name='farm'),
    path('download-pdf/<int:farm_id>/', views.download_pdf, name='download_pdf'),
    path('join/', views.join, name='join'),
    path('contacts/', views.contacts, name='contacts'),
    path('news', views.news_view, name='news_list'),
    path('recipes', views.recipe_view, name='recipes_list'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('recipes/<int:pk>', views.RecipesDetailView.as_view(), name='recipe_detail')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)