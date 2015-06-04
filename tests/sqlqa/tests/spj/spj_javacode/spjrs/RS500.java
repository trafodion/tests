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
import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class RS500
{
  public static void main(String[] paramArrayOfString)
  {
  }

  public static void RS500(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    String str2 = "select * from stream(trn)";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS276(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    String str2 = "select * from btab";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS273(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    String str2 = "select * from btab";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS274(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    String str2 = "select * from btab";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS277(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("create table tb1 (a int not null, b int not null primary key)");
    localStatement.executeUpdate("create table tb2 (a int not null primary key, b int not null references tb1)");
    localStatement.executeUpdate("insert into tb1 values (1,2),(2,3),(3,4)");
    localStatement.executeUpdate("insert into tb2 values (1,3),(3,4)");

    String str2 = "select * from tb2,tb1 as x;";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS278(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("create catalog spjcat");
    localStatement.executeUpdate("create schema spjcat.spjsch");
    localStatement.executeUpdate("create table spjcat.spjsch.tb1 (a int not null, b int not null primary key)");
    localStatement.executeUpdate("create table spjcat.spjsch.tb2 (a int not null primary key, b int not null references spjcat.spjsch.tb1)");
    localStatement.executeUpdate("insert into spjcat.spjsch.tb1 values (1,2),(2,3),(3,4)");
    localStatement.executeUpdate("insert into spjcat.spjsch.tb2 values (1,3),(3,4)");

    String str2 = "select * from spjcat.spjsch.tb2,spjcat.spjsch.tb1";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS279(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4, ResultSet[] paramArrayOfResultSet5, ResultSet[] paramArrayOfResultSet6, ResultSet[] paramArrayOfResultSet7, ResultSet[] paramArrayOfResultSet8, ResultSet[] paramArrayOfResultSet9, ResultSet[] paramArrayOfResultSet10, ResultSet[] paramArrayOfResultSet11, ResultSet[] paramArrayOfResultSet12, ResultSet[] paramArrayOfResultSet13, ResultSet[] paramArrayOfResultSet14, ResultSet[] paramArrayOfResultSet15, ResultSet[] paramArrayOfResultSet16, ResultSet[] paramArrayOfResultSet17, ResultSet[] paramArrayOfResultSet18, ResultSet[] paramArrayOfResultSet19)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement1 = localConnection.createStatement();
    localStatement1.execute("control query default attempt_esp_parallelism 'off';");
    paramArrayOfResultSet1[0] = localStatement1.executeQuery("select count(*) from trs,trn,d4,d3,t1");
    localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement1.executeQuery("select count(*) from trn,d3,d4,t1,stmin");
    localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet3[0] = localStatement1.executeQuery("select count(*) from d3,d4,jdbctest,t1,t2");
    localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet4[0] = localStatement1.executeQuery("select count(*) from d4,t1,t2,t4,trs,trn");
    localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet5[0] = localStatement1.executeQuery("select count(*) from t1,t2,t4,daytab,d4,d3");
    localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet6[0] = localStatement1.executeQuery("select count(*) from t1,t2,t4,daytab,sthour,d4,d3");
    localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet7[0] = localStatement1.executeQuery("select count(*) from t2,t4,daytab,sthour,stmin,trn,trs");
    localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet8[0] = localStatement1.executeQuery("select count(*) from t2,t4,daytab,sthour,stmin,stsec,trn");
    localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet9[0] = localStatement1.executeQuery("select count(*) from t4,daytab,sthour,stmin,stsec,nshour,trs");
    localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet10[0] = localStatement1.executeQuery("select count(*) from daytab,sthour,stmin,stsec,nshour,d4,d3");
    localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet11[0] = localStatement1.executeQuery("select count(*) from sthour,stmin,stsec,nshour,nsminute,d4,d3");
    localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet12[0] = localStatement1.executeQuery("select count(*) from sthour,stmin,stsec,nshour,nsminute,sample,trn,trs");
    localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet13[0] = localStatement1.executeQuery("select count(*) from stmin,stsec,nshour,nsminute,sample,nssecond,d4");
    localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet14[0] = localStatement1.executeQuery("select count(*) from stsec,nshour,nsminute,sample,nssecond,jdbctest");
    localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet15[0] = localStatement1.executeQuery("select count(*) from nshour,nsminute,sample,nssecond,jdbctest,employ");
    localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet16[0] = localStatement1.executeQuery("select count(*) from nsminute,sample,nssecond,jdbctest,employ,tbint");
    localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet17[0] = localStatement1.executeQuery("select count(*) from nsminute,sample,nssecond,jdbctest,employ,tbint,str_num");
    localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet18[0] = localStatement1.executeQuery("select count(*) from nsminute,sample,nssecond,jdbctest,employ,tbint,str_num,lv_char");
    localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet19[0] = localStatement1.executeQuery("select count(*) from sample,nssecond,jdbctest,employ,tbint,str_num,lv_char,datetime_interval");
    Statement localStatement2 = localConnection.createStatement();
    localStatement2.execute("control query default attempt_esp_parallelism reset;");
  }

  public static void RS280(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("purgedata testtab");
    String str2 = "select count(*) from trs,trn,d3,d4";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS281a(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("create table m26 no partition as select * from testtab");
    String str2 = "select count(*) from m26";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS282(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    String str2 = "select * from (update stream(trig_tn043a) set b = upshift(b) set on rollback c = c+ 100) as x;";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS283(int[] paramArrayOfInt1, int[] paramArrayOfInt2, int[] paramArrayOfInt3, int[] paramArrayOfInt4, int[] paramArrayOfInt5, int[] paramArrayOfInt6, int[] paramArrayOfInt7, int[] paramArrayOfInt8, int[] paramArrayOfInt9, int[] paramArrayOfInt10, int[] paramArrayOfInt11, int[] paramArrayOfInt12, int[] paramArrayOfInt13, int[] paramArrayOfInt14, int[] paramArrayOfInt15, int[] paramArrayOfInt16, int[] paramArrayOfInt17, int[] paramArrayOfInt18, int[] paramArrayOfInt19, int[] paramArrayOfInt20, String[] paramArrayOfString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";

    DatabaseMetaData localDatabaseMetaData = null;

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();
    localDatabaseMetaData = localConnection.getMetaData();
    paramArrayOfInt1[0] = localDatabaseMetaData.getMaxBinaryLiteralLength();
    paramArrayOfInt2[0] = localDatabaseMetaData.getMaxCharLiteralLength();
    paramArrayOfInt2[0] = localDatabaseMetaData.getMaxCharLiteralLength();
    paramArrayOfInt3[0] = localDatabaseMetaData.getMaxColumnNameLength();
    paramArrayOfInt4[0] = localDatabaseMetaData.getMaxColumnsInGroupBy();
    paramArrayOfInt5[0] = localDatabaseMetaData.getMaxColumnsInIndex();
    paramArrayOfInt6[0] = localDatabaseMetaData.getMaxColumnsInOrderBy();
    paramArrayOfInt7[0] = localDatabaseMetaData.getMaxColumnsInSelect();
    paramArrayOfInt8[0] = localDatabaseMetaData.getMaxColumnsInTable();
    paramArrayOfInt9[0] = localDatabaseMetaData.getMaxConnections();
    paramArrayOfInt10[0] = localDatabaseMetaData.getMaxCursorNameLength();
    paramArrayOfInt11[0] = localDatabaseMetaData.getMaxIndexLength();
    paramArrayOfInt12[0] = localDatabaseMetaData.getMaxSchemaNameLength();
    paramArrayOfInt13[0] = localDatabaseMetaData.getMaxProcedureNameLength();
    paramArrayOfInt14[0] = localDatabaseMetaData.getMaxCatalogNameLength();
    paramArrayOfInt15[0] = localDatabaseMetaData.getMaxRowSize();
    paramArrayOfInt16[0] = localDatabaseMetaData.getMaxStatementLength();
    paramArrayOfInt17[0] = localDatabaseMetaData.getMaxStatements();
    paramArrayOfInt18[0] = localDatabaseMetaData.getMaxTableNameLength();
    paramArrayOfInt19[0] = localDatabaseMetaData.getMaxTablesInSelect();
    paramArrayOfInt20[0] = localDatabaseMetaData.getMaxUserNameLength();
    boolean bool = localDatabaseMetaData.doesMaxRowSizeIncludeBlobs();
    System.out.println("doesMaxRowSizeIncludeBlobs:> " + bool);
  }

  public static void RS284(int paramInt, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("insert into a13 values(:a)");
    String str2 = "select * from a13";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS284a(int paramInt)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("insert into a13 values(:a)");
  }

  public static void RS288(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("create table a13(a int not null primary key)");
    localStatement.executeUpdate("insert into a13 values(424245),(7557575),(5353553),(9796844)");
    String str2 = "select * from a13";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
    localStatement.executeUpdate("delete from a13");
    Thread.currentThread(); Thread.sleep(50L);
  }

  public static void RS289(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("create table a13(a int not null primary key)");
    localStatement.executeUpdate("insert into a13 values(424245),(7557575),(5353553),(9796844)");
    String str2 = "select * from a13";
    paramArrayOfResultSet[0] = localStatement.executeQuery("select * from a13");

    Thread.currentThread(); Thread.sleep(50L);
    localStatement.executeUpdate("delete from a13");
    localStatement.executeUpdate("drop table a13");
  }

  public static void RS290(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("create table a13(a int not null primary key)");
    localStatement.executeUpdate("insert into a13 values(424245),(7557575),(5353553),(9796844)");
    String str2 = "select * from a13";
    paramArrayOfResultSet1[0] = localStatement.executeQuery(str2);
    localStatement.executeUpdate("delete from a13");
    localStatement.executeUpdate("drop table a13");
    paramArrayOfResultSet2[0] = localStatement.executeQuery("select * from a13");
    Thread.currentThread(); Thread.sleep(50L);
  }

  public static void RS291(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement.executeQuery("select * from a13");
  }

  public static void RS292(ResultSet[] paramArrayOfResultSet) throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement.executeQuery("select * from(delete from testtab where e_code>20000 return old.*) as t1");
  }

  public static void RS293(ResultSet[] paramArrayOfResultSet) throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement1 = localConnection.createStatement();

    localStatement1.executeUpdate("create table a13(a int not null primary key)");
    localStatement1.executeUpdate("create table a14(a int not null primary key)");
    localStatement1.executeUpdate("create trigger trig1 after delete on a14 insert into a13 values (5353535),(3124245),(468246),(5318371);");
    localStatement1.executeUpdate("delete from a14");
    Statement localStatement2 = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement2.executeQuery("select * from a13");
    localStatement1.executeUpdate("drop table a14 cascade");
    Thread.currentThread(); Thread.sleep(50L);
  }

  public static void RS294(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2) throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement1 = localConnection.createStatement();
    localStatement1.executeUpdate("create table a13(a int not null primary key)");
    localStatement1.executeUpdate("create table a14(b int not null primary key)");
    localStatement1.executeUpdate("create trigger trig1 after delete on a14 insert into a13 values (5353535),(3124245),(468246),(5318371);");
    localStatement1.executeUpdate("create trigger trig2 after insert on a13 insert into a14(select * from a13);");
    localStatement1.executeUpdate("delete from a14");
    Statement localStatement2 = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement2.executeQuery("select * from a13");
    localStatement2 = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement2.executeQuery("select * from a14");
    Thread.currentThread(); Thread.sleep(50L);
    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS295()}");
    localCallableStatement.execute();
  }

  public static void RS295()
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("drop table a13 cascade");
    localStatement.executeUpdate("drop table a14 cascade");
  }

  public static void RS296(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("control query default pos 'off';");
    localStatement.executeUpdate("control query default ddl_default_locations ' ';");
    localStatement.executeUpdate("create table qatab like testtab");

    for (int i = 0; i < 10000; ++i)
    {
      localStatement = localConnection.createStatement();
      localStatement.executeUpdate("insert into qatab values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    }
  }

  public static void RS355(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();

    localStatement = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement.executeQuery("select current_date from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement.executeQuery("select current_time from testtab");
    localStatement = localConnection.createStatement();
    paramArrayOfResultSet3[0] = localStatement.executeQuery("select current_timestamp from testtab");
  }

  public static void RS355a()
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("create table T221 (a int not null, b int not null primary key)");
    localStatement.executeUpdate("insert into T221 values (1,2),(2,3),(3,4)");
    localStatement.executeUpdate("drop table T221");
  }

  public static void RS356(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select a from tp2";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS358(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select * from megatab";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS360()
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("drop procedure tqz_2ypN8.rs360");
  }

  public static void RS361(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select object_name from HP_DEFINITION_SCHEMA.objects where object_type = 'BT'";
    paramArrayOfResultSet1[0] = localStatement.executeQuery(str2);

    localStatement = localConnection.createStatement();
    String str3 = "select object_name from HP_DEFINITION_SCHEMA.objects where object_type = 'UR'";
    paramArrayOfResultSet2[0] = localStatement.executeQuery(str3);

    localStatement = localConnection.createStatement();
    String str4 = "select object_name from HP_DEFINITION_SCHEMA.objects where object_type = 'IX'";
    paramArrayOfResultSet3[0] = localStatement.executeQuery(str4);

    localStatement = localConnection.createStatement();
    String str5 = "select object_name from HP_DEFINITION_SCHEMA.objects where object_type = 'PK'";
    paramArrayOfResultSet4[0] = localStatement.executeQuery(str5);
  }

  public static void RS362() throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();
    localStatement.execute("maintain table trn, all,return detail output");
  }

  public static void RS363()
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();

    CallableStatement localCallableStatement = localConnection.prepareCall("{call RS200()}");
    localCallableStatement.execute();
  }

  public static void RS364()
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("update statistics for table g_tpch2x.customer on every column");
  }

  public static void RS365(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();

    localStatement.execute("explain options 'n' select e_name from testtab");

    paramArrayOfResultSet[0] = localStatement.getResultSet();
  }

  public static void RS366(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();

    localStatement.execute("explain options 'n' call rs202();");

    paramArrayOfResultSet[0] = localStatement.getResultSet();
  }

  public static void RS367(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3, ResultSet[] paramArrayOfResultSet4)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select count(*) from bigdss_cat.bigdss_sch.table10";
    paramArrayOfResultSet1[0] = localStatement.executeQuery(str2);

    localStatement = localConnection.createStatement();
    String str3 = "select count(*) from bigdss_cat.bigdss_sch.table1h";
    paramArrayOfResultSet2[0] = localStatement.executeQuery(str3);

    localStatement = localConnection.createStatement();
    String str4 = "select count(*) from bigdss_cat.bigdss_sch.table1k";
    paramArrayOfResultSet3[0] = localStatement.executeQuery(str4);

    localStatement = localConnection.createStatement();
    String str5 = "select count(*) from bigdss_cat.bigdss_sch.table4k";
    paramArrayOfResultSet4[0] = localStatement.executeQuery(str5);
  }

  public static void RS501(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    String str2 = "select e_name from testtab";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
    System.exit(1);
  }

  public static void RS502(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    String str2 = "select cast(col_int as numeric(3,1))  from ief_tab;;";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }
}
