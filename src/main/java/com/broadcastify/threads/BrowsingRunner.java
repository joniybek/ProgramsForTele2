package com.broadcastify.threads;

import com.broadcastify.tasks.BrowsingTask;

public class BrowsingRunner {

    public void doBrowsing(BrowsingTask browsingTask) {

        BrowsingThread thread = new BrowsingThread(browsingTask.getCommands());
        thread.start();
        System.out.println("[Runner] Running browsing task:"+browsingTask.getId()+", duration: "+browsingTask.getDuration());
        try {
            Thread.sleep(browsingTask.getDuration() * 1000 * 60);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        thread.closeBrowser();
        thread.cancel();
    }

}


