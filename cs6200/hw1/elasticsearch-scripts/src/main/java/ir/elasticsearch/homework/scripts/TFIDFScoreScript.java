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
public class TFIDFScoreScript extends AbstractSearchScript {

    String field = null;
    ArrayList<String> terms = null;

    public static final String SCRIPT_NAME = "tf_idf_score_script";
    private final double avgDocLength = 164.68;

    public TFIDFScoreScript(Map<String, Object> params) {
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

            int lenDoc = ((ScriptDocValues.Strings)doc().get(field)).getValues().size();

            for (int i = 0; i < terms.size(); i++) {
                IndexFieldTerm indexFieldTerm = indexField.get(terms.get(i));
                float df = (float) indexFieldTerm.df();
                int tf = indexFieldTerm.tf();
                if (tf != 0) {
                    score += tf/(tf+0.5+1.5*((float)lenDoc/(float)avgDocLength))*Math.log10((float) indexField.docCount()/df);
                }
            }
            return score;
        } catch (IOException ex) {
            throw new ScriptException("Could not compute okapi-tf: ", ex);
        }
    }

    public static class TFIDFScoreScriptFactory implements NativeScriptFactory {

        @Override
        public ExecutableScript newScript(Map<String, Object> params) {
            return new TFIDFScoreScript(params);
        }
    }
}
