from django.contrib import admin
from .models import Profile
from .models import Message
from .forms import ProfileForm
import telebot
from django.conf import settings

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name')
    form = ProfileForm

@admin.register(Message)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'text', 'created_at', 'send')
    list_filter = ('send',)
    def show_message(self, request, queryset):
        bot_token = settings.TOKEN  
        bot = telebot.TeleBot(bot_token)
        message_text = "Здравствуйте! Вы недавно проходили анкетирование, наш бот обновился, можете пройти тест занова."
        for message in queryset:
            chat_id = message.profile.external_id
            bot.send_message(chat_id, message_text)

        self.message_user(request, "Рассылка запущена")
    show_message.short_description = "Создать рассылку"

    actions = [show_message]