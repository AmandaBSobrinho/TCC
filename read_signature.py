import json

def atribute_types():
    sig_path = input("Caminho: ")

    with open(sig_path, 'r') as signature_file:
        signature = json.load(signature_file)

    qualitativos = []
    quantitativos = []

    for step in signature['signature']:
        for atribute in signature['signature'][step]:
            if signature['signature'][step][atribute]['operator'] == 'equal':
                qualitativos.append(atribute)
            if signature['signature'][step][atribute]['operator'] == 'interval':
                quantitativos.append(atribute)

    return qualitativos, quantitativos