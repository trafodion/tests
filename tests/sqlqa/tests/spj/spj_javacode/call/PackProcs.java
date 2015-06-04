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

package Pack;

import java.io.BufferedReader;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.math.BigDecimal;
import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.Date;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Time;
import java.sql.Timestamp;

public class PackProcs
{
  public static String NULLVALUE = "-9999.00";
  public static String INULLVALUE = "-9999";

  public static Date NULLDATEVALUE = Date.valueOf("1999-09-09");
  public static Time NULLTIMEVALUE = Time.valueOf("09:09:09");
  public static Timestamp NULLTIMESTAMPVALUE = Timestamp.valueOf("1999-09-09 09:09:09");
  public static String NULLSTRING = "NULL";

  public static void main(String[] paramArrayOfString) {
  }

  public static void sop(String paramString) {
    System.out.println(paramString);
  }

  public static void N0219(int paramInt, int[] paramArrayOfInt)
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace();
    }
try {
      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate("INSERT INTO cat.sch.atable values(12,1,6534567890,'Henry Dickenson',1239927,60050.50,7.784225,date '1999-12-10',time '11:59:59',timestamp '2001-01-10 10:45:59') ");
      ResultSet localResultSet;
      try {
        localResultSet = localStatement.executeQuery("SELECT COUNT(*) from cat.sch.atable");
      } catch (SQLException localSQLException2) {
        System.out.println("Problem reading scale");
        while (localSQLException2 != null) {
          System.out.println("Message:" + localSQLException2.getMessage());
          SQLException localSQLException3 = localSQLException2.getNextException();
        }return;
      }

      localResultSet.next();
      paramInt = localResultSet.getInt("id");
      paramArrayOfInt[0] = paramInt;
    }
    catch (SQLException localSQLException1) {
      sop("Error: could not INSERT a new row ");
      sop(localSQLException1.getMessage());
      localSQLException1.printStackTrace();
    }
  }

  public static void N0220(int paramInt, int[] paramArrayOfInt)
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace();
    }
try {
      Statement localStatement = localConnection.createStatement();
      ResultSet localResultSet;
      try {
        localResultSet = localStatement.executeQuery("SELECT id FROM cat.sch.atable WHERE index = 1");
      } catch (SQLException localSQLException2) {
        System.out.println("Problem reading scale");
        while (localSQLException2 != null) {
          System.out.println("Message:" + localSQLException2.getMessage());
          SQLException localSQLException3 = localSQLException2.getNextException();
        }
        return;
      }

      localResultSet.next();
      paramInt = localResultSet.getInt(1);
      paramArrayOfInt[0] = paramInt;
    }
    catch (SQLException localSQLException1)
    {
      sop("Error: could not INSERT a new row ");
      sop(localSQLException1.getMessage());
      localSQLException1.printStackTrace();
    }
  }

  public static void N0221(int paramInt, int[] paramArrayOfInt)
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace();
    }
try {
      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate("INSERT INTO cat.sch.atable values(14,9,1234561190,'Linda Baxter',1211587,65210.50,7.781255,date '2001-12-11',time '11:39:59',timestamp '2001-11-10 10:45:59') ");
      ResultSet localResultSet;
      try {
        localResultSet = localStatement.executeQuery("SELECT COUNT(*) from cat.sch.atable");
      } catch (SQLException localSQLException2) {
        System.out.println("Problem reading scale");
        while (localSQLException2 != null) {
          System.out.println("Message:" + localSQLException2.getMessage());
          SQLException localSQLException3 = localSQLException2.getNextException();
        }
        return;
      }

      localResultSet.next();
      paramInt = localResultSet.getInt(1);
      paramArrayOfInt[0] = paramInt;
    }
    catch (SQLException localSQLException1)
    {
      sop("Error: could not INSERT a new row ");
      sop(localSQLException1.getMessage());
      localSQLException1.printStackTrace();
    }
  }

  public static void N0234(int paramInt, int[] paramArrayOfInt)
  {
    String str = "jdbc:default:connection";
    try {
      Connection localConnection = DriverManager.getConnection(str);
      CallableStatement localCallableStatement = localConnection.prepareCall("{call cat.sch.N0219(35,?)}");
      Statement localStatement = localConnection.createStatement();
      ResultSet localResultSet;
      try { localResultSet = localStatement.executeQuery("SELECT COUNT(*) from cat.sch.atable");
      } catch (SQLException localSQLException2) {
        System.out.println("Problem reading scale");
        while (localSQLException2 != null) {
          System.out.println("Message:" + localSQLException2.getMessage());
          SQLException localSQLException3 = localSQLException2.getNextException();
        }
        return;
      }

      localResultSet.next();
      paramInt = localResultSet.getInt("id");
      paramArrayOfInt[0] = paramInt;
    }
    catch (SQLException localSQLException1) {
      sop("Error: could not INSERT a new row ");
      sop(localSQLException1.getMessage());
      localSQLException1.printStackTrace();
    }
  }

  public static void N1209(Double paramDouble, int[] paramArrayOfInt)
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace();
    }
