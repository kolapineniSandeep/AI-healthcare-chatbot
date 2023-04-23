import random
from waitress import serve
from flask import Flask, request

from appointment_service import *
from dataset import *
from model import *
from autocorrect import Speller
from database import *
from flask_cors import CORS
from symptoms_model import SymptomsMLModel
from faker import Faker
import random
import datetime
from waitress import serve

app = Flask(__name__)
CORS(app)

### START PRE PROCESS STEPS ###
dataset = dataset()
dataset.process_data()
model = model()
spell = Speller(lang='en')
database = database()
database.create_connection()
database.create_tables()
symptoms_ml = SymptomsMLModel()
fake = Faker()


### END PRE PROCESS STEPS ###

@app.route('/ask', methods=['GET', 'POST'])
def index():
    request_data = request.get_json()
    previous_questions = []
    question = None
    answers = []
    intent = None
    if request_data:
        if 'previous_questions' in request_data:
            previous_questions = request_data['previous_questions']
        if 'question' in request_data:
            question = request_data['question']
        if 'answers' in request_data:
            answers = request_data['answers']
        if 'intent' in request_data:
            intent = request_data['intent']

    if model.model_trained:

        if intent not in ['BookAppointment', 'CancelAppointment', 'RescheduleAppointment']:
            question = spell(question)
            intent_current = model.predict(question)
            if "INVALID" != intent_current:
                answer = random.choice(dataset.responses[intent_current])
                if not (answer and answer.strip()):
                    answer = "I have not Trained on " + intent_current
            else:
                answer = "SORRY! I cant help you with that, I have not trained on that"
            intent = intent_current
        else:
            answer = find_work_flow(previous_questions, question, answers, intent)
            intent = ''

        answers.append(answer)
        previous_questions.append(question)
        question = ''
        return {"previous_questions": previous_questions, "question": question, "answers": answers, "intent": intent}
    else:
        return "MODEL IS NOT TRAINED, CONTACT TEAM!!"


@app.route('/test', methods=['GET', 'POST'])
def test():
    request_data = request.get_json()

    questions = []
    answers = []
    if request_data:

        if 'question' in request_data:
            questions = request_data['question']

    if model.model_trained:
        for question in questions:
            question = spell(question)
            intent = model.predict(question)

            if "INVALID" != intent:
                answer = random.choice(dataset.responses[intent])
                if not (answer and answer.strip()):
                    answer = "I have not Trained on " + intent
            else:
                answer = "SORRY! I cant help you with that, I have not trained on that"
            answers.append(
                {"question": question, "answer": answer, "intent": intent})
        return answers
    else:
        return "MODEL IS NOT TRAINED, CONTACT TEAM!!"


@app.route('/train')
def train():
    epochs = int(request.args.get('epochs', default=64))
    batch_size = request.args.get('batch', default=64)
    model.tain_model(dataset.data, epochs, batch_size)
    return "MODEL TRAINED, USE /ask ENDPOINT"


@app.route('/all_appointments', methods=['GET', 'POST'] )
def get_all_appointments():
    return database.get_all_appointments()


def find_work_flow(previous_questions, question, answer, intent):
    answer = ''

    if intent == 'BookAppointment':

        answer = book_appointment_work_flow(question)
    elif intent == 'CancelAppointment':
        answer = cancel_appointment_work_flow(question)
    elif intent == 'RescheduleAppointment':
        answer = reschedule_appointment_work_flow(question)
    else:
        answer = 'I am unable to understand the question'

    return answer


def book_appointment_work_flow(question):
    # split question for name , email, diseases
    # exameple::  sandeeep<sandeepk@gmail.com<fever|cough|cold
    questions = question.split('<')
    name = questions[0]
    email = questions[1]
    symptoms = questions[2].split("|")  # fever|cough|cold
    symptoms_dict = {symptom: random.randint(30, 95) for symptom in symptoms}
    department=symptoms_ml.handleChatSymptoms(symptoms_dict)
    doctor = fake.name()
    appointment_date = fake.date_between_dates(
        date_start=datetime.datetime.now().date(),
        date_end=datetime.datetime.now().date() + datetime.timedelta(days=random.randint(1, 7))
    ).strftime('%Y-%m-%d')
    severity = 5
    return book_appointment(name, email, appointment_date, doctor, department, severity)


def cancel_appointment_work_flow(question):
    # expecting email

    return cancel_appointment(question)


def reschedule_appointment_work_flow(question):
    # expecting email

    return "We will contact you with possible dates soon "


@app.route("/trainDisease")
def train_Disease():
    df = symptoms_ml.read_csv_file('./symptoms_to_disease/data/cleaned_disease_symptoms.csv')
    symptoms_ml.trainModel(df)
    return "MODEL TRAINED, USE /getDisease ENDPOINT"


@app.route("/getDisease", methods=['POST'])
def get_Disease():
    data = request.get_json()
    disease = symptoms_ml.handleChatSymptoms(data)
    return disease


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
