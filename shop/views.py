from django.contrib.auth.mixins import LoginRequiredMixin #로그인 상황이 아니면 자동으로 이동시킴
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from .models import Category, Shop, Review, Order, OrderItem, Item
from .forms import ReviewForm, OrderForm



index = ListView.as_view(model=Category)

category_detail = DetailView.as_view(model=Category)

shop_detail = DetailView.as_view(model=Shop)

class ReviewCreateView(LoginRequiredMixin, CreateView):
	model = Review
	form_class = ReviewForm

	def form_valid(self, form):
		self.shop = get_object_or_404(Shop, pk=self.kwargs['pk'])
		#shop을 가지고와서 url의 pk값을 가지고온다
		#self.shop <- 멤버변수
		print(self.shop)
		review = form.save(commit=False)
		review.shop = self.shop
		review.author = self.request.user #현재 유저를 대응 author는 유저모델에 대한 외래키
		#django.contrib.auth.models.AnonymousUser
		#단순 파이선 클래스의 인스턴스
		return super().form_valid(form)

	def get_success_url(self):
		return self.shop.get_absolute_url()

review_new = ReviewCreateView.as_view()

@login_required
def order_new(request, shop_pk):
	item_qs = Item.objects.filter(shop__pk=shop_pk, id__in=request.GET.keys())
	#어떤 특정 shop에 있는 메뉴만 필터링 하겠다
	# item_dict = { item.pk: item for item in item_qs }
	#해당 쿼리셋을 순회하면서 사전을 만든다
	#어떤 메뉴 pk에 대한 어떤 메뉴

	quantity_dict = request.GET.dict()
	quantity_dict = { int(k): int(v) for k, v in quantity_dict.items() }
	#항상 모든 GET인자는 문자열 형태를 띄기떄문에
	#quantity_dict을 순회하면서 key와 value를 숫자로 변환해서
	#quantity_dict에 저장

	item_order_list = []
	for item in item_qs:
		#item 순회를 돌면서
		quantity = quantity_dict[item.pk]
		#quantity_dict에서 실제 주문수량을 뽑아내고
		order_item = OrderItem(quantity=quantity, item=item)
		#현재 어떤 item에 대해서 수량은 얼마나있는지 확인한다
		item_order_list.append(order_item)

	amount = sum(order_item.amount for order_item in item_order_list)
	#총 합계 계산
	instance = Order(amount=amount)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=instance)
		if form.is_valid():
			order = form.save(commit=False)
			order.user = request.user #유저가 같을때 저장
			order.save

			for order_item in item_order_list:
				order_item.order = order
			OrderItem.objects.bluk_create(item_order_list)
			#bluk_create 한번에 묶어서 쿼리처리

			return redirect('shop:order_pay', shop_pk, order.pk)
	else:
		form = OrderForm(instance=instance)

	return render(request, 'shop/order_form.html',{
		'item_order_list': item_order_list,
		'form':form,
		})

def order_pay(request):
	pass
