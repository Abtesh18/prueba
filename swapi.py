import requests

# Base URL de la API de SWAPI
BASE_URL = "https://swapi.dev/api/"

# Función para obtener todos los resultados paginados de un endpoint
def get_all_results(endpoint):
    results = []
    url = f"{BASE_URL}{endpoint}"
    while url:
        response = requests.get(url).json()
        results.extend(response['results'])
        url = response['next']
    return results

# a) ¿En cuántas películas aparecen planetas cuyo clima sea árido?
def count_arid_planet_films():
    planets = get_all_results('planets/')
    arid_planet_films = set()
    
    for planet in planets:
        if 'arid' in planet['climate']:
            for film_url in planet['films']:
                arid_planet_films.add(film_url)
    
    return len(arid_planet_films)

# b) ¿Cuántos Wookies aparecen en toda la saga?
def count_wookies():
    species = get_all_results('species/')
    wookie_species = next((s for s in species if 'Wookiee' in s['name']), None)
    
    if wookie_species:
        wookies = wookie_species['people']
        return len(wookies)
    return 0

# c) ¿Cuál es el nombre de la aeronave más pequeña en la primera película?
def smallest_starship_in_first_film():
    first_film = requests.get(f"{BASE_URL}films/1/").json()
    starships = []
    
    for starship_url in first_film['starships']:
        starship = requests.get(starship_url).json()
        starships.append({
            'name': starship['name'],
            'length': float(starship['length'].replace(',', ''))
        })
    
    smallest_starship = min(starships, key=lambda x: x['length'])
    return smallest_starship['name']

# Llamadas a las funciones
arid_planet_films_count = count_arid_planet_films()
wookie_count = count_wookies()
smallest_starship_name = smallest_starship_in_first_film()

# Resultados
print(f"a) En {arid_planet_films_count} películas aparecen planetas cuyo clima es árido.")
print(f"b) Hay {wookie_count} Wookies en toda la saga.")
print(f"c) La aeronave más pequeña en la primera película es: {smallest_starship_name}.")
