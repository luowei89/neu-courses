package ir.homework.crawling;

import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.action.search.SearchType;
import org.elasticsearch.action.update.UpdateResponse;
import org.elasticsearch.client.Client;
import org.elasticsearch.common.unit.TimeValue;
import org.elasticsearch.common.xcontent.XContentBuilder;
import org.elasticsearch.index.engine.VersionConflictEngineException;
import org.elasticsearch.index.query.QueryBuilder;
import org.elasticsearch.index.query.functionscore.FunctionScoreQueryBuilder;
import org.elasticsearch.index.query.functionscore.ScoreFunctionBuilder;
import org.elasticsearch.node.Node;
import org.elasticsearch.node.NodeBuilder;
import org.elasticsearch.script.ScriptService;
import org.elasticsearch.search.SearchHit;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;
import java.util.concurrent.ConcurrentLinkedQueue;

import static org.elasticsearch.index.query.QueryBuilders.idsQuery;
import static org.elasticsearch.index.query.QueryBuilders.matchAllQuery;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 3/25/15.
 */
public class IndexMerger {

    private Node node;
    private Client client;

    private static final String FROM_INDEX_NAME = "crawler_data_luo";
    private static final String TO_INDEX_NAME = "crawler_data";
    private static final String DOC_TYPE = "document";

    private boolean merging;
    private ConcurrentLinkedQueue<ESElement> docQueue;
    private MergerThread[] mergeThreads;

    public IndexMerger() {
        node = NodeBuilder.nodeBuilder().node();
        client = node.client();
        merging = true;
        docQueue = new ConcurrentLinkedQueue<ESElement>();
        mergeThreads = new MergerThread[5];
    }

    public void releaseNode(){
        node.close();
    }

    public void merge() {
        for(int i = 0; i < mergeThreads.length; i++){
            mergeThreads[i] = new MergerThread();
            mergeThreads[i].start();
        }
        loadDocuments();
        merging = false;
        try {
            for (int i = 0; i < mergeThreads.length; i++) {
                mergeThreads[i].join();
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private void loadDocuments() {
        QueryBuilder qb = matchAllQuery();
        SearchResponse scrollResp = client.prepareSearch(FROM_INDEX_NAME)
                .setSearchType(SearchType.SCAN)
                .setScroll(new TimeValue(60000))
                .setQuery(qb).execute().actionGet();
        while(true) {
            for (SearchHit hit : scrollResp.getHits().getHits()) {
                ESElement ese = new ESElement(hit);
                docQueue.add(ese);
            }
            scrollResp = client.prepareSearchScroll(scrollResp.getScrollId())
                    .setScroll(new TimeValue(600000)).execute().actionGet();
            //Break condition: No hits are returned
            if (scrollResp.getHits().getHits().length == 0) {
                break;
            }
        }
    }

    private class MergerThread extends Thread {
        @Override
        public void run() {
            ESElement ese = docQueue.poll();
            while (merging || ese != null) {
                if(ese != null) {
                    QueryBuilder qb = idsQuery().ids(ese.getId());
                    SearchResponse searchResp = client.prepareSearch(TO_INDEX_NAME)
                            .setQuery(qb).execute().actionGet();
                    if(searchResp.getHits().totalHits() > 0){
                        updateIndex(ese);
                    } else{
                        System.out.println("Indexing " + ese.getId());
                        IndexResponse indexResp = null;
                        while(indexResp == null || !indexResp.getId().equals(ese.getId())){
                            // ensure success index creation
                            indexResp = client.prepareIndex(TO_INDEX_NAME, DOC_TYPE, ese.getId())
                                    .setSource(ese.getBuilder()).execute().actionGet();
                        }
                    }
                }
                ese = docQueue.poll();
            }
        }

        private void updateIndex(ESElement ese) {
            System.out.println("Updating " + ese.getId());
            StringBuffer sb = new StringBuffer();
            if(ese.getInlinks().size() > 0) {
                sb.append("ctx._source.inlinks = ctx._source.inlinks.unique(false); ctx._source.inlinks");
                for(String in : ese.getInlinks()){
                    sb.append("<<"+"\""+in+"\"");
                }
                sb.append("; ");
            }
            if(ese.getOutlinks().size() > 0) {
                sb.append("ctx._source.outlinks = ctx._source.outlinks.unique(false); ctx._source.outlinks");
                for(String out : ese.getOutlinks()){
                    sb.append("<<"+"\""+out+"\"");
                }
                sb.append("; ");
            }
            String script = sb.toString();
            if(script != ""){
                try {
                    client.prepareUpdate(TO_INDEX_NAME, "document", ese.getId())
                            .setScript(script, ScriptService.ScriptType.INLINE)
                            .execute().actionGet();
                } catch (VersionConflictEngineException e) {
                    // update conflict save for retry
                    docQueue.add(ese);
                    e.printStackTrace();
                }
            }
        }
    }

    public static void main(String[] args){
        IndexMerger im = new IndexMerger();
        im.merge();
        im.releaseNode();
    }
}
