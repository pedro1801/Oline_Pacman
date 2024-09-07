def ajustar_tupla(tupla):
    return tuple(5 * round(val / 5) for val in tupla)

def processar_retas(retas):
    retas_ajustadas = []
    for reta in retas:
        tupla1, tupla2 = reta
        
        # Calcular a variação em cada eixo
        variacao_x1 = abs(tupla1[0] - tupla2[0])
        variacao_y1 = abs(tupla1[1] - tupla2[1])
        
        if variacao_x1 > variacao_y1:
            tupla1 = ajustar_tupla(tupla1)
            tupla2 = ajustar_tupla(tupla2)
            valor_final = ((tupla1[0],tupla1[1]),(tupla2[0],tupla1[1]))
        else:
            tupla1 = ajustar_tupla(tupla1)
            tupla2 = ajustar_tupla(tupla2)
            valor_final = ((tupla1[0],tupla1[1]),(tupla1[0],tupla2[1]))        
        retas_ajustadas.append(valor_final)

    return retas_ajustadas

# Exemplo de uso
retas = [((260, 293), (319, 293)), ((318, 293), (379, 295)), ((321, 294), (319, 231))]
retas_ajustadas = processar_retas(retas)
print(retas_ajustadas)
