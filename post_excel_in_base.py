import pandas as pd
import mysql.connector
import re
from datetime import datetime

# Установите соединение с базой данных
conn = mysql.connector.connect(
    host='172.18.11.103',
    # host='localhost',
    user='root',        # Замените на ваше имя пользователя
    password='enigma1418',    # Замените на ваш пароль
    database='mdtomskbot'
)
cursor = conn.cursor()

try:
    # Загрузите данные из Excel
    file_path = 'C:/Users/neverov/Desktop/gaz_1.xlsx'
    sheet_name = 'РЕЕСТР'  # Замените на имя вашего листа
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=2,
                    dtype={'№ п/п': str, 'ФИО заявителя': str,
                        'СНИЛС': str, 'Район': str, 'Адрес нп': str,
                        'Адрес': str, 'Льгота': str, 'Серия и № сертификата': str,
                        'Дата выдачи сертификата': str, 'Размер выплаты': str, 'Сертификат': str,
                        'Дата и № решения о выдаче сертификата': str, 'Дата и № решения об аннулировании сертификата': str, 'Отказ в выдаче сертификата': str,
                        'Основная причина отказа (пункт)': str, 'Дата решения об отказе в выдаче сертификата': str, 'ТРЕК': str,
                        '№ решения об отказе в выдаче сертификата': str,
                        'Дата отправки почтой': str, 'ПАВАПВАПВЫАП': str, 'ТРЕК': str})

    def extract_number(value, default="0.0"):
        import re
        """Извлекает первое число из строки, если оно есть."""
        match = re.search(r"[-+]?\d*[,\.]\d+|\d+", str(value))
        if match:
            number = match.group(0).replace(',', '.') # Заменяем запятую на точку
            if number.endswith(".0"):
                number = number[:-2] # Удаляем ".0" в конце
            return number
            # return match.group(0).replace(',', '.')  # Заменяем запятую на точку для поддержки формата float
        return default

    def extract_date_and_number(value):
        """Извлекает дату и номер из строки."""
        if pd.isna(value):
            return '', ''

        # Попробуем извлечь дату в формате ДД.ММ.ГГГГ или ГГГГ-ММ-ДД
        date_match = re.search(r"\b(\d{2}\.\d{2}\.\d{4})\b|\b(\d{4}-\d{2}-\d{2})\b", str(value))
        if date_match:
            date_value = date_match.group(0)
            remaining_value = value.replace(date_value, '').strip()  # Остальное как номер

            try:
                # Преобразуем строку даты в объект datetime
                parsed_date = datetime.strptime(date_value, '%Y-%m-%d')
                # Возвращаем дату в нужном формате
                return parsed_date.strftime('%d.%m.%Y'), str(remaining_value).replace(' от', '').strip()
            except ValueError:
                return date_value, str(remaining_value).replace(' от', '').strip()

        return '', str(value)

    def safe_date_conversion(value):
        if pd.isna(value):
            return ''  # Возвращаем None для недопустимых значений

        # Попробуем извлечь дату в формате ДД.ММ.ГГГГ или ГГГГ-ММ-ДД
        date_match = re.search(r"\b(\d{2}\.\d{2}\.\d{4})\b|\b(\d{4}-\d{2}-\d{2})\b", str(value))
        if date_match:
            date_value = date_match.group(0)

            try:
                # Преобразуем строку даты в объект datetime
                parsed_date = datetime.strptime(date_value, '%Y-%m-%d')
                # Возвращаем дату в нужном формате
                return parsed_date.strftime('%d.%m.%Y')
            except ValueError:
                return date_value  # Возвращаем исходную строку, если не удаётся распарсить

        return str(value) # Возвращаем None, если не удалось распарсить дату

    # Функции для преобразования данных
    def safe_conversion(value):
        if pd.isna(value):
            return ''
        return str(value)  # Преобразуем в строку, если значение не NaN

    def safe_float_conversion(value):
        if pd.isna(value):
            return "0.0"
        try:
            number_str = extract_number(float(value))
            return f"{number_str}"
        except ValueError:
            return "0.0"

    def safe_int_conversion(value):
        if pd.isna(value):
            return "0"
        try:
            number_str = extract_number(value)
            return f"{number_str}"
        except ValueError:
            return "0"

    # Примените функцию для извлечения даты и номера решения об отказе
    df['Дата решения об отказе в выдаче сертификата'], df['№ решения об отказе в выдаче сертификата'] = zip(*df['Дата и № решения об отказе в выдаче сертификата'].apply(extract_date_and_number))

    # Заполните NaN значения в DataFrame и обработайте данные
    df['№ п/п'] = df['№ п/п'].apply(safe_conversion)
    df['ФИО заявителя'] = df['ФИО заявителя'].apply(safe_conversion)
    df['СНИЛС'] = df['СНИЛС'].apply(safe_int_conversion)
    df['Район'] = df['Район'].apply(safe_conversion)
    df['Адрес нп'] = df['Адрес нп'].apply(safe_conversion)
    df['Адрес'] = df['Адрес'].apply(safe_conversion)
    df['Льгота'] = df['Льгота'].apply(safe_conversion)
    df['Серия и № сертификата'] = df['Серия и № сертификата'].apply(safe_conversion)
    df['Дата выдачи сертификата'] = df['Дата выдачи сертификата'].apply(safe_date_conversion)
    df['Размер выплаты'] = df['Размер выплаты'].apply(safe_float_conversion)
    df['Сертификат'] = df['Сертификат'].apply(safe_int_conversion)
    df['Дата и № решения о выдаче сертификата'] = df['Дата и № решения о выдаче сертификата'].apply(safe_conversion)
    df['Дата и № решения об аннулировании сертификата'] = df['Дата и № решения об аннулировании сертификата'].apply(safe_conversion)

    df['Отказ в выдаче сертификата'] = df['Отказ в выдаче сертификата'].apply(safe_int_conversion)
    df['Основная причина отказа (пункт)'] = df['Основная причина отказа (пункт)'].apply(safe_conversion)
    df['ТРЕК'] = df['ТРЕК'].apply(safe_conversion)
    df['Дата отправки почтой'] = df['Дата отправки почтой'].apply(safe_conversion)

    # Определите SQL-запрос для вставки данных
    insert_query = """
    INSERT INTO services (
        id_id, name, snils, location, address_p, address, benefit, number, year, cost,
        certificate, date_number_get, date_number_cancellation, date_number_no_one, date_number_no_two,
        certificate_no, reason, track, date_post, comment, color
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    """

    # Подготовьте данные для вставки
    data_to_insert = []
    for _, row in df.iterrows():
        if pd.notna(row.get('ФИО заявителя')) and row.get('ФИО заявителя').strip():
            # Проверяем значение 'Сертификат' для заполнения колонки 'Цвет'
            certificate_value = safe_int_conversion(row.get('Сертификат'))
            refusal_value = safe_int_conversion(row.get('Отказ в выдаче сертификата'))
            color_value = "#dff0d8" if certificate_value == "0" and refusal_value == '0' else ""

            data_row = (
                safe_conversion(row.get('№ п/п')),
                safe_conversion(row.get('ФИО заявителя')),
                safe_int_conversion(row.get('СНИЛС')),
                safe_conversion(row.get('Район')),
                safe_conversion(row.get('Адрес нп')),
                safe_conversion(row.get('Адрес')),
                safe_conversion(row.get('Льгота')),
                safe_conversion(row.get('Серия и № сертификата')),
                safe_date_conversion(row.get('Дата выдачи сертификата')),
                safe_float_conversion(row.get('Размер выплаты')),
                safe_int_conversion(row.get('Сертификат')),
                safe_conversion(row.get('Дата и № решения о выдаче сертификата')),
                safe_conversion(row.get('Дата и № решения об аннулировании сертификата')),

                safe_conversion(row.get('Дата решения об отказе в выдаче сертификата')),
                safe_conversion(row.get('№ решения об отказе в выдаче сертификата')),

                safe_int_conversion(row.get('Отказ в выдаче сертификата')),
                safe_conversion(row.get('Основная причина отказа (пункт)')),
                safe_conversion(row.get('ТРЕК')),
                safe_conversion(row.get('Дата отправки почтой')),
                "",  # Пустая строка для поля 'comment'
                color_value
            )

            data_to_insert.append(data_row)

    if data_to_insert:
        # Вставьте данные в базу данных
        cursor.executemany(insert_query, data_to_insert)
        conn.commit()
        print('Данные загружены')
    else:
        print('Данные НЕ загружены')

except Exception as e:
    # Вывод подробной информации об ошибке
    print(f"Поймано исключение: {type(e).__name__}")
    print(f"Сообщение об ошибке: {str(e)}")
    import traceback
    print("Трассировка стека (stack trace):")
    traceback.print_exc()

finally:
    # Закройте соединение
    cursor.close()
    conn.close()