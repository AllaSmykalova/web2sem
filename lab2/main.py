from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Основная страница
@app.route('/')
def index_page():
    return render_template('index.html')


# Страница отображения данных запроса
@app.route('/request-data')
def request_data():
    url_params = request.args
    headers = request.headers
    cookies = request.cookies
    form_data = request.form
    return render_template('request_data.html', url_params=url_params, headers=headers, cookies=cookies, form_data=form_data)

# Регулярное выражение для допустимых символов в номере телефона
PHONE_REGEX = re.compile(r'^[\d\s\-\(\)\.\+]+$')

@app.route('/validate-phone', methods=['GET', 'POST'])
def validate_phone():
    error = None
    validated_phone = None
    phone = None

    if request.method == 'POST':
        phone = request.form.get('phone', '')

        # Проверяем, что введенный номер телефона содержит только допустимые символы
        if not PHONE_REGEX.match(phone):
            error = 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'
        else:
            # Очищаем телефон от всех символов, кроме цифр
            cleaned_phone = ''.join(filter(str.isdigit, phone))

            # Проверяем количество цифр
            if len(cleaned_phone) not in [10, 11]:
                error = 'Недопустимый ввод. Неверное количество цифр.'
            elif len(cleaned_phone) == 11 and not (cleaned_phone.startswith('8') or cleaned_phone.startswith('7')):
                error = 'Недопустимый ввод. Неверное количество цифр.'
            else:
                # Преобразование номера телефона в формат 8----
                if cleaned_phone.startswith('7'):
                    cleaned_phone = '8' + cleaned_phone[1:]
                validated_phone = f"8-{cleaned_phone[1:4]}-{cleaned_phone[4:7]}-{cleaned_phone[7:9]}-{cleaned_phone[9:]}"
    
    return render_template('form.html', error=error, phone=phone, validated_phone=validated_phone)


if __name__ == '__main__':
    app.run(debug=True)
