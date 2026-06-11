import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

df = pd.read_csv("dataset/ransomware_dataset.csv")

encoder = LabelEncoder()
df["Threat"] = encoder.fit_transform(df["Threat"])

X = df.drop("Threat", axis=1)
y = df["Threat"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

pickle.dump(
    model,
    open("models/ransomware_model.pkl", "wb")
)

print("Model Trained Successfully")