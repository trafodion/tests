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
import java.sql.Statement;

public class RS254
{
  public static void main(String[] paramArrayOfString)
  {
  }

  public static void sop(String paramString)
  {
    System.out.println(paramString);
  }

  public static void RS204(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6, ResultSet[] paramArrayOfResultSet7, ResultSet[] paramArrayOfResultSet8, ResultSet[] paramArrayOfResultSet9, ResultSet[] paramArrayOfResultSet10, ResultSet[] paramArrayOfResultSet11, ResultSet[] paramArrayOfResultSet12, ResultSet[] paramArrayOfResultSet13)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);

    Statement localStatement1 = localConnection.createStatement(1005, 1007);

    paramArrayOfResultSet1[0] = localStatement1.executeQuery("select * from trn");

    Statement localStatement2 = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement2.executeQuery("select * from trs");

    Statement localStatement3 = localConnection.createStatement();
    paramArrayOfResultSet3[0] = localStatement3.executeQuery("select * from tbint");

    Statement localStatement4 = localConnection.createStatement();
    paramArrayOfResultSet4[0] = localStatement4.executeQuery("select * from nshour");

    Statement localStatement5 = localConnection.createStatement();
    paramArrayOfResultSet5[0] = localStatement5.executeQuery("select * from nsminute");

    Statement localStatement6 = localConnection.createStatement();
    paramArrayOfResultSet6[0] = localStatement6.executeQuery("select * from nssecond");

    Statement localStatement7 = localConnection.createStatement();
    paramArrayOfResultSet7[0] = localStatement7.executeQuery("select * from d4");

    Statement localStatement8 = localConnection.createStatement();
    paramArrayOfResultSet8[0] = localStatement8.executeQuery("select * from str_num");

    Statement localStatement9 = localConnection.createStatement();
    paramArrayOfResultSet9[0] = localStatement9.executeQuery("select * from jdbctest");

    Statement localStatement10 = localConnection.createStatement();
    paramArrayOfResultSet10[0] = localStatement10.executeQuery("select * from b3");

    Statement localStatement11 = localConnection.createStatement();
    paramArrayOfResultSet11[0] = localStatement11.executeQuery("select * from stsec");

    Statement localStatement12 = localConnection.createStatement();
    paramArrayOfResultSet12[0] = localStatement12.executeQuery("select * from daytab");

    Statement localStatement13 = localConnection.createStatement();
    paramArrayOfResultSet13[0] = localStatement13.executeQuery("select * from stmin");
  }

  public static void dttab(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement(1005, 1007);

    paramArrayOfResultSet[0] = localStatement.executeQuery("select * from dttab");
  }

  public static void RS346(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement(1005, 1007);

    paramArrayOfResultSet[0] = localStatement.executeQuery("select s2 from d3");
  }

  public static void RS266(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from .b2uwl20";
    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS267(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select int0_dTOf6_n100,int1_yTOm_uniq,int2_dTOf6_n2,int3_yTOm_4,int4_yTOm_uniq,int5_hTOs_500 ,int6_dTOf6_nuniq,int7_hTOs_nuniq,int8_y_n1000,int9_dTOf6_2000,int11_h_n10,int12_yTOm_100,int13_yTOm_n1000,int14_d_500,int15_dTOf6_n100,int16_h_20,int17_y_n10 from b2uwl20";
    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS268(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select INTEGER_US from str_num";
    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
    System.exit(0);
  }
}
