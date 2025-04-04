import requests
import pprint as pp
import csv

def get_pokemon_info(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url,timeout=3)
    
    if response.status_code == 200:
        pokemon_data = response.json()
        pokemon_info = {
            "name": pokemon_data["name"],
            "height": pokemon_data["height"],
            "weight": pokemon_data["weight"],
            "abilities": [ability["ability"]["name"] for ability in pokemon_data["abilities"]],
            "types": [type_data["type"]["name"] for type_data in pokemon_data["types"]]
        }
        return pokemon_info
    else:
        return None

def get_pokemon_info_row(pokemon_name):
    print(pokemon_name)
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    try:
        response = requests.get(url,timeout=3)
    except requests.exceptions.Timeout:
        print("Timed out")
    if response.status_code == 200:
        pokemon_data = response.json()
        pokemon_info = [pokemon_data["name"],pokemon_data["height"],pokemon_data["weight"]]
        return pokemon_info
    else:
        return []

def get_pokemon_names():
    url = "https://pokeapi.co/api/v2/pokemon/"
    params = {'limit': 50}
    pokemon_names=[]
    for offset in range(0, 1000, 100):
        params['offset'] = offset 
        response = requests.get(url, params=params)

        if response.status_code != 200: 
            print(response.text)
        else:
            data = response.json()
            for item in data['results']:
                print(item['name'])
                pokemon_names.append(item['name'])
    return pokemon_names

def write_data_to_seed(pokemon_names):
    with open('../seeds/pokemon_data.csv', 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(["Name","Height","Weight"])
        for pokemon_name in pokemon_names:
            row=get_pokemon_info_row(pokemon_name)
            if len(row)>0:
                wr.writerow(row)

if __name__ == "__main__":
    pokemon_names = get_pokemon_names()
    write_data_to_seed(pokemon_names)
