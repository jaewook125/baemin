from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Category, Shop, Review
from .forms import ReviewForm

index = ListView.as_view(model=Category)

category_detail = DetailView.as_view(model=Category)

shop_detail = DetailView.as_view(model=Shop)

class ReviewCreateView(CreateView):
	model = Review
	form_class = ReviewForm

	def form_valid(self, form):
		self.shop = get_object_or_404(Shop, pk=self.kwargs['pk'])
		#shop을 가지고와서 url의 pk값을 가지고온다
		#self.shop <- 멤버변수
		print(self.shop)
		review = form.save(commit=False)
		review.shop = self.shop
		review.author = self.request.user #현재 유저를 대응
		return super().form_valid(form)

	def get_success_url(self):
		return self.shop.get_absolute_url()

review_new = ReviewCreateView.as_view()
