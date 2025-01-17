# -*- coding: utf-8 -*-
"""galaxy star quasar .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1up9Try43qBiNB3jJvjPMqCYYESNVnH1D

# Importing Libraries
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt

"""# Loading the dataset"""

file_path = "star_classification.csv"  # Replace with the correct file path
data = pd.read_csv(file_path)

"""# Showing the data"""

data

data.head()

data.tail()

"""# Information about the dataset"""

data.info()

"""# Descriptive Statistics"""

data.describe()

"""# Checking Null values"""

data.isnull()

data.isnull().sum()

"""# Drop unnecessary columns"""

columns_to_drop = ['obj_ID', 'spec_obj_ID', 'run_ID', 'rerun_ID', 'cam_col', 'field_ID', 'plate', 'MJD', 'fiber_ID']
data = data.drop(columns=columns_to_drop)

"""# Encode the target variable"""

label_encoder = LabelEncoder()
data['class'] = label_encoder.fit_transform(data['class'])  # Encode class (e.g., Galaxy, Star, Quasar)

"""# Split features and target"""

X = data.drop(columns=['class'])
y = data['class']

"""# Scale features"""

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

"""# Train-test split"""

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

"""# Class distribution"""

sns.countplot(x=data['class'], palette='viridis')
plt.title("Distribution of Classes (Galaxy, Star, Quasar)")
plt.xlabel("Class")
plt.ylabel("Count")
plt.show()

"""#  Pairplot of magnitudes (u, g, r, i, z)"""

sns.pairplot(data[['u', 'g', 'r', 'i', 'z', 'class']], hue='class', palette='Set2')
plt.title("Pairplot of Magnitudes by Class")
plt.show()

"""# Redshift distribution by class"""

sns.boxplot(x='class', y='redshift', data=data, palette='coolwarm')
plt.title("Redshift Distribution by Class")
plt.xlabel("Class")
plt.ylabel("Redshift")
plt.show()

"""# Correlation heatmap"""

correlation_matrix = data.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.show()

"""# Distribution of Magnitude by Class"""

magnitude_columns = ['u', 'g', 'r', 'i', 'z']

for mag in magnitude_columns:
    plt.figure(figsize=(8, 4))
    sns.kdeplot(data=data, x=mag, hue='class', fill=True, alpha=0.5, palette='Set2')
    plt.title(f"Distribution of {mag} Magnitude by Class")
    plt.xlabel(f"{mag} Magnitude")
    plt.ylabel("Density")
    plt.show()

"""# Scatter Matrix of Redshift and Magnitudes"""

import seaborn as sns
import matplotlib.pyplot as plt

# Now you can use sns for plotting

# Scatterplot matrix for redshift and magnitudes
sns.pairplot(data[['redshift', 'u', 'g', 'r', 'i', 'z']], kind='scatter', diag_kind='kde', corner=True, palette='coolwarm')
plt.suptitle("Scatter Matrix of Redshift and Magnitudes", y=1.02)
plt.show()

"""# Class distribution across redshift ranges"""

bins = [0, 0.5, 1.0, 1.5]
labels = ['Low', 'Medium', 'High']
data['redshift_range'] = pd.cut(data['redshift'], bins=bins, labels=labels)
sns.countplot(x='redshift_range', hue='class', data=data, palette='Set1')
plt.title("Class Distribution Across Redshift Ranges")
plt.xlabel("Redshift Range")
plt.ylabel("Count")
plt.show()

"""# Model Building"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

"""# Random Forest Classifier"""

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

"""# Support Vector Machine"""

svm_model = SVC(kernel='linear', probability=True)
svm_model.fit(X_train, y_train)

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

from sklearn.metrics import roc_curve, roc_auc_score

# Evaluate Random Forest
rf_predictions = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_predictions)

"""# Random Forest Accuracy"""

print("Random Forest Accuracy:", rf_accuracy)

"""# Random Forest Classification Report"""

print("Random Forest Classification Report:\n", classification_report(y_test, rf_predictions))

# Evaluate SVM
svm_predictions = svm_model.predict(X_test)
svm_accuracy = accuracy_score(y_test, svm_predictions)

"""# SVM Accuracy"""

print("SVM Accuracy:", svm_accuracy)

"""# SVM Classification Report"""

|
print("SVM Classification Report:\n", classification_report(y_test, svm_predictions))

"""# Random Forest Confusion Matrix"""

from sklearn.metrics import ConfusionMatrixDisplay

# For Random Forest
cm_rf = confusion_matrix(y_test, rf_model.predict(X_test))
disp_rf = ConfusionMatrixDisplay(confusion_matrix=cm_rf, display_labels=label_encoder.classes_)
disp_rf.plot(cmap='Blues')
plt.title("Random Forest Confusion Matrix")
plt.show()

