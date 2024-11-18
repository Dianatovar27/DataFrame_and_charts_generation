import random
import pandas as pd
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


OS_grouped_by_country = hosts_df.groupby(['country', 'os']).size()
OS_grouped_by_country = OS_grouped_by_country.unstack()

country_counts = hosts_df['country'].value_counts()

hosts_by_country_and_environment = hosts_df.groupby(['country', 'environment']).size()

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# Barh of Type of OS grouped by country

palette_barh= color_palette(palette= 'Dark2')
OS_grouped_by_country.plot(kind='barh', stacked=False, ax=axs[0, 0], color=palette_barh )
axs[0, 0].set_title('Type of OS grouped by country')
axs[0, 0].set_ylabel('Country')

# Pie chart of Total Operating Systems

pie_values = hosts_df.groupby(['os']).size()
pie_labels = [f"{value}" for label, value in zip(pie_values.index, pie_values)]
pie_index = pie_values.index 

wedges, texts = axs[0, 1].pie(pie_values, labels=pie_labels, autopct=None)

total = pie_values.sum()

porcentajes = [] 
for label, value in zip(pie_index, pie_values):
    porcentaje = f"{label}: {value / total * 100:.1f}%"  
    porcentajes.append(porcentaje)  

axs[0, 1].legend(wedges, porcentajes, loc="best", bbox_to_anchor=(1, 0.5))
axs[0, 1].set_title('Total Operating Systems')

# Barh for Total hosts by country
palette = color_palette("ch:s=.25,rot=-.25", n_colors=len(country_counts))

country_counts.plot(kind='barh', stacked=False, ax=axs[1, 0], color=palette)
axs[1, 0].set_title('Total hosts by country')
axs[1, 0].set_xlabel('Number of hosts')
axs[1, 0].set_ylabel('Country')

for i, value in enumerate(country_counts):
    axs[1, 0].annotate(str(value), xy=(value, i), xytext=(5, -3), textcoords='offset points')

max_value = country_counts.max() 
axs[1, 0].set_xlim(0, max_value + 100) 

# bar for Hosts by country grouped by environment
hosts_by_country_and_environment.unstack(0).plot(kind='bar', stacked=False, ax=axs[1, 1])
axs[1, 1].set_title('Hosts by country grouped by environment')
axs[1, 1].set_ylabel('Number of hosts')
axs[1, 1].set_xlabel('environment')

fig.tight_layout()

plt.show()
