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
import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

public class catalog
{
  public static void main(String[] paramArrayOfString)
  {
  }

  public static void sop(String paramString)
  {
    System.out.println(paramString);
  }

  public static void N0351()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("insert into t2 values('Hewlett Packard')");
    localStatement.close();
    localConnection.close();
  }

  public static void N0352()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate("insert into t2 values('Hewlett Packard')");
      localStatement.close();
      localConnection.close();
    }
    catch (Exception localException)
    {
      output.redirectOutput("/usr/ns/spjqa/mxudr.out");
      System.out.println("Exception = " + localException);
    }
  }

  public static void N0350()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("create table qatab( e_name varchar(20) not null, a int not null primary key)");
    localStatement.executeUpdate("insert into qatab values('AAA Computers',2433233)");
  }

  public static void N0350a()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("create table qatab( e_name varchar(20) not null)");
    localStatement.executeUpdate("insert into qatab values('AAA Computers')");
    localStatement.executeUpdate("update qatab set e_name = 'Hewlett Packard'");
    localStatement.close();
    localConnection.close();
  }

  public static void N0353()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("insert into schq2p.t2 values('Hewlett Packard')");
  }

  public static void N0354()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("insert into t2 values('Hewlett Packard')");
  }

  public static void N0355()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    CallableStatement localCallableStatement = null;
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException1)
    {
      sop("ex.toString is: " + localException1.toString());
      sop("ex.printStackTrace is: ");
      localException1.printStackTrace();
    }
    try {
      localCallableStatement = localConnection.prepareCall("{call N0350()}");
      localCallableStatement.execute();
      localConnection.close();
    }
    catch (Exception localException2)
    {
      output.redirectOutput("/usr/ns/spjqa/mxudr.out");
      System.out.println("Exception = " + localException2);
    }
  }
}
