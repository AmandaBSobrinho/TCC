import json

def atribute_types():
    sig_path = input("Caminho: ")

    with open(sig_path, 'r') as signature_file:
        signature = json.load(signature_file)

    qualitativos = {}
    quantitativos = {}

    for step in signature['signature']:
        for atribute in signature['signature'][step]:
            if signature['signature'][step][atribute]['operator'] == 'equal':
                qualitativos[atribute] = signature['signature'][step][atribute]['value_max']
            if signature['signature'][step][atribute]['operator'] == 'interval':
                quantitativos[atribute] = signature['signature'][step][atribute]['value']

    return qualitativos, quantitativos