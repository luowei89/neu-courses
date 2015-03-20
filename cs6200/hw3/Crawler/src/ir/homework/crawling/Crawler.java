package ir.homework.crawling;

import java.io.IOException;
import java.util.HashSet;
import java.util.Set;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 3/18/15.
 */
public class Crawler {

    public static final String[] KEYWORDS = {"September 11","terror"}; // 9/11 terrorism terrorist
    public static final int MAX_DOCS = 30000;
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
    private Indexer indexer;
    private Set<String> crawled;

    public Crawler(){
        frontier = new Frontier();
        indexer = new Indexer();
        for(String s : SEEDS){
            frontier.add(s,null);
        }
        crawled = new HashSet<String>();
    }

    public void crawl(){
        while(!frontier.empty() && crawled.size() < MAX_DOCS){
            long startTime = System.currentTimeMillis();
            String url = frontier.next();
            Set<String> inlinks = frontier.getInlinks(url);
            Set<String> newUrls = crawlAndIndex(url,inlinks);
            if(newUrls != null && newUrls.size() > 0) {
                crawled.add(url);
                System.out.println("Crawling "+crawled.size()+"\t\t"+url);
                for (String nu : newUrls) {
                    if(!crawled.contains(nu)) {
                        frontier.add(nu,url);
                    } else {
                        indexer.updateInlinks(nu, url);
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

    protected Set<String> crawlAndIndex(String url,Set<String> inlinks) {
        ESElement ese;
        try {
            ese = new ESElement(url, inlinks);
            indexer.buildIndex(ese);
        } catch (IOException e) {
            // url could not be opened
            return null;
        }
        return ese.getOutlinks();
    }

    public void closeConnections() {
        indexer.close();
    }

    public static void main(String[] args){
        Crawler crawler = new Crawler();
        crawler.crawl();
        crawler.closeConnections();
    }
}
