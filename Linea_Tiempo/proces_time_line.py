import json
from datetime import datetime

json_file_path = 'Linea_del_tiempo_ME.json'

category_mapping = {
    "951433": "Escala Internacional",
    "951431": "Escala Nacional",
    "951432": "Escala Regional",
}

tag_mapping = {
    "94105": "Colombia",
    "94104": "Comunismo Internacional",
    "94101": "Guerra Fría",
    "94103": "Inteligencia Militar",
    "94106": "Latinoamérica",
}

with open(json_file_path, 'r') as json_file:
    data_list = json.load(json_file)

transformed_data = []

for storie in data_list['stories']:
    media_info = storie['media'][0]
    start_date = datetime.strptime(storie['startDate'], '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(storie['startDate'], '%Y-%m-%d %H:%M:%S')
    tag_ids = storie.get('tags', '').split(',')
    formatted_tags = [f"<strong>{tag_mapping.get(tag_id, '')}</strong>" for tag_id in tag_ids]
    background = media_info['externalMediaThumb'] if media_info['externalMediaThumb']  != '' else media_info['src']
    if len(storie['media']) > 1:
        media_info2 = storie['media'][1]
        background = media_info2['externalMediaThumb'] if media_info2['externalMediaThumb']  != '' else media_info2['src']

    if background == '':
        background = storie['externalLink']


    new_event = {
        "media": {
            "url": media_info['src'],
            "caption": media_info['caption'],
            "credit": media_info.get('externalLink', ''),
            "thumbnail": background,
        },
        "start_date": {
            "month": str(start_date.month),
            "day": str(start_date.day),
            "year": str(start_date.year),
        },
        "end_date": {
            "month": str(end_date.month),
            "day": str(end_date.day),
            "year": str(end_date.year),
        },
        "text": {
            "headline": storie['title'],
            "text": ", ".join(formatted_tags) + f"<p>{storie['text']}</p>" + (f"<a href='{storie['externalLink']}' target='_blank' style='color: #f5bd56;'>Para saber más</a>" if storie['externalLink'] else ""),
        },
        "group" : category_mapping.get(storie['category'], ''),
        "background":{"url" : background, "color": "#2d2d2d"},
    }

    transformed_data.append(new_event)


output_data = {
    "title": {
        "media": {
            "url": "https://lh3.googleusercontent.com/pw/ADCreHeHEqa9RX6UgnwzzbGc8mLovnt9pnus1GlgPEq24UyrblXqdX9qSWutsjxrd4zoNEPrLtFo1ex83Za19V7F0B15GBAsmKrCrTxZht6t_cKIvV4yG_DMfab_ua4GroDeohASlHwjNkdo-VZdtU3EN56jeQ=w443-h627-s-no-gm",
            "caption": "EL MUNDO DEL ENEMIGO",
        },
        "text": {
            "headline": "EL MUNDO DEL ENEMIGO",
            "text": "<p>Las dinámicas del conflicto armado colombiano traspasaron las fronteras nacionales. Y es a través de este fenómeno que actores como las guerrillas, los gobiernos, los partidos políticos y los movimientos sociales, tuvieron relaciones importantes con actores externos que permitieron que la imagen del enemigo interno pasara a tener un alcance regional e internacional. En esta línea del tiempo se pueden visualizar los hitos más significativos para el mundo enemigo.</p>"
        },
        "background":{"color": "#2d2d2d"},
    },
    "events": transformed_data,
}

with open('transformed.json', 'w') as output_file:
    json.dump(output_data, output_file, indent=2)