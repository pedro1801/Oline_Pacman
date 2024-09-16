import paho.mqtt.client as mqtt

listaplayers = []
listaTemp = []
multplayers = False
acabo = True

def checkPos(vetor, listaplayers):    
    for ip in listaplayers:
        if vetor[-1] != ip:
            msg = f'{vetor[0]}:{vetor[1]}:{vetor[2]}:checkPos'
            client.publish(ip, msg)

def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker com código {rc}")
    client.subscribe("ServerPac")

def startGame(listaip):
    for ip in listaip:
        client.publish(ip, "StartGame")

def saveTime(vetor):
    global listaTemp
    listaTemp.append((int(vetor[0]), vetor[1]))

def endgame(listaTemp, listaip):
    for ip in listaip:
        for tempo, player_ip in listaTemp:
            msg = f'{tempo}:{player_ip}:endGame'
            client.publish(ip, msg)

# def reset_game():
#     global listaplayers, listaTemp, multplayers, acabo
#     listaplayers = []
#     listaTemp = []
#     multplayers = False
#     acabo = True
#     print("Jogo resetado")

def on_message(client, userdata, msg):
    global multplayers, acabo
    payload = msg.payload.decode()
    parts = payload.split(':')
    
    if len(parts) < 2:
        #print(f"Mensagem inválida recebida: {payload}")
        return

    mensage = parts[-2]
    ip = parts[-1]
    
    # print(f"Mensagem recebida: {mensage} de {ip}")
    
    if mensage == 'SaveIP':
        if ip not in listaplayers:
            listaplayers.append(ip)
            #print(f"Lista de jogadores: {listaplayers}")
    elif mensage == 'playersPos':
        checkPos(parts, listaplayers)
    elif mensage == 'saveTime':
        saveTime(parts)
    # elif payload == 'ResetGame':
    #     reset_game()
    else:
        pass

    if len(listaplayers) >= 2 and not multplayers:
        print('startGame')
        startGame(listaplayers)
        multplayers = True
        
    if len(listaplayers) == len(listaTemp) and acabo:
        #print(f"Tempos dos jogadores: {listaTemp}")
        endgame(listaTemp, listaplayers)
        acabo = False

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()