package ir.homework.elasticsearch;

import java.io.*;
import java.util.ArrayList;
import java.util.List;
import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.client.Client;
import org.elasticsearch.common.xcontent.XContentBuilder;
import org.elasticsearch.common.xcontent.XContentFactory;
import org.elasticsearch.node.Node;
import org.elasticsearch.node.NodeBuilder;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 1/21/15.
 */
public class IndexBuilder {

    private static int id = 1;

    public static void buildIndex(List<XContentBuilder> builders, Client client){
        for (XContentBuilder builder : builders) {
            System.out.println("ID: " + id);
            IndexResponse response = client.prepareIndex("ap_dataset", "document", ""+id)
                    .setSource(builder)
                    .execute()
                    .actionGet();
            ++id;
        }
    }

    public static List<XContentBuilder> parseDocuments(File file){
        List<XContentBuilder> builders = new ArrayList<XContentBuilder>();
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
                    id = line.substring(7,line.length()-8);
                } else if (line.startsWith("<TEXT>")) {
                    texting = true;
                } else if (line.startsWith("</TEXT>")) {
                    texting = false;
                } else if (line.startsWith("</DOC>")) {
                    XContentBuilder builder = XContentFactory.jsonBuilder()
                            .startObject()
                            .field("docno", id)
                            .field("text", text)
                            .endObject();
                    builders.add(builder);
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
        return builders;
    }

    public static void main(String[] args){
        File folder = new File("../../dataset/AP_DATA/ap89_collection/");
        File[] listOfFiles = folder.listFiles();

        Node node = NodeBuilder.nodeBuilder().node();
        Client client = node.client();

        for (File file : listOfFiles){
            buildIndex(parseDocuments(file), client);
        }
        node.close();
    }
}
