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
import colorcet as cc
from bokeh.palettes import Turbo256, Reds256, Greens256, Inferno256, Magma256, Plasma256, Greys256
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

yearlist = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021"]
crime_subsetlist = ["TotaalGeregistreerdeMisdrijven_1", "GeregistreerdeMisdrijvenRelatief_2",
                    "GeregistreerdeMisdrijvenPer1000Inw_3", "TotaalOpgehelderdeMisdrijven_4",
                    "OpgehelderdeMisdrijvenRelatief_5", "RegistratiesVanVerdachten_6"]
typelist = ['Misdrijven, totaal', 'CHI value', '1 Vermogensmisdrijven', '11 Diefstal/verduistering en inbraak',
            '111 Diefstal en inbraak met geweld', '112 Diefstal en inbraak zonder geweld', '12 Bedrog',
            '121 Oplichting',
            '122 Flessentrekkerij', '123 Bedrog (overig)', '13 Valsheidsmisdrijven', '131 Muntmisdrijf',
            '132 Valsheid in zegels en merken', '133 Valsheid in geschriften', '14 Heling',
            '15 Afpersing en afdreiging',
            '16 Bankbreuk', '17 Witwassen', '18 Vermogensmisdrijf (overig)', '2 Vernielingen,misdropenborde/gezag',
            '21 Vernieling en beschadiging', '211 Vernieling aan auto', '212 Vernieling aan openbaar gebouw',
            '213 Vernieling middel openb vervoer', '215 Vernieling, beschadiging (overig)', '22 Openbare orde misdrijf',
            '221 Openlijke geweldpleging', '2211 Openlijk geweld tegen persoon', '2212 Openlijke geweld tegen goed',
            '222 Huisvredebreuk', '223 Lokaalvredebreuk', '224 Computervredebreuk', '225 Discriminatie',
            '226 Openbare orde misdrijf (overig)', '23 Brandstichting / ontploffing', '24 Openbaar gezag misdrijf',
            '241 Niet opvolgen van ambtelijk bevel', '242 Wederspannigheid', '243 Valse aangifte',
            '245 Verblijf ongewenste vreemdeling', '246 Openbaar gezag misdrijf (overig)',
            '3 Gewelds- en seksuele misdrijven', '31 Mishandeling', '32 Bedreiging en stalking', '321 Bedreiging',
            '322 Stalking', '33 Seksueel misdrijf', '331 Aanranding', '332 Verkrachting',
            '333 Schennis der eerbaarheid',
            '334 Ontucht met minderjarige', '335 Pornografie', '336 Ontucht met misbruik van gezag',
            '337 Seksueel misdrijf (overig)', '34 Levensmisdrijf', '35 Vrijheidsbeneming/gijzeling',
            '36 Mensenhandel en 244 mensensmokkel',
            '37 Geweldsmisdrijf (overig)', '4 Misdrijven WvSr (overig)', '5 Verkeersmisdrijven',
            '51 Verlaten plaats ongeval', '52 Rijden onder invloed', '53 Rijden tijdens ontzegging besturen',
            '54 Rijden tijdens rijverbod', '55 Voeren vals kenteken', '56 Joyriding',
            '57 Weigeren blaastest/bloedonderzoek ed', '58 Verkeersmisdrijf (overig)', '6 Drugsmisdrijven',
            '61 Harddrugs', '62 Softdrugs', '6.3 Drugsmisdrijf (overig)', '7 Vuurwapenmisdrijven',
            '9 Misdrijven overige wetten', '91 Militaire misdrijven', '92 Misdrijven (overig)']

