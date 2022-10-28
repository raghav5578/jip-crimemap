def install():
    import pip
    pip.main(['install', 'IPython'])
    pip.main(['install', 'pandas'])
    pip.main(['install', 'bokeh'])
    pip.main(['install', 'matplotlib'])
    pip.main(['install', 'colorcet'])
    pip.main(['install', 'cbsodata'])
    pip.main(['install', 'holoviews'])


# install()
import bokeh
from bokeh.layouts import column, row
from bokeh.models import Select
from bokeh.palettes import Spectral5
from bokeh.plotting import curdoc
from bokeh.sampledata.autompg import autompg_clean as df
from dictionaries import subset_itemlist, colourlist
import holoviews as hv
import pandas as pd

import matplotlib.pyplot as plt

from bokeh.models import (
    GeoJSONDataSource,
    HoverTool,
    EqHistColorMapper
)
import os

import json
from collections import OrderedDict

import cbsodata
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

plt.style.use('fivethirtyeight')
hv.extension('matplotlib')

df = df.copy()

SIZES = list(range(6, 22, 3))
COLORS = Spectral5
N_SIZES = len(SIZES)
N_COLORS = len(COLORS)

# data cleanup
df.cyl = df.cyl.astype(str)
df.yr = df.yr.astype(str)
del df['name']

columns = sorted(df.columns)
discrete = [x for x in columns if df[x].dtype == object]
continuous = [x for x in columns if x not in discrete]

yearlist = ["2012", "2013", "2014", "2015", "2016", "2017", "2019", ]


def importdata(reload_s):
    if (not os.path.exists('satisfaction.csv')) or reload_s:
        df_s = pd.DataFrame(cbsodata.get_data('81928NED'))
        path = os.getcwd()
        path = os.path.join(path, 'satisfaction.csv')
        df_s.to_csv(path, index=False)
    return pd.read_csv('satisfaction.csv', header=0, index_col=0, dtype={'ID': int, 'Marges': str, 'RegioS': str,
                                                                         'Perioden': str})


def selection(df_crimes_s, year_s, subset_item_s):
    # only get the correct year
    df_crimes_s = df_crimes_s[df_crimes_s['Marges'] == 'Waarde']
    df_crimes_s = df_crimes_s[df_crimes_s['Perioden'] == year_s]
    # select type of crime, regio and state of crimes (all, solved etc)
    df_crimes_s = df_crimes_s[['RegioS', subset_item_s]]
    # fill empty data with 0
    df_crimes_s = df_crimes_s.fillna(0)
    # set the index as the regio
    df_crimes_s = df_crimes_s.set_index('RegioS')
    # round the numbers to int (they were 3.0 for example)
    # df_crimes = df_crimes.round(0).astype(int)
    return df_crimes_s


