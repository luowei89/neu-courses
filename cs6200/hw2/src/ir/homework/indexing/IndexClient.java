package ir.homework.indexing;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;

import java.io.*;
import java.util.*;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 3/3/15.
 */
public class IndexClient {
    
    private HashMap<String,Integer> termsMap;
    private HashMap<Integer, HashMap<Integer,List<Integer>>> docsIndex;
    private HashMap<Integer,String> docIdMap;
    private HashMap<Integer,Integer> docLengthMap;
    private HashMap<Integer,Integer> termsCatalog;

    private static int totalDocs = 0;
    private static int totalDocLength = 0;

    // models
    public static final String VSM = "TF_IDF";
    public static final String BM25 = "OKAPI_BM25";
    public static final String LM = "LM_LAPLACE";
    public static final String PS = "PROXIMITY_SEARCH";

    // for okapi_bm25
    private static final double b = 0.75;
    private static final double k1 = 1.2;
    private static final int k2 = 100;
    // for proximity search
    private static final int C = 1000;

    public IndexClient(){
        docsIndex = new HashMap<Integer, HashMap<Integer, List<Integer>>>();
        loadDocId();
        loadDocLength();
        loadTerms();
        loadTermsCatalog();
    }

    private HashMap<Integer, List<Integer>> getDocsIndex(int termId){
        if(! docsIndex.containsKey(termId)){
            try{
                File file = new File("out/inverted_index");
                FileInputStream fis = new FileInputStream(file);
                LineNumberReader lnr = new LineNumberReader(new InputStreamReader(fis));
                while(lnr.getLineNumber()<termsCatalog.get(termId)){
                    lnr.readLine();
                }

                String line = lnr.readLine();
                if(!line.equals("")) {
                    String[] docs = line.split("\t");
                    HashMap<Integer, List<Integer>> termIndex = new HashMap<Integer, List<Integer>>();
                    for(int i = 1;i < docs.length;i++){
                        String[] positions = docs[i].split(" ");
                        int docId = Integer.parseInt(positions[0]);
                        List<Integer> poss = new ArrayList<Integer>();
                        for(int j = 1;j < positions.length;j++){
                            poss.add(Integer.parseInt(positions[j]));
                        }
                        termIndex.put(docId,poss);
                    }
                    docsIndex.put(termId,termIndex);
                }
                lnr.close();
            } catch (IOException e){
                e.printStackTrace();
            }
        }
        return docsIndex.get(termId);
    }

