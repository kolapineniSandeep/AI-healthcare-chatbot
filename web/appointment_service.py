import pygmail
from app import *


def book_appointment(name, email, appointment_date, doctor, department, severity):
    try:
        database.create_connection()
        val = database.add_appointment(name, email, appointment_date, doctor, department, severity)
        if val > 0:
            sub = "Confirmed: Doctor Appointment Booked"

            msg = "Hey " + name + ",\n\nYour Appointment has been Successfully Booked with Dr." + doctor + " of Department "+ department + "\n\n Date : " + appointment_date + "\n Thank you for using AI Healthcare Chatbot."
            pygmail.send_email(email, sub, msg)
            return "SUCCESS! CONFORMATION SEND TO " + email
        else:
            return "UNABLE TO CREATE APPOINTMENT! I am figuring out"
    except Exception as e:
        print(e)
        return "UNABLE TO CREATE APPOINTMENT! I am figuring out"

def cancel_appointment(email):
    try:
        database.create_connection()
        val = database.get_appointment(email)
        if len(val) >0:
            database.remove_appointment(email)
            sub = "CANCELLED: Doctor Appointment "

            msg = "Hey " + val[0][0] + ",\n\nYour Appointment has been CANCELLED Booked with Dr." + val[0][3] + "\n\nDate : " + \
                  val[0][2] + "\n Thank you for using AI Healthcare Chatbot."

            pygmail.send_email(email, sub, msg)
            return "SUCCESSFULLY Canceled! CONFORMATION SEND TO " + email
        else:
            return "UNABLE TO FIND YOUR APPOINTMENT! DID THIS CORRECT EMAIL ? " + email
    except Exception as e:
        print(e)
        return "INTERNAL DB ERROR! I am figuring out"



def reschedule_appointment(appointment):
    pass
