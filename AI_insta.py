import requests
import openai

ACCESS_TOKEN = "ВАШ_ТОКЕН_ДОСТУПА"
IG_USER_ID = "ВАШ_IG_USER_ID"


def get_messages():
    url = f"https://graph.facebook.com/v15.0/{IG_USER_ID}/conversations?access_token={ACCESS_TOKEN}"
    response = requests.get(url)
    data = response.json()
    return data


messages = get_messages()

openai.api_key = "ВАШ_OPENAI_API_КЛЮЧ"

conversation = [{"role": "system", "content": "Ты помощник, который помогает пользователям."}]

def generate_response(user_message, conversation):
    conversation.append({"role": "user", "content": user_message})
    # Оставляем только последние 10 сообщений
    if len(conversation) > 10:
        conversation.pop(1)  # Удаляем самое старое сообщение, кроме системного
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )
        bot_message = response.choices[0].message['content']
        conversation.append({"role": "assistant", "content": bot_message})
        return bot_message
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return "Извините, сейчас я не могу ответить на ваш запрос."


def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v15.0/me/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    data = {
        "messaging_type": "RESPONSE",
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Сообщение отправлено успешно!")
    else:
        print(f"Ошибка при отправке сообщения: {response.status_code}")
        print(response.json())

    return response.json()


recipient_id = "ID_ПОЛЬЗОВАТЕЛЯ"
bot_response = "Ваш текст сообщения"
send_message(recipient_id, bot_response)
