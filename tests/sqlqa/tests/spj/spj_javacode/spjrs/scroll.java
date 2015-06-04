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

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class scroll
{
  public static void RS256(String[] paramArrayOfString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement(1005, 1007);

    String str2 = "select st1 from trs";

    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
    paramArrayOfResultSet[0].last();
    paramArrayOfString[0] = paramArrayOfResultSet[0].getString(1);
  }

  public static void RS257(String[] paramArrayOfString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement(1005, 1007);

    String str2 = "select st1 from trs";

    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
    paramArrayOfResultSet[0].absolute(4);
    paramArrayOfString[0] = paramArrayOfResultSet[0].getString(1);
  }

  public static void RS258(String[] paramArrayOfString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement(1005, 1007);

    String str2 = "select st1 from trs";

    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
    paramArrayOfResultSet[0].absolute(4);
    paramArrayOfResultSet[0].relative(-3);
    paramArrayOfString[0] = paramArrayOfResultSet[0].getString(1);
  }

  public static void RS259(String[] paramArrayOfString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement(1005, 1007);

    String str2 = "select st1 from trs";

    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
    paramArrayOfResultSet[0].relative(21);
    paramArrayOfString[0] = paramArrayOfResultSet[0].getString(1);
  }

  public static void RS260(String[] paramArrayOfString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement(1005, 1007);

    String str2 = "select st1 from trs";

    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
    paramArrayOfResultSet[0].first();
    paramArrayOfString[0] = paramArrayOfResultSet[0].getString(1);
  }

  public static void RS261(String[] paramArrayOfString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement(1005, 1007);

    String str2 = "select st1 from trs";

    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
    paramArrayOfResultSet[0].previous();
    paramArrayOfString[0] = paramArrayOfResultSet[0].getString(1);
  }

  public static void RS262(String[] paramArrayOfString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement(1005, 1007);

    String str2 = "select st1 from trs";

    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
    paramArrayOfResultSet[0].absolute(-1);
    paramArrayOfString[0] = paramArrayOfResultSet[0].getString(1);
  }

  public static void RS263(String[] paramArrayOfString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);

    Statement localStatement = localConnection.createStatement(1003, 1007);

    String str2 = "select st1 from trs";

    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
    paramArrayOfResultSet[0].next();
    paramArrayOfString[0] = paramArrayOfResultSet[0].getString(1);
  }

  public static void RS264(String[] paramArrayOfString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);

    Statement localStatement = localConnection.createStatement(1003, 1007);

    String str2 = "select st1 from trs";

    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
    paramArrayOfResultSet[0].next();
    paramArrayOfResultSet[0].absolute(-1);
    paramArrayOfString[0] = paramArrayOfResultSet[0].getString(1);
  }

  public static void RS265(String[] paramArrayOfString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);

    Statement localStatement = localConnection.createStatement(1003, 1007);

    String str2 = "select st1 from trs";

    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
    paramArrayOfResultSet[0].next();
    paramArrayOfResultSet[0].absolute(-1);
    paramArrayOfString[0] = paramArrayOfResultSet[0].getString(1);
  }
}
