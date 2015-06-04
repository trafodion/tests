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

public class RS323
{
  public static void main(String[] paramArrayOfString)
  {
  }

  public static void RS323(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    String str2 = "select * from d4";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS323a(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6, ResultSet[] paramArrayOfResultSet7, ResultSet[] paramArrayOfResultSet8, ResultSet[] paramArrayOfResultSet9, ResultSet[] paramArrayOfResultSet10, ResultSet[] paramArrayOfResultSet11, ResultSet[] paramArrayOfResultSet12, ResultSet[] paramArrayOfResultSet13)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement1 = localConnection.createStatement();

    String str2 = "select i1 from d4";
    paramArrayOfResultSet1[0] = localStatement1.executeQuery(str2);

    Statement localStatement2 = localConnection.createStatement();

    String str3 = "select i2 from d4";
    paramArrayOfResultSet2[0] = localStatement2.executeQuery(str3);

    Statement localStatement3 = localConnection.createStatement();

    String str4 = "select i3 from d4";
    paramArrayOfResultSet3[0] = localStatement3.executeQuery(str4);

    Statement localStatement4 = localConnection.createStatement();

    String str5 = "select g0 from d4";
    paramArrayOfResultSet4[0] = localStatement4.executeQuery(str5);

    Statement localStatement5 = localConnection.createStatement();

    String str6 = "select g1 from d4";
    paramArrayOfResultSet5[0] = localStatement5.executeQuery(str6);

    Statement localStatement6 = localConnection.createStatement();

    String str7 = "select g2 from d4";
    paramArrayOfResultSet6[0] = localStatement6.executeQuery(str7);

    Statement localStatement7 = localConnection.createStatement();

    String str8 = "select g3 from d4";
    paramArrayOfResultSet7[0] = localStatement7.executeQuery(str8);

    Statement localStatement8 = localConnection.createStatement();

    String str9 = "select g4 from d4";
    paramArrayOfResultSet8[0] = localStatement8.executeQuery(str9);

    Statement localStatement9 = localConnection.createStatement();

    String str10 = "select g5 from d4";
    paramArrayOfResultSet9[0] = localStatement9.executeQuery(str10);

    Statement localStatement10 = localConnection.createStatement();

    String str11 = "select g6 from d4";
    paramArrayOfResultSet10[0] = localStatement10.executeQuery(str11);

    Statement localStatement11 = localConnection.createStatement();

    String str12 = "select g7 from d4";
    paramArrayOfResultSet11[0] = localStatement11.executeQuery(str12);

    Statement localStatement12 = localConnection.createStatement();

    String str13 = "select i1 from d4";
    paramArrayOfResultSet12[0] = localStatement12.executeQuery(str13);

    Statement localStatement13 = localConnection.createStatement();

    String str14 = "select i2 from d4";
    paramArrayOfResultSet13[0] = localStatement13.executeQuery(str14);
  }

  public static void RS323b(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6, ResultSet[] paramArrayOfResultSet7, ResultSet[] paramArrayOfResultSet8, ResultSet[] paramArrayOfResultSet9, ResultSet[] paramArrayOfResultSet10, ResultSet[] paramArrayOfResultSet11, ResultSet[] paramArrayOfResultSet12, ResultSet[] paramArrayOfResultSet13, ResultSet[] paramArrayOfResultSet14, ResultSet[] paramArrayOfResultSet15, ResultSet[] paramArrayOfResultSet16, ResultSet[] paramArrayOfResultSet17, ResultSet[] paramArrayOfResultSet18, ResultSet[] paramArrayOfResultSet19, ResultSet[] paramArrayOfResultSet20, ResultSet[] paramArrayOfResultSet21, ResultSet[] paramArrayOfResultSet22, ResultSet[] paramArrayOfResultSet23, ResultSet[] paramArrayOfResultSet24, ResultSet[] paramArrayOfResultSet25, ResultSet[] paramArrayOfResultSet26, ResultSet[] paramArrayOfResultSet27)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement1 = localConnection.createStatement();

    String str2 = "select double_preci from str_num";
    paramArrayOfResultSet1[0] = localStatement1.executeQuery(str2);

    Statement localStatement2 = localConnection.createStatement();

    String str3 = "select decimal_us from str_num";
    paramArrayOfResultSet2[0] = localStatement2.executeQuery(str3);

    Statement localStatement3 = localConnection.createStatement();

