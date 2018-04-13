from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.urls import reverse
from django.db import models
from jsonfield import JSONField

class Category(models.Model):
	name = models.CharField(max_length=100, db_index=True)
	icon = models.ImageField(blank=True)
	is_public = models.BooleanField(default=False, db_index=True)
	#공개된 카테고리만 찾고싶을때


	def get_absolute_url(self):
		return reverse('shop:category_detail', args=[self.pk])

	def __str__(self):
		return self.name

class Shop(models.Model):
	category = models.ForeignKey(Category, on_delete=models.PROTECT)
	name = models.CharField(max_length=100, db_index=True)
	desc = models.TextField(blank=True)
	latlng = models.CharField(max_length=100, blank=True)
	image = models.ImageField(blank=True)
	is_public = models.BooleanField(default=False, db_index=True)
	meta = JSONField() # NoSQL적 특성
	#공개된 가게

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:shop_detail', args=[self.pk])

	@property
	def address(self):
		return self.meta.get('address')
		#meta모델의 address를 가지고온다 없으면 none

class Review(models.Model):
	shop = models.ForeignKey(Shop, on_delete=models.PROTECT)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
	photo = models.ImageField(blank=True)
	rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	message = models.TextField()

	def __str__(self):
		return self.author

class Item(models.Model):
	shop = models.ForeignKey(Shop, on_delete=models.PROTECT)
	name = models.CharField(max_length=100, db_index=True)
	desc = models.TextField(blank=True)
	amount = models.PositiveIntegerField()
	photo = models.ImageField(blank=True)
	is_public = models.BooleanField(default=False, db_index=True)
	#공개된 아이템
	meta = JSONField()

	def __str__(self):
		return self.name
# class Order(models.Model):
# 	pass