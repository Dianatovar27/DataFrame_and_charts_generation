import random
import pandas as pd
import matplotlib.pyplot as plt
from seaborn import color_palette

hosts= []
dataset= []
df= None 

def set_hostnames(number_of_hosts: int) -> None:
    sistema_prefix = ['L']*4 + ['S']*3 + ['A']*2 + ['H']*1
    entorno_prefix = ['D']*10 + ['I']*10 + ['T']*25 + ['S']*25 + ['P']*30
    pais_prefix= ['NOR']*6 + ['FRA']*9 + ['ITA']*16 + ['ESP']*16 + ['DEU']*23 + ['IRL']*30
    grupo_alpha=[]

    for i in range (number_of_hosts):
        pais= random.choice(pais_prefix)
        host= random.choice(sistema_prefix) + random.choice(entorno_prefix) 
        host+= pais
        grupo_alpha.append(host)
        host += str(grupo_alpha.count(host)).zfill(3)
        hosts.append(host)

def get_os(hostname:str)-> str:
    if hostname.startswith ('L'):
        return 'Linux'
    elif hostname.startswith('S'):
        return 'Solaris'
    elif hostname.startswith('A'):
        return 'AIX'
    elif hostname.startswith('H'):
        return 'HP-UX'
    else:
        return 'Unknow'
    
def get_enviroment(hostname:str)-> str:
    if hostname [1] == ('D'):
        return 'Development'
    elif hostname [1] == ('I'):
        return 'Integration'
    elif hostname [1] == ('T'):
        return 'Testing'
    elif hostname [1] == ('S'):
        return 'Staging'
    elif hostname [1] == ('P'):
        return 'Production'
    else:
        return 'Unknow'

def get_country(hostname:str)-> str:
    if hostname [2:5] == ('NOR'):
        return 'Norway'
    elif hostname [2:5] == ('FRA'):
        return 'France'
    elif hostname [2:5] == ('ITA'):
        return 'Italy'
    elif hostname [2:5] == ('ESP'):
        return 'Spain'
    elif hostname [2:5] == ('IRL'):
        return 'Irland'
    elif hostname [2:5] == ('DEU'):
        return 'Germany'
    else:
        return 'Unknow'
    
def set_dataframe(count:int):
    global df 
    
    set_hostnames(count)

    for hostname in hosts:
        dataset.append({
            'hostname': hostname,
            'os': get_os(hostname),
            'enviroment': get_enviroment(hostname),
            'country': get_country(hostname),
            'node': int(hostname[-3:])
        })
    df=pd.DataFrame(dataset)

set_dataframe(1500)

df.to_csv('hosts.csv', header=True, index=False)

hosts_df = pd.read_csv(r'hosts.csv', encoding='ISO-8859-1')

print(hosts_df.head())

#Chart Generation

country_enviroment = hosts_df
country_enviroment = country_enviroment.groupby(['country', country_enviroment['enviroment']]).size()
print(country_enviroment.head())

country_enviroment.unstack()
print(country_enviroment.head())

country_enviroment.unstack().plot(kind='bar')
plt.show()