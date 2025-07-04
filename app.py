from flask import Flask, request
import requests
import openai

app = Flask(__name__)

VERIFY_TOKEN = 'mi_token_de_verificacion'
ACCESS_TOKEN = 'IGAAO5z0RsQkxBZAE9nbVlRaFNCTzhURkpydzZA4NXZAEcGwxZA1hXcHRCOVlJUjhHWjFkeGdtRmltSFBLbmR5ZAURNbm5SVHZALMkdtSjQwSl9URjhpRkhLQzhBVVhGMzJ3cGF6UzFjLW9IQ3Q3Y3ZARMG9KN210bjJsQlZAHU3lUWll2TQZDZD'
OPENAI_KEY = 'tu_clave_openai'

openai.api_key = OPENAI_KEY

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge'), 200
    return 'Error de verificación', 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    for entry in data.get('entry', []):
        for message in entry.get('messaging', []):
            sender_id = message['sender']['id']
            text = message['message'].get('text')

            if text:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": text}]
                )

                reply = response['choices'][0]['message']['content']
                send_message(sender_id, reply)
    return "ok", 200

def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={ACCESS_TOKEN}"
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    requests.post(url, json=data)

if __name__ == '__main__':
    app.run(port=5000)