    String str4 = "select n5 from trn";
    paramArrayOfResultSet3[0] = localStatement3.executeQuery(str4);

    Statement localStatement4 = localConnection.createStatement();

    String str5 = "select n3 from trn";
    paramArrayOfResultSet4[0] = localStatement4.executeQuery(str5);

    Statement localStatement5 = localConnection.createStatement();

    String str6 = "select n2 from trn";
    paramArrayOfResultSet5[0] = localStatement5.executeQuery(str6);

    Statement localStatement6 = localConnection.createStatement();

    String str7 = "select s1 from trn";
    paramArrayOfResultSet6[0] = localStatement6.executeQuery(str7);

    Statement localStatement7 = localConnection.createStatement();

    String str8 = "select s0 from trn";
    paramArrayOfResultSet7[0] = localStatement7.executeQuery(str8);

    Statement localStatement8 = localConnection.createStatement();

    String str9 = "select n6 from trn";
    paramArrayOfResultSet8[0] = localStatement8.executeQuery(str9);

    Statement localStatement9 = localConnection.createStatement();

    String str10 = "select n1 from trn";
    paramArrayOfResultSet9[0] = localStatement9.executeQuery(str10);

    Statement localStatement10 = localConnection.createStatement();

    String str11 = "select s2 from trn";
    paramArrayOfResultSet10[0] = localStatement10.executeQuery(str11);

    Statement localStatement11 = localConnection.createStatement();

    String str12 = "select s3 from trn";
    paramArrayOfResultSet11[0] = localStatement11.executeQuery(str12);

    Statement localStatement12 = localConnection.createStatement();

    String str13 = "select n4 from trn";
    paramArrayOfResultSet12[0] = localStatement12.executeQuery(str13);

    Statement localStatement13 = localConnection.createStatement();

    String str14 = "select st1 from trs";
    paramArrayOfResultSet13[0] = localStatement13.executeQuery(str14);

    Statement localStatement14 = localConnection.createStatement();

    String str15 = "select st2 from trs";
    paramArrayOfResultSet14[0] = localStatement14.executeQuery(str15);

    Statement localStatement15 = localConnection.createStatement();

    String str16 = "select st3 from trs";
    paramArrayOfResultSet15[0] = localStatement15.executeQuery(str16);

    Statement localStatement16 = localConnection.createStatement();

    String str17 = "select st4 from trs";
    paramArrayOfResultSet16[0] = localStatement16.executeQuery(str17);

    Statement localStatement17 = localConnection.createStatement();

    String str18 = "select st5 from trs";
    paramArrayOfResultSet17[0] = localStatement17.executeQuery(str18);

    Statement localStatement18 = localConnection.createStatement();

    String str19 = "select st6 from trs";
    paramArrayOfResultSet18[0] = localStatement18.executeQuery(str19);

    Statement localStatement19 = localConnection.createStatement();

    String str20 = "select s0 from trs";
    paramArrayOfResultSet19[0] = localStatement19.executeQuery(str20);

    Statement localStatement20 = localConnection.createStatement();

    String str21 = "select s1 from trs";
    paramArrayOfResultSet20[0] = localStatement20.executeQuery(str21);

    Statement localStatement21 = localConnection.createStatement();

    String str22 = "select date_key from datetime_interval";
    paramArrayOfResultSet21[0] = localStatement21.executeQuery(str22);

    Statement localStatement22 = localConnection.createStatement();

    String str23 = "select date_col from datetime_interval";
    paramArrayOfResultSet22[0] = localStatement22.executeQuery(str23);

    Statement localStatement23 = localConnection.createStatement();

    String str24 = "select timestamp_col from datetime_interval";
    paramArrayOfResultSet23[0] = localStatement23.executeQuery(str24);

    Statement localStatement24 = localConnection.createStatement();

    String str25 = "select i1 from d3";
    paramArrayOfResultSet24[0] = localStatement24.executeQuery(str25);

    Statement localStatement25 = localConnection.createStatement();

    String str26 = "select i2 from d3";
    paramArrayOfResultSet25[0] = localStatement25.executeQuery(str26);

    Statement localStatement26 = localConnection.createStatement();

    String str27 = "select i3 from d3";
    paramArrayOfResultSet26[0] = localStatement26.executeQuery(str27);

    Statement localStatement27 = localConnection.createStatement();

    String str28 = "select s0 from d3";
    paramArrayOfResultSet27[0] = localStatement27.executeQuery(str28);
  }
}
