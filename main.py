def install():
    import pip
    pip.main(['install', 'IPython'])
    pip.main(['install', 'bokeh'])
    pip.main(['install', 'matplotlib'])
    pip.main(['install', 'colorcet'])
    pip.main(['install', 'cbsodata'])

# install()
import bokeh
from bokeh.layouts import column, row
from bokeh.models import Select, Button, CustomJS
from bokeh.palettes import Spectral5
from bokeh.plotting import curdoc, figure
from bokeh.sampledata.autompg import autompg_clean as df

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

yearlist = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021"]
crime_subsetlist=["TotaalGeregistreerdeMisdrijven_1","GeregistreerdeMisdrijvenRelatief_2",
                  "GeregistreerdeMisdrijvenPer1000Inw_3", "TotaalOpgehelderdeMisdrijven_4",
                  "OpgehelderdeMisdrijvenRelatief_5", "RegistratiesVanVerdachten_6"]
typelist = ['Misdrijven, totaal', '1 Vermogensmisdrijven', '11 Diefstal/verduistering en inbraak',
            '111 Diefstal en inbraak met geweld', '112 Diefstal en inbraak zonder geweld', '12 Bedrog', '121 Oplichting',
            '122 Flessentrekkerij', '123 Bedrog (overig)', '13 Valsheidsmisdrijven', '131 Muntmisdrijf',
            '132 Valsheid in zegels en merken', '133 Valsheid in geschriften', '14 Heling', '15 Afpersing en afdreiging',
            '16 Bankbreuk', '17 Witwassen', '18 Vermogensmisdrijf (overig)', '2 Vernielingen,misdropenborde/gezag',
            '21 Vernieling en beschadiging', '211 Vernieling aan auto', '212 Vernieling aan openbaar gebouw',
            '213 Vernieling middel openb vervoer', '215 Vernieling, beschadiging (overig)', '22 Openbare orde misdrijf',
            '221 Openlijke geweldpleging', '2211 Openlijk geweld tegen persoon', '2212 Openlijke geweld tegen goed',
            '222 Huisvredebreuk', '223 Lokaalvredebreuk', '224 Computervredebreuk', '225 Discriminatie',
            '226 Openbare orde misdrijf (overig)', '23 Brandstichting / ontploffing', '24 Openbaar gezag misdrijf',
            '241 Niet opvolgen van ambtelijk bevel', '242 Wederspannigheid', '243 Valse aangifte',
            '245 Verblijf ongewenste vreemdeling', '246 Openbaar gezag misdrijf (overig)',
            '3 Gewelds- en seksuele misdrijven',  '31 Mishandeling', '32 Bedreiging en stalking', '321 Bedreiging',
            '322 Stalking', '33 Seksueel misdrijf', '331 Aanranding', '332 Verkrachting', '333 Schennis der eerbaarheid',
            '334 Ontucht met minderjarige', '335 Pornografie', '336 Ontucht met misbruik van gezag',
            '337 Seksueel misdrijf (overig)', '34 Levensmisdrijf', '35 Vrijheidsbeneming/gijzeling',
            '36 Mensenhandel en 244 mensensmokkel',
            '37 Geweldsmisdrijf (overig)', '4 Misdrijven WvSr (overig)', '5 Verkeersmisdrijven',
            '51 Verlaten plaats ongeval', '52 Rijden onder invloed', '53 Rijden tijdens ontzegging besturen',
            '54 Rijden tijdens rijverbod', '55 Voeren vals kenteken', '56 Joyriding',
            '57 Weigeren blaastest/bloedonderzoek ed', '58 Verkeersmisdrijf (overig)', '6 Drugsmisdrijven',
            '61 Harddrugs', '62 Softdrugs', '6.3 Drugsmisdrijf (overig)', '7 Vuurwapenmisdrijven',
            '9 Misdrijven overige wetten', '91 Militaire misdrijven', '92 Misdrijven (overig)']


import pandas as pd

import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')
from bokeh.plotting import figure, save