try {
      Statement localStatement = localConnection.createStatement();
      ResultSet localResultSet;
      try {
        localResultSet = localStatement.executeQuery("SELECT salary from cat.sch.atable where index = 13");
      } catch (SQLException localSQLException2) {
        System.out.println("Problem reading scale");
        while (localSQLException2 != null) {
          System.out.println("Message:" + localSQLException2.getMessage());
          SQLException localSQLException3 = localSQLException2.getNextException();
        }
        return;
      }

      localResultSet.next();
      double d = localResultSet.getDouble("salary");
      paramDouble = new Double(d);
      paramArrayOfInt[0] = paramDouble.intValue();
    }
    catch (SQLException localSQLException1) {
      sop("Error: could not SELECT double ");
      sop(localSQLException1.getMessage());
      localSQLException1.printStackTrace();
    }
  }

  public static void N1210(Double paramDouble, int[] paramArrayOfInt)
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace();
    }
    try {
      Statement localStatement = localConnection.createStatement();
      ResultSet localResultSet;
      try {
        localResultSet = localStatement.executeQuery("UPDATE cat.sch.atable SET salary = 150000 WHERE index = 9");
        localResultSet = localStatement.executeQuery("SELECT salary from cat.sch.atable where index = 9");
      }
      catch (SQLException localSQLException2) {
        System.out.println("Problem reading scale");
        while (localSQLException2 != null) {
          System.out.println("Message:" + localSQLException2.getMessage());
          SQLException localSQLException3 = localSQLException2.getNextException();
        }
        return;
      }

      localResultSet.next();
      double d = localResultSet.getDouble("salary");
      paramDouble = new Double(d);
      paramArrayOfInt[0] = paramDouble.intValue();
    }
    catch (SQLException localSQLException1)
    {
      sop("Error: could not SELECT double ");
      sop(localSQLException1.getMessage());
      localSQLException1.printStackTrace();
    }
  }

  public static void N1211(Double paramDouble, int[] paramArrayOfInt)
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace();
    }

    try
    {
      Statement localStatement = localConnection.createStatement();
      try {
        ResultSet localResultSet = localStatement.executeQuery("ROLLBACK");
      }
      catch (SQLException localSQLException2) {
        System.out.println("Problem using transactional statement");
        while (localSQLException2 != null) {
          System.out.println("Message:" + localSQLException2.getMessage());
          SQLException localSQLException3 = localSQLException2.getNextException();
        }
        return;
      }

    }
    catch (SQLException localSQLException1)
    {
      sop(localSQLException1.getMessage());
      localSQLException1.printStackTrace();
    }
  }

  public static void N4334(short paramShort, short[] paramArrayOfShort, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = paramArrayOfShort[0];
    paramArrayOfShort[0] = paramShort;
  }

  public static void N4325(int paramInt, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = paramInt;
  }

  public static void N4014(short paramShort, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = paramShort;
  }

  public static void N4015(int paramInt, long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = paramInt;
  }

  public static void N4016(int paramInt, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = ((short)paramInt);
  }

  public static void N4018(long paramLong, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = ((int)paramLong);
  }

  public static void N4020(long paramLong, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = ((short)(int)paramLong);
  }

  public static void N4038(BigDecimal paramBigDecimal, long[] paramArrayOfLong)
  {
    long l = paramBigDecimal.longValue();
    paramArrayOfLong[0] = l;
  }

  public static void N4039(BigDecimal paramBigDecimal, short[] paramArrayOfShort)
  {
    int i = paramBigDecimal.shortValue();
    paramArrayOfShort[0] = (short)i;
  }

  public static void N4040(BigDecimal paramBigDecimal, int[] paramArrayOfInt)
  {
    int i = paramBigDecimal.intValue();
    paramArrayOfInt[0] = i;
  }

  public static void N4042(int paramInt, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramInt);
  }

  public static void N4043(short paramShort, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramShort);
  }

  public static void N4044(long paramLong, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramLong);
  }

  public static void N4048(float paramFloat, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramFloat;
  }

  public static void N4049(double paramDouble, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramDouble;
  }

  public static void N4050(double paramDouble, float[] paramArrayOfFloat)
  {
    paramArrayOfFloat[0] = ((float)paramDouble);
  }

  public static void N4054(int paramInt, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramInt;
  }

  public static void N4055(short paramShort, float[] paramArrayOfFloat)
  {
    paramArrayOfFloat[0] = paramShort;
  }

  public static void N4056(long paramLong, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramLong;
  }

  public static void N4057(float paramFloat, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = ((short)(int)paramFloat);
  }

  public static void N4058(double paramDouble, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = ((int)paramDouble);
  }

  public static void N4059(double paramDouble, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = ((short)(int)paramDouble);
  }

  public static void N4060(float paramFloat, long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = ((long)paramFloat);
  }

  public static void N4061(float paramFloat, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramFloat);
  }

  public static void N4063(double paramDouble, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramDouble);
  }

  public static void N4067(BigDecimal paramBigDecimal, float[] paramArrayOfFloat)
  {
    float f = paramBigDecimal.floatValue();
    paramArrayOfFloat[0] = f;
  }

  public static void N4068(BigDecimal paramBigDecimal, double[] paramArrayOfDouble)
  {
    double d = paramBigDecimal.doubleValue();
    paramArrayOfDouble[0] = d;
  }

  public static void N4079(double paramDouble, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = ((short)(int)paramDouble);
  }

  public static void N4080(double paramDouble, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = ((int)paramDouble);
  }

  public static void N4081(short paramShort, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramShort;
  }

  public static void N4082(long paramLong, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramLong;
  }

  public static void N4208(Timestamp paramTimestamp)
  {
    System.out.println("Timestamp " + paramTimestamp + ".");
  }

  public static void N4210(Time paramTime)
  {
    System.out.println("Time " + paramTime + ".");
  }

  public static void N4211(Date paramDate)
  {
    System.out.println("Date " + paramDate + ".");
  }

  public static void N4214(short paramShort, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = paramShort;
  }

  public static void N4215(int paramInt, long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = paramInt;
  }

  public static void N4216(int paramInt, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = ((short)paramInt);
  }

  public static void N4218(long paramLong, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = ((int)paramLong);
  }

  public static void N4220(long paramLong, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = ((short)(int)paramLong);
  }

  public static void N4238(BigDecimal paramBigDecimal, long[] paramArrayOfLong)
  {
    long l = paramBigDecimal.longValue();
    paramArrayOfLong[0] = l;
  }

  public static void N4239(BigDecimal paramBigDecimal, short[] paramArrayOfShort)
  {
    int i = paramBigDecimal.shortValue();
    paramArrayOfShort[0] = (short)i;
  }

  public static void N4240(BigDecimal paramBigDecimal, int[] paramArrayOfInt)
  {
    int i = paramBigDecimal.intValue();
    paramArrayOfInt[0] = i;
  }

  public static void N4242(int paramInt, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramInt);
  }

  public static void N4243(short paramShort, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramShort);
  }

  public static void N4244(long paramLong, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramLong);
  }

  public static void N4248(float paramFloat, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramFloat;
  }

  public static void N4249(double paramDouble, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramDouble;
  }

  public static void N4250(double paramDouble, float[] paramArrayOfFloat)
  {
    paramArrayOfFloat[0] = ((float)paramDouble);
  }

  public static void N4254(int paramInt, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramInt;
  }

  public static void N4255(short paramShort, float[] paramArrayOfFloat)
  {
    paramArrayOfFloat[0] = paramShort;
  }

  public static void N4256(long paramLong, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramLong;
  }

  public static void N4257(float paramFloat, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramFloat);
  }

  public static void N4258(double paramDouble, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = ((int)paramDouble);
  }

  public static void N4259(double paramDouble, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = ((short)(int)paramDouble);
  }

  public static void N4260(float paramFloat, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = ((int)paramFloat);
  }

  public static void N4261(BigDecimal paramBigDecimal, float[] paramArrayOfFloat)
  {
    float f = paramBigDecimal.floatValue();
    paramArrayOfFloat[0] = f;
  }

  public static void N4263(double paramDouble, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramDouble);
  }

  public static void N4267(BigDecimal paramBigDecimal, float[] paramArrayOfFloat)
  {
    float f = paramBigDecimal.floatValue();
    paramArrayOfFloat[0] = f;
  }

  public static void N4268(BigDecimal paramBigDecimal, double[] paramArrayOfDouble)
  {
    double d = paramBigDecimal.doubleValue();
    paramArrayOfDouble[0] = d;
  }

  public static void N4279(short paramShort, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramShort;
  }

  public static void N4280(int paramInt, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramInt;
  }

  public static void N4281(double paramDouble, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = ((int)paramDouble);
  }

  public static void N4282(long paramLong, float[] paramArrayOfFloat)
  {
    paramArrayOfFloat[0] = ((float)paramLong);
  }

  public static void N4283(double paramDouble, long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = ((long)paramDouble);
  }

  public static void N4284(double paramDouble, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = ((short)(int)paramDouble);
  }

  public static void N4286(double paramDouble, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramDouble);
  }

  public static void N0176(float paramFloat)
  {
    System.out.println("IN1 Value    :" + paramFloat);
  }

  public static void N0177(float[] paramArrayOfFloat)
  {
    System.out.println("INOUT1 Value    :" + paramArrayOfFloat[0]);
  }

  public static void N0178(double[] paramArrayOfDouble)
  {
    System.out.println("INOUT1 Value    :" + paramArrayOfDouble[0]);
  }

  public static void N0179(int[] paramArrayOfInt)
  {
    System.out.println("INOUT1 Value    :" + paramArrayOfInt[0]);
  }

  public static void N0180(short[] paramArrayOfShort)
  {
    System.out.println("INOUT1 Value    :" + paramArrayOfShort[0]);
  }

  public static void N0181(long[] paramArrayOfLong)
  {
    System.out.println("INOUT1 Value    :" + paramArrayOfLong[0]);
  }

  public static void N0182(BigDecimal[] paramArrayOfBigDecimal)
  {
    System.out.println("INOUT1 Value    :" + paramArrayOfBigDecimal[0]);
  }

  public static void N0183(String[] paramArrayOfString)
  {
    System.out.println("INOUT1 Value    :" + paramArrayOfString[0]);
  }

  public static void N0184(double paramDouble)
  {
    System.out.println("IN1 Value    :" + paramDouble);
  }

  public static void N0185(int paramInt)
  {
    System.out.println("IN1 Value    :" + paramInt);
  }

  public static void N0186(short paramShort)
  {
    System.out.println("IN1 Value    :" + paramShort);
  }

  public static void N0187(long paramLong)
  {
    System.out.println("IN1 Value    :" + paramLong);
  }

  public static void N0188(int paramInt)
  {
    System.out.println("IN1 Value    :" + paramInt);
  }

  public static void N0189(String paramString)
  {
    System.out.println("IN1 Value    :" + paramString);
  }

  public static void N0305(BigDecimal paramBigDecimal, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = paramBigDecimal;
  }

  public static void N4100(Time paramTime, String[] paramArrayOfString, Time[] paramArrayOfTime)
  {
    paramArrayOfString[0] = String.valueOf(paramArrayOfTime[0]);
    paramArrayOfTime[0] = Time.valueOf(paramArrayOfString[0]);
  }

  public static void N4101(long paramLong, long[] paramArrayOfLong, int[] paramArrayOfInt)
  {
    paramArrayOfLong[0] = paramLong;
    paramArrayOfInt[0] = ((int)paramArrayOfLong[0]);
  }

  public static void N4102(short paramShort, short[] paramArrayOfShort, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramShort);
    paramArrayOfShort[0] = Short.valueOf(paramArrayOfString[0]).shortValue();
  }

  public static void N4103(int paramInt, int[] paramArrayOfInt, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfInt[0] = paramArrayOfBigDecimal[0].scale();
    paramArrayOfBigDecimal[0] = new BigDecimal(paramInt);
  }

  public static void N4104(long paramLong, int[] paramArrayOfInt, long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = paramLong;
    paramArrayOfLong[0] = paramArrayOfInt[0];
  }

  public static void N4105(float paramFloat, float[] paramArrayOfFloat, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = ((int)paramFloat);
    paramArrayOfFloat[0] = paramArrayOfInt[0];
  }

  public static void N4106(double paramDouble, double[] paramArrayOfDouble, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramArrayOfDouble[0]);
    paramArrayOfString[0] = String.valueOf(paramDouble);
  }

  public static void N4107(String paramString, String[] paramArrayOfString1, String[] paramArrayOfString2)
  {
    paramArrayOfString2[0] = paramArrayOfString1[0];
    paramArrayOfString1[0] = paramString;
  }

  public static void N0001()
    throws Exception
  {
    System.out.println("SPJ N0001 has no parameters");
  }

  public static void N0100(String paramString, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramString);
  }

  public static void N0101(BigDecimal paramBigDecimal)
  {
    System.out.println("Decimal " + paramBigDecimal + ".");
  }

  public static void N0102(String paramString, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = Short.valueOf(paramString).shortValue();
  }

  public static void N0103(String paramString, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = Integer.valueOf(paramString).intValue();
  }

  public static void N0104(String paramString, long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = Long.valueOf(paramString).longValue();
  }

  public static void N0105(String paramString, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = Double.valueOf(paramString).doubleValue();
  }

  public static void N0106(String paramString, Time[] paramArrayOfTime)
  {
    paramArrayOfTime[0] = Time.valueOf(paramString.toString());
  }

  public static void N0107(String paramString, Timestamp[] paramArrayOfTimestamp)
  {
    paramArrayOfTimestamp[0] = Timestamp.valueOf(paramString.toString());
  }

  public static void N0108(BigDecimal paramBigDecimal, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramBigDecimal);
  }

  public static void N0109(int paramInt, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramInt);
  }

  public static void N0110(long paramLong, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramLong);
  }

  public static void N0111(float paramFloat, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramFloat);
  }

  public static void N0112(double paramDouble, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramDouble);
  }

  public static void N0113(Date paramDate, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramDate);
  }

  public static void N0114(Time paramTime, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramTime);
  }

  public static void N0115(Timestamp paramTimestamp, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramTimestamp);
  }

  public static void N0116(String paramString, BigDecimal[] paramArrayOfBigDecimal1, BigDecimal[] paramArrayOfBigDecimal2)
  {
    paramArrayOfBigDecimal2[0] = new BigDecimal(paramString);
    paramArrayOfBigDecimal1[0] = paramArrayOfBigDecimal2[0];
  }

  public static void N0117(String paramString, short[] paramArrayOfShort1, short[] paramArrayOfShort2)
  {
    paramArrayOfShort2[0] = Short.valueOf(paramString).shortValue();
    paramArrayOfShort1[0] = paramArrayOfShort2[0];
  }

  public static void N0118(String paramString, int[] paramArrayOfInt1, int[] paramArrayOfInt2)
  {
    paramArrayOfInt2[0] = Integer.valueOf(paramString).intValue();

    paramArrayOfInt1[0] = paramArrayOfInt2[0];
  }

  public static void N0119(String paramString, long[] paramArrayOfLong1, long[] paramArrayOfLong2)
  {
    paramArrayOfLong2[0] = Long.valueOf(paramString).longValue();
    paramArrayOfLong1[0] = paramArrayOfLong2[0];
  }

  public static void N0120(String paramString, float[] paramArrayOfFloat1, float[] paramArrayOfFloat2)
  {
    paramArrayOfFloat2[0] = Float.valueOf(paramString).floatValue();
    paramArrayOfFloat1[0] = paramArrayOfFloat2[0];
  }

  public static void N0121(String paramString, double[] paramArrayOfDouble1, double[] paramArrayOfDouble2)
  {
    paramArrayOfDouble2[0] = Double.valueOf(paramString).doubleValue();
    paramArrayOfDouble1[0] = paramArrayOfDouble2[0];
  }

  public static void N0122(String paramString, Date[] paramArrayOfDate1, Date[] paramArrayOfDate2)
  {
    paramArrayOfDate2[0] = Date.valueOf(paramString.toString());
    paramArrayOfDate1[0] = paramArrayOfDate2[0];
  }

  public static void N0123(String paramString, Time[] paramArrayOfTime1, Time[] paramArrayOfTime2)
  {
    paramArrayOfTime2[0] = Time.valueOf(paramString.toString());
    paramArrayOfTime1[0] = paramArrayOfTime2[0];
  }

  public static void N0124(String paramString, Timestamp[] paramArrayOfTimestamp1, Timestamp[] paramArrayOfTimestamp2)
  {
    paramArrayOfTimestamp2[0] = Timestamp.valueOf(paramString.toString());
    paramArrayOfTimestamp1[0] = paramArrayOfTimestamp2[0];
  }

  public static void N0125(String paramString1, String[] paramArrayOfString1, String[] paramArrayOfString2, String paramString2)
  {
    paramArrayOfString1[0] = paramString1;
    paramArrayOfString1[0] = paramString2;
    paramArrayOfString2[0] = paramArrayOfString1[0];
  }

  public static void N0126(String paramString, BigDecimal[] paramArrayOfBigDecimal, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = paramString;
    paramArrayOfString[0] = String.valueOf(paramArrayOfBigDecimal[0]);
  }

  public static void N0127(String paramString, short[] paramArrayOfShort, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = paramString;
    paramArrayOfString[0] = String.valueOf(paramArrayOfShort[0]);
  }

  public static void N0128(String paramString, int[] paramArrayOfInt, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = paramString;
    paramArrayOfString[0] = String.valueOf(paramArrayOfInt[0]);
  }

  public static void N0129(String paramString, long[] paramArrayOfLong, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = paramString;
    paramArrayOfString[0] = String.valueOf(paramArrayOfLong[0]);
  }

  public static void N0130(String paramString, float[] paramArrayOfFloat, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = paramString;
    paramArrayOfString[0] = String.valueOf(paramArrayOfFloat[0]);
  }

  public static void N0131(String paramString, double[] paramArrayOfDouble, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = paramString;
    paramArrayOfString[0] = String.valueOf(paramArrayOfDouble[0]);
  }

  public static void N0132(String paramString, Date[] paramArrayOfDate, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = paramString;
    paramArrayOfString[0] = String.valueOf(paramArrayOfDate[0]);
  }

  public static void N0133(String paramString, Time[] paramArrayOfTime, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = paramString;
    paramArrayOfString[0] = String.valueOf(paramArrayOfTime[0]);
  }

  public static void N0134(String paramString, Timestamp[] paramArrayOfTimestamp, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = paramString;
    paramArrayOfString[0] = String.valueOf(paramArrayOfTimestamp[0]);
  }

  public static void N0135(String paramString, BigDecimal[] paramArrayOfBigDecimal, String[] paramArrayOfString, BigDecimal paramBigDecimal)
  {
    paramArrayOfString[0] = paramString;
    paramArrayOfBigDecimal[0] = paramBigDecimal;
    paramArrayOfString[0] = String.valueOf(paramArrayOfBigDecimal[0]);
  }

  public static void N0136(String paramString, short[] paramArrayOfShort, String[] paramArrayOfString, short paramShort)
  {
    paramArrayOfString[0] = paramString;
    paramArrayOfShort[0] = paramShort;
    paramArrayOfString[0] = String.valueOf(paramArrayOfShort[0]);
  }

  public static void N0137(String paramString, int[] paramArrayOfInt, String[] paramArrayOfString, int paramInt)
  {
    paramArrayOfString[0] = paramString;
    paramArrayOfInt[0] = paramInt;
    paramArrayOfString[0] = String.valueOf(paramArrayOfInt[0]);
  }

  public static void N0138(String paramString, long[] paramArrayOfLong, String[] paramArrayOfString, long paramLong)
  {
    paramArrayOfString[0] = paramString;
    paramArrayOfLong[0] = paramLong;
    paramArrayOfString[0] = String.valueOf(paramArrayOfLong[0]);
  }

  public static void N0139(String paramString, float[] paramArrayOfFloat, String[] paramArrayOfString, float paramFloat)
  {
    paramArrayOfString[0] = paramString;
    paramArrayOfFloat[0] = paramFloat;
    paramArrayOfString[0] = String.valueOf(paramArrayOfFloat[0]);
  }

  public static void N0140(String paramString, double[] paramArrayOfDouble, String[] paramArrayOfString, double paramDouble)
  {
    paramArrayOfString[0] = paramString;
    paramArrayOfDouble[0] = paramDouble;
    paramArrayOfString[0] = String.valueOf(paramArrayOfDouble[0]);
  }

  public static void N0141(String paramString, Date[] paramArrayOfDate, String[] paramArrayOfString, Date paramDate)
  {
    paramArrayOfString[0] = paramString;
    paramArrayOfDate[0] = paramDate;
    paramArrayOfString[0] = String.valueOf(paramArrayOfDate[0]);
  }

  public static void N0142(String paramString, Time[] paramArrayOfTime, String[] paramArrayOfString, Time paramTime)
  {
    paramArrayOfString[0] = paramString;
    paramArrayOfTime[0] = paramTime;
    paramArrayOfString[0] = String.valueOf(paramArrayOfTime[0]);
  }

  public static void N0143(String paramString, Timestamp[] paramArrayOfTimestamp, String[] paramArrayOfString, Timestamp paramTimestamp)
  {
    paramArrayOfString[0] = paramString;
    paramArrayOfTimestamp[0] = paramTimestamp;
    paramArrayOfString[0] = String.valueOf(paramArrayOfTimestamp[0]);
  }

  public static void N0144(String paramString, Timestamp[] paramArrayOfTimestamp1, Timestamp[] paramArrayOfTimestamp2, Timestamp paramTimestamp)
  {
    paramArrayOfTimestamp2[0] = Timestamp.valueOf(paramString.toString());
    paramArrayOfTimestamp1[0] = paramTimestamp;
    paramArrayOfTimestamp1[0] = paramArrayOfTimestamp2[0];
  }

  public static void N0145(String paramString, String[] paramArrayOfString1, String[] paramArrayOfString2, Timestamp paramTimestamp)
  {
    paramArrayOfString2[0] = paramString;
    paramArrayOfString1[0] = String.valueOf(paramTimestamp);
    paramArrayOfString1[0] = paramArrayOfString2[0];
  }

  public static void N0146(String paramString, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramString);
  }

  public static void N0147(String paramString, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = Short.valueOf(paramString).shortValue();
  }

  public static void N0148(String paramString, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = Integer.valueOf(paramString).intValue();
  }

  public static void N0149(String paramString, long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = Long.valueOf(paramString).longValue();
  }

  public static void N0150(String paramString, float[] paramArrayOfFloat)
  {
    paramArrayOfFloat[0] = Float.valueOf(paramString).floatValue();
  }

  public static void N0151(String paramString, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = Double.valueOf(paramString).doubleValue();
  }

  public static void N0152(String paramString, Date[] paramArrayOfDate)
  {
    paramArrayOfDate[0] = Date.valueOf(paramString.toString());
  }

  public static void N0153(String paramString, Time[] paramArrayOfTime)
  {
    paramArrayOfTime[0] = Time.valueOf(paramString.toString());
  }

  public static void N0154(String paramString, Timestamp[] paramArrayOfTimestamp)
  {
    paramArrayOfTimestamp[0] = Timestamp.valueOf(paramString.toString());
  }

  public static void N0190(double paramDouble, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramDouble;
  }

  public static void N0191(Float paramFloat, Float[] paramArrayOfFloat)
  {
    paramArrayOfFloat[0] = paramFloat;
  }

  public static void N0192(Integer paramInteger, Integer[] paramArrayOfInteger)
  {
    paramArrayOfInteger[0] = paramInteger;
  }

  public static void N0193(Long paramLong, Long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = paramLong;
  }

  public static void N0194(BigDecimal paramBigDecimal, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = paramBigDecimal;
  }

  public static void N0195(String paramString, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = paramString;
  }

  public static void N0199(BigDecimal paramBigDecimal, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = paramBigDecimal;
  }

  public static void N0200(String paramString, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = paramString;
  }

  public static void N0201(String paramString, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = paramString;
  }

  public static void N0202(BigDecimal paramBigDecimal, BigDecimal[] paramArrayOfBigDecimal)
  {
    if (paramBigDecimal == null)
      paramArrayOfBigDecimal[0] = null;
    else
      paramArrayOfBigDecimal[0] = paramBigDecimal;
  }

  public static void N0203(Date paramDate, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = ("[" + paramDate + "]");
  }

  public static void N0204(short paramShort, float[] paramArrayOfFloat)
  {
    paramArrayOfFloat[0] = paramShort;
  }

  public static void N0205(short paramShort, byte[] paramArrayOfByte, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = ("[" + paramShort + "]");
    paramArrayOfByte[0] = ((byte)paramShort);
  }

  public static void N0206(String paramString, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = paramString;
  }

  public static void N0207(String[] paramArrayOfString, Timestamp paramTimestamp)
  {
    paramArrayOfString[0] = paramTimestamp.toString();
  }

  public static void N0208(long[] paramArrayOfLong, float paramFloat)
  {
    paramArrayOfLong[0] = ((long)paramFloat);
  }

  public static void N0209(short paramShort, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = paramShort;
  }

  public static void N0210(int paramInt, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = paramInt;
  }

  public static void N0211(long paramLong, long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = paramLong;
  }

  public static void N0212(float paramFloat, float[] paramArrayOfFloat)
  {
    paramArrayOfFloat[0] = paramFloat;
  }

  public static void N0198(float paramFloat, float[] paramArrayOfFloat)
  {
    paramArrayOfFloat[0] = paramFloat;
  }

  public static void N0213(double paramDouble, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramDouble;
  }

  public static void N0214(String paramString, String[] paramArrayOfString)
  {
    StringBuffer localStringBuffer = new StringBuffer(paramString);
    localStringBuffer.reverse();
    paramArrayOfString[0] = localStringBuffer.toString();
  }

  public static void N0215(Date paramDate, Date[] paramArrayOfDate)
  {
    paramArrayOfDate[0] = paramDate;
  }

  public static void N0216(Time paramTime, Time[] paramArrayOfTime)
  {
    if (paramTime == null)
      paramArrayOfTime[0] = null;
    else
      paramArrayOfTime[0] = paramTime;
  }

  public static void N0217(Timestamp paramTimestamp, Timestamp[] paramArrayOfTimestamp)
  {
    if (paramTimestamp == null)
      paramArrayOfTimestamp[0] = null;
    else
      paramArrayOfTimestamp[0] = paramTimestamp;
  }

  public static void N0218(int paramInt, float[] paramArrayOfFloat)
  {
    paramArrayOfFloat[0] = paramInt;
  }

  public static void N0222(Date paramDate)
  {
    System.out.println("IN1 Value    :" + paramDate);
  }

  public static void N0223(Time paramTime)
  {
    System.out.println("IN1 Value    :" + paramTime);
  }

  public static void N0224(Timestamp paramTimestamp)
  {
    System.out.println("IN1 Value    :" + paramTimestamp);
  }

  public static void N0226(String paramString1, int paramInt, String paramString2, String paramString3, BigDecimal paramBigDecimal1, short paramShort, Date paramDate, Time paramTime, Timestamp paramTimestamp, long paramLong, double paramDouble1, float paramFloat, double paramDouble2, BigDecimal paramBigDecimal2, BigDecimal paramBigDecimal3, BigDecimal paramBigDecimal4, BigDecimal paramBigDecimal5, String[] paramArrayOfString1, int[] paramArrayOfInt1, String[] paramArrayOfString2, String[] paramArrayOfString3, BigDecimal[] paramArrayOfBigDecimal1, short[] paramArrayOfShort1, Date[] paramArrayOfDate1, Time[] paramArrayOfTime1, Timestamp[] paramArrayOfTimestamp1, long[] paramArrayOfLong1, double[] paramArrayOfDouble1, float[] paramArrayOfFloat1, double[] paramArrayOfDouble2, BigDecimal[] paramArrayOfBigDecimal2, BigDecimal[] paramArrayOfBigDecimal3, BigDecimal[] paramArrayOfBigDecimal4, BigDecimal[] paramArrayOfBigDecimal5, String[] paramArrayOfString4, int[] paramArrayOfInt2, String[] paramArrayOfString5, String[] paramArrayOfString6, BigDecimal[] paramArrayOfBigDecimal6, short[] paramArrayOfShort2, Date[] paramArrayOfDate2, Time[] paramArrayOfTime2, Timestamp[] paramArrayOfTimestamp2, long[] paramArrayOfLong2, double[] paramArrayOfDouble3, float[] paramArrayOfFloat2, double[] paramArrayOfDouble4, BigDecimal[] paramArrayOfBigDecimal7, BigDecimal[] paramArrayOfBigDecimal8, BigDecimal[] paramArrayOfBigDecimal9, BigDecimal[] paramArrayOfBigDecimal10)
  {
    paramArrayOfString4[0] = paramString1;
    paramArrayOfInt2[0] = paramInt;
    paramArrayOfString5[0] = paramString2;
    paramArrayOfString6[0] = paramString3;
    paramArrayOfBigDecimal6[0] = paramBigDecimal1;
    paramArrayOfShort2[0] = paramShort;
    paramArrayOfDate2[0] = paramDate;
    paramArrayOfTime2[0] = paramTime;
    paramArrayOfTimestamp2[0] = paramTimestamp;
    paramArrayOfLong2[0] = paramLong;
    paramArrayOfDouble3[0] = paramDouble1;
    paramArrayOfFloat2[0] = paramFloat;
    paramArrayOfDouble4[0] = paramDouble2;
    paramArrayOfBigDecimal7[0] = paramBigDecimal2;
    paramArrayOfBigDecimal8[0] = paramBigDecimal3;
    paramArrayOfBigDecimal9[0] = paramBigDecimal4;
    paramArrayOfBigDecimal10[0] = paramBigDecimal5;
    paramArrayOfString1[0] = paramArrayOfString4[0];
    paramArrayOfInt1[0] = paramArrayOfInt2[0];
    paramArrayOfString2[0] = paramArrayOfString5[0];
    paramArrayOfString3[0] = paramArrayOfString6[0];
    paramArrayOfBigDecimal1[0] = paramArrayOfBigDecimal6[0];
    paramArrayOfShort1[0] = paramArrayOfShort2[0];
    paramArrayOfDate1[0] = paramArrayOfDate2[0];
    paramArrayOfTime1[0] = paramArrayOfTime2[0];
    paramArrayOfTimestamp1[0] = paramArrayOfTimestamp2[0];
    paramArrayOfLong1[0] = paramArrayOfLong2[0];
    paramArrayOfDouble1[0] = paramArrayOfDouble3[0];
    paramArrayOfFloat1[0] = paramArrayOfFloat2[0];
    paramArrayOfDouble2[0] = paramArrayOfDouble4[0];
    paramArrayOfBigDecimal2[0] = paramArrayOfBigDecimal7[0];
    paramArrayOfBigDecimal3[0] = paramArrayOfBigDecimal8[0];
    paramArrayOfBigDecimal4[0] = paramArrayOfBigDecimal9[0];
    paramArrayOfBigDecimal5[0] = paramArrayOfBigDecimal10[0];
  }

  public static void N0227(String paramString, String[] paramArrayOfString)
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace(); } 
    try {
      Statement localStatement = localConnection.createStatement();
      sop("Inserting sql(hello)");
      localStatement.executeUpdate("insert into cat.sch.emp values('Rajani')");
      System.out.println("SQL insert completed");
      ResultSet localResultSet;
      try { localResultSet = localStatement.executeQuery("select user from cat.sch.usertab");
      } catch (SQLException localSQLException2) {
        System.out.println("Problem reading table");
        while (localSQLException2 != null) {
          System.out.println("Message:" + localSQLException2.getMessage());
          SQLException localSQLException3 = localSQLException2.getNextException();
        }
        return;
      }

      localResultSet.next();
      paramString = localResultSet.getString(1);
      paramArrayOfString[0] = paramString;
    }
    catch (SQLException localSQLException1)
    {
      sop("Error: could not INSERT String ");
      sop(localSQLException1.getMessage());
      localSQLException1.printStackTrace();
    }
  }

  public static void N0228(String paramString, String[] paramArrayOfString)
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace(); } 
try { Statement localStatement = localConnection.createStatement();
      sop("Inserting sql(hello)");
      localStatement.executeUpdate("delete from cat.sch.emp");
      localStatement.executeUpdate("insert into cat.sch.emp values('Rajani')");
      System.out.println("SQL insert completed");
      ResultSet localResultSet;
      try { localResultSet = localStatement.executeQuery("select current_user from cat.sch.emp");
      } catch (SQLException localSQLException2) {
        System.out.println("Problem reading table");
        while (localSQLException2 != null) {
          System.out.println("Message:" + localSQLException2.getMessage());
          SQLException localSQLException3 = localSQLException2.getNextException();
        }
        return;
      }

      localResultSet.next();
      paramString = localResultSet.getString(1);
      paramArrayOfString[0] = paramString;
    }
    catch (SQLException localSQLException1)
    {
      sop("Error: could not INSERT String ");
      sop(localSQLException1.getMessage());
      localSQLException1.printStackTrace();
    }
  }

  public static void N0238(String paramString, String[] paramArrayOfString)
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace();
    }
    try
    {
      Statement localStatement = localConnection.createStatement();
      sop("Inserting sql(hello)");
      localStatement.executeUpdate("insert into cat.sch.emp values('Rajani')");
    }
    catch (SQLException localSQLException1)
    {
      System.out.println("Problem inserting a row");
      while (localSQLException1 != null) {
        System.out.println("Message:" + localSQLException1.getMessage());
        SQLException localSQLException2 = localSQLException1.getNextException();
      }
      return;
    }
  }

  public static void N0229(String paramString, String[] paramArrayOfString)
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace(); } 
try { Statement localStatement = localConnection.createStatement();
      sop("Inserting sql(hello)");
      localStatement.executeUpdate("delete from cat.sch.emp");
      localStatement.executeUpdate("insert into cat.sch.emp values('Radha')");
      System.out.println("SQL insert completed");
      ResultSet localResultSet;
      try { localResultSet = localStatement.executeQuery("select ename from cat.sch.emp");
      } catch (SQLException localSQLException2) {
        System.out.println("Problem reading table");
        while (localSQLException2 != null) {
          System.out.println("Message:" + localSQLException2.getMessage());
          SQLException localSQLException3 = localSQLException2.getNextException();
        }
        return;
      }

      localResultSet.next();
      paramString = localResultSet.getString(1);
      paramArrayOfString[0] = paramString;
    }
    catch (SQLException localSQLException1)
    {
      sop("Error: could not INSERT String ");
      sop(localSQLException1.getMessage());
      localSQLException1.printStackTrace();
    }
  }

  public static void N0235(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace();
    }

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("insert into cat.sch.emp values('AAA Computers')");
    System.out.println("SQL insert completed");
  }

  public static void N0233(String paramString1, int paramInt, String paramString2, String paramString3, BigDecimal paramBigDecimal1, short paramShort, Date paramDate, Time paramTime, Timestamp paramTimestamp, long paramLong, double paramDouble1, float paramFloat, double paramDouble2, BigDecimal paramBigDecimal2, BigDecimal paramBigDecimal3, BigDecimal paramBigDecimal4, BigDecimal paramBigDecimal5, String[] paramArrayOfString1, int[] paramArrayOfInt, String[] paramArrayOfString2, String[] paramArrayOfString3, BigDecimal[] paramArrayOfBigDecimal1, short[] paramArrayOfShort, Date[] paramArrayOfDate, Time[] paramArrayOfTime, Timestamp[] paramArrayOfTimestamp, long[] paramArrayOfLong, double[] paramArrayOfDouble1, float[] paramArrayOfFloat, double[] paramArrayOfDouble2, BigDecimal[] paramArrayOfBigDecimal2, BigDecimal[] paramArrayOfBigDecimal3, BigDecimal[] paramArrayOfBigDecimal4, BigDecimal[] paramArrayOfBigDecimal5)
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace(); } 
try { Statement localStatement = localConnection.createStatement();
      sop("Inserting sql(hello)");
      localStatement.executeUpdate("delete from cat.sch.testtab");
      localStatement.executeUpdate("insert into cat.sch.testtab values('AAA Computers',1234567890,'San Francisco','programmer', 123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.out.println("SQL insert completed");
      ResultSet localResultSet1;
      ResultSet localResultSet2;
      ResultSet localResultSet3;
      ResultSet localResultSet4;
      ResultSet localResultSet5;
      ResultSet localResultSet6;
      ResultSet localResultSet7;
      ResultSet localResultSet8;
      ResultSet localResultSet9;
      ResultSet localResultSet10;
      ResultSet localResultSet11;
      ResultSet localResultSet12;
      ResultSet localResultSet13;
      ResultSet localResultSet14;
      ResultSet localResultSet15;
      ResultSet localResultSet16;
      ResultSet localResultSet17;
      try { localResultSet1 = localStatement.executeQuery("select e_name from cat.sch.testtab");
        localResultSet2 = localStatement.executeQuery("select e_num from cat.sch.testtab");
        localResultSet3 = localStatement.executeQuery("select e_city from cat.sch.testtab");
        localResultSet4 = localStatement.executeQuery("select e_title from cat.sch.testtab");
        localResultSet5 = localStatement.executeQuery("select e_salary from cat.sch.testtab");
        localResultSet6 = localStatement.executeQuery("select e_code from cat.sch.testtab");
        localResultSet7 = localStatement.executeQuery("select e_date from cat.sch.testtab");
        localResultSet8 = localStatement.executeQuery("select e_time from cat.sch.testtab");
        localResultSet9 = localStatement.executeQuery("select e_tstamp from cat.sch.testtab");
        localResultSet10 = localStatement.executeQuery("select e_long from cat.sch.testtab");
        localResultSet11 = localStatement.executeQuery("select e_float from cat.sch.testtab");
        localResultSet12 = localStatement.executeQuery("select e_real from cat.sch.testtab");
        localResultSet13 = localStatement.executeQuery("select e_double from cat.sch.testtab");
        localResultSet14 = localStatement.executeQuery("select e_numeric from cat.sch.testtab");
        localResultSet15 = localStatement.executeQuery("select e_decimal from cat.sch.testtab");
        localResultSet16 = localStatement.executeQuery("select e_numeric1 from cat.sch.testtab");
        localResultSet17 = localStatement.executeQuery("select e_decimal1 from cat.sch.testtab");
      } catch (SQLException localSQLException2)
      {
        System.out.println("Problem reading table");
        while (localSQLException2 != null) {
          System.out.println("Message:" + localSQLException2.getMessage());
          SQLException localSQLException3 = localSQLException2.getNextException();
        }
        return;
      }

      paramString1 = localResultSet1.getString(1);
      paramArrayOfString1[0] = paramString1;
      paramInt = localResultSet2.getInt(1);
      paramArrayOfInt[0] = paramInt;
      paramString2 = localResultSet3.getString(1);
      paramArrayOfString2[0] = paramString2;
      paramString3 = localResultSet4.getString(1);
      paramArrayOfString3[0] = paramString3;
      paramBigDecimal1 = localResultSet5.getBigDecimal(1);
      paramArrayOfBigDecimal1[0] = paramBigDecimal1;
      paramShort = localResultSet6.getShort(1);
      paramArrayOfShort[0] = paramShort;
      paramDate = localResultSet7.getDate(1);
      paramArrayOfDate[0] = paramDate;
      paramTime = localResultSet8.getTime(1);
      paramArrayOfTime[0] = paramTime;
      paramTimestamp = localResultSet9.getTimestamp(1);
      paramArrayOfTimestamp[0] = paramTimestamp;
      paramLong = localResultSet10.getLong(1);
      paramArrayOfLong[0] = paramLong;
      paramDouble1 = localResultSet11.getDouble(1);
      paramArrayOfDouble1[0] = paramDouble1;
      paramFloat = localResultSet12.getFloat(1);
      paramArrayOfFloat[0] = paramFloat;
      paramDouble2 = localResultSet13.getDouble(1);
      paramArrayOfDouble2[0] = paramDouble2;
      paramBigDecimal2 = localResultSet14.getBigDecimal(1);
      paramArrayOfBigDecimal2[0] = paramBigDecimal2;
      paramBigDecimal3 = localResultSet15.getBigDecimal(1);
      paramArrayOfBigDecimal3[0] = paramBigDecimal3;
      paramBigDecimal4 = localResultSet16.getBigDecimal(1);
      paramArrayOfBigDecimal4[0] = paramBigDecimal4;
      paramBigDecimal5 = localResultSet17.getBigDecimal(1);
      paramArrayOfBigDecimal5[0] = paramBigDecimal5;
    }
    catch (SQLException localSQLException1)
    {
      sop("Error: could not INSERT String ");
      sop(localSQLException1.getMessage());
      localSQLException1.printStackTrace();
    }
  }

  public static void N0240(String paramString1, int paramInt, String paramString2, String paramString3, BigDecimal paramBigDecimal1, short paramShort, Date paramDate, Time paramTime, Timestamp paramTimestamp, long paramLong, double paramDouble1, float paramFloat, double paramDouble2, BigDecimal paramBigDecimal2, BigDecimal paramBigDecimal3, BigDecimal paramBigDecimal4, BigDecimal paramBigDecimal5, String[] paramArrayOfString1, int[] paramArrayOfInt, String[] paramArrayOfString2, String[] paramArrayOfString3, BigDecimal[] paramArrayOfBigDecimal1, short[] paramArrayOfShort, Date[] paramArrayOfDate, Time[] paramArrayOfTime, Timestamp[] paramArrayOfTimestamp, long[] paramArrayOfLong, double[] paramArrayOfDouble1, float[] paramArrayOfFloat, double[] paramArrayOfDouble2, BigDecimal[] paramArrayOfBigDecimal2, BigDecimal[] paramArrayOfBigDecimal3, BigDecimal[] paramArrayOfBigDecimal4, BigDecimal[] paramArrayOfBigDecimal5)
  {
    paramArrayOfString1[0] = paramString1;
    paramArrayOfInt[0] = paramInt;
    paramArrayOfString2[0] = paramString2;
    paramArrayOfString3[0] = paramString3;
    paramArrayOfBigDecimal1[0] = paramBigDecimal1;
    paramArrayOfShort[0] = paramShort;
    paramArrayOfDate[0] = paramDate;
    paramArrayOfTime[0] = paramTime;
    paramArrayOfTimestamp[0] = paramTimestamp;
    paramArrayOfLong[0] = paramLong;
    paramArrayOfDouble1[0] = paramDouble1;
    paramArrayOfFloat[0] = paramFloat;
    paramArrayOfDouble2[0] = paramDouble2;
    paramArrayOfBigDecimal2[0] = paramBigDecimal2;
    paramArrayOfBigDecimal3[0] = paramBigDecimal3;
    paramArrayOfBigDecimal4[0] = paramBigDecimal4;
    paramArrayOfBigDecimal5[0] = paramBigDecimal5;
  }

  public static void N0241(String paramString1, int paramInt, String paramString2, String paramString3, BigDecimal paramBigDecimal1, short paramShort, Date paramDate, Time paramTime, Timestamp paramTimestamp, long paramLong, double paramDouble1, float paramFloat, double paramDouble2, BigDecimal paramBigDecimal2, BigDecimal paramBigDecimal3, BigDecimal paramBigDecimal4, BigDecimal paramBigDecimal5)
  {
    System.out.println("IN1 value                :   " + paramString1);
  }

  public static void N0242(long[] paramArrayOfLong1, BigDecimal[] paramArrayOfBigDecimal1, int[] paramArrayOfInt1, long[] paramArrayOfLong2, String[] paramArrayOfString1, short[] paramArrayOfShort1, BigDecimal[] paramArrayOfBigDecimal2, short[] paramArrayOfShort2, BigDecimal[] paramArrayOfBigDecimal3, Time[] paramArrayOfTime1, Timestamp paramTimestamp, double[] paramArrayOfDouble1, String[] paramArrayOfString2, Timestamp[] paramArrayOfTimestamp1, BigDecimal[] paramArrayOfBigDecimal4, double[] paramArrayOfDouble2, String paramString1, int[] paramArrayOfInt2, BigDecimal[] paramArrayOfBigDecimal5, Date paramDate, String[] paramArrayOfString3, String paramString2, Date[] paramArrayOfDate1, BigDecimal[] paramArrayOfBigDecimal6, BigDecimal[] paramArrayOfBigDecimal7, Time[] paramArrayOfTime2, Date[] paramArrayOfDate2, double paramDouble1, BigDecimal paramBigDecimal1, long paramLong, BigDecimal paramBigDecimal2, float[] paramArrayOfFloat1, BigDecimal[] paramArrayOfBigDecimal8, double paramDouble2, BigDecimal paramBigDecimal3, BigDecimal[] paramArrayOfBigDecimal9, String[] paramArrayOfString4, int paramInt, String[] paramArrayOfString5, String[] paramArrayOfString6, Time paramTime, float paramFloat, double[] paramArrayOfDouble3, String paramString3, short paramShort, BigDecimal paramBigDecimal4, double[] paramArrayOfDouble4, Timestamp[] paramArrayOfTimestamp2, float[] paramArrayOfFloat2, BigDecimal[] paramArrayOfBigDecimal10, BigDecimal paramBigDecimal5)
  {
    paramArrayOfString3[0] = paramString2;
    paramArrayOfInt2[0] = paramInt;
    paramArrayOfString1[0] = paramString3;
    paramArrayOfString5[0] = paramString1;
    paramArrayOfBigDecimal6[0] = paramBigDecimal4;
    paramArrayOfShort2[0] = paramShort;
    paramArrayOfDate2[0] = paramDate;
    paramArrayOfTime1[0] = paramTime;
    paramArrayOfTimestamp1[0] = paramTimestamp;
    paramArrayOfLong1[0] = paramLong;
    paramArrayOfDouble1[0] = paramDouble2;
    paramArrayOfFloat1[0] = paramFloat;
    paramArrayOfDouble4[0] = paramDouble1;
    paramArrayOfBigDecimal5[0] = paramBigDecimal5;
    paramArrayOfBigDecimal2[0] = paramBigDecimal1;
    paramArrayOfBigDecimal10[0] = paramBigDecimal3;
    paramArrayOfBigDecimal7[0] = paramBigDecimal2;
    paramArrayOfString4[0] = paramArrayOfString3[0];
    paramArrayOfInt1[0] = paramArrayOfInt2[0];
    paramArrayOfString2[0] = paramArrayOfString1[0];
    paramArrayOfString6[0] = paramArrayOfString5[0];
    paramArrayOfBigDecimal1[0] = paramArrayOfBigDecimal6[0];
    paramArrayOfShort1[0] = paramArrayOfShort2[0];
    paramArrayOfDate1[0] = paramArrayOfDate2[0];
    paramArrayOfTime2[0] = paramArrayOfTime1[0];
    paramArrayOfTimestamp2[0] = paramArrayOfTimestamp1[0];
    paramArrayOfLong2[0] = paramArrayOfLong1[0];
    paramArrayOfDouble3[0] = paramArrayOfDouble1[0];
    paramArrayOfFloat2[0] = paramArrayOfFloat1[0];
    paramArrayOfDouble2[0] = paramArrayOfDouble4[0];
    paramArrayOfBigDecimal3[0] = paramArrayOfBigDecimal5[0];
    paramArrayOfBigDecimal8[0] = paramArrayOfBigDecimal2[0];
    paramArrayOfBigDecimal4[0] = paramArrayOfBigDecimal10[0];
    paramArrayOfBigDecimal9[0] = paramArrayOfBigDecimal7[0];
  }

  public static void N0243(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace(); } 
