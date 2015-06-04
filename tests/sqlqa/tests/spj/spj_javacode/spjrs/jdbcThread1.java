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
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

class jdbcThread1 extends Thread
{
  public jdbcThread1(String paramString)
  {
    super(paramString);
  }

  public void run()
  {
    String str = "select * from mt_employee";

    Connection localConnection = null;
    try
    {
      localConnection = DriverManager.getConnection("jdbc:default:connection");
      PreparedStatement localPreparedStatement = localConnection.prepareStatement(str);
      ResultSet localResultSet = localPreparedStatement.executeQuery();
      boolean bool;
      do
      {
        if ((bool = localResultSet.next()) != true)
          continue;
        System.out.println(getName() + "==> " + localResultSet.getString(1));
        System.out.println(getName() + "==> " + localResultSet.getString(2));
      }
      while (bool);
      System.out.println("End of data - " + getName());
      localResultSet.close();

      localConnection.close();
    }
    catch (SQLException localSQLException1)
    {
      SQLException localSQLException2 = localSQLException1;
      do
      {
        System.out.println("Messge : " + localSQLException1.getMessage());
        System.out.println("Vendor Code : " + localSQLException1.getErrorCode());
        System.out.println("SQLState : " + localSQLException1.getSQLState());
      }
      while ((localSQLException2 = localSQLException2.getNextException()) != null);
      System.out.println("MultiThreadTest: " + getName() + ": Failed.");
    }
  }

  public static void RS235(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws SQLException
  {
    String str = "jdbc:default:connection";

    Object localObject = null;

    Connection localConnection = DriverManager.getConnection(str);

    Statement localStatement1 = localConnection.createStatement(1005, 1007);

    paramArrayOfResultSet1[0] = localStatement1.executeQuery("select * from t1");
    Statement localStatement2 = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement2.executeQuery("select * from ntab");
    Statement localStatement3 = localConnection.createStatement();
    paramArrayOfResultSet3[0] = localStatement3.executeQuery("select * from t2");
  }

  public static void RS235a(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5)
    throws SQLException
  {
    String str = "jdbc:default:connection";

    Object localObject = null;

    Connection localConnection = DriverManager.getConnection(str);

    Statement localStatement1 = localConnection.createStatement(1005, 1007);

    paramArrayOfResultSet1[0] = localStatement1.executeQuery("select * from n1");
    Statement localStatement2 = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement2.executeQuery("select * from n2");
    Statement localStatement3 = localConnection.createStatement();
    paramArrayOfResultSet3[0] = localStatement3.executeQuery("select * from n3");
    Statement localStatement4 = localConnection.createStatement();
    paramArrayOfResultSet4[0] = localStatement4.executeQuery("select * from n4");
    Statement localStatement5 = localConnection.createStatement();
    paramArrayOfResultSet5[0] = localStatement5.executeQuery("select * from n5");
  }

  public static void RS235b(ResultSet[] paramArrayOfResultSet)
    throws SQLException
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement(1005, 1007);

    paramArrayOfResultSet[0] = localStatement.executeQuery("select * from n1,n2");
  }

  public static void RS236(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws SQLException
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select cof_name,sup_id,price,sales,total from coffees";
    Object localObject = null;

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement(1003, 1007);

    ResultSet localResultSet = localStatement.executeQuery(str2);
    while (localResultSet.next())
    {
      System.out.println(localResultSet.getString("cof_name") + "\t\t" + localResultSet.getInt("sup_id") + "\t\t" + localResultSet.getFloat("price") + "\t\t" + localResultSet.getInt("sales") + "\t\t" + localResultSet.getInt("total"));
    }
  }

  public static void RS237(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws SQLException
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select cof_name,sup_id,price,sales,total from coffees";
    Object localObject = null;
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);
      Statement localStatement = localConnection.createStatement(1003, 1008);

      ResultSet localResultSet = localStatement.executeQuery(str2);
      while (localResultSet.next())
      {
        System.out.println(localResultSet.getString("cof_name") + "\t\t" + localResultSet.getInt("sup_id") + "\t\t" + localResultSet.getFloat("price") + "\t\t" + localResultSet.getInt("sales") + "\t\t" + localResultSet.getInt("total"));
      }

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

  public static void RS238(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws SQLException
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select cof_name,sup_id,price,sales,total from coffees";
    Object localObject = null;

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement(1004, 1007);

    ResultSet localResultSet = localStatement.executeQuery(str2);
    while (localResultSet.next());
  }

  public static void RS239(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws SQLException
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select cof_name,sup_id,price,sales,total from coffees";
    Object localObject = null;

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement(1005, 1007);

    ResultSet localResultSet = localStatement.executeQuery(str2);
    while (localResultSet.next());
  }

  public static void RS240(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws SQLException
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select cof_name,sup_id,price,sales,total from coffees";
    Object localObject = null;

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement(1005, 1008);

    ResultSet localResultSet = localStatement.executeQuery(str2);
    while (localResultSet.next())
    {
      System.out.println(localResultSet.getString("cof_name") + "\t\t" + localResultSet.getInt("sup_id") + "\t\t" + localResultSet.getFloat("price") + "\t\t" + localResultSet.getInt("sales") + "\t\t" + localResultSet.getInt("total"));
    }
  }

  public static void RS241(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws SQLException
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);

    Statement localStatement = localConnection.createStatement(1004, 1007);

    ResultSet localResultSet = localStatement.executeQuery("select * from coffees");

