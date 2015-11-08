package com.broadcastify.tasks;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;


public class BrowsingTask {
    private String commands;
    private Date start;
    private long duration;

    public BrowsingTask(String commands, String start, long duration) {
        this.commands = commands;
        this.duration = duration;
        this.start = parseDate(start);
    }

    public Date parseDate(String text) {
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy.MM.dd HH:mm:ss");
        try {
            return formatter.parse(text);
        } catch (ParseException e) {
            e.printStackTrace();
            Calendar cal = Calendar.getInstance(); // creates calendar
            cal.setTime(new Date()); // sets calendar time/date
            cal.add(Calendar.HOUR_OF_DAY, 3); // adds one hour
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
}
