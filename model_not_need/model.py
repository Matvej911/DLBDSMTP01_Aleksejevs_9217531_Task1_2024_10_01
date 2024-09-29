import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle

try:
    df = pd.read_csv('dataset.csv')
except Exception as e:
    print(f"Error reading the file: {e}")
    raise


df.drop_duplicates(inplace=True)


if not all(col in df.columns for col in ['temperature', 'humidity', 'sound_volume', 'target']):
    raise ValueError("Some required columns are missing in the dataset.")

X = df[['temperature', 'humidity', 'sound_volume']]
y = df['target']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=50)


scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


models = {
    'Logistic Regression': LogisticRegression(),
    'Random Forest': RandomForestClassifier(),
    'Support Vector Machine': SVC(),
    'K-Nearest Neighbors': KNeighborsClassifier(),
    'Gradient Boosting': GradientBoostingClassifier()
}

best_model = None
best_accuracy = 0


for name, model in models.items():
 
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)

    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)

    accuracy = accuracy_score(y_test, y_pred)


    print(f'Model: {name}, Accuracy: {accuracy:.2f}, CV Average: {cv_scores.mean():.2f}')

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model

with open('best_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print(f'Best model: {best_model.__class__.__name__}, Accuracy: {best_accuracy:.2f}')
