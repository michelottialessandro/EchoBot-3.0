from transformers import pipeline
import time
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")
sequence_to_classify = "che ore sono?"
candidate_labels = ['asking for time','calculation','play a game','asking for date',]
t1=time.time()
classification=classifier(sequence_to_classify, candidate_labels)
print(type(classification))
print(classification)
t2=time.time()
print(t2-t1)
#{'labels': ['travel', 'dancing', 'cooking'],
# 'scores': [0.9938651323318481, 0.0032737774308770895, 0.002861034357920289],
# 'sequence': 'one day I will see the world'}
