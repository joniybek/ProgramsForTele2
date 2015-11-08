package com.broadcastify.threads;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

import java.util.Stack;

public class BrowsingThread extends Thread {
    private Thread thread;
    private String commands;
    private String currentCommand;
    private String url;

    public BrowsingThread(String commands) {
        this.commands = commands;
        this.url = "google.com";
    }

    public void run() {
        synchronized (BrowserLock.CHROME_LOCK) {
            System.setProperty("webdriver.chrome.driver", "chromedriver/chromedriver.exe");
            WebDriver driver = new ChromeDriver();
            String[] commandsArray = commands.split("->>");
            Stack<WebElement> elementStack = new Stack<WebElement>();
            for (String command : commandsArray) {
                this.currentCommand = command;
                System.out.println("Performing command..." + command);
                if (command.startsWith("click(")) {
                    System.out.println("Clicking ... " + command);
                    String xpath = command.substring(6, command.length() - 1);
                    WebElement element = driver.findElement(By.xpath(xpath));
                    element.click();
                    elementStack.push(element);
                } else if (command.startsWith("write(")) {
                    System.out.println("Writing ... " + command);
                    String textToWrite = command.substring(6, command.length() - 1);
                    if (!elementStack.empty()) {
                        WebElement element = elementStack.pop();
                        element.sendKeys(textToWrite);
                    }
                } else if (command.startsWith("wait(")) {
                    System.out.println("Waiting ... " + command);
                    String secText = command.substring(5, command.length() - 1);
                    System.out.println(secText);
                    int sec = 1;
                    try {
                        sec = Integer.parseInt(secText);
                        Thread.sleep(sec * 1000);
                        System.out.println("Finished slepping ---");
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
                        System.out.println("Cannot execute, internal error");
                    }
                } else if (command.startsWith("play(")) {
                    String video = command.substring(5, command.length() - 1);
                    if ("" .equals(video)) {
                        video = "D4sBxMl_5wk";
                    }
                    String urlYoutube = "https://www.youtube.com/v/%s?rel=0&autoplay=1";
                    driver.get(String.format(urlYoutube, video));
                } else if (command.startsWith("goto(")) {
                    this.url = command.substring(5, command.length() - 1);
                    driver.get(url);
                } else {
                    System.out.println("Command not found");
                }

            }
        }
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
