package ir.homework.crawling;

import crawlercommons.robots.BaseRobotRules;
import crawlercommons.robots.SimpleRobotRules;
import crawlercommons.robots.SimpleRobotRulesParser;
import org.apache.commons.io.IOUtils;

import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 3/18/15.
 */
public class Crawler {

    public static final String KEYWORD = "terror"; // 9/11 terrorism terrorist
    public static final int MAX_DOCS = 12000;
    public static final long POLITENESS = 1000;
    public static final String[] SEEDS = {
            "http://september11.archive.org/",
            "http://pentagon.spacelist.org/",
            "http://www.911research.wtc7.net/",
            "http://www.history.com/topics/9-11-attacks",
            "http://www.cnn.com/2013/07/27/us/september-11-anniversary-fast-facts/",
            "http://en.wikipedia.org/wiki/September_11_attacks",
            "http://en.wikipedia.org/wiki/Collapse_of_the_World_Trade_Center",
            "http://en.wikipedia.org/wiki/American_Airlines_Flight_77",
            "http://en.wikipedia.org/wiki/List_of_terrorist_incidents",
            "http://en.wikipedia.org/wiki/The_Pentagon"
    };

    private Frontier frontier;
    private Indexer indexer;
    private Set<String> crawled;
    private HashMap<String,Long> domianVisited;
    private HashMap<String,BaseRobotRules> domianRules;

    public Crawler(){
        frontier = new Frontier();
        indexer = new Indexer();
        for(String s : SEEDS){
            frontier.add(s);
        }
        crawled = new HashSet<String>();
        domianVisited = new HashMap<String, Long>();
        domianRules = new HashMap<String, BaseRobotRules>();
    }

    public void crawl(){
        while (!frontier.empty() && crawled.size() < MAX_DOCS) {
            String url = frontier.next();
            String domain = getDomainName(url);
            BaseRobotRules rules;
            if(domianVisited.containsKey(domain)) {
                Long timeFromLastVisited = System.currentTimeMillis() - domianVisited.get(domain);
                if (timeFromLastVisited < POLITENESS) {
                    try {
                        Thread.sleep(POLITENESS - timeFromLastVisited);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
                rules = domianRules.get(domain);
            } else {
                rules = findRobotsRules(domain);
            }
            try {
                if(!rules.isAllowed(url)){
                    continue;
                }
                ESElement ese = new ESElement(url);
                domianVisited.put(domain, System.currentTimeMillis());
                Set<String> newUrls = ese.getOutlinks();
                if (newUrls.size() > 0) {
                    crawled.add(url);
                    indexer.buildIndex(crawled.size(),ese);
                    System.out.println("Crawling " + crawled.size() + "\t" + url);
                    for (String nu : newUrls) {
                        if (!crawled.contains(nu)) {
                            frontier.add(nu);
                        }
                        indexer.addLink(nu,url);
                    }
                }
                //}
            } catch (Exception e) {
                // failed analyze url continue to next
                indexer.removeLink(url);
                // e.printStackTrace();
            }
        }
        System.out.println("Documents crawled: " + crawled.size());
    }

    private BaseRobotRules findRobotsRules(String domain) {
        BaseRobotRules rules = null;
        try {
            InputStream robotsStream = new URL("http://"+domain+"/robots.txt").openStream();
            SimpleRobotRulesParser srrParser = new SimpleRobotRulesParser();
            rules = srrParser.parseContent("http://"+domain,
                    IOUtils.toByteArray(robotsStream),"text/plain","Googlebot");
            domianRules.put(domain, rules);
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if(rules == null){
                rules = new SimpleRobotRules(SimpleRobotRules.RobotRulesMode.ALLOW_ALL);
            }
        }
        return rules;
    }

    private String getDomainName(String url) {
        String host = "";
        try {
            URL netUrl = new URL(url);
            host = netUrl.getHost();
            if (host.startsWith("www")) {
                host = host.substring("www".length() + 1);
            }
        } catch (MalformedURLException e) {
            e.printStackTrace();
        }
        return host;
    }

    public void startIndexer() {
        indexer.startIndexer();
    }

    public void stopIndexer() {
        indexer.updateLinks();
    }

    public static void main(String[] args){
        long startTime = System.currentTimeMillis();
        Crawler crawler = new Crawler();
        crawler.startIndexer();
        crawler.crawl();
        System.out.println(" -- Time used " +(System.currentTimeMillis()-startTime)/3600000.0+" hours.");
        crawler.stopIndexer();
        System.out.println(" -- Total time used " +(System.currentTimeMillis()-startTime)/3600000.0+" hours.");
    }
}
