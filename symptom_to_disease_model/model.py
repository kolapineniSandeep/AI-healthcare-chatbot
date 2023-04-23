from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import numpy as np

class MLModel:

    SVMClassifier = SVC()
    
    def classificationModel(self, df):
        data = df.iloc[:,1:].values
        labels = df['Disease'].values
        x_train, x_test, y_train, y_test = train_test_split(data, labels, train_size = 0.8,random_state=42)
        self.SVMClassifier.fit( x_train, y_train)
        return x_test, y_test


    def predict(self, x_test):
        preds = self.SVMClassifier.predict(x_test)
        return preds

    def handleChatSymptoms(self, symptoms, df , diseaseDataFrame):
        symptomslist = df["Symptom"].to_list()
        indices = []
        for element in symptoms:
            try:
                index = symptomslist.index(element)
                indices.append(index)
            except ValueError:
                print(f"Symptom {element} not found in the symptomslist")
        indices.extend([0] * (len(diseaseDataFrame.columns) - len(indices) -1))
        print(indices)
        a = np.array(df["Symptom"])
        b = np.array(df["weight"])
        for j in range(len(symptomslist)):
            for k in range(len(a)):
                if symptomslist[j]==a[k]:
                    symptomslist[j]=b[k]
        psy = [indices]
        pred = self.predict(psy)
        print("The prediction is", pred[0])
        return pred[0]
