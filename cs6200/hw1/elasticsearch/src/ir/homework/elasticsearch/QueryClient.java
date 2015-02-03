package ir.homework.elasticsearch;

import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.client.Client;
import org.elasticsearch.index.query.QueryBuilder;
import org.elasticsearch.node.Node;
import org.elasticsearch.node.NodeBuilder;
import org.elasticsearch.search.SearchHit;

import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;

import static org.elasticsearch.index.query.QueryBuilders.termsQuery;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 1/23/15.
 */
public class QueryClient {

    public static HashMap<String,String[]> parseQueries(File file){
        HashMap<String,String[]> queries= new HashMap<String,String[]>();
        try {
            FileInputStream fis = new FileInputStream(file);
            BufferedReader br = new BufferedReader(new InputStreamReader(fis));
            String line = br.readLine();
            while (line != null) {
                line = line.trim();
                if(! line.equals("")) {
                    String[] words = line.split(" |,|\\.");
                    List<String> terms = new ArrayList<String>();
                    for (int i = 1; i < words.length; i++) {
                        if (!words[i].equals("")) {
                            terms.add(words[i]);
                        }
                    }
                    String[] termsArray = new String[terms.size()];
                    queries.put(words[0], terms.toArray(termsArray));
                }
                line = br.readLine();
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return queries;
    }

    public static void executeQuery(String[] terms,Client client){
        QueryBuilder qb = termsQuery("text", terms);
        SearchResponse response = client.prepareSearch("ap_dataset")
                .setQuery(qb).setSize(100).setExplain(true)
                .execute()
                .actionGet();
        for (SearchHit hit : response.getHits().getHits()) {
            System.out.println(hit.getScore());
            //TODO: Handle the hit...
        }
    }

    public static void main(String[] args){
        File queryFile = new File("../../dataset/AP_DATA/query_desc.51-100.short.txt");
        HashMap<String,String[]> queries = parseQueries(queryFile);

        Node node = NodeBuilder.nodeBuilder().node();
        Client client = node.client();
        Iterator<String> keySetIterator = queries.keySet().iterator();

        while(keySetIterator.hasNext()){
            String key = keySetIterator.next();
            executeQuery(queries.get(key),client);
        }

        node.close();
    }
}
