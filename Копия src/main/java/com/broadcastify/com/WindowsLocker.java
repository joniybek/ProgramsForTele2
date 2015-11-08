package com.broadcastify.com;

import java.awt.*;
import java.awt.event.KeyEvent;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Calendar;
import java.util.Date;
import java.util.Properties;

public class WindowsLocker {

    public String getProperties(String string) {
        Properties properties = new Properties();
        InputStream input = null;
        try {
            input = new FileInputStream("../HackDayConfig/config.properties");
            properties.load(input);
        } catch (IOException ex) {
            ex.printStackTrace();
        } finally {
            if (input != null) {
                try {
                    input.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }

        }

        return properties.getProperty(string);

    }

    public boolean getCanBeLocked(){
        String canBeLocked = getProperties("canbelocked");
        return "1".equals(canBeLocked)?true:false;
    }

    public void lockComputer(){
        if (getCanBeLocked()){
            try {
                Robot robot =new Robot();
                robot.keyPress(KeyEvent.VK_WINDOWS);
                robot.keyPress(KeyEvent.VK_L);
                robot.keyRelease(KeyEvent.VK_WINDOWS);
                robot.keyRelease(KeyEvent.VK_L);
                Runtime.getRuntime().exec("cmd /c start lockWindows.bat");
            } catch (IOException e) {
                e.printStackTrace();
            } catch (AWTException e) {
                e.printStackTrace();
            }
        }
    }

    public long returnSleepingTime(){
        Calendar cal = Calendar.getInstance();
        cal.set(Calendar.HOUR_OF_DAY,14);
        cal.set(Calendar.MINUTE,38);
        cal.set(Calendar.SECOND,0);
        cal.set(Calendar.MILLISECOND,0);
        Date shouldBe = cal.getTime();
        Date now = new Date();
        return (shouldBe.getTime()-now.getTime())*24*60;
    }
}
