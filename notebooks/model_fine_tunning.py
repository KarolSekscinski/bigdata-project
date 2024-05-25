import pandas as pd
import tensorflow as tf
from transformers import TFAutoModelForSequenceClassification, AutoTokenizer, AutoConfig
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

tf.keras.mixed_precision.set_global_policy('mixed_float16')

# Verify TensorFlow is using the GPU
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

# Load WHO data
who_data = pd.read_csv('who_data.csv')
who_data = who_data.sample(3000)
# Create a labeled dataset (example)
labeled_data = []

for index, row in who_data.iterrows():
    if row['New_deaths'] > 0:
        labeled_data.append((row['Country'], 'death'))
    elif row['New_cases'] > 0:
        labeled_data.append((row['Country'], 'infection'))
    else:
        labeled_data.append((row['Country'], 'vaccine'))

labeled_df = pd.DataFrame(labeled_data, columns=['text', 'label'])

# Encode the labels
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labeled_df['label'])

# Load the tokenizer and model
model_name = 'facebook/bart-large-mnli'
tokenizer = AutoTokenizer.from_pretrained(model_name)
config = AutoConfig.from_pretrained(model_name, num_labels=3)
model = TFAutoModelForSequenceClassification.from_pretrained(model_name, config=config)

# Tokenize the text
encodings = tokenizer(list(labeled_df['text']), truncation=True, padding=True, max_length=128)

# Convert the tokenized inputs to a TensorFlow dataset
def convert_to_tf_dataset(encodings, labels):
    dataset = tf.data.Dataset.from_tensor_slices((
        dict(encodings),
        labels
    ))
    return dataset

# Prepare the data for train/test split
input_ids = encodings['input_ids']
attention_mask = encodings['attention_mask']
train_input_ids, val_input_ids, train_attention_mask, val_attention_mask, train_labels, val_labels = train_test_split(
    input_ids, attention_mask, encoded_labels, test_size=0.2
)

# Update batch size
batch_size = 1  # Reduce batch size further
train_dataset = tf.data.Dataset.from_tensor_slices(({
    'input_ids': train_input_ids,
    'attention_mask': train_attention_mask
}, train_labels)).shuffle(1000).batch(batch_size)

val_dataset = tf.data.Dataset.from_tensor_slices(({
    'input_ids': val_input_ids,
    'attention_mask': val_attention_mask
}, val_labels)).batch(batch_size)

# Compile the model with mixed precision policy
optimizer = tf.keras.optimizers.Adam(learning_rate=5e-5)
model.compile(
    optimizer=optimizer,
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

# Define gradient accumulation parameters
accumulation_steps = 4  # Accumulate gradients over 4 steps
accumulated_grads = [tf.Variable(tf.zeros_like(var), trainable=False) for var in model.trainable_variables]

# Custom training loop with gradient accumulation
@tf.function
def train_step(inputs, labels):
    with tf.GradientTape() as tape:
        logits = model(inputs, training=True)[0]
        loss = tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)
        scaled_loss = loss / accumulation_steps
    
    gradients = tape.gradient(scaled_loss, model.trainable_variables)
    for grad, acc_grad in zip(gradients, accumulated_grads):
        acc_grad.assign_add(grad)
    
    return scaled_loss

@tf.function
def apply_accumulated_gradients():
    optimizer.apply_gradients(zip(accumulated_grads, model.trainable_variables))
    for acc_grad in accumulated_grads:
        acc_grad.assign(tf.zeros_like(acc_grad))

# Training loop
for epoch in range(3):  # Number of epochs
    for step, (batch_inputs, batch_labels) in enumerate(train_dataset):
        loss = train_step(batch_inputs, batch_labels)
        if (step + 1) % accumulation_steps == 0:
            apply_accumulated_gradients()
            tf.keras.backend.clear_session()  # Clear session to free up memory

    # Validation step
    val_loss, val_accuracy = model.evaluate(val_dataset)
    print(f'Epoch {epoch + 1}, Loss: {loss.numpy()}, Validation Loss: {val_loss}, Validation Accuracy: {val_accuracy}')

# Save the fine-tuned model
model.save_pretrained('./fine_tuned_model')
tokenizer.save_pretrained('./fine_tuned_model')