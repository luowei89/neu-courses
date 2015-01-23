package ir.homework.elasticsearch;

import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.client.Client;
import org.elasticsearch.common.unit.TimeValue;
import org.elasticsearch.node.Node;
import org.elasticsearch.node.NodeBuilder;

import java.io.File;
import java.util.HashMap;
import java.util.Iterator;

import org.elasticsearch.index.query.FilterBuilders.*;
import static org.elasticsearch.index.query.QueryBuilders.*;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 1/23/15.
 */
public class QueryClient {

    public static HashMap<String,String> parseQueries(File file){
        HashMap<String,String> queries= new HashMap<String,String>();
        return queries;
    }

    public static void executeQuery(String query,Client client){
        //TODO: implement the query logic
    }

    public static void main(String[] args){
        File queryFile = new File("../../dataset/AP_DATA/query_desc.51-100.short.txt");
        HashMap<String,String> queries = parseQueries(queryFile);

        Node node = NodeBuilder.nodeBuilder().node();
        Client client = node.client();
        Iterator<String> keySetIterator = queries.keySet().iterator();

        while(keySetIterator.hasNext()){
            String key = keySetIterator.next();
            System.out.println("key: " + key + " value: " + queries.get(key));
        }

        node.close();
    }
}
