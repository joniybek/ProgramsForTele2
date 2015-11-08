package com.broadcastify.db;


import com.broadcastify.tasks.BrowsingTask;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;

public class DBUtils {
    private Connection mysqlConnection;
    private long pollingEverySec;

    public DBUtils(long pollingEverySec) {
        this.pollingEverySec = pollingEverySec;
    }

    public void initialise() {
        try {
            Class.forName("com.mysql.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            System.out.println("Where is your MySQL JDBC Driver?");
            e.printStackTrace();
            return;
        }

        this.mysqlConnection = null;

        try {
            this.mysqlConnection = DriverManager.getConnection(
                    "jdbc:mysql://localhost:3306/hackDay",
                    "root",
                    "");

        } catch (SQLException e) {
            System.out.println("Connection Failed! Check output console");
            e.printStackTrace();
            return;
        }
    }

    public boolean isConnectionAlive() {
        return mysqlConnection != null ? true : false;
    }

    public void startAddingToQueue(final ConcurrentHashMap<Long, BrowsingTask> queue) {

        Thread dbThread = new Thread() {
            public void run() {
                while (true) {
                    try {
                        List<BrowsingTask> browsingTasks = getTasks();
                        for (int i = 0; i < browsingTasks.size(); i++) {
                            queue.putIfAbsent(browsingTasks.get(i).getId(), browsingTasks.get(i));
                        }
                        Thread.sleep(pollingEverySec * 1000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }

            }
        };
        dbThread.start();


    }


    public List<BrowsingTask> getTasks() {

        Statement statement = null;
        ResultSet resultSet = null;
        List<BrowsingTask> list = new ArrayList<BrowsingTask>();
        try {
            statement = mysqlConnection.createStatement();
            resultSet = statement.executeQuery("SELECT commands, start,duration, isonetimetask, id from tasks order by start");
            while (resultSet.next()) {
                BrowsingTask browsingTask = null;
                browsingTask = new BrowsingTask(
                        resultSet.getString(1),
                        resultSet.getString(2),
                        resultSet.getLong(3),
                        resultSet.getInt(4),
                        resultSet.getLong(5));
                list.add(browsingTask);

            }

        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            try {
                statement.close();
                resultSet.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
        return list;
    }
}
