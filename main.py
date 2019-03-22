from preprocess_reviews.Preprocess import Preprocess

review = "1.Hi  23 3.hello my name $ is Eshwar. ,"
p = Preprocess()
result = p.pre_process(review)
print(result)