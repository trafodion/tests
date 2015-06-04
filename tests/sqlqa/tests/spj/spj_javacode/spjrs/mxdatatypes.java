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
import java.util.Properties;

public class mxdatatypes
{
  public static void main(String[] paramArrayOfString)
  {
  }

  public static void RS300(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6, ResultSet[] paramArrayOfResultSet7, ResultSet[] paramArrayOfResultSet8, ResultSet[] paramArrayOfResultSet9, ResultSet[] paramArrayOfResultSet10, ResultSet[] paramArrayOfResultSet11, ResultSet[] paramArrayOfResultSet12, ResultSet[] paramArrayOfResultSet13, ResultSet[] paramArrayOfResultSet14, ResultSet[] paramArrayOfResultSet15, ResultSet[] paramArrayOfResultSet16, ResultSet[] paramArrayOfResultSet17, ResultSet[] paramArrayOfResultSet18, ResultSet[] paramArrayOfResultSet19, ResultSet[] paramArrayOfResultSet20, ResultSet[] paramArrayOfResultSet21, ResultSet[] paramArrayOfResultSet22, ResultSet[] paramArrayOfResultSet23, ResultSet[] paramArrayOfResultSet24, ResultSet[] paramArrayOfResultSet25, ResultSet[] paramArrayOfResultSet26, ResultSet[] paramArrayOfResultSet27, ResultSet[] paramArrayOfResultSet28, ResultSet[] paramArrayOfResultSet29, ResultSet[] paramArrayOfResultSet30, ResultSet[] paramArrayOfResultSet31)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement1 = localConnection.createStatement();
    String str2 = "select  char_up from str_num";
    paramArrayOfResultSet1[0] = localStatement1.executeQuery(str2);

    Statement localStatement2 = localConnection.createStatement();
    String str3 = "select  varchars  from str_num";
    paramArrayOfResultSet2[0] = localStatement2.executeQuery(str3);

    Statement localStatement3 = localConnection.createStatement();
    String str4 = "select varchar_up from str_num";
    paramArrayOfResultSet3[0] = localStatement3.executeQuery(str4);

    Statement localStatement4 = localConnection.createStatement();
    String str5 = "select picx from str_num";
    paramArrayOfResultSet4[0] = localStatement4.executeQuery(str5);

    Statement localStatement5 = localConnection.createStatement();
    String str6 = "select picx_up from str_num";
    paramArrayOfResultSet5[0] = localStatement5.executeQuery(str6);

    Statement localStatement6 = localConnection.createStatement();
    String str7 = "select picx_dis   from str_num";
    paramArrayOfResultSet6[0] = localStatement6.executeQuery(str7);

    Statement localStatement7 = localConnection.createStatement();
    String str8 = "select picx_updis from str_num";
    paramArrayOfResultSet7[0] = localStatement7.executeQuery(str8);

    Statement localStatement8 = localConnection.createStatement();
    String str9 = "select char_vary from str_num";
    paramArrayOfResultSet8[0] = localStatement8.executeQuery(str9);

    Statement localStatement9 = localConnection.createStatement();
    String str10 = "select char_vary_up from str_num";
    paramArrayOfResultSet9[0] = localStatement9.executeQuery(str10);

    Statement localStatement10 = localConnection.createStatement();
    String str11 = "select num_s from str_num";
    paramArrayOfResultSet10[0] = localStatement10.executeQuery(str11);

    Statement localStatement11 = localConnection.createStatement();
    String str12 = "select num_s2 from str_num";
    paramArrayOfResultSet11[0] = localStatement11.executeQuery(str12);

    Statement localStatement12 = localConnection.createStatement();
    String str13 = "select num_us from str_num";
    paramArrayOfResultSet12[0] = localStatement12.executeQuery(str13);

    Statement localStatement13 = localConnection.createStatement();
    String str14 = "select smallint_s   from str_num";
    paramArrayOfResultSet13[0] = localStatement13.executeQuery(str14);

    Statement localStatement14 = localConnection.createStatement();
    String str15 = "select smallint_us   from str_num";
    paramArrayOfResultSet14[0] = localStatement14.executeQuery(str15);

    Statement localStatement15 = localConnection.createStatement();
    String str16 = "select integer_s   from str_num";
    paramArrayOfResultSet15[0] = localStatement15.executeQuery(str16);

