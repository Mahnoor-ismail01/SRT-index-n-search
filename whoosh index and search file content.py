from typing import Dict, List, Sequence

from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import MultifieldParser
from whoosh.filedb.filestore import RamStorage
from whoosh.analysis import StemmingAnalyzer

import json




class SearchEngine:

    def __init__(self, schema):
        self.schema = schema
        schema.add('raw', TEXT(stored=True))
        self.ix = RamStorage().create_index(self.schema)

    def index_documents(self, docs: Sequence):
        writer = self.ix.writer()
        for doc in docs:
            d = {k: v for k,v in doc.items() if k in self.schema.stored_names()}
            d['raw'] = json.dumps(doc) # raw version of all of doc
            
            writer.add_document(**d)
        writer.commit(optimize=True)

    def get_index_size(self) -> int:
        return self.ix.doc_count_all()

    def query(self, q: str, fields: Sequence, highlight: bool=True) -> List[Dict]:
        search_results = []
        with self.ix.searcher() as searcher:
            results = searcher.search(MultifieldParser(fields, schema=self.schema).parse(q))
            for r in results:
                d = json.loads(r['raw'])
                if highlight:
                    for f in fields:
                        if r[f] and isinstance(r[f], str):
                            d[f] = r.highlights(f) or r[f]

                search_results.append(d)

        return search_results

if __name__ == '__main__':
    l = []
    f = open("a7.srt","r")
    for x in f:
        p=x.replace("\n\n","\n")
        l.append(p)
    aa=(len(l)//4)
    print(aa)
    f = open(r"a7.srt")

    p = f.read().replace("\n\n","\n")
    print(p)



    test_str = p

    
    delim = "\n"

    
    dicts = test_str.split(', ')

    res = dict()
    ab=aa*3
    dlist=[]
    print(dlist)


    for sub in dicts:
        
        
        
        

        for i in range(0,ab,3): 
            doc={}
        
            
           
            res[sub.split(delim)[i+1]] = sub.split(delim)[i+2]
            doc["time_stamp"]= sub.split(delim)[i+1]
            doc["content"]=sub.split(delim)[i+2]
            print(doc,"p")
            dlist.append(doc)
       


            






   

    schema = Schema(
       
        time_stamp=TEXT(stored=True),
        content=TEXT(stored=True, analyzer=StemmingAnalyzer()),
       
    )

    engine = SearchEngine(schema)
    engine.index_documents(dlist)

    print(f"indexed {engine.get_index_size()} documents")

    fields_to_search = ["content", "content"]

    for q in ["vivian"]:
        print(f"Query:: {q}")
        print("\t", engine.query(q, fields_to_search, highlight=True))
        print("-"*70)
