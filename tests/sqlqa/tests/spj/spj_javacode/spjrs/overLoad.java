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
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class overLoad
{
  public static void main(String[] paramArrayOfString)
  {
  }

  public static void sop(String paramString)
  {
    System.out.println(paramString);
  }

  public static void RS205(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";
    try
    {
      Class.forName("org.trafodion.jdbc.t4.T4Driver");
    }
    catch (ClassNotFoundException localClassNotFoundException)
    {
      System.err.print("ClassNotFoundException: ");
      System.err.println(localClassNotFoundException.getMessage());
    }

    try
    {
      Connection localConnection = t4connection.getPropertiesConnection();
      Statement localStatement = localConnection.createStatement();
      paramArrayOfResultSet[0] = localStatement.executeQuery("select e_city from testtab");
    }
    catch (SQLException localSQLException) {
      System.err.println("-----SQLException-----");
      System.err.println("SQLState:  " + localSQLException.getSQLState());
      System.err.println("Message:  " + localSQLException.getMessage());
      System.err.println("Vendor:  " + localSQLException.getErrorCode());
      localSQLException.getNextException();
    }
  }

  public static void RS205(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from t1";
    Connection localConnection = t4connection.getPropertiesConnection();
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement.executeQuery(str2);
  }

  public static void RS205(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from t1";
    Connection localConnection = t4connection.getPropertiesConnection();
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement.executeQuery(str2);
  }

  public static void RS206()
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from t1";
    Connection localConnection = t4connection.getPropertiesConnection();
    Statement localStatement = localConnection.createStatement();
    ResultSet localResultSet = localStatement.executeQuery(str2);
  }

  public static void RS206(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from t1";
    Connection localConnection = t4connection.getPropertiesConnection();
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement.executeQuery(str2);
  }

  public static void RS207(long paramLong, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from t1";
    Connection localConnection = t4connection.getPropertiesConnection();
    Statement localStatement = localConnection.createStatement();
    ResultSet localResultSet = localStatement.executeQuery(str2);
  }

  public static void RS207(long paramLong, ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from t1";
    Connection localConnection = t4connection.getPropertiesConnection();
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement.executeQuery(str2);
  }

  public static void RS208(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, long paramLong, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from t1";
    Connection localConnection = t4connection.getPropertiesConnection();
    Statement localStatement = localConnection.createStatement();
    ResultSet localResultSet = localStatement.executeQuery(str2);
  }

  public static void RS208(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, long paramLong)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from t1";
    Connection localConnection = t4connection.getPropertiesConnection();
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement.executeQuery(str2);
  }

  public static void RS209(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, long paramLong)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from t1";
    Connection localConnection = t4connection.getPropertiesConnection();
    Statement localStatement = localConnection.createStatement();
    ResultSet localResultSet = localStatement.executeQuery(str2);
  }

  public static void RS209(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, long paramLong)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from t1";
    Connection localConnection = t4connection.getPropertiesConnection();
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement.executeQuery(str2);
  }
}
