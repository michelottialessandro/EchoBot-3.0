from transformers import pipeline
classifier = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-large-zeroshot-v2.0")
candidate_labels = ['asking for time','asking for date',"asking for weather","calculation"]
while True:
    input_=input("enter: ")
    sequence_to_classify = input_
    output = classifier(sequence_to_classify, candidate_labels, multi_label=False)
    print(output)