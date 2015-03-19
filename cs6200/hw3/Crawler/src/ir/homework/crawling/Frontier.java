package ir.homework.crawling;

import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.Set;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 3/18/15.
 */
public class Frontier {
    private HashMap<Integer,Set<String>> frontier;
    private HashMap<String,Integer> urlsMap;
    private int maxCount;

    public Frontier(){
        frontier = new HashMap<Integer, Set<String>>();
        urlsMap = new HashMap<String, Integer>();
        maxCount = 0;
    }

    // get the next url to be crawled in the frontier
    public String next(){
        if(empty()){
            return "Frontier Empty!";
        }
        Set<String> list = frontier.get(maxCount);
        if(list.size()==0){
            frontier.remove(maxCount);
            maxCount--;
            return next();
        }
        String next = list.iterator().next();
        urlsMap.remove(next);
        list.remove(next);
        if(list.size() == 0){
            frontier.remove(maxCount);
            maxCount--;
        } else {
            frontier.put(maxCount,list);
        }
        return next;
    }

    public boolean empty(){
        return maxCount == 0;
    }

    // add a new url to the frontier
    public void add(String url){
        int level = 0;
        Set<String> oldList;
        Set<String> newList;
        if(urlsMap.containsKey(url)){
            // get the level from frontier
            level = urlsMap.get(url);
        }
        if(level > 0){
            // remove it from old level list
            oldList = frontier.get(level);
            oldList.remove(url);
            frontier.put(level,oldList);
        }
        // get the new level list
        if(frontier.containsKey(level+1)){
            newList = frontier.get(level+1);
        } else {
            newList = new LinkedHashSet<String>();
            maxCount++;
        }
        // add it to the new level list
        newList.add(url);
        frontier.put(level+1,newList);
        // update its level
        urlsMap.put(url,level+1);
    }
}
