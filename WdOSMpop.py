#!/usr/bin/env python3

# lib to query for OSM data
import overpass

# lib to query for wikidata
from SPARQLWrapper import SPARQLWrapper, JSON

#define a bbox for the generation of the report
bbox = '48.6531,9.6343,48.7263,9.7638'
#  Tobias Wendorff Talk-DE about bboxes for german federal states
# 1. swap 3rd with 1st value and set commas between
#
# Baden-Wuerttemberg: 49.7913749328 7.5113934084 47.5338000528 10.4918239143
# Bayern: 50.5644529365 8.9771580802 47.2703623267 13.8350427083
# Berlin: 52.6697240587 13.0882097323 52.3418234221 13.7606105539
# Brandenburg: 53.5579500214 11.2681664447 51.3606627053 14.7647105012
# Bremen: 53.6061664164 8.4813576818 53.0103701114 8.9830477728
# Hamburg: 53.9644376366 8.4213643278 53.3949251389 10.3242585128
# Hessen: 51.6540496066 7.7731704009 49.3948229196 10.2340156149
# Mecklenburg-Vorpommern: 54.6849886830 10.5932460856 53.1158637944 14.4122799503
# Niedersachsen: 53.8941514415 6.6545841239 51.2954150799 11.59769814
# Nordrhein-Westfalen: 52.5310351488 5.8659988131 50.3226989435 9.4476584861
# Rheinland-Pfalz: 50.9404435711 6.1173598760 48.9662745077 8.5084754437
# Saarland: 49.6393467247 6.3584695643 49.1130992988 7.4034901078
# Sachsen: 51.6831408995 11.8723081683 50.1715419914 15.0377433357
# Sachsen-Anhalt: 53.0421316033 10.5614755400 50.9379979829 13.1865600846
# Schleswig-Holstein: 55.0573747014 7.8685145620 53.3590675115 11.3132037822
# Thueringen: 51.6490678544 9.8778443239 50.2042330625 12.6531964048



# the file where you can find the results
html_file = "index.html"

# if you query larger areas you must be patient and might experience a timeout if you use the default value.
api = overpass.API(timeout=600)


endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
sparql = SPARQLWrapper(endpoint)

# 3 functions to write the html stuff
def html_header(wikidata_file):
    with open(wikidata_file, 'w') as preview_html:
        print('<!DOCTYPE html>', file=preview_html)
        print('<html lang="en">', file=preview_html)
        print('<meta charset="utf-8"/>', file=preview_html)
        print('    <body><table border="1">', file=preview_html)
        print('    <thead>', file=preview_html)
        print('        <tr>', file=preview_html)
        print('            <th>Name</th>', file=preview_html)
        print('            <th>WikidataName</th>', file=preview_html)
        print('            <th>WikidataID</th>', file=preview_html)
        print('            <th>Place</th>', file=preview_html)
        print('            <th>Boundary</th>', file=preview_html)
        print('            <th>OSM Link</th>', file=preview_html)
        print('            <th>OSM Pop</th>', file=preview_html)
        print('            <th>Wikidata Pop</th>', file=preview_html)
        print('            <th>Pop Diff</th>', file=preview_html)
        print('        </tr>', file=preview_html)
        print('    <thead>', file=preview_html)

def html_footer(wikidata_file):
    with open(wikidata_file, 'a') as preview_html:
        print('    </tbody>', file=preview_html)
        print('</table>', file=preview_html)

