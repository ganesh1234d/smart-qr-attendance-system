from sqlalchemy import text

from app.database import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT DB_NAME()"))
        print("Connected Successfully!")

        for row in result:
            print("Database :", row[0])

except Exception as e:
    print("Connection Failed!")
    print(e)