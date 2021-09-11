from django.shortcuts import render
from rest_framework.views import APIView
from WPI.core.mongo_models import Location, Food, Symptom

class searchView(APIView):
	def get(self, request):
		wd = request.GET.get('wd')
		tag = request.GET.get('radio')
		
		if tag == 'location':
			rs = Location.search(wd)
		elif tag == 'food':
			rs = Food.search(wd)
		else:   # tag == 'Symptom'
			rs = Symptom.search(wd)
		context = {}
		# for r in rs:
		# 	r['id'] = r['_id']
		context['wd'] = wd
		context['tag'] = tag
		context['results'] = rs
		context['num'] = len(context['results'])
		return render(request, 'result.html', context=context)
	