    private void loadDocId(){
        docIdMap = new HashMap<Integer, String>();
        try {
            File file = new File("out/doc_id");
            FileInputStream fis = new FileInputStream(file);
            BufferedReader br = new BufferedReader(new InputStreamReader(fis));
            String line = br.readLine();
            while (line != null) {
                if(!line.equals("")) {
                    String[] docs = line.split(" ");
                    int docId = Integer.parseInt(docs[0]);
                    String docNo = docs[1];
                    docIdMap.put(docId, docNo);
                }
                line = br.readLine();
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void loadDocLength(){
        docLengthMap = new HashMap<Integer, Integer>();
        try {
            File file = new File("out/doc_length");
            FileInputStream fis = new FileInputStream(file);
            BufferedReader br = new BufferedReader(new InputStreamReader(fis));
            String line = br.readLine();
            while (line != null) {
                if(!line.equals("")) {
                    String[] docs = line.split(" ");
                    int docId = Integer.parseInt(docs[0]);
                    int docLength = Integer.parseInt(docs[1]);
                    docLengthMap.put(docId,docLength);
                    totalDocs += 1;
                    totalDocLength += docLength;
                }
                line = br.readLine();
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void loadTerms(){
        termsMap = new HashMap<String, Integer>();
        try {
            File file = new File("out/terms");
            FileInputStream fis = new FileInputStream(file);
            BufferedReader br = new BufferedReader(new InputStreamReader(fis));
            String line = br.readLine();
            while (line != null) {
                if(!line.equals("")) {
                    String[] docs = line.split("&");
                    String term = docs[0];
                    int termId = Integer.parseInt(docs[1]);
                    termsMap.put(term,termId);
                }
                line = br.readLine();
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void loadTermsCatalog(){
        termsCatalog = new HashMap<Integer, Integer>();
        try {
            File file = new File("out/terms_catalog");
            FileInputStream fis = new FileInputStream(file);
            BufferedReader br = new BufferedReader(new InputStreamReader(fis));
            String line = br.readLine();
            while (line != null) {
                if(!line.equals("")) {
                    String[] docs = line.split(" ");
                    int termId = Integer.parseInt(docs[0]);
                    int lineNum = Integer.parseInt(docs[1]);
                    termsCatalog.put(termId,lineNum);
                }
                line = br.readLine();
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

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

    public void executeQueries(HashMap<String,String[]> queries, String model){
        Iterator<String> keySetIterator = queries.keySet().iterator();
        double[][] scores = new double[totalDocs][2];
        try {
            File indexFile = new File("out/"+model + ".txt");
            indexFile.createNewFile();
            FileOutputStream fos = new FileOutputStream(indexFile);

            while (keySetIterator.hasNext()) {
                String key = keySetIterator.next();
                String[] terms = queries.get(key);
                for (int i = 0; i < totalDocs; i++) {
                    scores[i][0] = i + 1;
                    if (model.equals(VSM)) {
                        scores[i][1] = tfIdfScore(i + 1, terms);
                    } else if (model.equals(BM25)) {
                        scores[i][1] = bm25Score(i + 1, terms);
                    } else if (model.equals(LM)) {
                        scores[i][1] = lmScore(i + 1, terms);
                    } else if (model.equals(PS)) {
                        scores[i][1] = proximitySearch(i + 1, terms);
                    }
                }

                Arrays.sort(scores, new Comparator<double[]>() {
                    @Override
                    public int compare(double[] o1, double[] o2) {
                        if (o1[1] < o2[1]) {
                            return 1;
                        } else if (o1[1] > o2[1]) {
                            return -1;
                        } else {
                            return 0;
                        }
                    }
                });
                outputScores(key, scores, fos);
            }
            fos.flush();
            fos.close();
        } catch (FileNotFoundException e){
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void outputScores(String queryId,double[][] scores,FileOutputStream fos) {
        try {
            for (int i = 0; i < 100; i++) {
                StringBuffer sb = new StringBuffer();
                sb.append(queryId);
                sb.append(" Q0");
                sb.append(" " + docIdMap.get((int)scores[i][0]));
                sb.append(" " + (i+1));
                sb.append(" " + scores[i][1]);
                sb.append(" Exp\n");
                fos.write(sb.toString().getBytes());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private double tfIdfScore(int docId, String[] terms) {
        double score = 0;
        for(String term : terms){
            if(termsMap.containsKey(term)) {
                int termId = termsMap.get(term);
                if (getDocsIndex(termId).containsKey(docId)) {
                    int tf = getDocsIndex(termId).get(docId).size();
                    int df = getDocsIndex(termId).size();
                    double avgDocLength = totalDocLength / (double) totalDocs;
                    score += tf / (tf + 0.5 + 1.5 * (docLengthMap.get(docId) / avgDocLength)) * Math.log10(totalDocs / (double) df);
                }
            }
        }
        return score;
    }

    private double bm25Score(int docId, String[] terms) {
        double score = 0;
        HashMap<String,Integer> tfQuery = new HashMap<String, Integer>();
        for(String term : terms){
            if(!tfQuery.containsKey(term)){
                tfQuery.put(term, 0);
            }
            tfQuery.put(term,tfQuery.get(term)+1);
        }
        for(String term : terms){
            if(termsMap.containsKey(term)) {
                int termId = termsMap.get(term);
                if (getDocsIndex(termId).containsKey(docId)) {
                    int tf = getDocsIndex(termId).get(docId).size();
                    int df = getDocsIndex(termId).size();
                    int tfq = tfQuery.get(term);
                    double avgDocLength = totalDocLength / (double) totalDocs;
                    if(tf != 0){
                        double log_term = Math.log10((totalDocs + 0.5) / (df + 0.5));
                        double k1_term = (tf+k1*tf)/(tf+k1*((1-b)+b*(docLengthMap.get(docId)/avgDocLength)));
                        double k2_term = (tfq+k2*tfq)/(double)(tfq+k2);
                        score += log_term*k1_term*k2_term;
                    }
                }
            }
        }
        return score;
    }

    private double lmScore(int docId, String[] terms) {
        double score = 0;
        for(String term : terms){
            if(termsMap.containsKey(term)) {
                int termId = termsMap.get(term);
                if (getDocsIndex(termId).containsKey(docId)) {
                    int tf = getDocsIndex(termId).get(docId).size();
                    score += Math.log10((tf+1)/(double)(docLengthMap.get(docId)+termsMap.size()));
                } else {
                    score += Math.log10(1.0/(double)(docLengthMap.get(docId)+termsMap.size()));
                }
            }
        }
        return score;
    }

    private double proximitySearch(int docId, String[] terms){
        List<List<Integer>> termsPositions = new ArrayList<List<Integer>>();
        for(String term : terms){
            if(termsMap.containsKey(term)) {
                int termId = termsMap.get(term);
                if (getDocsIndex(termId).containsKey(docId)) {
                    termsPositions.add(getDocsIndex(termId).get(docId));
                }
            }
        }
        int numContainTerms = termsPositions.size();
        int rangeOfWindow = getMinSpan(termsPositions);
        double proximity = (C - rangeOfWindow) * numContainTerms / ((double)(docLengthMap.get(docId)+termsMap.size()));
        return proximity + tfIdfScore(docId,terms);
    }

    private int getMinSpan(List<List<Integer>> termsPositions) {
        int minSpan = Integer.MAX_VALUE;
        int terms = termsPositions.size();
        int[][] poss = new int[terms][2];
        int[] currentIndex = new int[terms];
        int minIndex = 0;
        while(minIndex < terms) {
            for (int i = 0; i < terms; i++) {
                poss[i][0] = i;
                poss[i][1] = termsPositions.get(i).get(currentIndex[i]);
            }
            Arrays.sort(poss, new Comparator<int[]>() {
                @Override
                public int compare(int[] o1, int[] o2) {
                    if (o1[1] < o2[1]) {
                        return -1;
                    } else if (o1[1] > o2[1]) {
                        return 1;
                    } else {
                        return 0;
                    }
                }
            });
            if((poss[terms-1][1] - poss[0][1]) < minSpan){
                minSpan = poss[terms-1][1] - poss[0][1];
            }
            if(currentIndex[poss[minIndex][0]] < termsPositions.get(poss[minIndex][0]).size()-1){
                currentIndex[poss[minIndex][0]]++;
            } else {
                minIndex++;
            }
        }
        return minSpan;
    }

    public static void main(String[] args){
        File queryFile = new File("../dataset/AP_DATA/query_desc.51-100.short.txt");
        HashMap<String,String[]> queries = parseQueries(queryFile);

        IndexClient ic = new IndexClient();
        ic.executeQueries(queries, VSM);
        ic.executeQueries(queries, BM25);
        ic.executeQueries(queries, LM);
        ic.executeQueries(queries, PS);
    }
}
