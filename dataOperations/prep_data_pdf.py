import json
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import collections
import math, re

def read_file(file_name):
    with open(file_name) as f:
        data = json.load(f)
        return data


def data_price_vs_screen(data):
    screen_prices = {}

    for row in data:
        if row['screen'] != '':
            key = math.floor(float(row['screen'].replace(',', '.')))
            key_str = str(key)
            if key < 18 and key > 10:     
                if 'prices' in row:
                    if key_str not in screen_prices.keys():
                        screen_prices[key_str] = [ np.mean(list(row['prices'].values())) ]
                    else:
                        screen_prices[key_str] += [ np.mean(list(row['prices'].values())) ]
                        
                elif 'price' in row:
                    if key_str not in screen_prices.keys():
                        screen_prices[key_str] = [row['price']]
                    else:
                        screen_prices[key_str].append(row['price'])

    for key, value in screen_prices.items():
        screen_prices[key] = [ np.mean(value),  np.min(value), np.max(value)]

    return collections.OrderedDict(sorted(screen_prices.items()))
           

def chart_drawer(dict_, title):
    x_values = list(dict_.keys())
    prices = [el[0] for el in list(dict_.values()) ]
    min_p = [el[1] for el in list(dict_.values()) ]
    max_p = [el[2] for el in list(dict_.values()) ]
    X = np.arange(len(prices))
    
    plt.bar(X, min_p, color = 'g', width = 0.25)
    plt.bar(X + 0.25, prices, color = 'black', width = 0.25)
    plt.bar(X + 0.5, max_p, color = 'red', width = 0.25)
    plt.legend(['Min Price', 'Average Price', 'Max Price'])
    plt.xticks([i + 0.25 for i in range(len(x_values))], x_values, rotation='vertical')
    plt.title(f'Average price per {title} size')
    plt.ylabel('Price')
    # plt.savefig('Memory_plot.png')
    plt.show()


def data_price_vs_cpu(data):
    cpu_prices = {}

    for row in data:
        row['cpu'] = row['cpu'].lower()
        
        if '-' in row['cpu']: 
            row['cpu'] = row['cpu'].split('-')[0]    

        if row['cpu'] != '':
            if row['cpu'] == '17,3\"':
                continue
            if 'prices' in row:
                if row['cpu'] not in cpu_prices.keys():
                    cpu_prices[row['cpu']] = [ np.mean(list(row['prices'].values())) ]
                else:
                    cpu_prices[row['cpu']] += [ np.mean(list(row['prices'].values())) ]
            elif 'price' in row:
                if row['cpu'] not in cpu_prices.keys():
                    cpu_prices[row['cpu']] = [ row['price'] ]
                else:
                    cpu_prices[row['cpu']] += [ row['price'] ]


    for key, value in cpu_prices.items():
        cpu_prices[key] = [ np.mean(value),  np.min(value), np.max(value)]

    return cpu_prices


def data_price_vs_memory(data):
    memory_prices = {}

    for row in data:
        row['memory'] = row['memory'].upper()

        if row['memory'] != '':
            if 'prices' in row:
                if row['memory'] not in memory_prices.keys():
                    memory_prices[row['memory']] = [ np.mean(list(row['prices'].values())) ]
                else:
                    memory_prices[row['memory']] += [ np.mean(list(row['prices'].values())) ]
            elif 'price' in row:
                if row['memory'] not in memory_prices.keys():
                    memory_prices[row['memory']] = [ row['price'] ]
                else:
                    memory_prices[row['memory']] += [ row['price'] ] 

    for key, value in memory_prices.items():
        memory_prices[key] = [ np.mean(value),  np.min(value), np.max(value)]   

    return memory_prices        


def data_price_vs_storage(data):
    storage_prices = {}

    for row in data:
        if row['storage'] != '':
            row['storage'] = row['storage'].upper()
            regex = r'^(([0-9]+)(GB|G)?)$' 
            res = re.match(regex, row['storage'])
            
            if row['storage'][0] == '/':
                row['storage'] = row['storage'][1:]   

            if res:
                if res[3] == 'GB':
                    row['storage'] = res[2] + res[3]
                elif res[3] == 'G':
                    row['storage'] = res[2] + res[3] + 'B'
                else:
                    row['storage'] = res[2] + 'GB'

            
            if row['storage'] == '1000GB':
                row['storage'] = '1TB'        
                
            
            if 'prices' in row:
                if row['storage'] not in storage_prices.keys():
                    storage_prices[row['storage']] = [ np.mean(list(row['prices'].values())) ]
                else:
                    storage_prices[row['storage']] += [ np.mean(list(row['prices'].values())) ]
            elif 'price' in row:
                storage_prices[row['storage']] = storage_prices.get(row['storage'], []) + [ row['price'] ]

    for key, value in storage_prices.items():
        storage_prices[key] = [ np.mean(value),  np.min(value), np.max(value)]   

    return storage_prices                

   

    


prices = read_file('prices1.json')
# screen_prices = data_price_vs_screen(prices)
# chart_screen_prices = chart_drawer(screen_prices, 'screen')

# cpu_prices = data_price_vs_cpu(prices)
# chart_cpu_prices = chart_drawer(cpu_prices, 'cpu')

# memory_prices = data_price_vs_memory(prices)
# chart_memory_prices = chart_drawer(memory_prices, 'memory')

# storage_prices = data_price_vs_storage(prices)
# chart_storage_prices = chart_drawer(storage_prices, 'storage')