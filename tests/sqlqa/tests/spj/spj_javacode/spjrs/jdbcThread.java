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

import java.io.PrintStream;
import java.math.BigDecimal;
import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Timestamp;

class jdbcThread extends Thread
{
  public jdbcThread(String paramString)
  {
    super(paramString);
  }

  public void run() {
    Connection localConnection = null;
    try
    {
      localConnection = DriverManager.getConnection("jdbc:default:connection");
      String str = "select * from testtab";
      PreparedStatement localPreparedStatement = localConnection.prepareStatement(str);

      ResultSet localResultSet = localPreparedStatement.executeQuery();
      boolean bool;
      while (((bool = localResultSet.next()) == true) && 
        (bool));
      localResultSet.close();
      localPreparedStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      localSQLException.printStackTrace();
    }
  }

  public static void twoResultSets(double paramDouble, ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws SQLException
  {
    int i = 0;
    String str1 = null;
    try
    {
      str1 = "GET CONNECTION";
      Connection localConnection = DriverManager.getConnection("jdbc:default:connection");

      str1 = "SELECT STATEMENT 1";

      String str2 = "SELECT name, job, CAST(salary AS DOUBLE) FROM staff   WHERE salary > ?   ORDER BY salary";

      PreparedStatement localPreparedStatement1 = localConnection.prepareStatement(str2);

      localPreparedStatement1.setDouble(1, paramDouble);

      paramArrayOfResultSet1[0] = localPreparedStatement1.executeQuery();

      str1 = "SELECT STATEMENT 2";

      String str3 = "SELECT name, job, CAST(salary AS DOUBLE) FROM staff   WHERE salary < ?   ORDER BY salary DESC";

      PreparedStatement localPreparedStatement2 = localConnection.prepareStatement(str3);

      localPreparedStatement2.setDouble(1, paramDouble);

      paramArrayOfResultSet2[0] = localPreparedStatement2.executeQuery();

      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      i = localSQLException.getErrorCode();
      throw new SQLException(i + " : " + str1 + " FAILED");
    }
  }

  public static void RS232(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws SQLException
  {
    try
    {
      String str = "jdbc:default:connection";
      Connection localConnection = DriverManager.getConnection(str);
      Statement localStatement = localConnection.createStatement();
      try
      {
        localStatement.executeUpdate("drop table sample");
      }
      catch (SQLException localSQLException2)
      {
      }
      localStatement.executeUpdate("create table sample (c1 char(20), c2 smallint, c3 integer, c4 largeint, c5 varchar(120), c6 numeric(10,2), c7 decimal(10,2),c8 date, c9 time, c10 timestamp, c11 float, c12 double precision)");
      localStatement.executeUpdate("insert into sample values('Moe', 100, 12345678, 123456789012, 'Moe', 100.12, 100.12, {d '2000-05-16'}, {t '10:11:12'}, {ts '2000-05-06 10:11:12.0'}, 100.12, 100.12)");
      localStatement.executeUpdate("insert into sample values('Larry', -100, -12345678, -123456789012, 'Larry', -100.12, -100.12, {d '2000-05-16'}, {t '10:11:12'}, {ts '2000-05-06 10:11:12'}, -100.12, -100.12)");
      localStatement.executeUpdate("insert into sample values('Curly', 100, -12345678, 123456789012, 'Curly', -100.12, 100.12, {d '2000-05-16'}, {t '10:11:12'}, {ts '2000-05-06 10:11:12'}, -100.12, 100.12)");
      localStatement.executeUpdate("insert into sample values('Smith', 125, -987654321, 987654321233, 'Smith', -125.99, 125.32, {d '2005-10-20'}, {t '12:10:10'}, {ts '2005-10-20 12:45:45'}, -125.32, 124.98)");
      for (int j = 0; j < 10; ++j)
      {
        ResultSet localResultSet;
        PreparedStatement localPreparedStatement;
        DatabaseMetaData localDatabaseMetaData;
        switch (j)
        {
        case 0:
          System.out.println("");
          System.out.println("Simple Select ");
          localStatement = localConnection.createStatement();
          localResultSet = localStatement.executeQuery("select * from sample");
          break;
        case 1:
          System.out.println("");
          System.out.println("Parameterized Select - CHAR");
          localPreparedStatement = localConnection.prepareStatement("select c1, c2 from sample where c1 = ?");
          localPreparedStatement.setString(1, "Moe");
          localResultSet = localPreparedStatement.executeQuery();
          break;
        case 2:
          System.out.println("");
          System.out.println("Parameterized Select - INT");
          localPreparedStatement = localConnection.prepareStatement("select c1, c2, c3 from sample where c2 = ?  or c2 = ? or c2 = ?");
          localPreparedStatement.setInt(1, 100);
          localPreparedStatement.setInt(2, -100);
          localPreparedStatement.setInt(3, 125);
          localResultSet = localPreparedStatement.executeQuery();
          break;
        case 3:
          System.out.println("");
          System.out.println("Parameterized Select - TIMESTAMP");
          localPreparedStatement = localConnection.prepareStatement("select c1, c2, c3, c10 from sample where c10 = ?");
          localPreparedStatement.setTimestamp(1, Timestamp.valueOf("2000-05-06 10:11:12.0"));
          localResultSet = localPreparedStatement.executeQuery();
          break;
        case 4:
          System.out.println("");
          System.out.println("Parameterized Select - DECIMAL");
          localPreparedStatement = localConnection.prepareStatement("select c1, c2, c3, c7 from sample where c7 = ? or c7 = ?");
          localPreparedStatement.setBigDecimal(1, new BigDecimal("100.12"));
          localPreparedStatement.setBigDecimal(2, new BigDecimal("-100.12"));
          localResultSet = localPreparedStatement.executeQuery();
          break;
        case 5:
          System.out.println("");
          System.out.println("Parameterized Select - NUMERIC");
          localPreparedStatement = localConnection.prepareStatement("select c1, c2, c3, c6 from sample where c6 = ? or c6 = ?");
          localPreparedStatement.setBigDecimal(1, new BigDecimal("100.12"));
          localPreparedStatement.setBigDecimal(2, new BigDecimal("-100.12"));
          localResultSet = localPreparedStatement.executeQuery();
          break;
        case 6:
          System.out.println("");
          System.out.println("getTypeInfo() ");
          localDatabaseMetaData = localConnection.getMetaData();
          localResultSet = localDatabaseMetaData.getTypeInfo();
          break;
        case 7:
          System.out.println("");
          System.out.println("getCatalogs()");
          localDatabaseMetaData = localConnection.getMetaData();
          localResultSet = localDatabaseMetaData.getCatalogs();
          break;
        case 8:
          System.out.println("");
          System.out.println("getTables() ");
          localDatabaseMetaData = localConnection.getMetaData();
          localResultSet = localDatabaseMetaData.getTables(null, null, "SAM%", null);
          break;
        default:
          localResultSet = null;
          break;
        }

        ResultSetMetaData localResultSetMetaData = localResultSet.getMetaData();
        System.out.println("");
        System.out.println("Printing ResultSetMetaData ...");
        System.out.println("No. of Columns " + localResultSetMetaData.getColumnCount());
        for (int k = 1; k <= localResultSetMetaData.getColumnCount(); ++k)
        {
          System.out.println("Column " + k + " Data Type: " + localResultSetMetaData.getColumnTypeName(k) + " Name: " + localResultSetMetaData.getColumnName(k));
        }
        System.out.println("");
        System.out.println("Fetching rows...");
        int i = 0;
        while (localResultSet.next())
        {
          ++i;
          System.out.println("");
          System.out.println("Printing Row " + i + " using getString(), getObject()");
          for (int k = 1; k <= localResultSetMetaData.getColumnCount(); ++k)
          {
            System.out.println("Column " + k + " - " + localResultSet.getString(k) + "," + localResultSet.getObject(k));
          }
        }
        System.out.println("");
        System.out.println("End of Data");
        localResultSet.close();
      }
      localStatement = localConnection.createStatement();
      localStatement.executeUpdate("drop table sample");
      localConnection.close();
    }
    catch (SQLException localSQLException1)
    {
      SQLException localSQLException3 = localSQLException1;
      do
      {
        System.out.println(localSQLException3.getMessage());
        System.out.println("SQLState   " + localSQLException3.getSQLState());
        System.out.println("Error Code " + localSQLException3.getErrorCode());
      }while ((localSQLException3 = localSQLException3.getNextException()) != null);
    }
  }

  public static void RS233(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws SQLException
  {
    int i = 99999;
    long l = 0L;
    try
    {
      Connection localConnection = DriverManager.getConnection("jdbc:default:connection");

      DatabaseMetaData localDatabaseMetaData = localConnection.getMetaData();

      System.out.println("HOLD_CURSORS_OVER_COMMIT = " + localDatabaseMetaData.supportsResultSetHoldability(1));
      System.out.println("CLOSE_CURSORS_AT_COMMIT = " + localDatabaseMetaData.supportsResultSetHoldability(2));
      Statement localStatement = localConnection.createStatement();
      try
      {
        localStatement.executeUpdate("drop table holdJdbcMx");
      }
      catch (SQLException localSQLException2)
      {
      }

      localStatement.executeUpdate("create table holdJdbcMx (dest_id integer unsigned, msg_id largeint, msg_object varchar(70))");

      PreparedStatement localPreparedStatement = localConnection.prepareStatement("insert into holdJdbcMx values ( ?, ?, ?)");
      localPreparedStatement.setInt(1, 100);

      for (int j = 0; j < i; ++j)
      {
        l = System.currentTimeMillis();
        localPreparedStatement.setLong(2, l);
        localPreparedStatement.setString(3, "test object " + j);
        localPreparedStatement.execute();
      }

    }
    catch (SQLException localSQLException1)
    {
      SQLException localSQLException3 = localSQLException1;
      do
      {
        System.out.println(localSQLException3.getMessage());
        System.out.println(localSQLException3.getSQLState());
      }while ((localSQLException3 = localSQLException3.getNextException()) != null);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }

    subscribeThread localsubscribeThread = new subscribeThread();
    localsubscribeThread.start();
  }
}
