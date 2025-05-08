# wordsim
This is the source code of a smart model that finds the similarity between a given word and a reference list of words. Then it returns the word that has the most similarity.

## Code

```python
from wordsim import wordSim  # import the model.

lst = ['Red', 'Green', 'Blue']  # declare a list of reference words.

model = wordSim()  # create an instance of the class 'wordSim'.
model.train(lst)  # train the model.

test_word = 'gren'  # specify the required word to test.

results = model.predict(word=test_word, tunner=2)  # pass the 'test word' as an argument and tune the 'tunner' for best performance.

print(results)  # print the results.
print(model.get_best())  # or print the results that way.

#console:
{'word': 'gren', 'word_match': 'Green', 'status': 'successful', 'score': 0.3333333333333333}
{'word': 'gren', 'word_match': 'Green', 'status': 'successful', 'score': 0.3333333333333333}