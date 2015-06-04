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

public class Jdbc_Get_Short
{
  public static void getShort(short[] paramArrayOfShort)
    throws Exception
  {
    Connection localConnection = null;

    String str1 = "jdbc:default:connection";
    Statement localStatement = null;
    ResultSet localResultSet = null;
    String str2 = "select smallcol from jdbctest where integercol=1";

    localConnection = DriverManager.getConnection(str1);

    localStatement = localConnection.createStatement();
    localResultSet = localStatement.executeQuery(str2);

    localResultSet.next();
    paramArrayOfShort[0] = localResultSet.getShort(1);
  }
}
