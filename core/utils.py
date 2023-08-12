from .models import Post, Profile
from django.db.models import Q

def shorten_caption(sentence, max_length):
	if len(sentence) <= max_length:
		return sentence
	else:
		words = sentence.split()
		shortened_words = []
		length_count = 0
		for word in words:
			if length_count + len(word) + 1 <= max_length:
				shortened_words.append(word)
				length_count += len(word) + 1
			else:
				break
		return ' '.join(shortened_words) + '...'
	

def searchProfiles(request):
	search_query = ''
	if request.GET.get('search_query'):
		search_query= request.GET.get('search_query')

	profiles= Profile.objects.distinct().filter(
		Q(username__icontains=search_query) |
		Q(bio__icontains=search_query) 
	)
	return profiles, search_query