    Statement localStatement16 = localConnection.createStatement();
    String str17 = "select integer_us from str_num";
    paramArrayOfResultSet16[0] = localStatement16.executeQuery(str17);

    Statement localStatement17 = localConnection.createStatement();
    String str18 = "select large_int from str_num";
    paramArrayOfResultSet17[0] = localStatement17.executeQuery(str18);

    Statement localStatement18 = localConnection.createStatement();
    String str19 = "select decimal_s from str_num";
    paramArrayOfResultSet18[0] = localStatement18.executeQuery(str19);

    Statement localStatement19 = localConnection.createStatement();
    String str20 = "select decimal_us  from str_num";
    paramArrayOfResultSet19[0] = localStatement19.executeQuery(str20);

    Statement localStatement20 = localConnection.createStatement();
    String str21 = "select pic_scomp  from str_num";
    paramArrayOfResultSet20[0] = localStatement20.executeQuery(str21);

    Statement localStatement21 = localConnection.createStatement();
    String str22 = "select pic_uscomp  from str_num";
    paramArrayOfResultSet21[0] = localStatement21.executeQuery(str22);

    Statement localStatement22 = localConnection.createStatement();
    String str23 = "select pic_s   from str_num";
    paramArrayOfResultSet22[0] = localStatement22.executeQuery(str23);

    Statement localStatement23 = localConnection.createStatement();
    String str24 = "select pic_us from str_num";
    paramArrayOfResultSet23[0] = localStatement23.executeQuery(str24);

    Statement localStatement24 = localConnection.createStatement();
    String str25 = "select pic_vscomp from str_num";
    paramArrayOfResultSet24[0] = localStatement24.executeQuery(str25);

    Statement localStatement25 = localConnection.createStatement();
    String str26 = "select pic_vuscomp from str_num";
    paramArrayOfResultSet25[0] = localStatement25.executeQuery(str26);

    Statement localStatement26 = localConnection.createStatement();
    String str27 = "select pic_vs  from str_num";
    paramArrayOfResultSet26[0] = localStatement26.executeQuery(str27);

    Statement localStatement27 = localConnection.createStatement();
    String str28 = "select pic_vus   from str_num";
    paramArrayOfResultSet27[0] = localStatement27.executeQuery(str28);

    Statement localStatement28 = localConnection.createStatement();
    String str29 = "select real_col from str_num";
    paramArrayOfResultSet28[0] = localStatement28.executeQuery(str29);

    Statement localStatement29 = localConnection.createStatement();
    String str30 = "select float_col from str_num";
    paramArrayOfResultSet29[0] = localStatement29.executeQuery(str30);

    Statement localStatement30 = localConnection.createStatement();
    String str31 = "select double_preci from str_num";
    paramArrayOfResultSet30[0] = localStatement30.executeQuery(str31);

