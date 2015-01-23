package ir.homework.elasticsearch;

import java.io.*;
import java.util.List;
import java.util.ArrayList;
import org.elasticsearch.common.xcontent.XContentBuilder;
import org.elasticsearch.common.xcontent.XContentFactory;

public class FileParser {
    public static List<XContentBuilder> parse(File file){
        List<XContentBuilder> builders = new ArrayList<XContentBuilder>();
        try {
            FileInputStream fis = new FileInputStream(file);
            BufferedReader br = new BufferedReader(new InputStreamReader(fis));
            String line = br.readLine();
            String id = null;
            String text = null;
            Boolean texting = false;
            while (line != null) {
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
}
