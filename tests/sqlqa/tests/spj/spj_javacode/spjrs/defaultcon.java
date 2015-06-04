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
import java.sql.BatchUpdateException;
import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Savepoint;
import java.sql.Statement;
import java.sql.Timestamp;

public class defaultcon
{
  public static void main(String[] paramArrayOfString)
  {
  }

  public static void sop(String paramString)
  {
    System.out.println(paramString);
  }

  public static void RS216(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select * from t4";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS400(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from t1,t2";

    System.err.println("In the Java Stored Procedure !");
    Connection localConnection = DriverManager.getConnection(str1);

    Statement localStatement = localConnection.createStatement();

    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS200A(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from t1";
    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS200B(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from t1";
    String str3 = "select * from t2";
    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement1.executeQuery(str2);
    Statement localStatement2 = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement2.executeQuery(str3);
  }

  public static void RS200c(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from s2";
    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS200d(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    for (int i = 0; i < 10; ++i)
    {
      Statement localStatement = localConnection.createStatement();
      String str2 = "select * from t1";
      paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
    }
  }

  public static void RS217(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement1 = localConnection.createStatement();
    String str2 = "select * from trs";
    paramArrayOfResultSet1[0] = localStatement1.executeQuery(str2);

    localConnection = DriverManager.getConnection(str1);
    Statement localStatement2 = localConnection.createStatement();
    String str3 = "select * from trn";
    paramArrayOfResultSet2[0] = localStatement2.executeQuery(str3);
  }

  public static void RS200(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);
      Statement localStatement = localConnection.createStatement();

      String str2 = "select e_name,e_title,e_city,e_salary,e_code,e_long,e_float,e_real,e_double,e_numeric,e_numeric1 from testtab";
      paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
    }
    catch (SQLException localSQLException) {
      System.err.print("SQLException: ");
      System.err.println(localSQLException.getMessage());
      localSQLException.getNextException();
    }
  }

  public static void RS201(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str);
      Statement localStatement = localConnection.createStatement();
      ResultSet tmp29_24 = localStatement.executeQuery("select * from coffees"); paramArrayOfResultSet1[0] = tmp29_24; paramArrayOfResultSet2[0] = tmp29_24;
    }
    catch (SQLException localSQLException)
    {
      System.err.println("-----SQLException-----");
      System.err.println("SQLState:  " + localSQLException.getSQLState());
      System.err.println("Message:  " + localSQLException.getMessage());
      System.err.println("Vendor:  " + localSQLException.getErrorCode());
      localSQLException.getNextException();
    }
  }

  public static void RS201b(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();
    localStatement.setFetchSize(4);
    paramArrayOfResultSet[0] = localStatement.executeQuery("select * from i3");
  }

  public static void DRS202(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);

    Statement localStatement1 = localConnection.createStatement(1005, 1007);

    paramArrayOfResultSet1[0] = localStatement1.executeQuery("select * from trn");
    Statement localStatement2 = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement2.executeQuery("select * from trnv");
  }

  public static void RS218(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement(1004, 1007);

    paramArrayOfResultSet[0] = localStatement.executeQuery("select * from trn");
    paramArrayOfResultSet[0].afterLast();
  }

  public static void RS206(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);

      Statement localStatement = localConnection.createStatement(1004, 1008);

      ResultSet localResultSet = localStatement.executeQuery("select e_name from testtab");
      localResultSet.afterLast();

      while (localResultSet.previous())
      {
        String str2 = localResultSet.getString("e_name");
        System.out.print("e_name: " + str2);
      }

      localResultSet.close();
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException) {
      System.err.println("-----SQLException-----");
      System.err.println("SQLState:  " + localSQLException.getSQLState());
      System.err.println("Message:  " + localSQLException.getMessage());
      System.err.println("Vendor:  " + localSQLException.getErrorCode());
      localSQLException.getNextException();
    }
  }

  public static void RS207(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str);

      Statement localStatement = localConnection.createStatement(1005, 1007);

      paramArrayOfResultSet1[0] = localStatement.executeQuery("select a from bd");

      paramArrayOfResultSet2[0] = localStatement.executeQuery("select a from bd");
    }
    catch (SQLException localSQLException)
    {
      System.err.println("-----SQLException-----");
      System.err.println("SQLState:  " + localSQLException.getSQLState());
      System.err.println("Message:  " + localSQLException.getMessage());
      System.err.println("Vendor:  " + localSQLException.getErrorCode());
      localSQLException.getNextException();
    }
  }

  public static void RS208(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str);

      Statement localStatement = localConnection.createStatement(1005, 1007);

      paramArrayOfResultSet[0] = localStatement.executeQuery("select e_long from testtab");
      paramArrayOfResultSet[0].next();
    }
    catch (SQLException localSQLException)
    {
      System.err.println("-----SQLException-----");
      System.err.println("SQLState:  " + localSQLException.getSQLState());
      System.err.println("Message:  " + localSQLException.getMessage());
      System.err.println("Vendor:  " + localSQLException.getErrorCode());
      localSQLException.getNextException();
    }
  }

  public static void RS209(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);

      Statement localStatement = localConnection.createStatement(1005, 1007);

      ResultSet localResultSet = localStatement.executeQuery("select e_name from testtab");
      localResultSet.relative(2);
      while (localResultSet.next())
      {
        String str2 = localResultSet.getString("e_name");
        System.out.print("e_name: " + str2);
      }

      localResultSet.close();
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException) {
      System.err.println("-----SQLException-----");
      System.err.println("SQLState:  " + localSQLException.getSQLState());
      System.err.println("Message:  " + localSQLException.getMessage());
      System.err.println("Vendor:  " + localSQLException.getErrorCode());
      localSQLException.getNextException();
    }
  }

  public static void RS204(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);
      Statement localStatement = localConnection.createStatement();

      String str2 = "select *  from testtab";
      ResultSet localResultSet = localStatement.executeQuery(str2);

      while (localResultSet.next());
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException) {
      System.err.print("SQLException: ");
      System.err.println(localSQLException.getMessage());
      localSQLException.getNextException();
    }
  }

  public static void RS205b(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);
      Statement localStatement = localConnection.createStatement();

      String str2 = "select *  from testtab";
      ResultSet localResultSet = localStatement.executeQuery(str2);

      while (localResultSet.next());
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException) {
      System.err.print("SQLException: ");
      System.err.println(localSQLException.getMessage());
      localSQLException.getNextException();
    }
  }

  public static void RS211(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);

      Statement localStatement = localConnection.createStatement(1005, 1007);

      localStatement.executeUpdate("insert into coffees values ('Colombian', 101, 7.99, 0, 0)");

      localStatement.executeUpdate("insert into coffees values ('French_Roast', 49, 8.99, 0, 0)");

      localStatement.executeUpdate("insert into coffees values ('Espresso', 150, 9.99, 0, 0)");

      localStatement.executeUpdate("insert into coffees values ('Colombian_Decaf', 101, 8.99, 0, 0)");

      localStatement.executeUpdate("insert into coffees values ('French_Roast_Decaf', 49, 9.99, 0, 0)");

      String str2 = "select *  from coffees";
      paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
    }
    catch (SQLException localSQLException) {
      System.err.print("SQLException: ");
      System.err.println(localSQLException.getMessage());
      localSQLException.getNextException();
    }
  }

  public static void RS212(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);
      localConnection.setAutoCommit(false);
      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate("Delete from coffees ");
      localStatement.executeUpdate("insert into coffees values ('Colombian', 101, 7.99, 0, 0)");

      localStatement.executeUpdate("insert into coffees values ('French_Roast', 49, 8.99, 0, 0)");

      localStatement.executeUpdate("insert into coffees values ('Espresso', 150, 9.99, 0, 0)");

      localStatement.executeUpdate("insert into coffees values ('Colombian_Decaf', 101, 8.99, 0, 0)");

      localStatement.executeUpdate("insert into coffees values ('French_Roast_Decaf', 49, 9.99, 0, 0)");

      localConnection.rollback();
      String str2 = "select *  from coffees";
      paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
    }
    catch (SQLException localSQLException)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException.getMessage());
      localSQLException.getNextException();
    }
  }

  public static void RS213(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);

      Statement localStatement = localConnection.createStatement(1005, 1007);

      ResultSet localResultSet = localStatement.executeQuery("select e_name from testtab");

      localResultSet.moveToCurrentRow();
      while (localResultSet.next())
      {
        String str2 = localResultSet.getString("e_name");
        System.out.print("e_name: " + str2);
      }

      if (localResultSet != null) localResultSet.close();
      if (localStatement != null) localStatement.close();
      if (localConnection != null) localConnection.close(); 
    }
    catch (SQLException localSQLException)
    {
      System.err.println("-----SQLException-----");
      System.err.println("SQLState:  " + localSQLException.getSQLState());
      System.err.println("Message:  " + localSQLException.getMessage());
      System.err.println("Vendor:  " + localSQLException.getErrorCode());
      localSQLException.getNextException();
    }
  }

  public static void RS214(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);

      Statement localStatement = localConnection.createStatement(1005, 1007);

      ResultSet localResultSet = localStatement.executeQuery("select cof_name, price from coffees");

      localResultSet.absolute(4);
      int i = localResultSet.getRow();
      System.out.println("rowNum should be 4 " + i);
      localResultSet.relative(-3);
      i = localResultSet.getRow();
      System.out.println("rowNum should be 1 " + i);
      localResultSet.relative(2);
      i = localResultSet.getRow();
      System.out.println("rowNum should be 3 " + i);

      localResultSet.absolute(1);
      System.out.println("after last? " + localResultSet.isAfterLast());
      String str2;
      float f;
      if (!localResultSet.isAfterLast()) {
        str2 = localResultSet.getString("cof_name");
        f = localResultSet.getFloat("price");
        System.out.println(str2 + "     " + f);
      }

      localResultSet.afterLast();
      while (localResultSet.previous()) {
        str2 = localResultSet.getString("cof_name");
        f = localResultSet.getFloat("price");
        System.out.println(str2 + "     " + f);
      }

      if (localResultSet != null) localResultSet.close();
      if (localStatement != null) localStatement.close();
      if (localConnection != null) localConnection.close(); 
    }
    catch (BatchUpdateException localBatchUpdateException)
    {
      System.err.println("-----BatchUpdateException-----");
      System.err.println("SQLState:  " + localBatchUpdateException.getSQLState());
      System.err.println("Message:  " + localBatchUpdateException.getMessage());
      System.err.println("Vendor:  " + localBatchUpdateException.getErrorCode());
      System.err.print("Update counts:  ");
      int[] arrayOfInt = localBatchUpdateException.getUpdateCounts();
      for (int j = 0; j < arrayOfInt.length; ++j) {
        System.err.print(arrayOfInt[j] + "   ");
      }
      System.out.println("");
    }
    catch (SQLException localSQLException) {
      System.err.println("-----SQLException-----");
      System.err.println("SQLState:  " + localSQLException.getSQLState());
      System.err.println("Message:  " + localSQLException.getMessage());
      System.err.println("Vendor:  " + localSQLException.getErrorCode());
    }
  }

  public static void RS216a(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);
      Statement localStatement = localConnection.createStatement();
      String str2 = "select e_date,e_time,e_tstamp from testtab";
      paramArrayOfResultSet1[0] = localStatement.executeQuery(str2);
      localStatement.close();

      paramArrayOfResultSet2[0] = localStatement.executeQuery(str2);
    }
    catch (SQLException localSQLException) {
      System.err.print("SQLException: ");
      System.out.println("Sqlcode = " + localSQLException.getErrorCode());
      System.out.println("Message = " + localSQLException.getMessage());
      System.out.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void RS218(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from bigb";
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);
      Statement localStatement = localConnection.createStatement();

      ResultSet localResultSet = localStatement.executeQuery(str2);
      ResultSetMetaData localResultSetMetaData = localResultSet.getMetaData();

      System.out.println("");

      int i = localResultSetMetaData.getColumnCount();
      String str3;
      for (int j = 1; j <= i; ++j)
      {
        if (j > 1) System.out.print(",  ");
        str3 = localResultSetMetaData.getColumnName(j);
        System.out.print(str3);
      }
      System.out.println("");

      while (localResultSet.next())
      {
        for (int j = 1; j <= i; ++j)
        {
          if (j > 1) System.out.print(",  ");
          str3 = localResultSet.getString(j);
          System.out.print(str3);
        }
        System.out.println("");
      }

      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException.getMessage());
    }
  }

  public static void RS220(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);
      localConnection.setAutoCommit(false);
      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate("control query default udr_java_options '-Dcatalog=cat -Dschema=javaqa'");
      localStatement.executeUpdate("Delete from coffees ");
      localStatement.executeUpdate("insert into coffees values ('Colombian', 101, 7.99, 0, 0)");

      localStatement.executeUpdate("insert into coffees values ('French_Roast', 49, 8.99, 0, 0)");

      localStatement.executeUpdate("insert into coffees values ('Espresso', 150, 9.99, 0, 0)");

      localStatement.executeUpdate("insert into coffees values ('Colombian_Decaf', 101, 8.99, 0, 0)");

      localStatement.executeUpdate("insert into coffees values ('French_Roast_Decaf', 49, 9.99, 0, 0)");

      localConnection.commit();
      String str2 = "select *  from coffees";
      ResultSet localResultSet = localStatement.executeQuery(str2);

      while (localResultSet.next())
      {
        System.out.println("cof_name    : " + localResultSet.getString("cof_name"));
        System.out.println("sup_id      : " + localResultSet.getInt("sup_id"));
        System.out.println("price       : " + localResultSet.getFloat("price"));
      }

      localResultSet.close();
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException.getMessage());
      localSQLException.getNextException();
    }
  }

  public static void RS221(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);
      Statement localStatement = localConnection.createStatement();
      String str2 = "select *  from coffees";
      ResultSet localResultSet1 = localStatement.executeQuery(str2);
      System.out.println("Getting the first result set");
      localResultSet1 = localStatement.getResultSet();
      while (localResultSet1.next())
      {
        System.out.println("cof_name    : " + localResultSet1.getString("cof_name"));
        System.out.println("sup_id      : " + localResultSet1.getInt("sup_id"));
        System.out.println("price       : " + localResultSet1.getFloat("price"));
      }

      String str3 = "select *  from testtab";
      ResultSet localResultSet2 = localStatement.executeQuery(str3);
      System.out.println("Getting the second result set :");
      localResultSet2 = localStatement.getResultSet();
      while (localResultSet2.next())
      {
        System.out.println("e_name      : " + localResultSet2.getString("e_name"));
        System.out.println("e_city      : " + localResultSet2.getString("e_city"));
        System.out.println("e_title     : " + localResultSet2.getString("e_title"));
      }

      localResultSet1.close();
      localResultSet2.close();
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException) {
      System.err.print("SQLException: ");
      System.err.println(localSQLException.getMessage());
      localSQLException.getNextException();
    }
  }

  public static void RS222(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    Object localObject1 = null;
    Object localObject2 = null;

    String str1 = "jdbc:default:connection";
    ResultSet localObject3;
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);
      localConnection.setAutoCommit(false);

      Statement localStatement = localConnection.createStatement();

      localStatement.addBatch("insert into coffees values('Amaretto', 49, 9.99, 0, 0)");

      localStatement.addBatch("insert into coffees values('Hazelnut', 49, 9.99, 0, 0)");

      localStatement.addBatch("insert into coffees values('Amaretto_decaf', 49, 10.99, 0, 0)");

      localStatement.addBatch("insert into coffees values('Hazelnut_decaf', 49, 10.99, 0, 0)");

      int[] arrayOfInt = localStatement.executeBatch();
      localConnection.commit();
      localConnection.setAutoCommit(true);

      localObject3 = localStatement.executeQuery("select * from coffees");

      System.out.println("Table coffees after insertion:");
      while (localObject3.next()) {
        String str2 = localObject3.getString("cof_name");
        int j = localObject3.getInt("sup_id");
        float f = localObject3.getFloat("price");
        int k = localObject3.getInt("sales");
        int l = localObject3.getInt("total");
        System.out.print(str2 + "   " + j + "   " + f);
        System.out.println("   " + k + "   " + l);
      }

      localObject3.close();
      localStatement.close();
      localConnection.close();
    }
    catch (BatchUpdateException localBatchUpdateException) {
      System.err.println("-----BatchUpdateException-----");
      System.err.println("SQLState:  " + localBatchUpdateException.getSQLState());
      System.err.println("Message:  " + localBatchUpdateException.getMessage());
      System.err.println("Vendor:  " + localBatchUpdateException.getErrorCode());
      System.err.print("Update counts:  ");
      int[] counts = localBatchUpdateException.getUpdateCounts();
      for (int i = 0; i < counts.length; ++i) {
        System.err.print(counts[i] + "   ");
      }
      System.err.println("");
    }
    catch (SQLException localSQLException) {
      System.err.println("-----SQLException-----");
      System.err.println("SQLState:  " + localSQLException.getSQLState());
      System.err.println("Message:  " + localSQLException.getMessage());
      System.err.println("Vendor:  " + localSQLException.getErrorCode());
    }
  }

  public static void RS223(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);

      Statement localStatement = localConnection.createStatement(1005, 1007);

      ResultSet localResultSet = localStatement.executeQuery("select e_name,e_city,e_salary,e_code,e_title from testtab");

      DatabaseMetaData localDatabaseMetaData = localConnection.getMetaData();

      System.out.println("\nConnected to " + localDatabaseMetaData.getURL() + " using driver = " + localDatabaseMetaData.getDriverName() + ", version = " + localDatabaseMetaData.getDriverVersion());

      System.out.println("\nVendor product name is " + localDatabaseMetaData.getDatabaseProductName() + ".\n\tDatabase software version is " + localDatabaseMetaData.getDatabaseProductVersion() + ".\n\tUser name is " + localDatabaseMetaData.getUserName() + ".\n\tCatalog is called " + localDatabaseMetaData.getCatalogTerm() + ".\n\tSchema is called " + localDatabaseMetaData.getSchemaTerm() + ".\n\tProcedure is called " + localDatabaseMetaData.getProcedureTerm() + ".");

      System.out.println("\nNumeric functions are:\n" + localDatabaseMetaData.getNumericFunctions() + "\nString functions are:\n" + localDatabaseMetaData.getStringFunctions() + "\nDate and Time functions are:\n" + localDatabaseMetaData.getTimeDateFunctions() + "\nSystem functions are:\n" + localDatabaseMetaData.getSystemFunctions() + "\n");

      System.out.println("Use the escape string \"" + localDatabaseMetaData.getSearchStringEscape() + "\" to escape wildcard characters.");

      System.out.println("Is the database in read only mode? Answer: " + localDatabaseMetaData.isReadOnly() + "");

      int i = localResultSet.getType();
      System.out.println("srs is type :" + i);

      int j = localResultSet.getConcurrency();
      System.out.println("srs has concurrency: " + j);

      String str2 = localResultSet.getCursorName();
      System.out.println("String Cursor Name :" + str2);

      int k = localResultSet.getFetchDirection();
      System.out.println("get fetch direction :" + k);

      int l = localResultSet.getFetchSize();
      System.out.println("get fetch Size :" + l);
      int i1 = localResultSet.getType();
      System.out.println("get Type of RS :" + i1);
      int i2 = localResultSet.getRow();
      System.out.println("get cursor position:" + i2);

      while (localResultSet.next())
      {
        String str3 = localResultSet.getString("e_name");
        String str4 = localResultSet.getString("e_city");
        String str5 = localResultSet.getString("e_title");
        int i3 = localResultSet.getInt("e_salary");
        int i4 = localResultSet.getShort("e_code");

        System.out.print(str3 + "   " + str4 + "   " + i3);
        System.out.println("   " + i4 + "   " + str5);
      }

      localResultSet.close();
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException) {
      System.err.println("-----SQLException-----");
      System.err.println("SQLState:  " + localSQLException.getSQLState());
      System.err.println("Message:  " + localSQLException.getMessage());
      System.err.println("Vendor:  " + localSQLException.getErrorCode());
    }
  }

  public static void RS224(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "create table suppliersPK (sup_id INTEGER NOT NULL, sup_name VARCHAR(40), STREET VARCHAR(40), CITY VARCHAR(20), STATE CHAR(2), ZIP CHAR(5), primary key(sup_id))";

    Connection localConnection = DriverManager.getConnection(str1);

    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate(str2);

    DatabaseMetaData localDatabaseMetaData = localConnection.getMetaData();

    ResultSet localResultSet = localDatabaseMetaData.getPrimaryKeys("cat", "javaqa", "suppliersPK");
    while (localResultSet.next()) {
      String str3 = localResultSet.getString("TABLE_NAME");
      String str4 = localResultSet.getString("COLUMN_NAME");
      String str5 = localResultSet.getString("KEY_SEQ");
      String str6 = localResultSet.getString("PK_NAME");
      System.out.println("table name :  " + str3);
      System.out.println("column name:  " + str4);
      System.out.println("sequence in key:  " + str5);
      System.out.println("primary key name:  " + str6);
      System.out.println("");
    }
  }

  public static void RS225(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select e_name,e_title,e_city from testtab";
    String str3 = null;
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);

      Statement localStatement = localConnection.createStatement();

      ResultSet localResultSet = localStatement.executeQuery(str2);

      if (!localResultSet.next())
      {
        str3 = "100 : NO DATA FOUND";
        throw new SQLException(str3);
      }

      System.out.println(localResultSet.getString("e_name") + "\t\t" + localResultSet.getString("e_title") + "\t\t" + localResultSet.getString("e_city"));

      if (localResultSet != null) localResultSet.close();
      if (localStatement != null) localStatement.close();
      if (localConnection != null) localConnection.close(); 
    }
    catch (SQLException localSQLException)
    {
      System.out.println("+++++++++SQLException:++++++++++ ");
      System.out.println("Sqlcode  ==> " + localSQLException.getErrorCode());
      System.out.println("Message  ==> " + localSQLException.getMessage());
      System.out.println("Sqlstate ==> " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void RS226(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select suppliers.sup_name, coffees.cof_name from coffees, suppliers where suppliers.sup_name like 'Acme, Inc.' and suppliers.sup_id = coffees.sup_id";
    try
    {
      Connection localConnection = DriverManager.getConnection(str1, "myLogin", "myPassword");

      Statement localStatement = localConnection.createStatement();

      ResultSet localResultSet = localStatement.executeQuery(str2);
      System.out.println("Supplier, Coffee:");
      while (localResultSet.next()) {
        String str3 = localResultSet.getString(1);
        String str4 = localResultSet.getString(2);
        System.out.println("    " + str3 + ", " + str4);
      }

      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException) {
      System.err.print("SQLException: ");
      System.err.println(localSQLException.getMessage());
    }
  }

  public static void RS229(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str1, "myLogin", "myPassword");

      localConnection.setAutoCommit(false);

      String str2 = "SELECT cof_name, PRICE FROM coffees WHERE TOTAL > ?";

      String str3 = "UPDATE coffees SET PRICE = ? WHERE cof_name = ?";

      PreparedStatement localPreparedStatement1 = localConnection.prepareStatement(str2);
      PreparedStatement localPreparedStatement2 = localConnection.prepareStatement(str3);

      localPreparedStatement1.setInt(1, 7000);
      ResultSet localResultSet = localPreparedStatement1.executeQuery();

      Savepoint localSavepoint = localConnection.setSavepoint();
      float f2;
      while (localResultSet.next()) {
        String localObject1 = localResultSet.getString("cof_name");
        float f1 = localResultSet.getFloat("PRICE");
        f2 = f1 + f1 * 0.05F;
        localPreparedStatement2.setFloat(1, f2);
        localPreparedStatement2.setString(2, localObject1);
        localPreparedStatement2.executeUpdate();
        System.out.println("New price of " + localObject1 + " is " + f2);

        if (f2 > 11.99D) {
          localConnection.rollback(localSavepoint);
        }

      }

      localPreparedStatement1 = localConnection.prepareStatement(str2);
      localPreparedStatement2 = localConnection.prepareStatement(str3);

      localPreparedStatement1.setInt(1, 8000);

      localResultSet = localPreparedStatement1.executeQuery();
      System.out.println();

      Object localObject1 = localConnection.setSavepoint();
      float f3;
      while (localResultSet.next()) {
        String localObject2 = localResultSet.getString("cof_name");
        f2 = localResultSet.getFloat("PRICE");
        f3 = f2 + f2 * 0.05F;
        localPreparedStatement2.setFloat(1, f3);
        localPreparedStatement2.setString(2, localObject2);
        localPreparedStatement2.executeUpdate();
        System.out.println("New price of " + localObject2 + " is " + f3);

        if (f3 > 11.99D) {
          localConnection.rollback((Savepoint)localObject1);
        }
      }

      localConnection.commit();

      Object localObject2 = localConnection.createStatement();
      localResultSet = ((Statement)localObject2).executeQuery("SELECT cof_name, PRICE FROM coffees");

      System.out.println();
      while (localResultSet.next()) {
        String str4 = localResultSet.getString("cof_name");
        f3 = localResultSet.getFloat("PRICE");
        System.out.println("Current price of " + str4 + " is " + f3);
      }

      if (localResultSet != null) localResultSet.close();
      if (localObject2 != null) ((Statement)localObject2).close();
      if (localConnection != null) localConnection.close(); 
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
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
