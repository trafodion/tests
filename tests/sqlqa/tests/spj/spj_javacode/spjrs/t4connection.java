// @@@ START COPYRIGHT @@@
//
// (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.
//
// @@@ END COPYRIGHT @@@

import java.io.File;
import java.io.FileInputStream;
import java.io.PrintStream;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Time;
import java.sql.Timestamp;
import java.util.Properties;
import java.util.logging.Level;
import java.util.logging.Logger;

public class t4connection
{
  static String url;
  static String usr;
  static String pwd;
  public static Properties props;

  static void checkprops()
    throws SQLException
  {
    if (props == null)
      throw new SQLException("Error: hpt4jdbc.properties is null. Exiting.");
  }

  public static Connection getUserConnection()
    throws SQLException
  {
    Connection localConnection = null;
    checkprops();

    Logger.global.log(Level.FINE, "DriverManager.getConnection(url, usr, pwd)");
    localConnection = DriverManager.getConnection(url, usr, pwd);
    Logger.global.log(Level.INFO, "DriverManager.getConnection(url, usr, pwd) passed");
    Logger.global.log(Level.FINE, "==============\n\n");

    return localConnection;
  }

  public static Connection getPropertiesConnection()
    throws SQLException
  {
    Connection localConnection = null;
    checkprops();

    localConnection = DriverManager.getConnection(url, props);

    Logger.global.log(Level.FINE, "==============\n\n");

    return localConnection;
  }

  public static Connection getUrlConnection()
    throws SQLException
  {
    Connection localConnection = null;
    checkprops();

    Logger.global.log(Level.FINE, "DriverManager.getConnection(url)");
    localConnection = DriverManager.getConnection(url);
    Logger.global.log(Level.INFO, "DriverManager.getConnection(url) passed");
    Logger.global.log(Level.FINE, "==============\n\n");

    return localConnection;
  }

  public static Connection getUrlConnection(String paramString)
    throws SQLException
  {
    Connection localConnection = null;
    checkprops();

    Logger.global.log(Level.FINE, "DriverManager.getConnection(newUrl)  newUrl = " + paramString);
    localConnection = DriverManager.getConnection(paramString);
    Logger.global.log(Level.INFO, "DriverManager.getConnection(newUrl) passed  mewUrl = " + paramString);
    Logger.global.log(Level.FINE, "==============\n\n");

    return localConnection;
  }

