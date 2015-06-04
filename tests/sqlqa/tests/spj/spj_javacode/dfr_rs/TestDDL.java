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
import java.sql.Statement;

public class TestDDL
{
  public static void main(String[] paramArrayOfString)
  {
  }

  public static void createTable(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str1 = "jdbc:default:connection";
    String str2 = paramString.trim();
    try
    {
      System.out.println("Enter createTable...");
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate("create table " + str2 + " (c1 int not null primary key, c2 varchar(20) not null, c3 int)");
      localStatement.executeUpdate("alter table " + str2 + " rename to " + str2 + "_tmp");
      localStatement.executeUpdate("drop table " + str2 + "_tmp");
      localStatement.executeUpdate("create table " + str2 + " (c1 int not null primary key, c2 varchar(20) not null, c3 int)");
      paramArrayOfString[0] = "";
    }
    catch (Exception localException)
    {
      paramArrayOfString[0] = localException.getMessage();
    }
  }

  public static void createIndex(String paramString1, String paramString2, String[] paramArrayOfString) throws Exception
  {
    Connection localConnection = null;
    String str1 = "jdbc:default:connection";
    String str2 = paramString1.trim();
    String str3 = paramString2.trim();
    try
    {
      System.out.println("Enter createIndex...");
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate("create index " + str2 + " on " + str3 + "(c2)");
      localStatement.executeUpdate("drop index " + str2);
      localStatement.executeUpdate("create index " + str2 + " on " + str3 + "(c2)");
      paramArrayOfString[0] = "";
    }
    catch (Exception localException)
    {
      paramArrayOfString[0] = localException.getMessage();
    }
  }

  public static void createView(String paramString1, String paramString2, String[] paramArrayOfString) throws Exception
  {
    Connection localConnection = null;
    String str1 = "jdbc:default:connection";
    String str2 = paramString1.trim();
    String str3 = paramString2.trim();
    try
    {
      System.out.println("Enter createView...");
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate("create view " + str2 + " (a, b) as select c1, c3 from " + str3);
      localStatement.executeUpdate("alter view " + str2 + " rename to " + str2 + "_tmp");
      localStatement.executeUpdate("drop view " + str2 + "_tmp");
      localStatement.executeUpdate("create view " + str2 + " (a, b) as select c1, c3 from " + str3);
      paramArrayOfString[0] = "";
    }
    catch (Exception localException)
    {
      paramArrayOfString[0] = localException.getMessage();
    }
  }

  public static void createTrigger(String paramString1, String paramString2, String[] paramArrayOfString) throws Exception
  {
    Connection localConnection = null;
    String str1 = "jdbc:default:connection";
    String str2 = paramString1.trim();
    String str3 = paramString2.trim();
    try
    {
      System.out.println("Enter createTrigger...");
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate("create trigger " + str2 + " before insert on " + str3 + 
        " REFERENCING NEW AS newR " + 
        "FOR EACH ROW SET newR.c3 = newR.c3 + 100");
      localStatement.executeUpdate("alter trigger disable " + str2);
      localStatement.executeUpdate("drop trigger " + str2);
      localStatement.executeUpdate("create trigger " + str2 + " before insert on " + str3 + 
        " REFERENCING NEW AS newR " + 
        "FOR EACH ROW SET newR.c3 = newR.c3 + 100");
      paramArrayOfString[0] = "";
    }
    catch (Exception localException)
    {
      paramArrayOfString[0] = localException.getMessage();
    }
  }

  public static void createMV(String paramString1, String paramString2, String[] paramArrayOfString) throws Exception
  {
    Connection localConnection = null;
    String str1 = "jdbc:default:connection";
    String str2 = paramString1.trim();
    String str3 = paramString2.trim();
    try
    {
      System.out.println("Enter createMV...");
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate("create mv " + str2 + " refresh on request initialize on refresh " + 
        "hash partition by (c1)" + 
        "as select c1, c2 from " + str3);
      localStatement.executeUpdate("alter mv " + str2 + " rename to " + str2 + "_tmp");
      localStatement.executeUpdate("drop mv " + str2 + "_tmp");
      localStatement.executeUpdate("create mv " + str2 + " refresh on request initialize on refresh " + 
        "hash partition by (c1)" + 
        "as select c1, c2 from " + str3);
      paramArrayOfString[0] = "";
    }
    catch (Exception localException)
    {
      paramArrayOfString[0] = localException.getMessage();
    }
  }

  public static void createSynonym(String paramString1, String paramString2, String[] paramArrayOfString) throws Exception
  {
    Connection localConnection = null;
    String str1 = "jdbc:default:connection";
    String str2 = paramString1.trim();
    String str3 = paramString2.trim();
    try
    {
      System.out.println("Enter createSynonym ...");
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate("create synonym " + str2 + " for " + str3);
      localStatement.executeUpdate("drop synonym " + str2);
      localStatement.executeUpdate("create synonym " + str2 + " for " + str3);
      paramArrayOfString[0] = "";
    }
    catch (Exception localException)
    {
      paramArrayOfString[0] = localException.getMessage();
    }
  }

  public static void createProcedure(String paramString1, String paramString2, String[] paramArrayOfString) throws Exception
  {
    Connection localConnection = null;
    String str1 = "jdbc:default:connection";
    String str2 = paramString1.trim();
    String str3 = paramString2.trim();
    try
    {
      System.out.println("Enter createProcedure...");
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate("create procedure " + str2 + " (in in1 nchar(50), out out1 nchar(100)) " + 
        "external name 'TestDDL.createTable' " + 
        "library " + str3 + 
        " language java " + 
        "parameter style java");
      localStatement.executeUpdate("drop procedure " + str2);
      localStatement.executeUpdate("create procedure " + str2 + " (in in1 nchar(50), out out1 nchar(100)) " + 
        "external name 'TestDDL.createTable' " + 
        "library " + str3 + 
        " language java " + 
        "parameter style java");
      paramArrayOfString[0] = "";
    }
    catch (Exception localException)
    {
      paramArrayOfString[0] = localException.getMessage();
    }
  }
}
