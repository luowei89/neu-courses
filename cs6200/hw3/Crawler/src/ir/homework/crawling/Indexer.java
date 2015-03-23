package ir.homework.crawling;

import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.client.Client;
import org.elasticsearch.common.xcontent.XContentBuilder;
import org.elasticsearch.node.Node;
import org.elasticsearch.node.NodeBuilder;
import org.elasticsearch.script.ScriptService;

import java.util.HashMap;
import java.util.concurrent.ConcurrentLinkedQueue;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 3/19/15.
 */
public class Indexer extends Thread {
    private static int id;
    private Node node;
    private Client client;
    private HashMap<String,Integer> docIdMap;
    private ConcurrentLinkedQueue<Runnable> indexTaskQueue;
    private ConcurrentLinkedQueue<Runnable> updateTaskQueue;
    private boolean running;
    private IndexerThread[] its;

    private static Object lock = new Object();

    public Indexer(){
        id = 1;
        node = NodeBuilder.nodeBuilder().node();
        client = node.client();
        docIdMap = new HashMap<String, Integer>();
        indexTaskQueue = new ConcurrentLinkedQueue<Runnable>();
        updateTaskQueue = new ConcurrentLinkedQueue<Runnable>();
        running = true;
        its = new IndexerThread[10];
    }

    public void startIndexer(){
        for(int i = 0; i < its.length; i++){
            its[i] = new IndexerThread();
            its[i].start();
        }
    }

    public void stopIndexer(){
        running = false;
        try {
            for(int i = 0; i < its.length; i++){
                its[i].join();
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        node.close();
    }

    public void buildIndex(ESElement ese){
        Runnable task = new IndexTask(ese);
        indexTaskQueue.add(task);
    }

    public void updateInlinks(String url, String inlink) {
        Runnable task = new UpdateTask(url,inlink);
        updateTaskQueue.add(task);
    }

    private class IndexerThread extends Thread {

        @Override
        public void run() {
            Runnable task = indexTaskQueue.poll();
            if(task == null){
                task = updateTaskQueue.poll();
            }
            while (running || task != null) {
                if (task != null){
                    task.run();
                }
                task = indexTaskQueue.poll();
                if(task == null){
                    task = updateTaskQueue.poll();
                }
            }
        }
    }

    private class IndexTask implements Runnable {

        private ESElement ese;

        public IndexTask(ESElement e){
            ese = e;
        }

        @Override
        public void run() {

            XContentBuilder builder = ese.getBuilder();
            //System.out.println("--Indexing " + id + "\t" + ese.getId());
            IndexResponse response = null;
            while(response == null || !response.getId().equals(""+id)){
                // ensure success index creation
                if(response != null) {
                    System.out.println(" -- Failed " + id);
                }
                response = client.prepareIndex("crawler_data", "document", "" + id)
                        .setSource(builder)
                        .execute()
                        .actionGet();
            }
            docIdMap.put(ese.getId(),id);
            id++;
        }
    }

    private class UpdateTask implements Runnable {

        private String url;
        private String inlink;

        public UpdateTask(String u,String in){
            url = u;
            inlink = in;
        }

        @Override
        public void run() {
            if(docIdMap.containsKey(url)) {
                synchronized (lock) {
                    //System.out.println("----Updating " + docIdMap.get(url) + "\t" + url);
                    client.prepareUpdate("crawler_data", "document", "" + docIdMap.get(url))
                            .addScriptParam("new_inlink", inlink)
                            .setScript("ctx._source.inlinks += new_inlink", ScriptService.ScriptType.INLINE)
                            .execute()
                            .actionGet();
                }
            } else {
                // got executed before the index creation, put the task back to task queue
                updateTaskQueue.add(this);
            }
        }
    }
}
