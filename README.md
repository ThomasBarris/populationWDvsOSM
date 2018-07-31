# Population in OSM and Wikidata

### Summary
The Python script compares the population in OSM (place nodes and boundary relations) with Wikidata. Before you edit/add data in either database, please be sure you have some idea of the hierarchical model of the region and how it is represented in OSM and Wikidata. 

### Requires
Python 3.x with the following libraries:    
[SPARQLWrapper](https://rdflib.github.io/sparqlwrapper/)    
[overpass](https://github.com/mvexel/overpass-api-python-wrapper)  >= 0.6.0

### Installation & first steps
1. `git clone https://github.com/ThomasBarris/populationWDvsOSM.git` 
2. `cd  populationWDvsOSM`.
2. `pip install SPARQLWrapper`
3. `pip install overpass`
4. change location and name of the html output file in line 10 in WdOSMpop.py if necessary
5. change to bounding box in line 13 WdOSMpop.py. A tool that helps you to find the bbox can be found [here](http://lxbarth.com/bbox/#0,0,0,0,2,17.999999999999986,0)
6. `python3 WdOSMpop.py` 

### Output

##### Html Output
A file with the example output is [>>> here <<<](https://htmlpreview.github.com/?https://github.com/ThomasBarris/populationWDvsOSM/blob/master/example.html)

##### Terminal output
###### Place Node
```
> name       :  Göppingen
> type       :  node
> id         :  240084735
> wikidata   :  Q4072
> population :  55846
> place      :  town
> boundary   :  
> WD Label   :  Göppingen
> WD Pop     :  55846
```

###### Boundary Relation
```
> name       :  Ottenbach
> type       :  relation
> id         :  2826029
> wikidata   :  Q80639
> population :  
> place      :  
> boundary   :  administrative
> WD Label   :  Ottenbach
> WD Pop     :  2442
```
