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
import java.sql.Timestamp;

public class Jdbc_Set_Timestamp
{
  public static void setTimestamp(Timestamp paramTimestamp, int[] paramArrayOfInt)
    throws Exception
  {
    System.err.println("In the Java Stored Procedure !");

    Connection localConnection = null;
    String str1 = "jdbc:default:connection";
    PreparedStatement localPreparedStatement = null;
    ResultSet localResultSet = null;
    String str2 = "select integercol from jdbctest where tscol=?";
    localConnection = DriverManager.getConnection(str1);
    localPreparedStatement = localConnection.prepareStatement(str2);
    localPreparedStatement.setTimestamp(1, paramTimestamp);

    System.err.println("sending query : " + str2);
    localResultSet = localPreparedStatement.executeQuery();

    localResultSet.next();
    paramArrayOfInt[0] = localResultSet.getInt(1);
  }
}
