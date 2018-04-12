from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import Category, Shop, Item
from urllib.parse import quote

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['icon_img','name','is_public']
	list_display_links = ['name']
	list_filter = ['is_public'] #is_public이 표시된것만 보기
	search_fields = ['name']

	def icon_img(self, category):
		if category.icon: #카테고리아이콘에 필드명이 없는경우도 있기때문에
		#필드명이 있는경우
		#파일필드와 이미지 필드는 실제로는,스테이트 필드 즉 문자열필드
		#해당 문자열로 참거짓을 판단가능
			img_tag = '<img src="{}" style="max-width: 72px;"/>'
			return mark_safe(img_tag.format(category.icon.url))
			#이 문자열은 안전하다(mark_safe), 꺽새표시 바로잡기
			#경로가 있을때만 url을 만들어줌
		return None
		#없을땐 none

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
	list_display = ('name','address_link')

	def address_link(self, shop):
		if shop.address: #위와 동일
			url = 'https://map.naver.com/?query=' + quote(shop.address)
			return mark_safe('<a href={} target=_blank>{}</a>'.format(url, shop.address))
		return None
	address_link.short_description = "주소 (네이버 지도)"
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
	list_display = ['shop','name']
	list_display_links = ['name']
	list_filter = ['shop']
	search_fields = ['name']