package ir.homework.crawling;

import org.elasticsearch.common.xcontent.XContentBuilder;
import org.elasticsearch.common.xcontent.XContentFactory;
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
 * Created by Wei Luo on 3/19/15.
 */
public class ESElement {
    private String id; // canonical URL
    private String text; // cleaned text
    private String html; // raw html text
    private Set<String> inlinks; // inlinks list (canonical URLs)
    private Set<String> outlinks; // outlinks list (canonical URLs)

    public ESElement(String url) throws IOException {
        id = url;
        text = "";
        inlinks = new HashSet<String>();
        outlinks = new HashSet<String>();
        Document doc = Jsoup.connect(url).userAgent("Chrome").get();
        html = doc.html();
        if (!doc.html().contains(Crawler.KEYWORD)) {
            // no need to crawl
            throw new IOException();
        }
        Elements newsHeadlines = doc.select("div#content ul a[href],div#content p a[href]");
        if(newsHeadlines.size() == 0){
            newsHeadlines = doc.select("div.content ul a[href],div.content p a[href]");
        }
        if(newsHeadlines.size() == 0){
            newsHeadlines = doc.select("ul a[href],p a[href]");
        }
        for (Element link : newsHeadlines) {
            String linkURL = canonicalizeURL(link.attr("abs:href"));
            if(linkURL != null && !linkURL.endsWith(".png") && !linkURL.endsWith(".svg")) {
                outlinks.add(linkURL);
            }
        }
        Elements textElements = doc.select("div#content ul,div#content p");
        if(textElements.size() == 0){
            textElements = doc.select("div.content ul,div.content p");
        }
        if(textElements.size() == 0){
            textElements = doc.select("ul,p");
        }
        for (Element textElement : textElements) {
            text += textElement.text() + " ";
        }
    }

    protected String canonicalizeURL(String url){
        try {
            if(url.contains("mailto:") || url.contains("/wiki/Category:")){
                return null;
            }
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
            while (path.contains("//")) {
                path = path.replace("//", "/");
            }
            path = path.trim();
            url = new URL(protocol, host, port, path).toString();
        } catch (MalformedURLException e) {
            // url could not be parsed
            return null;
        } catch (URISyntaxException e) {
            // url could not be parsed
            return null;
        }
        return url;
    }

    public XContentBuilder getBuilder(){
        XContentBuilder builder = null;
        try {
            builder = XContentFactory.jsonBuilder()
                    .startObject()
                    .field("id", id)
                    .field("text", text)
                    .field("html", html)
                    .field("inlinks", inlinks)
                    .field("outlinks", outlinks)
                    .endObject();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return builder;
    }

    public Set<String> getOutlinks() {
        return outlinks;
    }
}
