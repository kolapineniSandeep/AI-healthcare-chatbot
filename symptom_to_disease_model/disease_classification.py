from data_processor import DataProcessor
from flask import Flask, request
from model import MLModel
app = Flask(__name__)

dataProcessor  = DataProcessor()

diseaseDataFrame = dataProcessor.preprocessDiseaseData("./Data/dataset.csv")
symptomSeverity =  dataProcessor.readAndProcessSSData("./Data/Symptom-severity.csv")
preprocessData =  dataProcessor.convertData(diseaseDataFrame,symptomSeverity)
model = MLModel()
x_test, y_test = model.classificationModel(preprocessData)
model.predict(x_test)
@app.route("/", methods=['POST'])
def index():
    data = request.get_json()
    symptomsList = data.get('symptoms')
    found = set(symptomSeverity.loc[symptomSeverity["Symptom"].isin(symptomsList), "Symptom"])
    not_found = set(symptomsList).difference(found)
    if not not_found: 
        print("result:" , list(found))
        prediction = model.handleChatSymptoms(found, symptomSeverity, diseaseDataFrame)
        return prediction, 200
    else: 
        return "UnKnown Error Occured", 500

if __name__ == "__main__":
    app.run()
