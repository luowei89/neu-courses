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
public class UniLMLaplaceScoreScript extends AbstractSearchScript {

    String field = null;
    ArrayList<String> terms = null;

    public static final String SCRIPT_NAME = "lm_laplace_script";

    private static final long V = 178050;

    public UniLMLaplaceScoreScript(Map<String, Object> params) {
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
                int tf = indexFieldTerm.tf();
                score += Math.log10((float)(tf+1)/(float)(lenDoc+V));
            }
            return score;
        } catch (IOException ex) {
            throw new ScriptException("Could not compute score: ", ex);
        }
    }

    public static class UniLMLaplaceScoreScriptFactory implements NativeScriptFactory {

        @Override
        public ExecutableScript newScript(Map<String, Object> params) {
            return new UniLMLaplaceScoreScript(params);
        }
    }
}
