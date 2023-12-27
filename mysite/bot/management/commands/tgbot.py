from django.core.management.base import BaseCommand
from django.conf import settings
import telebot
from telebot import TeleBot
from bot.models import Profile
from bot.models import Message

class DirectionBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.questions = [
            "",
            "1. Хотели бы вы посетить столицу России?",
            "2. Заинтересованы ли вы в посещении города, который был построен на множестве островов?",
            "3. Интересует ли вас осмотр достопримечательностей в самом большом городе России?",
            "4. Хотели бы вы посетить город, расположенный на границе Европы и Азии?",
            "5. Хотели бы вы посетить крупный город в Сибири?",
            "6. Хотели бы вы отправиться в город, который является центром науки и образования в России?",
            "7. Хотели бы вы отправиться в город, который является одним из крупнейших туристических центров России?",
            "8. Хотели бы вы отправиться в город, который является культурным, политическим и экономическим центром России?",
            "9. Интересует ли вас поездка в город, который имеет историческое значение для Сибири и России в целом?",
            "10. Вам интересно посетить город, где проводятся многочисленные культурные мероприятия и фестивали?",
            "11. Хотели бы вы посетить крупный город на реке Оби?",
            "12. Интересует ли вас осмотр знаменитых дворцов и садов города?"
        ]
        self.current_question = 0

        self.city = {
            'Москва': "Рекоменду посетить город Москва и такие места в нем как:\nБункер-42 на Таганке. Адрес:5-й Котельнический переулок, дом 11.\nСмотровая площадка башни «ОКО». Адрес: 1-й Красногвардейский проезд 21/2.\nОстанкинская телебашня. Адрес: ул. Академика Королёва, дом 15, корпус 2.",
            'Санкт-Петербург': "Рекоменду посетить город Санкт-Петербург и такие места в нем:\nПарк аттракционов Диво Остров. Адрес: м. Крестовский остров.\nЭкскурсии в темноте «Мир на ощупь». Адрес: ТРЦ Питерлэнд, Приморский пр., 72, 2 этаж.\n Океанариум «Нептун». Адрес: ул. Марата, 86.",
            'Екатеринбург': "Рекоменду посетить город Екатеринбург и такие места в нем:\nМузей Бориса Ельцина. Адрес: ул. Бориса Ельцина, 3.\nUral Vision Gallery.  Адрес: ул. Шейнкмана, 10.\nСмотровая площадка в «Высоцком». Адрес: ул. Малышева 51, 52 этаж.",
            'Новосибирск': "Рекоменду посетить город Новосибирск и такие места в нем:\nАквапарк «Аквамир». Адрес: улица Яринская, 8.\nМузей мировой погребальной культуры.  Адрес: поселок Восход, улица Военторговская, дом 4/16.\nЦентральный сибирский ботанический сад. Адрес: Золотодолинская, 101."
        }

        self.user_answers = {}

    def restart(self, message):
        self.current_question = 0
        self.user_answers = {}
        self.start(message)

    def start(self, message):
        self.bot.send_message(message.chat.id, "Привет, я бот помогающий выбрать город в России для посещения, а так же хорошие места для время провождения, ответь на пару вопросов и я помогу тебе, хочешь начать?")

    def ask_question(self, message):
        user_answer = message.text.lower()
        if user_answer == 'да' or user_answer == 'нет':
            # Сохраняем ответ пользователя
            self.user_answers[self.current_question] = user_answer

            self.current_question += 1

            if self.current_question < len(self.questions):
                self.bot.send_message(message.chat.id, self.questions[self.current_question])
            else:
                self.calculate_direction(message)
        else:
            self.bot.send_message(message.chat.id, "Пожалуйста, ответьте 'Да' или 'Нет'.")
            self.current_question += 0

    def calculate_direction(self, message):
    # Подсчет количества ответов "Да" для каждого города
        city_count = {city: 0 for city in self.city}

        for question_num, answer in self.user_answers.items():
            if answer == 'да':
                for direction, question_numbers in settings.DIRECTIONS_QUESTIONS.items():
                    if question_num in question_numbers:
                        city_count[direction] += 1

    # Выбор города с максимальным количеством ответов "Да"
        max_count = max(city_count.values())
        global recommended_city
        recommended_city = [city for city, count in city_count.items() if count == max_count]

        if len(recommended_city) == 1:
            recommended_city = recommended_city[0]
            response_text = self.city.get(recommended_city)
            self.bot.send_message(message.chat.id, response_text)
        else:
             self.bot.send_message(message.chat.id, "Я не могу подобрать вам город для посещения.")

        additional_question = "Хотели бы вы получать интересную информацию о новых интересных места в городах?"
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.row('Да', 'Нет')
        self.bot.send_message(message.chat.id, additional_question, reply_markup=markup)   

    def handle_additional_question(self, message):
        user_answer = message.text.lower()
        if user_answer == 'да':
            self.bot.send_message(message.chat.id, "Отлично! Буду стараться радовать тебя информацией.")
            chat_id = message.chat.id
            profiles, _ = Profile.objects.get_or_create(
                external_id=chat_id,
                defaults={'name': message.from_user.username}
            )
            Message(
                profile =profiles,
                text = recommended_city,
                send = user_answer,
            ).save()
            self.restart(message)
        elif user_answer == 'нет':
            self.bot.send_message(message.chat.id, ":Жаль. Хорошего время провождения!")
            chat_id = message.chat.id
            prof, _ = Profile.objects.get_or_create(
                external_id=chat_id,
                defaults={'name': message.from_user.username}
            )
            Message(
                profile =prof,
                text = recommended_city,
                send = user_answer,
            ).save()
            self.restart(message)
        else:
            self.bot.send_message(message.chat.id, "Пожалуйста, ответьте 'Да' или 'Нет'.")

    def run(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.start(message)

        @self.bot.message_handler(func=lambda message: True)
        def handle_messages(message):
            if self.current_question < len(self.questions):
                self.ask_question(message)
            else:
                self.handle_additional_question(message)

        self.bot.polling()

class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **kwargs):
        bot = TeleBot(settings.TOKEN, threaded=False)
        direction_bot = DirectionBot(settings.TOKEN)
        direction_bot.run()