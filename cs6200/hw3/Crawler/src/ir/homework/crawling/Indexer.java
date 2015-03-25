package ir.homework.crawling;

import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.client.Client;
import org.elasticsearch.common.xcontent.XContentBuilder;
import org.elasticsearch.node.Node;
import org.elasticsearch.node.NodeBuilder;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;
import java.util.concurrent.ConcurrentLinkedQueue;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 3/19/15.
 */
public class Indexer extends Thread {

    private Node node;
    private Client client;
    private HashMap<String,Integer> docIdMap;
    private ConcurrentLinkedQueue<Runnable> indexTaskQueue;
    private boolean crawling;
    // for updating inlinks and outlinks
    private ConcurrentLinkedQueue<String> docs;
    private HashMap<String,Set<String>> inlinksMap;
    private HashMap<String,Set<String>> outlinksMap;
    // indexing and updating threads
    private IndexThread[] indexThreads;
    private UpdateThread[] updateThreads;

    public Indexer(){
        node = NodeBuilder.nodeBuilder().node();
        client = node.client();
        docIdMap = new HashMap<String, Integer>();
        indexTaskQueue = new ConcurrentLinkedQueue<Runnable>();
        crawling = true;

        docs = new ConcurrentLinkedQueue<String>();
        inlinksMap = new HashMap<String, Set<String>>();
        outlinksMap = new HashMap<String, Set<String>>();

        indexThreads = new IndexThread[2];
        updateThreads = new UpdateThread[10];
    }

    public void startIndexer(){
        for(int i = 0; i < indexThreads.length; i++){
            indexThreads[i] = new IndexThread();
            indexThreads[i].start();
        }
    }

    public void updateLinks(){
        try {
            crawling = false;
            // wait for indexing
            for(int i = 0; i < indexThreads.length; i++){
                indexThreads[i].join();
            }
            // start update threads
            for(int i = 0; i < updateThreads.length; i++){
                updateThreads[i] = new UpdateThread();
                updateThreads[i].start();
            }
            // wait for update threads to finish
            for(int i = 0; i < updateThreads.length; i++){
                updateThreads[i].join();
            }
            node.close();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public void buildIndex(int id, ESElement ese){
        Runnable task = new IndexTask(id,ese);
        indexTaskQueue.add(task);
    }

    public void addLink(String to, String from) {
        Set<String> inlinks;
        if(inlinksMap.containsKey(to)){
            inlinks = inlinksMap.get(to);
        } else {
            inlinks = new HashSet<String>();
        }
        inlinks.add(from);
        inlinksMap.put(to,inlinks);
        Set<String> outlinks;
        if(inlinksMap.containsKey(from)){
            outlinks = inlinksMap.get(from);
        } else {
            outlinks = new HashSet<String>();
        }
        outlinks.add(to);
        outlinksMap.put(from,outlinks);
    }

    public void removeLink(String url) {
        Set<String> inlinks = inlinksMap.get(url);
        if(inlinks != null) {
            for (String in : inlinks) {
                outlinksMap.get(in).remove(url);
            }
        }
        inlinksMap.remove(url);
    }

    private class IndexThread extends Thread {

        @Override
        public void run() {
            Runnable task = indexTaskQueue.poll();
            while (crawling || task != null) {
                if (task != null){
                    task.run();
                }
                task = indexTaskQueue.poll();
            }
        }
    }

    private class IndexTask implements Runnable {

        private Integer docId;
        private ESElement ese;

        public IndexTask(int id,ESElement e){
            docId = id;
            ese = e;
        }

        @Override
        public void run() {
            XContentBuilder builder = ese.getBuilder();
            System.out.println("Indexing " + docId + "\t" + ese.getId());
            IndexResponse response = null;
            while(response == null || !response.getId().equals(ese.getId())){
                // ensure success index creation
                response = client.prepareIndex("crawler_data", "document", ese.getId())
                        .setSource(builder)
                        .execute()
                        .actionGet();
            }
            docIdMap.put(ese.getId(),docId);
            docs.add(ese.getId());
        }
    }

    private class UpdateThread extends Thread {

        @Override
        public void run() {
            String doc = docs.poll();
            while(doc != null){
                System.out.println("Updating " + docIdMap.get(doc) + "\t" + doc);
                HashMap<String, Object> updateObject = new HashMap<String, Object>();
                updateObject.put("inlinks",inlinksMap.get(doc));
                updateObject.put("outlinks",outlinksMap.get(doc));
                client.prepareUpdate("crawler_data", "document", "" + doc)
                        .setDoc(updateObject)
                        .execute()
                        .actionGet();
                doc = docs.poll();
            }
        }
    }
}
