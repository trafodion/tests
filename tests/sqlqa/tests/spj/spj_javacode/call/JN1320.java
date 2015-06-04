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
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class JN1320
{
  public static void N1320(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str1 = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str1);
    } catch (Exception localException) {
      System.out.println("ex.toString is: " + localException.toString());
      System.out.println("ex.printStackTrace is: ");
      localException.printStackTrace();
    }

    try
    {
      Statement localStatement = localConnection.createStatement();
      String str2 = "delete from testtab";
      localStatement.executeUpdate(str2);

      for (int i = 1; i <= 10; i++)
      {
        String str3 = " insert into cat.javaqa.testtab values(33,'AAA Computers', 1234567890,'San Francisco', 'programmer',  123456789,  32766, date '2001-10-31',  time '10:10:10', timestamp '2001-10-10 10:10:10.00', 123456789987654321, 3.40E+37, 3.0125E+18, 1.78145E+75, 8765432.45678,  8765478.56895,  987654321.0,  123456789.0)";
        localStatement.executeUpdate(str3);

        String str4 = "update cat.javaqa.testtab set e_name = 'Hewlett Packard', e_num = 122121212,e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00',e_long = 123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15,e_double =  1.78145E+69, e_numeric = 8765432.54321,e_decimal = 8765478.98765,e_numeric1 =  987654321.0,e_decimal1 =  123456789.0 where e_id=33";
        localStatement.executeUpdate(str4);
        try
        {
          String str5 = "SELECT distinct e_name from testtab";
          ResultSet localResultSet = null;
          localResultSet = localStatement.executeQuery(str5);
          localResultSet.next();
          paramString = localResultSet.getString(1);
          paramArrayOfString[0] = paramString;
          localStatement.close();
        }
        catch (SQLException localSQLException2)
        {
          System.out.println("We got an exception while getting a result:this shouldn't happen: we've done something really bad.");
          localSQLException2.printStackTrace();
          System.exit(1);
        }

        localConnection.close();
      }
    } catch (SQLException localSQLException1) {
      localSQLException1.printStackTrace();
    }
  }
}