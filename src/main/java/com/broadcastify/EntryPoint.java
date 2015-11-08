package com.broadcastify;

import com.broadcastify.com.WindowsLocker;
import com.broadcastify.db.DBUtils;
import com.broadcastify.tasks.BrowsingTask;
import com.broadcastify.threads.BrowsingRunner;

import java.util.Calendar;
import java.util.Date;
import java.util.Iterator;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.ExecutionException;

public class EntryPoint {
    final static long CHECK_STARTTIME_POLLING_EVERY_SEC = 1;
    final static int EXIT_AT_OCLOCK = 23;
    final static long FETCH_DB_POLLING_EVERY_SEC = 1;
    final static int LOCK_AT_OCKLOCK = 19;

    public static void main(String[] args) throws ExecutionException, InterruptedException {
        final WindowsLocker windowsLocker = new WindowsLocker(LOCK_AT_OCKLOCK);
        windowsLocker.startLocker();
        ConcurrentHashMap<Long, BrowsingTask> concurrentHashMap = new ConcurrentHashMap<Long, BrowsingTask>();
        final DBUtils db = new DBUtils(FETCH_DB_POLLING_EVERY_SEC);
        db.initialise();
        db.startAddingToQueue(concurrentHashMap);
        while (!isTimeToExit()) {
            System.out.println("[Main] size=" + concurrentHashMap.size());
            BrowsingRunner runner = new BrowsingRunner();
            for (Map.Entry<Long, BrowsingTask> entry : concurrentHashMap.entrySet()) {
                BrowsingTask browsingTask = entry.getValue();
                Long key = entry.getKey();
                Date now = new Date();
                System.out.println("[Main] current time: " + now);
                if (now.after(browsingTask.getStart()) && canBeFinished(browsingTask)) {
                    runner.doBrowsing(browsingTask);
                    concurrentHashMap.remove(key);
                }

            }
            Thread.sleep(CHECK_STARTTIME_POLLING_EVERY_SEC * 1000);
        }

        System.exit(10);
    }

    public static boolean isTimeToExit() {
        Calendar cal = Calendar.getInstance();
        cal.set(Calendar.HOUR_OF_DAY, EXIT_AT_OCLOCK);
        cal.set(Calendar.MINUTE, 0);
        Date timeToExit = cal.getTime();
        Date now = new Date();
        if (now.after(timeToExit)) {
            return true;
        } else {
            return false;
        }
    }

    public static boolean canBeFinished(BrowsingTask browsingTask) {
        Date now = new Date();
        Date shouldEnd = new Date(browsingTask.getStart().getTime() + browsingTask.getDuration() * 60000);
        if (now.before(shouldEnd)) {
            return true;
        } else {
            System.out.println("[Main] Task " + browsingTask.getId() + " cannot be finished");
            return false;
        }
    }

}
