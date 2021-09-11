from django.conf import settings
from pymongo import TEXT
import ast

'''
References:
https://www.mongodb.com/compatibility/mongodb-and-django
'''

# First define the database name
conn = settings.MONGOCLIENT['foodborne_illness']


class Tweet(object):
	# Now get/create collection name (remember that you will see the database in your mongodb cluster only after you create a collection
	db_tweet = conn['tweet']
	
	@classmethod
	def insert_one_tweet(cls, tweet):
		# insert into tweet table
		_id = str(cls.db_tweet.count())
		tweet.update({'_id': _id})
		rs = cls.db_tweet.insert_one(tweet)
		tweet_id = rs.inserted_id
		
		# update food/loc/symp tables
		food = ast.literal_eval(tweet['food'])
		food_list = list(food.values())
		# print(food_list)
		for f in food_list:
			# check if this food already stored in DB
			res = Food.find_food(f)
			# if not, add into food colletion
			if (res == None):
				print('insert food: ', f)
				tweetIds = [tweet_id]
				Food.insert_new_food({'name': f, 'tweet_ids': tweetIds, 'count': 1})
			# append the tweet id to this food
			else:
				print('update food: ', tweet_id)
				Food.update_food_by_tweet_id(res, tweet_id)
		
		loc = ast.literal_eval(tweet['loc'])
		loc_list = list(loc.values())
		# print(loc_list)
		for l in loc_list:
			res = Location.find_loc(l)
			if (res == None):
				print('insert location: ', l)
				tweetIds = [tweet_id]
				Location.insert_new_loc({'name': l, 'tweet_ids': tweetIds, 'count': 1})
			else:
				print('update location: ', tweet_id)
				Location.update_loc_by_tweet_id(res, tweet_id);
		
		symptom = ast.literal_eval(tweet['symptom'])
		sym_list = list(symptom.values())
		# print(sym_list)
		for s in sym_list:
			res = Symptom.find_symptom(s)
			if (res == None):
				print('insert symptom: ', s)
				tweetIds = [tweet_id]
				Symptom.insert_new_symptom({'name': s, 'tweet_ids': tweetIds, 'count': 1})
			else:
				print('update symptom: ', tweet_id)
				Symptom.update_symp_by_tweet_id(res, tweet_id);
		
		return rs


class Food(object):
	db_food = conn['food']
	db_tweet = conn['tweet']
	
	@classmethod
	def insert_new_food(cls, food):
		food.update({'_id': cls.db_food.count()})
		rs = cls.db_food.insert_one(food)
		
		return rs
	
	@classmethod
	def find_food(cls, food):
		res = cls.db_food.find_one({'name': food})
		return res
	
	@classmethod
	def update_food_by_tweet_id(cls, food, tweet_id):
		food_id = food['_id']
		tweet_ids = food['tweet_ids']
		print(type(tweet_ids))
		if tweet_id not in tweet_ids:
			tweet_ids.append(tweet_id)
			cls.db_food.update({'_id': food_id},
			                       {'$set': {'tweet_ids': tweet_ids},
			                       '$inc': {'count': 1}}, True)
	
	@classmethod
	def search(cls, search_str):
		index_info = cls.db_food.index_information()
		print(index_info)
		if len(index_info) < 2:
			Food.reset_index('name')
		else:
			cur_index = list(index_info.keys())[1]
			if cur_index != 'name':
				Food.reset_index('name')
		# print('reach search location ', search_str)
		ids_cursor = cls.db_food.find({"$text": {"$search": search_str, '$caseSensitive': False}}).sort("date", 1)
		res = []
		for ids in ids_cursor:
			for id in ids['tweet_ids']:
				res.append(cls.db_tweet.find_one({'_id': id}))
		# print(res)
		
		return res
	
	@classmethod
	def reset_index(cls, index_str):
		cls.db_food.drop_indexes()
		if len(cls.db_food.index_information()) == 1:
			cls.db_food.create_index([(index_str, TEXT)], default_language='english')
		
		return cls.db_food.index_information()


class Location(object):
	db_loc = conn['location']
	db_tweet = conn['tweet']
	
	@classmethod
	def insert_new_loc(cls, loc):
		loc.update({'_id': cls.db_loc.count()})
		rs = cls.db_loc.insert_one(loc)
		
		return rs
	
	@classmethod
	def find_loc(cls, loc):
		res = cls.db_loc.find_one({'name': loc})
		return res
	
	@classmethod
	def update_loc_by_tweet_id(cls, loc, tweet_id):
		loc_id = loc['_id']
		tweet_ids = loc['tweet_ids']
		print(type(tweet_ids))
		if tweet_id not in tweet_ids:
			tweet_ids.append(tweet_id)
			cls.db_loc.update({'_id': loc_id},
			                      {'$set': {'tweet_ids': tweet_ids},
			                      '$inc': {'count': 1}}, upsert=True)
	
	@classmethod
	def search(cls, search_str):
		index_info = cls.db_loc.index_information()
		if len(index_info) < 2:
			Location.reset_index('name')
		else:
			cur_index = list(index_info.keys())[1]
			if cur_index != 'name':
				Location.reset_index('name')
		# print('reach search location ', search_str)
		ids_cursor = cls.db_loc.find({"$text": {"$search": search_str, '$caseSensitive': False}}).sort("date",1)
		res = []
		for ids in ids_cursor:
			for id in ids['tweet_ids']:
				res.append(cls.db_tweet.find_one({'_id': id}))
		# print(res)
		
		return res
	
	@classmethod
	def reset_index(cls, index_str):
		cls.db_loc.drop_indexes()
		if len(cls.db_loc.index_information()) == 1:
			cls.db_loc.create_index([(index_str, TEXT)], default_language='english')
		
		return cls.db_loc.index_information()


class Symptom(object):
	db_symp = conn['symptom']
	db_tweet = conn['tweet']
	
	@classmethod
	def insert_new_symptom(cls, symp):
		symp.update({'_id': cls.db_symp.count()})
		rs = cls.db_symp.insert_one(symp)
		
		return rs
	
	@classmethod
	def find_symptom(cls, symp):
		res = cls.db_symp.find_one({'name': symp})
		return res
	
	@classmethod
	def update_symp_by_tweet_id(cls, symptoms, tweet_id):
		symp_id = symptoms['_id']
		tweet_ids = symptoms['tweet_ids']
		print(type(tweet_ids))
		if tweet_id not in tweet_ids:
			tweet_ids.append(tweet_id)
			cls.db_symp.update({'_id': symp_id},
			                      {'$set': {'tweet_ids': tweet_ids},
			                      '$inc': {'count': 1}}, upsert=True)
	
	@classmethod
	def search(cls, search_str):
		index_info = cls.db_symp.index_information()
		if len(index_info) < 2:
			Symptom.reset_index('name')
		else:
			cur_index = list(index_info.keys())[1]
			if cur_index != 'name':
				Symptom.reset_index('name')
		# print('reach search location ', search_str)
		ids_cursor = cls.db_symp.find({"$text": {"$search": search_str, '$caseSensitive': False}}).sort("_id", 1)
		res = []
		for ids in ids_cursor:
			for id in ids['tweet_ids']:
				res.append(cls.db_tweet.find_one({'_id': id}))
		# print(res)
		
		return res
	
	@classmethod
	def reset_index(cls, index_str):
		cls.db_symp.drop_indexes()
		if len(cls.db_symp.index_information()) == 1:
			cls.db_symp.create_index([(index_str, TEXT)], default_language='english')
		
		return cls.db_symp.index_information()