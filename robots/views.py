import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .excel import create_robot_summary_excel
from .models import Robot
import json
from .forms import LoginForm
from django.contrib.auth import login as auth_login


@csrf_exempt  # Временное отключение CSRF-защиты (настроить для безопасности)
def request_robot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Валидация данных и создание объекта Robot
        # Обработка ошибок валидации, если необходимо
        try:
            new_robot = Robot(
                model=data['model'],
                version=data['version'],
                created=data['created'],
                available=True  # По умолчанию ставим, что робот доступен
            )

            new_robot.save()

            # Проверка доступности робота
            if new_robot.available:
                # Отправить письмо клиенту
                customer_email = "elelion@yandex.ru"  # Замените на реальный адрес клиента
                robot_model = data['model']
                robot_version = data['version']
                message_text = f"""
                    Добрый день!
                    Недавно вы интересовались нашим роботом модели {robot_model}, 
                    версии {robot_version}.
                    Этот робот теперь в наличии. Если вам подходит этот 
                    вариант - пожалуйста, свяжитесь с нами.
                    """
                MailSend(customer_email, message_text)

            return JsonResponse({'message': 'Робот успешно создан'}, status=200)

        except KeyError:
            return JsonResponse({'error': 'Некорректные данные'}, status=400)

    return JsonResponse({'message': 'GET-запрос обработан'}, status=200)


def download_robot_summary(request):
    # Вызов функции для создания файла
    excel_file = create_robot_summary_excel()

    # Отправка файла как ответ на запрос
    with open(excel_file, 'rb') as file:
        # для загрузки с браузера
        # response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # для загрузки в проект
        response = FileResponse(file)
        response['Content-Disposition'] = 'attachment; filename="robot_summary.xlsx"'
        return response



@csrf_exempt
def request_robot(request):
    # Замените на реальную модель
    robot_model = "R2"

    # Замените на реальную версию
    robot_version = "D2"

    # Проверка доступности робота
    if robot_is_available(robot_model, robot_version):
        # Отправить письмо клиенту
        mail_receiver_address = "elelion@yandex.ru"  # Замените на реальный адрес клиента

        message_text = f"""
            Добрый день!
            Недавно вы интересовались нашим роботом модели {robot_model}, 
            версии {robot_version}.
            Этот робот теперь в наличии. Если вам подходит этот 
            вариант - пожалуйста, свяжитесь с нами.
            """

        MailSend(mail_receiver_address, message_text)


def robot_is_available(model, version):
    try:
        # Попытка найти робота с заданной моделью и версией
        robot = Robot.objects.get(model=model, version=version)
        # Если робот найден и поле available равно True, то робот доступен
        return robot.available

    except Robot.DoesNotExist:
        # Если робот не найден, он не доступен
        return False


def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('home')  # Измените на URL-шаблон, на который хотите перенаправить пользователя после входа
    else:
        form = LoginForm(request)

    return render(request, 'robots/login.html', {'form': form})



# -----------------------------------------------------------------------------


class MailSend:
    def __init__(self, mail_receiver_address, mail_body, file_path="settings.conf"):
        self.mail_sender_login = ''
        self.mail_sender_password = ''
        self.mail_subject = 'Робот доступен в наличии'

        self.mail_receiver_address = mail_receiver_address
        self.mail_body = mail_body

        self.settings = {}
        self.settings_loaded = False

        self.file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), file_path)

        print("MailSend - Загружаем конфиг из:", self.file_path)
        self()

    # загружаем данные из конфига в словарь settings.conf
    def __load_settings(self):
        with open(self.file_path, 'r') as file:
            for line in file:
                line = line.strip()  # Удаляем лишние пробелы и символы перевода строки

                if line and not line.startswith('#'):  # Пропускаем пустые строки и комментарии
                    key, value = line.split('=')  # Разделяем ключ и значение
                    key = key.strip()  # Удаляем лишние пробелы в ключе
                    value = value.strip()  # Удаляем лишние пробелы в значении
                    self.settings[key] = value  # Добавляем ключ и значение в словарь settings.conf

            print("MailSend - Данные успешно занесены в переменные")

    # парсим данные по переменным из словаря settings.conf
    def __apply_settings(self):
        self.mail_sender_login = self.settings.get('mail_sender_login')
        self.mail_sender_password = self.settings.get('mail_sender_password')
        self.settings_loaded = True
        print("MailSend - Данные успешно загружены")

    # отправляем письмо
    def __send_email(self, sender_email, sender_password, receiver_email, subject, body):
        try:
            # Создание объекта MIMEText
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject

            # Добавление текста письма в объект MIMEText
            msg.attach(MIMEText(body, 'plain'))

            # Установка соединения с SMTP-сервером
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()

            # Авторизация на сервере
            server.login(sender_email, sender_password)

            # Отправка письма
            server.sendmail(sender_email, receiver_email, msg.as_string())

            # Закрытие соединения с сервером
            server.quit()
            print("Письмо успешно отправлено!")
        except Exception as e:
            print("Ошибка при отправке письма:", e)


    # делаем класс ф-цией, так же делаем проверку, если данные уже загружены
    # мы их НЕ загружаем повторно
    def __call__(self):
        if not self.settings_loaded:
            self.__load_settings()
            self.__apply_settings()

        print(
              self.mail_receiver_address,
              self.mail_subject)
        self.__send_email(
            self.mail_sender_login,
            self.mail_sender_password,
            self.mail_receiver_address,
            self.mail_subject,
            self.mail_body)