package ir.homework.machinelearning;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;

import java.io.*;
import java.util.*;
import java.util.regex.Pattern;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 4/18/15.
 */
public class DataProcessor {
    private HashMap<String,Integer> termsMap;
    private HashMap<Integer, HashMap<Integer,List<Integer>>> docsIndex;
    private HashMap<String,Integer> docIdMap;
    private HashMap<Integer,Integer> docLengthMap;

    private Set<String> stopList;
    private HashMap<String,String[]> queries;
    private HashMap<String,HashMap<String,String>> assesses;
    private Set<String> assessedDocs;

    private static int totalDocs = 0;
    private static int totalDocLength = 0;
    private static Pattern pattern = Pattern.compile("\\w+(\\.?\\w+)*");
    private static QueryParser parser = new QueryParser("",new EnglishAnalyzer());

    // for okapi_bm25
    private static final double b = 0.75;
    private static final double k1 = 1.2;
    private static final int k2 = 100;
    // for proximity search
    private static final int C = 1000;

    public DataProcessor(){
        termsMap = new HashMap<String,Integer>();
        docIdMap = new HashMap<String, Integer>();
        docLengthMap = new HashMap<Integer, Integer>();
        docsIndex = new HashMap<Integer, HashMap<Integer, List<Integer>>>();
        loadStopList();
        loadQueries();
        loadAssesses();
    }

