package ir.homework.indexing;

import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;

import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.regex.Pattern;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 3/2/15.
 */
public class Indexer {

    private HashMap<String,Integer> termsMap;
    private HashMap<Integer, HashMap<Integer,List<Integer>>> docsIndex;
    private HashMap<Integer,String> docIdMap;
    private HashMap<Integer,Integer> docLengthMap;

    private List<String> stopList;

    private static int totalDocs = 0;
    private static int totalDocLength = 0;
    private static Pattern pattern = Pattern.compile("\\w+(\\.?\\w+)*");
    private static QueryParser parser = new QueryParser("",new EnglishAnalyzer());

    public Indexer(){
        termsMap = new HashMap<String,Integer>();
        docIdMap = new HashMap<Integer, String>();
        docLengthMap = new HashMap<Integer, Integer>();
        docsIndex = new HashMap<Integer, HashMap<Integer, List<Integer>>>();
        setStopList();
    }

    private void setStopList(){
        stopList = new ArrayList<String>();
        try {
            File stopFile = new File("../dataset/AP_DATA/stoplist.txt");
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

    private void saveIndex(){
        try {
            File indexFile = new File("out/inverted_index");
            indexFile.createNewFile();
            FileOutputStream fos = new FileOutputStream(indexFile);
            for (Integer termId : docsIndex.keySet()) {
                StringBuffer sb = new StringBuffer();
                sb.append(termId);
                HashMap<Integer,List<Integer>> docTermIndex = docsIndex.get(termId);
                for(Integer docId: docTermIndex.keySet()){
                    sb.append("\t");
                    sb.append(docId);
                    List<Integer> poss = docTermIndex.get(docId);
                    for(Integer pos : poss){
                        sb.append(" ");
                        sb.append(pos);
                    }
                }
                sb.append("\n");
                fos.write(sb.toString().getBytes());
            }
            fos.flush();
            fos.close();
        } catch (FileNotFoundException e){
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
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

    public void buildIndexFromFiles(){
        File folder = new File("../dataset/AP_DATA/ap89_collection/");
        File[] listOfFiles = folder.listFiles();

        for (File file : listOfFiles){
            buildIndexFromFile(file);
        }
        saveIndex();
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
                    newDocIndex(totalDocs+++1, id, text);
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
        updateDocsIndex(id,docIndex);
        docIdMap.put(id,docNo);
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

    public int getTotalDocs(){
        return totalDocs;
    }
    public int getTotalDocLength(){
        return totalDocLength;
    }

    public HashMap<String,Integer> getTermsMap(){
        return termsMap;
    }
    public HashMap<Integer, HashMap<Integer,List<Integer>>> getDocsIndex(){
        return docsIndex;
    }
    public HashMap<Integer,String> getDocIdMap(){
        return docIdMap;
    }
    public HashMap<Integer,Integer> getDocLengthMap(){
        return docLengthMap;
    }

    public static void main(String[] args){
        Indexer in = new Indexer();
        in.buildIndexFromFiles();
    }
}
