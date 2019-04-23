import requests

# Controls whether all combinations or just the best for each game will be shown
show_best_only = True

with open('api-key.txt') as f:
    api_key = f.read().strip()

URL_BASE = 'https://api.the-odds-api.com/v3/'

# sports_response = requests.get(URL_BASE + 'sports', params={'api_key': api_key})
# sports_json = json.loads(sports_response.text)

epl_response = requests.get(URL_BASE + 'odds', params={
    'api_key': api_key,
    'sport': 'soccer_epl',
    'region': 'uk',
    'mkt': 'h2h'
})

odds_json = epl_response.json()
data = odds_json['data']

for game in data:
    winning_combos = []

    for h in game['sites']:
        for d in game['sites']:
            for a in game['sites']:
                hv = h['odds']['h2h'][0]
                dv = d['odds']['h2h'][2]
                av = a['odds']['h2h'][1]

                odds_value = (1/hv) + (1/dv) + (1/av)
                if odds_value < 1:
                    winning_combos.append((odds_value, h, d, a))

    if len(winning_combos):
        print("\n")
        print(f'Found winning combos for game {game["teams"][0]} vs {game["teams"][1]}:')

        winning_combos.sort(key=lambda x: x[0])

        for w in winning_combos:
            print()
            print(f'Value: {w[0]}')
            print(f'Profit: {1/w[0] - 1:.3%}')
            print(f'Home: {w[1]["site_nice"]} ({w[1]["odds"]["h2h"][0]})')
            print(f'Draw: {w[2]["site_nice"]} ({w[2]["odds"]["h2h"][2]})')
            print(f'Away: {w[3]["site_nice"]} ({w[3]["odds"]["h2h"][1]})')

            if show_best_only:
                break
