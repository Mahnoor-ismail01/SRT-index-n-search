
import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import sys
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
 
def createSearchableData(root):   
    #is m titlte m file aaegi hamari 
 
   
    schema = Schema(title=TEXT(stored=True),path=ID(stored=True),\
              content=TEXT,textdata=TEXT(stored=True))
    if not os.path.exists("indexdir1"):
        os.mkdir("indexdir1")
 
  
    ix = create_in("indexdir1",schema)
    writer = ix.writer()
 
    filepaths = [os.path.join(root,i) for i in os.listdir(root)]
    for path in filepaths:
        fp = open(path,'r')
        print(path)
        text = fp.read()
       # print(text)
        writer.add_document(title=path.split("/")[4], path=path,\
          content=text,textdata=text)
        
        fp.close()
    writer.commit()
 
    ix = open_dir("indexdir1")

  
    query_str = sys.argv[1]
    
    topN = int(sys.argv[2])
    print(topN)
    
    with ix.searcher(weighting=scoring.Frequency) as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        
        results = searcher.search(query,limit=topN)
        print(results,"p")
        for i in range(topN):
            print(results[i]['title'], str(results[i].score), results[i]['textdata'])

root = "/home/mahnoor/re"
createSearchableData(root)