CallableStatement localCallableStatement = localConnection.prepareCall("{call cat.sch.N0235(?,?)}");
    localCallableStatement.setString(1, "Smith");
    localCallableStatement.registerOutParameter(2, 1);
    ResultSet localResultSet2 = localCallableStatement.executeQuery();
    ResultSet localResultSet1;
    try { localResultSet1 = localCallableStatement.executeQuery("select ename from cat.sch.emp");
    } catch (SQLException localSQLException1) {
      System.out.println("Problem reading table");
      while (localSQLException1 != null) {
        System.out.println("Message:" + localSQLException1.getMessage());
        SQLException localSQLException2 = localSQLException1.getNextException();
      }
      return;
    }

    localResultSet1.next();
    paramString = localResultSet1.getString(1);
    paramArrayOfString[0] = paramString;
    localCallableStatement.close();
  }

  public static void N0232(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace();
    }

    CallableStatement localCallableStatement = localConnection.prepareCall("{call cat.sch.N0244(?,?)}");
    localCallableStatement.setString(1, "Smith");
    localCallableStatement.registerOutParameter(2, 1);
    ResultSet localResultSet = localCallableStatement.executeQuery();
    localCallableStatement.close();
  }

  public static void N0244(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace();
    }

    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("delete from cat.sch.emp");
    localStatement.executeUpdate("insert into cat.sch.emp values('AAA Computers')");
    CallableStatement localCallableStatement = localConnection.prepareCall("{call cat.sch.N0245(?,?)}");
    localCallableStatement.setString(1, "Smith");
    localCallableStatement.registerOutParameter(2, 1);
    ResultSet localResultSet = localCallableStatement.executeQuery();
    localStatement.close();
  }

  public static void N0245(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace();
    }

    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("delete from cat.sch.emp");
    localStatement.executeUpdate("insert into cat.sch.emp values('Innovation Technology')");
    CallableStatement localCallableStatement = localConnection.prepareCall("{call cat.sch.N0246(?,?)}");
    localCallableStatement.setString(1, "Smith");
    localCallableStatement.registerOutParameter(2, 1);
    ResultSet localResultSet = localCallableStatement.executeQuery();
    localStatement.close();
  }

  public static void N0246(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace();
    }

    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("insert into cat.sch.emp values('Hewlett Packard')");
    CallableStatement localCallableStatement = localConnection.prepareCall("{call cat.sch.N0247(?,?)}");
    localCallableStatement.setString(1, "Smith");
    localCallableStatement.registerOutParameter(2, 1);
    ResultSet localResultSet = localCallableStatement.executeQuery();
    localStatement.close();
  }

  public static void N0247(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace();
    }

    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("insert into cat.sch.emp values('NonStop Division')");
    CallableStatement localCallableStatement = localConnection.prepareCall("{call cat.sch.N0248(?,?)}");
    localCallableStatement.setString(1, "Smith");
    localCallableStatement.registerOutParameter(2, 1);
    ResultSet localResultSet = localCallableStatement.executeQuery();
    localStatement.close();
  }

  public static void N0248(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace();
    }

    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("insert into cat.sch.emp values('Inspiration Technology')");
    CallableStatement localCallableStatement = localConnection.prepareCall("{call cat.sch.N0249(?,?)}");
    localCallableStatement.setString(1, "Smith");
    localCallableStatement.registerOutParameter(2, 1);
    ResultSet localResultSet = localCallableStatement.executeQuery();
  }

  public static void N0249(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace();
    }

    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("insert into cat.sch.emp values('HighEnd Server Division')");
    CallableStatement localCallableStatement = localConnection.prepareCall("{call cat.sch.N0250(?,?)}");
    localCallableStatement.setString(1, "Smith");
    localCallableStatement.registerOutParameter(2, 1);
    ResultSet localResultSet = localCallableStatement.executeQuery();
  }

  public static void N0250(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace();
    }

    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("insert into cat.sch.emp values('Java Stored procedures')");
    CallableStatement localCallableStatement = localConnection.prepareCall("{call cat.sch.N0251(?,?)}");
    localCallableStatement.setString(1, "Smith");
    localCallableStatement.registerOutParameter(2, 1);
    ResultSet localResultSet = localCallableStatement.executeQuery();
  }

  public static void N0251(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace();
    }

    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("insert into cat.sch.emp values('Business Unit')");
  }

  public static void N0300(String paramString, String[] paramArrayOfString1, String[] paramArrayOfString2)
  {
    paramArrayOfString2[0] = paramArrayOfString1[0];
    paramArrayOfString1[0] = paramString;
  }

  public static void N0301(BigDecimal paramBigDecimal, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = paramBigDecimal;
  }

  public static void N0302(int paramInt, int[] paramArrayOfInt1, int[] paramArrayOfInt2)
  {
    paramArrayOfInt2[0] = paramArrayOfInt1[0];
    paramArrayOfInt1[0] = paramInt;
  }

  public static void N0303(short paramShort, short[] paramArrayOfShort1, short[] paramArrayOfShort2)
  {
    paramArrayOfShort2[0] = paramArrayOfShort1[0];
    paramArrayOfShort1[0] = paramShort;
  }

  public static void N0304(long paramLong, long[] paramArrayOfLong1, long[] paramArrayOfLong2)
  {
    paramArrayOfLong2[0] = paramArrayOfLong1[0];
    paramArrayOfLong1[0] = paramLong;
  }

  public static void N0306(int paramInt, String[] paramArrayOfString, short[] paramArrayOfShort)
  {
    paramArrayOfString[0] = ("[" + paramArrayOfShort[0] + "]");
    paramArrayOfShort[0] = ((short)paramInt);
  }

  public static void N0309(String[] paramArrayOfString, BigDecimal paramBigDecimal, int[] paramArrayOfInt)
  {
    paramArrayOfString[0] = ("[" + paramArrayOfInt[0] + "]");
    int i = paramBigDecimal.intValue();
    paramArrayOfInt[0] = i;
  }

  public static void N0310(String[] paramArrayOfString, Time[] paramArrayOfTime, Time paramTime)
  {
    paramArrayOfString[0] = String.valueOf(paramArrayOfTime[0]);
    paramArrayOfTime[0] = paramTime;
  }

  public static void N0311(BigDecimal paramBigDecimal, BigDecimal[] paramArrayOfBigDecimal1, BigDecimal[] paramArrayOfBigDecimal2)
  {
    paramArrayOfBigDecimal2[0] = paramArrayOfBigDecimal1[0];
    paramArrayOfBigDecimal1[0] = paramBigDecimal;
  }

  public static void N0315(float paramFloat, float[] paramArrayOfFloat1, float[] paramArrayOfFloat2)
  {
    paramArrayOfFloat2[0] = paramArrayOfFloat1[0];
    paramArrayOfFloat1[0] = paramFloat;
  }

  public static void N0316(double paramDouble, double[] paramArrayOfDouble1, double[] paramArrayOfDouble2)
  {
    paramArrayOfDouble2[0] = paramArrayOfDouble1[0];
    paramArrayOfDouble1[0] = paramDouble;
  }

  public static void N0317(Date paramDate, Date[] paramArrayOfDate1, Date[] paramArrayOfDate2)
  {
    paramArrayOfDate2[0] = paramArrayOfDate1[0];
    paramArrayOfDate1[0] = paramDate;
  }

  public static void N0318(Time paramTime, Time[] paramArrayOfTime1, Time[] paramArrayOfTime2)
  {
    paramArrayOfTime2[0] = paramArrayOfTime1[0];
    paramArrayOfTime1[0] = paramTime;
  }

  public static void N0319(Timestamp paramTimestamp, Timestamp[] paramArrayOfTimestamp1, Timestamp[] paramArrayOfTimestamp2)
  {
    paramArrayOfTimestamp2[0] = paramArrayOfTimestamp1[0];
    paramArrayOfTimestamp1[0] = paramTimestamp;
  }

  public static void N0411(int[] paramArrayOfInt, BigDecimal paramBigDecimal, double[] paramArrayOfDouble, float paramFloat)
  {
    paramArrayOfInt[0] = paramBigDecimal.intValue();
    paramArrayOfDouble[0] = paramFloat;
  }

  public static void N0501(String paramString, int paramInt, String[] paramArrayOfString1, String[] paramArrayOfString2, String[] paramArrayOfString3)
  {
    paramArrayOfString1[0] = paramString;
    paramArrayOfString2[0] = ("[" + paramInt + "]");
    paramArrayOfString3[0] = (paramArrayOfString1[0] + paramArrayOfString2[0]);
  }

  public static void N0601(double paramDouble, String[] paramArrayOfString, Date paramDate, BigDecimal paramBigDecimal, Timestamp[] paramArrayOfTimestamp, short paramShort)
  {
    double d = paramDouble + paramBigDecimal.doubleValue() + paramShort;
    paramArrayOfString[0] = ("[" + paramDate.toString() + "]" + "[" + paramArrayOfTimestamp[0].toString() + "]" + d);
    paramArrayOfTimestamp[0].setNanos(paramArrayOfTimestamp[0].getNanos() * 2);
  }

  public static void N0602(String paramString, int paramInt, BigDecimal paramBigDecimal, float paramFloat, Date paramDate, String[] paramArrayOfString)
  {
    String str = new String("");
    str = str + "[" + paramString + "]";
    str = str + "[" + paramInt + "]";
    str = str + "[" + paramBigDecimal.toString() + "]";
    str = str + "[" + paramFloat + "]";
    str = str + "[" + paramDate.toString() + "]";
    paramArrayOfString[0] = str;
  }

  public static void N0603(long paramLong1, long paramLong2, long[] paramArrayOfLong, String[] paramArrayOfString1, String[] paramArrayOfString2)
  {
    paramArrayOfLong[0] = (paramLong1 * paramLong2);
    paramArrayOfString1[0] = String.valueOf(paramArrayOfLong[0]);
    paramArrayOfString2[0] = paramArrayOfString1[0];
  }

  public static void N0999(int paramInt1, double paramDouble1, int[] paramArrayOfInt1, double[] paramArrayOfDouble1, int[] paramArrayOfInt2, double[] paramArrayOfDouble2, Timestamp paramTimestamp1, Date paramDate1, Timestamp[] paramArrayOfTimestamp1, Date[] paramArrayOfDate1, Timestamp[] paramArrayOfTimestamp2, Date[] paramArrayOfDate2, String paramString1, String paramString2, String[] paramArrayOfString1, String[] paramArrayOfString2, String[] paramArrayOfString3, String[] paramArrayOfString4, BigDecimal paramBigDecimal1, long paramLong1, BigDecimal[] paramArrayOfBigDecimal1, long[] paramArrayOfLong1, BigDecimal[] paramArrayOfBigDecimal2, long[] paramArrayOfLong2, float paramFloat1, short paramShort1, float[] paramArrayOfFloat1, short[] paramArrayOfShort1, float[] paramArrayOfFloat2, short[] paramArrayOfShort2, int paramInt2, double paramDouble2, int[] paramArrayOfInt3, double[] paramArrayOfDouble3, int[] paramArrayOfInt4, double[] paramArrayOfDouble4, Timestamp paramTimestamp2, Date paramDate2, Timestamp[] paramArrayOfTimestamp3, Date[] paramArrayOfDate3, Timestamp[] paramArrayOfTimestamp4, Date[] paramArrayOfDate4, String paramString3, String paramString4, String[] paramArrayOfString5, String[] paramArrayOfString6, String[] paramArrayOfString7, String[] paramArrayOfString8, BigDecimal paramBigDecimal2, long paramLong2, BigDecimal[] paramArrayOfBigDecimal3, long[] paramArrayOfLong3, BigDecimal[] paramArrayOfBigDecimal4, long[] paramArrayOfLong4, float paramFloat2, short paramShort2, float[] paramArrayOfFloat3, short[] paramArrayOfShort3, float[] paramArrayOfFloat4, short[] paramArrayOfShort4, int paramInt3, double paramDouble3, int[] paramArrayOfInt5, double[] paramArrayOfDouble5, int[] paramArrayOfInt6, double[] paramArrayOfDouble6, Timestamp paramTimestamp3, Date paramDate3, Timestamp[] paramArrayOfTimestamp5, Date[] paramArrayOfDate5, Timestamp[] paramArrayOfTimestamp6, Date[] paramArrayOfDate6, String paramString5, String paramString6, String[] paramArrayOfString9, String[] paramArrayOfString10, String[] paramArrayOfString11, String[] paramArrayOfString12, BigDecimal paramBigDecimal3, long paramLong3, BigDecimal[] paramArrayOfBigDecimal5, long[] paramArrayOfLong5, BigDecimal[] paramArrayOfBigDecimal6, long[] paramArrayOfLong6, float paramFloat3, short paramShort3, float[] paramArrayOfFloat5, short[] paramArrayOfShort5, float[] paramArrayOfFloat6, short[] paramArrayOfShort6, int paramInt4, double paramDouble4, int[] paramArrayOfInt7, double[] paramArrayOfDouble7, int[] paramArrayOfInt8, double[] paramArrayOfDouble8, Timestamp paramTimestamp4, Date paramDate4, Timestamp[] paramArrayOfTimestamp7, Date[] paramArrayOfDate7, Timestamp[] paramArrayOfTimestamp8, Date[] paramArrayOfDate8, String paramString7, String paramString8, String[] paramArrayOfString13, String[] paramArrayOfString14, String[] paramArrayOfString15, String[] paramArrayOfString16, BigDecimal paramBigDecimal4, long paramLong4, BigDecimal[] paramArrayOfBigDecimal7, long[] paramArrayOfLong7, BigDecimal[] paramArrayOfBigDecimal8, long[] paramArrayOfLong8, float paramFloat4, short paramShort4, float[] paramArrayOfFloat7, short[] paramArrayOfShort7, float[] paramArrayOfFloat8, short[] paramArrayOfShort8)
  {
    paramArrayOfInt1[0] = paramArrayOfInt2[0];
    paramArrayOfInt2[0] = paramInt1;

    paramArrayOfDouble1[0] = paramArrayOfDouble2[0];
    paramArrayOfDouble2[0] = paramDouble1;

    paramArrayOfTimestamp1[0] = paramArrayOfTimestamp2[0];
    paramArrayOfTimestamp2[0] = paramTimestamp1;

    paramArrayOfDate1[0] = paramArrayOfDate2[0];
    paramArrayOfDate2[0] = paramDate1;

    paramArrayOfString1[0] = paramArrayOfString3[0];
    paramArrayOfString3[0] = paramString1;

    paramArrayOfString2[0] = paramArrayOfString4[0];
    paramArrayOfString4[0] = paramString2;

    paramArrayOfBigDecimal1[0] = paramArrayOfBigDecimal2[0];
    paramArrayOfBigDecimal2[0] = paramBigDecimal1;

    paramArrayOfLong1[0] = paramArrayOfLong2[0];
    paramArrayOfLong2[0] = paramLong1;

    paramArrayOfFloat1[0] = paramArrayOfFloat2[0];
    paramArrayOfFloat2[0] = paramFloat1;

    paramArrayOfShort1[0] = paramArrayOfShort2[0];
    paramArrayOfShort2[0] = paramShort1;

    paramArrayOfInt3[0] = paramArrayOfInt4[0];
    paramArrayOfInt4[0] = paramInt2;

    paramArrayOfDouble3[0] = paramArrayOfDouble4[0];
    paramArrayOfDouble4[0] = paramDouble2;

    paramArrayOfTimestamp3[0] = paramArrayOfTimestamp4[0];
    paramArrayOfTimestamp4[0] = paramTimestamp2;

    paramArrayOfDate3[0] = paramArrayOfDate4[0];
    paramArrayOfDate4[0] = paramDate2;

    paramArrayOfString5[0] = paramArrayOfString7[0];
    paramArrayOfString7[0] = paramString3;

    paramArrayOfString6[0] = paramArrayOfString8[0];
    paramArrayOfString8[0] = paramString4;

    paramArrayOfBigDecimal3[0] = paramArrayOfBigDecimal4[0];
    paramArrayOfBigDecimal4[0] = paramBigDecimal2;

    paramArrayOfLong3[0] = paramArrayOfLong4[0];
    paramArrayOfLong4[0] = paramLong2;

    paramArrayOfFloat3[0] = paramArrayOfFloat4[0];
    paramArrayOfFloat4[0] = paramFloat2;

    paramArrayOfShort3[0] = paramArrayOfShort4[0];
    paramArrayOfShort4[0] = paramShort2;

    paramArrayOfInt5[0] = paramArrayOfInt6[0];
    paramArrayOfInt6[0] = paramInt3;

    paramArrayOfDouble5[0] = paramArrayOfDouble6[0];
    paramArrayOfDouble6[0] = paramDouble3;

    paramArrayOfTimestamp5[0] = paramArrayOfTimestamp6[0];
    paramArrayOfTimestamp6[0] = paramTimestamp3;

    paramArrayOfDate5[0] = paramArrayOfDate6[0];
    paramArrayOfDate6[0] = paramDate3;

    paramArrayOfString9[0] = paramArrayOfString11[0];
    paramArrayOfString11[0] = paramString5;

    paramArrayOfString10[0] = paramArrayOfString12[0];
    paramArrayOfString12[0] = paramString6;

    paramArrayOfBigDecimal5[0] = paramArrayOfBigDecimal6[0];
    paramArrayOfBigDecimal6[0] = paramBigDecimal3;

    paramArrayOfLong5[0] = paramArrayOfLong6[0];
    paramArrayOfLong6[0] = paramLong3;

    paramArrayOfFloat5[0] = paramArrayOfFloat6[0];
    paramArrayOfFloat6[0] = paramFloat3;

    paramArrayOfShort5[0] = paramArrayOfShort6[0];
    paramArrayOfShort6[0] = paramShort3;

    paramArrayOfInt7[0] = paramArrayOfInt8[0];
    paramArrayOfInt8[0] = paramInt4;

    paramArrayOfDouble7[0] = paramArrayOfDouble8[0];
    paramArrayOfDouble8[0] = paramDouble4;

    paramArrayOfTimestamp7[0] = paramArrayOfTimestamp8[0];
    paramArrayOfTimestamp8[0] = paramTimestamp4;

    paramArrayOfDate7[0] = paramArrayOfDate8[0];
    paramArrayOfDate8[0] = paramDate4;

    paramArrayOfString13[0] = paramArrayOfString15[0];
    paramArrayOfString15[0] = paramString7;

    paramArrayOfString14[0] = paramArrayOfString16[0];
    paramArrayOfString16[0] = paramString8;

    paramArrayOfBigDecimal7[0] = paramArrayOfBigDecimal8[0];
    paramArrayOfBigDecimal8[0] = paramBigDecimal4;

    paramArrayOfLong7[0] = paramArrayOfLong8[0];
    paramArrayOfLong8[0] = paramLong4;

    paramArrayOfFloat7[0] = paramArrayOfFloat8[0];
    paramArrayOfFloat8[0] = paramFloat4;

    paramArrayOfShort7[0] = paramArrayOfShort8[0];
    paramArrayOfShort8[0] = paramShort4;
  }

  public static void N1200(Integer paramInteger, float[] paramArrayOfFloat)
  {
    if (paramInteger == null)
      paramArrayOfFloat[0] = 1.03E+010F;
    else
      paramArrayOfFloat[0] = paramInteger.floatValue();
  }

  public static void N1201(Float paramFloat, String[] paramArrayOfString)
  {
    if (paramFloat == null)
      paramArrayOfString[0] = "null";
    else
      paramArrayOfString[0] = paramFloat.toString();
  }

  public static void N1202(Double paramDouble, int[] paramArrayOfInt)
  {
    if (paramDouble == null)
      paramArrayOfInt[0] = 0;
    else
      paramArrayOfInt[0] = paramDouble.intValue();
  }

  public static void N1203(Long paramLong, Long[] paramArrayOfLong)
  {
    if (paramLong == null)
      paramArrayOfLong[0] = null;
    else
      paramArrayOfLong[0] = paramLong;
  }

  public static void N1204(Integer paramInteger, Double[] paramArrayOfDouble)
  {
    if (paramInteger == null)
      paramArrayOfDouble[0] = null;
    else
      paramArrayOfDouble[0] = new Double(paramInteger.doubleValue());
  }

  public static void N1205(String paramString, Float[] paramArrayOfFloat)
  {
    if (paramString == null)
      paramArrayOfFloat[0] = null;
    else
      paramArrayOfFloat[0] = new Float(paramString);
  }

  public static void N1206(String paramString, Integer[] paramArrayOfInteger)
  {
    paramArrayOfInteger[0] = new Integer(paramString);
  }

  public static void N1207(String paramString, Long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = new Long(paramString);
  }

  public static void N1208(Double paramDouble, Double[] paramArrayOfDouble)
  {
    if (paramDouble != null) {
      double d = paramDouble.doubleValue();
      paramArrayOfDouble[0] = new Double(d);
    }
    else {
      paramArrayOfDouble[0] = null;
    }
  }

  public static void N1300(Integer paramInteger, Integer[] paramArrayOfInteger, long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = paramArrayOfInteger[0].longValue();
    paramArrayOfInteger[0] = paramInteger;
  }

  public static long N1300a(Integer paramInteger, Integer[] paramArrayOfInteger, long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = paramArrayOfInteger[0].longValue();
    paramArrayOfInteger[0] = paramInteger;
    long l = paramArrayOfInteger[0].longValue();
    return l;
  }

  public static void N1300b(Integer paramInteger, Integer[] paramArrayOfInteger, long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = paramArrayOfInteger[0].longValue();
    paramArrayOfInteger[0] = paramInteger;
  }

  public static void N1300b(Long paramLong, Long[] paramArrayOfLong, long[] paramArrayOfLong1)
  {
    paramArrayOfLong1[0] = paramArrayOfLong[0].longValue();
    paramArrayOfLong[0] = paramLong;
  }

  public static void N1301(Float paramFloat, Float[] paramArrayOfFloat, long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = paramArrayOfFloat[0].longValue();
    paramArrayOfFloat[0] = paramFloat;
  }

  public static void N1302(Double paramDouble, Double[] paramArrayOfDouble, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = paramArrayOfDouble[0].shortValue();
    paramArrayOfDouble[0] = paramDouble;
  }

  public static void N1303(Long paramLong, Long[] paramArrayOfLong, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = paramArrayOfLong[0].intValue();
    paramArrayOfLong[0] = paramLong;
  }

  public static void N1400(Double paramDouble, String paramString, Double[] paramArrayOfDouble, long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = paramDouble.longValue();
    paramArrayOfDouble[0] = new Double(paramString);
  }

  public static void N1401(Float paramFloat, String paramString, Float[] paramArrayOfFloat, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = paramFloat.intValue();
    paramArrayOfFloat[0] = new Float(paramString);
  }

  public static void N1402(Float paramFloat, int paramInt, Integer[] paramArrayOfInteger, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = paramFloat.intValue();
    paramArrayOfInteger[0] = new Integer(paramInt);
  }

  public static void N1403(int paramInt, long paramLong, Long[] paramArrayOfLong, float[] paramArrayOfFloat)
  {
    paramArrayOfFloat[0] = paramInt;
    paramArrayOfLong[0] = new Long(paramLong);
  }

  public static void R0300(String paramString, int[] paramArrayOfInt, String[] paramArrayOfString)
  {
    try
    {
      BufferedReader localBufferedReader = new BufferedReader(new FileReader(paramString));
      String str = localBufferedReader.readLine();
      Integer localInteger = new Integer(str);
      paramArrayOfInt[0] = localInteger.intValue();
      paramArrayOfString[0] = "OK";
    }
    catch (Exception localException)
    {
      paramArrayOfString[0] = ("ERROR: " + localException.toString());
    }
  }

  public static void W0300(String paramString, int paramInt, String[] paramArrayOfString)
  {
    try
    {
      FileOutputStream localFileOutputStream = new FileOutputStream(paramString);
      PrintWriter localPrintWriter = new PrintWriter(localFileOutputStream);
      localPrintWriter.println(paramInt);
      localPrintWriter.close();
      localFileOutputStream.close();
      paramArrayOfString[0] = "OK";
    }
    catch (Exception localException)
    {
      paramArrayOfString[0] = ("ERROR: " + localException.toString());
    }
  }

  public static void N5201(Date[] paramArrayOfDate1, Date[] paramArrayOfDate2)
  {
    paramArrayOfDate1[0] = null;
    paramArrayOfDate2[0] = null;
  }

  public static void N5401(Float[] paramArrayOfFloat1, Float[] paramArrayOfFloat2, Double[] paramArrayOfDouble1, Double[] paramArrayOfDouble2)
  {
    paramArrayOfFloat1[0] = null;
    paramArrayOfFloat2[0] = null;
    paramArrayOfDouble1[0] = null;
    paramArrayOfDouble2[0] = null;
  }

  public static void N5402(Integer[] paramArrayOfInteger1, Integer[] paramArrayOfInteger2, Long[] paramArrayOfLong1, Long[] paramArrayOfLong2)
  {
    paramArrayOfInteger1[0] = null;
    paramArrayOfInteger2[0] = null;
    paramArrayOfLong1[0] = null;
    paramArrayOfLong2[0] = null;
  }

  public static void N5403(BigDecimal[] paramArrayOfBigDecimal1, BigDecimal[] paramArrayOfBigDecimal2, String[] paramArrayOfString1, String[] paramArrayOfString2)
  {
    paramArrayOfBigDecimal1[0] = null;
    paramArrayOfBigDecimal2[0] = null;
    paramArrayOfString1[0] = null;
    paramArrayOfString2[0] = null;
  }

  public static void N5404(Time[] paramArrayOfTime1, Time[] paramArrayOfTime2, Timestamp[] paramArrayOfTimestamp1, Timestamp[] paramArrayOfTimestamp2)
  {
    paramArrayOfTime1[0] = null;
    paramArrayOfTime2[0] = null;
    paramArrayOfTimestamp1[0] = null;
    paramArrayOfTimestamp2[0] = null;
  }

  public static void N5406(Date paramDate, Date[] paramArrayOfDate, String[] paramArrayOfString1, String[] paramArrayOfString2)
  {
    if (paramDate == null)
      paramArrayOfString1[0] = "NULL";
    else {
      paramArrayOfString1[0] = paramDate.toString();
    }
    if (paramArrayOfDate[0] == null) {
      paramArrayOfString2[0] = "NULL";
      paramArrayOfDate[0] = NULLDATEVALUE;
    }
    else {
      paramArrayOfString2[0] = paramArrayOfDate[0].toString();
    }
  }

  public static void N5801(Timestamp paramTimestamp, Timestamp[] paramArrayOfTimestamp, Time paramTime, Time[] paramArrayOfTime, String[] paramArrayOfString1, String[] paramArrayOfString2, String[] paramArrayOfString3, String[] paramArrayOfString4)
  {
    if (paramTimestamp == null)
      paramArrayOfString1[0] = "NULL";
    else {
      paramArrayOfString1[0] = paramTimestamp.toString();
    }
    if (paramArrayOfTimestamp[0] == null) {
      paramArrayOfString2[0] = "NULL";
      paramArrayOfTimestamp[0] = NULLTIMESTAMPVALUE;
    }
    else {
      paramArrayOfString2[0] = paramArrayOfTimestamp[0].toString();
    }
    if (paramTime == null)
      paramArrayOfString3[0] = "NULL";
    else {
      paramArrayOfString3[0] = paramTime.toString();
    }
    if (paramArrayOfTime[0] == null) {
      paramArrayOfString4[0] = "NULL";
      paramArrayOfTime[0] = NULLTIMEVALUE;
    }
    else {
      paramArrayOfString4[0] = paramArrayOfTime[0].toString();
    }
  }

  public static void N5802(Integer paramInteger, Integer[] paramArrayOfInteger, Long paramLong, Long[] paramArrayOfLong, String[] paramArrayOfString1, String[] paramArrayOfString2, String[] paramArrayOfString3, String[] paramArrayOfString4)
  {
    if (paramInteger == null)
      paramArrayOfString1[0] = "NULL";
    else {
      paramArrayOfString1[0] = paramInteger.toString();
    }
    if (paramArrayOfInteger[0] == null) {
      paramArrayOfString2[0] = "NULL";
      paramArrayOfInteger[0] = Integer.valueOf(INULLVALUE);
    }
    else {
      paramArrayOfString2[0] = paramArrayOfInteger[0].toString();
    }
    if (paramLong == null)
      paramArrayOfString3[0] = "NULL";
    else {
      paramArrayOfString3[0] = paramLong.toString();
    }
    if (paramArrayOfLong[0] == null) {
      paramArrayOfString4[0] = "NULL";
      paramArrayOfLong[0] = Long.valueOf(INULLVALUE);
    }
    else {
      paramArrayOfString4[0] = paramArrayOfLong[0].toString();
    }
  }

  public static void N5803(Float paramFloat, Float[] paramArrayOfFloat, Double paramDouble, Double[] paramArrayOfDouble, String[] paramArrayOfString1, String[] paramArrayOfString2, String[] paramArrayOfString3, String[] paramArrayOfString4)
  {
    if (paramFloat == null)
      paramArrayOfString1[0] = "NULL";
    else {
      paramArrayOfString1[0] = paramFloat.toString();
    }
    if (paramArrayOfFloat[0] == null) {
      paramArrayOfString2[0] = "NULL";
      paramArrayOfFloat[0] = Float.valueOf(NULLVALUE);
    }
    else {
      paramArrayOfString2[0] = paramArrayOfFloat[0].toString();
    }
    if (paramDouble == null)
      paramArrayOfString3[0] = "NULL";
    else {
      paramArrayOfString3[0] = paramDouble.toString();
    }
    if (paramArrayOfDouble[0] == null) {
      paramArrayOfString4[0] = "NULL";
      paramArrayOfDouble[0] = Double.valueOf(NULLVALUE);
    }
    else {
      paramArrayOfString4[0] = paramArrayOfDouble[0].toString();
    }
  }

  public static void N5804(String paramString, String[] paramArrayOfString1, BigDecimal paramBigDecimal, BigDecimal[] paramArrayOfBigDecimal, String[] paramArrayOfString2, String[] paramArrayOfString3, String[] paramArrayOfString4, String[] paramArrayOfString5)
  {
    if (paramString == null)
      paramArrayOfString2[0] = "NULL";
    else {
      paramArrayOfString2[0] = paramString;
    }
    if (paramArrayOfString1[0] == null) {
      paramArrayOfString3[0] = "NULL";
      paramArrayOfString1[0] = "NULL";
    }
    else {
      paramArrayOfString3[0] = paramArrayOfString1[0].toString();
    }
    if (paramBigDecimal == null)
      paramArrayOfString4[0] = "NULL";
    else {
      paramArrayOfString4[0] = paramBigDecimal.toString();
    }
    if (paramArrayOfBigDecimal[0] == null) {
      paramArrayOfString5[0] = "NULL";
      paramArrayOfBigDecimal[0] = new BigDecimal(NULLVALUE);
    }
    else {
      paramArrayOfString5[0] = paramArrayOfBigDecimal[0].toString();
    }
  }
}
