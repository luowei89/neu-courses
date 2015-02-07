package ir.elasticsearch.homework.plugin;

import ir.elasticsearch.homework.scripts.*;
import org.elasticsearch.plugins.AbstractPlugin;
import org.elasticsearch.script.ScriptModule;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 2/5/15.
 */
public class ScoreScriptsPlugin extends AbstractPlugin {
    @Override
    public String name() {
        return "score-script-plugin";
    }

    @Override
    public String description() {
        return "plugin for native score scripts";
    }

    public void onModule(ScriptModule module) {
        module.registerScript(OkapiTFScoreScript.SCRIPT_NAME, OkapiTFScoreScript.OkapiTFScoreScriptFactory.class);
        module.registerScript(TFIDFScoreScript.SCRIPT_NAME, TFIDFScoreScript.TFIDFScoreScriptFactory.class);
        module.registerScript(OkapiBM25ScoreScript.SCRIPT_NAME, OkapiBM25ScoreScript.OkapiBM25ScoreScriptFactory.class);
        module.registerScript(UniLMLaplaceScoreScript.SCRIPT_NAME, UniLMLaplaceScoreScript.UniLMLaplaceScoreScriptFactory.class);
        module.registerScript(UniLMJelinekMercerScoreScript.SCRIPT_NAME, UniLMJelinekMercerScoreScript.UniLMJelinekMercerScoreScriptFactory.class);
    }
}
