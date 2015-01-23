package ir.homework.elasticsearch;

import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.client.Client;
import org.elasticsearch.common.xcontent.XContentBuilder;

import java.util.List;

public class IndexBuilder {
    private static int id = 1;
    public static void build(List<XContentBuilder> builders, Client client){
        for (XContentBuilder builder : builders) {
            System.out.println("ID: " + id);
            IndexResponse response = client.prepareIndex("ap_dataset", "document", ""+id)
                    .setSource(builder)
                    .execute()
                    .actionGet();
            ++id;
        }
    }
}
