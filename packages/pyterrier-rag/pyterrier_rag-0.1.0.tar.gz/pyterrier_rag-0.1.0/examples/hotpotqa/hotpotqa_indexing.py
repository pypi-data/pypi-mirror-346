import pyterrier as pt
import pyterrier_rag
index = "./hpq_index"
pt.IterDictIndexer(index, meta={'docno' : '20', 'text' : '1000', 'title' : '100'}).index(pt.get_dataset('rag:hotpotqa_wiki').get_corpus_iter(), fields=('title', 'text'))
hpq_index = pt.IndexFactory.of(index)
print(len(hpq_index))
print(hpq_index.getCollectionStatistics().toString())