    System.out.println("");
    localResultSet.first();
    String str2 = localResultSet.getString("cof_name");
    float f = localResultSet.getFloat("PRICE");
    int i = localResultSet.getInt("sup_id");
    System.out.println(str2 + "     " + f + "     " + i);
  }

  public static void RS242(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws SQLException
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);

    Statement localStatement = localConnection.createStatement(1004, 1007);

    ResultSet localResultSet = localStatement.executeQuery("select * from coffees");

    localResultSet.last();
    String str2 = localResultSet.getString("cof_name");
    float f = localResultSet.getFloat("PRICE");
    int i = localResultSet.getInt("sup_id");
  }

  public static void RS243(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws SQLException
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement(1004, 1007);

    ResultSet localResultSet = localStatement.executeQuery("select * from coffees");

    localResultSet.last();
    int i = localResultSet.getRow();
  }

  public static void RS244(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws SQLException
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement(1004, 1007);

    ResultSet localResultSet = localStatement.executeQuery("select * from spjrs");

    System.out.println("");
    localResultSet.absolute(8001010);
  }

  public static void RS245(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws SQLException
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement(1004, 1007);

    ResultSet localResultSet = localStatement.executeQuery("select * from spjrs");

    System.out.println("");
    localResultSet.absolute(-8001010);
  }

  public static void RS246(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws SQLException
  {
    String str1 = "jdbc:default:connection";
    Connection localConnection = null;

    localConnection = DriverManager.getConnection(str1);

    Statement localStatement = localConnection.createStatement(1004, 1008);

    ResultSet localResultSet = localStatement.executeQuery("select * from coffees");
    localResultSet.first();
    localResultSet.deleteRow();

    while (localResultSet.next()) {
      String str2 = localResultSet.getString("cof_name");
    }
  }

  public static void RS247(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws SQLException
  {
    String str1 = "jdbc:default:connection";
    Connection localConnection = null;

    localConnection = DriverManager.getConnection(str1);

    Statement localStatement = localConnection.createStatement(1004, 1008);

    ResultSet localResultSet = localStatement.executeQuery("select * from t2");
    localResultSet.first();
    localResultSet.updateString("NAME", "Hewlett packard");
    localResultSet.updateRow();

    while (localResultSet.next()) {
      String str2 = localResultSet.getString("name");
      System.out.println("Name       :  " + str2);
    }
  }

  public static void RS248(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws SQLException
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement(1004, 1007);

    String str2 = "select * from spjrs";
    ResultSet localResultSet = localStatement.executeQuery(str2);

    localResultSet.next();
  }

  public static void RS249(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws SQLException
  {
    String str1 = "jdbc:default:connection";

    String str2 = "INSERT INTO COFFEES VALUES ('HYPER_BLEND', 101, 10.99, 0, 0)";

    String str3 = "UPDATE COFFEES SET PRICE = ? WHERE KEY = ?";

    Connection localConnection = DriverManager.getConnection(str1, "myLogin", "myPassword");

    PreparedStatement localPreparedStatement = localConnection.prepareStatement(str2, 1);

    localPreparedStatement.executeUpdate();
    ResultSet localResultSet = localPreparedStatement.getGeneratedKeys();

    int i = 0;

    localResultSet.next();
    int j = localResultSet.getInt(1);

    localPreparedStatement = localConnection.prepareStatement(str3);
    localPreparedStatement.setFloat(1, 11.99F);
    localPreparedStatement.setInt(2, j);
    localPreparedStatement.executeUpdate();

    localResultSet.close();
  }

  public static void RS250(ResultSet[] paramArrayOfResultSet)
    throws SQLException
  {
    String str1 = "jdbc:default:connection";

    String str2 = "create table managers(mgr_id int not null not droppable primary key,last_name varchar(25),first_name varchar(25),phone varchar(20))";

    String str3 = "insert into managers (mgr_id, last_name, first_name, phone) values (000001, 'MONTOYA', 'ALFREDO', '8317225600')";

    String str4 = "insert into managers (mgr_id, last_name, first_name, phone) values (000002, 'HASKINS', 'MARGARET', '4084355600')";

    String str5 = "insert into managers (mgr_id, last_name, first_name, phone) values (000003, 'CHEN', 'HELEN', '4153785600')";

    Connection localConnection = DriverManager.getConnection(str1, "myLogin", "myPassword");

    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate(str2);

    localConnection.setAutoCommit(true);

    localStatement.addBatch(str3);
    localStatement.addBatch(str4);
    localStatement.addBatch(str5);
    int[] arrayOfInt = localStatement.executeBatch();

    localConnection.rollback();

    localStatement = localConnection.createStatement(1004, 1008);

    paramArrayOfResultSet[0] = localStatement.executeQuery("select * from managers");
  }

  public static void RS251(ResultSet[] paramArrayOfResultSet)
    throws SQLException
  {
    String str = "jdbc:default:connection";
    Connection localConnection = null;
    PreparedStatement localPreparedStatement = null;
    Object localObject = null;

    localConnection = DriverManager.getConnection(str);

    localPreparedStatement = localConnection.prepareStatement("select * from jdbctest");
    localPreparedStatement.execute();
    paramArrayOfResultSet[0] = localPreparedStatement.getResultSet();
  }

  public static void RS252(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws SQLException
  {
    String str = "jdbc:default:connection";
    Connection localConnection = null;
    PreparedStatement localPreparedStatement = null;
    ResultSet localResultSet = null;

    localConnection = DriverManager.getConnection(str);

    localPreparedStatement = localConnection.prepareStatement("select * from jdbctest");
    localResultSet = localPreparedStatement.executeQuery();
    while (localResultSet.next());
  }

  public static void RS254(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from t1";
    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS255(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from t3";
    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS256X(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from testtab";
    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }
}
