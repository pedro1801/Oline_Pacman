import math

def distancia(p1, p2):
    """Calcula a distância euclidiana entre dois pontos."""
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def circulo_sobreposto(circulos, novo_circulo, raio):
    """Verifica se o novo círculo se sobrepõe a algum dos círculos existentes."""
    (cx, cy), _, _ = novo_circulo
    for circulo in circulos:
        (ex, ey), _, _ = circulo
        if distancia((cx, cy), (ex, ey)) < 2 * raio:
            return True
    return False

def circulos_ao_longo_das_retas(retas, espaco):
    """Gera círculos ao longo das retas com um espaçamento, evitando sobreposições."""
    circulos = []
    raio = 5
    for reta in retas:
        (x1, y1), (x2, y2) = reta
        comprimento = distancia((x1, y1), (x2, y2))
        n_circulos = int(comprimento // espaco)

        for i in range(n_circulos + 1):
            t = i / n_circulos if n_circulos > 0 else 0
            # Interpolação linear entre os dois pontos
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            novo_circulo = ((int(x), int(y)), raio, 0)
            
            if not circulo_sobreposto(circulos, novo_circulo, raio):
                circulos.append(novo_circulo)
    return circulos

reta_pares = [
                ((30, 25), (30, 175)), ((30, 175), (145, 175)), 
                ((30, 25), (290, 25)),  ((30, 105), (605, 105)),
                ((145, 175), (145, 545)), ((290, 25), (290, 105)), 
                ((605, 105), (605, 25)), ((145, 175), (145, 25)), 
                ((605, 25), (350, 25)), ((350, 25), (350, 105)), 
                ((490, 25), (490, 545)),  ((605, 105), (605, 175)),
                ((605, 175), (490, 175)), ((490, 545), (595, 545)), 
                ((145, 545), (40, 545)), ((40, 545), (40, 615)), 
                ((595, 545), (595, 615)), ((40, 615), (595, 615)),
                ((210, 105), (210, 180)), ((430, 105), (430, 180)),
                ((210, 180), (290, 180)), ((430, 180), (350, 180)),
                ((290, 180), (290, 230)), ((350, 180), (350, 230)),
                ((290, 230), (350, 230)), 
                ((280, 615), (280, 550)), ((360, 615), (360, 550)),
                ((360, 550), (430, 550)), ((280, 550), (210, 550)),
                ((490, 485), (145, 485)), ((430, 550), (430, 485)), 
                ((210, 550), (210, 485)), ((145, 420), (295, 420)), 
                ((490, 420), (345, 420)), ((295, 420), (295, 485)), 
                ((345, 420), (345, 485)),((290, 230), (210, 230)), 
                ((350, 230), (430, 230)), ((210, 230), (210, 420)), 
                ((430, 230), (430, 420)), ((210, 360), (430, 360)), 
                ((210, 295), (145, 295)), ((430, 295), (490, 295)),
                ((145, 420), (30, 420)), ((490, 420), (605, 420)),
                ((90, 545), (90, 480)), ((550, 545), (550, 485)),
                ((90, 480), (30, 480)), ((550, 485), (605, 485)),
                ((30, 420), (30, 480)), ((605, 420), (605, 485))
             ]

# Gerando os círculos com espaçamento de 15 pixels
circulos = circulos_ao_longo_das_retas(reta_pares, 25)
for i in range(0, len(circulos), 3):
    item = circulos[i:i+3]
    if len(item) > 2:
        print(item[0], ',', item[1], ',', item[2], ',')
    elif len(item) > 1:
        print(item[0], ',', item[1], ',')
    else:
        print(item[0], ',')
