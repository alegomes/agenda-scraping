import requests
import json
import csv

PRODUCTIONS_KEY = 'nodes'

def get_production_details(id, path):
    url = f"https://carre.nl/api/render{path}"
    
    headers = {}
    response = requests.get(url, headers=headers)

    data = json.loads(response.text)

    if 'productions' in data:
        events = data['productions'][id]['events']

        if len(events) == 0:
            raise Exception(f'No event found for production {id}')

        if len(events) > 1:
            raise Exception(f'Weird. More than one event found for production {id}')

        return {
            'date' : events[0]['start_date']
        }
    else:
        raise Exception(f'Production {id} not available anymore')


def save_productions(productions):
    file = open('productions.csv', 'a', newline='')
    writer = csv.writer(file)

    writer.writerow(["ID", "Show Name", "Date", "Theater Name", "Link to Show"])

    for p in productions:
        writer.writerow([
            p['id'],
            p['showName'],
            p['date'],
            p['theaterName'],
            p['linkToShow']
        ])

    file.close()

def summarize_productions(productions):

    summary = []

    for k in productions:
        kind = productions[k]['kind']
        if kind == 'production-page':
            id = productions[k]['production_id']
            show_name = productions[k]['data']['title']
            theater_name = productions[k]['data']['siteTitle']
            path  = productions[k]['data']['url']
            
            print(f'Enriching production {id} at {path}...')

            try:
                details = get_production_details(id, path)
                show_date = details['date']

                summary.append({
                    'id': id,
                    'showName' : show_name,
                    'date' : show_date,
                    'theaterName' : theater_name,
                    'linkToShow' : f'https://carre.nl{path}',
                })

            except Exception as e:
                print(e)
                # Ignore
    
    return summary

def get_production_list():
    url = "https://carre.nl/api/render/production-page-list-nl"

    headers = {}

    response = requests.get(url, headers=headers)

    data = json.loads(response.text)

    productions = data[PRODUCTIONS_KEY]

    return productions
            

if __name__ == '__main__':
    productions = get_production_list()
    productions = summarize_productions(productions)
    save_productions(productions)

