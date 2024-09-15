import paho.mqtt.client as mqtt
import time
# Função callback quando o subscriber se conecta ao broker
listaplayers = []

def checkPos(vetor,listaplayers):    
    for ip in listaplayers:
        if vetor[-1] != ip:
            msg = f'{vetor[0]}:{vetor[1]}:{vetor[2]}'
            client.publish(ip,msg)

def on_connect(client, userdata, flags, rc):
    client.subscribe("ServerPac")

def saveTime(time):
    print()
# Função callback quando uma mensagem é recebida
def get_ip(ip):
    listaplayers.append(ip)
    
def on_message(client, userdata, msg):
    # Imprime a mensagem recebida e o ID do cliente que enviou
    mensage = msg.payload.decode().split(':')[-2]
    ip = msg.payload.decode().split(':')[-1]
    vetor = msg.payload.decode().split(':')

    if mensage == 'SaveIP':
        if ip not in listaplayers:
            get_ip(ip)
            print(listaplayers)
    elif  mensage == 'playersPos':
        checkPos(vetor,listaplayers)
    elif mensage == 'saveTime':
        print()
    else:
        pass

client = mqtt.Client()

client.on_connect = on_connect

client.on_message = on_message
# Conecta ao broker (localhost ou IP do servidor)
client.connect("localhost", 1883, 60)

# Mantém o loop para ficar recebendo as mensagens
client.loop_forever()