    Statement localStatement31 = localConnection.createStatement();
    String str32 = "select * from lv_char";
    paramArrayOfResultSet31[0] = localStatement31.executeQuery(str32);
  }

  public static void RS301(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6, ResultSet[] paramArrayOfResultSet7, ResultSet[] paramArrayOfResultSet8, ResultSet[] paramArrayOfResultSet9, ResultSet[] paramArrayOfResultSet10, ResultSet[] paramArrayOfResultSet11, ResultSet[] paramArrayOfResultSet12, ResultSet[] paramArrayOfResultSet13, ResultSet[] paramArrayOfResultSet14, ResultSet[] paramArrayOfResultSet15, ResultSet[] paramArrayOfResultSet16, ResultSet[] paramArrayOfResultSet17, ResultSet[] paramArrayOfResultSet18, ResultSet[] paramArrayOfResultSet19, ResultSet[] paramArrayOfResultSet20, ResultSet[] paramArrayOfResultSet21, ResultSet[] paramArrayOfResultSet22, ResultSet[] paramArrayOfResultSet23, ResultSet[] paramArrayOfResultSet24, ResultSet[] paramArrayOfResultSet25, ResultSet[] paramArrayOfResultSet26, ResultSet[] paramArrayOfResultSet27, ResultSet[] paramArrayOfResultSet28, ResultSet[] paramArrayOfResultSet29, ResultSet[] paramArrayOfResultSet30, ResultSet[] paramArrayOfResultSet31)
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    Connection localConnection;
    try {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement19 = localConnection.createStatement();
      String str2 = "select decimal_us  from str_num";
      paramArrayOfResultSet19[0] = localStatement19.executeQuery(str2);
    }
    catch (SQLException localSQLException1)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException1.getMessage());
      localSQLException1.getNextException();
    }
    try {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement13 = localConnection.createStatement();
      String str3 = "select smallint_s   from str_num";
      paramArrayOfResultSet13[0] = localStatement13.executeQuery(str3);
    }
    catch (SQLException localSQLException2)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException2.getMessage());
      localSQLException2.getNextException();
    }Statement localStatement18;
    try {
      localConnection = DriverManager.getConnection(str1);
      localStatement18 = localConnection.createStatement();
      String str4 = "select decimal_s from str_num";
      paramArrayOfResultSet18[0] = localStatement18.executeQuery(str4);
    }
    catch (SQLException localSQLException3)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException3.getMessage());
      localSQLException3.getNextException();
    }
    try
    {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement2 = localConnection.createStatement();
      String str5 = "select  varchars  from str_num";
      paramArrayOfResultSet2[0] = localStatement2.executeQuery(str5);
    }
    catch (SQLException localSQLException4)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException4.getMessage());
      localSQLException4.getNextException();
    }
    try {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement27 = localConnection.createStatement();
      String str6 = "select pic_vus   from str_num";
      paramArrayOfResultSet27[0] = localStatement27.executeQuery(str6);
    }
    catch (SQLException localSQLException5)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException5.getMessage());
      localSQLException5.getNextException();
    }
    try {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement4 = localConnection.createStatement();
      String str7 = "select picx from str_num";
      paramArrayOfResultSet4[0] = localStatement4.executeQuery(str7);
    }
    catch (SQLException localSQLException6)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException6.getMessage());
      localSQLException6.getNextException();
    }
    try {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement15 = localConnection.createStatement();
      String str8 = "select integer_s   from str_num";
      paramArrayOfResultSet15[0] = localStatement15.executeQuery(str8);
    }
    catch (SQLException localSQLException7)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException7.getMessage());
      localSQLException7.getNextException();
    }

    try
    {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement6 = localConnection.createStatement();
      String str9 = "select picx_dis   from str_num";
      paramArrayOfResultSet6[0] = localStatement6.executeQuery(str9);
    }
    catch (SQLException localSQLException8)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException8.getMessage());
      localSQLException8.getNextException();
    }
    try {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement25 = localConnection.createStatement();
      String str10 = "select pic_vuscomp from str_num";
      paramArrayOfResultSet25[0] = localStatement25.executeQuery(str10);
    }
    catch (SQLException localSQLException9)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException9.getMessage());
      localSQLException9.getNextException();
    }
    try
    {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement8 = localConnection.createStatement();
      String str11 = "select char_vary from str_num";
      paramArrayOfResultSet8[0] = localStatement8.executeQuery(str11);
    }
    catch (SQLException localSQLException10)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException10.getMessage());
      localSQLException10.getNextException();
    }
    try
    {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement10 = localConnection.createStatement();
      String str12 = "select num_s from str_num";
      paramArrayOfResultSet10[0] = localStatement10.executeQuery(str12);
    }
    catch (SQLException localSQLException11)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException11.getMessage());
      localSQLException11.getNextException();
    }
    try {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement1 = localConnection.createStatement();
      String str13 = "select  char_up from str_num";
      paramArrayOfResultSet1[0] = localStatement1.executeQuery(str13);
    }
    catch (SQLException localSQLException12)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException12.getMessage());
      localSQLException12.getNextException();
    }
    try
    {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement12 = localConnection.createStatement();
      String str14 = "select num_us from str_num";
      paramArrayOfResultSet12[0] = localStatement12.executeQuery(str14);
    }
    catch (SQLException localSQLException13)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException13.getMessage());
      localSQLException13.getNextException();
    }

    try
    {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement16 = localConnection.createStatement();
      String str15 = "select integer_us from str_num";
      paramArrayOfResultSet16[0] = localStatement16.executeQuery(str15);
    }
    catch (SQLException localSQLException14)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException14.getMessage());
      localSQLException14.getNextException();
    }
    try {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement7 = localConnection.createStatement();
      String str16 = "select picx_updis from str_num";
      paramArrayOfResultSet7[0] = localStatement7.executeQuery(str16);
    }
    catch (SQLException localSQLException15)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException15.getMessage());
      localSQLException15.getNextException();
    }
    try {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement17 = localConnection.createStatement();
      String str17 = "select large_int from str_num";
      paramArrayOfResultSet17[0] = localStatement17.executeQuery(str17);
    }
    catch (SQLException localSQLException16)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException16.getMessage());
      localSQLException16.getNextException();
    }
    try {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement29 = localConnection.createStatement();
      String str18 = "select double_preci from str_num";
      paramArrayOfResultSet30[0] = localStatement29.executeQuery(str18);
    }
    catch (SQLException localSQLException17)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException17.getMessage());
      localSQLException17.getNextException();
    }
    try {
      localConnection = DriverManager.getConnection(str1);
      localStatement18 = localConnection.createStatement();
      String str19 = "select decimal_s from str_num";
      paramArrayOfResultSet18[0] = localStatement18.executeQuery(str19);
    }
    catch (SQLException localSQLException18)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException18.getMessage());
      localSQLException18.getNextException();
    }
    try
    {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement20 = localConnection.createStatement();
      String str20 = "select pic_scomp  from str_num";
      paramArrayOfResultSet20[0] = localStatement20.executeQuery(str20);
    }
    catch (SQLException localSQLException19)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException19.getMessage());
      localSQLException19.getNextException();
    }
    try
    {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement22 = localConnection.createStatement();
      String str21 = "select pic_s   from str_num";
      paramArrayOfResultSet22[0] = localStatement22.executeQuery(str21);
    }
    catch (SQLException localSQLException20)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException20.getMessage());
      localSQLException20.getNextException();
    }
    try {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement23 = localConnection.createStatement();
      String str22 = "select pic_us from str_num";
      paramArrayOfResultSet23[0] = localStatement23.executeQuery(str22);
    }
    catch (SQLException localSQLException21)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException21.getMessage());
      localSQLException21.getNextException();
    }
    try {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement24 = localConnection.createStatement();
      String str23 = "select pic_vscomp from str_num";
      paramArrayOfResultSet24[0] = localStatement24.executeQuery(str23);
    }
    catch (SQLException localSQLException22)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException22.getMessage());
      localSQLException22.getNextException();
    }

    try
    {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement30 = localConnection.createStatement();
      String str24 = "select * from lv_char";
      paramArrayOfResultSet31[0] = localStatement30.executeQuery(str24);
    }
    catch (SQLException localSQLException23)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException23.getMessage());
      localSQLException23.getNextException();
    }
    try {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement11 = localConnection.createStatement();
      String str25 = "select num_s2 from str_num";
      paramArrayOfResultSet11[0] = localStatement11.executeQuery(str25);
    }
    catch (SQLException localSQLException24)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException24.getMessage());
      localSQLException24.getNextException();
    }
    try {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement3 = localConnection.createStatement();
      String str26 = "select varchar_up from str_num";
      paramArrayOfResultSet3[0] = localStatement3.executeQuery(str26);
    }
    catch (SQLException localSQLException25)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException25.getMessage());
      localSQLException25.getNextException();
    }
    try {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement14 = localConnection.createStatement();
      String str27 = "select smallint_us   from str_num";
      paramArrayOfResultSet14[0] = localStatement14.executeQuery(str27);
    }
    catch (SQLException localSQLException26)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException26.getMessage());
      localSQLException26.getNextException();
    }
    try {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement5 = localConnection.createStatement();
      String str28 = "select picx_up from str_num";
      paramArrayOfResultSet5[0] = localStatement5.executeQuery(str28);
    }
    catch (SQLException localSQLException27)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException27.getMessage());
      localSQLException27.getNextException();
    }
    try {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement28 = localConnection.createStatement();
      String str29 = "select float_col from str_num";
      paramArrayOfResultSet29[0] = localStatement28.executeQuery(str29);
    }
    catch (SQLException localSQLException28)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException28.getMessage());
      localSQLException28.getNextException();
    }
    try {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement9 = localConnection.createStatement();
      String str30 = "select char_vary_up from str_num";
      paramArrayOfResultSet9[0] = localStatement9.executeQuery(str30);
    }
    catch (SQLException localSQLException29)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException29.getMessage());
      localSQLException29.getNextException();
    }
    try {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement21 = localConnection.createStatement();
      String str31 = "select pic_uscomp  from str_num";
      paramArrayOfResultSet21[0] = localStatement21.executeQuery(str31);
    }
    catch (SQLException localSQLException30)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException30.getMessage());
      localSQLException30.getNextException();
    }
    try {
      localConnection = DriverManager.getConnection(str1);
      Statement localStatement26 = localConnection.createStatement();
      String str32 = "select pic_vs  from str_num";
      paramArrayOfResultSet26[0] = localStatement26.executeQuery(str32);
    }
    catch (SQLException localSQLException31)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException31.getMessage());
      localSQLException31.getNextException();
    }
  }

  public static void RS202(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);

    Statement localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement1.executeQuery("select e_city from testtab");

    Statement localStatement2 = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement2.executeQuery("select e_date from testtab");

    Statement localStatement3 = localConnection.createStatement();
    paramArrayOfResultSet3[0] = localStatement3.executeQuery("select e_long from testtab");
  }

  public static void RS203(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);

    Statement localStatement3 = localConnection.createStatement();
    paramArrayOfResultSet3[0] = localStatement3.executeQuery("select e_long from testtab");

    Statement localStatement2 = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement2.executeQuery("select e_city from testtab");

    Statement localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement1.executeQuery("select e_date from testtab");
  }

  public static void RS204(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);

    Statement localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement1.executeQuery("SELECT cast(date_key as varchar(11)),cast(date_col as varchar(11)),cast(time_col as varchar(9)),cast(timestamp_col as varchar(27)),cast(interval_year as varchar(3)),cast(yr2_to_mo as varchar(7)),cast(yr6_to_mo as varchar(10)),cast(yr16_to_mo as varchar(20)),cast(year18 as varchar(19))from datetime_interval order By 1 FOR READ ONLY");

    Statement localStatement2 = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement2.executeQuery("SELECT cast(date_key as varchar(11)),cast(date_col as varchar(11)),cast(time_col as varchar(9)),cast(timestamp_col as varchar(27)),cast(interval_year as varchar(3)),cast(yr2_to_mo as varchar(7)),cast(yr6_to_mo as varchar(10)),cast(yr16_to_mo as varchar(20)),cast(year18 as varchar(19))from datetime_interval where date_key = date '2999-12-30' for update");

    Statement localStatement3 = localConnection.createStatement();
    paramArrayOfResultSet3[0] = localStatement3.executeQuery("SELECT cast(date_key as varchar(11)),cast(day2 as varchar(4)),cast(day18 as varchar(20)),cast(day16_to_hr as varchar(21)),cast(day14_to_min as varchar(21)),cast(day5_to_second6 as varchar(23)),cast(hour2 as varchar(4)),cast(hour18 as varchar(20)),cast(hour16_to_min as varchar(21)),cast(hour14_to_ss0 as varchar(22)),cast(hour10_to_second4 as varchar(23))from datetime_interval order By 1 FOR READ ONLY");

    Statement localStatement4 = localConnection.createStatement();
    paramArrayOfResultSet4[0] = localStatement4.executeQuery("SELECT cast(date_key as varchar(11)),cast(day2 as varchar(4)),cast(day18 as varchar(20)),cast(day16_to_hr as varchar(21)),cast(day14_to_min as varchar(21)),cast(day5_to_second6 as varchar(23)),cast(hour2 as varchar(4)),cast(hour18 as varchar(20)),cast(hour16_to_min as varchar(21)),cast(hour14_to_ss0 as varchar(22)),cast(hour10_to_second4 as varchar(23))from datetime_interval where date_key = date '1011-07-18' for update");

    Statement localStatement5 = localConnection.createStatement();
    paramArrayOfResultSet5[0] = localStatement5.executeQuery("SELECT cast(date_key as varchar(11)),cast(min2 as varchar(4)),cast(min18 as varchar(20)),cast(min13_s3 as varchar(22)),cast(min16_s0 as varchar(21)),cast(seconds as varchar(11)),cast(seconds5 as varchar(14)),cast(seconds18 as varchar(20)),cast(seconds15 as varchar(21))from datetime_interval order By 1 FOR READ ONLY");

    Statement localStatement6 = localConnection.createStatement();
    paramArrayOfResultSet6[0] = localStatement6.executeQuery("SELECT cast(date_key as varchar(11)),cast(min2 as varchar(4)),cast(min18 as varchar(20)),cast(min13_s3 as varchar(22)),cast(min16_s0 as varchar(21)),cast(seconds as varchar(11)),cast(seconds5 as varchar(14)),cast(seconds18 as varchar(20)),cast(seconds15 as varchar(21))from datetime_interval where date_key = date '7009-02-01' order by 1 for update");
  }

  public static void RS205(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);

    Statement localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement1.executeQuery("SELECT cast(date_key as varchar(11)),cast(date_col as varchar(11)),cast(time_col as varchar(9)),cast(timestamp_col as varchar(27)),cast(interval_year as varchar(3)),cast(yr2_to_mo as varchar(7)),cast(yr6_to_mo as varchar(10)),cast(yr16_to_mo as varchar(20)),cast(year18 as varchar(19))from datetime_interval where date_key = date '2999-12-30' for update");

    Statement localStatement2 = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement2.executeQuery("SELECT cast(date_key as varchar(11)),cast(day2 as varchar(4)),cast(day18 as varchar(20)),cast(day16_to_hr as varchar(21)),cast(day14_to_min as varchar(21)),cast(day5_to_second6 as varchar(23)),cast(hour2 as varchar(4)),cast(hour18 as varchar(20)),cast(hour16_to_min as varchar(21)),cast(hour14_to_ss0 as varchar(22)),cast(hour10_to_second4 as varchar(23))from datetime_interval where date_key = date '1011-07-18' for update");

    Statement localStatement3 = localConnection.createStatement();
    paramArrayOfResultSet3[0] = localStatement3.executeQuery("SELECT cast(date_key as varchar(11)),cast(min2 as varchar(4)),cast(min18 as varchar(20)),cast(min13_s3 as varchar(22)),cast(min16_s0 as varchar(21)),cast(seconds as varchar(11)),cast(seconds5 as varchar(14)),cast(seconds18 as varchar(20)),cast(seconds15 as varchar(21))from datetime_interval where date_key = date '7009-02-01' order by 1 for update");
  }

  public static void RS206(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement.executeQuery("select current_date,current_time,current_timestamp from t1");
  }

  public static void RS320(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = null;

    localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    String str2 = "select * from b212";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS321(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Properties localProperties = new Properties();

    localProperties.setProperty("maxPoolSize", "-1");
    localProperties.setProperty("minPoolSize", "-1");
    localProperties.setProperty("initialPoolSize", "-1");
    Connection localConnection = DriverManager.getConnection("jdbc:default:connection", localProperties);

    Statement localStatement = localConnection.createStatement();
    String str2 = "select * from i3";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS322(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    String str2 = "select * from tbint";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS323(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    String str2 = "select * from dt2";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS255(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    String str2 = "select ch_1 from t6";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS266(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    String str2 = "create table sp402 (Emp_Hire_Date varchar (30), Emp_Name varchar(32), Emp_ID int not null not droppable, Emp_Address varchar(32), Emp_City varchar(32), Emp_Salary decimal(10,2), Dept_ID int, primary key (Emp_ID))";

    localStatement.executeUpdate(str2);

    localStatement.executeUpdate("insert into sp402  values ('1/1/1900', 'John Doe', 1, 'unknown',  'unknown', 1111110.09, 1 )");

    localStatement.executeUpdate("insert into sp402  values ('2/2/1991', 'Jane Doelman', 2, 'unknown',  'unknown', 22220.99, 1 )");

    localStatement.executeUpdate("insert into sp402  values ('3/3/1903', 'James Smith', 3, '11 Pomoroy',  'Santa Clara', 400000.0, 1 )");

    localStatement.executeUpdate("insert into sp402  values ('1/1/1998', 'Tim Thomas', 4, '11 mainst',  'San Jose', 50000.0, 1 )");

    localStatement.executeUpdate("insert into sp402  values ('2/2/1999', 'Jane Mars', 5, '11 cala',  'San Francisco', 100000.0, 1 )");

    localStatement.executeUpdate("insert into sp402  values ('4/3/1909', 'Ken Thompson', 6, '44 Duke',  'Santa Cruz', 14000.0, 1 )");

    String str3 = "select * from sp402";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str3);
  }
}
