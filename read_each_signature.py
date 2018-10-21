import json


def read_atributes(file):

    qualitativos = {}
    quantitativos = {}
    number_atrib = 0

    with open(file, 'r') as signature_file:
        signature = json.load(signature_file)
        for step in signature['signature']:
            number_atrib += len(signature['signature'][step])
            for atribute in signature['signature'][step]:
                if signature['signature'][step][atribute]['operator'] == 'equal':
                    qualitativos.setdefault(atribute, signature['signature'][step][atribute]['value_max'])
                if signature['signature'][step][atribute]['operator'] == 'interval':
                    quantitativos.setdefault(atribute, signature['signature'][step][atribute]['value'])

    return qualitativos, quantitativos, number_atrib