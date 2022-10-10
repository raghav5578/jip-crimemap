def install():
    import pip
    pip.main(['install', 'IPython'])
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
from dictionaries import typelist, colourlist, crime_subsetlist, chidict, yearlist

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


def importdata(reload_s):
    if (not os.path.exists('dataframe.csv')) or reload_s:
        df_s = pd.DataFrame(cbsodata.get_data('83648NED'))
        path = os.getcwd()
        path = os.path.join(path, 'dataframe.csv')
        df_s.to_csv(path, index=False)
    return pd.read_csv('dataframe.csv', header=0, index_col=0, dtype={'ID': int, 'SoortMisdrijf': str, 'RegioS': str,
                                                                      'Perioden': str,
                                                                      'TotaalGeregistreerdeMisdrijven_1': float,
                                                                      'GeregistreerdeMisdrijvenRelatief_2': float,
                                                                      'GeregistreerdeMisdrijvenPer1000Inw_3': float,
                                                                      'TotaalOpgehelderdeMisdrijven_4': float,
                                                                      'OpgehelderdeMisdrijvenRelatief_5': float,
                                                                      'RegistratiesVanVerdachten_6': float})


def multiplychi_1(rosw):
    return chidict[rosw["SoortMisdrijf"]] * rosw["TotaalGeregistreerdeMisdrijven_1"]


def multiplychi_2(rosw):
    return chidict[rosw["SoortMisdrijf"]] * rosw["GeregistreerdeMisdrijvenRelatief_2"]


def multiplychi_3(rosw):
    return chidict[rosw["SoortMisdrijf"]] * rosw["GeregistreerdeMisdrijvenPer1000Inw_3"]


def multiplychi_4(rosw):
    return chidict[rosw["SoortMisdrijf"]] * rosw["TotaalOpgehelderdeMisdrijven_4"]


def multiplychi_5(rosw):
    return chidict[rosw["SoortMisdrijf"]] * rosw["OpgehelderdeMisdrijvenRelatief_5"]


def multiplychi_6(rosw):
    return chidict[rosw["SoortMisdrijf"]] * rosw["RegistratiesVanVerdachten_6"]


def add_chi(df_crimes_s, reload_s):
    if (not os.path.exists('chidf.pkl')) or reload_s:
        df_crimes_s["CHI_1"] = df_crimes_s.apply(multiplychi_1, axis=1)
        df_crimes_s["CHI_2"] = df_crimes_s.apply(multiplychi_2, axis=1)
        df_crimes_s["CHI_3"] = df_crimes_s.apply(multiplychi_3, axis=1)
        df_crimes_s["CHI_4"] = df_crimes_s.apply(multiplychi_4, axis=1)
        df_crimes_s["CHI_5"] = df_crimes_s.apply(multiplychi_5, axis=1)
        df_crimes_s["CHI_6"] = df_crimes_s.apply(multiplychi_6, axis=1)
        column_names = ["SoortMisdrijf", "RegioS", "Perioden", "TotaalGeregistreerdeMisdrijven_1",
                        "GeregistreerdeMisdrijvenRelatief_2", "GeregistreerdeMisdrijvenPer1000Inw_3",
                        "TotaalOpgehelderdeMisdrijven_4", "OpgehelderdeMisdrijvenRelatief_5",
                        "RegistratiesVanVerdachten_6",
                        "CHI_1", "CHI_2", "CHI_3", "CHI_4", "CHI_5", "CHI_6"]
        df_chi = pd.DataFrame(columns=column_names)
        regios = df_crimes_s.RegioS.unique()
        for regio in regios:
            for years in yearlist:
                df_subset = df_crimes_s[df_crimes_s['RegioS'] == regio]
                df_subset = df_subset[df_subset['Perioden'] == years]
                df_sum = df_subset['CHI_1'].sum()
                df_sum_2 = df_subset['CHI_2'].sum()
                df_sum_3 = df_subset['CHI_3'].sum()
                df_sum_4 = df_subset['CHI_1'].sum()
                df_sum_5 = df_subset['CHI_2'].sum()
                df_sum_6 = df_subset['CHI_3'].sum()
                crime = {"SoortMisdrijf": 'CHI value', "RegioS": regio, 'Perioden': years,
                         "TotaalGeregistreerdeMisdrijven_1": df_sum, "GeregistreerdeMisdrijvenRelatief_2": df_sum_2,
                         "GeregistreerdeMisdrijvenPer1000Inw_3": df_sum_3, "TotaalOpgehelderdeMisdrijven_4": df_sum_4,
                         "OpgehelderdeMisdrijvenRelatief_5": df_sum_5, "RegistratiesVanVerdachten_6": df_sum_6
                         }
                df_chi = df_chi.append(crime, ignore_index=True)

        frames = [df_crimes_s, df_chi]
        df_crime = pd.concat(frames)
        for i in range(1, 6):
            df_crime.drop([str('CHI_' + str(i))], axis=1)
        df_crime = df_crime.fillna(0)
        df_crime.to_pickle("chidf.pkl")
    else:
        df_crime = pd.read_pickle("chidf.pkl")
    return df_crime


