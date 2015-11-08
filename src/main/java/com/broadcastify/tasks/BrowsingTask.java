package com.broadcastify.tasks;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;


public class BrowsingTask {
    private String commands;
    private Date start;
    private long duration;
    private long id;

    public BrowsingTask(String commands, String start, long duration, int isonetimetask, long id) {
        this.commands = commands;
        this.duration = duration;
        this.id = id;
        if (isonetimetask == 0) {
            this.start = createNewDate(start);
        } else {
            this.start = parseDate(start);
        }
    }

    private Date createNewDate(String text) {
        Calendar today = Calendar.getInstance();
        today.set(Calendar.HOUR_OF_DAY, Integer.parseInt(text.substring(11, 13)));
        today.set(Calendar.MINUTE, Integer.parseInt(text.substring(14, 16)));
        today.set(Calendar.SECOND, Integer.parseInt(text.substring(17, 19)));
        return today.getTime();
    }

    public Date parseDate(String text) {
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        try {
            return formatter.parse(text.substring(0, 19));
        } catch (ParseException e) {
            e.printStackTrace();
            Calendar cal = Calendar.getInstance();
            cal.setTime(new Date());
            cal.add(Calendar.HOUR_OF_DAY, 3);
            return cal.getTime();
        }

    }

    public String getCommands() {
        return commands;
    }

    public Date getStart() {
        return start;
    }

    public long getDuration() {
        return duration;
    }

    public long getId() {
        return id;
    }

    public String toString() {
        return "Task: " + "\n" + "start: " + start + "\n duration: " + duration + "\n command: " + commands;
    }
}