    private void loadStopList(){
        stopList = new HashSet<String>();
        try {
            File stopFile = new File("../../data/AP_DATA/stoplist.txt");
            FileInputStream fis = new FileInputStream(stopFile);
            BufferedReader br = new BufferedReader(new InputStreamReader(fis));
            String line = br.readLine();
            while(line != null){
                stopList.add(line.trim());
                line = br.readLine();
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void loadQueries(){
        queries = new HashMap<String, String[]>();
        try {
            Analyzer a  = new EnglishAnalyzer();
            QueryParser parser = new QueryParser("",a);
            File queryFile = new File("../../data/AP_DATA/query_desc.51-100.short.txt");
            FileInputStream fis = new FileInputStream(queryFile);
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
    }

    private void loadAssesses(){
        assesses = new HashMap<String, HashMap<String, String>>();
        assessedDocs = new HashSet<String>();
        try {
            File qrelFile = new File("../../data/AP_DATA/qrels.adhoc.51-100.AP89.txt");
            FileInputStream fis = new FileInputStream(qrelFile);
            BufferedReader br = new BufferedReader(new InputStreamReader(fis));
            String line = br.readLine();
            while(line != null){
                String[] terms = line.split(" ");
                if(queries.containsKey(terms[0])) {
                    if (!assesses.containsKey(terms[0])) {
                        assesses.put(terms[0], new HashMap<String, String>());
                    }
                    assesses.get(terms[0]).put(terms[2], terms[3]);
                    assessedDocs.add(terms[2]);
                }
                line = br.readLine();
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void buildIndexFromFiles(){
        File folder = new File("../../data/AP_DATA/ap89_collection/");
        File[] listOfFiles = folder.listFiles();

        for (File file : listOfFiles){
            buildIndexFromFile(file);
        }
    }

    public HashMap<Integer, Integer> updateTerms(String text){
        HashMap<Integer, Integer> termPositions = new HashMap<Integer, Integer>();
        try {
            int position = 0;
            text = text.replace("AND","").replace("OR","").replace("NOT","");
            String[] words = text.split(" ");
            for(String word : words) {
                if(!word.equals("")) {
                    String term = parser.parse(QueryParser.escape(word)).toString();
                    if (!term.equals("") && pattern.matcher(word).find() && !stopList.contains(term)) {
                        if (!termsMap.containsKey(term)) {
                            termsMap.put(term, termsMap.size() + 1);
                        }
                        termPositions.put(position++, termsMap.get(term));
                    }
                }
            }
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return termPositions;
    }

    public void buildIndexFromFile(File file){
        try {
            FileInputStream fis = new FileInputStream(file);
            BufferedReader br = new BufferedReader(new InputStreamReader(fis));
            String line = br.readLine();
            String id = null;
            String text = null;
            Boolean texting = false;
            while (line != null) {
                line = line.trim();
                if (line.startsWith("<DOC>")){
                    id = "";
                    text = "";
                } else if (line.startsWith("<DOCNO>")){
                    id = line.substring(7,line.length()-8).trim();
                } else if (line.startsWith("<TEXT>")) {
                    texting = true;
                } else if (line.startsWith("</TEXT>")) {
                    texting = false;
                } else if (line.startsWith("</DOC>")) {
                    if(assessedDocs.contains(id)) {
                        newDocIndex(++totalDocs, id, text);
                    }
                }
                if (texting && !line.startsWith("<TEXT>")){
                    text = text + " " + line;
                }
                line = br.readLine();
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void newDocIndex(int id,String docNo,String text){
        HashMap<Integer, Integer> docIndex = updateTerms(text);
        updateDocsIndex(id, docIndex);
        docIdMap.put(docNo,id);
        docLengthMap.put(id,docIndex.size());
        totalDocLength += docIndex.size();
    }

    public void updateDocsIndex(Integer id, HashMap<Integer, Integer> positions){
        for(Integer p :positions.keySet()){
            Integer term = positions.get(p);

            HashMap<Integer,List<Integer>> docTermIndex;
            if(docsIndex.containsKey(term)) {
                docTermIndex = docsIndex.get(term);
            } else {
                docTermIndex = new HashMap<Integer, List<Integer>>();
            }

            List<Integer> poss;
            if(docTermIndex.containsKey(id)){
                poss = docTermIndex.get(id);
            } else {
                poss = new ArrayList<Integer>();
            }
            poss.add(p);
            docTermIndex.put(id,poss);
            docsIndex.put(term,docTermIndex);
        }
    }


    private void generateFeatures() {
        Random generator = new Random();
        Set<String> queryIds = new HashSet<String>(queries.keySet());
        List<String> queryIdList = new ArrayList<String>(queryIds);
        Set<String> testQueries = new HashSet<String>();
        while(testQueries.size() < 5){
            testQueries.add(queryIdList.get(generator.nextInt(queryIds.size())));
        }
        queryIds.removeAll(testQueries);
        generateFeatures(testQueries,true);
        generateFeatures(queryIds,false);
    }

    private void generateFeatures(Set<String> queryIds, boolean test) {
        StringBuffer sb = new StringBuffer();
        for(String queryId : queryIds){
            String[] terms = queries.get(queryId);
            HashMap<String,String> docs = assesses.get(queryId);
            for(String docId : docs.keySet()){
                sb.append(queryId+"-"+docId);
                sb.append(", "+okapiTf(docIdMap.get(docId), terms));
                sb.append(", "+tfIdfScore(docIdMap.get(docId), terms));
                sb.append(", "+bm25Score(docIdMap.get(docId),terms));
                sb.append(", "+lmScore(docIdMap.get(docId), terms));
                sb.append(", "+proximitySearch(docIdMap.get(docId), terms));
                if(!test){
                    sb.append(", "+docs.get(docId));
                }
                sb.append("\n");
            }
        }
        try {
            String fileName = test?"test.csv":"train.csv";
            File indexFile = new File(fileName);
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

    private double tfIdfScore(int docId, String[] terms) {
        double score = 0;
        for(String term : terms){
            if(termsMap.containsKey(term)) {
                int termId = termsMap.get(term);
                if (docsIndex.get(termId).containsKey(docId)) {
                    int tf = docsIndex.get(termId).get(docId).size();
                    int df = docsIndex.get(termId).size();
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
                if (docsIndex.get(termId).containsKey(docId)) {
                    int tf = docsIndex.get(termId).get(docId).size();
                    int df = docsIndex.get(termId).size();
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
                if (docsIndex.get(termId).containsKey(docId)) {
                    int tf = docsIndex.get(termId).get(docId).size();
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
                if (docsIndex.get(termId).containsKey(docId)) {
                    termsPositions.add(docsIndex.get(termId).get(docId));
                }
            }
        }
        int numContainTerms = termsPositions.size();
        int rangeOfWindow = getMinSpan(termsPositions);
        double proximity = (C - rangeOfWindow) * numContainTerms / ((double)(docLengthMap.get(docId)+termsMap.size()));
        return proximity + tfIdfScore(docId,terms);
    }

    private double okapiTf(int docId, String[] terms){
        double score = 0;
        for(String term : terms){
            if(termsMap.containsKey(term)) {
                int termId = termsMap.get(term);
                if (docsIndex.get(termId).containsKey(docId)) {
                    int tf = docsIndex.get(termId).get(docId).size();
                    double avgDocLength = totalDocLength / (double) totalDocs;
                    score += tf / (tf + 0.5 + 1.5 * (docLengthMap.get(docId) / avgDocLength));
                }
            }
        }
        return score;
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
        DataProcessor dp = new DataProcessor();
        dp.buildIndexFromFiles();
        dp.generateFeatures();
    }
}
