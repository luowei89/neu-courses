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

    public static final String KEYWORD = "September 11"; // 9/11
    public static final int MAX_DOCS = 100;
    public static final long POLITENESS = 1000;
    public static final String[] SEEDS = {
            "http://september11.archive.org/",
            "http://pentagon.spacelist.org/",
            "http://www.911research.wtc7.net/",
            "http://en.wikipedia.org/wiki/September_11_attacks",
            "http://en.wikipedia.org/wiki/Collapse_of_the_World_Trade_Center",
            "http://en.wikipedia.org/wiki/United_Airlines_Flight_93",
            "http://en.wikipedia.org/wiki/American_Airlines_Flight_77",
            "http://en.wikipedia.org/wiki/List_of_terrorist_incidents",
            "http://en.wikipedia.org/wiki/The_Pentagon",
            "http://en.wikipedia.org/wiki/World_Trade_Center"
    };

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
            long startTime = System.currentTimeMillis();
            String url = frontier.next();
            Set<String> newUrls = getLinksFromURL(url);
            if(newUrls != null && newUrls.size() > 0) {
                System.out.println("Crawling "+url);
                crawled.add(url);
                for (String nu : newUrls) {
                    if(!crawled.contains(nu)) {
                        frontier.add(nu);
                    }
                }
            }
            // wait until 1 second to process next crawl (politeness policy)
            try {
                long crawlTime = System.currentTimeMillis() - startTime;
                if(crawlTime < POLITENESS){
                    Thread.sleep(POLITENESS-crawlTime);
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        System.out.println("Documents crawled: " + crawled.size());
    }

    protected Set<String> getLinksFromURL(String url) {
        Set<String> urls = new HashSet<String>();
        try {
            Document doc = Jsoup.connect(url).userAgent("Chrome").get();
            if (!doc.html().contains(KEYWORD)) {
                // no need to crawl
                return null;
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
                    urls.add(linkURL);
                }
            }
        } catch (IOException e) {
            // url could not be opened
            return null;
        }
        return urls;
    }

    protected String canonicalizeURL(String url){
        try {
            if(url.contains("mailto:") ||url.contains("/wiki/Category:")){
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

    public static void main(String[] args){
        Crawler crawler = new Crawler();
        crawler.crawl();
    }
}
