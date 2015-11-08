package com.broadcastify.threads;

import java.util.Date;
import java.util.Queue;

public class BrowsingRunner {
    private static BrowsingRunner instance =null;
    private Queue<BrowsingObject> browsingObjectQueue;
    protected BrowsingRunner() { }
    public BrowsingRunner getInstance(){
        if (instance==null){
            instance = new BrowsingRunner();
        }
        return instance;
    }

    public void addBrowsing(String commands, Date start, Long duration){
        browsingObjectQueue.add(new BrowsingObject(new BrowsingThread(commands),start,duration));

    }
    public void doBrowsing(){


    }
/*    synchronized(BrowserLock.CHROME_LOCK){


    }*/
}


