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

public class Jdbc_Get_BigDecimal
{
  public static void RS310(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    Connection localConnection = null;

    String str1 = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str1);
    String str2 = "select numericcol from jdbctest where integercol=2";
    Statement localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement1.executeQuery(str2);

    String str3 = "select numericcol from jdbctest";
    Statement localStatement2 = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement2.executeQuery(str3);
  }
}
