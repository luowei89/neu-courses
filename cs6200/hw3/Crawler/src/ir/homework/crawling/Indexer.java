package ir.homework.crawling;

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
    ConcurrentLinkedQueue<Runnable> taskQueue;
    private boolean running;

    public Indexer(){
        id = 1;
        node = NodeBuilder.nodeBuilder().node();
        client = node.client();
        docIdMap = new HashMap<String, Integer>();
        taskQueue = new ConcurrentLinkedQueue<Runnable>();
        running = true;
    }

    public void startIndexer(){
        this.start();
    }

    public void stopIndexer(){
        running = false;
        node.close();
        try {
            this.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public void buildIndex(ESElement ese){
        Runnable task = new IndexTask(ese);
        taskQueue.add(task);
    }

    public void updateInlinks(String url, String inlink) {
        Runnable task = new UpdateTask(url,inlink);
        taskQueue.add(task);
    }

    @Override
    public void run() {
        Runnable task = taskQueue.poll();
        while (running || task != null) {
            if (task != null){
                task.run();
            }
            task = taskQueue.poll();
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
            client.prepareIndex("crawler_data_1", "document", ""+id)
                    .setSource(builder)
                    .execute()
                    .actionGet();
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
            client.prepareUpdate("crawler_data_1","document",""+docIdMap.get(url))
                    .addScriptParam("new_inlink", inlink)
                    .setScript("ctx._source.inlinks += new_inlink", ScriptService.ScriptType.INLINE)
                    .execute()
                    .actionGet();
        }
    }
}
