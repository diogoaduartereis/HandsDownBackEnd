from config import insert_one


def insert_transcription(transcription):
    """ insert a new transcription into the transcriptions table """
    sql = """INSERT INTO transcriptions(user_id, processed_transcription)
    VALUES(%s, %s)"""
    insert_one(sql, transcription)


if __name__ == "__main__":
    insert_transcription((
        1,
        "Isto é uma transcrição pequena"))
