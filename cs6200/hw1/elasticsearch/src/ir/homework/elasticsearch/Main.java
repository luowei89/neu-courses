package ir.homework.elasticsearch;

import org.elasticsearch.client.Client;
import org.elasticsearch.node.Node;
import org.elasticsearch.node.NodeBuilder;

import java.io.File;

public class Main {

    public static void main(String[] args){
        File folder = new File("../../dataset/AP_DATA/ap89_collection/");
        File[] listOfFiles = folder.listFiles();

        Node node = NodeBuilder.nodeBuilder().node();
        Client client = node.client();

        for (File file : listOfFiles){
            IndexBuilder.build(FileParser.parse(file),client);
        }

        node.close();
    }
}
