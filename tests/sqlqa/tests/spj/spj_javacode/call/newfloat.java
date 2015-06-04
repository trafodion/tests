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
import java.sql.Date;
import java.sql.DriverManager;
import java.sql.Statement;
import java.sql.Time;
import java.sql.Timestamp;

public class newfloat
{
  public static void N1100(double paramDouble, BigDecimal[] paramArrayOfBigDecimal1, BigDecimal[] paramArrayOfBigDecimal2)
  {
    paramArrayOfBigDecimal2[0] = paramArrayOfBigDecimal1[0];
    paramArrayOfBigDecimal1[0] = new BigDecimal(paramDouble);
  }

  public static void N1104(double paramDouble, short[] paramArrayOfShort1, short[] paramArrayOfShort2)
  {
    paramArrayOfShort2[0] = paramArrayOfShort1[0];
    paramArrayOfShort1[0] = ((short)(int)paramDouble);
  }

  public static void N1105(double paramDouble, float[] paramArrayOfFloat1, float[] paramArrayOfFloat2)
  {
    paramArrayOfFloat2[0] = paramArrayOfFloat1[0];
    paramArrayOfFloat1[0] = ((float)paramDouble);
  }

  public static void N1106(double paramDouble, long[] paramArrayOfLong1, long[] paramArrayOfLong2)
  {
    paramArrayOfLong2[0] = paramArrayOfLong1[0];
    paramArrayOfLong1[0] = ((long)paramDouble);
  }

  public static void N1107(double paramDouble, int[] paramArrayOfInt1, int[] paramArrayOfInt2)
  {
    paramArrayOfInt2[0] = paramArrayOfInt1[0];
    paramArrayOfInt1[0] = ((int)paramDouble);
  }

  public static void N1108(double paramDouble, String[] paramArrayOfString1, String[] paramArrayOfString2)
  {
    paramArrayOfString2[0] = paramArrayOfString1[0];
    paramArrayOfString1[0] = String.valueOf(paramDouble);
  }

