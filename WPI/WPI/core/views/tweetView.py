# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import QueryDict
from WPI.core.mongo_models import Tweet

class tweet_view(APIView):
	# only used for populating data, so no auth
	def post(self, request):
		tweet = request.POST.dict()
		print(tweet)
		rs = Tweet.insert_one_tweet(tweet)
		inserted_id = rs.inserted_id
		print('id ', inserted_id)
		return Response(inserted_id)