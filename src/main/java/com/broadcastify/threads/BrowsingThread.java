package com.broadcastify.threads;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

import java.awt.*;
import java.awt.event.KeyEvent;
import java.util.Date;
import java.util.Stack;

public class BrowsingThread extends Thread {
    private Thread thread;
    private String commands;
    private String currentCommand;
    private String url;
    private WebDriver driver;
    public static int count=0;

    public BrowsingThread(String commands) {
        this.commands = commands;
        count++;
        this.url = "https://www.google.lv";
    }

    public void run() {
             System.out.println("[Browsing thread] Running Chrome");
                System.setProperty("webdriver.chrome.driver", "chromedriver/chromedriver.exe");
                driver = new ChromeDriver();
                Robot robot = null;
                try {
                    System.out.println("trying to max");
                    robot = new Robot();
                    //robot.keyPress(KeyEvent.VK_F11);
                    //robot.keyRelease(KeyEvent.VK_F11);
                } catch (AWTException e) {
                    e.printStackTrace();
                }

                String[] commandsArray = commands.split("->>");
                Stack<WebElement> elementStack = new Stack<WebElement>();
                for (String command : commandsArray) {
                    this.currentCommand = command;
                    System.out.println("[Chrome] Performing command..." + command);
                    if (command.startsWith("click(")) {
                        System.out.println("[Chrome] Clicking ... " + command);
                        String xpath = command.substring(6, command.length() - 1);
                        WebElement element = driver.findElement(By.xpath(xpath));
                        element.click();
                        elementStack.push(element);
                    } else if (command.startsWith("write(")) {
                        System.out.println("[Chrome] Writing ... " + command);
                        String textToWrite = command.substring(6, command.length() - 1);
                        if (!elementStack.empty()) {
                            WebElement element = elementStack.pop();
                            element.sendKeys(textToWrite);
                        }
                    } else if (command.startsWith("wait(")) {
                        System.out.println("[Chrome] Waiting ... " + command);
                        String secText = command.substring(5, command.length() - 1);
                        int sec = 1;
                        try {
                            sec = Integer.parseInt(secText);
                            Thread.sleep(sec * 1000);
                            System.out.println("[Chrome] Finished sleeping");
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    } else if (command.startsWith("refresh(")) {
                        driver.navigate().refresh();
                    } else if (command.startsWith("execute(")) {
                        String jsCommand = command.substring(8, command.length() - 1);
                        if (driver instanceof JavascriptExecutor) {
                            ((JavascriptExecutor) driver).executeScript(jsCommand);
                        } else {
                            System.out.println("[Chrome] Cannot execute, internal error");
                        }
                    } else if (command.startsWith("play(")) {
                        System.out.println("[Chrome] Playing video ");
                        String video = command.substring(5, command.length() - 1);
                        if ("".equals(video)) {
                            video = "D4sBxMl_5wk";
                        }
                        String urlYoutube = "https://www.youtube.com/v/%s?rel=0&autoplay=1";
                        driver.get(String.format(urlYoutube, video));
                    } else if (command.startsWith("goto(")) {
                        this.url = command.substring(5, command.length() - 1);
                        System.out.println(url);
                        driver.get(url);
                    } else {
                        System.out.println("[Chrome] Command not found");
                    }

                }

    }

    public void cancel(){
        System.out.println("starting interruption");
        thread.interrupt();
    }

    public void closeBrowser(){
        driver.close();
        driver.quit();
    }

    public String getCurrentCommand() {
        return this.currentCommand;
    }

    public void start() {
        if (this.thread == null) {
            this.thread = new Thread(this, "browsing");
            this.thread.start();
        }
    }


}
