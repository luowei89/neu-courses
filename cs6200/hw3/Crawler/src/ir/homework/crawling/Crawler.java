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
public class Crawler {
    public static final String[] SEEDS = {
            "http://en.wikipedia.org/wiki/List_of_terrorist_incidents",
            "http://en.wikipedia.org/wiki/September_11_attacks",
            "http://en.wikipedia.org/wiki/American_Airlines_Flight_77",
            "http://en.wikipedia.org/wiki/World_Trade_Center",
            "http://en.wikipedia.org/wiki/Collapse_of_the_World_Trade_Center"
    };
    public static final String KEYWORD = "terrorism";
    public static final int MAX_DOCS = 500;

    private Frontier frontier;
    private Set<String> crawled;

    public Crawler(){
        frontier = new Frontier();
        for(String s : SEEDS){
            frontier.add(s);
        }
        crawled = new HashSet<String>();
    }

    public void crawl(){
        while(!frontier.empty() && crawled.size() < MAX_DOCS){
            String url = frontier.next();
            Set<String> newUrls = getLinksFromURL(url);
            if(newUrls != null) {
                System.out.println("Crawling "+url);
                for (String nu : newUrls) {
                    if(!crawled.contains(nu)) {
                        frontier.add(nu);
                    }
                }
                crawled.add(url);
            }
        }
        System.out.println("Documents crawled: " + crawled.size());
    }

    public static Set<String> getLinksFromURL(String url) {
        Set<String> urls = new HashSet<String>();
        try {
            Document doc = Jsoup.connect(url).get();
            if (!doc.html().contains(KEYWORD)) {
                // no need to crawl
                return null;
            }
            Elements newsHeadlines = doc.select("a[href]");
            for (Element link : newsHeadlines) {
                String linkURL = canonicalizeURL(link.attr("abs:href"));
                if(linkURL != null) {
                    urls.add(linkURL);
                }
            }

        } catch (IOException e) {
            // url could not be opened
            return null;
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

    public static void main(String[] args){
        Crawler crawler = new Crawler();
        crawler.crawl();
    }
}
