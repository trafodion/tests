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
import java.math.BigDecimal;
import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Timestamp;

public class RS210
{
  public static void main(String[] paramArrayOfString)
  {
  }

  public static void RS210(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6, ResultSet[] paramArrayOfResultSet7, ResultSet[] paramArrayOfResultSet8, ResultSet[] paramArrayOfResultSet9, ResultSet[] paramArrayOfResultSet10, ResultSet[] paramArrayOfResultSet11, ResultSet[] paramArrayOfResultSet12, ResultSet[] paramArrayOfResultSet13, ResultSet[] paramArrayOfResultSet14, ResultSet[] paramArrayOfResultSet15, ResultSet[] paramArrayOfResultSet16, ResultSet[] paramArrayOfResultSet17, ResultSet[] paramArrayOfResultSet18, ResultSet[] paramArrayOfResultSet19, ResultSet[] paramArrayOfResultSet20, ResultSet[] paramArrayOfResultSet21, ResultSet[] paramArrayOfResultSet22, ResultSet[] paramArrayOfResultSet23, ResultSet[] paramArrayOfResultSet24, ResultSet[] paramArrayOfResultSet25)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    String str2 = "select * from d4";
    paramArrayOfResultSet1[0] = localStatement.executeQuery(str2);
    localStatement = localConnection.createStatement();
    String str3 = "select * from testtab";
    paramArrayOfResultSet2[0] = localStatement.executeQuery(str3);
    localStatement = localConnection.createStatement();
    String str4 = "select * from i3";
    paramArrayOfResultSet3[0] = localStatement.executeQuery(str4);
    localStatement = localConnection.createStatement();
    String str5 = "select * from trn";
    paramArrayOfResultSet4[0] = localStatement.executeQuery(str5);
    localStatement = localConnection.createStatement();
    String str6 = "select * from trs";
    paramArrayOfResultSet5[0] = localStatement.executeQuery(str6);
    localStatement = localConnection.createStatement();
    String str7 = "select * from t6";
    paramArrayOfResultSet6[0] = localStatement.executeQuery(str7);
    localStatement = localConnection.createStatement();
    String str8 = "select * from d3";
    paramArrayOfResultSet7[0] = localStatement.executeQuery(str8);
    localStatement = localConnection.createStatement();
    String str9 = "select * from daytab";
    paramArrayOfResultSet8[0] = localStatement.executeQuery(str9);
    localStatement = localConnection.createStatement();
    String str10 = "select * from tab2000";
    paramArrayOfResultSet9[0] = localStatement.executeQuery(str10);
    localStatement = localConnection.createStatement();
    String str11 = "select * from jdbctest";
    paramArrayOfResultSet10[0] = localStatement.executeQuery(str11);
    localStatement = localConnection.createStatement();
    String str12 = "select * from stday";
    paramArrayOfResultSet11[0] = localStatement.executeQuery(str12);
    localStatement = localConnection.createStatement();
    String str13 = "select * from sthour";
    paramArrayOfResultSet12[0] = localStatement.executeQuery(str13);
    localStatement = localConnection.createStatement();
    String str14 = "select * from stmin";
    paramArrayOfResultSet13[0] = localStatement.executeQuery(str14);
    localStatement = localConnection.createStatement();
    String str15 = "select * from stsec";
    paramArrayOfResultSet14[0] = localStatement.executeQuery(str15);
    localStatement = localConnection.createStatement();
    String str16 = "select * from nshour";
    paramArrayOfResultSet15[0] = localStatement.executeQuery(str16);
    localStatement = localConnection.createStatement();
    String str17 = "select * from nsminute";
    paramArrayOfResultSet16[0] = localStatement.executeQuery(str17);
    localStatement = localConnection.createStatement();
    String str18 = "select * from nssecond";
    paramArrayOfResultSet17[0] = localStatement.executeQuery(str18);
    localStatement = localConnection.createStatement();
    String str19 = "select * from str_num";
    paramArrayOfResultSet18[0] = localStatement.executeQuery(str19);
    localStatement = localConnection.createStatement();
    String str20 = "select * from d4";
    paramArrayOfResultSet19[0] = localStatement.executeQuery(str20);
    localStatement = localConnection.createStatement();
    String str21 = "select * from s2";
    paramArrayOfResultSet20[0] = localStatement.executeQuery(str21);
    localStatement = localConnection.createStatement();
    String str22 = "select * from datetime_interval";
    paramArrayOfResultSet21[0] = localStatement.executeQuery(str22);
    localStatement = localConnection.createStatement();
    String str23 = "select * from sample";
    paramArrayOfResultSet22[0] = localStatement.executeQuery(str23);
    localStatement = localConnection.createStatement();
    String str24 = "select * from tbint";
    paramArrayOfResultSet23[0] = localStatement.executeQuery(str24);
    localStatement = localConnection.createStatement();
    String str25 = "select * from b212";
    paramArrayOfResultSet24[0] = localStatement.executeQuery(str25);
    localStatement = localConnection.createStatement();
    String str26 = "select * from t4";
    paramArrayOfResultSet25[0] = localStatement.executeQuery(str26);
    localStatement = localConnection.createStatement();
  }

  public static void RS348(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6, ResultSet[] paramArrayOfResultSet7, ResultSet[] paramArrayOfResultSet8, ResultSet[] paramArrayOfResultSet9, ResultSet[] paramArrayOfResultSet10, ResultSet[] paramArrayOfResultSet11, ResultSet[] paramArrayOfResultSet12, ResultSet[] paramArrayOfResultSet13, ResultSet[] paramArrayOfResultSet14, ResultSet[] paramArrayOfResultSet15, ResultSet[] paramArrayOfResultSet16, ResultSet[] paramArrayOfResultSet17)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();

    localStatement = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement.executeQuery("select e_name from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement.executeQuery("select e_num from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet3[0] = localStatement.executeQuery("select e_city from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet4[0] = localStatement.executeQuery("select e_title from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet5[0] = localStatement.executeQuery("select e_salary from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet6[0] = localStatement.executeQuery("select e_code from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet7[0] = localStatement.executeQuery("select e_date from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet8[0] = localStatement.executeQuery("select e_time from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet9[0] = localStatement.executeQuery("select e_tstamp from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet10[0] = localStatement.executeQuery("select e_long from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet11[0] = localStatement.executeQuery("select e_float from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet12[0] = localStatement.executeQuery("select e_real from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet13[0] = localStatement.executeQuery("select e_double from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet14[0] = localStatement.executeQuery("select e_numeric from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet15[0] = localStatement.executeQuery("select e_decimal from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet16[0] = localStatement.executeQuery("select e_numeric1 from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet17[0] = localStatement.executeQuery("select e_decimal1 from testtab");
  }

  public static void RS348a(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6, ResultSet[] paramArrayOfResultSet7, ResultSet[] paramArrayOfResultSet8, ResultSet[] paramArrayOfResultSet9, ResultSet[] paramArrayOfResultSet10, ResultSet[] paramArrayOfResultSet11, ResultSet[] paramArrayOfResultSet12, ResultSet[] paramArrayOfResultSet13, ResultSet[] paramArrayOfResultSet14, ResultSet[] paramArrayOfResultSet15, ResultSet[] paramArrayOfResultSet16, ResultSet[] paramArrayOfResultSet17)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();

    localConnection.setAutoCommit(false);

    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement.executeQuery("select e_name from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement.executeQuery("select e_num from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet3[0] = localStatement.executeQuery("select e_city from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet4[0] = localStatement.executeQuery("select e_title from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet5[0] = localStatement.executeQuery("select e_salary from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet6[0] = localStatement.executeQuery("select e_code from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet7[0] = localStatement.executeQuery("select e_date from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet8[0] = localStatement.executeQuery("select e_time from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet9[0] = localStatement.executeQuery("select e_tstamp from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet10[0] = localStatement.executeQuery("select e_long from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet11[0] = localStatement.executeQuery("select e_float from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet12[0] = localStatement.executeQuery("select e_real from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet13[0] = localStatement.executeQuery("select e_double from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet14[0] = localStatement.executeQuery("select e_numeric from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet15[0] = localStatement.executeQuery("select e_decimal from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet16[0] = localStatement.executeQuery("select e_numeric1 from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet17[0] = localStatement.executeQuery("select e_decimal1 from testtab");

    localConnection.rollback();
  }

  public static void RS348b(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6, ResultSet[] paramArrayOfResultSet7, ResultSet[] paramArrayOfResultSet8, ResultSet[] paramArrayOfResultSet9, ResultSet[] paramArrayOfResultSet10, ResultSet[] paramArrayOfResultSet11, ResultSet[] paramArrayOfResultSet12, ResultSet[] paramArrayOfResultSet13, ResultSet[] paramArrayOfResultSet14, ResultSet[] paramArrayOfResultSet15, ResultSet[] paramArrayOfResultSet16, ResultSet[] paramArrayOfResultSet17)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();

    localConnection.setAutoCommit(false);

    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement.executeQuery("select e_name from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement.executeQuery("select e_num from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet3[0] = localStatement.executeQuery("select e_city from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet4[0] = localStatement.executeQuery("select e_title from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet5[0] = localStatement.executeQuery("select e_salary from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet6[0] = localStatement.executeQuery("select e_code from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet7[0] = localStatement.executeQuery("select e_date from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet8[0] = localStatement.executeQuery("select e_time from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet9[0] = localStatement.executeQuery("select e_tstamp from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet10[0] = localStatement.executeQuery("select e_long from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet11[0] = localStatement.executeQuery("select e_float from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet12[0] = localStatement.executeQuery("select e_real from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet13[0] = localStatement.executeQuery("select e_double from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet14[0] = localStatement.executeQuery("select e_numeric from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet15[0] = localStatement.executeQuery("select e_decimal from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet16[0] = localStatement.executeQuery("select e_numeric1 from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet17[0] = localStatement.executeQuery("select e_decimal1 from testtab");

    localConnection.rollback();
  }

  public static void RS349(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();

    localStatement = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement.executeQuery("select a from s32");
  }

  public static void RS356(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from cat.javaqa.bigb";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    ResultSet localResultSet = localStatement.executeQuery(str2);
    ResultSetMetaData localResultSetMetaData = paramArrayOfResultSet[0].getMetaData();

    //PrintColumnTypes.printColTypes(localResultSetMetaData);
    System.out.println("");

    int i = localResultSetMetaData.getColumnCount();

    for (int j = 1; j <= i; ++j) {
      if (j > 1) System.out.print(",  ");
      String str3 = localResultSetMetaData.getColumnName(j);
      System.out.print(str3);
    }

    System.out.println("");
  }

  public static void RS354(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6, ResultSet[] paramArrayOfResultSet7, ResultSet[] paramArrayOfResultSet8, ResultSet[] paramArrayOfResultSet9, ResultSet[] paramArrayOfResultSet10, ResultSet[] paramArrayOfResultSet11, ResultSet[] paramArrayOfResultSet12)
    throws Exception
  {
    String str = "jdbc:default:connection";
    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();
    try
    {
      localStatement.executeUpdate("drop table sample");
    }
    catch (SQLException localSQLException)
    {
    }
    localStatement.executeUpdate("create table sample (c1 char(20) not null primary key, c2 smallint not null, c3 integer, c4 largeint, c5 varchar(120), c6 numeric(10,2), c7 decimal(10,2),c8 date, c9 time, c10 timestamp, c11 float, c12 double precision)");
    localStatement.executeUpdate("insert into sample values('Moe', 100, 12345678, 123456789012, 'Moe', 100.12, 100.12, {d '2000-05-16'}, {t '10:11:12'}, {ts '2000-05-06 10:11:12.0'}, 100.12, 100.12)");
    localStatement.executeUpdate("insert into sample values('Larry', -100, -12345678, -123456789012, 'Larry', -100.12, -100.12, {d '2000-05-16'}, {t '10:11:12'}, {ts '2000-05-06 10:11:12'}, -100.12, -100.12)");
    localStatement.executeUpdate("insert into sample values('Curly', 100, -12345678, 123456789012, 'Curly', -100.12, 100.12, {d '2000-05-16'}, {t '10:11:12'}, {ts '2000-05-06 10:11:12'}, -100.12, 100.12)");
    localStatement.executeUpdate("insert into sample values('Smith', 125, -987654321, 987654321233, 'Smith', -125.99, 125.32, {d '2005-10-20'}, {t '12:10:10'}, {ts '2005-10-20 12:45:45'}, -125.32, 124.98)");

    for (int i = 0; i < 10; ++i)
    {
      PreparedStatement localPreparedStatement;
      DatabaseMetaData localDatabaseMetaData;
      switch (i)
      {
      case 0:
        System.out.println("");
        System.out.println("Simple Select ");
        localStatement = localConnection.createStatement();
        paramArrayOfResultSet1[0] = localStatement.executeQuery("select * from sample");
        break;
      case 1:
        System.out.println("");
        System.out.println("Parameterized Select - CHAR");
        localPreparedStatement = localConnection.prepareStatement("select c1, c2 from sample where c1 = ?");
        localPreparedStatement.setString(1, "Moe");
        paramArrayOfResultSet2[0] = localPreparedStatement.executeQuery();
        break;
      case 2:
        System.out.println("");
        System.out.println("Parameterized Select - INT");
        localPreparedStatement = localConnection.prepareStatement("select c1, c2, c3 from sample where c2 = ?  or c2 = ? or c2 = ?");
        localPreparedStatement.setInt(1, 100);
        localPreparedStatement.setInt(2, -100);
        localPreparedStatement.setInt(3, 125);
        paramArrayOfResultSet3[0] = localPreparedStatement.executeQuery();
        break;
      case 3:
        System.out.println("");
        System.out.println("Parameterized Select - TIMESTAMP");
        localPreparedStatement = localConnection.prepareStatement("select c1, c2, c3, c10 from sample where c10 = ?");
        localPreparedStatement.setTimestamp(1, Timestamp.valueOf("2000-05-06 10:11:12.0"));
        paramArrayOfResultSet4[0] = localPreparedStatement.executeQuery();
        break;
      case 4:
        System.out.println("");
        System.out.println("Parameterized Select - DECIMAL");
        localPreparedStatement = localConnection.prepareStatement("select c1, c2, c3, c7 from sample where c7 = ? or c7 = ?");
        localPreparedStatement.setBigDecimal(1, new BigDecimal("100.12"));
        localPreparedStatement.setBigDecimal(2, new BigDecimal("-100.12"));
        paramArrayOfResultSet5[0] = localPreparedStatement.executeQuery();
        break;
      case 5:
        System.out.println("");
        System.out.println("Parameterized Select - NUMERIC");
        localPreparedStatement = localConnection.prepareStatement("select c1, c2, c3, c6 from sample where c6 = ? or c6 = ?");
        localPreparedStatement.setBigDecimal(1, new BigDecimal("100.12"));
        localPreparedStatement.setBigDecimal(2, new BigDecimal("-100.12"));
        paramArrayOfResultSet6[0] = localPreparedStatement.executeQuery();
        break;
      case 6:
        System.out.println("");
        System.out.println("getTypeInfo() ");
        localDatabaseMetaData = localConnection.getMetaData();
        paramArrayOfResultSet7[0] = localDatabaseMetaData.getTypeInfo();
        break;
      case 7:
        System.out.println("");
        System.out.println("getCatalogs()");
        localDatabaseMetaData = localConnection.getMetaData();
        paramArrayOfResultSet8[0] = localDatabaseMetaData.getCatalogs();
        break;
      case 8:
        System.out.println("");
        System.out.println("getTables() ");
        localDatabaseMetaData = localConnection.getMetaData();
        paramArrayOfResultSet9[0] = localDatabaseMetaData.getTables(null, null, "SAM%", null);
        break;
      case 9:
        System.out.println("");
        System.out.println("getColumns()");
        localDatabaseMetaData = localConnection.getMetaData();
        paramArrayOfResultSet10[0] = localDatabaseMetaData.getColumns(null, null, "SAMPLE", "%");
      }
    }
  }

  public static void RS355(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";
    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();

    ResultSetMetaData localResultSetMetaData = paramArrayOfResultSet[0].getMetaData();

    System.out.println("No. of Columns " + localResultSetMetaData.getColumnCount());
    for (int j = 1; j <= localResultSetMetaData.getColumnCount(); ++j)
    {
      System.out.println("Column " + j + " Data Type: " + localResultSetMetaData.getColumnTypeName(j) + " Name: " + localResultSetMetaData.getColumnName(j));
    }
    System.out.println("Fetching rows...");
    int i = 0;
    while (paramArrayOfResultSet[0].next())
    {
      ++i;

      for (int j = 1; j <= localResultSetMetaData.getColumnCount(); ++j);
    }
  }

  public static void RS348L(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6, ResultSet[] paramArrayOfResultSet7, ResultSet[] paramArrayOfResultSet8, ResultSet[] paramArrayOfResultSet9, ResultSet[] paramArrayOfResultSet10, ResultSet[] paramArrayOfResultSet11, ResultSet[] paramArrayOfResultSet12, ResultSet[] paramArrayOfResultSet13, ResultSet[] paramArrayOfResultSet14, ResultSet[] paramArrayOfResultSet15, ResultSet[] paramArrayOfResultSet16, ResultSet[] paramArrayOfResultSet17)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");

    localStatement = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement.executeQuery("select e_name from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement.executeQuery("select e_num from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet3[0] = localStatement.executeQuery("select e_city from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet4[0] = localStatement.executeQuery("select e_title from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet5[0] = localStatement.executeQuery("select e_salary from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet6[0] = localStatement.executeQuery("select e_code from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet7[0] = localStatement.executeQuery("select e_date from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet8[0] = localStatement.executeQuery("select e_time from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet9[0] = localStatement.executeQuery("select e_tstamp from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet10[0] = localStatement.executeQuery("select e_long from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet11[0] = localStatement.executeQuery("select e_float from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet12[0] = localStatement.executeQuery("select e_real from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet13[0] = localStatement.executeQuery("select e_double from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet14[0] = localStatement.executeQuery("select e_numeric from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet15[0] = localStatement.executeQuery("select e_decimal from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet16[0] = localStatement.executeQuery("select e_numeric1 from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet17[0] = localStatement.executeQuery("select e_decimal1 from testtab");
  }

  public static void RS348M(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6, ResultSet[] paramArrayOfResultSet7, ResultSet[] paramArrayOfResultSet8, ResultSet[] paramArrayOfResultSet9, ResultSet[] paramArrayOfResultSet10, ResultSet[] paramArrayOfResultSet11, ResultSet[] paramArrayOfResultSet12, ResultSet[] paramArrayOfResultSet13, ResultSet[] paramArrayOfResultSet14, ResultSet[] paramArrayOfResultSet15, ResultSet[] paramArrayOfResultSet16, ResultSet[] paramArrayOfResultSet17)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");

    localStatement = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement.executeQuery("select e_name from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement.executeQuery("select e_num from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet3[0] = localStatement.executeQuery("select e_city from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet4[0] = localStatement.executeQuery("select e_title from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet5[0] = localStatement.executeQuery("select e_salary from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet6[0] = localStatement.executeQuery("select e_code from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet7[0] = localStatement.executeQuery("select e_date from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet8[0] = localStatement.executeQuery("select e_time from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet9[0] = localStatement.executeQuery("select e_tstamp from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet10[0] = localStatement.executeQuery("select e_long from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet11[0] = localStatement.executeQuery("select e_float from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet12[0] = localStatement.executeQuery("select e_real from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet13[0] = localStatement.executeQuery("select e_double from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet14[0] = localStatement.executeQuery("select e_numeric from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet15[0] = localStatement.executeQuery("select e_decimal from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet16[0] = localStatement.executeQuery("select e_numeric1 from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet17[0] = localStatement.executeQuery("select e_decimal1 from testtab");
    localConnection.close();
  }

  public static void N0165()
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    Connection localConnection = DriverManager.getConnection(str1);
    String str2 = "CREATE PROCEDURE SPJTEST(VARCHAR(50), OUT VARCHAR(50)) EXTERNAL NAME 'Procs.N0200(java.lang.String,java.lang.String[])'  EXTERNAL PATH '/usr/spjqa/Testware/Class'  LANGUAGE JAVA PARAMETER STYLE JAVA CONTAINS SQL NO ISOLATE";

    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate(str2);
  }
}
