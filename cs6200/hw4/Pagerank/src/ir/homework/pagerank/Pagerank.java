package ir.homework.pagerank;

import java.io.*;
import java.util.*;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 4/8/15.
 */
public class Pagerank {

    private HashMap<String, Set<String>> inlinksMap;
    private HashMap<String, Set<String>> outlinksMap;
    private HashMap<String, Double> prTable;

    public static final double d = 0.85;
    public static long MAX_ITER = 10000;

    public Pagerank(){
        inlinksMap = new HashMap<String, Set<String>>();
        outlinksMap = new HashMap<String, Set<String>>();
        prTable = new HashMap<String, Double>();
    }

    public void loadInlinks(String file) {
        try {
            File f = new File(file);
            FileInputStream fis = new FileInputStream(f);
            BufferedReader br = new BufferedReader(new InputStreamReader(fis));
            String line = br.readLine();
            while(line != null){
                boolean headOfLine = true;
                String nodeId = "";
                String[] ids = line.split(" ");
                for(String id : ids){
                    if(headOfLine){
                        nodeId = id;
                        headOfLine = false;
                        prTable.put(id, 1.0);
                    } else {
                        if(!inlinksMap.containsKey(nodeId)){
                            inlinksMap.put(nodeId,new HashSet<String>());
                        }
                        inlinksMap.get(nodeId).add(id);
                        if(!outlinksMap.containsKey(id)){
                            outlinksMap.put(id,new HashSet<String>());
                        }
                        outlinksMap.get(id).add(nodeId);
                    }
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

    public void pagerank() {
        int iterations = 0;
        int update = 1;
        while(iterations < MAX_ITER && update > 0) {
            update = 0;
            for (String node : prTable.keySet()) {
                double pr = 0.0;
                Set<String> inlinks = inlinksMap.get(node);
                if (inlinks != null) {
                    for (String in : inlinks) {
                        pr += prTable.get(in) / outlinksMap.get(in).size();
                    }
                }
                pr = (1 - d) + d * pr;
                update += Math.abs(pr - prTable.get(node));
                prTable.put(node, pr);
            }
            iterations++;
        }
    }

    public void printPagerank(String file){
        // Sort the ranks
        PagerankComparator prc =  new PagerankComparator(prTable);
        TreeMap<String,Double> sorted = new TreeMap<String,Double>(prc);
        sorted.putAll(prTable);
        try {
            File f = new File(file);
            FileOutputStream fos = new FileOutputStream(f);
            BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(fos));
            for (String doc : sorted.keySet()) {
                bw.write(doc + "  \t" + prTable.get(doc)+"\n");
                //System.out.println(doc + "  \t" + prTable.get(doc));
            }
            bw.flush();
            bw.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args){
        String inlinks_file = "../../data/wt2g_inlinks.txt";
        Pagerank pr = new Pagerank();
        pr.loadInlinks(inlinks_file);
        pr.pagerank();
        String output_file = "../../data/pagerank.txt";
        pr.printPagerank(output_file);

    }

    public class PagerankComparator implements Comparator<String> {

        Map<String, Double> base;
        public PagerankComparator(Map<String, Double> base) {
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
