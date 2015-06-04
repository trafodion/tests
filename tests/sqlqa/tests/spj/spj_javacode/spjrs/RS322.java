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

public class RS322
{
  public static void main(String[] paramArrayOfString)
  {
  }

  public static void RS322(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6, ResultSet[] paramArrayOfResultSet7)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement1 = localConnection.createStatement();

    String str2 = "select ivyr from tbint";
    paramArrayOfResultSet1[0] = localStatement1.executeQuery(str2);

    Statement localStatement2 = localConnection.createStatement();

    String str3 = "select ivmn from tbint";
    paramArrayOfResultSet2[0] = localStatement2.executeQuery(str3);

    Statement localStatement3 = localConnection.createStatement();

    String str4 = "select ivdy from tbint";
    paramArrayOfResultSet3[0] = localStatement3.executeQuery(str4);

    Statement localStatement4 = localConnection.createStatement();

    String str5 = "select ivhr from tbint";
    paramArrayOfResultSet4[0] = localStatement4.executeQuery(str5);

    Statement localStatement5 = localConnection.createStatement();

    String str6 = "select ivmt from tbint";
    paramArrayOfResultSet5[0] = localStatement5.executeQuery(str6);

    Statement localStatement6 = localConnection.createStatement();

    String str7 = "select ivsc from tbint";
    paramArrayOfResultSet6[0] = localStatement6.executeQuery(str7);

    Statement localStatement7 = localConnection.createStatement();

    String str8 = "select ivsc6 from tbint";
    paramArrayOfResultSet7[0] = localStatement7.executeQuery(str8);
  }
}
