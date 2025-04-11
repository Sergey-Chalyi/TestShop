import telebot
from base.settings import TELEGRAM_BOT_TOKEN

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def send_order_notification(order_data):
    message = f"""
        🛍️ Новый заказ #{order_data['order_id']}!

        📦 Товар: {order_data['product_name']}
        📊 Количество: {order_data['quantity']}
        👤 Покупатель: {order_data['customer_name']}
        📱 Телефон: {order_data['phone']}
        📍 Адрес: {order_data['address']}
        💬 Комментарий: {order_data['comment']}
    """
    try:
        updates = bot.get_updates()
        if updates:
            chat_id = updates[-1].message.chat.id
            bot.send_message(chat_id, message)
    except Exception as e:
        print(f"Error sending message: {e}")