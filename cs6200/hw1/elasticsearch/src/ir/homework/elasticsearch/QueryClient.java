package ir.homework.elasticsearch;

import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.client.Client;
import org.elasticsearch.index.query.QueryBuilder;
import org.elasticsearch.index.query.functionscore.FunctionScoreQueryBuilder;
import org.elasticsearch.index.query.functionscore.ScoreFunctionBuilder;
import org.elasticsearch.index.query.functionscore.script.ScriptScoreFunctionBuilder;
import org.elasticsearch.node.Node;
import org.elasticsearch.node.NodeBuilder;
import org.elasticsearch.search.SearchHit;
import org.apache.lucene.analysis.Analyzer;

import java.io.*;
import java.util.*;

import static org.elasticsearch.index.query.QueryBuilders.termsQuery;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 1/23/15.
 */
public class QueryClient {

    public static final String OKAPI_TF = "okapitf_score_script";
    public static final String TF_IDF = "tf_idf_score_script";
    public static final String OKAPI_BM25 = "okapi_bm25_score_script";
    public static final String LM_LAPLACE = "lm_laplace_script";
    public static final String LM_JM = "lm_jm_script";

    public static HashMap<String,String[]> parseQueries(File file){
        HashMap<String,String[]> queries= new HashMap<String,String[]>();
        try {
            Analyzer a  = new EnglishAnalyzer();
            QueryParser parser = new QueryParser("",a);
            FileInputStream fis = new FileInputStream(file);
            BufferedReader br = new BufferedReader(new InputStreamReader(fis));
            String line = br.readLine();
            while (line != null) {
                line = line.trim();
                if(! line.equals("")) {

                    String[] words = line.split(" ");
                    List<String> terms = new ArrayList<String>();
                    for (int i = 7; i < words.length; i++) {
                        if (!words[i].equals("")) {
                            String term = parser.parse(words[i]).toString();
                            if(!term.equals("")) {
                                terms.add(term);
                            }
                        }
                    }
                    String[] termsArray = new String[terms.size()];
                    queries.put(parser.parse(words[0]).toString(), terms.toArray(termsArray));
                }
                line = br.readLine();
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return queries;
    }

    public static void executeQuery(String queryID, String[] terms,Client client){
        Map<String,Object> params = new HashMap<String, Object>();
        params.put("field","text");
        params.put("terms",terms);
        QueryBuilder qb = termsQuery("text", terms);
        ScoreFunctionBuilder sfb = new ScriptScoreFunctionBuilder()
                .script(OKAPI_TF).lang("native").params(params);
        FunctionScoreQueryBuilder fsqb = new FunctionScoreQueryBuilder(qb)
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

    public static void main(String[] args){
        File queryFile = new File("../../dataset/AP_DATA/query_desc.51-100.short.txt");
        HashMap<String,String[]> queries = parseQueries(queryFile);

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
