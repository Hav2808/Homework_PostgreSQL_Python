import psycopg2


# Функция, создающая структуру БД (таблицы)
# Функция, позволяющая добавить нового клиента
# Функция, позволяющая добавить телефон для существующего клиента
# Функция, позволяющая изменить данные о клиенте
# Функция, позволяющая удалить телефон для существующего клиента
# Функция, позволяющая удалить существующего клиента
# Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE phones;
        DROP TABLE person;
        """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS person(
                        id SERIAL PRIMARY KEY,
                        first_name VARCHAR(100) NOT NULL,
                        second_name VARCHAR(100) NOT NULL,
                        email VARCHAR(100) UNIQUE
                    );
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS phones(
                        id SERIAL PRIMARY KEY,
                        number VARCHAR(100),
                        person_id INTEGER REFERENCES person(id)
                    );
                    """)
        conn.commit()


def add_client(conn):
    with conn.cursor() as cur:
        id = input("Введите порядковый номер клиента: ")
        first_name = input("Введите имя клиента: ")
        second_name = input("Введите фамилию клиента: ")
        email = input("Введите адрес почты клиента: ")
        insert_person = """ INSERT INTO person (id, first_name, second_name, email)
                                      VALUES (%s, %s, %s, %s) RETURNING id, first_name, second_name, email;"""
        item_tuple = (id, first_name, second_name, email)
        cur.execute(insert_person, item_tuple)
        conn.commit()
        print(cur.fetchone())
        print("Список клиентов")
        select_person = """select * from person"""
        cur.execute(select_person)
        print(cur.fetchall())

def add_phone(conn):
    with conn.cursor() as cur:
        id = input("Введите число - номер записи в таблице: ")
        number = input("Введите номер телефона: ")
        person_id = input("Введите персональный номер (id) клиента: ")
        print(number.isnumeric())
        print("*"*50)
        print(len(number))
        if number.isnumeric() == False or len(number) > 12:
            number = 0
            print("Номер телефона не внесен: номер записи, номер телефона = 0, номер клиента ID (из таблицы PERSON)")
        else:
            print(
                    "Номер успешно внесен: номер записи, номер телефона " f"{number}" ", номер клиента ID (из таблицы PERSON)")

        insert_phones = """ INSERT INTO phones (id, number, person_id)
                                       VALUES (%s, %s, %s) RETURNING id, number, person_id;"""
        item_phones = (id, number, person_id)
        cur.execute(insert_phones, item_phones)
        conn.commit()
        print(cur.fetchone())
        print()
        select_phones = """select * from phones"""
        cur.execute(select_phones)
        print(cur.fetchall())
    print("*" * 50)

def change_client(conn):
    with conn.cursor() as cur:
        id = input("Введите число - номер записи в таблице: ")
        print("Строка таблицы до обновления записи")
        select_person = """select * from person where id = %s"""
        cur.execute(select_person, id)
        print(cur.fetchone())
        while (True):
            print()
            print("Введите команду: \neсли хотите изменить имя, наберите: N \nесли фамилию, "
                              "наберите : F \nесли адрес почты, наберите цифру: A \nесли номер телефона, наберите: T")
            select_action = input().lower()
            if select_action == "n":
                print("ВНИМАНИЕ вы вносите изменения в таблице PERSON")
                first_name = input("Наберите другое имя: ")
                update_person = """Update person set first_name = %s where id = %s"""
                cur.execute(update_person, (first_name, id))
                conn.commit()
                count = cur.rowcount
                print(count, "Запись успешно обновлена")
                print()
                print("Обновленная запись")
                select_person = """select * from person where id = %s"""
                cur.execute(select_person, id)
                print(cur.fetchone())

            elif select_action == "f":
                print("ВНИМАНИЕ вы вносите изменения в таблице PERSON")
                second_name = input("Наберите другую фамилию: ")
                update_person = """Update person set second_name = %s where id = %s"""
                cur.execute(update_person, (second_name, id))
                conn.commit()
                count = cur.rowcount
                print(count, "Запись успешно обновлена")
                print()
                print("Обновленная запись")
                select_person = """select * from person where id = %s"""
                cur.execute(select_person, id)
                print(cur.fetchone())
            elif select_action == "a":
                print("ВНИМАНИЕ вы вносите изменения в таблице PERSON")
                email = input("Укажите новую почту: ")
                update_person = """Update person set email = %s where id = %s"""
                cur.execute(update_person, (email, id))
                conn.commit()
                count = cur.rowcount
                print(count, "Запись успешно обновлена")
                print()
                print("Обновленная запись")
                select_person = """select * from person where id = %s"""
                cur.execute(select_person, id)
                print(cur.fetchone())
            elif select_action == "t":
                print("ВНИМАНИЕ вы вносите изменения в таблице PHONES")
                person_id = id
                number = input("Укажите новый телефон: ")
                update_phone = """Update phones set number = %s where person_id = %s"""
                cur.execute(update_phone, (number, person_id))
                conn.commit()
                count = cur.rowcount
                print(count, "Запись успешно обновлена")
                print()
                print("Обновленная запись")
                select_phone = """select * from phones where person_id = %s"""
                cur.execute(select_phone, person_id)
                print(cur.fetchone())
            elif select_action == "q":
                break
            else:
                print("Введите правильную команду или q.")
        print("Таблица после обновления записи")
        select_phone = """select * from phones where person_id = %s"""
        cur.execute(select_phone, person_id)
        print (cur.fetchone())
    print("*" * 50)