"""# SVM Confusion Matrix"""

# For SVM
cm_svm = confusion_matrix(y_test, svm_model.predict(X_test))
disp_svm = ConfusionMatrixDisplay(confusion_matrix=cm_svm, display_labels=label_encoder.classes_)
disp_svm.plot(cmap='Oranges')
plt.title("SVM Confusion Matrix")
plt.show()

"""# Neural Network Model Building"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

# Convert target to one-hot encoding for multi-class classification
y_train_encoded = to_categorical(y_train)
y_test_encoded = to_categorical(y_test)

# Define Neural Network architecture
nn_model = Sequential([
    Dense(128, input_dim=X_train.shape[1], activation='relu'),
    Dropout(0.3),  # Dropout for regularization
    Dense(64, activation='relu'),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dense(y_train_encoded.shape[1], activation='softmax')  # Output layer with softmax
])

# Compile the model
nn_model.compile(optimizer=Adam(learning_rate=0.001),
                 loss='categorical_crossentropy',
                 metrics=['accuracy'])

# Display model architecture
nn_model.summary()

"""# Training the Neural Network"""

# Train the model
history = nn_model.fit(X_train, y_train_encoded,
                       validation_data=(X_test, y_test_encoded),
                       epochs=50,
                       batch_size=32,
                       verbose=1)

# Save the model
nn_model.save('neural_network_model.h5')

"""# Evaluation and Visualizations"""

print(data['class'].value_counts())

from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

from sklearn.utils.class_weight import compute_class_weight

class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
class_weights_dict = dict(enumerate(class_weights))
print(class_weights_dict)

history = nn_model.fit(X_train, y_train_encoded,
                       validation_data=(X_test, y_test_encoded),
                       epochs=50,
                       batch_size=32,
                       class_weight=class_weights_dict,
                       verbose=1)

from sklearn.metrics import classification_report

print(classification_report(y_true, y_pred, target_names=label_encoder.classes_))

# Predict classes
y_pred_encoded = nn_model.predict(X_test)
y_pred = np.argmax(y_pred_encoded, axis=1)
y_true = np.argmax(y_test_encoded, axis=1)

# Confusion matrix
cm = confusion_matrix(y_true, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

"""#Training History Visualization"""

plt.figure(figsize=(10, 6))


plt.plot(history.history['accuracy'], label='Training Accuracy', color='blue')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy', color='blue', linestyle='dashed')


plt.plot(history.history['loss'], label='Training Loss', color='red')
plt.plot(history.history['val_loss'], label='Validation Loss', color='red', linestyle='dashed')


plt.title('Model Accuracy and Loss')
plt.xlabel('Epochs')
plt.ylabel('Value')
plt.legend()
plt.grid(True)


plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Extract feature importance from Random Forest
feature_importances = rf_model.feature_importances_
features = data.drop(columns=['class']).columns

# Sort features by importance
sorted_indices = np.argsort(feature_importances)[::-1]
sorted_features = features[sorted_indices]
sorted_importances = feature_importances[sorted_indices]

# Plot feature importance
plt.figure(figsize=(10, 6))
plt.barh(sorted_features, sorted_importances, color='skyblue')
plt.gca().invert_yaxis()
plt.title("Feature Importance (Random Forest)")
plt.xlabel("Importance Score")
plt.ylabel("Features")
plt.show()

from sklearn.metrics import confusion_matrix
import seaborn as sns

# Function to plot confusion matrix
def plot_conf_matrix(y_true, y_pred, title):
    cm = confusion_matrix(y_true, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
    plt.title(title)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.show()

# Plot for Random Forest
plot_conf_matrix(y_test, rf_predictions, "Confusion Matrix - Random Forest")

# Plot for SVM
plot_conf_matrix(y_test, svm_predictions, "Confusion Matrix - SVM")

# Plot for Neural Network
plot_conf_matrix(y_true, y_pred, "Confusion Matrix - Neural Network")

"""# Class Distribution by Model Predictions"""

# Add predictions to a DataFrame for comparison
predictions_df = pd.DataFrame({
    'Random Forest': rf_predictions,
    'SVM': svm_predictions,
    'Neural Network': y_pred,
    'True': y_test
})

# Melt the DataFrame for visualization
melted = predictions_df.melt(var_name="Model", value_name="Predicted Class")

# Plot class distribution for each model
sns.countplot(data=melted, x="Predicted Class", hue="Model", palette="Set2")
plt.title("Class Distribution by Model Predictions")
plt.xlabel("Predicted Class")
plt.ylabel("Count")
plt.legend(title="Model")
plt.show()

