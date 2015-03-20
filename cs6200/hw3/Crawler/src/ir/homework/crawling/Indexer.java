package ir.homework.crawling;

import org.elasticsearch.client.Client;
import org.elasticsearch.common.xcontent.XContentBuilder;
import org.elasticsearch.node.Node;
import org.elasticsearch.node.NodeBuilder;
import org.elasticsearch.script.ScriptService;

import java.util.HashMap;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 3/19/15.
 */
public class Indexer {
    private static int id;
    private Node node;
    private Client client;
    private HashMap<String,Integer> docIdMap;

    public Indexer(){
        id = 1;
        node = NodeBuilder.nodeBuilder().node();
        client = node.client();
        docIdMap = new HashMap<String, Integer>();
    }

    public void close(){
        node.close();
    }

    public void buildIndex(ESElement ese){
        XContentBuilder builder = ese.getBuilder();
        client.prepareIndex("crawler_data", "document", ""+id)
                .setSource(builder)
                .execute()
                .actionGet();
        docIdMap.put(ese.getId(),id);
        id++;
    }

    public void updateInlinks(String url, String inlink) {
        client.prepareUpdate("crawler_data","document",""+docIdMap.get(url))
                .addScriptParam("new_inlink", inlink)
                .setScript("ctx._source.inlinks += new_inlink", ScriptService.ScriptType.INLINE)
                .execute()
                .actionGet();

    }
}
