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

public class RS326
{
  public static void main(String[] paramArrayOfString)
  {
  }

  public static void RS326(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    String str2 = "select * from trs";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS326a(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6, ResultSet[] paramArrayOfResultSet7, ResultSet[] paramArrayOfResultSet8, ResultSet[] paramArrayOfResultSet9, ResultSet[] paramArrayOfResultSet10, ResultSet[] paramArrayOfResultSet11)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement1 = localConnection.createStatement();

    String str2 = "select i1 from d4";
    paramArrayOfResultSet1[0] = localStatement1.executeQuery(str2);

    Statement localStatement2 = localConnection.createStatement();
    String str3 = "select i2 from d4";
    paramArrayOfResultSet2[0] = localStatement2.executeQuery(str3);

    Statement localStatement3 = localConnection.createStatement();
    String str4 = "select i3 from d4";
    paramArrayOfResultSet3[0] = localStatement3.executeQuery(str4);

    Statement localStatement4 = localConnection.createStatement();
    String str5 = "select g0 from d4";
    paramArrayOfResultSet4[0] = localStatement4.executeQuery(str5);

    Statement localStatement5 = localConnection.createStatement();
    String str6 = "select g1 from d4";
    paramArrayOfResultSet5[0] = localStatement5.executeQuery(str6);

    Statement localStatement6 = localConnection.createStatement();
    String str7 = "select g2 from d4";
    paramArrayOfResultSet6[0] = localStatement6.executeQuery(str7);

    Statement localStatement7 = localConnection.createStatement();
    String str8 = "select g3 from d4";
    paramArrayOfResultSet7[0] = localStatement7.executeQuery(str8);

    Statement localStatement8 = localConnection.createStatement();
    String str9 = "select g4 from d4";
    paramArrayOfResultSet8[0] = localStatement8.executeQuery(str9);

    Statement localStatement9 = localConnection.createStatement();
    String str10 = "select g5 from d4";
    paramArrayOfResultSet9[0] = localStatement9.executeQuery(str10);

    Statement localStatement10 = localConnection.createStatement();
    String str11 = "select g6 from d4";
    paramArrayOfResultSet10[0] = localStatement10.executeQuery(str11);

    Statement localStatement11 = localConnection.createStatement();
    String str12 = "select g7 from d4";
    paramArrayOfResultSet11[0] = localStatement11.executeQuery(str12);
  }

  public static void RS326b(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6, ResultSet[] paramArrayOfResultSet7, ResultSet[] paramArrayOfResultSet8, ResultSet[] paramArrayOfResultSet9, ResultSet[] paramArrayOfResultSet10, ResultSet[] paramArrayOfResultSet11, ResultSet[] paramArrayOfResultSet12, ResultSet[] paramArrayOfResultSet13, ResultSet[] paramArrayOfResultSet14, ResultSet[] paramArrayOfResultSet15, ResultSet[] paramArrayOfResultSet16, ResultSet[] paramArrayOfResultSet17, ResultSet[] paramArrayOfResultSet18, ResultSet[] paramArrayOfResultSet19, ResultSet[] paramArrayOfResultSet20, ResultSet[] paramArrayOfResultSet21, ResultSet[] paramArrayOfResultSet22, ResultSet[] paramArrayOfResultSet23, ResultSet[] paramArrayOfResultSet24, ResultSet[] paramArrayOfResultSet25, ResultSet[] paramArrayOfResultSet26, ResultSet[] paramArrayOfResultSet27)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement.executeQuery("select c7 from dttab");
  }

  public static void RS329(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    int i = -20;

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    String str2 = "select * from d4";

    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS330(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    String str2 = "select * from b2pwl16";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }
}
