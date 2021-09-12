from flask import Flask, request
import requests
import controller

app = Flask(__name__)
app.secret_key = '1234'


@app.route("/sanity", methods=['GET'])
def index():
    """
    server home page 
    :return: str to show that the server is running
    """
    return 'Server is running'


# TOKEN = '1689855772:AAEBslKOF7UmGZCKSWx1JaF45tcHyoQgu_g'
#TOKEN = '1949765999:AAHTBPmq4YWdDOA0OO643q_15gb9-JWvi5c'
TOKEN= '1863158093:AAGeVkKauNy1HaNJz5qXUtSlQHmTXutMBgw'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://29b4c24261bf.ngrok.io/message'.format(
    TOKEN)
requests.get(TELEGRAM_INIT_WEBHOOK_URL)


@app.route('/message', methods=["POST"])
def handle_message():
    """
    get message from the telegram bot and send the wright answer
    """
    print("got message")
    answer = 'I do not understand :('
    command = list(request.get_json()['message']['text'].split(" "))
    ''' if command[0] == '/start':
        answer = controller.start()

    if command[0] == '/menu':
        answer = controller.menu()

    if command[0] == '/popular_coin':
        answer = controller.popular()

    if command[0] == '/coins' and len(command) == 4:
        answer = controller.converter(command[1].upper(), command[2].upper(), command[3])

    if command[0] == '/weight' and len(command) == 4:
        answer = controller.convert_weight(command[1], command[2], command[3])

    if command[0] == '/temp' and len(command) == 4:
        answer = controller.convert_temp(command[1], command[2], command[3])'''

    if command[0] == '/options':
        if controller.app_controller.COUNTER == 1 or controller.app_controller.COUNTER == 2:
            if controller.app_controller.con[0] == '/weight':
                answer = "Use kg (for kilogram) or lbs (for pound)"
            elif controller.app_controller.con[0] == '/temp':
                answer = "Use C (Celsius), F (Fahrenheit) or K (kelvin) "
            elif controller.app_controller.con[0] == '/coins':
                answer = "check by yourself!"

    elif controller.app_controller.COUNTER == 3:
        controller.app_controller.con.append(command[0])
        controller.app_controller.COUNTER = 0
        answer = controller.gen_function(controller.app_controller.con[0], controller.app_controller.con[1],
                                         controller.app_controller.con[2], controller.app_controller.con[3])

    elif controller.app_controller.COUNTER == 2:
        controller.app_controller.con.append(command[0])
        controller.app_controller.COUNTER = 3
        answer = 'Amount:'

    elif controller.app_controller.COUNTER == 1:
        controller.app_controller.con.append(command[0])
        controller.app_controller.COUNTER = 2
        answer = 'To:'

    elif command[0] == '/coins' or command[0] == '/weight' or command[0] == '/temp':  # '/convert':
        controller.app_controller.con = [command[0]]
        controller.app_controller.COUNTER = 1
        answer = 'From:'

    elif command[0] == '/start':
        answer = controller.start()

    elif command[0] == '/menu':
        answer = controller.menu()

    elif command[0] == '/popular_coin':
        answer = controller.popular()

    chat_id = request.get_json()['message']['chat']['id']
    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                       .format(TOKEN, chat_id, answer))
    return "success"


if __name__ == '__main__':
    app.run(port=5001)
