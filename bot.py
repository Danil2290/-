import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup


API_TOKEN = '8920794171:AAGc_gxUHs0kA-J5Ev52TNQ43eJfKNyGnoY'
PREMIUM_USER_ID = '6074593241'

bot = telebot.TeleBot(API_TOKEN)
bot.remove_webhook()



@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Показывает главное меню при запуске.
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🛒 Каталог", "🔎 Поиск")
    markup.row("👤 Профиль", "ℹ️ О нас")
    markup.row("💬 Отзывы", "❓ Помощь")

    bot.send_message(
        message.chat.id,
        "Привет! Я твой бот-ассистент. Выбери действие.",
        reply_markup=markup
    )



@bot.message_handler(func=lambda message: message.text == "🔎 Поиск")
def start_search(message):
    bot.send_message(message.chat.id, "Введи, что нужно найти...")
    bot.register_next_step_handler(message, process_search)


def process_search(message):
    query = message.text
    try:
        url = f"https://yandex.ru/search/?text={query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        answer = soup.find('div', class_='organic__subtitle')
        if answer:
            bot.send_message(message.chat.id, f"Ответ:\n{answer.text}")
        else:
            bot.send_message(message.chat.id, f"Вот что мне удалось найти. [Смотрите]({url})", parse_mode='Markdown')
    except Exception:
        bot.send_message(message.chat.id, "Ошибка при поиске.")



@bot.message_handler(func=lambda message: message.text == "🛒 Каталог")
def show_catalog(message):
    """
    Показывает каталог с категориями.
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🖥️ Компьютеры", "📱 Техника Apple")
    markup.row("📦 Другие товары", "⬅️ Назад")

    bot.send_message(
        message.chat.id,
        "Каталог товаров:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == "🖥️ Компьютеры")
def send_pc_info(message):
    info = (
        "🖥️ **Компьютеры**\n\n"
        "Мы делаем сборки только на заказ все уточняйте у администратора"
        ". Витринный образец:\n"
        "• Процессор: Intel Core i5\n"
        "• Видеокарта: RTX 3060\n"
        "• **Цена:** 75 000 ₽"
    )
    bot.send_message(message.chat.id, info)


@bot.message_handler(func=lambda message: message.text == "📱 Техника Apple")
def send_apple_info(message):
    info = (
        "📱 **Техника Apple**\n\n"
        "• В продаже на данный момент только эти товары."
        "• iPhone 17 Pro Max - 189 990 ₽\n"
        "• iPhone 17 - 99 990 ₽"
    )
    bot.send_message(message.chat.id, info)


@bot.message_handler(func=lambda message: message.text == "📦 Другие товары")
def send_others_info(message):
    info = (
        "📦 **Другие товары**\n\n"
        "*Извините все товары появятся в ближайшее время , но вы пока можете сделать предзаказ у администратора @IDVPrivat.*"
    )
    bot.send_message(message.chat.id, info)



@bot.message_handler(func=lambda message: message.text == "⬅️ Назад")
def go_back(message):
    send_welcome(message)  # Возвращаем главное меню



@bot.message_handler(func=lambda message: message.text == "👤 Профиль")
def show_profile(message):
    user_id = str(message.from_user.id)

    if user_id == PREMIUM_USER_ID:
        profile_text = (
            "👤 **Твой Профиль**\n\n"
            "⚜️ **Подписка:** Premium (Активна)\n"
            "🎯 У тебя есть доступ к эксклюзивным скидкам!\n"
            f"🆔 **ID:** {user_id}"
        )
    else:
        profile_text = (
            "👤 **Твой Профиль**\n\n"
            "🔷 **Подписка:** Стандартная\n"
            "💎 *Премиум* дает доступ к скидкам.\n"
            f"🆔 **ID:** {user_id}"
        )

    bot.send_message(message.chat.id, profile_text)



@bot.message_handler(func=lambda message: message.text == "ℹ️ О нас")
def about_us(message):
    text = "🏭 **О нас**\n\nМы — команда инженеров, специализирующаяся на создании компьютеров и продаже товаров."
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda message: message.text == "💬 Отзывы")
def reviews(message):
    text = "💬 **Отзывы**\n\n*«Здесь пока нечего нет , надеюсь твой комментарий будет первым.»*"
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda message: message.text == "❓ Помощь")
def help_contact(message):
    text = (
        "❓ **Помощь**\n\n"
        "Если у вас возникли вопросы, обращайтесь к владельцу бота @IDVPrivat."
    )
    bot.send_message(message.chat.id, text)

if __name__ == '__main__':
    print("Бот запущен и работает!")
    bot.infinity_polling()
