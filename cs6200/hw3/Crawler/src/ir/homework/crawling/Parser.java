package ir.homework.crawling;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.HashSet;
import java.util.Set;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 3/18/15.
 */
public class Parser {

    public static Set<String> parse(String url){
        Set<String> urls = new HashSet<String>();
        try {
            Document doc = Jsoup.connect(url).get();
            Elements newsHeadlines = doc.select("a[href]");
            for(Element link : newsHeadlines){
                String linkURL = link.attr("abs:href");
                urls.add(canonicalizeURL(linkURL));
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
        return urls;
    }

    private static String canonicalizeURL(String url){
        try {
            URL curl = new URL(url);
            // Convert the scheme and host to lower case
            String protocol = curl.getProtocol().toLowerCase();
            String host = curl.getHost().toLowerCase();
            // Remove port 80 from http URLs, and port 443 from HTTPS URLs
            int port = curl.getPort();
            if (port == curl.getDefaultPort()) {
                port = -1;
            }
            String path = curl.getPath();
            path = new URI(path).normalize().toString();
            // Remove duplicate slashes
            while(path.contains("//")){
                path = path.replace("//","/");
            }
            path = path.trim();
            url = new URL(protocol, host, port, path).toString();
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (URISyntaxException e) {
            e.printStackTrace();
        }
        return url;
    }

    public static void main(String[] args){
        System.out.println(canonicalizeURL("HTTP://www.Example.com/SomeFile.html"));
        System.out.println(canonicalizeURL("http://www.example.com:80"));
        System.out.println(canonicalizeURL("http://www.example.com/a.html#anything"));
        System.out.println(canonicalizeURL("http://www.example.com//a.html"));
    }
}