from bokeh.io import show, output_notebook
from bokeh.models import (
    GeoJSONDataSource,
    HoverTool,
    EqHistColorMapper
)
import colorcet as cc
# from bokeh.palettes import Turbo256 as palette
import os

import json
from collections import OrderedDict

import cbsodata


def importdata(reload):
    if (not os.path.exists('dataframe.csv')) or reload:
        df = pd.DataFrame(cbsodata.get_data('83648NED'))
        path = os.getcwd()
        path = os.path.join(path, 'dataframe.csv')
        df.to_csv(path, index=False)
    return pd.read_csv('dataframe.csv', header=0, index_col=0, dtype={'ID': int, 'SoortMisdrijf': str, 'RegioS': str,
                                                                      'Perioden': str,
                                                                      'TotaalGeregistreerdeMisdrijven_1': float,
                                                                      'GeregistreerdeMisdrijvenRelatief_2': float,
                                                                      'GeregistreerdeMisdrijvenPer1000Inw_3': float,
                                                                      'TotaalOpgehelderdeMisdrijven_4': float,
                                                                      'OpgehelderdeMisdrijvenRelatief_5': float,
                                                                      'RegistratiesVanVerdachten_6': float})


def selection(df_crimes, year, crime_subset, type_of_crimes):
    # only get the correct year
    df_crimes = df_crimes[df_crimes['Perioden'] == year]
    # select type of crime, regio and state of crimes (all, solved etc)
    df_crimes = df_crimes[['SoortMisdrijf', 'RegioS', crime_subset]]
    # only select the type of crimes that were chosen in beginning
    df_crimes = df_crimes[df_crimes['SoortMisdrijf'] == type_of_crimes]
    # fill empty data with 0
    df_crimes = df_crimes.fillna(0)
    # remove type of crimes from the dataframe as it is all the same
    df_crimes = df_crimes[['RegioS', crime_subset]]
    # set the index as the regio
    df_crimes = df_crimes.set_index('RegioS')
    # round the numbers to int (they were 3.0 for example)
    # df_crimes = df_crimes.round(0).astype(int)
    return df_crimes


def fixmunic(df_total):
    df_total = df_total.rename(index={'Dantumadiel': 'Dantumadeel (Dantumadiel)'})
    df_total = df_total.rename(index={'Ferwerderadiel': 'Ferwerderadeel (Ferwerderadiel)'})
    df_total = df_total.rename(index={'Littenseradiel': 'Littenseradeel (Littenseradiel)'})
    df_total = df_total.rename(index={'Menameradiel': 'Menaldumadeel (Menaldumadiel)'})
    df_total = df_total.rename(index={'Súdwest-Fryslân': 'SÃºdwest-FryslÃ¢n'})
    df_total = df_total.rename(index={'Tytsjerksteradiel': 'Tietjerksteradeel (Tytsjerksteradiel)'})
    df_total = df_total.rename(index={'Bergen (L.)': 'Bergen (L)'})
    df_total = df_total.rename(index={'Bergen (NH.)': 'Bergen (NH)'})
    df_total = df_total.rename(index={'Utrecht (gemeente)': 'Utrecht (Ut)'})
    df_total = df_total.rename(index={'Groningen (gemeente)': 'Groningen (Gr)'})
    df_total = df_total.rename(index={'Beek (L.)': 'Beek'})
    df_total = df_total.rename(index={'Stein (L.)': 'Stein'})
    df_total = df_total.rename(index={'Hengelo (O.)': 'Hengelo (O)'})
    df_total = df_total.rename(index={'Middelburg (Z.)': 'Middelburg'})
    df_total = df_total.rename(index={'Rijswijk (ZH.)': 'Rijswijk'})
    df_total = df_total.rename(index={"'s-Gravenhage (gemeente)": "'s-Gravenhage"})
    df_total = df_total.rename(index={'Laren (NH.)': 'Laren'})
    return df_total


