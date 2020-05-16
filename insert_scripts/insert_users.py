from config import insert_multiple, insert_one
from werkzeug.security import generate_password_hash


def insert_user(user):
    """ insert a new vendor into the vendors table """
    sql_statement = """INSERT INTO
    users(email, password,
    name) VALUES(%s, %s, %s);"""
    insert_one(sql_statement, user)
    # user_id = None


def insert_user_list(user_list):
    """ insert a new user into the users table """
    sql_statement = """INSERT INTO users(email,
    password, name)
    VALUES(%s, %s, %s)
    ON CONFLICT ON CONSTRAINT users_email_key
    DO
    UPDATE
    SET password = EXCLUDED.password"""
    insert_multiple(sql_statement, user_list)


if __name__ == "__main__":
    insert_user_list([
        ('admin@admin.com',
            generate_password_hash('admin', method='sha256'),
            'admin',),
        ('diogo@diogo.com',
            generate_password_hash('diogo', method='sha256'),
            'diogo',)
    ])
