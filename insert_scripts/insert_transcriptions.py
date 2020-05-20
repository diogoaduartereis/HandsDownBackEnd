from config import insert_one, insert_multiple

sql_statement = """INSERT INTO transcriptions(user_id, processed_transcription)
    VALUES(%s, %s)"""

def insert_transcription(transcription):
    insert_one(sql_statement, transcription)

def insert_transcription_list(transcription_list):
    insert_multiple(sql_statement, transcription_list)

if __name__ == "__main__":
    insert_transcription_list([(
        1,
        """ The SOAP note (an acronym for subjective, objective, assessment, and plan) is a method of documentation employed by healthcare providers to write out notes in a patient's chart, along with other common formats, such as the admission note.
        [1][2] Documenting patient encounters in the medical record is an integral part of practice workflow starting with appointment scheduling, patient check-in and exam, documentation of notes, check-out, rescheduling, and medical billing.
        [3] Additionally, it serves as a general cognitive framework for physicians to follow as they assess their patients.[1]
The SOAP note originated from the problem-oriented medical record (POMR), developed nearly 50 years ago by Lawrence Weed, MD.[1][4] 
It was initially developed for physicians to allow them to approach complex patients with multiple problems in a highly organized way.[4] 
Today, it is widely adopted as a communication tool between inter-disciplinary healthcare providers as a way to document a patient's progress.[1]

SOAP notes are commonly found in electronic medical records (EMR) and are used by providers of various backgrounds.[2] 
Generally, SOAP notes are used as a template to guide the information that physicians add to a patient's EMR.[2] 
Prehospital care providers such as emergency medical technicians may use the same format to communicate patient information to emergency department clinicians.[5]
Due to its clear objectives, the SOAP note provides physicians a way to standardize the organization of a patient's information to reduce confusion when patients are seen by various members of healthcare professionals.[2] Many healthcare providers, 
ranging from physicians to behavioral healthcare professionals to veterinarians, use the SOAP note format for their patient's initial visit and to monitor progress during follow-up care.[4][6][7]  """)
        , (1, "Isto é uma transcrição pequena")])
