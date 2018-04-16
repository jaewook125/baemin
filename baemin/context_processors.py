from django.conf import settings

def baemin(request):
	return {
		'settings' : settings,
	} #settings라는 이름으로 배민을 쓰겠다