from transformers import pipeline

# # Carica il modello e il tokenizer addestrati
# model = BartForSequenceClassification.from_pretrained("modello_personalizzato")
# tokenizer = AutoTokenizer.from_pretrained("modello_personalizzato")
classifier_personalizzato = pipeline("zero-shot-classification", model="modello_personalizzato")
classifier = pipeline("zero-shot-classification",model="facebook/bart-large-mnli")
candidate_labels = ['asking for time','asking for date',"asking for weather","calculation"]

while True:
    input_=input("enter something: ")
    risultato_pers=classifier_personalizzato(input_,candidate_labels)
    risultato_non_pers = classifier(input_,candidate_labels)
    print("my model: ")
    print(risultato_pers)
    print("\n")
    print("original model")
    print(risultato_non_pers)
    print("\n")
