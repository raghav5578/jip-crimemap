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
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Aa en Hunze'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Assen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Borger-Odoorn'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Coevorden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'De Wolden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Hoogeveen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Midden-Drenthe'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Noordenveld'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Tynaarlo'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Westerveld'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Dronten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Noordoostpolder'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Urk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Zeewolde'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Achtkarspelen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Ameland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Dantumadeel (Dantumadiel)'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'De Friese Meren'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Dongeradeel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Ferwerderadeel (Ferwerderadiel)'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Franekeradeel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Harlingen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Heerenveen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'het Bildt'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Kollumerland en Nieuwkruisland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Leeuwarderadeel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Littenseradeel (Littenseradiel)'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Menaldumadeel (Menaldumadiel)'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Ooststellingwerf'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Opsterland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Schiermonnikoog'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Smallingerland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'SÃºdwest-FryslÃ¢n'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Terschelling'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Tietjerksteradeel (Tytsjerksteradiel)'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Vlieland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Weststellingwerf'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Aalten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Barneveld'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Berkelland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Beuningen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Bronckhorst'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Brummen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Buren'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Culemborg'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Doesburg'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Doetinchem'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Druten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Duiven'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Elburg'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Epe'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Ermelo'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Geldermalsen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Groesbeek'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Harderwijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Hattem'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Heerde'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Heumen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Lingewaal'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Lingewaard'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Lochem'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Maasdriel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Montferland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Neder-Betuwe'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Neerijnen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Nijkerk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Nunspeet'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Oldebroek'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Oost Gelre'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Oude IJsselstreek'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Overbetuwe'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Putten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Renkum'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Rheden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Rijnwaarden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Rozendaal'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Scherpenzeel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Tiel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Voorst'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Wageningen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'West Maas en Waal'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Westervoort'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Wijchen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Winterswijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Zaltbommel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Zevenaar'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Zutphen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Appingedam'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Bedum'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Bellingwedde'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'De Marne'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Delfzijl'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Eemsmond'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Groningen (Gr)'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Grootegast'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Haren'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Hoogezand-Sappemeer'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Leek'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Loppersum'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Marum'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Menterwolde'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Oldambt'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Pekela'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Slochteren'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Stadskanaal'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Ten Boer'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Veendam'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Vlagtwedde'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Winsum'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Zuidhorn'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Beek'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Bergen (L)'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Brunssum'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Echt-Susteren'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Eijsden-Margraten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Gennep'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Gulpen-Wittem'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Horst aan de Maas'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Kerkrade'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Landgraaf'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Leudal'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Maasgouw'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Meerssen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Mook en Middelaar'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Nederweert'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Nuth'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Onderbanken'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Peel en Maas'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Roerdalen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Roermond'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Schinnen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Simpelveld'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Stein'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Vaals'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Valkenburg aan de Geul'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Venray'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Voerendaal'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Weert'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Aalburg'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Alphen-Chaam'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Asten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Baarle-Nassau'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Bergeijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Bergen op Zoom'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Bernheze'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Best'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Bladel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Boekel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Boxmeer'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Boxtel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Cranendonck'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Cuijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Deurne'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Dongen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Drimmelen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Eersel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Etten-Leur'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Geertruidenberg'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Geldrop-Mierlo'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Gemert-Bakel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Gilze en Rijen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Goirle'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Grave'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Haaren'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Halderberge'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Heeze-Leende'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Heusden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Hilvarenbeek'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Laarbeek'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Landerd'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Loon op Zand'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Maasdonk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Mill en Sint Hubert'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Moerdijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Nuenen, Gerwen en Nederwetten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Oirschot'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Oisterwijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Oosterhout'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Reusel-De Mierden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Rucphen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Schijndel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Sint Anthonis'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Sint-Michielsgestel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Sint-Oedenrode'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Someren'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Son en Breugel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Steenbergen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Uden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Valkenswaard'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Veghel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Veldhoven'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Vught'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Waalre'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Waalwijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Werkendam'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Woensdrecht'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Woudrichem'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Zundert'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Aalsmeer'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Beemster'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Bergen (NH)'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Beverwijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Blaricum'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Bloemendaal'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Bussum'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Castricum'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Den Helder'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Diemen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Drechterland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Edam-Volendam'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Enkhuizen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Haarlemmerliede en Spaarnwoude'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Heemskerk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Heemstede'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Heerhugowaard'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Heiloo'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Hollands Kroon'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Huizen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Koggenland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Landsmeer'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Langedijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Laren'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Medemblik'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Muiden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Naarden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Oostzaan'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Opmeer'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Ouder-Amstel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Schagen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Stede Broec'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Texel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Uitgeest'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Uithoorn'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Velsen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Waterland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Weesp'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Wijdemeren'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Wormerland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Zandvoort'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Zeevang'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Borne'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Dalfsen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Dinkelland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Haaksbergen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Hardenberg'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Hellendoorn'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Hengelo (O)'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Hof van Twente'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Kampen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Losser'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Oldenzaal'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Olst-Wijhe'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Ommen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Raalte'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Rijssen-Holten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Staphorst'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Steenwijkerland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Tubbergen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Twenterand'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Wierden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Zwartewaterland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Baarn'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Bunnik'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Bunschoten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'De Bilt'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'De Ronde Venen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Eemnes'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Houten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'IJsselstein'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Leusden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Lopik'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Montfoort'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Nieuwegein'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Oudewater'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Renswoude'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Rhenen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Soest'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Stichtse Vecht'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Utrecht (Ut)'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Utrechtse Heuvelrug'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Veenendaal'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Vianen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Wijk bij Duurstede'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Woerden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Woudenberg'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Zeist'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Borsele'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Goes'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Hulst'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Kapelle'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Middelburg'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Noord-Beveland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Reimerswaal'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Schouwen-Duiveland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Sluis'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Terneuzen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Tholen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Veere'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Vlissingen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Alblasserdam'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Albrandswaard'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Barendrecht'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Binnenmaas'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Bodegraven-Reeuwijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Brielle'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Capelle aan den IJssel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Cromstrijen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Giessenlanden'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Goeree-Overflakkee'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Gorinchem'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Hardinxveld-Giessendam'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Hellevoetsluis'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Hendrik-Ido-Ambacht'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Hillegom'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Kaag en Braassem'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Katwijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Korendijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Krimpen aan den IJssel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Krimpenerwaard'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Lansingerland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Leerdam'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Leiderdorp'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Lisse'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Maassluis'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Midden-Delfland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Molenwaard'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Nieuwkoop'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Noordwijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Noordwijkerhout'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Oegstgeest'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Oud-Beijerland'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Papendrecht'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Pijnacker-Nootdorp'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Ridderkerk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Rijswijk'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': "'s-Gravenhage"}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Sliedrecht'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Strijen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Teylingen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Voorschoten'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Waddinxveen'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Wassenaar'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Westvoorne'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Zederik'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Zoeterwoude'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Zuidplas'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Zwijndrecht'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Meppel'}), ignore_index=False)
    df_total = df_total.append(df_total.loc[['Groningen (PV)']].rename(index={'Groningen (PV)': 'Beesel'}), ignore_index=False)

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
