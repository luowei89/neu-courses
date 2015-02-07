package ir.homework.elasticsearch;

import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.action.search.SearchType;
import org.elasticsearch.client.Client;
import org.elasticsearch.common.unit.TimeValue;
import org.elasticsearch.index.query.functionscore.FunctionScoreQueryBuilder;
import org.elasticsearch.index.query.functionscore.ScoreFunctionBuilder;
import org.elasticsearch.index.query.functionscore.script.ScriptScoreFunctionBuilder;
import org.elasticsearch.node.Node;
import org.elasticsearch.node.NodeBuilder;
import org.elasticsearch.search.SearchHit;

import java.io.*;
import java.util.*;

import static org.elasticsearch.index.query.QueryBuilders.queryString;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 1/23/15.
 */
public class QueryClient {

    public static float avgDocLength = -1;
    public static int docNum = -1;

    public static final String OKAPI_TF = "okapitf_score_script";
    public static final String TF_IDF = "tf_idf_score_script";
    public static final String OKAPI_BM25 = "okapi_bm25_score_script";
    public static final String LM_LAPLACE = "lm_laplace_script";
    public static final String LM_JM = "lm_jm_script";


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

    public static void executeQuery(String queryID, String[] terms,Client client){
        Map<String,Object> params = new HashMap<String, Object>();
        params.put("field","text");
        params.put("terms",terms);
        ScoreFunctionBuilder sfb = new ScriptScoreFunctionBuilder()
                .script(LM_JM).lang("native").params(params);
        FunctionScoreQueryBuilder fsqb = new FunctionScoreQueryBuilder()
                .add(sfb)
                .boostMode("replace");
        SearchResponse response = client.prepareSearch("ap_dataset")
                .setQuery(fsqb).setSize(100)
                .execute()
                .actionGet();

        int index = 1;
        for(SearchHit hit : response.getHits().getHits()){
            String out = queryID;
            out += " Q0";
            out += " " + hit.getSource().get("docno").toString();
            out += " " + index++;
            out += " " + hit.getScore();
            out += " Exp";
            System.out.println(out);
        }
    }

    public static void initClient(Client client){
        int docs = 0;
        int totalLength = 0;
        SearchResponse scrollResp = client.prepareSearch("ap_dataset")
                .setSearchType(SearchType.SCAN)
                .setScroll(new TimeValue(60000))
                .setQuery(queryString("*:*"))
                .setSize(10000).execute().actionGet();
        //Scroll until no hits are returned
        while (true) {
            for (SearchHit hit : scrollResp.getHits().getHits()) {
                docs += 1;
                totalLength += hit.getSource().get("text").toString().trim().split(" ").length;
            }
            scrollResp = client.prepareSearchScroll(scrollResp.getScrollId())
                    .setScroll(new TimeValue(600000)).execute().actionGet();
            //Break condition: No hits are returned
            if (scrollResp.getHits().getHits().length == 0) {
                break;
            }
        }
        docNum = docs;
        avgDocLength = totalLength / docs;
    }

    public static void main(String[] args){
        File queryFile = new File("../../dataset/AP_DATA/query_desc.51-100.short.txt");
        HashMap<String,String[]> queries = parseQueries(queryFile);

        Node node = NodeBuilder.nodeBuilder().node();
        Client client = node.client();

        //initClient(client);

        Iterator<String> keySetIterator = queries.keySet().iterator();
        while(keySetIterator.hasNext()){
            String key = keySetIterator.next();
            executeQuery(key,queries.get(key),client);
        }
        node.close();
    }
}
