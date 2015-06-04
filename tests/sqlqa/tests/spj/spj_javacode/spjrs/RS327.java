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
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class RS327
{
  public static void main(String[] paramArrayOfString)
  {
  }

  public static void RS353(int paramInt1, int paramInt2, int paramInt3, int[] paramArrayOfInt1, int[] paramArrayOfInt2, String[] paramArrayOfString, ResultSet[] paramArrayOfResultSet)
    throws SQLException
  {
    paramArrayOfInt2[0] = 0;

    Connection localConnection = DriverManager.getConnection("jdbc:default:connection");

    String str = "select * from trn";
    PreparedStatement localPreparedStatement;
    if (paramInt3 == 1) {
      localPreparedStatement = localConnection.prepareStatement(str, 1004, 1007);
    }
    else if (paramInt3 == 2) {
      localPreparedStatement = localConnection.prepareStatement(str, 1005, 1007);
    }
    else
    {
      localPreparedStatement = localConnection.prepareStatement(str);
    }
    if (paramInt1 > 0) {
      localPreparedStatement.setFetchSize(paramInt1);
    }
    ResultSet localResultSet = localPreparedStatement.executeQuery();

    paramArrayOfInt1[0] = localPreparedStatement.getFetchSize();

    if (localResultSet.getType() == 1003)
      paramArrayOfString[0] = "TYPE_FORWARD_ONLY";
    else if (localResultSet.getType() == 1005)
      paramArrayOfString[0] = "TYPE_SCROLL_SENSITIVE";
    else if (localResultSet.getType() == 1004) {
      paramArrayOfString[0] = "TYPE_SCROLL_INSENSITIVE";
    }
    if (paramInt2 > 0)
    {
      int i = 0;
      for (; i < paramInt2; ++i)
      {
        localResultSet.next();
      }

      paramArrayOfInt2[0] = i;
    }

    paramArrayOfResultSet[0] = localResultSet;
  }

  public static void RS354(int paramInt1, int paramInt2, int paramInt3, int[] paramArrayOfInt1, int[] paramArrayOfInt2, String[] paramArrayOfString, ResultSet[] paramArrayOfResultSet)
    throws SQLException
  {
    paramArrayOfInt2[0] = 0;

    Connection localConnection = DriverManager.getConnection("jdbc:default:connection");

    String str = "select * from trn";
    PreparedStatement localPreparedStatement;
    if (paramInt3 == 1) {
      localPreparedStatement = localConnection.prepareStatement(str, 1004, 1008);
    }
    else if (paramInt3 == 2) {
      localPreparedStatement = localConnection.prepareStatement(str, 1005, 1008);
    }
    else
    {
      localPreparedStatement = localConnection.prepareStatement(str);
    }
    if (paramInt1 > 0) {
      localPreparedStatement.setFetchSize(paramInt1);
    }
    ResultSet localResultSet = localPreparedStatement.executeQuery();

    paramArrayOfInt1[0] = localPreparedStatement.getFetchSize();

    if (localResultSet.getType() == 1003)
      paramArrayOfString[0] = "TYPE_FORWARD_ONLY";
    else if (localResultSet.getType() == 1005)
      paramArrayOfString[0] = "TYPE_SCROLL_SENSITIVE";
    else if (localResultSet.getType() == 1004) {
      paramArrayOfString[0] = "TYPE_SCROLL_INSENSITIVE";
    }
    if (paramInt2 > 0)
    {
      int i = 0;
      for (; i < paramInt2; ++i)
      {
        localResultSet.next();
      }

      paramArrayOfInt2[0] = i;
    }

    paramArrayOfResultSet[0] = localResultSet;
  }
}
