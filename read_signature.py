import json
from os import listdir
from os.path import isfile, join


def atribute_types(sig_path):
    # sig_path = input("Caminho: ")
    files = [join(sig_path, f) for f in listdir(sig_path) if isfile(join(sig_path, f))]

    qualitativos = {}
    quantitativos = {}

    for file in files:
        with open(file, 'r') as signature_file:
            signature = json.load(signature_file)
            for step in signature['signature']:
                for atribute in signature['signature'][step]:
                    if signature['signature'][step][atribute]['operator'] == 'equal':
                        qualitativos.setdefault(atribute, []).append(signature['signature'][step][atribute]['value_max'])
                    if signature['signature'][step][atribute]['operator'] == 'interval':
                        quantitativos.setdefault(atribute, []).append(signature['signature'][step][atribute]['value'])

    return qualitativos, quantitativos