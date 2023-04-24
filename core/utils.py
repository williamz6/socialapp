from .models import Post


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