def delete_phone(conn): # client_id, phone):
    with conn.cursor() as cur:
        print("ВНИМАНИЕ вы вносите изменения в таблице PHONES")
        select_phones = """select * from phones"""
        cur.execute(select_phones)
        print(cur.fetchall())
        id = input("Укажите ID у которого хотите удалить номер телефона: ")
        delete_phones = """Delete from phones where id = %s"""
        cur.execute(delete_phones, (id,))
        conn.commit()
        count = cur.rowcount
        print(count, "Запись успешно удалена")
        select_phones = """select * from phones"""
        cur.execute(select_phones)
        print(cur.fetchall())
    print("*" * 50)


def delete_client(conn): # client_id
    with conn.cursor() as cur:
        print("ВНИМАНИЕ вы вносите изменения в таблице PERSON и PHONES")
        print("Список клиентов")
        select_person = """select * from person"""
        cur.execute(select_person)
        print(cur.fetchall())
        id = input("Введите число - ID клиента, запись которую хотите удалить в таблице PERSON: ")

        select_phones = """select * from phones"""
        cur.execute(select_phones)
        print(cur.fetchall())
        person_id = id
        delete_phones = """Delete from phones where person_id = %s"""
        cur.execute(delete_phones, (person_id))
        conn.commit()
        count = cur.rowcount
        print("Перечень телефонов в количестве" f"{count}" " записей успешно удален для клиента под номером " f"{id}" " из таблицы PHONES")
        select_phones = """select * from phones"""
        cur.execute(select_phones)
        print(cur.fetchall())

        select_person = """select * from person"""
        cur.execute(select_person)
        print(cur.fetchall())

        delete_person = """Delete from person where id = %s"""
        cur.execute(delete_person, (id,))
        conn.commit()
        count = cur.rowcount
        print(count, "Запись успешно удалена")
        print("Записи имеющиеся в таблице PERSON (ID, имя, фамилия, email")
        select_person = """select * from person"""
        cur.execute(select_person)
        print(cur.fetchall())
    print("*" * 50)