chidict = {
    'Misdrijven, totaal': 0, '1 Vermogensmisdrijven': 0, '11 Diefstal/verduistering en inbraak': 0,
    '111 Diefstal en inbraak met geweld': 3243, '112 Diefstal en inbraak zonder geweld': 856, '12 Bedrog': 0,
    '121 Oplichting': 1236, '122 Flessentrekkerij': 0, '123 Bedrog (overig)': 871, '13 Valsheidsmisdrijven': 0,
    '131 Muntmisdrijf': 1769, '132 Valsheid in zegels en merken': 1221, '133 Valsheid in geschriften': 856,
    '14 Heling': 1601, '15 Afpersing en afdreiging': 2148, '16 Bankbreuk': 1601, '17 Witwassen': 1236,
    '18 Vermogensmisdrijf (overig)': 0, '2 Vernielingen,misdropenborde/gezag': 0, '21 Vernieling en beschadiging': 0,
    '211 Vernieling aan auto': 491, '212 Vernieling aan openbaar gebouw': 856,
    '213 Vernieling middel openb vervoer': 674, '215 Vernieling, beschadiging (overig)': 755,
    '22 Openbare orde misdrijf': 0, '221 Openlijke geweldpleging': 0, '2211 Openlijk geweld tegen persoon': 2696,
    '2212 Openlijke geweld tegen goed': 1221, '222 Huisvredebreuk': 233, '223 Lokaalvredebreuk': 71,
    '224 Computervredebreuk': 309, '225 Discriminatie': 390, '226 Openbare orde misdrijf (overig)': 938,
    '23 Brandstichting / ontploffing': 5601, '24 Openbaar gezag misdrijf': 0,
    '241 Niet opvolgen van ambtelijk bevel': 71, '242 Wederspannigheid': 1146, '243 Valse aangifte': 233,
    '245 Verblijf ongewenste vreemdeling': 142, '246 Openbaar gezag misdrijf (overig)': 1120,
    '3 Gewelds- en seksuele misdrijven': 0, '31 Mishandeling': 1221, '32 Bedreiging en stalking': 0,
    '321 Bedreiging': 187, '322 Stalking': 674, '33 Seksueel misdrijf': 0, '331 Aanranding': 1966,
    '332 Verkrachting': 2696, '333 Schennis der eerbaarheid': 71, '334 Ontucht met minderjarige': 856,
    '335 Pornografie': 81, '336 Ontucht met misbruik van gezag': 1221, '337 Seksueel misdrijf (overig)': 1586,
    '34 Levensmisdrijf': 5981, '35 Vrijheidsbeneming/gijzeling': 5981, '36 Mensenhandel en 244 mensensmokkel': 3243,
    '37 Geweldsmisdrijf (overig)': 2864, '4 Misdrijven WvSr (overig)': 1120, '5 Verkeersmisdrijven': 0,
    '51 Verlaten plaats ongeval': 309, '52 Rijden onder invloed': 309, '53 Rijden tijdens ontzegging besturen': 309,
    '54 Rijden tijdens rijverbod': 96, '55 Voeren vals kenteken': 142, '56 Joyriding': 142,
    '57 Weigeren blaastest/bloedonderzoek ed': 96, '58 Verkeersmisdrijf (overig)': 1146, '6 Drugsmisdrijven': 0,
    '61 Harddrugs': 2316, '62 Softdrugs': 755, '6.3 Drugsmisdrijf (overig)': 755, '7 Vuurwapenmisdrijven': 1586,
    '9 Misdrijven overige wetten': 0, '91 Militaire misdrijven': 0, '92 Misdrijven (overig)': 0
}

colourlist = {
    'Blue': cc.blues, 'Red': Reds256[::-1], 'Green': Greens256[::-1], 'Grey': Greys256[::-1], 'Rainbow': cc.CET_R1,
    'Turbo': Turbo256,
    'Inferno': Inferno256[::-1], 'Magma': Magma256[::-1], 'Plasma': Plasma256[::-1], 'Fridge': cc.CET_L19
}


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
        for i in range (1, 6):
            df_crime.drop([str('CHI_'+str(i))], axis=1)
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
        background_fill_color="white", title=str("Crimes per municipality. "+year+ ", "+
                                                 type_of_crimes+ ", "+crime_subset), tools=TOOLS,
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
        crime_subset = new
    elif new in typelist:
        type_of_crimes = new
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

crime_subset_sel = Select(title='Crime subset', value='TotaalGeregistreerdeMisdrijven_1', options=crime_subsetlist)
crime_subset_sel.on_change('value', update)

type_of_crime_sel = Select(title='Type of crime', value='Misdrijven, totaal', options=typelist)
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
