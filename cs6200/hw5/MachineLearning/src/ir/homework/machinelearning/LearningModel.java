package ir.homework.machinelearning;

import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import weka.classifiers.functions.LinearRegression;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 4/20/15.
 */
public class LearningModel {

    private static HashMap<String,HashMap<String,Double>> testModel(LinearRegression model, String testFile) throws Exception {
        HashMap<String,HashMap<String,Double>> scores = new HashMap<String, HashMap<String, Double>>();
        DataSource test = new DataSource(testFile);
        Instances testData = test.getDataSet();
        for(int i = 0; i < testData.numInstances();i++){
            Instance inst = testData.instance(i);
            String id = inst.stringValue(0);
            Instance new_inst = new Instance(inst);
            new_inst.deleteAttributeAt(0);
            double score = model.classifyInstance(new_inst);
            String qid = id.substring(0,id.indexOf('-'));
            String did = id.substring(id.indexOf('-')+1);
            if(!scores.containsKey(qid)){
                scores.put(qid,new HashMap<String, Double>());
            }
            scores.get(qid).put(did, score);
        }
        return scores;
    }

    private static void saveScores(HashMap<String, HashMap<String, Double>> scores,String filename) {
        StringBuffer sb = new StringBuffer();
        for(String query : scores.keySet()){
            int rank = 1;
            HashMap<String, Double> queryScores = scores.get(query);
            ScoreComparator sc =  new ScoreComparator(queryScores);
            TreeMap<String,Double> sorted = new TreeMap<String,Double>(sc);
            sorted.putAll(queryScores);
            for(String doc : sorted.keySet()){
                sb.append(query + " Q0");
                sb.append(" " + doc);
                sb.append(" " + rank++);
                sb.append(" "+ queryScores.get(doc));
                sb.append(" Exp\n");
                if(rank > 1000){
                    break;
                }
            }
        }
        try {
            File indexFile = new File(filename);
            indexFile.createNewFile();
            FileOutputStream fos = new FileOutputStream(indexFile);
            fos.write(sb.toString().getBytes());
            fos.flush();
            fos.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args){
        try {
            DataSource source = new DataSource("train.csv");
            Instances data = source.getDataSet();
            data.setClassIndex(data.numAttributes()-1);
            data.deleteAttributeAt(0);
            LinearRegression model = new LinearRegression();
            model.buildClassifier(data);

            HashMap<String,HashMap<String,Double>> scores = testModel(model,"test.csv");
            saveScores(scores,"test-results.txt");

            HashMap<String,HashMap<String,Double>> train_scores = testModel(model,"train.csv");
            saveScores(train_scores,"train-results.txt");
        } catch (IOException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static class ScoreComparator implements Comparator<String> {

        Map<String, Double> base;
        public ScoreComparator(Map<String, Double> base) {
            this.base = base;
        }

        public int compare(String a, String b) {
            if (base.get(a) >= base.get(b)) {
                return -1;
            } else {
                return 1;
            }
        }
    }
}