def find_client(conn): # first_name=None, last_name=None, email=None, phone=None)
    with conn.cursor() as cur:
        while (True):
            print()

            print("Введите команду: "
                  "\nдля поиска клиента по ID нажмите : I "
                  "\nдля поиска клиента по имени, наберите : N "
                  "\nдля поиска клиента по фамилию, наберите : F "
                  "\nесли адрес почты, наберите цифру: A "
                  "\nесли номер телефона, наберите: P"
                  "\nq - завершить")
            select_action = input().lower()
            if select_action == "i":
                print("Список клиентов")
                select_person = """select * from person"""
                cur.execute(select_person)
                add_list = cur.fetchall()
                # print(add_list)
                id = int(input("Введите id: "))
                print("ВНИМАНИЕ вы вносите изменения в таблице PERSON и PHONES")
                print("Список клиентов")
                counter = 0
                for el in add_list:
                    list_new = list(el)
                    # print(list_new[0])
                    if list_new[0] == id:
                        print("Клиент по ID = " f"{id}" " найден!")
                        counter = 1
                if counter == 0:
                    print("Клиент по ID = " f"{id}" " не найден!")

                print("*" * 50)

            if select_action == "n":
                print("Список клиентов")
                select_person = """select * from person"""
                cur.execute(select_person)
                add_list = cur.fetchall()
                name_search = str(input("Введите для поиска имя клиента : "))
                print("ВНИМАНИЕ вы вносите изменения в таблице PERSON и PHONES")
                print("Список клиентов")
                counter = 0
                for el in add_list:
                    list_new = list(el)
                    if list_new[1] == name_search:
                        print("Клиент по имени = " f"{name_search}" " найден!")
                        print(list_new)
                        counter = 1
                if counter == 0:
                    print("Клиент по имени = " f"{name_search}" " не найден!")

                print("*" * 50)

            if select_action == "f":
                print("Список клиентов")
                select_person = """select * from person"""
                cur.execute(select_person)
                add_list = cur.fetchall()
                print(add_list)
                name_search = str(input("Введите для поиска фамилии клиента : "))
                print("ВНИМАНИЕ вы вносите изменения в таблице PERSON и PHONES")
                print("Список клиентов")
                counter = 0
                for el in add_list:
                    list_new = list(el)
                    if list_new[2] == name_search:
                        print("Клиент по фамилии = " f"{name_search}" " найден!")
                        print(list_new)
                        counter = 1
                if counter == 0:
                    print("Клиент по фамилии = " f"{name_search}" " не найден!")

                print("*" * 50)

            if select_action == "a":
                # print("Список клиентов")
                # select_person = """select * from person"""
                # cur.execute(select_person)
                # add_list = cur.fetchall()
                # print(add_list)
                name_search = str(input("Введите для поиска клиента его почту (email): "))
                print("ВНИМАНИЕ вы вносите изменения в таблице PERSON и PHONES")
                print("Список клиентов")
                counter = 0
                for el in add_list:
                    list_new = list(el)
                    if list_new[3] == name_search:
                        print("Клиент имеющий данную почту в базе данных = " f"{name_search}" " найден!")
                        print(list_new)
                        counter = 1
                if counter == 0:
                    print("Клиент имеющий данную почту в базе данных = " f"{name_search}" " не найден!")

                print("*" * 50)

            if select_action == "p":
                number = str(input("Введите номер телефона: "))
                select_phones = ("""
                SELECT * FROM person as p
                LEFT JOIN phones AS c ON person_id = p.id;
                """)
                cur.execute(select_phones)
                add_list = cur.fetchall()
                print("="*100)
                counter = 0
                for el in add_list:
                    list_new = list(el)
                    # print(list_new)
                    if list_new[5] == number:
                        # print(list_new[5]) - вся база для отладки
                        print("Клиент имеющий  номер телефона = " f"{number}" " в базе данных найден!")
                        print("Имя клиента: "  f"{list_new[1]}")
                        print("Фамилия клиента: "  f"{list_new[2]}")
                        counter = 1
                if counter == 0:
                    print("Клиент имеющий  номер телефона = " f"{number}" " не найден!")

            if select_action == "q":
                break
            else:
                print("Введите правильную команду или q.")
            print("="*100)

def main():

    with psycopg2.connect(database="CLIENT_db", user="postgres", password="Hawk43601$") as conn:
        while (True):
            print()
            print("Введите команду:")
            print(
                "Справочно:\ncr - команда которая позволяет создать новую таблицу; "
                "\nс команда которая позволяет ввести данные клиента ( id = порядковый номер клиента в таблице PERSON, first_name = имя клиента, second_name = фамилию клиента, email = адрес почты клиента); "
                "\nh - команда которая позволяет ввести номер телефона (телефонов) клиента (id = порядковый номер клиента в таблице PHONES, number = номер телефона,"
                " person_id = номер ID из таблицы PERSON; \nch - команда которая позволяет изменить данные в таблицах; "
                "\ndel - команда которая позволяет изменить данные в таблицах: состав строки id = порядковый номер клиента в таблице PHONES,"
                " number = номер телефона, person_id = номер ID из таблицы PERSON; \ndc - команда которая позволяет удалить запись о клиенте "
                "в таблицах;\nq - завершить\n")
            command = input().lower()
            if command == "cr":
                create_db(conn)
            elif command == "c":
                print("ВНИМАНИЕ вносите изменения в таблице PERSON")
                add_client(conn)
            elif command == "h":
                print("ВНИМАНИЕ вносите изменения в таблице PHONES")
                add_phone(conn)
            elif command == "ch":
                change_client(conn)
            elif command == "del":
                delete_phone(conn)
            elif command == "dc":
                delete_client(conn)
            elif command == "f":
                find_client(conn)
            elif command == "q":
                break
            else:
                print("Введите правильную команду или q.")

main()


with psycopg2.connect(database="CLIENT_db", user="postgres", password="Hawk43601$") as conn:
    if __name__ == '__main__':
        main()






