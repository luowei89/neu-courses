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
    private HashMap<Integer,String> docIdMap;
    private HashMap<Integer,Integer> docLengthMap;
    private HashMap<Integer,Integer> termsCatalog;
    private HashMap<Integer, HashMap<Integer,List<Integer>>> partDocsIndex;
    private HashMap<Integer,List<Integer>> termsIndexFileMap;
    private HashMap<Integer,HashMap<Integer,Integer>> termsFileCatalogs;

    private List<String> stopList;

    private static int totalDocs = 0;
    private static Pattern pattern = Pattern.compile("\\w+(\\.?\\w+)*");
    private static QueryParser parser = new QueryParser("",new EnglishAnalyzer());

    public Indexer(){
        termsMap = new HashMap<String,Integer>();
        docIdMap = new HashMap<Integer, String>();
        docLengthMap = new HashMap<Integer, Integer>();
        termsCatalog = new HashMap<Integer, Integer>();
        partDocsIndex = new HashMap<Integer, HashMap<Integer, List<Integer>>>();
        termsFileCatalogs = new HashMap<Integer, HashMap<Integer, Integer>>();
        termsIndexFileMap = new HashMap<Integer, List<Integer>>();
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

    private void savePartIndex(int partNum){
        try {
            HashMap<Integer,Integer> termsPartCatalog = new HashMap<Integer, Integer>();
            File indexFile = new File("out/temp/inverted_index_"+partNum);
            indexFile.createNewFile();
            FileOutputStream fos = new FileOutputStream(indexFile);
            int lineNum = 0;
            for (Integer termId : partDocsIndex.keySet()) {
                StringBuffer sb = new StringBuffer();
                sb.append(termId);
                HashMap<Integer,List<Integer>> docTermIndex = partDocsIndex.get(termId);
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

                termsPartCatalog.put(termId,lineNum++);
                List<Integer> fileIds = termsIndexFileMap.get(termId);
                fileIds.add(partNum);
                termsIndexFileMap.put(termId,fileIds);
            }
            termsFileCatalogs.put(partNum,termsPartCatalog);
            fos.flush();
            fos.close();
        } catch (FileNotFoundException e){
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void saveDocId(){
        try {
            File file = new File("out/doc_id");
            file.createNewFile();
            FileOutputStream fos = new FileOutputStream(file);
            for (Integer docId : docIdMap.keySet()) {
                StringBuffer sb = new StringBuffer();
                sb.append(docId);
                sb.append(" ");
                sb.append(docIdMap.get(docId));
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

    private void saveDocLength(){
        try {
            File file = new File("out/doc_length");
            file.createNewFile();
            FileOutputStream fos = new FileOutputStream(file);
            for (Integer docId : docLengthMap.keySet()) {
                StringBuffer sb = new StringBuffer();
                sb.append(docId);
                sb.append(" ");
                sb.append(docLengthMap.get(docId));
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

    private void saveTerms(){
        try {
            File file = new File("out/terms");
            file.createNewFile();
            FileOutputStream fos = new FileOutputStream(file);
            for (String term : termsMap.keySet()) {
                StringBuffer sb = new StringBuffer();
                sb.append(term);
                sb.append("&");
                sb.append(termsMap.get(term));
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

    private void saveTermsCatalog(){
        try {
            File file = new File("out/terms_catalog");
            file.createNewFile();
            FileOutputStream fos = new FileOutputStream(file);
            for (Integer termId : termsCatalog.keySet()) {
                StringBuffer sb = new StringBuffer();
                sb.append(termId);
                sb.append(" ");
                sb.append(termsCatalog.get(termId));
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
                            termsIndexFileMap.put(termsMap.size(),new ArrayList<Integer>());
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
        mergePartIndex();
        saveDocId();
        saveDocLength();
        saveTerms();
        saveTermsCatalog();
    }

    public void mergePartIndex(){
        try {
            File indexFile = new File("out/inverted_index");
            indexFile.createNewFile();
            FileOutputStream fos = new FileOutputStream(indexFile);
            int lineNum = 0;
            for (String term : termsMap.keySet()){
                int termId = termsMap.get(term);
                StringBuffer sb = new StringBuffer();
                sb.append(termId);
                List<Integer> files = termsIndexFileMap.get(termId);
                for(int fileId :files){
                    HashMap<Integer,Integer> catalog = termsFileCatalogs.get(fileId);
                    File file = new File("out/temp/inverted_index_"+fileId);
                    FileInputStream fis = new FileInputStream(file);
                    LineNumberReader lnr = new LineNumberReader(new InputStreamReader(fis));
                    while(lnr.getLineNumber() < catalog.get(termId)){
                        lnr.readLine();
                    }
                    String line = lnr.readLine();
                    String[] docs = line.split("\t");
                    for(int i = 1;i < docs.length;i++){
                        sb.append("\t");
                        sb.append(docs[i]);
                    }
                }
                sb.append("\n");
                fos.write(sb.toString().getBytes());
                termsCatalog.put(termId,lineNum++);
            }
        }  catch (IOException e) {
            e.printStackTrace();
        }
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
                    if(totalDocs> 0 && totalDocs%1000==0){
                        savePartIndex(totalDocs/1000);
                        partDocsIndex = new HashMap<Integer, HashMap<Integer, List<Integer>>>();
                    }
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
        updateDocsIndex(id, docIndex);
        docIdMap.put(id,docNo);
        docLengthMap.put(id,docIndex.size());
    }

    public void updateDocsIndex(Integer id, HashMap<Integer, Integer> positions){
        for(Integer p :positions.keySet()){
            Integer term = positions.get(p);

            HashMap<Integer,List<Integer>> docTermIndex;
            if(partDocsIndex.containsKey(term)) {
                docTermIndex = partDocsIndex.get(term);
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
            partDocsIndex.put(term,docTermIndex);
        }
    }

    public static void main(String[] args){
        Indexer in = new Indexer();
        in.buildIndexFromFiles();
    }
}
