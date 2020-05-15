import psycopg2
from config import config


def insert_vendor(user_name):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO users(email, password, name) VALUES(%s, %s, %s) RETURNING vendor_id;"""
    conn = None
    user_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (user_name,))
        # get the generated id back
        user_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_user_list(user_list):
    """ insert a new user into the users table """
    sql = """INSERT INTO users(email, password, name) VALUES(%s, %s, %s)"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql, user_list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
     insert_user_list([
        ('admin@admin.com', 'admin', 'admin',),
        ('diogo@diogo.com', 'diogo', 'diogo',)
    ])