  public static void N1109(double paramDouble, BigDecimal[] paramArrayOfBigDecimal, double[] paramArrayOfDouble)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramArrayOfDouble[0]);
    paramArrayOfDouble[0] = paramDouble;
  }

  public static void N1113(double paramDouble, short[] paramArrayOfShort, double[] paramArrayOfDouble)
  {
    paramArrayOfShort[0] = ((short)(int)paramArrayOfDouble[0]);
    paramArrayOfDouble[0] = paramDouble;
  }

  public static void N1114(double paramDouble, double[] paramArrayOfDouble1, double[] paramArrayOfDouble2)
  {
    paramArrayOfDouble1[0] = paramArrayOfDouble2[0];
    paramArrayOfDouble2[0] = paramDouble;
  }

  public static void N1115(double paramDouble, long[] paramArrayOfLong, double[] paramArrayOfDouble)
  {
    paramArrayOfLong[0] = ((long)paramArrayOfDouble[0]);
    paramArrayOfDouble[0] = paramDouble;
  }

  public static void N1116(double paramDouble, int[] paramArrayOfInt, double[] paramArrayOfDouble)
  {
    paramArrayOfInt[0] = ((int)paramArrayOfDouble[0]);
    paramArrayOfDouble[0] = paramDouble;
  }

  public static void N1117(double paramDouble, String[] paramArrayOfString, double[] paramArrayOfDouble)
  {
    paramArrayOfString[0] = String.valueOf(paramArrayOfDouble[0]);
    paramArrayOfDouble[0] = paramDouble;
  }

  public static void N1118(double paramDouble, BigDecimal[] paramArrayOfBigDecimal, double[] paramArrayOfDouble)
  {
    double d = paramArrayOfBigDecimal[0].doubleValue();
    paramArrayOfDouble[0] = d;
    paramArrayOfBigDecimal[0] = new BigDecimal(paramDouble);
  }

  public static void N1122(double paramDouble, short[] paramArrayOfShort, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramArrayOfShort[0];
    paramArrayOfShort[0] = ((short)(int)paramDouble);
  }

  public static void N1123(double paramDouble, float[] paramArrayOfFloat, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramArrayOfFloat[0];
    paramArrayOfFloat[0] = ((float)paramDouble);
  }

  public static void N1124(double paramDouble, long[] paramArrayOfLong, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramArrayOfLong[0];
    paramArrayOfLong[0] = ((long)paramDouble);
  }

  public static void N1125(double paramDouble, int[] paramArrayOfInt, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramArrayOfInt[0];
    paramArrayOfInt[0] = ((int)paramDouble);
  }

  public static void N1126(double paramDouble, String[] paramArrayOfString, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = Double.valueOf(paramArrayOfString[0]).doubleValue();
    paramArrayOfString[0] = String.valueOf(paramDouble);
  }

  public static void N1127(String paramString, BigDecimal[] paramArrayOfBigDecimal1, BigDecimal[] paramArrayOfBigDecimal2)
  {
    paramArrayOfBigDecimal2[0] = paramArrayOfBigDecimal1[0];
    paramArrayOfBigDecimal1[0] = new BigDecimal(paramString);
  }

  public static void N1131(String paramString, short[] paramArrayOfShort1, short[] paramArrayOfShort2)
  {
    paramArrayOfShort2[0] = paramArrayOfShort1[0];
    paramArrayOfShort1[0] = Short.valueOf(paramString).shortValue();
  }

  public static void N1132(String paramString, float[] paramArrayOfFloat1, float[] paramArrayOfFloat2)
  {
    paramArrayOfFloat2[0] = paramArrayOfFloat1[0];
    paramArrayOfFloat1[0] = Float.valueOf(paramString).floatValue();
  }

  public static void N1133(String paramString, long[] paramArrayOfLong1, long[] paramArrayOfLong2)
  {
    paramArrayOfLong2[0] = paramArrayOfLong1[0];
    paramArrayOfLong1[0] = Long.valueOf(paramString).longValue();
  }

  public static void N1134(String paramString, int[] paramArrayOfInt1, int[] paramArrayOfInt2)
  {
    paramArrayOfInt2[0] = paramArrayOfInt1[0];
    paramArrayOfInt1[0] = Integer.valueOf(paramString).intValue();
  }

  public static void N1135(String paramString, double[] paramArrayOfDouble1, double[] paramArrayOfDouble2)
  {
    paramArrayOfDouble2[0] = paramArrayOfDouble1[0];
    paramArrayOfDouble1[0] = Double.valueOf(paramString).doubleValue();
  }

  public static void N1137(String paramString, Date[] paramArrayOfDate1, Date[] paramArrayOfDate2)
  {
    paramArrayOfDate2[0] = paramArrayOfDate1[0];
    paramArrayOfDate1[0] = Date.valueOf(paramString.toString());
  }

  public static void N1138(String paramString, Time[] paramArrayOfTime1, Time[] paramArrayOfTime2)
  {
    paramArrayOfTime2[0] = paramArrayOfTime1[0];
    paramArrayOfTime1[0] = Time.valueOf(paramString.toString());
  }

  public static void N1139(String paramString, Timestamp[] paramArrayOfTimestamp1, Timestamp[] paramArrayOfTimestamp2)
  {
    paramArrayOfTimestamp2[0] = paramArrayOfTimestamp1[0];
    paramArrayOfTimestamp1[0] = Timestamp.valueOf(paramString.toString());
  }

  public static void N1140(String paramString, BigDecimal[] paramArrayOfBigDecimal, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramArrayOfBigDecimal[0]);
    paramArrayOfBigDecimal[0] = new BigDecimal(paramString);
  }

  public static void N1144(String paramString, short[] paramArrayOfShort, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramArrayOfShort[0]);
    paramArrayOfShort[0] = Short.valueOf(paramString).shortValue();
  }

  public static void N1145(String paramString, float[] paramArrayOfFloat, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramArrayOfFloat[0]);
    paramArrayOfFloat[0] = Float.valueOf(paramString).floatValue();
  }

  public static void N1146(String paramString, long[] paramArrayOfLong, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramArrayOfLong[0]);
    paramArrayOfLong[0] = Long.valueOf(paramString).longValue();
  }

  public static void N1147(String paramString, int[] paramArrayOfInt, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramArrayOfInt[0]);
    paramArrayOfInt[0] = Integer.valueOf(paramString).intValue();
  }

  public static void N1148(String paramString, double[] paramArrayOfDouble, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramArrayOfDouble[0]);
    paramArrayOfDouble[0] = Double.valueOf(paramString).doubleValue();
  }

  public static void N1150(String paramString, Date[] paramArrayOfDate, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramArrayOfDate[0]);
    paramArrayOfDate[0] = Date.valueOf(paramString.toString());
  }

  public static void N1151(String paramString, Time[] paramArrayOfTime, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramArrayOfTime[0]);
    paramArrayOfTime[0] = Time.valueOf(paramString.toString());
  }

  public static void N1152(String paramString, Timestamp[] paramArrayOfTimestamp, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramArrayOfTimestamp[0]);
    paramArrayOfTimestamp[0] = Timestamp.valueOf(paramString.toString());
  }

  public static void N1153(String paramString, BigDecimal[] paramArrayOfBigDecimal, String[] paramArrayOfString)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramArrayOfString[0]);
    paramArrayOfString[0] = paramString;
  }

  public static void N1157(String paramString, short[] paramArrayOfShort, String[] paramArrayOfString)
  {
    paramArrayOfShort[0] = Short.valueOf(paramArrayOfString[0]).shortValue();
    paramArrayOfString[0] = paramString;
  }

  public static void N1158(String paramString, float[] paramArrayOfFloat, String[] paramArrayOfString)
  {
    paramArrayOfFloat[0] = Float.valueOf(paramArrayOfString[0]).floatValue();
    paramArrayOfString[0] = paramString;
  }

  public static void N1159(String paramString, long[] paramArrayOfLong, String[] paramArrayOfString)
  {
    paramArrayOfLong[0] = Long.valueOf(paramArrayOfString[0]).longValue();
    paramArrayOfString[0] = paramString;
  }

  public static void N1160(String paramString, int[] paramArrayOfInt, String[] paramArrayOfString)
  {
    paramArrayOfInt[0] = Integer.valueOf(paramArrayOfString[0]).intValue();
    paramArrayOfString[0] = paramString;
  }

  public static void N1161(String paramString, double[] paramArrayOfDouble, String[] paramArrayOfString)
  {
    paramArrayOfDouble[0] = Double.valueOf(paramArrayOfString[0]).doubleValue();
    paramArrayOfString[0] = paramString;
  }

  public static void N1163(String paramString, Date[] paramArrayOfDate, String[] paramArrayOfString)
  {
    paramArrayOfDate[0] = Date.valueOf(paramArrayOfString[0].toString());
    paramArrayOfString[0] = paramString;
  }

  public static void N1164(String paramString, Time[] paramArrayOfTime, String[] paramArrayOfString)
  {
    paramArrayOfTime[0] = Time.valueOf(paramArrayOfString[0].toString());
    paramArrayOfString[0] = paramString;
  }

  public static void N1165(String paramString, Timestamp[] paramArrayOfTimestamp, String[] paramArrayOfString)
  {
    paramArrayOfTimestamp[0] = Timestamp.valueOf(paramArrayOfString[0].toString());
    paramArrayOfString[0] = paramString;
  }

  public static void N1166(long paramLong, BigDecimal[] paramArrayOfBigDecimal1, BigDecimal[] paramArrayOfBigDecimal2)
  {
    paramArrayOfBigDecimal2[0] = paramArrayOfBigDecimal1[0];
    paramArrayOfBigDecimal1[0] = new BigDecimal(paramLong);
  }

  public static void N1170(long paramLong, short[] paramArrayOfShort1, short[] paramArrayOfShort2)
  {
    paramArrayOfShort2[0] = paramArrayOfShort1[0];
    paramArrayOfShort1[0] = ((short)(int)paramLong);
  }

  public static void N1171(long paramLong, float[] paramArrayOfFloat1, float[] paramArrayOfFloat2)
  {
    paramArrayOfFloat2[0] = paramArrayOfFloat1[0];
    paramArrayOfFloat1[0] = ((float)paramLong);
  }

  public static void N1172(long paramLong, int[] paramArrayOfInt1, int[] paramArrayOfInt2)
  {
    paramArrayOfInt2[0] = paramArrayOfInt1[0];
    paramArrayOfInt1[0] = ((int)paramLong);
  }

  public static void N1173(long paramLong, String[] paramArrayOfString1, String[] paramArrayOfString2)
  {
    paramArrayOfString2[0] = paramArrayOfString1[0];
    paramArrayOfString1[0] = String.valueOf(paramLong);
  }

  public static void N1174(long paramLong, double[] paramArrayOfDouble1, double[] paramArrayOfDouble2)
  {
    paramArrayOfDouble2[0] = paramArrayOfDouble1[0];
    paramArrayOfDouble1[0] = paramLong;
  }

  public static void N1176(long paramLong, BigDecimal[] paramArrayOfBigDecimal, long[] paramArrayOfLong)
  {
    long l = paramArrayOfBigDecimal[0].longValue();
    paramArrayOfLong[0] = l;
    paramArrayOfBigDecimal[0] = new BigDecimal(paramLong);
  }

  public static void N1180(long paramLong, short[] paramArrayOfShort, long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = paramArrayOfShort[0];
    paramArrayOfShort[0] = ((short)(int)paramLong);
  }

  public static void N1181(long paramLong, float[] paramArrayOfFloat, long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = ((long)paramArrayOfFloat[0]);
    paramArrayOfFloat[0] = ((float)paramLong);
  }

  public static void N1183(long paramLong, int[] paramArrayOfInt, long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = paramArrayOfInt[0];
    paramArrayOfInt[0] = ((int)paramLong);
  }

  public static void N1184(long paramLong, String[] paramArrayOfString, long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = Long.valueOf(paramArrayOfString[0]).longValue();
    paramArrayOfString[0] = String.valueOf(paramLong);
  }

  public static void N1185(long paramLong, double[] paramArrayOfDouble, long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = ((long)paramArrayOfDouble[0]);
    paramArrayOfDouble[0] = paramLong;
  }

  public static void N1187(long paramLong, BigDecimal[] paramArrayOfBigDecimal, long[] paramArrayOfLong)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramArrayOfLong[0]);
    paramArrayOfLong[0] = paramLong;
  }

  public static void N1191(long paramLong, short[] paramArrayOfShort, long[] paramArrayOfLong)
  {
    paramArrayOfShort[0] = ((short)(int)paramArrayOfLong[0]);
    paramArrayOfLong[0] = paramLong;
  }

  public static void N1192(long paramLong, double[] paramArrayOfDouble, long[] paramArrayOfLong)
  {
    paramArrayOfDouble[0] = paramArrayOfLong[0];
    paramArrayOfLong[0] = paramLong;
  }

  public static void N1193(long paramLong, int[] paramArrayOfInt, long[] paramArrayOfLong)
  {
    paramArrayOfInt[0] = ((int)paramArrayOfLong[0]);
    paramArrayOfLong[0] = paramLong;
  }

  public static void N1194(long paramLong, String[] paramArrayOfString, long[] paramArrayOfLong)
  {
    paramArrayOfString[0] = String.valueOf(paramArrayOfLong[0]);
    paramArrayOfLong[0] = paramLong;
  }

  public static void N1195(long paramLong, double[] paramArrayOfDouble, long[] paramArrayOfLong)
  {
    paramArrayOfDouble[0] = paramArrayOfLong[0];
    paramArrayOfLong[0] = paramLong;
  }

  public static void N1196(long paramLong, double[] paramArrayOfDouble, long[] paramArrayOfLong)
  {
    paramArrayOfDouble[0] = paramArrayOfLong[0];
    paramArrayOfLong[0] = paramLong;
  }

  public static void N1197(float paramFloat, BigDecimal[] paramArrayOfBigDecimal1, BigDecimal[] paramArrayOfBigDecimal2)
  {
    paramArrayOfBigDecimal2[0] = paramArrayOfBigDecimal1[0];
    paramArrayOfBigDecimal1[0] = new BigDecimal(paramFloat);
  }

  public static void N1201(float paramFloat, short[] paramArrayOfShort1, short[] paramArrayOfShort2)
  {
    paramArrayOfShort2[0] = paramArrayOfShort1[0];
    paramArrayOfShort1[0] = ((short)(int)paramFloat);
  }

  public static void N1202(float[] paramArrayOfFloat1, float[] paramArrayOfFloat2, float paramFloat)
  {
    paramArrayOfFloat2[0] = paramArrayOfFloat1[0];
    paramArrayOfFloat1[0] = paramFloat;
  }

  public static void N1203(float paramFloat, long[] paramArrayOfLong1, long[] paramArrayOfLong2)
  {
    paramArrayOfLong2[0] = paramArrayOfLong1[0];
    paramArrayOfLong1[0] = ((long)paramFloat);
  }

  public static void N1204(float paramFloat, int[] paramArrayOfInt1, int[] paramArrayOfInt2)
  {
    paramArrayOfInt2[0] = paramArrayOfInt1[0];
    paramArrayOfInt1[0] = ((int)paramFloat);
  }

  public static void N1205(float paramFloat, double[] paramArrayOfDouble1, double[] paramArrayOfDouble2)
  {
    paramArrayOfDouble2[0] = paramArrayOfDouble1[0];
    paramArrayOfDouble1[0] = paramFloat;
  }

  public static void N1207(double paramDouble, BigDecimal[] paramArrayOfBigDecimal, double[] paramArrayOfDouble)
  {
    double d = paramArrayOfBigDecimal[0].doubleValue();
    paramArrayOfDouble[0] = d;
    paramArrayOfBigDecimal[0] = new BigDecimal(paramDouble);
  }

  public static void N1211(double paramDouble, short[] paramArrayOfShort, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramArrayOfShort[0];
    paramArrayOfShort[0] = ((short)(int)paramDouble);
  }

  public static void N1212(double[] paramArrayOfDouble1, double[] paramArrayOfDouble2, double paramDouble)
  {
    paramArrayOfDouble2[0] = paramArrayOfDouble1[0];
    paramArrayOfDouble1[0] = paramDouble;
  }

  public static void N1213(double paramDouble, long[] paramArrayOfLong, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramArrayOfLong[0];
    paramArrayOfLong[0] = ((long)paramDouble);
  }

  public static void N1214(double paramDouble, int[] paramArrayOfInt, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramArrayOfInt[0];
    paramArrayOfInt[0] = ((int)paramDouble);
  }

  public static void N1215(double paramDouble, double[] paramArrayOfDouble1, double[] paramArrayOfDouble2)
  {
    paramArrayOfDouble2[0] = paramArrayOfDouble1[0];
    paramArrayOfDouble1[0] = paramDouble;
  }

  public static void N1217(float paramFloat, BigDecimal[] paramArrayOfBigDecimal, float[] paramArrayOfFloat)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramArrayOfFloat[0]);
    paramArrayOfFloat[0] = paramFloat;
  }

  public static void N1221(float paramFloat, short[] paramArrayOfShort, float[] paramArrayOfFloat)
  {
    paramArrayOfShort[0] = ((short)(int)paramArrayOfFloat[0]);
    paramArrayOfFloat[0] = paramFloat;
  }

  public static void N1222(float paramFloat, short[] paramArrayOfShort, double[] paramArrayOfDouble)
  {
    paramArrayOfShort[0] = ((short)(int)paramArrayOfDouble[0]);
    paramArrayOfDouble[0] = paramFloat;
  }

  public static void N1223(float paramFloat, long[] paramArrayOfLong, float[] paramArrayOfFloat)
  {
    paramArrayOfLong[0] = ((long)paramArrayOfFloat[0]);
    paramArrayOfFloat[0] = paramFloat;
  }

  public static void N1224(float paramFloat, int[] paramArrayOfInt, float[] paramArrayOfFloat)
  {
    paramArrayOfInt[0] = ((int)paramArrayOfFloat[0]);
    paramArrayOfFloat[0] = paramFloat;
  }

  public static void N1225(float paramFloat, double[] paramArrayOfDouble, float[] paramArrayOfFloat)
  {
    paramArrayOfDouble[0] = paramArrayOfFloat[0];
    paramArrayOfFloat[0] = paramFloat;
  }

  public static void N1227(short paramShort, BigDecimal[] paramArrayOfBigDecimal1, BigDecimal[] paramArrayOfBigDecimal2)
  {
    paramArrayOfBigDecimal2[0] = paramArrayOfBigDecimal1[0];
    paramArrayOfBigDecimal1[0] = new BigDecimal(paramShort);
  }

  public static void N1231(short paramShort, String[] paramArrayOfString1, String[] paramArrayOfString2)
  {
    paramArrayOfString2[0] = paramArrayOfString1[0];
    paramArrayOfString1[0] = String.valueOf(paramShort);
  }

  public static void N1232(short paramShort, float[] paramArrayOfFloat1, float[] paramArrayOfFloat2)
  {
    paramArrayOfFloat2[0] = paramArrayOfFloat1[0];
    paramArrayOfFloat1[0] = paramShort;
  }

  public static void N1233(short paramShort, long[] paramArrayOfLong1, long[] paramArrayOfLong2)
  {
    paramArrayOfLong2[0] = paramArrayOfLong1[0];
    paramArrayOfLong1[0] = paramShort;
  }

  public static void N1234(short paramShort, double[] paramArrayOfDouble1, double[] paramArrayOfDouble2)
  {
    paramArrayOfDouble2[0] = paramArrayOfDouble1[0];
    paramArrayOfDouble1[0] = paramShort;
  }

  public static void N1236(short paramShort, BigDecimal[] paramArrayOfBigDecimal, short[] paramArrayOfShort)
  {
    int i = paramArrayOfBigDecimal[0].shortValue();
    paramArrayOfShort[0] = (short)i;
    paramArrayOfBigDecimal[0] = new BigDecimal(paramShort);
  }

  public static void N1240(short paramShort, String[] paramArrayOfString, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = Short.valueOf(paramArrayOfString[0]).shortValue();
    paramArrayOfString[0] = String.valueOf(paramShort);
  }

  public static void N1241(short paramShort, float[] paramArrayOfFloat, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = ((short)(int)paramArrayOfFloat[0]);
    paramArrayOfFloat[0] = paramShort;
  }

  public static void N1242(short paramShort, long[] paramArrayOfLong, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = ((short)(int)paramArrayOfLong[0]);
    paramArrayOfLong[0] = paramShort;
  }

  public static void N1243(short paramShort, double[] paramArrayOfDouble, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = ((short)(int)paramArrayOfDouble[0]);
    paramArrayOfDouble[0] = paramShort;
  }

  public static void N1245(short paramShort, BigDecimal[] paramArrayOfBigDecimal, short[] paramArrayOfShort)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramArrayOfShort[0]);
    paramArrayOfShort[0] = paramShort;
  }

  public static void N1249(short paramShort, String[] paramArrayOfString, short[] paramArrayOfShort)
  {
    paramArrayOfString[0] = String.valueOf(paramArrayOfShort[0]);
    paramArrayOfShort[0] = paramShort;
  }

  public static void N1250(short paramShort, float[] paramArrayOfFloat, short[] paramArrayOfShort)
  {
    paramArrayOfFloat[0] = paramArrayOfShort[0];
    paramArrayOfShort[0] = paramShort;
  }

  public static void N1251(short paramShort, long[] paramArrayOfLong, short[] paramArrayOfShort)
  {
    paramArrayOfLong[0] = paramArrayOfShort[0];
    paramArrayOfShort[0] = paramShort;
  }

  public static void N1252(short paramShort, double[] paramArrayOfDouble, short[] paramArrayOfShort)
  {
    paramArrayOfDouble[0] = paramArrayOfShort[0];
    paramArrayOfShort[0] = paramShort;
  }

  public static void N1254(long[] paramArrayOfLong, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramArrayOfLong[0]);
  }

  public static void N1258(long[] paramArrayOfLong, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = ((short)(int)paramArrayOfLong[0]);
  }

  public static void N1259(long[] paramArrayOfLong, float[] paramArrayOfFloat)
  {
    paramArrayOfFloat[0] = ((float)paramArrayOfLong[0]);
  }

  public static void N1260(long[] paramArrayOfLong, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = ((int)paramArrayOfLong[0]);
  }

  public static void N1261(long[] paramArrayOfLong, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramArrayOfLong[0]);
  }

  public static void N1262(long[] paramArrayOfLong, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramArrayOfLong[0];
  }

  public static void N1264(short[] paramArrayOfShort, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramArrayOfShort[0]);
  }

  public static void N1268(short[] paramArrayOfShort1, short[] paramArrayOfShort2)
  {
    paramArrayOfShort2[0] = paramArrayOfShort1[0];
  }

  public static void N1269(short[] paramArrayOfShort, float[] paramArrayOfFloat)
  {
    paramArrayOfFloat[0] = paramArrayOfShort[0];
  }

  public static void N1270(short[] paramArrayOfShort, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = paramArrayOfShort[0];
  }

  public static void N1271(short[] paramArrayOfShort, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramArrayOfShort[0]);
  }

  public static void N1272(short[] paramArrayOfShort, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramArrayOfShort[0];
  }

  public static void N1274(double[] paramArrayOfDouble, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramArrayOfDouble[0]);
  }

  public static void N1278(double[] paramArrayOfDouble, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = ((short)(int)paramArrayOfDouble[0]);
  }

  public static void N1279(double[] paramArrayOfDouble, float[] paramArrayOfFloat)
  {
    paramArrayOfFloat[0] = ((float)paramArrayOfDouble[0]);
  }

  public static void N1280(double[] paramArrayOfDouble, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = ((int)paramArrayOfDouble[0]);
  }

  public static void N1281(double[] paramArrayOfDouble, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramArrayOfDouble[0]);
  }

  public static void N1282(double[] paramArrayOfDouble1, double[] paramArrayOfDouble2)
  {
    paramArrayOfDouble2[0] = paramArrayOfDouble1[0];
  }

  public static void N1284(int[] paramArrayOfInt, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramArrayOfInt[0]);
  }

  public static void N1288(int[] paramArrayOfInt, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = ((short)paramArrayOfInt[0]);
  }

  public static void N1289(int[] paramArrayOfInt, float[] paramArrayOfFloat)
  {
    paramArrayOfFloat[0] = paramArrayOfInt[0];
  }

  public static void N1290(int[] paramArrayOfInt1, int[] paramArrayOfInt2)
  {
    paramArrayOfInt2[0] = paramArrayOfInt1[0];
  }

  public static void N1291(int[] paramArrayOfInt, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramArrayOfInt[0]);
  }

  public static void N1292(int[] paramArrayOfInt, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramArrayOfInt[0];
  }

  public static void N1295(float[] paramArrayOfFloat, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramArrayOfFloat[0]);
  }

  public static void N1300(float[] paramArrayOfFloat, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = ((short)(int)paramArrayOfFloat[0]);
  }

  public static void N1301(float[] paramArrayOfFloat1, float[] paramArrayOfFloat2)
  {
    paramArrayOfFloat2[0] = paramArrayOfFloat1[0];
  }

  public static void N1302(float[] paramArrayOfFloat, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = ((int)paramArrayOfFloat[0]);
  }

  public static void N1303(float[] paramArrayOfFloat, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramArrayOfFloat[0]);
  }

  public static void N1304(float[] paramArrayOfFloat, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramArrayOfFloat[0];
  }

  public static void N1306(String[] paramArrayOfString, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = new BigDecimal(paramArrayOfString[0]);
  }

  public static void N1311(String[] paramArrayOfString, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = Short.valueOf(paramArrayOfString[0]).shortValue();
  }

  public static void N1312(String[] paramArrayOfString, float[] paramArrayOfFloat)
  {
    paramArrayOfFloat[0] = Float.valueOf(paramArrayOfString[0]).floatValue();
  }

  public static void N1313(String[] paramArrayOfString, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = Integer.valueOf(paramArrayOfString[0]).intValue();
  }

  public static void N1314(String[] paramArrayOfString1, String[] paramArrayOfString2)
  {
    paramArrayOfString2[0] = paramArrayOfString1[0];
  }

  public static void N1315(String[] paramArrayOfString, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = Double.valueOf(paramArrayOfString[0]).doubleValue();
  }

  public static void N1317(String[] paramArrayOfString, Date[] paramArrayOfDate)
  {
    paramArrayOfDate[0] = Date.valueOf(paramArrayOfString[0].toString());
  }

  public static void N1318(String[] paramArrayOfString, Time[] paramArrayOfTime)
  {
    paramArrayOfTime[0] = Time.valueOf(paramArrayOfString[0].toString());
  }

  public static void N1319(String[] paramArrayOfString, Timestamp[] paramArrayOfTimestamp)
  {
    paramArrayOfTimestamp[0] = Timestamp.valueOf(paramArrayOfString[0].toString());
  }

  public static void N1320(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException) {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("create table cat.sch.test_tab( e_name varchar(20) not null, e_num int not null, e_city char(15),\te_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
    System.err.println("Table created successfully");

    localStatement.executeUpdate("insert into cat.sch.test_tab values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
    System.err.println("First row inserted successfully");
    localStatement.executeUpdate("update cat.sch.test_tab set e_name = 'Hewlett Packard' where (e_name = 'AAA Computers')");
    localStatement.executeUpdate("update cat.sch.testtab set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',\te_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
    System.err.println("Table Updated successfully");
    localStatement.executeUpdate("delete from cat.sch.test_tab");
    System.err.println("Row deleted successfully");
    localStatement.executeUpdate("drop table cat.sch.test_tab");
    System.err.println("Table dropped successfully");
  }
}
