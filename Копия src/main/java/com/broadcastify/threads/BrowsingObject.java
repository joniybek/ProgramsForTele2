package com.broadcastify.threads;

import java.util.Date;

public class BrowsingObject {
    private BrowsingThread browsingThread;
    private long duration;
    private Date start;

    public BrowsingObject(BrowsingThread browsingThread,Date start, long duration) {
        this.browsingThread = browsingThread;
        this.duration = duration;
        this.start= start;
    }

    public BrowsingThread getBrowsingThread() {
        return browsingThread;
    }

    public long getDuration() {
        return duration;
    }
    public Date getStart() {
        return start;
    }

}
