from gensim.models import word2vec

token = [['오늘', '날씨는','어떤가요'], ['내일', '날씨는', '어떤가요']]
embedding = word2vec.Word2Vec(token, window=1, negative=3, min_count=1)

embedding.save('model') #모델 저장
embedding.wv.save_word2vec_format('my.embedding', binary=False) #모델 저장