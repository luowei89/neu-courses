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
public class UniLMJelinekMercerScoreScript extends AbstractSearchScript {

    String field = null;
    ArrayList<String> terms = null;

    public static final String SCRIPT_NAME = "lm_jm_script";
    private final double lambda = 0.6;

    public UniLMJelinekMercerScoreScript(Map<String, Object> params) {
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
            double score = 0.0;
            IndexField indexField = indexLookup().get(field);
            long V = indexField.sumttf();
            long lenD = ((ScriptDocValues.Longs) doc().get("word_count")).getValue();

            for (int i = 0; i < terms.size(); i++) {
                IndexFieldTerm indexFieldTerm = indexField.get(terms.get(i));
                int tf = indexFieldTerm.tf();
                long cf = indexFieldTerm.ttf();
                if (tf != 0) {
                    score += lambda*(tf/lenD)+(1-lambda)*(cf/V);
                }
            }
            return score;
        } catch (IOException ex) {
            throw new ScriptException("Could not compute score: ", ex);
        }
    }

    public static class UniLMJelinekMercerScoreScriptFactory implements NativeScriptFactory {

        @Override
        public ExecutableScript newScript(Map<String, Object> params) {
            return new UniLMJelinekMercerScoreScript(params);
        }
    }
}