  public static void main(String[] paramArrayOfString)
  {
    try
    {
      Connection localConnection1 = getUserConnection();
      Connection localConnection2 = getPropertiesConnection();
      Connection localConnection3 = getUrlConnection();

      Logger.global.log(Level.INFO, "testing valid setCatalog");
      localConnection1.setCatalog("Velu");
      Logger.global.log(Level.INFO, "testing valid setCatalog done");

      Logger.global.log(Level.INFO, "testing invalid setTransactionIsolation");
      localConnection1.setTransactionIsolation(2);
      Logger.global.log(Level.INFO, "testing invalid TransactionIsolation done");

      Logger.global.log(Level.FINE, "testing connection.close for (url)");
      localConnection1.close();
      Logger.global.log(Level.INFO, "testing connection.close for (url) passed");
      Logger.global.log(Level.FINE, "==============\n\n");

      Logger.global.log(Level.FINE, "testing connection.close for (url, usr, pwd)");
      localConnection2.close();
      Logger.global.log(Level.INFO, "testing connection.close for (url) passed");
      Logger.global.log(Level.FINE, "==============\n\n");

      Logger.global.log(Level.FINE, "testing connection.close for (url, info)");
      localConnection3.close();
      Logger.global.log(Level.INFO, "testing connection.close for (url) passed");
      Logger.global.log(Level.FINE, "==============\n\n");
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
  }

  public static void dropTable(Connection paramConnection, String paramString)
  {
    Statement localStatement = null;
    try
    {
      localStatement = paramConnection.createStatement();
      localStatement.executeUpdate("drop table " + paramString);
    }
    catch (SQLException localException2)
    {
      Logger.global.log(Level.FINE, "Drop table failed for = " + paramString);
      Logger.global.log(Level.FINE, "==============\n\n");
    } finally {
      try {
        localStatement.close();
      } catch (Exception localException3) {
      }
    }
  }

  public static void initialData(Connection paramConnection, String paramString) throws SQLException {
    Statement localStatement = null;
    try
    {
      localStatement = paramConnection.createStatement();
      localStatement.executeUpdate("create table " + paramString + " (c1 char(20), c2 smallint, c3 integer, c4 largeint, c5 varchar(120), c6 numeric(10,2), c7 decimal(10,2),c8 date, c9 time, c10 timestamp, c11 real, c12 double precision) NO PARTITION");

      localStatement.executeUpdate("insert into " + paramString + " values('Row1', 100, 12345678, 123456789012, 'Smith', 100.12, 100.12, {d '2000-05-06'}, {t '10:11:12'}, {ts '2000-05-06 10:11:12.0'}, 100.12, 100.12)");

      localStatement.executeUpdate("insert into " + paramString + " values('Row2', -100, -12345678, -123456789012, 'Smith', -100.12, -100.12, {d '2000-05-16'}, {t '10:11:12'}, {ts '2000-05-06 10:11:12'}, -100.12, -100.12)");
      localStatement.close();
    }
    catch (SQLException localSQLException)
    {
      Logger.global.log(Level.FINE, "InitialData failed = " + localSQLException);
      Logger.global.log(Level.FINE, "==============\n\n");
      try {
        localStatement.close(); } catch (Exception localException) {
      }
      throw localSQLException;
    }
  }

  public static void initialCurrentData(Connection paramConnection, String paramString) throws SQLException
  {
    PreparedStatement localPreparedStatement = null;
    try
    {
      System.out.println("");
      System.out.println("Inserting TimeStamp ");
      localPreparedStatement = paramConnection.prepareStatement("insert into " + paramString + " values('TimeStamp', -100, -12345678, -123456789012, 'Smith', -100.12, -100.12, ?, ?, ?, -100.12, -100.12)");

      localPreparedStatement.setDate(1, new java.sql.Date(new java.util.Date().getTime()));
      localPreparedStatement.setTime(2, new Time(new java.util.Date().getTime()));
      Timestamp localTimestamp = new Timestamp(new java.util.Date().getTime());
      localPreparedStatement.setTimestamp(3, localTimestamp);
      if (localPreparedStatement.executeUpdate() != 1)
      {
        System.out.println("executeUpdate of TimeStamp failed");
      }
      localPreparedStatement.close();
    }
    catch (SQLException localSQLException)
    {
      Logger.global.log(Level.FINE, "InitialCurrentData failed =" + localSQLException);
      Logger.global.log(Level.FINE, "==============\n\n");
      try {
        localPreparedStatement.close(); } catch (Exception localException) {
      }
      throw localSQLException;
    }
  }

  static
  {
    try
    {
      String str = System.getProperty("hpt4jdbc.properties");
      if (str != null)
      {
        FileInputStream localFileInputStream = new FileInputStream(new File(str));
        props = new Properties();
        props.load(localFileInputStream);

        url = props.getProperty("url");
        usr = props.getProperty("user");
        pwd = props.getProperty("password");
      } else {
        System.out.println("Error: hpt4jdbc.properties is not set. Exiting.");
        System.exit(0);
      }
    }
    catch (Exception localException1)
    {
      localException1.printStackTrace();
      System.out.println(localException1.getMessage());
    }

    try
    {
      Class.forName("org.trafodion.jdbc.t4.T4Driver");
      Logger.global.setLevel(Level.FINEST);
    } catch (Exception localException2) {
      localException2.printStackTrace();
      System.out.println(localException2.getMessage());
      System.exit(0);
    }
  }
}
