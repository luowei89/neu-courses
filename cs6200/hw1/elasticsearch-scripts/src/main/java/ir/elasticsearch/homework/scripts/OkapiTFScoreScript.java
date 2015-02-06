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
 * Created by Wei Luo on 2/5/15.
 */
public class OkapiTFScoreScript extends AbstractSearchScript {

    String field = null;
    ArrayList<String> terms = null;
    Float avgDocLength = null;

    final static public String SCRIPT_NAME = "okapitf_score_script";

    public OkapiTFScoreScript(Map<String, Object> params) {
        params.entrySet();
        terms = (ArrayList<String>) params.get("terms");
        field = (String) params.get("field");
        avgDocLength = (Float) params.get("avgDocLength");
        if (field == null || terms == null || avgDocLength == null) {
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
                int tf = indexFieldTerm.tf();
                if (tf != 0) {
                    score += tf/(tf+0.5+1.5*(lenD/avgDocLength));
                }
            }
            return score;
        } catch (IOException ex) {
            throw new ScriptException("Could not compute okapi-tf: ", ex);
        }
    }

    public static class OkapiTFScoreScriptFactory implements NativeScriptFactory {

        @Override
        public ExecutableScript newScript(Map<String, Object> params) {
            return new OkapiTFScoreScript(params);
        }
    }
}
