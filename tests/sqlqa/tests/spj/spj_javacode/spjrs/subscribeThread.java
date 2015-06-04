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

class subscribeThread extends Thread
{
  public void run()
  {
    boolean bool = true;
    try
    {
      Connection localConnection = DriverManager.getConnection("jdbc:default:connection");
      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate("CONTROL QUERY DEFAULT STREAM_TIMEOUT '500'");

      System.out.println("");
      System.out.println("Wait for the stream timeout of 5 secs after end of data ");
      System.out.println("");
      localConnection.setAutoCommit(false);
      PreparedStatement localPreparedStatement = localConnection.prepareStatement("SELECT * FROM stream(holdJdbcMx) WHERE msg_id > ? ", 1003, 1008, 1);

      localPreparedStatement.setLong(1, 0L);
      ResultSet localResultSet = localPreparedStatement.executeQuery();

      System.out.println("Fetching rows...");
      int i = 0;

      while (bool)
      {
        try
        {
          if ((bool = localResultSet.next()))
          {
            ++i;
            System.out.println("Row " + i + ": " + localResultSet.getString(1) + ", " + localResultSet.getString(2) + ", " + localResultSet.getString(3));
            localConnection.commit();
          }
        }
        catch (SQLException localSQLException1)
        {
          if (localSQLException1.getErrorCode() == -8006)
          {
            System.out.println("Stream timeout ...");
          }
          else
          {
            throw localSQLException1;
          }
        }
      }

      System.out.println("");
      System.out.println("End of Data");
      localConnection.commit();

      localResultSet.close();
      try
      {
        localStatement.executeUpdate("drop table holdJdbcMx");
      }
      catch (SQLException localSQLException2)
      {
        localSQLException2.printStackTrace();
      }

      localConnection.close();
    }
    catch (SQLException localSQLException3)
    {
      SQLException localSQLException4 = localSQLException3;
      do
      {
        System.out.println(localSQLException4.getMessage());
        System.out.println(localSQLException4.getSQLState());
      }while ((localSQLException4 = localSQLException4.getNextException()) != null);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
  }

  public static void RS234(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws SQLException
  {
    int i = 2;
    Object localObject;
    try
    {
      String str = "create table mt_employee (Emp_Hire_Date varchar (30), Emp_Name varchar(32), Emp_ID int not null not droppable, Emp_Address varchar(32), Emp_City varchar(32), Emp_Salary decimal(10,2), Dept_ID int, primary key (Emp_ID))";

      localObject = DriverManager.getConnection("jdbc:default:connection");
      Statement localStatement = ((Connection)localObject).createStatement();
      try
      {
        localStatement.executeUpdate("drop table mt_employee");
      }
      catch (SQLException localSQLException2) {
      }
      localStatement.executeUpdate(str);

      localStatement.executeUpdate("insert into mt_employee  values ('1/1/1900', 'John Doe', 1, 'unknown',  'unknown', 1111110.09, 1 )");

      localStatement.executeUpdate("insert into mt_employee  values ('2/2/1991', 'Jane Doelman', 2, 'unknown',  'unknown', 22220.99, 1 )");

      localStatement.executeUpdate("insert into mt_employee  values ('3/3/1903', 'James Smith', 3, '11 Pomoroy',  'Santa Clara', 400000.0, 1 )");

      localStatement.executeUpdate("insert into mt_employee  values ('1/1/1998', 'Tim Thomas', 4, '11 mainst',  'San Jose', 50000.0, 1 )");

      localStatement.executeUpdate("insert into mt_employee  values ('2/2/1999', 'Jane Mars', 5, '11 cala',  'San Francisco', 100000.0, 1 )");

      localStatement.executeUpdate("insert into mt_employee  values ('4/3/1909', 'Ken Thompson', 6, '44 Duke',  'Santa Cruz', 14000.0, 1 )");

      localStatement.close();
      ((Connection)localObject).close();
    }
    catch (SQLException localSQLException1)
    {
      localObject = localSQLException1;
      do
      {
        System.out.println("MultiThreadTest: Sample Program Failed during table creation.");
        System.out.println("MultiThreadTest: Message : " + localSQLException1.getMessage());
        System.out.println("MultiThreadTest: Vendor Code : " + localSQLException1.getErrorCode());
        System.out.println("MultiThreadTest: SQLState : " + localSQLException1.getSQLState());
      }
      while ((localObject = ((SQLException)localObject).getNextException()) != null);
    }

    for (int j = 1; j <= i; ++j)
    {
      jdbcThread localjdbcThread = new jdbcThread("Thread " + j);
      localjdbcThread.start();
    }
  }
}
