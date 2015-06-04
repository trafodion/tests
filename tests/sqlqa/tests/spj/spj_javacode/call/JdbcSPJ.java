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
import java.sql.SQLException;
import java.sql.Statement;

public class JdbcSPJ
{
  public static void main(String[] paramArrayOfString)
  {
  }

  public static void N0200SP()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    try
    {
      localStatement.executeUpdate("create table qatab( e_name varchar(20) not null, e_num int not null, e_city char(15),\te_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");

      localStatement.executeUpdate("insert into qatab values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");

      localStatement.executeUpdate("update qatab set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',\te_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0 ");
      System.err.println("Table Updated successfully");

      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N0200ST()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("CREATE PROCEDURE HP2003 (IN IN1 VARCHAR(50),OUT OUT1 VARCHAR(56)) \tEXTERNAL NAME 'Procs.N0200' EXTERNAL PATH '/usr/spjqa/Testware/Class' LANGUAGE JAVA  PARAMETER STYLE JAVA NO SQL NO ISOLATE");
    System.err.println("Procedure created successfully");

    localStatement.close();
    localConnection.close();
  }

  public static void N0200SU()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    try
    {
      localStatement.executeUpdate("drop procedure HP2003");

      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N0172()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    try
    {
      localStatement.executeUpdate("CREATE PROCEDURE HP2003 (IN IN1 VARCHAR(50),OUT OUT1 VARCHAR(56)) \tEXTERNAL NAME 'Procs.N0200' EXTERNAL PATH '/usr/spjqa/Testware/Class' LANGUAGE JAVA  PARAMETER STYLE JAVA");
      System.err.println("Procedure created successfully");
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N0173()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    try
    {
      localStatement.executeUpdate("CREATE PROCEDURE HP2003 (IN IN1 VARCHAR(50),OUT OUT1 VARCHAR(56)) \tEXTERNAL NAME 'Procs.N0200' EXTERNAL PATH '/usr/spjqa/Testware/Class' LANGUAGE JAVA  PARAMETER STYLE JAVA CONTAINS SQL NO SQL NO ISOLATE");
      System.err.println("Procedure created successfully");
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }
}