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
import java.sql.SQLException;
import java.sql.Statement;

public class RS320
{
  public static void main(String[] paramArrayOfString)
  {
  }

  public static void RS205(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    try
    {
      Statement localStatement1 = localConnection.createStatement();
      paramArrayOfResultSet1[0] = localStatement1.executeQuery("SELECT cast(date_key as varchar(11)),cast(date_col as varchar(11)),cast(time_col as varchar(9)),cast(timestamp_col as varchar(27)),cast(interval_year as varchar(3)),cast(yr2_to_mo as varchar(7)),cast(yr6_to_mo as varchar(10)),cast(yr16_to_mo as varchar(20)),cast(year18 as varchar(19))from datetime_interval where date_key = date '2999-12-30' for update");
    }
    catch (SQLException localSQLException1)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException1.getMessage());
      localSQLException1.getNextException();
    }

    try
    {
      Statement localStatement2 = localConnection.createStatement();
      paramArrayOfResultSet2[0] = localStatement2.executeQuery("SELECT cast(date_key as varchar(11)),cast(day2 as varchar(4)),cast(day18 as varchar(20)),cast(day16_to_hr as varchar(21)),cast(day14_to_min as varchar(21)),cast(day5_to_second6 as varchar(23)),cast(hour2 as varchar(4)),cast(hour18 as varchar(20)),cast(hour16_to_min as varchar(21)),cast(hour14_to_ss0 as varchar(22)),cast(hour10_to_second4 as varchar(23))from datetime_interval where date_key = date '1011-07-18' for update");
    }
    catch (SQLException localSQLException2)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException2.getMessage());
      localSQLException2.getNextException();
    }

    try
    {
      Statement localStatement3 = localConnection.createStatement();
      paramArrayOfResultSet3[0] = localStatement3.executeQuery("SELECT cast(date_key as varchar(11)),cast(min2 as varchar(4)),cast(min18 as varchar(20)),cast(min13_s3 as varchar(22)),cast(min16_s0 as varchar(21)),cast(seconds as varchar(11)),cast(seconds5 as varchar(14)),cast(seconds18 as varchar(20)),cast(seconds15 as varchar(21))from datetime_interval where date_key = date '7009-02-01' order by 1 for update");
    }
    catch (SQLException localSQLException3)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException3.getMessage());
      localSQLException3.getNextException();
    }
  }

  public static void RS206(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);

    Statement localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement1.executeQuery("SELECT cast(date_key as char(11)),cast(date_col as char(11)),cast(time_col as char(9)),cast(timestamp_col as char(27)),cast(interval_year as char(3)),cast(yr2_to_mo as char(7)),cast(yr6_to_mo as char(10)),cast(yr16_to_mo as char(20)),cast(year18 as char(19))from datetime_interval where date_key = date '2999-12-30' for update");

    Statement localStatement2 = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement2.executeQuery("SELECT cast(date_key as char(11)),cast(day2 as char(4)),cast(day18 as char(20)),cast(day16_to_hr as char(21)),cast(day14_to_min as char(21)),cast(day5_to_second6 as char(23)),cast(hour2 as char(4)),cast(hour18 as char(20)),cast(hour16_to_min as char(21)),cast(hour14_to_ss0 as char(22)),cast(hour10_to_second4 as char(23))from datetime_interval where date_key = date '1011-07-18' for update");

    Statement localStatement3 = localConnection.createStatement();
    paramArrayOfResultSet3[0] = localStatement3.executeQuery("SELECT cast(date_key as char(11)),cast(min2 as char(4)),cast(min18 as char(20)),cast(min13_s3 as char(22)),cast(min16_s0 as char(21)),cast(seconds as char(11)),cast(seconds5 as char(14)),cast(seconds18 as char(20)),cast(seconds15 as char(21))from datetime_interval where date_key = date '7009-02-01' order by 1 for update");
  }

  public static void RS207(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);

    Statement localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement1.executeQuery("SELECT date_key,date_col,time_col,timestamp_col ,interval_year ,yr2_to_mo,yr6_to_mo,yr16_to_mo,year18 from datetime_interval where date_key = date '2999-12-30' for update");

    Statement localStatement2 = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement2.executeQuery("SELECT date_key,day2,day18,day16_to_hr,day14_to_min,day5_to_second6,hour2,hour18,hour16_to_min,hour14_to_ss0,hour10_to_second4 from datetime_interval where date_key = date '1011-07-18' for update");

    Statement localStatement3 = localConnection.createStatement();
    paramArrayOfResultSet3[0] = localStatement3.executeQuery("SELECT date_key,min2,min18,min13_s3 ,min16_s0 ,seconds ,seconds5,seconds18,seconds15 from datetime_interval where date_key = date '7009-02-01' order by 1 for update");
  }

  public static void RS327(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select * from b32";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS328(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select * from b2pns03";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS315(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select * from t5";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS316(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);
      Statement localStatement = localConnection.createStatement();
      String str2 = "select * from t6";
      paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
    }
    catch (SQLException localSQLException)
    {
      System.out.println("+++++++++SQLException:++++++++++ ");
      System.out.println("Sqlcode  ==> " + localSQLException.getErrorCode());
      System.out.println("Message  ==> " + localSQLException.getMessage());
      System.out.println("Sqlstate ==> " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void RS317(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);
      Statement localStatement = localConnection.createStatement();
      String str2 = "select * from b2";
      paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
    }
    catch (SQLException localSQLException)
    {
      System.out.println("+++++++++SQLException:++++++++++ ");
      System.out.println("Sqlcode  ==> " + localSQLException.getErrorCode());
      System.out.println("Message  ==> " + localSQLException.getMessage());
      System.out.println("Sqlstate ==> " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void RS318(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6, ResultSet[] paramArrayOfResultSet7, ResultSet[] paramArrayOfResultSet8, ResultSet[] paramArrayOfResultSet9, ResultSet[] paramArrayOfResultSet10, ResultSet[] paramArrayOfResultSet11, ResultSet[] paramArrayOfResultSet12, ResultSet[] paramArrayOfResultSet13, ResultSet[] paramArrayOfResultSet14, ResultSet[] paramArrayOfResultSet15, ResultSet[] paramArrayOfResultSet16, ResultSet[] paramArrayOfResultSet17, ResultSet[] paramArrayOfResultSet18, ResultSet[] paramArrayOfResultSet19, ResultSet[] paramArrayOfResultSet20, ResultSet[] paramArrayOfResultSet21, ResultSet[] paramArrayOfResultSet22, ResultSet[] paramArrayOfResultSet23, ResultSet[] paramArrayOfResultSet24, ResultSet[] paramArrayOfResultSet25, ResultSet[] paramArrayOfResultSet26, ResultSet[] paramArrayOfResultSet27, ResultSet[] paramArrayOfResultSet28, ResultSet[] paramArrayOfResultSet29, ResultSet[] paramArrayOfResultSet30, ResultSet[] paramArrayOfResultSet31, ResultSet[] paramArrayOfResultSet32, ResultSet[] paramArrayOfResultSet33, ResultSet[] paramArrayOfResultSet34, ResultSet[] paramArrayOfResultSet35, ResultSet[] paramArrayOfResultSet36, ResultSet[] paramArrayOfResultSet37, ResultSet[] paramArrayOfResultSet38, ResultSet[] paramArrayOfResultSet39, ResultSet[] paramArrayOfResultSet40)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement1 = localConnection.createStatement();
    String str2 = "select * from nsyear";
    paramArrayOfResultSet1[0] = localStatement1.executeQuery(str2);

    Statement localStatement2 = localConnection.createStatement();
    String str3 = "select * from nsmonth";
    paramArrayOfResultSet2[0] = localStatement2.executeQuery(str3);

    Statement localStatement3 = localConnection.createStatement();
    String str4 = "select * from nsday";
    paramArrayOfResultSet3[0] = localStatement3.executeQuery(str4);

    Statement localStatement4 = localConnection.createStatement();
    String str5 = "select from nshour";
    paramArrayOfResultSet4[0] = localStatement4.executeQuery(str5);

    Statement localStatement5 = localConnection.createStatement();
    String str6 = "select * from nsminute";
    paramArrayOfResultSet5[0] = localStatement5.executeQuery(str6);

    Statement localStatement6 = localConnection.createStatement();
    String str7 = "select * from nssecond";
    paramArrayOfResultSet6[0] = localStatement6.executeQuery(str7);

    Statement localStatement7 = localConnection.createStatement();
    String str8 = "select styear";
    paramArrayOfResultSet7[0] = localStatement7.executeQuery(str8);

    Statement localStatement8 = localConnection.createStatement();
    String str9 = "select * from stmonth";
    paramArrayOfResultSet8[0] = localStatement8.executeQuery(str9);

    Statement localStatement9 = localConnection.createStatement();
    String str10 = "select * from stday";
    paramArrayOfResultSet9[0] = localStatement9.executeQuery(str10);

    Statement localStatement10 = localConnection.createStatement();
    String str11 = "select * from sthour";
    paramArrayOfResultSet10[0] = localStatement10.executeQuery(str11);

    Statement localStatement11 = localConnection.createStatement();
    String str12 = "select * from stmin";
    paramArrayOfResultSet11[0] = localStatement11.executeQuery(str12);

    Statement localStatement12 = localConnection.createStatement();
    String str13 = "select * from stsec";
    paramArrayOfResultSet12[0] = localStatement12.executeQuery(str13);

    Statement localStatement13 = localConnection.createStatement();
    String str14 = "select * from daytab";
    paramArrayOfResultSet13[0] = localStatement13.executeQuery(str14);

    Statement localStatement14 = localConnection.createStatement();
    String str15 = "select * from nsfrac";
    paramArrayOfResultSet14[0] = localStatement14.executeQuery(str15);

    Statement localStatement15 = localConnection.createStatement();
    String str16 = "select * from tbint";
    paramArrayOfResultSet15[0] = localStatement15.executeQuery(str16);

    Statement localStatement16 = localConnection.createStatement();
    String str17 = "select extract (year from ts),extract (year from ts1),extract (year from ts2),extract (year from ts3),extract (year from ts4),extract (year from ts5),extract (year from ts6),extract (year from ytosec),extract (year from ytomin),extract (year from ytohr),extract (year from ytoday),extract (year from ytomon),extract (year from y) from styear";

    paramArrayOfResultSet16[0] = localStatement16.executeQuery(str17);

    Statement localStatement17 = localConnection.createStatement();
    String str18 = "select extract (month from montof),extract (month from montof1),extract (month from montof2),extract (month from montof3),extract (month from montof4),extract (month from montof5),extract (month from montof6),extract (month from montosec),extract (month from montomin),extract (month from montohr),extract (month from montoday),extract (month from m) from stmonth";

    paramArrayOfResultSet17[0] = localStatement17.executeQuery(str18);

    Statement localStatement18 = localConnection.createStatement();
    String str19 = "select extract (month from ts),extract (month from ts1),extract (month from ts2),extract (month from ts3),extract (month from ts4),extract (month from ts5),extract (month from ts6),extract (month from ytosec),extract (month from ytomin),extract (month from ytohr),extract (month from ytoday),extract (month from ytomon)  from styear";

    paramArrayOfResultSet18[0] = localStatement18.executeQuery(str19);

    Statement localStatement19 = localConnection.createStatement();
    String str20 = "select extract (hour from htof),extract (hour from htof1),extract (hour from htof2),extract (hour from htof3),extract (hour from htof4),extract (hour from htof5),extract (hour from htof6),extract (hour from htosec),extract (hour from htomin),extract (hour from h)  from sthour";

    paramArrayOfResultSet19[0] = localStatement19.executeQuery(str20);

    Statement localStatement20 = localConnection.createStatement();
    String str21 = "select extract (year from ts),extract (year from ts1),extract (year from ts2),extract (year from ts3),extract (year from ts4),extract (year from ts5),extract (year from ts6),extract (year from ytosec),extract (year from ytomin),extract (year from ytohr),extract (year from ytoday),extract (year from ytomon),extract (year from y) from styear";

    paramArrayOfResultSet20[0] = localStatement20.executeQuery(str21);

    Statement localStatement21 = localConnection.createStatement();
    String str22 = "select extract (month from montof),extract (month from montof1),extract (month from montof2),extract (month from montof3),extract (month from montof4),extract (month from montof5),extract (month from montof6),extract (month from montosec),extract (month from montomin),extract (month from montohr),extract (month from montoday),extract (month from m)  from stmonth";

    paramArrayOfResultSet21[0] = localStatement21.executeQuery(str22);

    Statement localStatement22 = localConnection.createStatement();
    String str23 = "select extract (month from ts),extract (month from ts1),extract (month from ts2),extract (month from ts3),extract (month from ts4),extract (month from ts5),extract (month from ts6),extract (month from ytosec),extract (month from ytomin),extract (month from ytohr),extract (month from ytoday),extract (month from ytomon)  from styear";

    paramArrayOfResultSet22[0] = localStatement22.executeQuery(str23);

    Statement localStatement23 = localConnection.createStatement();
    String str24 = "select extract (day from daytof),extract (day from daytof1),extract (day from daytof2),extract (day from daytof3),extract (day from daytof4),extract (day from daytof5),extract (day from daytof6),extract (day from daytosec),extract (day from daytomin),extract (day from daytohr),extract (day from d) from stday";

    paramArrayOfResultSet23[0] = localStatement23.executeQuery(str24);

    Statement localStatement24 = localConnection.createStatement();
    String str25 = "select extract (day from montof),extract (day from montof1),extract (day from montof2),extract (day from montof3),extract (day from montof4),extract (day from montof5),extract (day from montof6),extract (day from montosec),extract (day from montomin),extract (day from montohr),extract (day from montoday)  from stmonth";

    paramArrayOfResultSet24[0] = localStatement24.executeQuery(str25);

    Statement localStatement25 = localConnection.createStatement();
    String str26 = "select extract (day from ts),extract (day from ts1),extract (day from ts2),extract (day from ts3),extract (day from ts4),extract (day from ts5),extract (day from ts6),extract (day from ytosec),extract (day from ytomin),extract (day from ytohr),extract (day from ytoday)  from styear";

    paramArrayOfResultSet25[0] = localStatement25.executeQuery(str26);

    Statement localStatement26 = localConnection.createStatement();
    String str27 = "select extract (hour from htof),extract (hour from htof1),extract (hour from htof2),extract (hour from htof3),extract (hour from htof4),extract (hour from htof5),extract (hour from htof6),extract (hour from htosec),extract (hour from htomin),extract (hour from h) from sthour";

    paramArrayOfResultSet26[0] = localStatement26.executeQuery(str27);

    Statement localStatement27 = localConnection.createStatement();
    String str28 = "select extract (hour from daytof),extract (hour from daytof1),extract (hour from daytof2),extract (hour from daytof3),extract (hour from daytof4),extract (hour from daytof5),extract (hour from daytof6),extract (hour from daytosec),extract (hour from daytomin),extract (hour from daytohr)  from stday";

    paramArrayOfResultSet27[0] = localStatement27.executeQuery(str28);

    Statement localStatement28 = localConnection.createStatement();
    String str29 = "select extract (hour from montof),extract (hour from montof1),extract (hour from montof2),extract (hour from montof3),extract (hour from montof4),extract (hour from montof5),extract (hour from montof6),extract (hour from montosec),extract (hour from montomin),extract (hour from montohr)  from stmonth";

    paramArrayOfResultSet28[0] = localStatement28.executeQuery(str29);

    Statement localStatement29 = localConnection.createStatement();
    String str30 = "select extract (hour from ts),extract (hour from ts1),extract (hour from ts2),extract (hour from ts3),extract (hour from ts4),extract (hour from ts5),extract (hour from ts6),extract (hour from ytosec),extract (hour from ytomin),extract (hour from ytohr)  from styear";

    paramArrayOfResultSet29[0] = localStatement29.executeQuery(str30);

    Statement localStatement30 = localConnection.createStatement();
    String str31 = "select extract (minute from mtof),extract (minute from mtof1),extract (minute from mtof2),extract (minute from mtof3),extract (minute from mtof4),extract (minute from mtof5),extract (minute from mtof6),extract (minute from mtosec),extract (minute from m)  from stmin";

    paramArrayOfResultSet30[0] = localStatement30.executeQuery(str31);

    Statement localStatement31 = localConnection.createStatement();
    String str32 = "select extract (minute from htof),extract (minute from htof1),extract (minute from htof2),extract (minute from htof3),extract (minute from htof4),extract (minute from htof5),extract (minute from htof6),extract (minute from htosec),extract (minute from htomin)  from sthour";

    paramArrayOfResultSet31[0] = localStatement31.executeQuery(str32);

    Statement localStatement32 = localConnection.createStatement();
    String str33 = "select extract (minute from daytof),extract (minute from daytof1),extract (minute from daytof2),extract (minute from daytof3),extract (minute from daytof4),extract (minute from daytof5),extract (minute from daytof6),extract (minute from daytosec),extract (minute from daytomin)  from stday";

    paramArrayOfResultSet32[0] = localStatement32.executeQuery(str33);

    Statement localStatement33 = localConnection.createStatement();
    String str34 = "select extract (minute from montof),extract (minute from montof1),extract (minute from montof2),extract (minute from montof3),extract (minute from montof4),extract (minute from montof5),extract (minute from montof6),extract (minute from montosec),extract (minute from montomin)  from stmonth";

    paramArrayOfResultSet33[0] = localStatement33.executeQuery(str34);

    Statement localStatement34 = localConnection.createStatement();
    String str35 = "select extract (minute from ts),extract (minute from ts1),extract (minute from ts2),extract (minute from ts3),extract (minute from ts4),extract (minute from ts5),extract (minute from ts6),extract (minute from ytosec),extract (minute from ytomin)  from styear";

    paramArrayOfResultSet34[0] = localStatement34.executeQuery(str35);

    Statement localStatement35 = localConnection.createStatement();
    String str36 = "select extract (second from stof),extract (second from stof1),extract (second from stof2),extract (second from stof3),extract (second from stof4),extract (second from stof5),extract (second from stof6),extract (second from s)  from stsec";

    paramArrayOfResultSet35[0] = localStatement35.executeQuery(str36);

    Statement localStatement36 = localConnection.createStatement();
    String str37 = "select extract (second from mtof),extract (second from mtof1),extract (second from mtof2),extract (second from mtof3),extract (second from mtof4),extract (second from mtof5),extract (second from mtof6),extract (second from mtosec)  from stmin";

    paramArrayOfResultSet36[0] = localStatement36.executeQuery(str37);

    Statement localStatement37 = localConnection.createStatement();
    String str38 = "select extract (second from htof),extract (second from htof1),extract (second from htof2),extract (second from htof3),extract (second from htof4),extract (second from htof5),extract (second from htof6),extract (second from htosec)  from sthour";

    paramArrayOfResultSet37[0] = localStatement37.executeQuery(str38);

    Statement localStatement38 = localConnection.createStatement();
    String str39 = "select extract (second from daytof),extract (second from daytof1),extract (second from daytof2),extract (second from daytof3),extract (second from daytof4),extract (second from daytof5),extract (second from daytof6),extract (second from daytosec)  from stday";

    paramArrayOfResultSet38[0] = localStatement38.executeQuery(str39);

    Statement localStatement39 = localConnection.createStatement();
    String str40 = "select extract (second from montof),extract (second from montof1),extract (second from montof2),extract (second from montof3),extract (second from montof4),extract (second from montof5),extract (second from montof6),extract (second from montosec)  from stmonth";

    paramArrayOfResultSet39[0] = localStatement39.executeQuery(str40);

    Statement localStatement40 = localConnection.createStatement();
    String str41 = "select extract (second from ts),extract (second from ts1),extract (second from ts2),extract (second from ts3),extract (second from ts4),extract (second from ts5),extract (second from ts6),extract (second from ytosec)  from styear";

    paramArrayOfResultSet40[0] = localStatement40.executeQuery(str41);
  }

  public static void RS350(String[] paramArrayOfString1, String[] paramArrayOfString2, ResultSet[] paramArrayOfResultSet)
    throws SQLException
  {
    Connection localConnection = DriverManager.getConnection("jdbc:default:connection");

    localConnection.createStatement().executeUpdate("CONTROL QUERY DEFAULT STREAM_TIMEOUT '500'");
    PreparedStatement localPreparedStatement = localConnection.prepareStatement("select * from stream(jdbctest)", 1004, 1008, 1);

    ResultSet localResultSet = localPreparedStatement.executeQuery();

    int i = localResultSet.getType();
    if (i == 1004)
      paramArrayOfString1[0] = "TYPE_SCROLL_INSENSITIVE";
    else {
      paramArrayOfString1[0] = "Not an expected SPJ ResultSet Type";
    }
    int j = localResultSet.getConcurrency();
    if (j == 1008)
      paramArrayOfString2[0] = "CONCUR_UPDATABLE";
    else
      paramArrayOfString2[0] = "Not an expected SPJ ResultSet Concurrency";
    paramArrayOfResultSet[0] = localResultSet;
  }

  public static void RS351(String[] paramArrayOfString1, String[] paramArrayOfString2, ResultSet[] paramArrayOfResultSet)
    throws SQLException
  {
    Connection localConnection = DriverManager.getConnection("jdbc:default:connection");

    localConnection.createStatement().executeUpdate("CONTROL QUERY DEFAULT STREAM_TIMEOUT '500'");
    PreparedStatement localPreparedStatement = localConnection.prepareStatement("select * from stream(jdbctest)", 1003, 1008, 1);

    ResultSet localResultSet = localPreparedStatement.executeQuery();

    int i = localResultSet.getType();
    if (i == 1003)
      paramArrayOfString1[0] = "TYPE_FORWARD_ONLY";
    else {
      paramArrayOfString1[0] = "Not an expected SPJ ResultSet Type";
    }
    int j = localResultSet.getConcurrency();
    if (j == 1008)
      paramArrayOfString2[0] = "CONCUR_UPDATABLE";
    else
      paramArrayOfString2[0] = "Not an expected SPJ ResultSet Concurrency";
    paramArrayOfResultSet[0] = localResultSet;
  }

  public static void RS352(String[] paramArrayOfString1, String[] paramArrayOfString2, ResultSet[] paramArrayOfResultSet)
    throws SQLException
  {
    Connection localConnection = DriverManager.getConnection("jdbc:default:connection");

    PreparedStatement localPreparedStatement = localConnection.prepareStatement("select * from stream(jdbctest)", 1004, 1008, 1);

    ResultSet localResultSet = localPreparedStatement.executeQuery();

    int i = localResultSet.getType();
    if (i == 1004)
      paramArrayOfString1[0] = "TYPE_SCROLL_INSENSITIVE";
    else {
      paramArrayOfString1[0] = "Not an expected SPJ ResultSet Type";
    }
    int j = localResultSet.getConcurrency();
    if (j == 1008)
      paramArrayOfString2[0] = "CONCUR_UPDATABLE";
    else
      paramArrayOfString2[0] = "Not an expected SPJ ResultSet Concurrency";
    paramArrayOfResultSet[0] = localResultSet;
  }

  public static void RS353(String[] paramArrayOfString1, String[] paramArrayOfString2, ResultSet[] paramArrayOfResultSet)
    throws SQLException
  {
    Connection localConnection = DriverManager.getConnection("jdbc:default:connection");

    localConnection.createStatement().executeUpdate("CONTROL QUERY DEFAULT STREAM_TIMEOUT '500'");
    PreparedStatement localPreparedStatement = localConnection.prepareStatement("select * from stream(jdbctest)", 1004, 1008, 1);

    ResultSet localResultSet = localPreparedStatement.executeQuery();

    int i = localResultSet.getType();
    if (i == 1004)
      paramArrayOfString1[0] = "TYPE_SCROLL_INSENSITIVE";
    else {
      paramArrayOfString1[0] = "Not an expected SPJ ResultSet Type";
    }
    int j = localResultSet.getConcurrency();
    if (j == 1008)
      paramArrayOfString2[0] = "CONCUR_UPDATABLE";
    else
      paramArrayOfString2[0] = "Not an expected SPJ ResultSet Concurrency";
    paramArrayOfResultSet[0] = localResultSet;
  }

  public static void RS350a(ResultSet[] paramArrayOfResultSet)
    throws SQLException
  {
    Connection localConnection = DriverManager.getConnection("jdbc:default:connection");

    PreparedStatement localPreparedStatement = localConnection.prepareStatement("select * from jdbctest");

    ResultSet localResultSet = localPreparedStatement.executeQuery();
    localResultSet.next();

    paramArrayOfResultSet[0] = localResultSet;
  }

  public static void RS275(int paramInt1, int paramInt2, int paramInt3, int[] paramArrayOfInt1, int[] paramArrayOfInt2, String[] paramArrayOfString, ResultSet[] paramArrayOfResultSet)
    throws SQLException
  {
    paramArrayOfInt2[0] = 0;
    Connection localConnection = DriverManager.getConnection("jdbc:default:connection");

    String str = "SELECT c1/c2  FROM ns102";
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
      paramArrayOfString[0] = "Forward_Only";
    else if (localResultSet.getType() == 1005)
      paramArrayOfString[0] = "Scroll_sensitive";
    else if (localResultSet.getType() == 1004) {
      paramArrayOfString[0] = "Scroll_InSensitive";
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