def fixmunic(df_total):
    df_total = df_total.append(df_total.loc[['Noord-Drenthe (BT)']].rename(index={'Noord-Drenthe (BT)': 'Aa en Hunze'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord-Drenthe (BT)']].rename(index={'Noord-Drenthe (BT)': 'Assen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord-Drenthe (BT)']].rename(index={'Noord-Drenthe (BT)': 'Borger-Odoorn'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuidoost-Drenthe (BT)']].rename(index={'Zuidoost-Drenthe (BT)': 'Coevorden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuidwest-Drenthe (BT)']].rename(index={'Zuidwest-Drenthe (BT)': 'De Wolden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuidwest-Drenthe (BT)']].rename(index={'Zuidwest-Drenthe (BT)': 'Hoogeveen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Drenthe (PV)']].rename(index={'Drenthe (PV)': 'Midden-Drenthe'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord-Drenthe (BT)']].rename(index={'Noord-Drenthe (BT)': 'Noordenveld'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord-Drenthe (BT)']].rename(index={'Noord-Drenthe (BT)': 'Tynaarlo'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuidwest-Drenthe (BT)']].rename(index={'Zuidwest-Drenthe (BT)': 'Westerveld'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Dronten / Noordoostpolder / Urk (BT)']].rename(index={'Dronten / Noordoostpolder / Urk (BT)': 'Dronten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Dronten / Noordoostpolder / Urk (BT)']].rename(index={'Dronten / Noordoostpolder / Urk (BT)': 'Noordoostpolder'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Dronten / Noordoostpolder / Urk (BT)']].rename(index={'Dronten / Noordoostpolder / Urk (BT)': 'Urk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Lelystad / Zeewolde (BT)']].rename(index={'Lelystad / Zeewolde (BT)': 'Zeewolde'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Oost-Fryslân (BT)']].rename(index={'Oost-Fryslân (BT)': 'Achtkarspelen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordwest-Fryslân (BT)']].rename(index={'Noordwest-Fryslân (BT)': 'Ameland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordoost-Fryslân (BT)']].rename(index={'Noordoost-Fryslân (BT)': 'Dantumadeel (Dantumadiel)'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordwest-Fryslân (BT)']].rename(index={'Noordwest-Fryslân (BT)': 'De Friese Meren'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordoost-Fryslân (BT)']].rename(index={'Noordoost-Fryslân (BT)': 'Dongeradeel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordoost-Fryslân (BT)']].rename(index={'Noordoost-Fryslân (BT)': 'Ferwerderadeel (Ferwerderadiel)'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordwest-Fryslân (BT)']].rename(index={'Noordwest-Fryslân (BT)': 'Franekeradeel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordwest-Fryslân (BT)']].rename(index={'Noordwest-Fryslân (BT)': 'Harlingen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordwest-Fryslân (BT)']].rename(index={'Noordwest-Fryslân (BT)': 'Heerenveen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordwest-Fryslân (BT)']].rename(index={'Noordwest-Fryslân (BT)': 'het Bildt'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordoost-Fryslân (BT)']].rename(index={'Noordoost-Fryslân (BT)': 'Kollumerland en Nieuwkruisland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordwest-Fryslân (BT)']].rename(index={'Noordwest-Fryslân (BT)': 'Leeuwarderadeel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordwest-Fryslân (BT)']].rename(index={'Noordwest-Fryslân (BT)': 'Littenseradeel (Littenseradiel)'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordwest-Fryslân (BT)']].rename(index={'Noordwest-Fryslân (BT)': 'Menaldumadeel (Menaldumadiel)'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuidoost-Fryslân (BT)']].rename(index={'Zuidoost-Fryslân (BT)': 'Ooststellingwerf'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuidoost-Fryslân (BT)']].rename(index={'Zuidoost-Fryslân (BT)': 'Opsterland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordwest-Fryslân (BT)']].rename(index={'Noordwest-Fryslân (BT)': 'Schiermonnikoog'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordoost-Fryslân (BT)']].rename(index={'Noordoost-Fryslân (BT)': 'Smallingerland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Súdwest-Fryslân']].rename(index={'Súdwest-Fryslân': 'SÃºdwest-FryslÃ¢n'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordwest-Fryslân (BT)']].rename(index={'Noordwest-Fryslân (BT)': 'Terschelling'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordoost-Fryslân (BT)']].rename(index={'Noordoost-Fryslân (BT)': 'Tietjerksteradeel (Tytsjerksteradiel)'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordwest-Fryslân (BT)']].rename(index={'Noordwest-Fryslân (BT)': 'Vlieland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuidoost-Fryslân (BT)']].rename(index={'Zuidoost-Fryslân (BT)': 'Weststellingwerf'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Achterhoek-Oost (BT)']].rename(index={'Achterhoek-Oost (BT)': 'Aalten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Gelderland Midden (PD)']].rename(index={'Gelderland Midden (PD)': 'Barneveld'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Achterhoek-Oost (BT)']].rename(index={'Achterhoek-Oost (BT)': 'Berkelland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Tweestromenland (BT)']].rename(index={'Tweestromenland (BT)': 'Beuningen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Achterhoek-West (BT)']].rename(index={'Achterhoek-West (BT)': 'Bronckhorst'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord en Oost Gelderland (PD)']].rename(index={'Noord en Oost Gelderland (PD)': 'Brummen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rivierenland-Oost (BT)']].rename(index={'Rivierenland-Oost (BT)': 'Buren'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rivierenland-Oost (BT)']].rename(index={'Rivierenland-Oost (BT)': 'Culemborg'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Achterhoek-West (BT)']].rename(index={'Achterhoek-West (BT)': 'Doesburg'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Achterhoek-West (BT)']].rename(index={'Achterhoek-West (BT)': 'Doetinchem'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Tweestromenland (BT)']].rename(index={'Tweestromenland (BT)': 'Druten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Achterhoek-West (BT)']].rename(index={'Achterhoek-West (BT)': 'Duiven'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Veluwe-Noord (BT)']].rename(index={'Veluwe-Noord (BT)': 'Elburg'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Veluwe-Noord (BT)']].rename(index={'Veluwe-Noord (BT)': 'Epe'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Veluwe-Noord (BT)']].rename(index={'Veluwe-Noord (BT)': 'Ermelo'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rivierenland-West (BT)']].rename(index={'Rivierenland-West (BT)': 'Geldermalsen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Veluwe-Noord (BT)']].rename(index={'Veluwe-Noord (BT)': 'Groesbeek'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Veluwe-Noord (BT)']].rename(index={'Veluwe-Noord (BT)': 'Harderwijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Veluwe-Noord (BT)']].rename(index={'Veluwe-Noord (BT)': 'Hattem'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Veluwe-Noord (BT)']].rename(index={'Veluwe-Noord (BT)': 'Heerde'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord en Oost Gelderland (PD)']].rename(index={'Noord en Oost Gelderland (PD)': 'Heumen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rivierenland-West (BT)']].rename(index={'Rivierenland-West (BT)': 'Lingewaal'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord en Oost Gelderland (PD)']].rename(index={'Noord en Oost Gelderland (PD)': 'Lingewaard'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Achterhoek-West (BT)']].rename(index={'Achterhoek-West (BT)': 'Lochem'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rivierenland-West (BT)']].rename(index={'Rivierenland-West (BT)': 'Maasdriel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Achterhoek-West (BT)']].rename(index={'Achterhoek-West (BT)': 'Montferland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rivierenland-Oost (BT)']].rename(index={'Rivierenland-Oost (BT)': 'Neder-Betuwe'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rivierenland-West (BT)']].rename(index={'Rivierenland-West (BT)': 'Neerijnen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Veluwe-West (BT)']].rename(index={'Veluwe-West (BT)': 'Nijkerk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Veluwe-West (BT)']].rename(index={'Veluwe-West (BT)': 'Nunspeet'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Veluwe-Noord (BT)']].rename(index={'Veluwe-Noord (BT)': 'Oldebroek'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Achterhoek-Oost (BT)']].rename(index={'Achterhoek-Oost (BT)': 'Oost Gelre'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Achterhoek-West (BT)']].rename(index={'Achterhoek-West (BT)': 'Oude IJsselstreek'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord en Oost Gelderland (PD)']].rename(index={'Noord en Oost Gelderland (PD)': 'Overbetuwe'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Veluwe-West (BT)']].rename(index={'Veluwe-West (BT)': 'Putten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Veluwe Vallei-Noord (BT)']].rename(index={'Veluwe Vallei-Noord (BT)': 'Renkum'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Veluwe Vallei-Noord (BT)']].rename(index={'Veluwe Vallei-Noord (BT)': 'Rheden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Achterhoek-West (BT)']].rename(index={'Achterhoek-West (BT)': 'Rijnwaarden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Veluwe Vallei-Noord (BT)']].rename(index={'Veluwe Vallei-Noord (BT)': 'Rozendaal'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Veluwe-West (BT)']].rename(index={'Veluwe-West (BT)': 'Scherpenzeel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rivierenland-Oost (BT)']].rename(index={'Rivierenland-Oost (BT)': 'Tiel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Veluwe-Noord (BT)']].rename(index={'Veluwe-Noord (BT)': 'Voorst'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Veluwe Vallei-Noord (BT)']].rename(index={'Veluwe Vallei-Noord (BT)': 'Wageningen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Tweestromenland (BT)']].rename(index={'Tweestromenland (BT)': 'West Maas en Waal'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Achterhoek-West (BT)']].rename(index={'Achterhoek-West (BT)': 'Westervoort'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Tweestromenland (BT)']].rename(index={'Tweestromenland (BT)': 'Wijchen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Achterhoek-Oost (BT)']].rename(index={'Achterhoek-Oost (BT)': 'Winterswijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rivierenland-West (BT)']].rename(index={'Rivierenland-West (BT)': 'Zaltbommel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Achterhoek-West (BT)']].rename(index={'Achterhoek-West (BT)': 'Zevenaar'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Achterhoek-West (BT)']].rename(index={'Achterhoek-West (BT)': 'Zutphen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen-Noord (BT)']].rename(index={'Groningen-Noord (BT)': 'Appingedam'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen-Noord (BT)']].rename(index={'Groningen-Noord (BT)': 'Bedum'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen-Noord (BT)']].rename(index={'Groningen-Noord (BT)': 'Bellingwedde'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen-Noord (BT)']].rename(index={'Groningen-Noord (BT)': 'De Marne'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen-Noord (BT)']].rename(index={'Groningen-Noord (BT)': 'Delfzijl'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen-Noord (BT)']].rename(index={'Groningen-Noord (BT)': 'Eemsmond'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (gemeente)']].rename(index={'Groningen (gemeente)': 'Groningen (Gr)'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Westerkwartier (BT)']].rename(index={'Westerkwartier (BT)': 'Grootegast'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen-Centrum (BT)']].rename(index={'Groningen-Centrum (BT)': 'Haren'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen-Centrum (BT)']].rename(index={'Groningen-Centrum (BT)': 'Hoogezand-Sappemeer'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Westerkwartier (BT)']].rename(index={'Westerkwartier (BT)': 'Leek'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen-Centrum (BT)']].rename(index={'Groningen-Centrum (BT)': 'Loppersum'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Westerkwartier (BT)']].rename(index={'Westerkwartier (BT)': 'Marum'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen-Centrum (BT)']].rename(index={'Groningen-Centrum (BT)': 'Menterwolde'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen-Centrum (BT)']].rename(index={'Groningen-Centrum (BT)': 'Oldambt'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen-Centrum (BT)']].rename(index={'Groningen-Centrum (BT)': 'Pekela'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen-Centrum (BT)']].rename(index={'Groningen-Centrum (BT)': 'Slochteren'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen-Zuid (BT)']].rename(index={'Groningen-Zuid (BT)': 'Stadskanaal'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen-Noord (BT)']].rename(index={'Groningen-Noord (BT)': 'Ten Boer'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen-Zuid (BT)']].rename(index={'Groningen-Zuid (BT)': 'Veendam'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen-Zuid (BT)']].rename(index={'Groningen-Zuid (BT)': 'Vlagtwedde'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Westerkwartier (BT)']].rename(index={'Westerkwartier (BT)': 'Winsum'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Westerkwartier (BT)']].rename(index={'Westerkwartier (BT)': 'Zuidhorn'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord en Midden Limburg (PD)']].rename(index={'Noord en Midden Limburg (PD)': 'Beek'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord en Midden Limburg (PD)']].rename(index={'Noord en Midden Limburg (PD)': 'Bergen (L)'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Brunssum / Landgraaf (BT)']].rename(index={'Brunssum / Landgraaf (BT)': 'Brunssum'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Echt (BT)']].rename(index={'Echt (BT)': 'Echt-Susteren'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuid-West-Limburg (PD)']].rename(index={'Zuid-West-Limburg (PD)': 'Eijsden-Margraten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Venray / Gennep (BT)']].rename(index={'Venray / Gennep (BT)': 'Gennep'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuid-West-Limburg (PD)']].rename(index={'Zuid-West-Limburg (PD)': 'Gulpen-Wittem'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Horst / Peel en Maas (BT)']].rename(index={'Horst / Peel en Maas (BT)': 'Horst aan de Maas'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Kerkrade (BT)']].rename(index={'Kerkrade (BT)': 'Kerkrade'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Brunssum / Landgraaf (BT)']].rename(index={'Brunssum / Landgraaf (BT)': 'Landgraaf'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord en Midden Limburg (PD)']].rename(index={'Noord en Midden Limburg (PD)': 'Leudal'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord en Midden Limburg (PD)']].rename(index={'Noord en Midden Limburg (PD)': 'Maasgouw'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuid-West-Limburg (PD)']].rename(index={'Zuid-West-Limburg (PD)': 'Meerssen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord en Midden Limburg (PD)']].rename(index={'Noord en Midden Limburg (PD)': 'Mook en Middelaar'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord en Midden Limburg (PD)']].rename(index={'Noord en Midden Limburg (PD)': 'Nederweert'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuid-West-Limburg (PD)']].rename(index={'Zuid-West-Limburg (PD)': 'Nuth'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord en Midden Limburg (PD)']].rename(index={'Noord en Midden Limburg (PD)': 'Onderbanken'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Horst / Peel en Maas (BT)']].rename(index={'Horst / Peel en Maas (BT)': 'Peel en Maas'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord en Midden Limburg (PD)']].rename(index={'Noord en Midden Limburg (PD)': 'Roerdalen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Roermond (BT)']].rename(index={'Roermond (BT)': 'Roermond'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord en Midden Limburg (PD)']].rename(index={'Noord en Midden Limburg (PD)': 'Schinnen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuid-West-Limburg (PD)']].rename(index={'Zuid-West-Limburg (PD)': 'Simpelveld'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord en Midden Limburg (PD)']].rename(index={'Noord en Midden Limburg (PD)': 'Stein'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuid-West-Limburg (PD)']].rename(index={'Zuid-West-Limburg (PD)': 'Vaals'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuid-West-Limburg (PD)']].rename(index={'Zuid-West-Limburg (PD)': 'Valkenburg aan de Geul'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Venray / Gennep (BT)']].rename(index={'Venray / Gennep (BT)': 'Venray'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuid-West-Limburg (PD)']].rename(index={'Zuid-West-Limburg (PD)': 'Voerendaal'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Weert (BT)']].rename(index={'Weert (BT)': 'Weert'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland - West-Brabant (RE)']].rename(index={'Zeeland - West-Brabant (RE)': 'Aalburg'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Hart van Brabant (PD)']].rename(index={'Hart van Brabant (PD)': 'Alphen-Chaam'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Peelland (BT)']].rename(index={'Peelland (BT)': 'Asten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Hart van Brabant (PD)']].rename(index={'Hart van Brabant (PD)': 'Baarle-Nassau'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['De Kempen (BT)']].rename(index={'De Kempen (BT)': 'Bergeijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Bergen op Zoom (BT)']].rename(index={'Bergen op Zoom (BT)': 'Bergen op Zoom'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Oost-Brabant (RE)']].rename(index={'Oost-Brabant (RE)': 'Bernheze'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Eindhoven-Noord (BT)']].rename(index={'Eindhoven-Noord (BT)': 'Best'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['De Kempen (BT)']].rename(index={'De Kempen (BT)': 'Bladel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Oost-Brabant (RE)']].rename(index={'Oost-Brabant (RE)': 'Boekel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Oost-Brabant (RE)']].rename(index={'Oost-Brabant (RE)': 'Boxmeer'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Oost-Brabant (RE)']].rename(index={'Oost-Brabant (RE)': 'Boxtel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['De Kempen (BT)']].rename(index={'De Kempen (BT)': 'Cranendonck'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Oost-Brabant (RE)']].rename(index={'Oost-Brabant (RE)': 'Cuijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Peelland (BT)']].rename(index={'Peelland (BT)': 'Deurne'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Hart van Brabant (PD)']].rename(index={'Hart van Brabant (PD)': 'Dongen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland - West-Brabant (RE)']].rename(index={'Zeeland - West-Brabant (RE)': 'Drimmelen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['De Kempen (BT)']].rename(index={'De Kempen (BT)': 'Eersel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland - West-Brabant (RE)']].rename(index={'Zeeland - West-Brabant (RE)': 'Etten-Leur'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland - West-Brabant (RE)']].rename(index={'Zeeland - West-Brabant (RE)': 'Geertruidenberg'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Eindhoven-Zuid (BT)']].rename(index={'Eindhoven-Zuid (BT)': 'Geldrop-Mierlo'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Eindhoven-Noord (BT)']].rename(index={'Eindhoven-Noord (BT)': 'Gemert-Bakel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Hart van Brabant (PD)']].rename(index={'Hart van Brabant (PD)': 'Gilze en Rijen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Hart van Brabant (PD)']].rename(index={'Hart van Brabant (PD)': 'Goirle'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Oost-Brabant (RE)']].rename(index={'Oost-Brabant (RE)': 'Grave'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Oost-Brabant (RE)']].rename(index={'Oost-Brabant (RE)': 'Haaren'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland - West-Brabant (RE)']].rename(index={'Zeeland - West-Brabant (RE)': 'Halderberge'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['De Kempen (BT)']].rename(index={'De Kempen (BT)': 'Heeze-Leende'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Hart van Brabant (PD)']].rename(index={'Hart van Brabant (PD)': 'Heusden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Hart van Brabant (PD)']].rename(index={'Hart van Brabant (PD)': 'Hilvarenbeek'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Peelland (BT)']].rename(index={'Peelland (BT)': 'Laarbeek'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Oost-Brabant (RE)']].rename(index={'Oost-Brabant (RE)': 'Landerd'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Hart van Brabant (PD)']].rename(index={'Hart van Brabant (PD)': 'Loon op Zand'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Oost-Brabant (RE)']].rename(index={'Oost-Brabant (RE)': 'Maasdonk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Oost-Brabant (RE)']].rename(index={'Oost-Brabant (RE)': 'Mill en Sint Hubert'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland - West-Brabant (RE)']].rename(index={'Zeeland - West-Brabant (RE)': 'Moerdijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Peelland (BT)']].rename(index={'Peelland (BT)': 'Nuenen, Gerwen en Nederwetten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Eindhoven-Noord (BT)']].rename(index={'Eindhoven-Noord (BT)': 'Oirschot'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Hart van Brabant (PD)']].rename(index={'Hart van Brabant (PD)': 'Oisterwijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland - West-Brabant (RE)']].rename(index={'Zeeland - West-Brabant (RE)': 'Oosterhout'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['De Kempen (BT)']].rename(index={'De Kempen (BT)': 'Reusel-De Mierden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland - West-Brabant (RE)']].rename(index={'Zeeland - West-Brabant (RE)': 'Rucphen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Meierijstad']].rename(index={'Meierijstad': 'Schijndel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Oost-Brabant (RE)']].rename(index={'Oost-Brabant (RE)': 'Sint Anthonis'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Oost-Brabant (RE)']].rename(index={'Oost-Brabant (RE)': 'Sint-Michielsgestel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Meierijstad']].rename(index={'Meierijstad': 'Sint-Oedenrode'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Peelland (BT)']].rename(index={'Peelland (BT)': 'Someren'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Eindhoven-Noord (BT)']].rename(index={'Eindhoven-Noord (BT)': 'Son en Breugel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland - West-Brabant (RE)']].rename(index={'Zeeland - West-Brabant (RE)': 'Steenbergen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Oost-Brabant (RE)']].rename(index={'Oost-Brabant (RE)': 'Uden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['De Kempen (BT)']].rename(index={'De Kempen (BT)': 'Valkenswaard'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Meierijstad']].rename(index={'Meierijstad': 'Veghel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Eindhoven-Zuid (BT)']].rename(index={'Eindhoven-Zuid (BT)': 'Veldhoven'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Oost-Brabant (RE)']].rename(index={'Oost-Brabant (RE)': 'Vught'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Eindhoven-Zuid (BT)']].rename(index={'Eindhoven-Zuid (BT)': 'Waalre'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Hart van Brabant (PD)']].rename(index={'Hart van Brabant (PD)': 'Waalwijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland - West-Brabant (RE)']].rename(index={'Zeeland - West-Brabant (RE)': 'Werkendam'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland - West-Brabant (RE)']].rename(index={'Zeeland - West-Brabant (RE)': 'Woensdrecht'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Oost-Brabant (RE)']].rename(index={'Oost-Brabant (RE)': 'Woudrichem'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland - West-Brabant (RE)']].rename(index={'Zeeland - West-Brabant (RE)': 'Zundert'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Aalsmeer - Uithoorn (BT)']].rename(index={'Aalsmeer - Uithoorn (BT)': 'Aalsmeer'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zaanstreek Waterland (PD)']].rename(index={'Zaanstreek Waterland (PD)': 'Beemster'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Kennemerland (PD)']].rename(index={'Kennemerland (PD)': 'Bergen (NH)'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['IJmond (BT)']].rename(index={'IJmond (BT)': 'Beverwijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Gooi en Vechtstreek (PD)']].rename(index={'Gooi en Vechtstreek (PD)': 'Blaricum'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Kennemerland (PD)']].rename(index={'Kennemerland (PD)': 'Bloemendaal'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Gooi en Vechtstreek (PD)']].rename(index={'Gooi en Vechtstreek (PD)': 'Bussum'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Kennemerland (PD)']].rename(index={'Kennemerland (PD)': 'Castricum'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Den Helder (BT)']].rename(index={'Den Helder (BT)': 'Den Helder'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Diemen-Ouder-Amstel (BT)']].rename(index={'Diemen-Ouder-Amstel (BT)': 'Diemen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordwest-Fryslân (BT)']].rename(index={'Noordwest-Fryslân (BT)': 'Drechterland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zaanstreek Waterland (PD)']].rename(index={'Zaanstreek Waterland (PD)': 'Edam-Volendam'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordwest-Fryslân (BT)']].rename(index={'Noordwest-Fryslân (BT)': 'Enkhuizen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Amstelveen (BT)']].rename(index={'Amstelveen (BT)': 'Haarlemmerliede en Spaarnwoude'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['IJmond (BT)']].rename(index={'IJmond (BT)': 'Heemskerk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Kennemerland (PD)']].rename(index={'Kennemerland (PD)': 'Heemstede'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Heerhugowaard (BT)']].rename(index={'Heerhugowaard (BT)': 'Heerhugowaard'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Kennemerland (PD)']].rename(index={'Kennemerland (PD)': 'Heiloo'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord Holland Noord (PD)']].rename(index={'Noord Holland Noord (PD)': 'Hollands Kroon'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Gooi en Vechtstreek (PD)']].rename(index={'Gooi en Vechtstreek (PD)': 'Huizen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordwest-Fryslân (BT)']].rename(index={'Noordwest-Fryslân (BT)': 'Koggenland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zaanstreek Waterland (PD)']].rename(index={'Zaanstreek Waterland (PD)': 'Landsmeer'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Alkmaar (BT)']].rename(index={'Alkmaar (BT)': 'Langedijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Gooi en Vechtstreek (PD)']].rename(index={'Gooi en Vechtstreek (PD)': 'Laren'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordwest-Fryslân (BT)']].rename(index={'Noordwest-Fryslân (BT)': 'Medemblik'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Gooi en Vechtstreek (PD)']].rename(index={'Gooi en Vechtstreek (PD)': 'Muiden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Gooi en Vechtstreek (PD)']].rename(index={'Gooi en Vechtstreek (PD)': 'Naarden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zaanstreek Waterland (PD)']].rename(index={'Zaanstreek Waterland (PD)': 'Oostzaan'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordwest-Fryslân (BT)']].rename(index={'Noordwest-Fryslân (BT)': 'Opmeer'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Amstelveen (BT)']].rename(index={'Amstelveen (BT)': 'Ouder-Amstel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord Holland Noord (PD)']].rename(index={'Noord Holland Noord (PD)': 'Schagen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordwest-Fryslân (BT)']].rename(index={'Noordwest-Fryslân (BT)': 'Stede Broec'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord Holland Noord (PD)']].rename(index={'Noord Holland Noord (PD)': 'Texel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Kennemerland (PD)']].rename(index={'Kennemerland (PD)': 'Uitgeest'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Aalsmeer - Uithoorn (BT)']].rename(index={'Aalsmeer - Uithoorn (BT)': 'Uithoorn'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['IJmond (BT)']].rename(index={'IJmond (BT)': 'Velsen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zaanstreek Waterland (PD)']].rename(index={'Zaanstreek Waterland (PD)': 'Waterland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Gooi en Vechtstreek (PD)']].rename(index={'Gooi en Vechtstreek (PD)': 'Weesp'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Gooi en Vechtstreek (PD)']].rename(index={'Gooi en Vechtstreek (PD)': 'Wijdemeren'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zaanstreek Waterland (PD)']].rename(index={'Zaanstreek Waterland (PD)': 'Wormerland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Kennemerland (PD)']].rename(index={'Kennemerland (PD)': 'Zandvoort'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noord Holland Noord (PD)']].rename(index={'Noord Holland Noord (PD)': 'Zeevang'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Twente-Midden (BT)']].rename(index={'Twente-Midden (BT)': 'Borne'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Vechtdal (BT)']].rename(index={'Vechtdal (BT)': 'Dalfsen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Twente-Noord (BT)']].rename(index={'Twente-Noord (BT)': 'Dinkelland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Twente-Midden (BT)']].rename(index={'Twente-Midden (BT)': 'Haaksbergen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Vechtdal (BT)']].rename(index={'Vechtdal (BT)': 'Hardenberg'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Twente-West (BT)']].rename(index={'Twente-West (BT)': 'Hellendoorn'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Twente-Midden (BT)']].rename(index={'Twente-Midden (BT)': 'Hengelo (O)'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Twente-West (BT)']].rename(index={'Twente-West (BT)': 'Hof van Twente'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['IJsselland-Noord (BT)']].rename(index={'IJsselland-Noord (BT)': 'Kampen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Twente-Midden (BT)']].rename(index={'Twente-Midden (BT)': 'Losser'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Twente-Midden (BT)']].rename(index={'Twente-Midden (BT)': 'Oldenzaal'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['IJsselland-Zuid (BT)']].rename(index={'IJsselland-Zuid (BT)': 'Olst-Wijhe'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Vechtdal (BT)']].rename(index={'Vechtdal (BT)': 'Ommen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['IJsselland-Zuid (BT)']].rename(index={'IJsselland-Zuid (BT)': 'Raalte'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Twente-West (BT)']].rename(index={'Twente-West (BT)': 'Rijssen-Holten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['IJsselland-Noord (BT)']].rename(index={'IJsselland-Noord (BT)': 'Staphorst'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['IJsselland-Noord (BT)']].rename(index={'IJsselland-Noord (BT)': 'Steenwijkerland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Twente-Noord (BT)']].rename(index={'Twente-Noord (BT)': 'Tubbergen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Twente-Noord (BT)']].rename(index={'Twente-Noord (BT)': 'Twenterand'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Twente-West (BT)']].rename(index={'Twente-West (BT)': 'Wierden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['IJsselland-Noord (BT)']].rename(index={'IJsselland-Noord (BT)': 'Zwartewaterland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Oost Utrecht (PD)']].rename(index={'Oost Utrecht (PD)': 'Baarn'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeist/Bunnik/Leusden/Woudenberg (BT)']].rename(index={'Zeist/Bunnik/Leusden/Woudenberg (BT)': 'Bunnik'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Oost Utrecht (PD)']].rename(index={'Oost Utrecht (PD)': 'Bunschoten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['De Bilt Eemdal Soest (BT)']].rename(index={'De Bilt Eemdal Soest (BT)': 'De Bilt'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['De Ronde Venen / Stichtse Vecht (BT)']].rename(index={'De Ronde Venen / Stichtse Vecht (BT)': 'De Ronde Venen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Oost Utrecht (PD)']].rename(index={'Oost Utrecht (PD)': 'Eemnes'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Utrecht-Zuid (BT)']].rename(index={'Utrecht-Zuid (BT)': 'Houten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Utrecht-Zuid (BT)']].rename(index={'Utrecht-Zuid (BT)': 'IJsselstein'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeist/Bunnik/Leusden/Woudenberg (BT)']].rename(index={'Zeist/Bunnik/Leusden/Woudenberg (BT)': 'Leusden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Utrecht-Zuid (BT)']].rename(index={'Utrecht-Zuid (BT)': 'Lopik'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Utrecht-West (BT)']].rename(index={'Utrecht-West (BT)': 'Montfoort'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Utrecht-Zuid (BT)']].rename(index={'Utrecht-Zuid (BT)': 'Nieuwegein'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Utrecht-West (BT)']].rename(index={'Utrecht-West (BT)': 'Oudewater'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Veluwe Vallei-Noord (BT)']].rename(index={'Veluwe Vallei-Noord (BT)': 'Renswoude'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Veluwe Vallei-Noord (BT)']].rename(index={'Veluwe Vallei-Noord (BT)': 'Rhenen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['De Bilt Eemdal Soest (BT)']].rename(index={'De Bilt Eemdal Soest (BT)': 'Soest'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['De Ronde Venen / Stichtse Vecht (BT)']].rename(index={'De Ronde Venen / Stichtse Vecht (BT)': 'Stichtse Vecht'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Utrecht (gemeente)']].rename(index={'Utrecht (gemeente)': 'Utrecht (Ut)'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Heuvelrug (BT)']].rename(index={'Heuvelrug (BT)': 'Utrechtse Heuvelrug'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Veluwe Vallei-Noord (BT)']].rename(index={'Veluwe Vallei-Noord (BT)': 'Veenendaal'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Utrecht-Zuid (BT)']].rename(index={'Utrecht-Zuid (BT)': 'Vianen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeist/Bunnik/Leusden/Woudenberg (BT)']].rename(index={'Zeist/Bunnik/Leusden/Woudenberg (BT)': 'Wijk bij Duurstede'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Utrecht-West (BT)']].rename(index={'Utrecht-West (BT)': 'Woerden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeist/Bunnik/Leusden/Woudenberg (BT)']].rename(index={'Zeist/Bunnik/Leusden/Woudenberg (BT)': 'Woudenberg'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeist/Bunnik/Leusden/Woudenberg (BT)']].rename(index={'Zeist/Bunnik/Leusden/Woudenberg (BT)': 'Zeist'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland (PD)']].rename(index={'Zeeland (PD)': 'Borsele'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland (PD)']].rename(index={'Zeeland (PD)': 'Goes'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeuws-Vlaanderen (BT)']].rename(index={'Zeeuws-Vlaanderen (BT)': 'Hulst'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland (PD)']].rename(index={'Zeeland (PD)': 'Kapelle'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland (PD)']].rename(index={'Zeeland (PD)': 'Middelburg'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland (PD)']].rename(index={'Zeeland (PD)': 'Noord-Beveland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland (PD)']].rename(index={'Zeeland (PD)': 'Reimerswaal'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland (PD)']].rename(index={'Zeeland (PD)': 'Schouwen-Duiveland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeuws-Vlaanderen (BT)']].rename(index={'Zeeuws-Vlaanderen (BT)': 'Sluis'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeuws-Vlaanderen (BT)']].rename(index={'Zeeuws-Vlaanderen (BT)': 'Terneuzen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland (PD)']].rename(index={'Zeeland (PD)': 'Tholen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland (PD)']].rename(index={'Zeeland (PD)': 'Veere'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zeeland (PD)']].rename(index={'Zeeland (PD)': 'Vlissingen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['De Waarden (BT)']].rename(index={'De Waarden (BT)': 'Alblasserdam'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['IJsselmonde (BT)']].rename(index={'IJsselmonde (BT)': 'Albrandswaard'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['IJsselmonde (BT)']].rename(index={'IJsselmonde (BT)': 'Barendrecht'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rijnmond Zuid-West (PD)']].rename(index={'Rijnmond Zuid-West (PD)': 'Binnenmaas'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Gouda (BT)']].rename(index={'Gouda (BT)': 'Bodegraven-Reeuwijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuid-Holland-Zuid (PD)']].rename(index={'Zuid-Holland-Zuid (PD)': 'Brielle'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rijnmond Noord (PD)']].rename(index={'Rijnmond Noord (PD)': 'Capelle aan den IJssel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rijnmond Zuid-West (PD)']].rename(index={'Rijnmond Zuid-West (PD)': 'Cromstrijen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rijnmond Oost (PD)']].rename(index={'Rijnmond Oost (PD)': 'Giessenlanden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuid-Holland-Zuid (PD)']].rename(index={'Zuid-Holland-Zuid (PD)': 'Goeree-Overflakkee'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['De Waarden (BT)']].rename(index={'De Waarden (BT)': 'Gorinchem'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rijnmond Oost (PD)']].rename(index={'Rijnmond Oost (PD)': 'Hardinxveld-Giessendam'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuid-Holland-Zuid (PD)']].rename(index={'Zuid-Holland-Zuid (PD)': 'Hellevoetsluis'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['IJsselmonde (BT)']].rename(index={'IJsselmonde (BT)': 'Hendrik-Ido-Ambacht'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Bollenstreek-Noord (BT)']].rename(index={'Bollenstreek-Noord (BT)': 'Hillegom'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Kaag en Braassem (BT)']].rename(index={'Kaag en Braassem (BT)': 'Kaag en Braassem'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Katwijk (BT)']].rename(index={'Katwijk (BT)': 'Katwijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rijnmond Zuid-West (PD)']].rename(index={'Rijnmond Zuid-West (PD)': 'Korendijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rijnmond Oost (PD)']].rename(index={'Rijnmond Oost (PD)': 'Krimpen aan den IJssel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Krimpenerwaard (BT)']].rename(index={'Krimpenerwaard (BT)': 'Krimpenerwaard'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Westland - Delft (PD)']].rename(index={'Westland - Delft (PD)': 'Lansingerland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['De Waarden (BT)']].rename(index={'De Waarden (BT)': 'Leerdam'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Leiden - Bollenstreek (PD)']].rename(index={'Leiden - Bollenstreek (PD)': 'Leiderdorp'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Leiden - Bollenstreek (PD)']].rename(index={'Leiden - Bollenstreek (PD)': 'Lisse'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Westland - Delft (PD)']].rename(index={'Westland - Delft (PD)': 'Maassluis'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Westland (BT)']].rename(index={'Westland (BT)': 'Midden-Delfland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rijnmond Oost (PD)']].rename(index={'Rijnmond Oost (PD)': 'Molenwaard'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rijnmond Noord (PD)']].rename(index={'Rijnmond Noord (PD)': 'Nieuwkoop'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Noordwijk (BT)']].rename(index={'Noordwijk (BT)': 'Noordwijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Bollenstreek-Noord (BT)']].rename(index={'Bollenstreek-Noord (BT)': 'Noordwijkerhout'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Leiden - Bollenstreek (PD)']].rename(index={'Leiden - Bollenstreek (PD)': 'Oegstgeest'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuid-Holland-Zuid (PD)']].rename(index={'Zuid-Holland-Zuid (PD)': 'Oud-Beijerland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rijnmond Oost (PD)']].rename(index={'Rijnmond Oost (PD)': 'Papendrecht'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Pijnacker - Nootdorp (BT)']].rename(index={'Pijnacker - Nootdorp (BT)': 'Pijnacker-Nootdorp'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['IJsselmonde (BT)']].rename(index={'IJsselmonde (BT)': 'Ridderkerk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rijswijk (BT)']].rename(index={'Rijswijk (BT)': 'Rijswijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Den Haag Centrum (PD)']].rename(index={'Den Haag Centrum (PD)': "'s-Gravenhage"}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rijnmond Oost (PD)']].rename(index={'Rijnmond Oost (PD)': 'Sliedrecht'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuid-Holland-Zuid (PD)']].rename(index={'Zuid-Holland-Zuid (PD)': 'Strijen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Leiden-Noord (BT)']].rename(index={'Leiden-Noord (BT)': 'Teylingen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Leiden-Zuid (BT)']].rename(index={'Leiden-Zuid (BT)': 'Voorschoten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Waddinxveen / Zuidplas (BT)']].rename(index={'Waddinxveen / Zuidplas (BT)': 'Waddinxveen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Wassenaar (BT)']].rename(index={'Wassenaar (BT)': 'Wassenaar'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuid-Holland-Zuid (PD)']].rename(index={'Zuid-Holland-Zuid (PD)': 'Westvoorne'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Rijnmond Oost (PD)']].rename(index={'Rijnmond Oost (PD)': 'Zederik'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zoetermeer']].rename(index={'Zoetermeer': 'Zoeterwoude'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Waddinxveen / Zuidplas (BT)']].rename(index={'Waddinxveen / Zuidplas (BT)': 'Zuidplas'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['IJsselmonde (BT)']].rename(index={'IJsselmonde (BT)': 'Zwijndrecht'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Zuidwest-Drenthe (BT)']].rename(index={'Zuidwest-Drenthe (BT)': 'Meppel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Venlo / Beesel (BT)']].rename(index={'Venlo / Beesel (BT)': 'Beesel'}), ignore_index=False)


    return df_total


def merge_crimes(unfindable_s, dutch_municipalities_dict_s, df_total, subset_s):
    municipality = dutch_municipalities_dict_s['properties']['name']

    try:
        dutch_municipalities_dict_s['properties']['Crimes'] = round(
            df_total[subset_s][municipality], 1).astype('float')
    except KeyError:
        unfindable_s.append(municipality)
        dutch_municipalities_dict_s['properties']['Crimes'] = 0.0
    return dutch_municipalities_dict_s


def create_figure(dutch_municipalities_dict_s, palette_s):
    geo_source = GeoJSONDataSource(geojson=json.dumps(dutch_municipalities_dict_s))
    color_mapper = EqHistColorMapper(bins=100000, palette=palette_s)

    TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,save"

    p = bokeh.plotting.figure(
        background_fill_color="white", title=str("Data per municipality. " + year + ", " + str(
            list(subset_itemlist.keys())[list(subset_itemlist.values()).index(subset_item)])), tools=TOOLS,
        x_axis_location=None, y_axis_location=None
    )

    p.grid.grid_line_color = None

    p.patches('xs', 'ys', source=geo_source,
              fill_color={'field': 'Crimes', 'transform': color_mapper},
              fill_alpha=0.7, line_color="lightgrey", line_width=0.5)

    hover = p.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    hover.tooltips = [
        ("Name", "@name"),
        ("Crimes", "@Crimes{0.0}"),
        # ("(Long, Lat)", "($x, $y)"),
    ]
    return p


def update_figure(reload_s, year_s, subset_s, palette_s):
    reload_a = True if (reload_s == 'Yes') else False
    # load the data, if reload is true, it will reload data from cbs
    df_s = importdata(reload_a)
    # select the correct year and type
    df_s = selection(df_s, year_s, subset_s)
    # fix the weird municipalities
    df_s = fixmunic(df_s)
    unfindables = []
    with open(r'Gemeenten.geojson', 'r') as f_s:
        dutch_municipalities_dicts = json.loads(f_s.read(), object_hook=OrderedDict)
    dutch_municipalities_dicts['features'] = [merge_crimes(unfindables, municipality, df_s, subset_s) for municipality
                                              in
                                              dutch_municipalities_dicts['features']]
    return create_figure(dutch_municipalities_dicts, palette_s)


# To update the figure, have to send back after drop down
def update(attr, old, new):
    global year, reload, subset_item, palette
    if new in yearlist:
        year = new
    elif new in subset_itemlist:
        subset_item = subset_itemlist[new]
    elif new in ["Yes", "No"]:
        reload = new
    elif new in colourlist:
        palette = colourlist[new]
    layout.children[1] = update_figure(reload, year, subset_item, palette)


# set all the variables, should be replaced by sliders/buttons
subset_item = 'VertrouwenInPolitieSchaalscore_51'
year = '2017'
reload = False
unfindable = []
palette = colourlist['Red']

# load the data, if reload is true, it will reload data from cbs
df_crimes = importdata(reload)
# select the correct amount of data
df_crimes = selection(df_crimes, year, subset_item)

# open nl geojson data
with open(r'Gemeenten.geojson', 'r') as f:
    dutch_municipalities_dict = json.loads(f.read(), object_hook=OrderedDict)

# fix the municipalities in the dataframe to match the geojson file
df_crimes = fixmunic(df_crimes)
# merge geojson data with crimedata
dutch_municipalities_dict['features'] = [merge_crimes(unfindable, municipality, df_crimes, subset_item) for
                                         municipality in
                                         dutch_municipalities_dict['features']]
# print all municipalities that can't be found in df
if len(unfindable) > 0:
    print("These municipalities can't be found:")
print(unfindable)
create_figure(dutch_municipalities_dict, palette)

year_sel = Select(title='Year', value='2017', options=yearlist)
year_sel.on_change('value', update)

subset_item_sel = Select(title='Crime subset', value='VertrouwenInPolitieSchaalscore_51',
                         options=list(subset_itemlist.keys()))
subset_item_sel.on_change('value', update)

reload_sel = Select(title='Reload: Warning, will reload data and will take a long time', value='No',
                    options=["Yes", "No"])
reload_sel.on_change('value', update)

colour_sel = Select(title='Colour', value='Red', options=list(colourlist.keys()))
colour_sel.on_change('value', update)

controls = column(year_sel, subset_item_sel, reload_sel, colour_sel, width=200)
layout = row(controls, create_figure(dutch_municipalities_dict, palette))

curdoc().theme = 'dark_minimal'
curdoc().add_root(layout)
curdoc().title = "Crossfilter"
