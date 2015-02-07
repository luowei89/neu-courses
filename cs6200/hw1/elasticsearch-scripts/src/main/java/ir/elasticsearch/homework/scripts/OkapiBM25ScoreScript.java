package ir.elasticsearch.homework.scripts;

import org.elasticsearch.index.fielddata.ScriptDocValues;
import org.elasticsearch.script.AbstractSearchScript;
import org.elasticsearch.script.ExecutableScript;
import org.elasticsearch.script.NativeScriptFactory;
import org.elasticsearch.script.ScriptException;
import org.elasticsearch.search.lookup.IndexField;
import org.elasticsearch.search.lookup.IndexFieldTerm;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Map;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 2/6/15.
 */
public class OkapiBM25ScoreScript extends AbstractSearchScript {

    String field = null;
    ArrayList<String> terms = null;

    public static final String SCRIPT_NAME = "okapi_bm25_score_script";

    private static final double b = 0.75;
    private static final double k1 = 1.2;
    private static final int k2 = 100;
    private static final long avgDocLength = 442;

    public OkapiBM25ScoreScript(Map<String, Object> params) {
        params.entrySet();
        terms = (ArrayList<String>) params.get("terms");
        field = (String) params.get("field");
        if (field == null || terms == null) {
            throw new ScriptException("Cannot initialize " + SCRIPT_NAME + ": parameter missing!");
        }
    }

    @Override
    public Object run() {
        try {
            float score = 0;
            IndexField indexField = indexLookup().get(field);

            long lenD = ((ScriptDocValues.Longs) doc().get("word_count")).getValue();

            for (int i = 0; i < terms.size(); i++) {
                IndexFieldTerm indexFieldTerm = indexField.get(terms.get(i));
                int df = (int) indexFieldTerm.df();
                int tf = indexFieldTerm.tf();
                if (tf != 0) {
                    double log_term = Math.log(((float)indexField.docCount()+0.5)/((float)df+0.5));
                    double k1_term = (tf+k1*tf)/(tf+k1*((1-b)+b*(lenD/avgDocLength)));
                    double k2_term = (tf+k2*tf)/(tf+k2);
                    score += log_term*k1_term*k2_term;
                }
            }
            return score;
        } catch (IOException ex) {
            throw new ScriptException("Could not compute score: ", ex);
        }
    }

    public static class OkapiBM25ScoreScriptFactory implements NativeScriptFactory {

        @Override
        public ExecutableScript newScript(Map<String, Object> params) {
            return new OkapiBM25ScoreScript(params);
        }
    }
}