def selection(df_crimes_s, year_s, crime_subset_s, type_of_crimes_s):
    # only get the correct year
    df_crimes_s = df_crimes_s[df_crimes_s['Perioden'] == year_s]
    # select type of crime, regio and state of crimes (all, solved etc)
    df_crimes_s = df_crimes_s[['SoortMisdrijf', 'RegioS', crime_subset_s]]
    # only select the type of crimes that were chosen in beginning
    df_crimes_s = df_crimes_s[df_crimes_s['SoortMisdrijf'] == type_of_crimes_s]
    # fill empty data with 0
    df_crimes_s = df_crimes_s.fillna(0)
    # remove type of crimes from the dataframe as it is all the same
    df_crimes_s = df_crimes_s[['RegioS', crime_subset_s]]
    # set the index as the regio
    df_crimes_s = df_crimes_s.set_index('RegioS')
    # round the numbers to int (they were 3.0 for example)
    # df_crimes = df_crimes.round(0).astype(int)
    return df_crimes_s


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
        background_fill_color="white", title=str("Crimes per municipality. " + year + ", " + str(list(typelist.keys())[list(typelist.values()).index(type_of_crimes)]) + ", " + str(list(crime_subsetlist.keys())[list(crime_subsetlist.values()).index(crime_subset)])), tools=TOOLS,
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


def update_figure(reload_s, year_s, type_s, subset_s, palette_s):
    reload_a = True if (reload_s == 'Yes') else False
    # load the data, if reload is true, it will reload data from cbs
    df_s = importdata(reload_a)
    # add the crime harm index column
    df_s = add_chi(df_s, reload_a)
    # select the correct year and type
    df_s = selection(df_s, year_s, subset_s, type_s)
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
    global year, reload, type_of_crimes, crime_subset, palette
    if new in yearlist:
        year = new
    elif new in crime_subsetlist:
        crime_subset = crime_subsetlist[new]
    elif new in typelist:
        type_of_crimes = typelist[new]
    elif new in ["Yes", "No"]:
        reload = new
    elif new in colourlist:
        palette = colourlist[new]
    layout.children[1] = update_figure(reload, year, type_of_crimes, crime_subset, palette)


# set all the variables, should be replaced by sliders/buttons
crime_subset = 'TotaalGeregistreerdeMisdrijven_1'
year = '2017'
type_of_crimes = 'Misdrijven, totaal'
reload = False
unfindable = []
palette = colourlist['Red']

# load the data, if reload is true, it will reload data from cbs
df_crimes = importdata(reload)
df_crimes = add_chi(df_crimes, reload)
# select the correct amount of data
df_crimes = selection(df_crimes, year, crime_subset, type_of_crimes)

# open nl geojson data
with open(r'Gemeenten.geojson', 'r') as f:
    dutch_municipalities_dict = json.loads(f.read(), object_hook=OrderedDict)

# fix the municipalities in the dataframe to match the geojson file
df_crimes = fixmunic(df_crimes)
# merge geojson data with crimedata
dutch_municipalities_dict['features'] = [merge_crimes(unfindable, municipality, df_crimes, crime_subset) for
                                         municipality in
                                         dutch_municipalities_dict['features']]
# print all municipalities that can't be found in df
if len(unfindable) > 0:
    print("These municipalities can't be found:")
print(unfindable)
create_figure(dutch_municipalities_dict, palette)

year_sel = Select(title='Year', value='2017', options=yearlist)
year_sel.on_change('value', update)

crime_subset_sel = Select(title='Crime subset', value='TotaalGeregistreerdeMisdrijven_1',
                          options=list(crime_subsetlist.keys()))
crime_subset_sel.on_change('value', update)

type_of_crime_sel = Select(title='Type of crime', value='Misdrijven, totaal', options=list(typelist.keys()))
type_of_crime_sel.on_change('value', update)

reload_sel = Select(title='Reload: Warning, will reload data and will take a long time', value='No',
                    options=["Yes", "No"])
reload_sel.on_change('value', update)

colour_sel = Select(title='Colour', value='Red', options=list(colourlist.keys()))
colour_sel.on_change('value', update)

controls = column(year_sel, crime_subset_sel, reload_sel, type_of_crime_sel, colour_sel, width=200)
layout = row(controls, create_figure(dutch_municipalities_dict, palette))

curdoc().theme = 'dark_minimal'
curdoc().add_root(layout)
curdoc().title = "Crossfilter"
