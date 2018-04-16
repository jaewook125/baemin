from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
	path('', views.index, name='index'),
	path('category/<int:pk>/', views.category_detail, name='category_detail'),
	path('<int:pk>/', views.shop_detail, name='shop_detail'),
	path('<int:pk>/review/new/', views.review_new, name='review_new'),
	path('<int:shop_pk>/order/new/', views.order_new, name='order_new'),
	# path('<int:shop_pk>/order/<int:pk>/pay/', views.order_pay, name='order_pay'),
]