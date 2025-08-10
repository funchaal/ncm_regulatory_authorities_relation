import json
import sys
from datetime import datetime

def proccess_json(attributes_json):
    result = {}
    ncms = attributes_json['listaNcm']

    for ncm_obj in ncms:
        ncm = str(ncm_obj['codigoNcm'])
        result[ncm] = []

        def proccess_row(main_attribute, cond_attr=False, sub_attr=False):
            attribute = None

            if cond_attr:
                attribute = main_attribute['atributo']
            else:
                attribute = main_attribute
            
            attr_code = attribute['codigo']

            result[ncm].extend(x for x in attribute['orgaos'])

            # Verifica se tem subatributos
            if len(attribute['listaSubatributos']) > 0:
                for sub_attr in attribute['listaSubatributos']:
                    proccess_row(sub_attr, sub_attr=True)
                
                return

            if attribute['atributoCondicionante']:
                for attribute_cond in attribute['condicionados']:
                    proccess_row(attribute_cond, cond_attr=True, sub_attr=sub_attr)
            

        for attr in ncm_obj['listaAtributos']:
            attr_dtls = next((d for d in attributes_json['detalhesAtributos'] if d['codigo'] == attr['codigo']), None)

            proccess_row(attr_dtls)

        result[ncm] = list(set(result[ncm]))
    return result

if __name__ == "__main__":
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")  # ex: 20250809_235900

    JSON_FILE_NAME_PATH = "attributes_relation_prod.json"

    try:
        with open(JSON_FILE_NAME_PATH, "r", encoding="utf-8") as f:
            attributes_json = json.load(f)
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{JSON_FILE_NAME_PATH}' não contém um JSON válido.")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{JSON_FILE_NAME_PATH}' não foi encontrado.")
        sys.exit(1)

    proccessed = proccess_json(attributes_json)

    output_filename = f"ncm_regulatory_authorities_relation_{timestamp}.json"
    
    with open(output_filename, "w", encoding="utf-8") as out_f:
        json.dump(proccessed, out_f, ensure_ascii=False, indent=2)

    print(f"Processed data saved to {output_filename}")