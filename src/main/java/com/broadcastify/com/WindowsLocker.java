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
    private int lockAt;

    public WindowsLocker(int lockAt) {
        this.lockAt = lockAt;
    }

    public String getProperties(String string, String defaultProperty) {
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
        String property = properties.getProperty(string);
        return "".equals(property) ? defaultProperty : property;

    }

    public boolean getCanBeLocked() {
        String canBeLocked = getProperties("canbelocked", "");
        return "1".equals(canBeLocked) ? true : false;
    }

    public void startLocker() {
        Thread lockerThread = new Thread() {
            public void run() {
                while (!isTimeToLock()) {

                    try {

                        Thread.sleep(1 * 60 * 1000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }
                lockComputer();

            }
        };
        lockerThread.start();
    }

    public void lockComputer() {
        if (getCanBeLocked()) {
            try {
                Robot robot = new Robot();
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

    public boolean isTimeToLock() {
        Calendar cal = Calendar.getInstance();
        cal.set(Calendar.HOUR_OF_DAY, lockAt);
        cal.set(Calendar.MINUTE, 0);
        Date timeToExit = cal.getTime();
        Date now = new Date();
        if (now.after(timeToExit)) {
            return true;
        } else {
            return false;
        }
    }
}
