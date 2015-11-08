package com.broadcastify.db;


import com.broadcastify.tasks.BrowsingTask;

import java.sql.*;

public class DBUtils {
    private Connection mysqlConnection;

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
            this.mysqlConnection = DriverManager.getConnection("jdbc:mysql://localhost:3306/mkyongcom", "root", "password");

        } catch (SQLException e) {
            System.out.println("Connection Failed! Check output console");
            e.printStackTrace();
            return;
        }
    }


    public BrowsingTask getTasks() {

        Statement statement = null;
        ResultSet resultSet = null;
        BrowsingTask browsingTask = null;
        try {
            statement = mysqlConnection.createStatement();
            resultSet = statement.executeQuery("SELECT VERSION()");
            while (resultSet.next()) {
                browsingTask = new BrowsingTask(resultSet.getString(1), resultSet.getString(2), resultSet.getLong(2));
                resultSet = statement.executeQuery("SELECT VERSION()");
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }
        return browsingTask;
    }
}
