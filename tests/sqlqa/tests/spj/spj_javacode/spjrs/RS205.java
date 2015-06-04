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

import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class RS205
{
  public static void main(String[] paramArrayOfString)
  {
  }

  public static void RS205(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";
    Connection localConnection = null;

    localConnection = DriverManager.getConnection(str);
    Statement localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement1.executeQuery("SELECT cast(date_key as varchar(11)),cast(date_col as varchar(11)),cast(time_col as varchar(9)),cast(timestamp_col as varchar(27)),cast(interval_year as varchar(3)),cast(yr2_to_mo as varchar(7)),cast(yr6_to_mo as varchar(10)),cast(yr16_to_mo as varchar(20)),cast(year18 as varchar(19))from datetime_interval where date_key = date '2999-12-30' for update");

    Statement localStatement2 = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement2.executeQuery("SELECT cast(date_key as varchar(11)),cast(day2 as varchar(4)),cast(day18 as varchar(20)),cast(day16_to_hr as varchar(21)),cast(day14_to_min as varchar(21)),cast(day5_to_second6 as varchar(23)),cast(hour2 as varchar(4)),cast(hour18 as varchar(20)),cast(hour16_to_min as varchar(21)),cast(hour14_to_ss0 as varchar(22)),cast(hour10_to_second4 as varchar(23))from datetime_interval where date_key = date '1011-07-18' for update");

    Statement localStatement3 = localConnection.createStatement();
    paramArrayOfResultSet3[0] = localStatement3.executeQuery("SELECT cast(date_key as varchar(11)),cast(min2 as varchar(4)),cast(min18 as varchar(20)),cast(min13_s3 as varchar(22)),cast(min16_s0 as varchar(21)),cast(seconds as varchar(11)),cast(seconds5 as varchar(14)),cast(seconds18 as varchar(20)),cast(seconds15 as varchar(21))from datetime_interval where date_key = date '7009-02-01' order by 1 for update");
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

  public static void RS208(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select * from tab2000";
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

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select * from t6";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS317(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select * from i3";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS318(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6, ResultSet[] paramArrayOfResultSet7, ResultSet[] paramArrayOfResultSet8, ResultSet[] paramArrayOfResultSet9, ResultSet[] paramArrayOfResultSet10, ResultSet[] paramArrayOfResultSet11, ResultSet[] paramArrayOfResultSet12, ResultSet[] paramArrayOfResultSet13, ResultSet[] paramArrayOfResultSet14, ResultSet[] paramArrayOfResultSet15, ResultSet[] paramArrayOfResultSet16, ResultSet[] paramArrayOfResultSet17, ResultSet[] paramArrayOfResultSet18, ResultSet[] paramArrayOfResultSet19, ResultSet[] paramArrayOfResultSet20, ResultSet[] paramArrayOfResultSet21, ResultSet[] paramArrayOfResultSet22, ResultSet[] paramArrayOfResultSet23, ResultSet[] paramArrayOfResultSet24, ResultSet[] paramArrayOfResultSet25, ResultSet[] paramArrayOfResultSet26, ResultSet[] paramArrayOfResultSet27, ResultSet[] paramArrayOfResultSet28, ResultSet[] paramArrayOfResultSet29, ResultSet[] paramArrayOfResultSet30, ResultSet[] paramArrayOfResultSet31, ResultSet[] paramArrayOfResultSet32, ResultSet[] paramArrayOfResultSet33, ResultSet[] paramArrayOfResultSet34, ResultSet[] paramArrayOfResultSet35, ResultSet[] paramArrayOfResultSet36, ResultSet[] paramArrayOfResultSet37, ResultSet[] paramArrayOfResultSet38, ResultSet[] paramArrayOfResultSet39, ResultSet[] paramArrayOfResultSet40)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);

    Statement localStatement1 = localConnection.createStatement();
    String str2 = "select * from d3";
    paramArrayOfResultSet1[0] = localStatement1.executeQuery(str2);

    Statement localStatement2 = localConnection.createStatement();
    String str3 = "select * from daytab";
    paramArrayOfResultSet2[0] = localStatement2.executeQuery(str3);

    Statement localStatement3 = localConnection.createStatement();
    String str4 = "select * from testtab";
    paramArrayOfResultSet3[0] = localStatement3.executeQuery(str4);

    Statement localStatement4 = localConnection.createStatement();
    String str5 = "select * from nsday";
    paramArrayOfResultSet4[0] = localStatement4.executeQuery(str5);

    Statement localStatement5 = localConnection.createStatement();
    String str6 = "select * from nsminute";
    paramArrayOfResultSet5[0] = localStatement5.executeQuery(str6);

    Statement localStatement6 = localConnection.createStatement();
    String str7 = "select * from nssecond";
    paramArrayOfResultSet6[0] = localStatement6.executeQuery(str7);

    Statement localStatement7 = localConnection.createStatement();
    String str8 = "select * from trn";
    paramArrayOfResultSet7[0] = localStatement7.executeQuery(str8);

    Statement localStatement8 = localConnection.createStatement();
    String str9 = "select * from trs";
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
    String str15 = "select * from str_num";
    paramArrayOfResultSet14[0] = localStatement14.executeQuery(str15);

    Statement localStatement15 = localConnection.createStatement();
    String str16 = "select * from tbint";
    paramArrayOfResultSet15[0] = localStatement15.executeQuery(str16);

    Statement localStatement16 = localConnection.createStatement();
    String str17 = "select * from datetime_interval";
    paramArrayOfResultSet16[0] = localStatement16.executeQuery(str17);

    Statement localStatement17 = localConnection.createStatement();
    String str18 = "select * from tab2000";
    paramArrayOfResultSet17[0] = localStatement17.executeQuery(str18);

    Statement localStatement18 = localConnection.createStatement();
    String str19 = "select * from d4";
    paramArrayOfResultSet18[0] = localStatement18.executeQuery(str19);

    Statement localStatement19 = localConnection.createStatement();
    String str20 = "select extract (hour from htof),extract (hour from htof1),extract (hour from htof2),extract (hour from htof3),extract (hour from htof4),extract (hour from htof5),extract (hour from htof6),extract (hour from htosec),extract (hour from htomin),extract (hour from h)  from sthour";

    paramArrayOfResultSet19[0] = localStatement19.executeQuery(str20);

    Statement localStatement20 = localConnection.createStatement();
    String str21 = "select * from ntab";
    paramArrayOfResultSet20[0] = localStatement20.executeQuery(str21);

    Statement localStatement21 = localConnection.createStatement();
    String str22 = "select * from s2";
    paramArrayOfResultSet21[0] = localStatement21.executeQuery(str22);

    Statement localStatement22 = localConnection.createStatement();
    String str23 = "select * from sample";
    paramArrayOfResultSet22[0] = localStatement22.executeQuery(str23);

    Statement localStatement23 = localConnection.createStatement();
    String str24 = "select extract (day from daytof),extract (day from daytof1),extract (day from daytof2),extract (day from daytof3),extract (day from daytof4),extract (day from daytof5),extract (day from daytof6),extract (day from daytosec),extract (day from daytomin),extract (day from daytohr),extract (day from d) from stday";

    paramArrayOfResultSet23[0] = localStatement23.executeQuery(str24);

    Statement localStatement24 = localConnection.createStatement();
    String str25 = "select * from employ";
    paramArrayOfResultSet24[0] = localStatement24.executeQuery(str25);

    Statement localStatement25 = localConnection.createStatement();
    String str26 = "select * from  dept";
    paramArrayOfResultSet25[0] = localStatement25.executeQuery(str26);

    Statement localStatement26 = localConnection.createStatement();
    String str27 = "select extract (hour from htof),extract (hour from htof1),extract (hour from htof2),extract (hour from htof3),extract (hour from htof4),extract (hour from htof5),extract (hour from htof6),extract (hour from htosec),extract (hour from htomin),extract (hour from h) from sthour";

    paramArrayOfResultSet26[0] = localStatement26.executeQuery(str27);

    Statement localStatement27 = localConnection.createStatement();
    String str28 = "select extract (hour from daytof),extract (hour from daytof1),extract (hour from daytof2),extract (hour from daytof3),extract (hour from daytof4),extract (hour from daytof5),extract (hour from daytof6),extract (hour from daytosec),extract (hour from daytomin),extract (hour from daytohr)  from stday";

    paramArrayOfResultSet27[0] = localStatement27.executeQuery(str28);

    Statement localStatement28 = localConnection.createStatement();
    String str29 = "select * from lv_char";
    paramArrayOfResultSet28[0] = localStatement28.executeQuery(str29);

    Statement localStatement29 = localConnection.createStatement();
    String str30 = "select * from i3";
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
    String str34 = "select * from b3";
    paramArrayOfResultSet33[0] = localStatement33.executeQuery(str34);

    Statement localStatement34 = localConnection.createStatement();
    String str35 = "select * from b212";
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
    String str40 = "select * from t6";
    paramArrayOfResultSet39[0] = localStatement39.executeQuery(str40);

    Statement localStatement40 = localConnection.createStatement();
    String str41 = "select * from t5";
    paramArrayOfResultSet40[0] = localStatement40.executeQuery(str41);
  }

  public static void RS333(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement1 = localConnection.createStatement();
    String str2 = "select * from trn";
    paramArrayOfResultSet1[0] = localStatement1.executeQuery(str2);
    localStatement1.close();

    Statement localStatement2 = localConnection.createStatement();
    String str3 = "select * from trs";
    paramArrayOfResultSet2[0] = localStatement2.executeQuery(str3);
  }

  public static void RS333a(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement1 = localConnection.createStatement();
    String str2 = "select * from trn";
    paramArrayOfResultSet1[0] = localStatement1.executeQuery(str2);

    Statement localStatement2 = localConnection.createStatement();
    String str3 = "select * from trs";
    paramArrayOfResultSet2[0] = localStatement2.executeQuery(str3);
  }

  public static void RS334(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement1 = localConnection.createStatement();
    String str2 = "select * from t1";
    paramArrayOfResultSet1[0] = localStatement1.executeQuery(str2);

    Statement localStatement2 = localConnection.createStatement();
    String str3 = "select * from t2";
    paramArrayOfResultSet2[0] = localStatement2.executeQuery(str3);
    localStatement2.close();

    Statement localStatement3 = localConnection.createStatement();
    String str4 = "select * from trn";
    paramArrayOfResultSet3[0] = localStatement3.executeQuery(str4);
  }

  public static void RS335(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS200()}");
    localCallableStatement.execute();
    paramArrayOfResultSet1[0] = localCallableStatement.getResultSet();
  }

  public static void RS336(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select * from trn";

    paramArrayOfResultSet1[0] = localStatement.executeQuery(str2);
    localStatement.close();
  }

  public static void RS337(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS202()}");
    localCallableStatement.execute();

    paramArrayOfResultSet1[0] = localCallableStatement.getResultSet();

    if (localCallableStatement.getMoreResults())
      paramArrayOfResultSet2[0] = localCallableStatement.getResultSet();
  }

  public static void RS338(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select * from table1";
    paramArrayOfResultSet1[0] = localStatement.executeQuery(str2);
  }

  public static void RS339(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select c1,c2,c3 from \"test\".d4";
    paramArrayOfResultSet1[0] = localStatement.executeQuery(str2);
  }

  public static void RS340(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select c1,c2,c3 from \"test\".d4";
    paramArrayOfResultSet1[0] = localStatement.executeQuery(str2);
  }

  public static void RS341(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS202()}");
    localCallableStatement.execute();

    paramArrayOfResultSet1[0] = localCallableStatement.getResultSet();

    if (localCallableStatement.getMoreResults()) {
      paramArrayOfResultSet2[0] = localCallableStatement.getResultSet();
    }
    if (localCallableStatement.getMoreResults())
      paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
  }

  public static void RS342(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS202()}");
    boolean bool = localCallableStatement.execute();

    paramArrayOfResultSet1[0] = localCallableStatement.getResultSet();

    bool = localCallableStatement.getMoreResults(2);
    paramArrayOfResultSet2[0] = localCallableStatement.getResultSet();
    bool = localCallableStatement.getMoreResults(2);
    paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
  }

  public static void RS343(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement1 = localConnection.createStatement();
    String str2 = "select i1,i2,i3 from d4";
    paramArrayOfResultSet1[0] = localStatement1.executeQuery(str2);
    localStatement1.close();

    Statement localStatement2 = localConnection.createStatement();
    String str3 = "select i1,i2,i3 from d4";
    paramArrayOfResultSet1[0] = localStatement2.executeQuery(str3);
  }

  public static void RS344(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS202()}");
    boolean bool = localCallableStatement.execute();

    paramArrayOfResultSet1[0] = localCallableStatement.getResultSet();
    bool = localCallableStatement.getMoreResults(2);

    paramArrayOfResultSet2[0] = localCallableStatement.getResultSet();
    bool = localCallableStatement.getMoreResults(1);
    paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
  }

  public static void RS345(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS202()}");
    boolean bool = localCallableStatement.execute();

    paramArrayOfResultSet1[0] = localCallableStatement.getResultSet();
    bool = localCallableStatement.getMoreResults(2);

    paramArrayOfResultSet2[0] = localCallableStatement.getResultSet();
    bool = localCallableStatement.getMoreResults(3);
    paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
  }

  public static void RS346(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS202()}");
    boolean bool = localCallableStatement.execute();

    paramArrayOfResultSet1[0] = localCallableStatement.getResultSet();

    if (localCallableStatement.getMoreResults() == true)
    {
      bool = localCallableStatement.getMoreResults(2);
    }paramArrayOfResultSet2[0] = localCallableStatement.getResultSet();
    bool = localCallableStatement.getMoreResults(2);
    paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
  }

  public static void RS347(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select * from bd";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS352(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select day5_to_second6 from datetime_interval";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS267(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "drop table bd";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS268(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "Select * from hpq.cpq.ns102";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS269(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("drop procedure rs269");
  }

  public static void RS270(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("drop procedure rs270");
    localStatement.executeUpdate("create procedure rs270(IN IN1 varchar(50),OUT OUT1 varchar(56))   external name 'Procs.N0200' external path 'spjrs' language java  parameter style java no sql isolate");
  }

  public static void RS271(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS202()}");
    boolean bool = localCallableStatement.execute();

    paramArrayOfResultSet[0] = localCallableStatement.getResultSet();
  }

  public static void RS272(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS202()}");
    boolean bool = localCallableStatement.execute();

    paramArrayOfResultSet1[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet2[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
  }

  public static void RS272a(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS272()}");
    boolean bool = localCallableStatement.execute();

    paramArrayOfResultSet1[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet2[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
    localCallableStatement.getMoreResults(2);
    paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
  }

  public static void RS272b(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS272a()}");
    boolean bool = localCallableStatement.execute();

    paramArrayOfResultSet1[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet2[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
    localCallableStatement.getMoreResults(2);
    paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
  }

  public static void RS272c(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS272b()}");
    boolean bool = localCallableStatement.execute();

    paramArrayOfResultSet1[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet2[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
    localCallableStatement.getMoreResults(2);
    paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
  }

  public static void RS272d(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS272c()}");
    boolean bool = localCallableStatement.execute();

    paramArrayOfResultSet1[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet2[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
    localCallableStatement.getMoreResults(2);
    paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
  }

  public static void RS272e(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS272d()}");
    boolean bool = localCallableStatement.execute();

    paramArrayOfResultSet1[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet2[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
    localCallableStatement.getMoreResults(2);
    paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
  }

  public static void RS272f(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS272e()}");
    boolean bool = localCallableStatement.execute();

    paramArrayOfResultSet1[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet2[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
    localCallableStatement.getMoreResults(2);
    paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
  }

  public static void RS272g(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS272f()}");
    boolean bool = localCallableStatement.execute();

    paramArrayOfResultSet1[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet2[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
    localCallableStatement.getMoreResults(2);
    paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
  }

  public static void RS272h(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS272g()}");
    boolean bool = localCallableStatement.execute();

    paramArrayOfResultSet1[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet2[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
    localCallableStatement.getMoreResults(2);
    paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
  }

  public static void RS272i(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS272h()}");
    boolean bool = localCallableStatement.execute();

    paramArrayOfResultSet1[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet2[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
    localCallableStatement.getMoreResults(2);
    paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
  }

  public static void RS272j(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS272i()}");
    boolean bool = localCallableStatement.execute();

    paramArrayOfResultSet1[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet2[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
    localCallableStatement.getMoreResults(2);
    paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
  }

  public static void RS272k(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS272j()}");
    boolean bool = localCallableStatement.execute();

    paramArrayOfResultSet1[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet2[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
    localCallableStatement.getMoreResults(2);
    paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
  }

  public static void RS285(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);

    Statement localStatement1 = localConnection.createStatement();

    String str2 = "select current_date from testtab";
    paramArrayOfResultSet1[0] = localStatement1.executeQuery(str2);

    Statement localStatement2 = localConnection.createStatement();

    String str3 = "select current_time from testtab";
    paramArrayOfResultSet2[0] = localStatement2.executeQuery(str3);

    Statement localStatement3 = localConnection.createStatement();

    String str4 = "select current_timestamp from testtab";
    paramArrayOfResultSet3[0] = localStatement3.executeQuery(str4);
  }

  public static void RS286(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement1 = localConnection.createStatement();

    String str2 = "select e_name from testtab";
    paramArrayOfResultSet4[0] = localStatement1.executeQuery(str2);

    Statement localStatement2 = localConnection.createStatement();

    String str3 = "select e_city  from testtab";
    paramArrayOfResultSet5[0] = localStatement2.executeQuery(str3);

    Statement localStatement3 = localConnection.createStatement();
    String str4 = "select e_title from testtab";
    paramArrayOfResultSet6[0] = localStatement3.executeQuery(str4);

    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS285()}");
    boolean bool = localCallableStatement.execute();

    paramArrayOfResultSet1[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet2[0] = localCallableStatement.getResultSet();
    if (localCallableStatement.getMoreResults(2) == true)
      paramArrayOfResultSet3[0] = localCallableStatement.getResultSet();
    localCallableStatement.getMoreResults(2);
    paramArrayOfResultSet4[0] = localCallableStatement.getResultSet();
  }

  public static void RS287(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select * from trn";
    paramArrayOfResultSet1[0] = localStatement.executeQuery(str2);

    localStatement = localConnection.createStatement();
    localStatement.executeUpdate("control query default udr_java_options '-Xms16k -Xmx16k'");

    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS205()}");
    boolean bool = localCallableStatement.execute();
    paramArrayOfResultSet2[0] = localCallableStatement.getResultSet();
  }

  public static void RS288(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS287()}");
    boolean bool = localCallableStatement.execute();
    paramArrayOfResultSet[0] = localCallableStatement.getResultSet();
  }

  public static void RS786(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select * from str_num";

    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void NS786(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    String str2 = "select * from " + paramString;
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS787(String paramString1, String paramString2, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    String str2 = "select " + paramString1 + " from " + paramString2;
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS788(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    String str2 = "select * from " + paramString;
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS789(String paramString1, String paramString2, String paramString3, String paramString4, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    String str2 = "select " + paramString1 + paramString2 + paramString3 + " from " + paramString4;
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }
}