def merge_crimes(unfindable, dutch_municipalities_dict, df_total):
    municipality = dutch_municipalities_dict['properties']['name']

    try:
        dutch_municipalities_dict['properties']['Crimes'] = round(
            df_total[crime_subset][municipality], 1).astype('float')
    except KeyError:
        unfindable.append(municipality)
        dutch_municipalities_dict['properties']['Crimes'] = 0.0
    return dutch_municipalities_dict


def create_figure(dutch_municipalities_dict):

    geo_source = GeoJSONDataSource(geojson=json.dumps(dutch_municipalities_dict))
    color_mapper = EqHistColorMapper(bins=100000, palette=cc.blues)

    TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,save"

    p = bokeh.plotting.figure(
        title="Misdrijven per gemeente", tools=TOOLS,
        x_axis_location=None, y_axis_location=None
    )

    p.grid.grid_line_color = None

    p.patches('xs', 'ys', source=geo_source,
              fill_color={'field': 'Crimes', 'transform': color_mapper},
              fill_alpha=0.7, line_color="white", line_width=0.5)

    hover = p.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    hover.tooltips = [
        ("Name", "@name"),
        ("Crimes", "@Crimes{0.0}"),
        # ("(Long, Lat)", "($x, $y)"),
    ]
    return p


def update_figure(reload_s, year_s, type_s, subset_s):
    reload_a = True if (reload_s == 'Yes') else False
    df = importdata(reload_a)
    df = selection(df, year_s, subset_s, type_s)
    df = fixmunic(df)
    unfindables = []
    with open(r'Gemeenten.geojson', 'r') as f:
        dutch_municipalities_dicts = json.loads(f.read(), object_hook=OrderedDict)
    dutch_municipalities_dicts['features'] = [merge_crimes(unfindables, municipality, df) for municipality in
                                             dutch_municipalities_dicts['features']]
    return create_figure(dutch_municipalities_dicts)


#To update the figure, have to send back after drop down
def update(attr, old, new):
    global year, reload, type_of_crimes, crime_subset
    if new in yearlist:
        year = new
    elif new in crime_subsetlist:
        crime_subset = new
    elif new in typelist:
        type_of_crimes = new
    elif new in ["Yes", "No"]:
        reload = new
    layout.children[1] = update_figure(reload, year, type_of_crimes, crime_subset)


# only run install first time
# install()

# set all the variables, should be replaced by sliders/buttons
crime_subset = 'TotaalGeregistreerdeMisdrijven_1'
year = '2017'
type_of_crimes = 'Misdrijven, totaal'
reload = False
unfindable = []

# load the data, if reload is true, it will reload data from cbs
df_crimes = importdata(reload)

# select the correct amount of data
df_crimes = selection(df_crimes, year, crime_subset, type_of_crimes)

# open nl geojson data
with open(r'Gemeenten.geojson', 'r') as f:
    dutch_municipalities_dict = json.loads(f.read(), object_hook=OrderedDict)

# fix the municipalities in the dataframe to match the geojson file
df_crimes = fixmunic(df_crimes)
# merge geojson data with crimedata
dutch_municipalities_dict['features'] = [merge_crimes(unfindable, municipality, df_crimes) for municipality in
                                         dutch_municipalities_dict['features']]
# print all municipalities that can't be found in df
if len(unfindable) > 0:
    print("These municipalities can't be found:")
print(unfindable)
create_figure(dutch_municipalities_dict)

year_sel = Select(title='Year', value='2017', options=yearlist)
year_sel.on_change('value', update)

crime_subset_sel = Select(title='Crime subset', value='TotaalGeregistreerdeMisdrijven_1', options=crime_subsetlist)
crime_subset_sel.on_change('value', update)

type_of_crime_sel = Select(title='Type of crime', value='Misdrijven, totaal', options=typelist)
type_of_crime_sel.on_change('value', update)

reload_sel = Select(title='Reload', value='No', options=["Yes", "No"])
reload_sel.on_change('value', update)

controls = column(year_sel, crime_subset_sel, reload_sel, type_of_crime_sel, width=200)
layout = row(controls, create_figure(dutch_municipalities_dict))

curdoc().theme = 'dark_minimal'
curdoc().add_root(layout)
curdoc().title = "Crossfilter"

