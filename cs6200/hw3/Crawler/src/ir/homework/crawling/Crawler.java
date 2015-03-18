package ir.homework.crawling;

/**
 * Information Retrieval Homework
 * Created by Wei Luo on 3/18/15.
 */
public class Crawler {
    private static final String[] seeds = {
            "http://en.wikipedia.org/wiki/List_of_terrorist_incidents",
            "http://en.wikipedia.org/wiki/September_11_attacks",
            "http://en.wikipedia.org/wiki/American_Airlines_Flight_77",
            "http://en.wikipedia.org/wiki/World_Trade_Center",
            "http://en.wikipedia.org/wiki/Collapse_of_the_World_Trade_Center"
    };

    public static void main(String[] args){
        for(String s : seeds) {
            System.out.println(s);
        }
    }
}
