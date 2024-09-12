import json
from datasets import Dataset, DatasetDict
from transformers import AutoTokenizer, BartForSequenceClassification, TrainingArguments, Trainer, AutoConfig, AutoModelForTokenClassification,AutoModelForSequenceClassification ,pipeline
import torch.nn as nn
import torch

# Carica il dataset dal file JSON
with open("dati_training.json", "r") as f:
    data = json.load(f)

# Converti la lista di dizionari in un Dataset Hugging Face
dataset = Dataset.from_list(data)

# Suddividi il dataset in train e test set
dataset = dataset.train_test_split(test_size=0.2)

# Crea un DatasetDict per compatibilità con Trainer
dataset_dict = DatasetDict({
    'train': dataset['train'],
    'test': dataset['test']
})

# Usa un tokenizer pre-addestrato
tokenizer = AutoTokenizer.from_pretrained("MoritzLaurer/deberta-v3-large-zeroshot-v2.0")

# Funzione di tokenizzazione
def tokenize_function(examples):
    return tokenizer(examples["question"], padding="max_length", truncation=True)

# Applica la funzione di tokenizzazione al dataset
tokenized_datasets = dataset_dict.map(tokenize_function, batched=True)

# Mappa le etichette di stringa a indici numerici, inclusa la quarta etichetta
label_to_id = {"asking for time": 0, "asking for date": 1, "asking for weather": 2, "calculation": 3}

# Funzione che converte le etichette di stringa in numeri
def encode_labels(example):
    example["label"] = label_to_id[example["label"]]
    return example

# Applica la funzione di codifica delle etichette al dataset tokenizzato
tokenized_datasets = tokenized_datasets.map(encode_labels)

config = AutoConfig.from_pretrained("MoritzLaurer/deberta-v3-large-zeroshot-v2.0")
config.num_labels = 4

model = AutoModelForTokenClassification.from_config(config)
# model = BartForSequenceClassification.from_pretrained("facebook/bart-large-mnli", num_labels=4,ignore_mismatched_sizes=True)
# model.classifier = nn.Linear(1024, 4)
# model._get_resized_lm_head=nn.Linear(1024, 4)
# # Reinizializza i pesi della testa di classificazione per adattarli al nuovo numero di etichette
# model.classification_head.out_proj = nn.Linear(model.config.d_model, len(label_to_id))
# model.classification_head.out_proj.weight.data.normal_(mean=0.0, std=model.config.init_std)
# model.classification_head.out_proj.bias.data.zero_()
# model.config.num_labels = len(label_to_id)

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Crea un oggetto Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
)

# Addestra il modello
trainer.train()

# Salva il modello e il tokenizer per un uso futuro
model.save_pretrained("modello_personalizzato")
tokenizer.save_pretrained("modello_personalizzato")

# Carica il modello e il tokenizer addestrati
model = BartForSequenceClassification.from_pretrained("modello_personalizzato")
tokenizer = AutoTokenizer.from_pretrained("modello_personalizzato")

# Crea una pipeline di classificazione
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, return_all_scores=True)

# Esegui una previsione
risultato = classifier("Che ore sono?")
print(risultato)