def html_line(wikidata_file, data_line):
    with open(wikidata_file, 'a') as preview_html:
        print('            <tr>', file=preview_html)

        print('                <td>', end='', file=preview_html)
        print(data_line[0],    end='', file=preview_html)
        print('                </td>', file=preview_html)

        print('                <td>', end='', file=preview_html)
        print(data_line[1],    end='', file=preview_html)
        print('                </td>', file=preview_html)

        print('                <td>', end='', file=preview_html)
        print(data_line[2],    end='', file=preview_html)
        print('                </td>', file=preview_html)

        print('                <td>', end='', file=preview_html)
        print(data_line[3],    end='', file=preview_html)
        print('                </td>', file=preview_html)

        print('                <td>', end='', file=preview_html)
        print(data_line[4],    end='', file=preview_html)
        print('                </td>', file=preview_html)

        print('                <td>', end='', file=preview_html)
        print(data_line[5],    end='', file=preview_html)
        print('                </td>', file=preview_html)

        print('                <td>', end='', file=preview_html)
        print(data_line[6],    end='', file=preview_html)
        print('                </td>', file=preview_html)

        print('                <td>', end='', file=preview_html)
        print(data_line[7],    end='', file=preview_html)
        print('                </td>', file=preview_html)

        print('                <td>', end='', file=preview_html)
        print(data_line[8],    end='', file=preview_html)
        print('                </td>', file=preview_html)

        print('            </tr>', file=preview_html)


# fucntion to query Wikidata. takes a wikidata ID and returns the population and the label.
# change the language code if you want to use another language in FILTER(LANGMATCHES(LANG(?label), "DE"))
def query_wd(wd_id):
    wd_population = ''
    label = ''
    sparql.setQuery("""
        SELECT * WHERE {
            wd:""" + wd_id + """ rdfs:label ?label.
            FILTER(LANGMATCHES(LANG(?label), "DE"))
            OPTIONAL { wd:""" + wd_id + """ wdt:P1082 ?Einwohnerzahl. }
        }
        LIMIT 1""")

    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        label = result['label']['value']
        try:
            wd_population = result['Einwohnerzahl']['value']
        except:
            wd_population = ''
    return label, wd_population


response_list = []

# building overpass query
query_string = ''
query_string = query_string + '(node[place](' + bbox + ');'
query_string = query_string + 'relation[boundary](' + bbox + ');'
query_string = query_string + ');'

# and get the response from overpass
overpass_response = api.Get(
        query_string,
        responseformat='csv(::"id",::"user",::"type","wikidata","name",population, place, boundary)',
        verbosity='meta')

# write the output header
html_header(html_file)

# write the data to the html file
for response_item in overpass_response[1:]:
    line_item = ['na', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na']
    if (response_item[7]=='administrative' or response_item[6] in ['city', 'village','town']):
        print("name       : ", response_item[4])
        line_item[0] = response_item[4]
        print("type       : ", response_item[2])
        print("id         : ", response_item[0])
        if (response_item[2] == "node"):
            line_item[5] = """<a href="https://openstreetmap.org/browse/node/""" + response_item[0] + """">""" + response_item[0] + """</a>"""
        if (response_item[2] == "relation"):
            line_item[5] = """<a href="https://openstreetmap.org/browse/relation/""" + response_item[0] + """">""" + response_item[0] + """</a>"""
        print("wikidata   : ", response_item[3])
        print("population : ", response_item[5])
        line_item[6] = response_item[5]
        print("place      : ", response_item[6])
        line_item[3] = response_item[6]
        print("boundary   : ", response_item[7])
        line_item[4] = response_item[7]
        wd_label, wd_pop = query_wd(response_item[3])
        line_item[1] = wd_label
        line_item[2] = """<a href="https://www.wikidata.org/wiki/""" + response_item[3] + """">""" + response_item[3] + """</a>"""
        print("WD Label   : ", wd_label)

        print("WD Pop     : ", wd_pop)
        line_item[7] = wd_pop

        if ( response_item[5].isnumeric()  and wd_pop.isnumeric() ):
            line_item[8] = int(response_item[5]) - int(wd_pop)
        elif response_item[5].isnumeric() :
            line_item[8] = response_item[5]
        elif wd_pop.isnumeric() :
            line_item[8] = wd_pop

        html_line(html_file, line_item)
        print("##############################")

# close the html file
html_footer(html_file)
