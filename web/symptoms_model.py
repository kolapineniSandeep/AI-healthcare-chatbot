from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import json


class SymptomsMLModel:

    randomForestClassifier = RandomForestClassifier()
    scaler = StandardScaler()
    department_dict ={}

    def __init__(self):
        with open('./symptoms_to_disease/data/department.json', 'r') as f:
            self.department_dict = json.load(f)

    def getDepartment(self, disease):
        if disease in self.department_dict:
            return self.department_dict[disease]
        else:
            return "General Surgery"

    def read_csv_file(self,filepath):
        df = pd.read_csv(filepath)
        return df

    def trainModel(self, df):
        X = df.drop('disease', axis=1)
        y = df['disease']
        x_train, x_test, y_train, y_test = train_test_split(X, y , train_size=0.8, random_state=42)
        X_train_scaled = self.scaler.fit_transform(x_train)
        X_test_scaled = self.scaler.transform(x_test)
        self.randomForestClassifier.fit(X_train_scaled, y_train)
        y_pred_rfc = self.randomForestClassifier.predict(X_test_scaled)

    def predict(self, symptoms):
        x = np.array(symptoms).reshape(1, -1)
        scaled_test = self.scaler.transform(x)
        preds = self.randomForestClassifier.predict(scaled_test)
        return preds[0]

    def handleChatSymptoms(self, chat_input):
        with open('./symptoms_to_disease/data/symptoms.json', 'r') as f:
            symptoms_json = json.load(f)
        for key, value in chat_input.items():
            if key in symptoms_json:
                symptoms_json[key] = value

        values = [symptoms_json[key] for key in symptoms_json]
        return self.getDepartment(self.predict(values))





