package ir.homework.treceval;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.ChartUtilities;
import org.jfree.chart.JFreeChart;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;

import java.io.*;
import java.util.*;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 4/6/15.
 */
public class TrecEval {

    private boolean qOption;
    private HashMap<String,HashMap<String,Boolean>> qrel;
    private HashMap<String,HashMap<String,Double>> trec;
    private HashMap<String,TreeMap<String,Double>> trecSorted;
    private HashMap<String,Evaluation> evaluations;

    private static final List<Integer> ks = Arrays.asList(5, 10, 20, 50, 100);

    public TrecEval(boolean q){
        qOption = q;
        qrel = new HashMap<String, HashMap<String, Boolean>>();
        trec = new HashMap<String, HashMap<String, Double>>();
        trecSorted = new HashMap<String, TreeMap<String, Double>>();
        evaluations = new HashMap<String, Evaluation>();
    }

    public void loadQrel(String qrelFile) {
        try {
            File f = new File(qrelFile);
            FileInputStream fis = new FileInputStream(f);
            BufferedReader br = new BufferedReader(new InputStreamReader(fis));
            String line = br.readLine();
            while(line != null){
                String[] parts = line.split(" ");
                if(qrel.containsKey(parts[0])){
                    qrel.get(parts[0]).put(parts[2],!parts[3].equals("0"));
                } else {
                    HashMap<String,Boolean> docs = new HashMap<String, Boolean>();
                    docs.put(parts[2],!parts[3].equals("0"));
                    qrel.put(parts[0],docs);
                }
                line = br.readLine();
            }
            br.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void loadTrec(String trecFile) {
        try {
            File f = new File(trecFile);
            FileInputStream fis = new FileInputStream(f);
            BufferedReader br = new BufferedReader(new InputStreamReader(fis));
            String line = br.readLine();
            while(line != null){
                String[] parts = line.split(" ");
                if(trec.containsKey(parts[0])){
                    trec.get(parts[0]).put(parts[2], Double.parseDouble(parts[3]));
                } else {
                    HashMap<String,Double> docs = new HashMap<String, Double>();
                    docs.put(parts[2],Double.parseDouble(parts[3]));
                    trec.put(parts[0],docs);
                }
                line = br.readLine();
            }
            br.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        for(String key : trec.keySet()){
            HashMap<String,Double> docs = trec.get(key);
            ScoreComparator sc = new ScoreComparator(docs);
            TreeMap<String,Double> sorted = new TreeMap<String, Double>(sc);
            sorted.putAll(docs);
            trecSorted.put(key,sorted);
        }
    }

    public void evaluate(){
        for(String query : trec.keySet()){
            Evaluation e = new Evaluation(query);
            e.evaluate();
            evaluations.put(query,e);
        }
    }

    public void print(){
        Evaluation sum_e = new Evaluation(""+evaluations.size());
        for(String key : evaluations.keySet()){
            if(qOption){
                evaluations.get(key).print();
            }
            evaluations.get(key).plotPrecRecall();
            sum_e.add(evaluations.get(key));
        }
        sum_e.avg(evaluations.size());
        sum_e.print();
    }

    public static void main(String[] args){
        if(args.length < 2 || (args.length < 3 && args[0].equals("-q"))){
            System.out.println("Usage:  java TrecEval [-q] <qrel_file> <trec_file>\n\n");
            System.exit(0);
        }
        boolean qOption = args[0].equals("-q");
        String qrelFile, trecFile;
        if(qOption){
            qrelFile = args[1];
            trecFile = args[2];
        } else {
            qrelFile = args[0];
            trecFile = args[1];
        }
        TrecEval te = new TrecEval(qOption);
        te.loadQrel(qrelFile);
        te.loadTrec(trecFile);
        te.evaluate();
        te.print();
    }

    private class ScoreComparator implements Comparator<String> {

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

    private class Evaluation{

        private String queryId;
        private int retrieved;
        private int num_rel;
        private int rec_rel;
        private double r_precision;
        private double avg_precision;
        private double ndcg;
        private HashMap<Integer,Double> precisions;
        private HashMap<Integer,Double> recalls;
        private HashMap<Integer,Double> f1s;
        //for the plot
        private List<Double> precList;
        private List<Double> recallList;

        public Evaluation(String query){
            queryId = query;
            precisions = new HashMap<Integer, Double>();
            recalls = new HashMap<Integer, Double>();
            f1s = new HashMap<Integer, Double>();
            num_rel = 0;
            rec_rel = 0;
            retrieved = 0;
            r_precision = 0.0;
            avg_precision = 0.0;
            ndcg = 0.0;
            for(int k : ks){
                precisions.put(k,0.0);
                recalls.put(k,0.0);
                f1s.put(k,0.0);
            }
            precList = new ArrayList<Double>();
            recallList = new ArrayList<Double>();
        }

        public void evaluate(){
            HashMap<String,Boolean> qrels = qrel.get(queryId);
            TreeMap<String,Double> trecs = trecSorted.get(queryId);
            List<Integer> r = new ArrayList<Integer>();
            retrieved = trecs.size();
            for(String key : qrels.keySet()){
                num_rel += qrels.get(key)?1:0;
            }
            int i = 0;
            double sum_prec = 0.0;
            for(String key : trecs.descendingKeySet()){
                Boolean t = qrels.get(key);
                if(t == null){
                    t = false;
                }
                i++;
                rec_rel += t?1:0;
                r.add(t?1:0);
                double prec = rec_rel *1.0/i;
                double recall = rec_rel *1.0/num_rel;

                precList.add(prec);
                recallList.add(recall);

                if(t){
                    sum_prec += prec;
                }
                if(ks.contains(i)){
                    precisions.put(i,prec);
                    recalls.put(i,recall);
                    if(prec*recall == 0){
                        f1s.put(i,0.0);
                    } else{
                        f1s.put(i,2*((prec*recall)/(prec+recall)));
                    }
                }
                if(i == num_rel){
                    r_precision = rec_rel *1.0/num_rel;
                }
            }
            avg_precision = sum_prec/num_rel;
            if(rec_rel > 0) {
                double dcg = dcg(r, i);
                Collections.sort(r);
                Collections.reverse(r);
                ndcg = dcg / dcg(r, i);
            }
        }

        private double dcg(List<Integer> r, int k) {
            double dcg = r.get(0);
            for(int i = 1;i < k; i++){
                dcg += r.get(i)/Math.log(i+1);
            }
            return dcg;
        }

        public void print(){
            StringBuffer sb = new StringBuffer();
            sb.append("============================================================\n");
            sb.append("Queryid (Num):\t" + queryId + "\n");
            sb.append("Total number of documents over all queries\n");
            sb.append("\tRetrieved:\t" + retrieved + "\n");
            sb.append("\tRelevant:\t" + num_rel + "\n");
            sb.append("\tRel_ret:\t" + rec_rel + "\n");

            sb.append("R-Precision (precision after R (= num_rel for a query) docs retrieved):\n");
            sb.append("\t\tExact:\t" + String.format("%.4f",r_precision) + "\n");
            sb.append("Average precision (non-interpolated) for all rel docs(averaged over queries)\n");
            sb.append("\t\t\t\t" + String.format("%.4f",avg_precision) + "\n");
            sb.append("nDCG (normalized Discounted Cumulative Gain)\n");
            sb.append("\t\t\t\t" + String.format("%.4f",ndcg) + "\n");

            sb.append("Precision:\n");
            for(int k : ks){
                sb.append("  at" + String.format("%4d",k) + " docs:\t" + String.format("%.4f", precisions.get(k)) + "\n");
            }

            sb.append("Recall:\n");
            for(int k : ks){
                sb.append("  at" + String.format("%4d",k) + " docs:\t" + String.format("%.4f",recalls.get(k)) + "\n");
            }

            sb.append("F1:\n");
            for(int k : ks){
                sb.append("  at" + String.format("%4d",k) + " docs:\t" + String.format("%.4f",f1s.get(k)) + "\n");
            }

            sb.append("============================================================\n");
            System.out.println(sb.toString());
        }

        public void plotPrecRecall(){
            double recall_level[] = {0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0};
            XYSeriesCollection dataset = new XYSeriesCollection();
            XYSeries precs = new XYSeries("Precision");
            XYSeries interpolated_precs = new XYSeries("Interpolated Precision");

            int i = 0;
            for(double rec : recall_level){
                while(i < recallList.size() && recallList.get(i) < rec){
                    i++;
                }
                if(i < recallList.size()){
                    precs.add(rec,precList.get(i));
                } else {
                    precs.add(rec,0);
                }
            }

            double[] reverse_recall = {1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0};
            double current_max = 0;
            i = recallList.size() - 1;
            for(double rec : reverse_recall){
                while(i >= 0 && recallList.get(i) >= rec){
                    if(current_max < precList.get(i)){
                        current_max = precList.get(i);
                    }
                    i--;
                }
                interpolated_precs.add(rec,current_max);
            }

            dataset.addSeries(precs);
            dataset.addSeries(interpolated_precs);
            String chartTitle = "Precision-Recall Curve " + queryId;
            String xAxisLabel = "Recall";
            String yAxisLabel = "Precision";

            JFreeChart chart = ChartFactory.createXYLineChart(chartTitle,
                    xAxisLabel, yAxisLabel, dataset);
            try {
                ChartUtilities.saveChartAsPNG(new File("curve_"+queryId+".png"),chart,400,400);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        public void add(Evaluation e) {
            for(int k: ks){
                precisions.put(k,precisions.get(k)+e.precisions.get(k));
                recalls.put(k,recalls.get(k)+e.recalls.get(k));
                f1s.put(k,f1s.get(k)+e.f1s.get(k));
            }
            retrieved += e.retrieved;
            num_rel += e.num_rel;
            rec_rel += e.rec_rel;
            r_precision += e.r_precision;
            avg_precision += e.avg_precision;
            ndcg += e.ndcg;
        }

        public void avg(int n) {
            for(int k: ks){
                precisions.put(k,precisions.get(k)/n);
                recalls.put(k,recalls.get(k)/n);
                f1s.put(k,f1s.get(k)/n);
            }
            r_precision /= n;
            avg_precision /= n;
            ndcg /= n;
        }
    }
}
