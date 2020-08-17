import psycopg2
def insertMessages(name, sec):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="password123",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="postgres")

        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO public."RANK" (name, play_time) VALUES (%s,%s)"""
        record_to_insert = (name, sec)

        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()

        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")

        # Print PostgreSQL version
        # cursor.execute("SELECT version();")
        # record = cursor.fetchone()
        # print("You are connected to - ", record, "\n")
        #
        # print("Table created successfully in PostgreSQL ")
        # cursor.execute("""SELECT table_name FROM information_schema.tables
        #       WHERE table_schema = 'public'""")
        cursor.execute("""SELECT "name", play_time FROM public."RANK";""")
        for table in cursor.fetchall():
            print(table)

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def get5():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="password123",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="postgres")

        cursor = connection.cursor()
        print(connection.get_dsn_parameters(), "\n")
        cursor.execute("""select * from public."RANK" order by play_time desc limit 5""")
        name = []
        time = []
        for row in cursor.fetchall():
            r = list(row)
            name.append(r[0])
            time.append(r[1])
            print(row)
        print(name)
        print(time)
        print(connection)
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return name, time
if __name__ == '__main__':
    get5()