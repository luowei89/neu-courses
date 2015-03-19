package ir.homework.crawling;

import org.elasticsearch.client.Client;
import org.elasticsearch.common.xcontent.XContentBuilder;
import org.elasticsearch.node.Node;
import org.elasticsearch.node.NodeBuilder;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 3/19/15.
 */
public class Indexer {
    private static int id;
    private Node node;
    private Client client;

    public Indexer(){
        id = 1;
        node = NodeBuilder.nodeBuilder().node();
        client = node.client();
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
        id++;
    }
}
