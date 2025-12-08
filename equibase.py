"""
Tools for interacting with the equibase dataset
"""

import xmlschema
import os

xs = xmlschema.XMLSchema("./equibase/tchSchema.xsd")

def deserialize() -> tuple[list,int]:
    """
    Turn the results into a big list of charts

    :return: list of desesrialized file contents and number of errors
    :rtype: tuple[list, int]
    """
    result_dir = "./equibase/2023 Result Charts" 
    files = os.listdir(result_dir)

    fs = []
    errors = 0
    for f in files:
        try:
            d = xs.to_dict(result_dir+"/"+f)
            fs.append(d)
        except xmlschema.validators.exceptions.XMLSchemaDecodeError:
            errors +=1
            continue
    
    return fs, errors

class PastPerformance():
    def __init__(self, raw: dict):
        self.track = raw['TRACK']['CODE'].upper()
        self.date = raw['RACE_DATE']
        self.race_num = raw['RACE_NUMBER']

    def __repr__(self):
        return f"{self.track}_{self.date}_{self.race_num}"
    
    def __eq__(self,other):
        return str(self) == str(other)
    
    def __hash__(self):
        # this lets us use the object like a string as a dict key
        return hash(str(self))

class Entry():
    def __init__(self,raw: dict):
        try:
            self.last_pp = PastPerformance(raw['LAST_PP'])
        except:
            self.last_pp = None
        self.horse = raw['AXCISKEY']
        self.odds = raw['DOLLAR_ODDS']
        self.place = raw['OFFICIAL_FIN']

    def __repr__(self):
        return self.horse
    
    def __lt__(self,other):
        return self.place<other.place

def handle_chart(raw: dict):
    date = raw['@RACE_DATE']
    track = raw['TRACK']['CODE'].upper()

    races = {}
    for r in raw['RACE']:
        ref = f"{track}_{date}_{r['@NUMBER']}"
        races[ref] = []
        for e in r['ENTRY']:
            races[ref].append(Entry(e))
        races[ref].sort()
        
    return races

def handle_all_charts(ds: list):
    all_races = {}
    for c in ds:
        all_races = all_races | handle_chart(c)

    return all_races