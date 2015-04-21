package ir.homework.elasticsearch;

import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.client.Client;
import org.elasticsearch.index.query.QueryBuilder;
import org.elasticsearch.node.Node;
import org.elasticsearch.node.NodeBuilder;
import org.elasticsearch.search.SearchHit;

import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import static org.elasticsearch.index.query.QueryBuilders.termsQuery;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 4/8/15.
 */
public class Elasticsearch {

    public static void executeQuery(String queryID, String query,Client client){
        Map<String,Object> params = new HashMap<String, Object>();
        String[] terms = query.split(" ");
        params.put("field","text");
        params.put("terms",terms);
        QueryBuilder qb = termsQuery("text", terms);
        SearchResponse response = client.prepareSearch("crawler_data")
                .setQuery(qb).setSize(100)
                .execute()
                .actionGet();

        int index = 1;
        for(SearchHit hit : response.getHits().getHits()){
            String out = queryID;
            out += " Q0";
            out += " " + hit.getSource().get("id").toString();
            out += " " + index++;
            out += " " + hit.getScore();
            out += " Exp";
            System.out.println(out);
        }
    }

    public static void main(String[] args){
        HashMap<String,String> queries = new HashMap<String, String>();
        queries.put("151001","pentagon crash");
        queries.put("151002","wtc twin towers");
        queries.put("151003","london bombing");


        Node node = NodeBuilder.nodeBuilder().node();
        Client client = node.client();

        Iterator<String> keySetIterator = queries.keySet().iterator();
        while(keySetIterator.hasNext()){
            String key = keySetIterator.next();
            executeQuery(key,queries.get(key),client);
        }
        node.close();
    }
}

