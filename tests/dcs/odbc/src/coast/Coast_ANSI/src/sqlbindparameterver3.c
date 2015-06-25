/**
  @@@ START COPYRIGHT @@@

  (C) Copyright 2015 Hewlett-Packard Development Company, L.P.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  @@@ END COPYRIGHT @@@
*/

#include <stdio.h>
#include <time.h>
#include <windows.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define NAME_LEN		350
#define	MAX_BINDPARAM1	17
#define MAX_BINDPARAM2	14
#define LOOP_BINDPARAM2	2
#define	MAX_BINDPARAM3	14
#define LOOP_BINDPARAM3	6
#define MAX_BINDPARAM4	9
#define MAX_BINDPARAM6	11
#define MAX_BINDPARAM7	2
#define MAX_BINDPARAM8  14

#ifndef _WM
	#define DATE_FORMAT			"1993-12-30"
	#define FLOAT_FORMAT		"0.123456"
	#define FLOAT_FORMAT_N		"-0.123456"
	#define FLOAT_FORMAT_E		"0.12345678"
	#define DOUBLE_FORMAT		"0.123456789123456"
	#define DOUBLE_FORMAT_N		"-0.123456789123456"
	#define DOUBLE_FORMAT_L		"0.1234567891"
	#define DOUBLE_FORMAT_LN	"-0.1234567891"
#else
	#define DATE_FORMAT			"93/12/30"
	#define FLOAT_FORMAT		".123456"
	#define FLOAT_FORMAT_N		"-.123456"
	#define FLOAT_FORMAT_E		".12345678"
	#define DOUBLE_FORMAT		".123456789123456"
	#define DOUBLE_FORMAT_N		"-.123456789123456"
	#define DOUBLE_FORMAT_L		".1234567891"
	#define DOUBLE_FORMAT_LN	"-.1234567891"
#endif

void TestMXSQLBindParamaterVer3_Cleanup(SQLHANDLE hstmt, char* DrpTab, char* tempType,
										char* InsStr, TestInfo* pTestInfo);

PassFail TestMXSQLBindParameterVer3(TestInfo *pTestInfo)
{
	TEST_DECLARE;
	char			Heading[MAX_HEADING_SIZE];
	RETCODE			returncode;
	SQLHANDLE 		henv;
	SQLHANDLE 		hdbc;
	SQLHANDLE		hstmt;
	int				i, j, k, m;
	int				loop_bindparam;
	SQLSMALLINT		ParamType = SQL_PARAM_INPUT;

	char			*InsStr;
	char			*tempType;
    char            temp[MAX_STRING_SIZE];

//=========================================================================
// Data structures for Testing Section #1

	struct // We have to support bit, tinyint, binary, varbinary, long varbinary
	{
		SQLSMALLINT	SQLType[MAX_BINDPARAM1];
	} CDataArgToSQL1 = 
		{
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,
			SQL_FLOAT,SQL_DOUBLE,SQL_DATE,SQL_TIME,SQL_TIMESTAMP,SQL_LONGVARCHAR,SQL_BIGINT,
            SQL_CHAR,SQL_VARCHAR,SQL_LONGVARCHAR
		};

	struct
	{
		SQLSMALLINT			CType;
		char				*CrtCol;
		SQLUINTEGER			ColPrec[MAX_BINDPARAM1];
		SQLSMALLINT			ColScale[MAX_BINDPARAM1];
		char				*OutputValue[MAX_BINDPARAM1];
	} CDataValueTOSQL1[] = 
		{	// real, float and double precision to char has problem it returns 12345.0 values as 12345.
			{	SQL_C_CHAR,
				"--",
				10,10,10,10,5,10,7,15,15,0,0,26,2000,0,10,10,2440,
				0, 0, 5, 5, 0,0, 0,0, 0, 0,0,6, 0,   0,0, 0, 0,
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1992-12-31 23:45:23.123456","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				"--",
				1,1,1,1,5,10,7,15,15,0,0,26,255,0,1,1,1,
				0,0,0,0,0,0, 0,0, 0, 0,0,6, 0,  0,0,0,0,
				"--","--","1","5","1","1","1","1","1",DATE_FORMAT,"11:45:23","1992-12-31 23:45:23.123456","--","1","--","--","--"
			},
			{	SQL_C_CHAR,
				"--",
				254,254,18,18,5,10,7,15,15,0,0,26,2000,0,254,254,2440,
				0,  0,  6, 6, 0,0, 0,0, 0, 0,0,6, 0,   0,0,  0,  0,
				"--","--","123456789012.3456","123456789012.3456","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1992-12-31 23:45:23.123456","--","1234567890123","--","--","--"
			}, 
			{	SQL_C_CHAR,
				"--",
				10,10,9,9,5,10,7,15,15,0,0,26,2000,0,500,500,2440,
				0,  0,  6,6,0,0, 0,0, 0, 0,0,6, 0,   0,0,  0,  0,
				"--","--","9.000001","12.001101","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1992-12-31 23:45:23.123456","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				"--",
				2,3,4,5,6,7,8,9,10,11,12,13,14,15,18,17,19,
				1,2,3,4,5,6,7,8,9, 10,11,12,13,14,8,9,8,
#ifndef _WM
				"-0.1","0.2","-0.3","0.4","-0.5","0.6","-0.7","0.8","-0.9","1.4","-1.3","2.8","-9.0000008011","0.00000007896","-0.1","0.2","-9.0000008011"
#else
				"-.1",".2","-.3",".4","-.5",".6","-.7",".8","-.9","1.4","-1.3","2.8","-9.0000008011",".00000007896","-.1",".2","-9.0000008011"
#endif
			},
			{	SQL_C_CHAR,
				"--",
				2,3,4,5,6,7,8,9,10,11,12,13,14,15,18,17,19,
				1,2,3,4,5,6,7,8,9, 10,11,12,13,14,8,9,8,
#ifndef _WM
				"-0.1","0.2","-0.3","0.4","-0.5","0.6","-0.7","0.8","-0.9","1.4","-1.3","2.8","-9.0000008011","0.00000007896","-0.1","0.2","-9.0000008011"
#else
				"-.1",".2","-.3",".4","-.5",".6","-.7",".8","-.9","1.4","-1.3","2.8","-9.0000008011",".00000007896","-.1",".2","-9.0000008011"
#endif
			},
			//These 3 cases are added for - leading zeros
			{	SQL_C_CHAR,
				"--",
				254,254,9,9,5,10,7,15,15,0,0,26,2000,0,10,10,2000,
				0,  0,  6,6,0,0, 0,0, 0, 0,0,6, 0,   0,0, 0, 0,
#ifndef _WM
				"--","--","0.00001","0.001101","1234","12345","0.1234","0.123","0.1234567",DATE_FORMAT,"11:45:23","1992-12-31 23:45:23.123456","--","123456","--","--","--"
#else
				"--","--",".00001",".001101","1234","12345","0.1234","0.123","0.1234567",DATE_FORMAT,"11:45:23","1992-12-31 23:45:23.123456","--","123456","--","--","--"
#endif
			},
			{	SQL_C_CHAR,
				"--",
				254,254,9,9,5,10,7,15,15,0,0,26,2000,0,254,254,2000,
				0,  0,  6,6,0,0, 0,0, 0, 0,0,6, 0,   0,0,  0,  0,
#ifndef _WM
				"--","--","-0.00001","-0.001101","1234","12345","-0.1234","-0.123","-0.1234567",DATE_FORMAT,"11:45:23","1992-12-31 23:45:23.123456","--","123456","--","--","--"
#else
				"--","--","-.00001","-.001101","1234","12345","-0.1234","-0.123","-0.1234567",DATE_FORMAT,"11:45:23","1992-12-31 23:45:23.123456","--","123456","--","--","--"
#endif
			},
			{	SQL_C_CHAR,
				"--",
				254,254,9,9,5,10,7,15,15,0,0,26,2000,0,254,254,2000,
				0,  0,  6,6,0,0, 0,0, 0, 0,0,6, 0,   0,0,  0,  0,
				"--","--","10","10","1234","12345","12340.0","12300.0","12345670.0",DATE_FORMAT,"11:45:23","1992-12-31 23:45:23.123456","--","123456","--","--","--"
			},
			//for bignum
			{	SQL_C_CHAR,
				"--",
				254,254,10,128,5,10,7,15,15,0,0,26,2000,0,254,254,2440,
				0,  0,  5, 20, 0,0, 0,0, 0, 0,0,6, 0,   0,0, 0, 0,
				"--","--","1234.56789","999999999999999999999999999999999999.01234567890123456789","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1992-12-31 23:45:23.123456","--","1234567890123","--","--","--"
			}, 
			{	SQL_C_CHAR,
				"--",
				254,254,10,128,5,10,7,15,15,0,0,26,2000,0,128,128,2440,
				0,  0,  5, 20, 0,0, 0,0, 0, 0,0,6, 0,   0,0,  0,  0,
				"--","--","-1234.56789","-999999999999999999999999999999999999.01234567890123456789","-1234","-12345","-12340","-12300","-12345670",DATE_FORMAT,"11:45:23","1992-12-31 23:45:23.123456","--","-1234567890123","--","--","--"
			}, 
			{	SQL_C_CHAR,
				"--",
				254,254,10,10,5,10,7,15,15,0,0,26,2000,0,10,10,2440,
				0,  0,  5, 5, 0,0, 0,0, 0, 0,0,6, 0,   0,0, 0, 0,
				"--","--","1234.56789","12345.56789","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1992-12-31 23:45:23.123456","--","1234567890123","--","--","--"
			}, 
			{	999,
			}
		};


//=========================================================================
// Data structures for Testing Section #2

	struct // We have to support bit, tinyint
	{
		char			*TestSQLType[MAX_BINDPARAM2];
		SQLSMALLINT		SQLType[MAX_BINDPARAM2];
		SQLUINTEGER		ColPrec[MAX_BINDPARAM2];
		SQLSMALLINT		ColScale[MAX_BINDPARAM2];
	} CDataArgToSQL2 = {
			"SQL_CHAR","SQL_VARCHAR","SQL_DECIMAL","SQL_NUMERIC","SQL_SMALLINT","SQL_INTEGER","SQL_REAL","SQL_FLOAT","SQL_DOUBLE","SQL_LONGVARCHAR","SQL_BIGINT","SQL_CHAR","SQL_VARCHAR","SQL_LONGVARCHAR",
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,SQL_FLOAT,SQL_DOUBLE,SQL_LONGVARCHAR,SQL_BIGINT,SQL_CHAR,SQL_VARCHAR,SQL_LONGVARCHAR,
			254,254,18,18,5,10,7,15,15,2000,19,254,254,2000,
			0,  0,  6, 6, 0,0, 0,0, 0, 0,   0, 0,  0,  0};
	
	struct
	{
		SCHAR		CSTINTTOSQL[LOOP_BINDPARAM2*MAX_BINDPARAM2];
		UCHAR		CUTINTTOSQL[LOOP_BINDPARAM2*MAX_BINDPARAM2];
		SCHAR		CTINTTOSQL[LOOP_BINDPARAM2*MAX_BINDPARAM2];
		SWORD		CSSHORTTOSQL[LOOP_BINDPARAM2*MAX_BINDPARAM2];
		UWORD		CUSHORTTOSQL[LOOP_BINDPARAM2*MAX_BINDPARAM2];
		SWORD		CSHORTTOSQL[LOOP_BINDPARAM2*MAX_BINDPARAM2];
		SDWORD		CSLONGTOSQL[LOOP_BINDPARAM2*MAX_BINDPARAM2];
		UDWORD		CULONGTOSQL[LOOP_BINDPARAM2*MAX_BINDPARAM2];
		SDWORD		CLONGTOSQL[LOOP_BINDPARAM2*MAX_BINDPARAM2];
	} CDataTypeTOSQL2 = 
		{
			-1,-2,-3,-4,-5,-6,-7,-8,-9,-1,-2,-1,-2,-1,  -123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,
			1,2,3,4,5,6,7,8,9,1,2,1,2,1,				123,123,123,123,123,123,123,123,123,123,123,123,123,123,
			-1,-2,-3,-4,-5,-6,-7,-8,-9,-1,-2,-1,-2,-1,  -123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,
			-1,-2,-3,-4,-5,-6,-7,-8,-9,-1,-2,-1,-2,-1,  -1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,
			1,2,3,4,5,6,7,8,9,1,2,1,2,2,                1234,1234,1234,1234,1234,1234,1234,1234,1234,1234,1234,1234,1234,1234,
			-1,-2,-3,-4,-5,-6,-7,-8,-9,-1,-2,-1,-2,-1,  -1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,
			-1,-2,-3,-4,-5,-6,-7,-8,-9,-1,-2,-1,-2,-2,  -12345,-12345,-12345,-12345,-1234,-12345,-12345,-12345,-12345,-12345,-12345,-12345,-12345,-12345,
			1,2,3,4,5,6,7,8,9,1,2,1,1,1,                12345,12345,12345,12345,1234,12345,12345,12345,12345,12345,12345,12345,12345,12345,
			-1,-2,-3,-4,-5,-6,-7,-8,-9,-1,-2,-1,-2,-1,  -12345,-12345,-12345,-12345,-1234,-12345,-12345,-12345,-12345,-12345,-12345,-12345,-12345,-12345
		};

	struct
	{
		SQLSMALLINT CType;
		char		*TestCType;
		char		*OutputValue[MAX_BINDPARAM2];
	} CDataValueTOSQL2[] = {
		{SQL_C_STINYINT,"SQL_C_STINYINT","-1","-2","-3","-4.0","-5","-6","-7","-8","-9","-1","-2","-1","-2","-1"},
		{SQL_C_STINYINT,"SQL_C_STINYINT","-123","-123","-123","-123","-123","-123","-123","-123","-123","-123","-123","-123","-123","-123"},
		{SQL_C_UTINYINT,"SQL_C_UTINYINT","1","2","3","4.0","5","6","7","8","9","1","2","1","2","1"},
		{SQL_C_UTINYINT,"SQL_C_UTINYINT","123","123","123","123.0","123","123","123","123","123","123","123","123","123","123"},
		{SQL_C_TINYINT,"SQL_C_TINYINT","-1","-2","-3","-4.0","-5","-6","-7","-8","-9","-1","-2","-1","-2","-1"},
		{SQL_C_TINYINT,"SQL_C_TINYINT","-123","-123","-123","-123","-123","-123","-123","-123","-123","-123","-123","-123","-123","-123"},
		{SQL_C_SSHORT,"SQL_C_SSHORT","-1","-2","-3","-4.0","-5","-6","-7","-8","-9","-1","-2","-1","-2","-1"},
		{SQL_C_SSHORT,"SQL_C_SSHORT","-1234","-1234","-1234.0","-1234.0","-1234","-1234","-1234","-1234","-1234","-1234","-1234","-1234","-1234","-1234"},
		{SQL_C_USHORT,"SQL_C_USHORT","1","2","3","4.0","5","6","7","8","9","1","2","1","2","2"},
		{SQL_C_USHORT,"SQL_C_USHORT","1234","1234","1234.0","1234.0","1234","1234","1234","1234","1234","1234","1234","1234","1234","1234"},
		{SQL_C_SHORT,"SQL_C_SHORT","-1","-2","-3","-4.0","-5","-6","-7","-8","-9","-1","-2","-1","-2","-1"},
		{SQL_C_SHORT,"SQL_C_SHORT","-1234","-1234","-1234.0","-1234.0","-1234","-1234","-1234","-1234","-1234","-1234","-1234","-1234","-1234","-1234"},
		{SQL_C_SLONG,"SQL_C_SLONG","-1","-2","-3","-4.0","-5","-6","-7","-8","-9","-1","-2","-1","-2","-2"},
		{SQL_C_SLONG,"SQL_C_SLONG","-12345","-12345","-12345.0","-12345.0","-1234","-12345","-12345","-12345","-12345","-12345","-12345","-12345","-12345","-12345"},
		{SQL_C_ULONG,"SQL_C_ULONG","1","2","3","4.0","5","6","7","8","9","1","2","1","1","1"},
		{SQL_C_ULONG,"SQL_C_ULONG","12345","12345","12345.0","12345.0","1234","12345","12345","12345","12345","12345","12345","12345","12345","12345"},
		{SQL_C_LONG,"SQL_C_LONG","-1","-2","-3","-4.0","-5","-6","-7","-8","-9","-1","-2","-1","-2","-1"},
		{SQL_C_LONG,"SQL_C_LONG","-12345","-12345","-12345.0","-12345.0","-1234","-12345","-12345","-12345","-12345","-12345","-12345","-12345","-12345","-12345"},
		{999,}
		};

//************************************************
// Data structures for Testing Section #3

	struct // We have to support bit, tinyint
	{
		char		*TestSQLType[MAX_BINDPARAM3];
		SQLSMALLINT	SQLType[MAX_BINDPARAM3];
		SQLUINTEGER	ColPrec[MAX_BINDPARAM3];
		SQLSMALLINT	ColScale[MAX_BINDPARAM3];
	} CDataArgToSQL3 = {
		"SQL_CHAR","SQL_VARCHAR","SQL_DECIMAL","SQL_NUMERIC","SQL_SMALLINT","SQL_INTEGER","SQL_REAL","SQL_FLOAT","SQL_DOUBLE","SQL_LONGVARCHAR","SQL_BIGINT","SQL_CHAR","SQL_VARCHAR","SQL_LONGVARCHAR",
		SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,SQL_FLOAT,SQL_DOUBLE,SQL_LONGVARCHAR,SQL_BIGINT,SQL_CHAR,SQL_VARCHAR,SQL_LONGVARCHAR,
		254,254,18,18,5,10,7,15,15,2000,19,255,255,255,
		  0,  0, 6, 6,0, 0,0, 0, 0,   0, 0,  0,  0,  0};

	struct
	{
		SFLOAT	CFLOATTOSQL[LOOP_BINDPARAM3*MAX_BINDPARAM3];
		SDOUBLE	CDOUBLETOSQL[LOOP_BINDPARAM3*MAX_BINDPARAM3];
	} CDataTypeTOSQL3 = 
		{
			(float)1.0,(float)2.0,(float)3.0,(float)4.0,(float)5,(float)6,(float)7.0,(float)8.0,(float)9.0,(float)1.0,(float)2,(float)1.0,(float)2.0,(float)1.0,
			(float)0.0,(float)0.0,(float)0.0,(float)0.0,(float)0,(float)0,(float)0.0,(float)0.0,(float)0.0,(float)0.0,(float)0,(float)0.0,(float)0.0,(float)0.0,
			(float)0.1,(float)0.2,(float)0.3,(float)0.4,(float)5,(float)6,(float)0.7,(float)0.8,(float)0.8999999761581421,(float)0.1,(float)2,(float)0.1,(float)0.2,(float)0.1,
			(float)12345.669922,(float)12345.669922,(float)12345.669922,(float)12345.669921,(float)1234,(float)12345,(float)12345.6699219,(float)12345.669921875,(float)123456.78,(float)12345.669922,(float)123456,(float)12345.669922,(float)12345.669922,(float)12345.669922,
			(float)-1.0,(float)-2.0,(float)-3.0,(float)-4.0,(float)-5,(float)-6,(float)-7.0,(float)-8.0,(float)-9.0,(float)-1.0,(float)-2,(float)-1.0,(float)-2.0,(float)-1.0,
			(float)-12345.669922,(float)-12345.669922,(float)-12345.669922,(float)-12345.669921,(float)-1234,(float)-12345,(float)-12345.6699219,(float)-12345.669921875,(float)-123456.78,(float)-12345.669922,(float)-123456,(float)-12345.669922,(float)-12345.669922,(float)-12345.669922,
			1.0,2.0,3.0,4.0,5,6,7.0,8.0,9.0,1.0,2,1.0,2.0,1.0,
			0.0,0.0,0.0,0.0,0,0,0.0,0.0,0.0,0.0,0,0.0,0.0,0.0,
			0.1,0.2,0.3,0.4,5,6,0.7,0.8,0.9,0.1,2,0.1,0.2,0.1,
			12345.67,12345.67,12345.67,12345.67,1234,12345,12345.6699219,12345.67,123456.78,12345.67,1234567,12345.67,12345.67,12345.67,
			-1.0,-2.0,-3.0,-4.0,-5,-6,-7.0,-8.0,-9.0,-1.0,-2,-1.0,-2.0,-1.0,
			-12345.67,-12345.67,-12345.67,-12345.67,-1234,-12345,-12345.6699219,-12345.67,-123456.78,-12345.67,-1234567,-12345.67,-12345.67,-12345.67
		};

	struct
	{
		SQLSMALLINT	CType;
		char		*TestCType;
		char		*OutputValue[MAX_BINDPARAM3];
	} CDataValueTOSQL3[] = {
		{SQL_C_FLOAT,"SQL_C_FLOAT","1","2","3.0","4.0","5","6","7","8","9","1","2","1","2","1"},
		{SQL_C_FLOAT,"SQL_C_FLOAT","0","0","0.0","0.0","0","0","0","0","0","0","0","0","0","0"},
		{SQL_C_FLOAT,"SQL_C_FLOAT","0.1","0.2","0.3","0.4","5","6","0.7","0.8","0.8999999761581421","0.1","2","0.1","0.2","0.1"},
		{SQL_C_FLOAT,"SQL_C_FLOAT","12345.669922","12345.669922","12345.669922","12345.669921","1234","12345","12345.6699219","12345.669921875","123456.78","12345.669922","123456","12345.669922","12345.669922","12345.669922"},
		{SQL_C_FLOAT,"SQL_C_FLOAT","-1","-2","-3","-4.0","-5","-6","-7","-8","-9","-1","-2","-1","-2","-1"},
		{SQL_C_FLOAT,"SQL_C_FLOAT","-12345.669922","-12345.669922","-12345.669922","-12345.669921","-1234","-12345","-12345.6699219","-12345.669921875","-123456.78","-12345.669922","-123456","-12345.669922","-12345.669922","-12345.669922"},
		{SQL_C_DOUBLE,"SQL_C_DOUBLE","1","2","3.0","4.0","5","6","7","8","9","1","2","1","2","1"},
		{SQL_C_DOUBLE,"SQL_C_DOUBLE","0","0","0.0","0.0","0","0","0","0","0","0","0","0","0","0"},
		{SQL_C_DOUBLE,"SQL_C_DOUBLE","0.1","0.2","0.3","0.4","5","6","0.7","0.8","0.9","0.1","2","0.1","0.2","0.1"},
		{SQL_C_DOUBLE,"SQL_C_DOUBLE","12345.67","12345.67","12345.67","12345.67","1234","12345","12345.6699219","12345.67","123456.78","12345.67","1234567","12345.67","12345.67","12345.67"},
		{SQL_C_DOUBLE,"SQL_C_DOUBLE","-1","-2","-3","-4.0","-5","-6","-7","-8","-9","-1","-2","-1","-2","-1"},
		{SQL_C_DOUBLE,"SQL_C_DOUBLE","-12345.67","-12345.67","-12345.67","-12345.67","-1234","-12345","-12345.6699219","-12345.67","-123456.78","-12345.67","-123456","-12345.67","-12345.67","-12345.67"},
		{999,}
		};

//************************************************
// Data structures for Testing Section #4

	struct // We have to support longvarchar
	{
		char		*TestSQLType[MAX_BINDPARAM4];
		SQLSMALLINT	SQLType[MAX_BINDPARAM4];
		SQLUINTEGER	ColPrec[MAX_BINDPARAM4];
		SQLSMALLINT	ColScale[MAX_BINDPARAM4];
	} CDataArgToSQL4 = {
			"SQL_CHAR","SQL_VARCHAR","SQL_DATE","SQL_TIME","SQL_TIMESTAMP","SQL_LONGVARCHAR","SQL_CHAR","SQL_VARCHAR","SQL_VARCHAR",
			SQL_CHAR,SQL_VARCHAR,SQL_DATE,SQL_TIME,SQL_TIMESTAMP,SQL_LONGVARCHAR,SQL_CHAR,SQL_VARCHAR,SQL_LONGVARCHAR,
			30,30,0,0,26,255,30,30,255,
			0,0,0,0,6,0,0,0,0};

	struct
	{
		short int	year;
		unsigned short int	month;
		unsigned short int	day;
	} CDATETOSQL = {1993,12,30};

	struct
	{
		unsigned short int	hour;
		unsigned short int	minute;
		unsigned short int	second;
	} CTIMETOSQL = {11,33,41};

	struct
	{
		short int	year;
		unsigned short int	month;
		unsigned short int	day;
		unsigned short int	hour;
		unsigned short int	minute;
		unsigned short int	second;
		unsigned int	fraction; //  
	} CTIMESTAMPTOSQL = {1993,12,30,11,33,41,123456};

	struct
	{
		short int	year;
		unsigned short int	month;
		unsigned short int	day;
		unsigned short int	hour;
		unsigned short int	minute;
		unsigned short int	second;
		unsigned int		fraction; //  
	} CTIMESTAMPTOSQL1 = {1993,12,30,0,0,0,0};

	struct
	{
		short int	year;
		unsigned short int	month;
		unsigned short int	day;
		unsigned short int	hour;
		unsigned short int	minute;
		unsigned short int	second;
		unsigned int		fraction; //  
	} CTIMESTAMPTOSQL2 = {1993,12,30,11,33,41,0};

	struct
	{
		SQLSMALLINT	CType;
		char		*TestCType;
		char		*OutputValue[MAX_BINDPARAM4];
	} CDataValueTOSQL4[] = {
		{
			SQL_C_DATE,"SQL_C_DATE",
			"1993-12-30","1993-12-30",DATE_FORMAT,"11:33:41","1993-12-30","1993-12-30","1993-12-30","1993-12-30","1993-12-30"
		},
		{
			SQL_C_TIME,"SQL_C_TIME",
			"11:33:41","11:33:41",DATE_FORMAT,"11:33:41","11:33:41.000000","11:33:41","11:33:41","11:33:41","11:33:41"
		},
		{
			SQL_C_TIMESTAMP,"SQL_C_TIMESTAMP",
			"1993-12-30 11:33:41.000123","1993-12-30 11:33:41.000123",DATE_FORMAT,"11:33:41","1993-12-30 11:33:41.000123","1993-12-30 11:33:41.000123","1993-12-30 11:33:41.000123","1993-12-30 11:33:41.000123","1993-12-30 11:33:41.000123"
		},
		{999,}
		};
	char	tmpbuf[70],tmpbuf1[30];

//************************************************
// Data structures for Testing Section #5

	struct // We have to support bit, tinyint, binary, varbinary, long varbinary
	{
		SQLSMALLINT	SQLType[MAX_BINDPARAM1];
	} CDataArgToSQL5 = 
		{
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,
			SQL_FLOAT,SQL_DOUBLE,SQL_DATE,SQL_TIME,SQL_TIMESTAMP,SQL_LONGVARCHAR,SQL_BIGINT,
            SQL_CHAR,SQL_VARCHAR,SQL_LONGVARCHAR
		};

	struct
	{
		SQLSMALLINT CType;
		RETCODE		PassFail;
		BOOL		NullData;
		char		*CrtCol;
		SQLUINTEGER	ColPrec[MAX_BINDPARAM1];
		SQLSMALLINT	ColScale[MAX_BINDPARAM1];
		char		*CharValue;
		char		*VarCharValue;
		char		*DecimalValue;
		char		*NumericValue;
		SWORD		ShortValue;
		SDWORD		LongValue;
		SFLOAT		RealValue;
		SDOUBLE		FloatValue;
		SDOUBLE		DoubleValue;
		struct
		{
			short int			year;
			unsigned short int	month;
			unsigned short int	day;
		} DateValue;
		struct
		{
			unsigned short int	hour;
			unsigned short int	minute;
			unsigned short int	second;
		} TimeValue;

		struct
		{
			short int			year;
			unsigned short int	month;
			unsigned short int	day;
			unsigned short int	hour;
			unsigned short int	minute;
			unsigned short int	second;
			unsigned int		fraction; //  
		} TimestampValue;
		char				*LongVarCharValue;
		#ifdef WIN32
			_int64	  			BigintValue;
		#else
			long long  			BigintValue;
		#endif
        char		        *NCharValue;
		char		        *NVarCharValue;
        char                *NLongVarCharValue;
		char				*OutputValue[MAX_BINDPARAM1];
	} CDataValueTOSQL5[] = 
		{		// real, float and double precision to char has problem it returns 12345.0 values as 12345.
			{	SQL_C_DEFAULT,
				SQL_SUCCESS,
				FALSE,
				"--",
				10,10,10,10,5,10,7,15,15,0,0,29,2000,19,10,10,2000,
				0, 0, 5, 5, 0,0, 0,0, 0, 0,0,6, 0,   0, 0, 0, 0,
				"--",
				"--",
				"1234.56789",			
				"5678.12345",//{10,5,1,0xF9,0x20,0xD8,0x21,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},//	"5678.12345"
				1234,
				12345,
				12340.0,
				12300.0,
				12345670.0,
				{1993,12,30},
				{11,45,23},
				{1997,10,12,11,33,41,123456000},
				"--",
				123456,
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.123456","--","123456","--","--","--"
			},
			{	SQL_C_DEFAULT,
				SQL_SUCCESS,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,0,0,29,2000,19,254,254,2000,
				0,  0,  5, 5, 0,0, 0,0, 0, 0,0,6, 0,   0, 0,  0,  0,
				"--",
				"--",
				"1234.56789",
				"5678.12345",//{10,5,1,0xF9,0x20,0xD8,0x21,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},//	"5678.12345"
				0,
				0,
				0,
				0,
				0,
				{1993,12,30},
				{11,45,23},
				{1997,10,12,11,33,41,123456000},
				"--",
				123456,
                "--","--","--",
				"--","--","1234.56789","5678.12345","0","0","0","0","0",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.123456","--","123456","--","--","--"
			},
			{	SQL_C_DEFAULT,//c_numeric
				SQL_SUCCESS,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,0,0,29,2000,19,254,254,2000,
				0,  0,  5, 5, 0,0, 0,0, 0, 0,0,6, 0,   0, 0,  0,  0,
				"--",
				"--",
				"1234.56789",
				"5678.12345",//{10,5,1,0xF9,0x20,0xD8,0x21,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},//	"5678.12345"
				1234,
				12345,
				12340.0,
				12300.0,
				12345670.0,
				{1993,12,30},
				{11,45,23},
				{1997,10,12,11,33,41,123456000},
				"--",
				123456,
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.123456","--","123456","--","--","--"
			},
			{	SQL_C_DEFAULT,
				SQL_SUCCESS,
				FALSE,
				"--",
				10,10,10,10,5,10,7,15,15,0,0,29,2000,19,10,10,2000,
				0, 0, 5, 5, 0,0, 0,0, 0, 0,0,6, 0,   0, 0, 0, 0,
				"--",
				"--",
				"1234.56789",
				"5678.12345",//{10,5,1,0xF9,0x20,0xD8,0x21,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},//	"5678.12345"
				1234,
				12345,
				12340.0,
				12300.0,
				12345670.0,
				{1993,12,30},
				{11,45,23},
				{1997,10,12,11,33,41,123456},
				"--",
				123456,
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			//5/9/06: For bad data testing
			{
				SQL_C_DEFAULT,
				SQL_ERROR, 
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,0,0,26,2000,19,254,254,2000,
				0,  0,  5, 5, 0,0, 0,0,0,0,0,6,   0,   0, 0,  0, 0,
				"--",//error
				"--",//error
				"123",
				"5678.12345",//{10,5,1,0xF9,0x20,0xD8,0x21,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				1234,
				12345,
				12340.0,
				12300.0,
				12345670.0,
				{1993,15,60},
				{11,85,93},
				{1997,15,42,11,33,41,123456},
				"--",
				123456,
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	
				SQL_C_DEFAULT,
				SQL_ERROR,
				FALSE,
				"--",
				10,10,10,10,5,10,7,15,15,0,0,26,2000,19,10,10,2000,
				0, 0, 5, 5, 0,0, 0,0, 0, 0,0,6, 0,   0, 0, 0, 0,
				"--",
				"--",
				"123-",//error
				"5678.12345",//{10,5,1,0xF9,0x20,0xD8,0x21,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				1234,
				12345,
				12340.0,
				12300.0,
				12345670.0,
				{1993,15,60},
				{11,85,93},
				{1997,15,42,11,33,41,123456},
				"--",
				123456,
                "--","--","--",
				"--","--","123","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	//*******************************err
				SQL_C_DEFAULT,//c_numeric
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,0,0,26,2000,19,254,254,2000,
				0,  0,  5, 5, 0,0, 0,0, 0, 0,0,6, 0,   0, 0,  0,  0,
				"--",
				"--",
				"1234.56789-", //error
				"5678.12345",//{10,5,1,0xF9,0x20,0xD8,0x21,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				1234,
				12345,
				12340.0,
				12300.0,
				12345670.0,
				{1993,12,30},
				{11,45,23},
				{1997,10,12,11,33,41,123456000},
				"--",
				123456,
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.123456","--","123456","--","--","--"
			},
			{	999,}
		};

//************************************************
// Data structures for Testing Section #6

	struct // We have to support bit, tinyint, binary, varbinary, long varbinary
	{
		SQLSMALLINT	SQLType[MAX_BINDPARAM6];
	} CDataArgToSQL6 = 
		{
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,
			SQL_FLOAT,SQL_DOUBLE,/*SQL_DATE,SQL_TIME,SQL_TIMESTAMP,*/SQL_LONGVARCHAR,SQL_BIGINT
		};
	struct
	{
		SQLSMALLINT		CType;
		RETCODE			PassFail;
		BOOL			NullData;
		char			*CrtCol;
		SQLUINTEGER		ColPrec[MAX_BINDPARAM6];
		SQLSMALLINT		ColScale[MAX_BINDPARAM6];
		SQL_NUMERIC_STRUCT NumericValue1;
		SQL_NUMERIC_STRUCT NumericValue2;
		SQL_NUMERIC_STRUCT NumericValue3;
		SQL_NUMERIC_STRUCT NumericValue4;
		SQL_NUMERIC_STRUCT NumericValue5;
		SQL_NUMERIC_STRUCT NumericValue6;
		SQL_NUMERIC_STRUCT NumericValue7;
		SQL_NUMERIC_STRUCT NumericValue8;
		SQL_NUMERIC_STRUCT NumericValue9;
		SQL_NUMERIC_STRUCT NumericValue10;
		SQL_NUMERIC_STRUCT NumericValue11;
		char				*OutputValue[MAX_BINDPARAM6];
	} CDataValueTOSQL6[] = 
		{			// real, float and double precision to char has problem it returns 12345.0 values as 12345.
			{	SQL_C_NUMERIC,
				SQL_SUCCESS,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,2000,10,
				0,0,5,5,0,0,0,0,0,0,0,	
				{9,0,1,0x15,0xCD,0x5B,0x07,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{9,0,1,0x15,0xCD,0x5B,0x07,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{10,5,1,0x15,0xCD,0x5B,0x07,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{10,5,1,0xF9,0x20,0xD8,0x21,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{4,0,1,0xD2,0x04,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{5,0,1,0x39,0x30,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{5,0,1,0x34,0x30,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{5,0,1,0x0C,0x30,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{8,0,1,0x46,0x61,0xBC,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{9,0,1,0x15,0xCD,0x5B,0x07,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{6,0,1,0x40,0xE2,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670","--","123456"
			},
			{	SQL_C_NUMERIC,//c_numeric
				SQL_SUCCESS,
				TRUE,
				"--",
				254,254,10,10,5,10,7,15,15,2000,10,
				0,0,5,5,0,0,0,0,0,0,0,
				{9,0,1,0x15,0xCD,0x5B,0x07,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{9,0,1,0x15,0xCD,0x5B,0x07,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{10,5,1,0x15,0xCD,0x5B,0x07,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{10,5,1,0xF9,0x20,0xD8,0x21,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{4,0,1,0xD2,0x04,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{5,0,1,0x39,0x30,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{5,0,1,0x34,0x30,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{5,0,1,0x0C,0x30,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{8,0,1,0x46,0x61,0xBC,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{9,0,1,0x15,0xCD,0x5B,0x07,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{6,0,1,0x40,0xE2,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670","--","123456"
			},
			{	SQL_C_NUMERIC,
				SQL_ERROR,
				TRUE,
				"--",
				254,254,10,10,5,10,7,15,15,2000,10,
				0,0,5,5,0,0,0,0,0,0,0,
				{9,0,1,0x15,0xCD,0x5B,0x07,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{9,0,1,0x15,0xCD,0x5B,0x07,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{10,5,1,0x15,0xCD,0x5B,0x07,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{10,5,1,0xF9,0x20,0xD8,0x21,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{4,0,1,0xD2,0x04,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{5,0,1,0x39,0x30,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{5,0,1,0x34,0x30,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{5,0,1,0x0C,0x30,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{8,0,1,0x46,0x61,0xBC,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{9,0,1,0x15,0xCD,0x5B,0x07,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				{6,0,1,0x40,0xE2,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670","--","123456"
			},
			{	999,
			}
		};

	SQLLEN	InValue = SQL_NTS, InValue1 = 0, InValueNullData = SQL_NULL_DATA;
	char	OutValue[NAME_LEN*2+1]; // doubled for UCS2
	SQLLEN	OutValueLen = SQL_NTS; //  
	
//===========================================================================================================
//************************************************
// Data structures for Testing Section #7

	struct 
	{
		SQLSMALLINT	SQLType[MAX_BINDPARAM7];
	} CDataArgToSQL7 = 
		{
			SQL_TIMESTAMP,SQL_TIMESTAMP
		};

	struct
	{
		SQLSMALLINT		CType;
		RETCODE			PassFail;
		BOOL			NullData;
		char			*CrtCol;
		SQLUINTEGER		ColPrec[MAX_BINDPARAM7];
		SQLSMALLINT		ColScale[MAX_BINDPARAM7];
		struct
		{
			short int	year;
			unsigned short int	month;
			unsigned short int	day;
			unsigned short int	hour;
			unsigned short int	minute;
			unsigned short int	second;
		} TimestampValue1;
		struct
		{
			short int	year;
			unsigned short int	month;
			unsigned short int	day;
			unsigned short int	hour;
			unsigned short int	minute;
			unsigned short int	second;
			unsigned int	fraction; //  
		} TimestampValue2;
		char				*OutputValue[MAX_BINDPARAM7];
	} CDataValueTOSQL7[] = 
		{			// real, float and double precision to char has problem it returns 12345.0 values as 12345.
			{	SQL_C_DEFAULT,
				SQL_SUCCESS,
				FALSE,
				"(C1 TIMESTAMP,C2 TIMESTAMP) NO PARTITION",
				26,26,
				6,6,
				{2000,10,12,11,33,41},
				{1997,10,12,11,33,41,123456},
				"2000-10-12 11:33:41","1997-10-12 11:33:41.000123"
			},
/*			{	SQL_C_DEFAULT,
				SQL_SUCCESS,
				TRUE,
				"(C1 TIMESTAMP,C2 TIMESTAMP)",
				26,26,
				6,6,
				{2000,10,12,11,33,41},
				{1997,10,12,11,33,41,123456},
				"2000-10-12 11:33:41","1997-10-12 11:33:41.000123"

			},
			{	SQL_C_TIMESTAMP,
				SQL_SUCCESS,
				FALSE,
				"(C1 TIMESTAMP,C2 TIMESTAMP)",
				26,26,
				6,6,
				{2000,10,12,11,33,41},
				{1997,10,12,11,33,41,123456},
				"2000-10-12 11:33:41","1997-10-12 11:33:41.000123"
			},
			{	SQL_C_TIMESTAMP,
				SQL_SUCCESS,
				TRUE,
				"(C1 TIMESTAMP,C2 TIMESTAMP)",
				26,26,
				6,6,
				{2000,10,12,11,33,41},
				{1997,10,12,11,33,41,123456},
				"2000-10-12 11:33:41","1997-10-12 11:33:41.000123"
			}, */
			{	999,
			}
		};
	
//************************************************
// Data structures for Testing Section #8
	
	struct // We have to support bit, tinyint, binary, varbinary, long varbinary
	{
		SQLSMALLINT	SQLType[MAX_BINDPARAM1];
	} CDataArgToSQL8 = 
		{
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,
			SQL_FLOAT,SQL_DOUBLE,SQL_DATE,SQL_TIME,SQL_TIMESTAMP,SQL_LONGVARCHAR,SQL_BIGINT,
            SQL_CHAR,SQL_VARCHAR,SQL_LONGVARCHAR
		};
	struct
	{
		SQLSMALLINT		CType;
		RETCODE			PassFail;
		BOOL			NullData;
		char			*CrtCol;
		SQLUINTEGER		ColPrec[MAX_BINDPARAM1];
		SQLSMALLINT		ColScale[MAX_BINDPARAM1];
		char	*CharValue;
		char	*VarCharValue;
		char	*DecimalValue;
		char	*NumericValue;
		char	*ShortValue;
		char	*LongValue;
		char	*RealValue;
		char	*FloatValue;
		char	*DoubleValue;
		char	*DateValue;
		char	*TimeValue;
		char	*TimestampValue;
		char	*LongVarCharValue;
		char	*BigintValue;
        char    *NCharValue;
        char    *NVarCharValue;
        char    *NLongVarCharValue;
		char	*OutputValue[MAX_BINDPARAM1];
	} CDataValueTOSQL8[] = 
		{// real, float and double precision to char has problem it returns 12345.0 values as 12345.

			{ 
				SQL_C_CHAR,
				SQL_SUCCESS,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",
				"--",
				"1234.56789", 
				"1234.56789", 
				"1234",
				"12345",
				"12340.0",
				"12300.0",
				"12345670.0",
				"1993-12-30",
				"11:45:23",
				"1997-10-12 11:33:41.000123",
				"--",
				"123456",
                "--","--","--",
				"--","--","1234.56789","1234.56789","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",
				"--",
				"1234.56789", 
				"1234.56789ABCDE", //error
				"1234",
				"12345",
				"12340.0",
				"12300.0",
				"12345670.0",
				"1993-12-30",
				"11:45:23",
				"1997-10-12 11:33:41.123456 AM",
				"--",
				"123456",
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0,0, 0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",
				"--",
				"1234.56789-", //error
				"1234.56789", 
				"1234",
				"12345",
				"12340.0",
				"12300.0",
				"12345670.0",
				"1993-12-30",
				"11:45:23",
				"1997-10-12 11:33:41.123456 AM",
				"--",
				"123456",
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",
				"--", //error, only 10 chars must be inserted
				"1234.56789", 
				"1234.56789", 
				"1234",
				"12345",
				"12340.0",
				"12300.0",
				"12345670.0",
				"1993-12-30",
				"11:45:23",
				"1997-10-12 11:33:41.123456 AM",
				"--",
				"123456",
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",//error, only first 10 chars must be inserted
				"--",
				"1234.56789", 
				"1234.56789", 
				"1234",
				"12345",
				"12340.0",
				"12300.0",
				"12345670.0",
				"1993-12-30",
				"11:45:23",
				"1997-10-12 11:33:41.123456 CM",
				"--",
				"123456",
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",
				"--",
				"1234.56789", 
				"1234.56789", 
				"1234-",//error
				"12345",
				"12340.0",
				"12300.0",
				"12345670.0",
				"1993-12-30",
				"11:45:23",
				"1997-10-12 11:33:41.123456 AM",
				"--",
				"123456",
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",
				"--",
				"1234.56789", 
				"1234.56789", 
				"1234",
				"12345abcde", //error
				"12340.0",
				"12300.0",
				"12345670.0",
				"1993-12-30",
				"11:45:23",
				"1997-10-12 11:33:41.123456 AM",
				"--",
				"123456",
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",                   // C1 CHAR(10)
				"--",                   //C2 VARCHAR(10)
				"1234.56789",           //C3 DECIMAL(10,5)
				"1234.56789",           //C4 NUMERIC(10,5)
				"1234",                 //C5 SMALLINT
				"12345",                //C6 INTEGER
				"12340.0-+",            //C7 REAL //error
				"12300.0",              //C8 FLOAT
				"12345670.0",           //C9 DOUBLE PRECISION
				"1993-12-30",           //C10 DATE
				"11:45:23",             //,C11 TIME
				"1997-10-12 11:33:41.123456 AM",//C12 TIMESTAMP
				"--",                   //C13 LONG VARCHAR
				"123456",               //C14 BIGINT
                "--","--","--",         //C15,C16,C17 NCHAR UCS2
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",// C1 CHAR(10)
				"--",//C2 VARCHAR(10)
				"1234.56789", //C3 DECIMAL(10,5)
				"1234.56789", //C4 NUMERIC(10,5)
				"1234",//C5 SMALLINT
				"12345",//C6 INTEGER
				"12340.0",//C7 REAL
				"12300.0abcde",//C8 FLOAT //error
				"12345670.0",//C9 DOUBLE PRECISION
				"1993-12-30",//C10 DATE
				"11:45:23",//,C11 TIME
				"1997-10-12 11:33:41.123456 AM",//C12 TIMESTAMP
				"--",//C13 LONG VARCHAR
				"123456",//C14 BIGINT
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",// C1 CHAR(10)
				"--",//C2 VARCHAR(10)
				"1234.56789", //C3 DECIMAL(10,5)
				"1234.56789", //C4 NUMERIC(10,5)
				"1234",//C5 SMALLINT
				"12345",//C6 INTEGER
				"12340.0",//C7 REAL
				"12300.0",//C8 FLOAT
				"12345670.0.9",//C9 DOUBLE PRECISION //error
				"1993-12-30",//C10 DATE
				"11:45:23",//,C11 TIME
				"1997-10-12 11:33:41.123456 AM",//C12 TIMESTAMP
				"--",//C13 LONG VARCHAR
				"123456",//C14 BIGINT
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",// C1 CHAR(10)
				"--",//C2 VARCHAR(10)
				"1234.56789", //C3 DECIMAL(10,5)
				"1234.56789", //C4 NUMERIC(10,5)
				"1234",//C5 SMALLINT
				"12345",//C6 INTEGER
				"12340.0",//C7 REAL
				"12300.0",//C8 FLOAT
				"12345670.0",//C9 DOUBLE PRECISION
				"19",//C10 DATE //error
				"11:45:23",//,C11 TIME
				"1997-10-12 11:33:41.123456 AM",//C12 TIMESTAMP
				"--",//C13 LONG VARCHAR
				"123456",//C14 BIGINT
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",// C1 CHAR(10)
				"--",//C2 VARCHAR(10)
				"1234.56789", //C3 DECIMAL(10,5)
				"1234.56789", //C4 NUMERIC(10,5)
				"1234",//C5 SMALLINT
				"12345",//C6 INTEGER
				"12340.0",//C7 REAL
				"12300.0",//C8 FLOAT
				"12345670.0",//C9 DOUBLE PRECISION
				"1993-234-30",//C10 DATE //error
				"11:45:23",//,C11 TIME
				"1997-10-12 11:33:41.123456 AM",//C12 TIMESTAMP
				"--",//C13 LONG VARCHAR
				"123456",//C14 BIGINT
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",// C1 CHAR(10)
				"--",//C2 VARCHAR(10)
				"1234.56789", //C3 DECIMAL(10,5)
				"1234.56789", //C4 NUMERIC(10,5)
				"1234",//C5 SMALLINT
				"12345",//C6 INTEGER
				"12340.0",//C7 REAL
				"12300.0",//C8 FLOAT
				"12345670.0",//C9 DOUBLE PRECISION
				"1993-12-30",//C10 DATE
				"11:495:237",//,C11 TIME //error
				"1997-10-12 11:33:41.123456 AM",//C12 TIMESTAMP
				"--",//C13 LONG VARCHAR
				"123456",//C14 BIGINT
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,0,0,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0,0,0, 6,   0, 0,  0,  0,   0,
				"--",// C1 CHAR(10)
				"--",//C2 VARCHAR(10)
				"1234.56789", //C3 DECIMAL(10,5)
				"1234.56789", //C4 NUMERIC(10,5)
				"1234",//C5 SMALLINT
				"12345",//C6 INTEGER
				"12340.0",//C7 REAL
				"12300.0",//C8 FLOAT
				"12345670.0",//C9 DOUBLE PRECISION
				"1993-12-30",//C10 DATE
				"abcde",//,C11 TIME //error
				"1997-10-12 11:33:41.123456 AM",//C12 TIMESTAMP
				"--",//C13 LONG VARCHAR
				"123456",//C14 BIGINT
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",// C1 CHAR(10)
				"--",//C2 VARCHAR(10)
				"1234.56789", //C3 DECIMAL(10,5)
				"1234.56789", //C4 NUMERIC(10,5)
				"1234",//C5 SMALLINT
				"12345",//C6 INTEGER
				"12340.0",//C7 REAL
				"12300.0",//C8 FLOAT
				"12345670.0",//C9 DOUBLE PRECISION
				"1993-12-30",//C10 DATE
				"11:45:23",//,C11 TIME
				"1997-10-12 11:33:41.123456 FM",//C12 TIMESTAMP //error
				"--",//C13 LONG VARCHAR
				"123456",//C14 BIGINT
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",// C1 CHAR(10)
				"--",//C2 VARCHAR(10)
				"1234.56789", //C3 DECIMAL(10,5)
				"1234.56789", //C4 NUMERIC(10,5)
				"1234",//C5 SMALLINT
				"12345",//C6 INTEGER
				"12340.0",//C7 REAL
				"12300.0",//C8 FLOAT
				"12345670.0",//C9 DOUBLE PRECISION
				"1993-12-30",//C10 DATE
				"11:45:23",//,C11 TIME
				"1997-10-12 11:33:41567.1234569999999999999 AM",//C12 TIMESTAMP //error
				"--",//C13 LONG VARCHAR
				"123456",//C14 BIGINT
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",// C1 CHAR(10)
				"--",//C2 VARCHAR(10)
				"1234.56789", //C3 DECIMAL(10,5)
				"1234.56789", //C4 NUMERIC(10,5)
				"1234",//C5 SMALLINT
				"12345",//C6 INTEGER
				"12340.0",//C7 REAL
				"12300.0",//C8 FLOAT
				"12345670.0",//C9 DOUBLE PRECISION
				"1993-12-30",//C10 DATE
				"11:45:23",//,C11 TIME
				"1997-10-123 11:33:41.123456 AM",//C12 TIMESTAMP //error
				"--",//C13 LONG VARCHAR
				"123456",//C14 BIGINT
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",// C1 CHAR(10)
				"--",//C2 VARCHAR(10)
				"1234.56789", //C3 DECIMAL(10,5)
				"1234.56789", //C4 NUMERIC(10,5)
				"1234",//C5 SMALLINT
				"12345",//C6 INTEGER
				"12340.0",//C7 REAL
				"12300.0",//C8 FLOAT
				"12345670.0",//C9 DOUBLE PRECISION
				"1993-12-30",//C10 DATE
				"11:45:23",//,C11 TIME
				"1997-1056-12 11:33:41.123456 AM",//C12 TIMESTAMP //error
				"--",//C13 LONG VARCHAR
				"123456",//C14 BIGINT
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",                               // C1 CHAR(10)
				"--",                               //C2 VARCHAR(10)
				"1234.56789",                       //C3 DECIMAL(10,5)
				"1234.56789",                       //C4 NUMERIC(10,5)
				"1234",                             //C5 SMALLINT
				"12345",                            //C6 INTEGER
				"12340.0",                          //C7 REAL
				"12300.0",                          //C8 FLOAT
				"12345670.0",                       //C9 DOUBLE PRECISION
				"1993-12-30",                       //C10 DATE
				"11:45:23",                         //,C11 TIME
				"1997-10-12 11:33:41.123456 AM",    //C12 TIMESTAMP
				"--",                               //C13 LONG VARCHAR
				"123456abcde",                      //C14 BIGINT //error
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,224,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",                               // C1 CHAR(10)
				"--",                               //C2 VARCHAR(10)
				"1234.56789",                       //C3 DECIMAL(10,5)
				"1234.56789",                       //C4 NUMERIC(10,5)
				"1234",                             //C5 SMALLINT
				"12345",                            //C6 INTEGER
				"12340.0",                          //C7 REAL
				"12300.0",                          //C8 FLOAT
				"12345670.0",                       //C9 DOUBLE PRECISION
				"1993-12-30",                       //C10 DATE
				"11:45:23",                         //,C11 TIME
				"1997-10-12 11:33:41.123456 AM",    //C12 TIMESTAMP
				"--",                               //C13 LONG VARCHAR
				"123456-",                          //C14 BIGINT //error
                "--","--","--",
				"--","--","1234.56789","5678.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			//Negative test for Bignum
			{ 
				SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",
				"--",
				"1234.56789", 
				"12345678901.12345", //NUMERIC(30,20)
				"1234",
				"12345",
				"12340.0",
				"12300.0",
				"12345670.0",
				"1993-12-30",
				"11:45:23",
				"1997-10-12 11:33:41.000123",
				"--",
				"123456",
                "--","--","--",
				"--","--","1234.56789","12345678901.12345","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{ 
				SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",
				"--",
				"1234.56789", 
				"1.23456789", //NUMERIC(30,30)
				"1234",
				"12345",
				"12340.0",
				"12300.0",
				"12345670.0",
				"1993-12-30",
				"11:45:23",
				"1997-10-12 11:33:41.000123",
				"--",
				"123456",
                "--","--","--",
				"--","--","1234.56789","1.23456789","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{ 
				SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",
				"--",
				"1234.56789", 
				"-1234.56789", //NUMERIC(10,5) UNSIGNED
				"1234",
				"12345",
				"12340.0",
				"12300.0",
				"12345670.0",
				"1993-12-30",
				"11:45:23",
				"1997-10-12 11:33:41.000123",
				"--",
				"123456",
                "--","--","--",
				"--","--","1234.56789","-1234.56789","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{ 
				SQL_C_CHAR,
				SQL_ERROR,
				FALSE,
				"--",
				254,254,10,10,5,10,7,15,15,12,10,26,2000,19,254,254,2000,
				  0,  0, 5, 5,0, 0,0, 0, 0, 0, 0, 6,   0, 0,  0,  0,   0,
				"--",
				"--",
				"1234.56789", 
				"-123456789012345678.123", //NUMERIC(18,5) UNSIGNED
				"1234",
				"12345",
				"12340.0",
				"12300.0",
				"12345670.0",
				"1993-12-30",
				"11:45:23",
				"1997-10-12 11:33:41.000123",
				"--",
				"123456",
                "--","--","--",
				"--","--","1234.56789","-123456789012345678.123","1234","12345","12340","12300","12345670",DATE_FORMAT,"11:45:23","1997-10-12 11:33:41.000123","--","123456","--","--","--"
			},
			{	999,}
		};

//************************************************
// Data structures for Testing Section #9

    struct {
		RETCODE		PassFail;
		char		*CrtCol;
		SQLUINTEGER	ColPrec[MAX_BINDPARAM8];
		SQLSMALLINT	ColScale[MAX_BINDPARAM8];
		SFLOAT		FloatValue[MAX_BINDPARAM8];
        char        *OutputValue[MAX_BINDPARAM8];
    } CFloatToNumeric[] = {
        {SQL_SUCCESS, 
            "--",
            {18,18,18,19,19,19,128,64,128,128,18,19,128,64},
            {0,18,17,0,19,18,0,0,128,127,0,10,0,32},
            {(float)12345678.0, (float)0.123456, (float)1.234567, (float)12345678.0, (float)0.123456, (float)1.234567, (float)12345678.0, (float)12345678, (float)0.123456, (float)1.234567, (float)12345678.0, (float)1.0123456789, (float)12345678.0,(float)1.0123456789},
            {"12345678",        FLOAT_FORMAT,    "1.234567",       "12345678",         FLOAT_FORMAT,   "1.234567",      "12345678",       "12345678",      FLOAT_FORMAT,    "1.234567",      "12345678",         "1.012346",         "12345678",       "1.012346"}
        },
        {SQL_SUCCESS, 
            "--",
            {18,18,18,19,19,19,128,64,128,128,18,19,128,64},
            {0,18,17,0,19,18,0,0,128,127,0,10,0,32},
            {(float)-12345678.0, (float)-0.123456, (float)-1.234567, (float)-12345678.0, (float)-0.123456, (float)-1.234567, (float)-12345678.0, (float)-12345678, (float)-0.123456, (float)-1.234567, (float)-12345678.0, (float)-1.0123456789, (float)-12345678.0, (float)-1.0123456789},
            {"-12345678",        FLOAT_FORMAT_N,   "-1.234567",     "-12345678",         FLOAT_FORMAT_N,  "-1.234567",      "-12345678",        "-12345678",      FLOAT_FORMAT_N,   "-1.234567",      "-12345678",        "-1.012346",           "-12345678",        "-1.012346"}
        },
        {SQL_SUCCESS, 
            "--",
            {18,18,18,19,19,19,128,64,128,128,18,19,128,64},
            {0,18,17,0,19,18,0,0,128,127,0,10,0,32},
            {(float)12345678.0, (float)0.123456, (float)1.234567, (float)12345678.0, (float)0.123456, (float)1.234567, (float)12345678.0, (float)12345678, (float)0.123456, (float)1.234567, (float)12345678.0, (float)1.0123456789, (float)12345678.0,(float)1.0123456789},
            {"12345678",        FLOAT_FORMAT,    "1.234567",       "12345678",         FLOAT_FORMAT,   "1.234567",      "12345678",       "12345678",      FLOAT_FORMAT,    "1.234567",      "12345678",         "1.012346",         "12345678",       "1.012346"}
        },
        {SQL_SUCCESS, 
            "--",
            {19,19,19,19,19,128,128,19,19,19,19,19,128,128},
            {0,1,2,18,19,0,128,0,1,2,18,19,0,128},
            {(float)-12345678.0, (float)-123456.789, (float)-123456.789, (float)-1.234567, (float)-0.123456, (float)-12345678.0, (float)-0.123456, (float)12345678.0, (float)123456.789, (float)123456.789, (float)1.234567, (float)0.123456, (float)12345678.0, (float)0.123456},
            {"-12345678",        "-123456.7",        "-123456.78",        "-1.234567",     FLOAT_FORMAT_N,   "-12345678",        FLOAT_FORMAT_N,   "12345678",        "123456.7",        "123456.78",        "1.234567",     FLOAT_FORMAT,    "12345678",        FLOAT_FORMAT}
        },
        {SQL_ERROR, 
            "--",
            {19,19,19,19,19,128,128,19,19,19,19,19,128,128},
            {0,1,2,18,19,0,128,0,1,2,18,19,0,128},
            {(float)-1.2345678901234567E+19, (float)-123456.789, (float)-123456.789, (float)-1.234567, (float)-0.123456, (float)-12345678.0, (float)-0.123456, (float)12345678.0, (float)123456.789, (float)123456.789, (float)1.234567, (float)0.123456, (float)12345678.0, (float)0.123456},
            {"-1.2345678901234567E+19",        "-123456.7",        "-123456.78",        "-1.234567",     FLOAT_FORMAT_N,   "-12345678",        FLOAT_FORMAT_N,   "12345678",        "123456.7",        "123456.78",        "1.234567",     FLOAT_FORMAT,    "12345678",        FLOAT_FORMAT}
        },
        {999,
        }
    };

//************************************************
// Data structures for Testing Section #10

    struct {
		RETCODE		PassFail;
		char		*CrtCol;
		SQLUINTEGER	ColPrec[MAX_BINDPARAM8];
		SQLSMALLINT	ColScale[MAX_BINDPARAM8];
		SDOUBLE		DoubleValue[MAX_BINDPARAM8];
        char        *OutputValue[MAX_BINDPARAM8];
    } CDoubleToNumeric[] = {
        {SQL_SUCCESS, 
            "--",
            {18,18,18,19,19,19,128,64,128,128,18,19,128,64},
            {0,18,17,0,19,18,0,0,128,127,0,10,0,32},
            {(double)123456789123456.0, (double)0.123456789123456, (double)1.23456789123456, (double)123456789123456.0, (double)0.123456789123456, (double)1.23456789123456, (double)123456789123456.0, (double)123456789123456, (double)0.123456789123456, (double)1.23456789123456, (double)123456789123456.0, (double)12345.6789123456, (double)123456789123456.0, (double)1234567.89123456},
            {"123456789123456",         DOUBLE_FORMAT,             "1.23456789123456",       "123456789123456",         DOUBLE_FORMAT,             "1.23456789123456",       "123456789123456",         "123456789123456",       DOUBLE_FORMAT,             "1.23456789123456",       "123456789123456",         "12345.6789123456",       "123456789123456",         "1234567.89123456"}
        },
        {SQL_SUCCESS, 
            "--",
            {18,18,18,19,19,19,128,64,128,128,18,19,128,64},
            {0,18,17,0,19,18,0,0,128,127,0,10,0,32},
            {(double)-123456789123456.0, (double)-0.123456789123456, (double)-1.23456789123456, (double)-123456789123456.0, (double)-0.123456789123456, (double)-1.23456789123456, (double)-123456789123456.0, (double)-123456789123456, (double)-0.123456789123456, (double)-1.23456789123456, (double)-123456789123456.0, (double)-12345.6789123456, (double)-123456789123456.0, (double)-1234567.89123456},
            {"-123456789123456",         DOUBLE_FORMAT_N,            "-1.23456789123456",       "-123456789123456",         DOUBLE_FORMAT_N,            "-1.23456789123456",       "-123456789123456",         "-123456789123456",       DOUBLE_FORMAT_N,            "-1.23456789123456",       "-123456789123456",         "-12345.6789123456",       "-123456789123456",         "-1234567.89123456"}
        },
        {SQL_SUCCESS, 
            "--",
            {18,18,18,19,19,19,128,64,128,128,18,19,128,64},
            {0,18,17,0,19,18,0,0,128,127,0,10,0,32},
            {(double)123456789123456.0, (double)0.123456789123456, (double)1.23456789123456, (double)123456789123456.0, (double)0.123456789123456, (double)1.23456789123456, (double)123456789123456.0, (double)123456789123456, (double)0.123456789123456, (double)1.23456789123456, (double)123456789123456.0, (double)12345.6789123456, (double)123456789123456.0, (double)1234567.89123456},
            {"123456789123456",         DOUBLE_FORMAT,             "1.23456789123456",       "123456789123456",         DOUBLE_FORMAT,             "1.23456789123456",       "123456789123456",         "123456789123456",       DOUBLE_FORMAT,             "1.23456789123456",       "123456789123456",         "12345.6789123456",       "123456789123456",         "1234567.89123456"}
        },
        {SQL_SUCCESS, 
            "--",
            {19,19,19,19,19,128,128,19,19,19,19,19,128,128},
            {0,1,2,18,19,0,128,0,1,2,18,19,0,128},
            {(double)-123456789123456.0, (double)-123456789123.456, (double)-123456789123.456, (double)-1.23456789123456, (double)-0.123456789123456, (double)-123456789123456.0, (double)-0.123456789123456, (double)123456789123456.0, (double)123456789123.456, (double)123456789123.456, (double)1.23456789123456, (double)0.123456789123456, (double)123456789123456.0, (double)0.123456789123456},
            {"-123456789123456",         "-123456789123.4",         "-123456789123.45",        "-1.23456789123456",       DOUBLE_FORMAT_N,            "-123456789123456",         DOUBLE_FORMAT_N,            "123456789123456",         "123456789123.4",         "123456789123.45",        "1.23456789123456",       DOUBLE_FORMAT,             "123456789123456",         DOUBLE_FORMAT}
        },
		{SQL_ERROR, 
            "--",
            {19,19,19,19,19,128,128,19,19,19,19,19,128,128},
            {0,1,2,18,19,0,128,0,1,2,18,19,0,128},
            {(double)-1.2345678901234567E+19, (double)-123456789123.456, (double)-123456789123.456, (double)-1.23456789123456, (double)-0.123456789123456, (double)-123456789123456.0, (double)-0.123456789123456, (double)123456789123456.0, (double)123456789123.456, (double)123456789123.456, (double)1.23456789123456, (double)0.123456789123456, (double)123456789123456.0, (double)0.123456789123456},
            {"-1.2345678901234567E+19",         "-123456789123.4",         "-123456789123.45",        "-1.23456789123456",       DOUBLE_FORMAT_N,            "-123456789123456",         DOUBLE_FORMAT_N,            "123456789123456",         "123456789123.4",         "123456789123.45",        "1.23456789123456",       DOUBLE_FORMAT,             "123456789123456",         DOUBLE_FORMAT}
        },
        {999,
        }
    };

    struct {
        char *DrpTab;
        char *DelTab;
        char *CrtTab;
        char *InsTab;
        char *SelTab;
    } SQLStmt[10];

//===========================================================================================================
	struct
	{
		SQLSMALLINT SQLType;
		RETCODE		PassFail;
		RETCODE		PassFail1;
		char		*CrtCol;
		SQLUINTEGER	ColPrec;
		SQLSMALLINT	ColScale;
		char		*CharValue;
		SFLOAT		FloatValue;
		SDOUBLE		DoubleValue;
		char		*OutputValue;
	} CDataValueTOSQL9[] = 
		{
			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS, " NUMERIC (8,0)) NO PARTITION",8,0, "1", (float)1, 1, "1"},
			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS, " NUMERIC (8,0) UNSIGNED) NO PARTITION",8,0, "1", (float)1, 1, "1"},
			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS, " NUMERIC (19,0)) NO PARTITION",19,0, "1", (float)1, 1, "1"},
			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS, " NUMERIC (19,0) UNSIGNED) NO PARTITION",19,0, "1", (float)1, 1, "1"},
			{SQL_DECIMAL, SQL_SUCCESS, SQL_SUCCESS, " DECIMAL (8,0)) NO PARTITION",8,0, "1", (float)1, 1, "1"},
			{SQL_DECIMAL, SQL_SUCCESS, SQL_SUCCESS, " DECIMAL (8,0) UNSIGNED) NO PARTITION",8,0, "1", (float)1, 1, "1"},

			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS, " NUMERIC (8,0)) NO PARTITION",8,0, "1.00", (float)1.00, 1.00, "1"},
			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS, " NUMERIC (8,0) UNSIGNED) NO PARTITION",8,0, "1.00", (float)1.00, 1.00, "1"},
			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS, " NUMERIC (19,0)) NO PARTITION",19,0, "1.00", (float)1.00, 1.00, "1"},
			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS, " NUMERIC (19,0) UNSIGNED) NO PARTITION",19,0, "1.00", (float)1.00, 1.00, "1"},
			{SQL_DECIMAL, SQL_SUCCESS, SQL_SUCCESS, " DECIMAL (8,0)) NO PARTITION",8,0, "1.00", (float)1.00, 1.00, "1"},
			{SQL_DECIMAL, SQL_SUCCESS, SQL_SUCCESS, " DECIMAL (8,0) UNSIGNED) NO PARTITION",8,0, "1.00", (float)1.00, 1.00, "1"},

			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (8,1)) NO PARTITION",8,1,"2.00071", (float)2.00071, 2.00071, "2.0"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (8,1) UNSIGNED) NO PARTITION",8,1,"2.00071", (float)2.00071, 2.00071, "2.0"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (19,1)) NO PARTITION",19,1,"2.00071", (float)2.00071, 2.00071, "2.0"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (19,1) UNSIGNED) NO PARTITION",19,1,"2.00071", (float)2.00071, 2.00071, "2.0"},
			{SQL_DECIMAL, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " DECIMAL (8,1)) NO PARTITION",8,1,"2.00071", (float)2.00071, 2.00071, "2.0"},
			{SQL_DECIMAL, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " DECIMAL (8,1) UNSIGNED) NO PARTITION",8,1,"2.00071", (float)2.00071, 2.00071, "2.0"},

			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (8,2)) NO PARTITION",8,2,"2.05671", (float)2.05671, 2.05671, "2.05"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (8,2) UNSIGNED) NO PARTITION",8,2,"2.05671", (float)2.05671, 2.05671, "2.05"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (19,2)) NO PARTITION",19,2,"2.05671", (float)2.05671, 2.05671, "2.05"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (19,2) UNSIGNED) NO PARTITION",19,2,"2.05671", (float)2.05671, 2.05671, "2.05"},
			{SQL_DECIMAL, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " DECIMAL (8,2)) NO PARTITION",8,2,"2.05471", (float)2.05471, 2.05471, "2.05"},
			{SQL_DECIMAL, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " DECIMAL (8,2) UNSIGNED) NO PARTITION",8,2,"2.05471", (float)2.05471, 2.05471, "2.05"},

			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS," NUMERIC (8,5)) NO PARTITION",8,5, "2.00071", (float)2.00071, 2.00071, "2.00071"},
			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS," NUMERIC (8,5) UNSIGNED) NO PARTITION",8,5, "2.00071", (float)2.00071, 2.00071, "2.00071"},
			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS," NUMERIC (19,5)) NO PARTITION",19,5, "2.00071", (float)2.00071, 2.00071, "2.00071"},
			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS," NUMERIC (19,5) UNSIGNED) NO PARTITION",19,5, "2.00071", (float)2.00071, 2.00071, "2.00071"},
			{SQL_DECIMAL, SQL_SUCCESS, SQL_SUCCESS," DECIMAL (8,5)) NO PARTITION",8,5, "2.00071", (float)2.00071, 2.00071, "2.00071"},
			{SQL_DECIMAL, SQL_SUCCESS, SQL_SUCCESS," DECIMAL (8,5) UNSIGNED) NO PARTITION",8,5, "2.00071", (float)2.00071, 2.00071, "2.00071"},

			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (8,5)) NO PARTITION",8,5, "2.0000071", (float)2.0000071, 2.0000071, "2.00000"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (8,5) UNSIGNED) NO PARTITION",8,5, "2.0000071", (float)2.0000071, 2.0000071, "2.00000"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (19,5)) NO PARTITION",19,5, "2.0000071", (float)2.0000071, 2.0000071, "2.00000"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (19,5) UNSIGNED) NO PARTITION",19,5, "2.0000071", (float)2.0000071, 2.0000071, "2.00000"},
			{SQL_DECIMAL, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " DECIMAL (8,5)) NO PARTITION",8,5, "2.0000041", (float)2.0000041, 2.0000041, "2.00000"},
			{SQL_DECIMAL, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " DECIMAL (8,5) UNSIGNED) NO PARTITION",8,5, "2.0000041", (float)2.0000041, 2.0000041, "2.00000"},

			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (8,5)) NO PARTITION",8,5, "2.0000719", (float)2.0000719, 2.0000719, "2.00007"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (8,5) UNSIGNED) NO PARTITION",8,5, "2.0000719", (float)2.0000719, 2.0000719, "2.00007"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (19,5)) NO PARTITION",19,5, "2.0000719", (float)2.0000719, 2.0000719, "2.00007"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (19,5) UNSIGNED) NO PARTITION",19,5, "2.0000719", (float)2.0000719, 2.0000719, "2.00007"},
			{SQL_DECIMAL, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " DECIMAL (8,5)) NO PARTITION",8,5, "2.0000719", (float)2.0000719, 2.0000719, "2.00007"},
			{SQL_DECIMAL, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " DECIMAL (8,5) UNSIGNED) NO PARTITION",8,5, "2.0000719", (float)2.0000719, 2.0000719, "2.00007"},

			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (8,5)) NO PARTITION",8,5, "2.2000719", (float)2.2000719, 2.2000719, "2.20007"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (8,5) UNSIGNED) NO PARTITION",8,5, "2.2000719", (float)2.2000719, 2.2000719, "2.20007"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (19,5)) NO PARTITION",19,5, "2.2000719", (float)2.2000719, 2.2000719, "2.20007"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (19,5) UNSIGNED) NO PARTITION",19,5, "2.2000719", (float)2.2000719, 2.2000719, "2.20007"},
			{SQL_DECIMAL, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " DECIMAL (8,5)) NO PARTITION",8,5, "2.2000719", (float)2.2000719, 2.2000719, "2.20007"},
			{SQL_DECIMAL, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " DECIMAL (8,5) UNSIGNED) NO PARTITION",8,5, "2.2000719", (float)2.2000719, 2.2000719, "2.20007"},

			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (8,5)) NO PARTITION",8,5, "2.2000019", (float)2.2000019, 2.2000019, "2.20000"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (8,5) UNSIGNED) NO PARTITION",8,5, "2.2000019", (float)2.2000019, 2.2000019,"2.20000"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (19,5)) NO PARTITION",19,5, "2.2000019", (float)2.2000019, 2.2000019,"2.20000"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " NUMERIC (19,5) UNSIGNED) NO PARTITION",19,5, "2.2000019", (float)2.2000019, 2.2000019,"2.20000"},
			{SQL_DECIMAL, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " DECIMAL (8,5)) NO PARTITION",8,5, "2.2000019", (float)2.2000019, 2.2000019,"2.20000"},
			{SQL_DECIMAL, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS, " DECIMAL (8,5) UNSIGNED) NO PARTITION",8,5, "2.2000019", (float)2.2000019, 2.2000019,"2.20000"},

			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS, " NUMERIC (8,8)) NO PARTITION",8,8, "0.1234567", (float)0.1234567, 0.1234567, "0.12345670"},
			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS, " NUMERIC (8,8) UNSIGNED) NO PARTITION",8,8, "0.1234567", (float)0.1234567, 0.1234567, "0.12345670"},
			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS, " NUMERIC (19,8)) NO PARTITION",19,8, "0.1234567", (float)0.1234567, 0.1234567, "0.12345670"},
			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS, " NUMERIC (19,8) UNSIGNED) NO PARTITION",19,8, "0.1234567", (float)0.1234567, 0.1234567, "0.12345670"},
			{SQL_DECIMAL, SQL_SUCCESS, SQL_SUCCESS, " DECIMAL (8,8)) NO PARTITION",8,8, "0.123456", (float)0.123456, 0.123456, "0.12345600"},
			{SQL_DECIMAL, SQL_SUCCESS, SQL_SUCCESS, " DECIMAL (8,8) UNSIGNED) NO PARTITION",8,8, "0.123456", (float)0.123456, 0.123456, "0.12345600"},

			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS, " NUMERIC (8,8)) NO PARTITION",8,8, "0.01234567", (float)0.01234567, 0.01234567, "0.01234567"},
			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS, " NUMERIC (8,8) UNSIGNED) NO PARTITION",8,8, "0.01234567", (float)0.01234567, 0.01234567, "0.01234567"},
			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS, " NUMERIC (19,8)) NO PARTITION",19,8, "0.01234567", (float)0.01234567, 0.01234567, "0.01234567"},
			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS, " NUMERIC (19,8) UNSIGNED) NO PARTITION",19,8, "0.01234567", (float)0.01234567, 0.01234567, "0.01234567"},
			{SQL_DECIMAL, SQL_SUCCESS, SQL_SUCCESS, " DECIMAL (8,8)) NO PARTITION",8,8, "0.0123456", (float)0.0123456, 0.0123456, "0.01234560"},
			{SQL_DECIMAL, SQL_SUCCESS, SQL_SUCCESS, " DECIMAL (8,8) UNSIGNED) NO PARTITION",8,8, "0.0123456", (float)0.0123456, 0.0123456, "0.01234560"},

			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS," NUMERIC (8,8)) NO PARTITION",8,8, "0.0123456789", (float)0.0123456789, 0.0123456789, "0.01234567"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS," NUMERIC (8,8) UNSIGNED) NO PARTITION",8,8, "0.0123456789", (float)0.0123456789, 0.0123456789, "0.01234567"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS," NUMERIC (19,8)) NO PARTITION",19,8, "0.0123456789", (float)0.0123456789, 0.0123456789, "0.01234567"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS," NUMERIC (19,8) UNSIGNED) NO PARTITION",19,8, "0.0123456789", (float)0.0123456789, 0.0123456789, "0.01234567"},
			{SQL_DECIMAL, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS," DECIMAL (8,8)) NO PARTITION",8,8, "0.0123456789", (float)0.0123456789, 0.0123456789, "0.01234567"},
			{SQL_DECIMAL, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS," DECIMAL (8,8) UNSIGNED) NO PARTITION",8,8, "0.0123456789", (float)0.0123456789, 0.0123456789, "0.01234567"},

			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS," NUMERIC (8,8)) NO PARTITION",8,8, "0.00000005", (float)0.00000005, 0.00000005, "0.00000005"},
			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS," NUMERIC (8,8) UNSIGNED) NO PARTITION",8,8, "0.00000005", (float)0.00000005, 0.00000005, "0.00000005"},
			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS," NUMERIC (19,8)) NO PARTITION",19,8, "0.00000005", (float)0.00000005, 0.00000005, "0.00000005"},
			{SQL_NUMERIC, SQL_SUCCESS, SQL_SUCCESS," NUMERIC (19,8) UNSIGNED) NO PARTITION",19,8, "0.00000005", (float)0.00000005, 0.00000005, "0.00000005"},
			{SQL_DECIMAL, SQL_SUCCESS, SQL_SUCCESS," DECIMAL (8,8)) NO PARTITION",8,8, "0.00000005", (float)0.00000005, 0.00000005, "0.00000005"},
			{SQL_DECIMAL, SQL_SUCCESS, SQL_SUCCESS," DECIMAL (8,8) UNSIGNED) NO PARTITION",8,8, "0.00000005", (float)0.00000005, 0.00000005, "0.00000005"},

			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS," NUMERIC (8,8)) NO PARTITION",8,8, "0.000000005", (float)0.000000005, 0.000000005, "0.00000000"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS," NUMERIC (8,8) UNSIGNED) NO PARTITION",8,8, "0.000000005", (float)0.000000005, 0.000000005, "0.00000000"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS," NUMERIC (19,8)) NO PARTITION",19,8, "0.000000005", (float)0.000000005, 0.000000005, "0.00000000"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS," NUMERIC (19,8) UNSIGNED) NO PARTITION",19,8, "0.000000005", (float)0.000000005, 0.000000005, "0.00000000"},
			{SQL_DECIMAL, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS," DECIMAL (8,8)) NO PARTITION",8,8, "0.000000005", (float)0.000000005, 0.000000005, "0.00000000"},
			{SQL_DECIMAL, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS," DECIMAL (8,8) UNSIGNED) NO PARTITION",8,8, "0.000000005", (float)0.000000005, 0.000000005, "0.00000000"},

			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS," NUMERIC (8,8)) NO PARTITION",8,8, "0.000000789", (float)0.000000789, 0.000000789, "0.00000078"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS," NUMERIC (8,8) UNSIGNED) NO PARTITION",8,8, "0.000000789", (float)0.000000789, 0.000000789, "0.00000078"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS," NUMERIC (19,8)) NO PARTITION",19,8, "0.000000789", (float)0.000000789, 0.000000789, "0.00000078"},
			{SQL_NUMERIC, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS," NUMERIC (19,8) UNSIGNED) NO PARTITION",19,8, "0.000000789", (float)0.000000789, 0.000000789, "0.00000078"},
			{SQL_DECIMAL, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS," DECIMAL (8,8)) NO PARTITION",8,8, "0.000000789", (float)0.000000789, 0.000000789, "0.00000078"},
			{SQL_DECIMAL, SQL_SUCCESS_WITH_INFO, SQL_SUCCESS," DECIMAL (8,8) UNSIGNED) NO PARTITION",8,8, "0.000000789", (float)0.000000789, 0.000000789, "0.00000078"},

			//Negative tests
			{SQL_NUMERIC, SQL_ERROR, SQL_SUCCESS, " NUMERIC (8,0)) NO PARTITION",8,0, "-1a  ", (float)-1, -1, "-1"},
			{SQL_NUMERIC, SQL_ERROR, SQL_ERROR, " NUMERIC (8,0) UNSIGNED) NO PARTITION",8,1, "-1.00071", (float)-1.00071, -1.00071, "1234.56789"},
			{SQL_NUMERIC, SQL_ERROR, SQL_SUCCESS, " NUMERIC (19,0)) NO PARTITION",19,0, "-1a  ", (float)-1, -1, "-1"},
			{SQL_NUMERIC, SQL_ERROR, SQL_ERROR, " NUMERIC (19,0) UNSIGNED) NO PARTITION",19,1, "-1.00071", (float)-1.00071, -1.00071, "1234.56789"},
			{SQL_DECIMAL, SQL_ERROR, SQL_SUCCESS, " DECIMAL (8,0)) NO PARTITION",8,0, "-1a  ", (float)-1, -1, "-1"},
			{SQL_DECIMAL, SQL_ERROR, SQL_ERROR, " DECIMAL (8,0) UNSIGNED) NO PARTITION",8,1, "-1.00071", (float)-1.00071, -1.00071, "1234.56789"},

			{SQL_NUMERIC, SQL_ERROR, SQL_ERROR, " NUMERIC (8,4)) NO PARTITION",8,4, "-3a.00071", (float)-12345.00071, -12345.00071, "-12345.00071"},
			{SQL_NUMERIC, SQL_ERROR, SQL_ERROR, " NUMERIC (8,4) UNSIGNED) NO PARTITION",8,4, "-0.00071", (float)-1.00071, -1.00071, "-1.00070"},
			{SQL_NUMERIC, SQL_ERROR, SQL_SUCCESS, " NUMERIC (19,4)) NO PARTITION",19,4, "-3a.00071", (float)-1.00071, -1.00071, "-1.00070"},
			{SQL_NUMERIC, SQL_ERROR, SQL_ERROR, " NUMERIC (19,4) UNSIGNED) NO PARTITION",19,4, "-0.00071", (float)-1.00071, -1.00071, "-1.00070"},
			{SQL_DECIMAL, SQL_ERROR, SQL_ERROR, " DECIMAL (8,4)) NO PARTITION",8,4, "-3a.00071", (float)-12345.00071, -12345.00071, "-12345.00071"},
			{SQL_DECIMAL, SQL_ERROR, SQL_ERROR, " DECIMAL (8,4) UNSIGNED) NO PARTITION",8,4, "-0.00071", (float)-1.00071, -1.00071, "-1.00070"},

			{SQL_NUMERIC, SQL_ERROR, SQL_ERROR, " NUMERIC (8,8)) NO PARTITION",8,8, "-3.00071", (float)-3.00071, -3.00071, "1234.56789"},
			{SQL_NUMERIC, SQL_ERROR, SQL_ERROR, " NUMERIC (8,8) UNSIGNED) NO PARTITION",8,8, "-0.00071", (float)-1.00071, -1.00071, "1234.56789"},
			{SQL_NUMERIC, SQL_ERROR, SQL_ERROR, " NUMERIC (19,19)) NO PARTITION",19,19, "-3.00071", (float)-3.00071, -3.00071, "1234.56789"},
			{SQL_NUMERIC, SQL_ERROR, SQL_ERROR, " NUMERIC (19,19) UNSIGNED) NO PARTITION",19,19, "-0.00071", (float)-1.00071, -1.00071, "1234.56789"},
			{SQL_DECIMAL, SQL_ERROR, SQL_ERROR, " DECIMAL (8,8)) NO PARTITION",8,8, "-3.00071", (float)-3.00071, -3.00071, "1234.56789"},
			{SQL_DECIMAL, SQL_ERROR, SQL_ERROR, " DECIMAL (8,8) UNSIGNED) NO PARTITION",8,8, "-0.00071", (float)-1.00071, -1.00071, "1234.56789"},

			{SQL_NUMERIC, SQL_ERROR, SQL_ERROR, " NUMERIC (8,8)) NO PARTITION",8,8, "0.000.71", (float)-3.00071, -3.00071, "1234.56789"},
			{SQL_NUMERIC, SQL_ERROR, SQL_ERROR, " NUMERIC (8,8) UNSIGNED) NO PARTITION",8,8, "0.000.71", (float)-3.00071, -3.00071, "1234.56789"},
			{SQL_NUMERIC, SQL_ERROR, SQL_ERROR, " NUMERIC (19,19)) NO PARTITION",19,19, "0.000.71", (float)-3.00071, -3.00071, "1234.56789"},
			{SQL_NUMERIC, SQL_ERROR, SQL_ERROR, " NUMERIC (19,19) UNSIGNED) NO PARTITION",19,19, "0.000.71", (float)-3.00071, -3.00071, "1234.56789"},
			{SQL_DECIMAL, SQL_ERROR, SQL_ERROR, " DECIMAL (8,8)) NO PARTITION",8,8, "0.000.71", (float)-3.00071, -3.00071, "1234.56789"},
			{SQL_DECIMAL, SQL_ERROR, SQL_ERROR, " DECIMAL (8,8) UNSIGNED) NO PARTITION",8,8, "0.000.71", (float)-3.00071, -3.00071, "1234.56789"},

			{SQL_NUMERIC, SQL_ERROR, SQL_ERROR, " NUMERIC (8,8)) NO PARTITION",8,8, "0.00071a", (float)-3.00071, -3.00071, "1234.56789"},
			{SQL_NUMERIC, SQL_ERROR, SQL_ERROR, " NUMERIC (8,8) UNSIGNED) NO PARTITION",8,8, "3.00071", (float)3.00071, 3.00071, "1234.56789"},
			{SQL_NUMERIC, SQL_ERROR, SQL_ERROR, " NUMERIC (19,19)) NO PARTITION",19,19, "0.00071a", (float)-3.00071, -3.00071, "1234.56789"},
			{SQL_NUMERIC, SQL_ERROR, SQL_ERROR, " NUMERIC (19,19) UNSIGNED) NO PARTITION",19,19, "3.00071", (float)3.00071, 3.00071, "1234.56789"},
			{SQL_DECIMAL, SQL_ERROR, SQL_ERROR, " DECIMAL (8,8)) NO PARTITION",8,8, "0.00071a", (float)-3.00071, -3.00071, "1234.56789"},
			{SQL_DECIMAL, SQL_ERROR, SQL_ERROR, " DECIMAL (8,8) UNSIGNED) NO PARTITION",8,8, "3.00071", (float)3.00071, 3.00071, "1234.56789"},

			{	999,
			}
		};

    char* ColName1;

	//===========================================================================================================
	// Negative tests to convert all CTypes -> SQL_NUMERIC
    char                    *NColDef = "NUMERIC(19,0)) NO PARTITION";
	char					*WcharVal = "123";
	char					*BinaryVal = "1";
	unsigned char			BitVal = 1;
	short int				ShortVal = 1;
	unsigned short int		UShortVal = 1;
	int						LongVal = 123;
	unsigned int			ULongVal = 123;
	signed char				TinyIntVal = 1;
	unsigned char			UTinyIntVal = 1;
	long long int			BigIntVal = 123;
	unsigned long long int	UBigIntVal = 123;
	SQL_INTERVAL_STRUCT		IntevalVal;
	SQL_NUMERIC_STRUCT		NumericVal = {19,0,1,0xF9,0x20,0xD8,0x21,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00};

	SQLSMALLINT CTypeAll[] = {
        999,
		SQL_C_WCHAR,
		SQL_C_BINARY, SQL_C_BIT, 
		SQL_C_SHORT, SQL_C_SSHORT, SQL_C_USHORT,
		SQL_C_LONG, SQL_C_SLONG, SQL_C_ULONG,
		SQL_C_TINYINT, SQL_C_STINYINT, SQL_C_UTINYINT,
		SQL_C_SBIGINT, SQL_C_UBIGINT,
		//SQL_C_NUMERIC, 
		SQL_C_DATE, SQL_C_TIME, SQL_C_TIMESTAMP,
		SQL_C_TYPE_DATE, SQL_C_TYPE_TIME, SQL_C_TYPE_TIMESTAMP,
		SQL_C_INTERVAL_DAY, SQL_C_INTERVAL_DAY_TO_HOUR, SQL_C_INTERVAL_DAY_TO_MINUTE, SQL_C_INTERVAL_DAY_TO_SECOND,
		SQL_C_INTERVAL_HOUR, SQL_C_INTERVAL_HOUR_TO_MINUTE, SQL_C_INTERVAL_HOUR_TO_SECOND,
		SQL_C_INTERVAL_MINUTE, SQL_C_INTERVAL_MINUTE_TO_SECOND, SQL_C_INTERVAL_SECOND,
		SQL_C_INTERVAL_MONTH, SQL_C_INTERVAL_YEAR, SQL_C_INTERVAL_YEAR_TO_MONTH,
		999
	};

	//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLBindParam30", charset_file);
    if (var_list == NULL) return FAILED;

    for(i=0;i<10;i++) {
        sprintf(temp,"SQLBindParam30_DrpTab_%d",i);
        SQLStmt[i].DrpTab = var_mapping(temp, var_list);
        sprintf(temp,"SQLBindParam30_DelTab_%d",i);
        SQLStmt[i].DelTab = var_mapping(temp, var_list);
        sprintf(temp,"SQLBindParam30_CrtTab_%d",i);
	    SQLStmt[i].CrtTab = var_mapping(temp, var_list);
        sprintf(temp,"SQLBindParam30_InsTab_%d",i);
	    SQLStmt[i].InsTab = var_mapping(temp, var_list);
        sprintf(temp,"SQLBindParam30_SelTab_%d",i);
	    SQLStmt[i].SelTab = var_mapping(temp, var_list);
    }

    i = 0;
    while(CDataValueTOSQL1[i].CType != 999) {
        sprintf(temp,"SQLBindParam30_CDataValueTOSQL1_CrtCol_%d",i);
        CDataValueTOSQL1[i].CrtCol = var_mapping(temp, var_list);
        if(i != 4 && i != 5) {
            sprintf(temp,"SQLBindParam30_CDataValueTOSQL1_OutputValue0_%d",i);
	        CDataValueTOSQL1[i].OutputValue[0] = var_mapping(temp, var_list);
            sprintf(temp,"SQLBindParam30_CDataValueTOSQL1_OutputValue1_%d",i);
	        CDataValueTOSQL1[i].OutputValue[1] = var_mapping(temp, var_list);
            sprintf(temp,"SQLBindParam30_CDataValueTOSQL1_OutputValue12_%d",i);
	        CDataValueTOSQL1[i].OutputValue[12] = var_mapping(temp, var_list);
            sprintf(temp,"SQLBindParam30_CDataValueTOSQL1_OutputValue14_%d",i);
	        CDataValueTOSQL1[i].OutputValue[14] = var_mapping(temp, var_list);
            sprintf(temp,"SQLBindParam30_CDataValueTOSQL1_OutputValue15_%d",i);
	        CDataValueTOSQL1[i].OutputValue[15] = var_mapping(temp, var_list);
            sprintf(temp,"SQLBindParam30_CDataValueTOSQL1_OutputValue16_%d",i);
	        CDataValueTOSQL1[i].OutputValue[16] = var_mapping(temp, var_list);
        }
        i++;
    }
	
    i = 0;
    while(CDataValueTOSQL5[i].CType != 999) {
        sprintf(temp,"SQLBindParam30_CDataValueTOSQL5_CrtCol_%d",i);
        CDataValueTOSQL5[i].CrtCol = var_mapping(temp, var_list);
        sprintf(temp,"SQLBindParam30_CDataValueTOSQL5_CharValue_%d",i);
	    CDataValueTOSQL5[i].CharValue = var_mapping(temp, var_list);
        CDataValueTOSQL5[i].OutputValue[0] = var_mapping(temp, var_list);
        sprintf(temp,"SQLBindParam30_CDataValueTOSQL5_VarCharValue_%d",i);
	    CDataValueTOSQL5[i].VarCharValue = var_mapping(temp, var_list);
        CDataValueTOSQL5[i].OutputValue[1] = var_mapping(temp, var_list);
        sprintf(temp,"SQLBindParam30_CDataValueTOSQL5_LongVarCharValue_%d",i);
	    CDataValueTOSQL5[i].LongVarCharValue = var_mapping(temp, var_list);
        CDataValueTOSQL5[i].OutputValue[12] = var_mapping(temp, var_list);
        sprintf(temp,"SQLBindParam30_CDataValueTOSQL5_NCharValue_%d",i);
	    CDataValueTOSQL5[i].NCharValue = var_mapping(temp, var_list);
        CDataValueTOSQL5[i].OutputValue[14] = var_mapping(temp, var_list);
        sprintf(temp,"SQLBindParam30_CDataValueTOSQL5_NVarCharValue_%d",i);
	    CDataValueTOSQL5[i].NVarCharValue = var_mapping(temp, var_list);
        CDataValueTOSQL5[i].OutputValue[15] = var_mapping(temp, var_list);
        sprintf(temp,"SQLBindParam30_CDataValueTOSQL5_NLongVarCharValue_%d",i);
	    CDataValueTOSQL5[i].NLongVarCharValue = var_mapping(temp, var_list);
        CDataValueTOSQL5[i].OutputValue[16] = var_mapping(temp, var_list);
        i++;
    }

	CDataValueTOSQL6[0].CrtCol = var_mapping("SQLBindParam30_CDataValueTOSQL6_CrtCol_0", var_list);
	CDataValueTOSQL6[0].OutputValue[0] = var_mapping("SQLBindParam30_CDataValueTOSQL6_OutputValue0_0", var_list);
	CDataValueTOSQL6[0].OutputValue[1] = var_mapping("SQLBindParam30_CDataValueTOSQL6_OutputValue1_0", var_list);
	CDataValueTOSQL6[0].OutputValue[9] = var_mapping("SQLBindParam30_CDataValueTOSQL6_OutputValue9_0", var_list);

	CDataValueTOSQL6[1].CrtCol = var_mapping("SQLBindParam30_CDataValueTOSQL6_CrtCol_1", var_list);
	CDataValueTOSQL6[1].OutputValue[0] = var_mapping("SQLBindParam30_CDataValueTOSQL6_OutputValue0_1", var_list);
	CDataValueTOSQL6[1].OutputValue[1] = var_mapping("SQLBindParam30_CDataValueTOSQL6_OutputValue1_1", var_list);
	CDataValueTOSQL6[1].OutputValue[9] = var_mapping("SQLBindParam30_CDataValueTOSQL6_OutputValue9_1", var_list);

	CDataValueTOSQL6[2].CrtCol = var_mapping("SQLBindParam30_CDataValueTOSQL6_CrtCol_2", var_list);
	CDataValueTOSQL6[2].OutputValue[0] = var_mapping("SQLBindParam30_CDataValueTOSQL6_OutputValue0_2", var_list);
	CDataValueTOSQL6[2].OutputValue[1] = var_mapping("SQLBindParam30_CDataValueTOSQL6_OutputValue1_2", var_list);
	CDataValueTOSQL6[2].OutputValue[9] = var_mapping("SQLBindParam30_CDataValueTOSQL6_OutputValue9_2", var_list);


    i = 0;
    while(CDataValueTOSQL8[i].CType != 999) {
        sprintf(temp,"SQLBindParam30_CDataValueTOSQL8_CrtCol_%d",i);
        CDataValueTOSQL8[i].CrtCol = var_mapping(temp, var_list);
        sprintf(temp,"SQLBindParam30_CDataValueTOSQL8_CharValue_%d",i);
	    CDataValueTOSQL8[i].CharValue = var_mapping(temp, var_list);
        CDataValueTOSQL8[i].OutputValue[0] = var_mapping(temp, var_list);
        sprintf(temp,"SQLBindParam30_CDataValueTOSQL8_VarCharValue_%d",i);
	    CDataValueTOSQL8[i].VarCharValue = var_mapping(temp, var_list);
        CDataValueTOSQL8[i].OutputValue[1] = var_mapping(temp, var_list);
        sprintf(temp,"SQLBindParam30_CDataValueTOSQL8_LongVarCharValue_%d",i);
	    CDataValueTOSQL8[i].LongVarCharValue = var_mapping(temp, var_list);
        CDataValueTOSQL8[i].OutputValue[12] = var_mapping(temp, var_list);
        sprintf(temp,"SQLBindParam30_CDataValueTOSQL8_NCharValue_%d",i);
	    CDataValueTOSQL8[i].NCharValue = var_mapping(temp, var_list);
        CDataValueTOSQL8[i].OutputValue[14] = var_mapping(temp, var_list);
        sprintf(temp,"SQLBindParam30_CDataValueTOSQL8_NVarCharValue_%d",i);
	    CDataValueTOSQL8[i].NVarCharValue = var_mapping(temp, var_list);
        CDataValueTOSQL8[i].OutputValue[15] = var_mapping(temp, var_list);
        sprintf(temp,"SQLBindParam30_CDataValueTOSQL8_NLongVarCharValue_%d",i);
	    CDataValueTOSQL8[i].NLongVarCharValue = var_mapping(temp, var_list);
        CDataValueTOSQL8[i].OutputValue[16] = var_mapping(temp, var_list);
        i++;
    }

	CFloatToNumeric[0].CrtCol = var_mapping("SQLBindParam30_CFloatToNumeric_0", var_list);
	CFloatToNumeric[1].CrtCol = var_mapping("SQLBindParam30_CFloatToNumeric_1", var_list);
	CFloatToNumeric[2].CrtCol = var_mapping("SQLBindParam30_CFloatToNumeric_2", var_list);
	CFloatToNumeric[3].CrtCol = var_mapping("SQLBindParam30_CFloatToNumeric_3", var_list);
	CFloatToNumeric[4].CrtCol = var_mapping("SQLBindParam30_CFloatToNumeric_4", var_list);

	CDoubleToNumeric[0].CrtCol = var_mapping("SQLBindParam30_CDoubleToNumeric_0", var_list);
	CDoubleToNumeric[1].CrtCol = var_mapping("SQLBindParam30_CDoubleToNumeric_1", var_list);
	CDoubleToNumeric[2].CrtCol = var_mapping("SQLBindParam30_CDoubleToNumeric_2", var_list);
	CDoubleToNumeric[3].CrtCol = var_mapping("SQLBindParam30_CDoubleToNumeric_3", var_list);
	CDoubleToNumeric[4].CrtCol = var_mapping("SQLBindParam30_CDoubleToNumeric_4", var_list);

    ColName1 = var_mapping("SQLBindParam30_ColName1", var_list);

//=============================================================================================
// Initialization Test Case

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API => MX Specific SQLBindParameter | SQLBindParameter30 | sqlbindparameterver3.c\n");

	TEST_INIT;

	TESTCASE_BEGIN("Conncetion for SQLBindParameter tests\n");
	TESTCASE_BEGIN("SQLBindParameter Ver3\n");

	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,"Unable to connect\n");
		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;

	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);	
 	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect3(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	TESTCASE_END; 

	tempType = (char *)malloc(NAME_LEN);
	InsStr = (char *)malloc(MAX_NOS_SIZE);
	strcpy(tempType,"");
	strcpy(InsStr,"");

//=================================================================================================================
// Testing Section #1: converting from cchar to all 

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		i = 0;
		while (CDataValueTOSQL1[i].CType != 999)
		{
			// Creating table
			TESTCASE_BEGIN("Setup for SQLBindParameter tests to create table for SQL_C_CHAR.\n");
			
			SQLExecDirect(hstmt,(SQLCHAR*) SQLStmt[0].DrpTab,SQL_NTS);
			strcpy(InsStr,"");
			strcat(InsStr,SQLStmt[0].CrtTab);
			strcat(InsStr,CDataValueTOSQL1[i].CrtCol);
			//LogMsg(NONE, InsStr);
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
 			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				// Couldn't even create our table. Test must exit.
				LogAllErrorsVer3(henv,hdbc,hstmt);
				TestMXSQLBindParamaterVer3_Cleanup(hstmt,"",tempType,InsStr,pTestInfo);
				TEST_FAILED;
				TEST_RETURN;
			}
			TESTCASE_END; 

			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for prepare SQL_C_CHAR.\n");
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLPrepare(hstmt,(SQLCHAR*)SQLStmt[0].InsTab,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					// Quit tests since we can't even insert into the table.
					// Making sure we clean up our table.
					LogAllErrorsVer3(henv,hdbc,hstmt);
					TestMXSQLBindParamaterVer3_Cleanup(hstmt,SQLStmt[0].DrpTab,tempType,InsStr,pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END; 
			}

			for (j = 0; j < MAX_BINDPARAM1; j++)
			{
				sprintf(Heading,"SQLBindParameter from SQL_C_CHAR to %s.\n",SQLTypeToChar(CDataArgToSQL1.SQLType[j],tempType));
				TESTCASE_BEGIN(Heading);
				InValue = SQL_NTS;
				returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL1[i].CType,
																			CDataArgToSQL1.SQLType[j],CDataValueTOSQL1[i].ColPrec[j],
																			CDataValueTOSQL1[i].ColScale[j],CDataValueTOSQL1[i].OutputValue[j],NAME_LEN,
																			&InValue);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
		

			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for Execute SQL_C_CHAR.\n");
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecute(hstmt);         // Execute statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for ExecDirect SQL_C_CHAR.\n");
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[0].InsTab,SQL_NTS);        // ExecDirect statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}

			if (returncode == SQL_SUCCESS)
			{
//				TESTCASE_BEGIN("Setup for checking SQLBindParameter tests\n");
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[0].SelTab,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					else
					{
						for (j = 0; j < MAX_BINDPARAM1; j++)
						{
							OutValueLen = SQL_NTS;
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN*2,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
                                LogMsg(NONE,"SQLBindParameter test:checking data for column c%d\n",j+1);
								TEST_FAILED;
								LogAllErrorsVer3(henv,hdbc,hstmt);
							}
							else
							{
								if (_strnicmp(CDataValueTOSQL1[i].OutputValue[j],OutValue,strlen(CDataValueTOSQL1[i].OutputValue[j])) == 0)
								{
									//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueTOSQL1[i].OutputValue[j],OutValue);
								}	
								else
								{
                                    LogMsg(NONE,"SQLBindParameter test:checking data for column c%d\n",j+1);
									TEST_FAILED;	
									LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at line: %d\n",CDataValueTOSQL1[i].OutputValue[j],OutValue,__LINE__);
								}
							}
						} // end for loop
					}
				}
				TESTCASE_END;
			}
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			i++;
		}
	}
	SQLExecDirect(hstmt,(SQLCHAR*) SQLStmt[0].DrpTab,SQL_NTS);

//====================================================================================================
// Testing Section #2: converting from ctinyint, cshort and clong to sql 
	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		TESTCASE_BEGIN("Setup for SQLBindParameter tests for create table\n");
		
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].CrtTab,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			TestMXSQLBindParamaterVer3_Cleanup(hstmt,"",tempType,InsStr,pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}
		TESTCASE_END;

		i = 0;
		while (CDataValueTOSQL2[i].CType != 999)
		{
			for (k = 0 ; k < LOOP_BINDPARAM2; k++)
			{
				if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
				{
					sprintf(Heading,"Setup for SQLBindParameter tests for prepare %s.\n",CDataValueTOSQL2[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					returncode = SQLPrepare(hstmt,(SQLCHAR*)SQLStmt[1].InsTab,SQL_NTS);
 					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						TestMXSQLBindParamaterVer3_Cleanup(hstmt,SQLStmt[1].DrpTab,tempType,InsStr,pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}
					TESTCASE_END;
				}

				m = k*MAX_BINDPARAM2;
				for (j = 0; j < MAX_BINDPARAM2; j++)
				{
					sprintf(Heading,"Set up SQLBindParameter to convert from %s to %s\n",CDataValueTOSQL2[i].TestCType, CDataArgToSQL2.TestSQLType[j]);
					TESTCASE_BEGIN(Heading);
					
			
					switch (CDataValueTOSQL2[i].CType)
					{
						case SQL_C_STINYINT:
							returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL2[i].CType,
																					CDataArgToSQL2.SQLType[j],CDataArgToSQL2.ColPrec[j],
																					CDataArgToSQL2.ColScale[j],&(CDataTypeTOSQL2.CSTINTTOSQL[m]),0,
																					&InValue1);
							break;
						case SQL_C_UTINYINT:
							returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL2[i].CType,
																					CDataArgToSQL2.SQLType[j],CDataArgToSQL2.ColPrec[j],
																					CDataArgToSQL2.ColScale[j],&(CDataTypeTOSQL2.CUTINTTOSQL[m]),0,
																					&InValue1);
							break;
						case SQL_C_TINYINT:
							returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL2[i].CType,CDataArgToSQL2.SQLType[j],
                                                                                CDataArgToSQL2.ColPrec[j],CDataArgToSQL2.ColScale[j],
                                                                                &(CDataTypeTOSQL2.CTINTTOSQL[m]),0,&InValue1);
							break;
						case SQL_C_SSHORT:
							returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL2[i].CType,CDataArgToSQL2.SQLType[j],
																				CDataArgToSQL2.ColPrec[j],CDataArgToSQL2.ColScale[j],
																				&(CDataTypeTOSQL2.CSSHORTTOSQL[m]),0,&InValue1);
							break;
						case SQL_C_USHORT:
							returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL2[i].CType,CDataArgToSQL2.SQLType[j],
																				CDataArgToSQL2.ColPrec[j],CDataArgToSQL2.ColScale[j],
																				&(CDataTypeTOSQL2.CUSHORTTOSQL[m]),0,&InValue1);
							break;
						case SQL_C_SHORT:
							returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL2[i].CType,CDataArgToSQL2.SQLType[j],
																				CDataArgToSQL2.ColPrec[j],CDataArgToSQL2.ColScale[j],
																				&(CDataTypeTOSQL2.CSHORTTOSQL[m]),0,&InValue1);
							break;
						case SQL_C_SLONG:
							returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL2[i].CType,CDataArgToSQL2.SQLType[j],
																				CDataArgToSQL2.ColPrec[j],CDataArgToSQL2.ColScale[j],
																				&(CDataTypeTOSQL2.CSLONGTOSQL[m]),0,&InValue1);
							break;
						case SQL_C_ULONG:
							returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL2[i].CType,CDataArgToSQL2.SQLType[j],
																				CDataArgToSQL2.ColPrec[j],CDataArgToSQL2.ColScale[j],
																				&(CDataTypeTOSQL2.CULONGTOSQL[m]),0,&InValue1);
							break;
						case SQL_C_LONG:
							returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL2[i].CType,CDataArgToSQL2.SQLType[j],
																				CDataArgToSQL2.ColPrec[j],CDataArgToSQL2.ColScale[j],
																				&(CDataTypeTOSQL2.CLONGTOSQL[m]),0,&InValue1);
							break;
						default: ;
					}

					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					TESTCASE_END;
					m++;
				}
			
				if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
				{
					sprintf(Heading,"Setup for SQLBindParameter tests for Execute %s.\n",CDataValueTOSQL2[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					returncode = SQLExecute(hstmt);         // Execute statement with 
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					TESTCASE_END;
				}
				if (loop_bindparam == BINDPARAM_EXECDIRECT)
				{
					sprintf(Heading,"Setup for SQLBindParameter tests for ExecDirect %s.\n",CDataValueTOSQL2[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].InsTab,SQL_NTS);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					TESTCASE_END;
				}
				if(returncode == SQL_SUCCESS)
				{
					sprintf(Heading,"Setup for checking SQLBindParameter tests %s.\n",CDataValueTOSQL2[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].SelTab,SQL_NTS);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					else
					{
						returncode = SQLFetch(hstmt);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
						{
							TEST_FAILED;
							LogAllErrorsVer3(henv,hdbc,hstmt);
						}
						else
						{
							for (j = 0; j < MAX_BINDPARAM2; j++)
							{
								returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
								{
                                    LogMsg(NONE,"SQLBindParameter test: checking data for column c%d\n",j+1);
									TEST_FAILED;
									LogAllErrorsVer3(henv,hdbc,hstmt);
								}
								else
								{
									if (_strnicmp(CDataValueTOSQL2[i].OutputValue[j],OutValue,strlen(CDataValueTOSQL2[i].OutputValue[j])) == 0)
									{
										//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueTOSQL2[i].OutputValue[j],OutValue);
									}	
									else
									{
                                        LogMsg(NONE,"SQLBindParameter test: checking data for column c%d\n",j+1);
										TEST_FAILED;	
										LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched at line: %d\n",CDataValueTOSQL2[i].OutputValue[j],OutValue,__LINE__);
									}
								}
							} // end for loop
						}
					}
					TESTCASE_END;
				}
				SQLFreeStmt(hstmt,SQL_CLOSE);
				SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
				sprintf(Heading,"Setup for SQLBindParameter tests for delete table %s.\n",CDataValueTOSQL2[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DelTab,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					TestMXSQLBindParamaterVer3_Cleanup(hstmt,SQLStmt[1].DrpTab,tempType,InsStr,pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END;
				i++;
			}
		}
	}
	SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
	
//====================================================================================================
// Testing Section #3: converting from cfloat and cdouble to sql 

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		TESTCASE_BEGIN("Setup for SQLBindParameter tests for create table\n");
		
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[2].DrpTab,SQL_NTS);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[2].CrtTab,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			TestMXSQLBindParamaterVer3_Cleanup(hstmt,"",tempType,InsStr,pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}
		TESTCASE_END;

		i = 0;
		while (CDataValueTOSQL3[i].CType != 999)
		{
			for (k = 0 ; k < LOOP_BINDPARAM3; k++)
			{
				if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
				{
					sprintf(Heading,"Setup for SQLBindParameter tests for prepare %s.\n",CDataValueTOSQL3[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					returncode = SQLPrepare(hstmt,(SQLCHAR*)SQLStmt[2].InsTab,SQL_NTS);
 					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
					{
						LogAllErrorsVer3(henv,hdbc,hstmt);
						TestMXSQLBindParamaterVer3_Cleanup(hstmt,SQLStmt[2].DrpTab,tempType,InsStr,pTestInfo);
						TEST_FAILED;
						TEST_RETURN;
					}
					TESTCASE_END;
				}

				m = k*MAX_BINDPARAM2;
				for (j = 0; j < MAX_BINDPARAM2; j++)
				{
					sprintf(Heading,"Set up SQLBindParameter to convert from %s to %s\n",CDataValueTOSQL3[i].TestCType, CDataArgToSQL3.TestSQLType[j]);
					TESTCASE_BEGIN(Heading);
			
					switch (CDataValueTOSQL3[i].CType)
					{
						case SQL_C_FLOAT:
							returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL3[i].CType,
																					CDataArgToSQL3.SQLType[j],CDataArgToSQL3.ColPrec[j],
																					CDataArgToSQL3.ColScale[j],&(CDataTypeTOSQL3.CFLOATTOSQL[m]),0,
																					&InValue1);
							break;
						case SQL_C_DOUBLE:
							returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL3[i].CType,
																					CDataArgToSQL3.SQLType[j],CDataArgToSQL3.ColPrec[j],
																					CDataArgToSQL3.ColScale[j],&(CDataTypeTOSQL3.CDOUBLETOSQL[m]),0,
																					&InValue1);
							break;
						default: 
                            break;
					}

					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					TESTCASE_END;
					m++;
				}
			
				if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
				{
					sprintf(Heading,"Setup for SQLBindParameter tests for Execute %s.\n",CDataValueTOSQL3[i].TestCType);
					TESTCASE_BEGIN(Heading);
					returncode = SQLExecute(hstmt);         // Execute statement with 
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					TESTCASE_END;
				}
				if (loop_bindparam == BINDPARAM_EXECDIRECT)
				{
					sprintf(Heading,"Setup for SQLBindParameter tests for ExecDirect %s.\n",CDataValueTOSQL3[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[2].InsTab,SQL_NTS);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					TESTCASE_END;
				}
				if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
				{
					sprintf(Heading,"Setup for checking SQLBindParameter tests %s.\n",CDataValueTOSQL3[i].TestCType);
					TESTCASE_BEGIN(Heading);
					returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[2].SelTab,SQL_NTS);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					else
					{
						returncode = SQLFetch(hstmt);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
						{
							TEST_FAILED;
							LogAllErrorsVer3(henv,hdbc,hstmt);
						}
						else
						{
							for (j = 0; j < MAX_BINDPARAM3; j++)
							{
                                strcpy(OutValue,"");
								returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
                                LogMsg(NONE,"Value out is: %s\n",OutValue);
								if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
								{
                                    LogMsg(NONE,"SQLBindParameter test: checking data for column c%d\n",j+1);
									TEST_FAILED;
									LogAllErrorsVer3(henv,hdbc,hstmt);
								}
								else
								{
									if (_strnicmp(CDataValueTOSQL3[i].OutputValue[j],OutValue,strlen(CDataValueTOSQL3[i].OutputValue[j])) == 0)
									{
										//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueTOSQL3[i].OutputValue[j],OutValue);
									}	
									else
									{
										LogMsg(NONE,"LABS: expect: %f and actual: %f , at line %d\n",atof(CDataValueTOSQL3[i].OutputValue[j]), atof(OutValue),__LINE__);
										if (labs((long)(atof(CDataValueTOSQL3[i].OutputValue[j]) - atof(OutValue))) > 0.001)
										{
                                            LogMsg(NONE,"SQLBindParameter test: checking data for column c%d\n",j+1);
											TEST_FAILED;	
											LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at line: %d\n",CDataValueTOSQL3[i].OutputValue[j],OutValue,__LINE__);
                                        }
									}
								}
							} // end for loop
						}
					}
					TESTCASE_END;
				}
				SQLFreeStmt(hstmt,SQL_CLOSE);
				SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
				sprintf(Heading,"Setup for SQLBindParameter tests for delete table %s.\n",CDataValueTOSQL3[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[2].DelTab,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					TestMXSQLBindParamaterVer3_Cleanup(hstmt,SQLStmt[2].DrpTab,tempType,InsStr,pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END;
				i++;
			}
		}
	}
	SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[2].DrpTab,SQL_NTS);

//====================================================================================================
// Testing Section #4: converting from cdate, ctime and ctimestamp to sql

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		TESTCASE_BEGIN("Setup for SQLBindParameter tests for create table\n");
		
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[3].DrpTab,SQL_NTS);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[3].CrtTab,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrorsVer3(henv,hdbc,hstmt);
			TestMXSQLBindParamaterVer3_Cleanup(hstmt,"",tempType,InsStr,pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}
		TESTCASE_END;

		i = 0;
		while (CDataValueTOSQL4[i].CType != 999)
		{
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for prepare %s.\n",CDataValueTOSQL4[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLPrepare(hstmt,(SQLCHAR*)SQLStmt[3].InsTab,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					TestMXSQLBindParamaterVer3_Cleanup(hstmt,SQLStmt[3].DrpTab,tempType,InsStr,pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END;
			}

			for (j = 0; j < MAX_BINDPARAM4; j++)
			{
				sprintf(Heading,"Set up SQLBindParameter to convert from %s to %s\n",CDataValueTOSQL4[i].TestCType, CDataArgToSQL4.TestSQLType[j]);
				TESTCASE_BEGIN(Heading);
				
				switch (CDataValueTOSQL4[i].CType)
				{
					case SQL_C_DATE:
						if (CDataArgToSQL4.SQLType[j] != SQL_TIME)
							returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL4[i].CType,
																				CDataArgToSQL4.SQLType[j],CDataArgToSQL4.ColPrec[j],
																				CDataArgToSQL4.ColScale[j],&CDATETOSQL,0,&InValue1);
						else
							returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_TIME,
																				SQL_TIME,CDataArgToSQL4.ColPrec[j],
																				CDataArgToSQL4.ColScale[j],&CTIMETOSQL,0,&InValue1);
						break;
					case SQL_C_TIME:
						if (CDataArgToSQL4.SQLType[j] != SQL_DATE)
						{
							returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL4[i].CType,
																				CDataArgToSQL4.SQLType[j],CDataArgToSQL4.ColPrec[j],
																				CDataArgToSQL4.ColScale[j],&CTIMETOSQL,0,&InValue1);
							if (CDataArgToSQL4.SQLType[j] == SQL_TIMESTAMP && loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
							{
								struct tm *newtime;
								time_t long_time;

								time( &long_time );					// Get time as long integer. 
								newtime = localtime( &long_time );	// Convert to local time. 
								strcpy(tmpbuf,"");
								strcpy(tmpbuf1,"");
								_itoa(newtime->tm_year+1900,tmpbuf1,10);
								strcpy(tmpbuf,tmpbuf1);
								strcat(tmpbuf,"-");
								strcpy(tmpbuf1,"");
								_itoa(newtime->tm_mon+1,tmpbuf1,10);
								if (strlen(tmpbuf1) ==  1)
									strcat(tmpbuf,"0");
								strcat(tmpbuf,tmpbuf1);
								strcat(tmpbuf,"-");
								strcpy(tmpbuf1,"");
								_itoa(newtime->tm_mday,tmpbuf1,10);
								if (strlen(tmpbuf1) ==  1)
									strcat(tmpbuf,"0");
								strcat(tmpbuf,tmpbuf1);
								strcat(tmpbuf," ");
								strcat(tmpbuf,CDataValueTOSQL4[i].OutputValue[j]);
                                CDataValueTOSQL4[i].OutputValue[j] = tmpbuf;
								//strcpy(CDataValueTOSQL4[i].OutputValue[j],"");
								//strcpy(CDataValueTOSQL4[i].OutputValue[j],tmpbuf);
								//strcpy(tmpbuf,"");
								strcpy(tmpbuf1,"");
							}
						}
						else
							returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_DATE,
																				SQL_DATE,CDataArgToSQL4.ColPrec[j],
																				CDataArgToSQL4.ColScale[j],&CDATETOSQL,0,&InValue1);
						break;
					case SQL_C_TIMESTAMP:
						if (CDataArgToSQL4.SQLType[j] == SQL_DATE)
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL4[i].CType,
																				CDataArgToSQL4.SQLType[j],CDataArgToSQL4.ColPrec[j],
																				CDataArgToSQL4.ColScale[j],&CTIMESTAMPTOSQL1,0,&InValue1);
						else
						if (CDataArgToSQL4.SQLType[j] == SQL_TIME)
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL4[i].CType,
																				CDataArgToSQL4.SQLType[j],CDataArgToSQL4.ColPrec[j],
																				CDataArgToSQL4.ColScale[j],&CTIMESTAMPTOSQL2,0,&InValue1);
						else {
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL4[i].CType,
																				CDataArgToSQL4.SQLType[j],CDataArgToSQL4.ColPrec[j],
																				CDataArgToSQL4.ColScale[j],&CTIMESTAMPTOSQL,0,&InValue1);
						//LogMsg(NONE,"SQLBindParameter(hstmt,%d,%d,%d,%d,%d,%d,<address>,<dummy>\n",(SWORD)(j+1),ParamType,CDataValueTOSQL4[i].CType,
						//														CDataArgToSQL4.SQLType[j],CDataArgToSQL4.ColPrec[j],
						//														CDataArgToSQL4.ColScale[j]);
						}
						break;
					default: break;
				}

				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
		
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for Execute %s.\n",CDataValueTOSQL4[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecute(hstmt);         // Execute statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for ExecDirect %s.\n",CDataValueTOSQL4[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[3].InsTab,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
			{
				sprintf(Heading,"Setup for checking SQLBindParameter tests %s.\n",CDataValueTOSQL4[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[3].SelTab,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					else
					{
						for (j = 0; j < MAX_BINDPARAM4; j++)
						{
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
                                LogMsg(NONE,"SQLBindParameter test: checking data for column c%d\n",j+1);
								TEST_FAILED;
								LogAllErrorsVer3(henv,hdbc,hstmt);
							}
							else
							{
								if (_strnicmp(CDataValueTOSQL4[i].OutputValue[j],OutValue,strlen(CDataValueTOSQL4[i].OutputValue[j])) == 0)
								{
									//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueTOSQL4[i].OutputValue[j],OutValue);
								}	
								else
								{
                                    LogMsg(NONE,"SQLBindParameter test: checking data for column c%d\n",j+1);
									TEST_FAILED;	
									LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at line: %d\n",CDataValueTOSQL4[i].OutputValue[j],OutValue,__LINE__);
								}
							}
						} // end for loop
					}
				}
				TESTCASE_END;
			}
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			
			sprintf(Heading,"Setup for SQLBindParameter tests for delete table %s.\n",CDataValueTOSQL4[i].TestCType);
			TESTCASE_BEGIN(Heading);
			
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[3].DelTab,SQL_NTS);
 			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrorsVer3(henv,hdbc,hstmt);
				TestMXSQLBindParamaterVer3_Cleanup(hstmt,SQLStmt[3].DrpTab,tempType,InsStr,pTestInfo);
				TEST_FAILED;
				TEST_RETURN;
			}
			TESTCASE_END;
			i++;
		}
	}
	SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[3].DrpTab,SQL_NTS);

//=================================================================================================================
// Testing Section #5: converting from cdefault to sql

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		i = 0;
		while (CDataValueTOSQL5[i].CType != 999)
		{
			// Creating the table
			TESTCASE_BEGIN("Setup for SQLBindParameter tests to create table for SQL_C_DEFAULT.\n");
			
			SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[4].DrpTab,SQL_NTS);
            sprintf(InsStr,"%s %s",SQLStmt[4].CrtTab,CDataValueTOSQL5[i].CrtCol);
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
 			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrorsVer3(henv,hdbc,hstmt);
				TestMXSQLBindParamaterVer3_Cleanup(hstmt,"",tempType,InsStr,pTestInfo);
				TEST_FAILED;
				TEST_RETURN;
			}
			TESTCASE_END; 

			// Preparing for an insert into the table.
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for prepare SQL_C_DEFAULT.\n");
				TESTCASE_BEGIN(Heading);

				returncode = SQLPrepare(hstmt,(SQLCHAR*)SQLStmt[4].InsTab,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					TestMXSQLBindParamaterVer3_Cleanup(hstmt,SQLStmt[4].DrpTab,tempType,InsStr,pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END; 
			}

			// Binding with all of the columns in the table.... this goes on for awhile.
			sprintf(Heading,"SQLBindParameter from SQL_C_DEFAULT to SQL_CHAR.\n");
			TESTCASE_BEGIN(Heading);
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(1),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[0],CDataValueTOSQL5[i].ColPrec[0],
																			CDataValueTOSQL5[i].ColScale[0],CDataValueTOSQL5[i].CharValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(1),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[0],CDataValueTOSQL5[i].ColPrec[0],
																			CDataValueTOSQL5[i].ColScale[0],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;
		
			sprintf(Heading,"SQLBindParameter from SQL_C_DEFAULT to SQL_VARCHAR.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(2),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[1],CDataValueTOSQL5[i].ColPrec[1],
																			CDataValueTOSQL5[i].ColScale[1],CDataValueTOSQL5[i].VarCharValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(2),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[1],CDataValueTOSQL5[i].ColPrec[1],
																			CDataValueTOSQL5[i].ColScale[1],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_DEFAULT to SQL_DECIMAL.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(3),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[2],CDataValueTOSQL5[i].ColPrec[2],
																			CDataValueTOSQL5[i].ColScale[2],CDataValueTOSQL5[i].DecimalValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(3),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[2],CDataValueTOSQL5[i].ColPrec[2],
																			CDataValueTOSQL5[i].ColScale[2],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_DEFAULT to SQL_NUMERIC.\n");
			TESTCASE_BEGIN(Heading);
			
            InValue = SQL_NTS;
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(4),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[3],CDataValueTOSQL5[i].ColPrec[3],
																			CDataValueTOSQL5[i].ColScale[3],CDataValueTOSQL5[i].NumericValue,NAME_LEN,
																			&InValue);
                /*LogMsg(NONE,"SQLBindParameter(hstmt,%d,%d,%d,%d,%d,%d,%s,%d,%d)\n",(SWORD)(4),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[3],CDataValueTOSQL5[i].ColPrec[3],
																			CDataValueTOSQL5[i].ColScale[3],CDataValueTOSQL5[i].NumericValue,NAME_LEN,
																			&InValue);*/
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(4),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[3],CDataValueTOSQL5[i].ColPrec[3],
																			CDataValueTOSQL5[i].ColScale[3],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_DEFAULT to SQL_SMALLINT.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(5),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[4],CDataValueTOSQL5[i].ColPrec[4],
																			CDataValueTOSQL5[i].ColScale[4],&(CDataValueTOSQL5[i].ShortValue),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(5),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[4],CDataValueTOSQL5[i].ColPrec[4],
																			CDataValueTOSQL5[i].ColScale[4],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_DEFAULT to SQL_INTEGER.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(6),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[5],CDataValueTOSQL5[i].ColPrec[5],
																			CDataValueTOSQL5[i].ColScale[5],&(CDataValueTOSQL5[i].LongValue),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(6),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[5],CDataValueTOSQL5[i].ColPrec[5],
																			CDataValueTOSQL5[i].ColScale[5],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_DEFAULT to SQL_REAL.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(7),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[6],CDataValueTOSQL5[i].ColPrec[6],
																			CDataValueTOSQL5[i].ColScale[6],&(CDataValueTOSQL5[i].RealValue),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(7),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[6],CDataValueTOSQL5[i].ColPrec[6],
																			CDataValueTOSQL5[i].ColScale[6],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_DEFAULT to SQL_FLOAT.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(8),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[7],CDataValueTOSQL5[i].ColPrec[7],
																			CDataValueTOSQL5[i].ColScale[7],&(CDataValueTOSQL5[i].FloatValue),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(8),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[7],CDataValueTOSQL5[i].ColPrec[7],
																			CDataValueTOSQL5[i].ColScale[7],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_DEFAULT to SQL_DOUBLE.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(9),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[8],CDataValueTOSQL5[i].ColPrec[8],
																			CDataValueTOSQL5[i].ColScale[8],&(CDataValueTOSQL5[i].DoubleValue),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(9),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[8],CDataValueTOSQL5[i].ColPrec[8],
																			CDataValueTOSQL5[i].ColScale[8],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_DEFAULT to SQL_DATE.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(10),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[9],CDataValueTOSQL5[i].ColPrec[9],
																			CDataValueTOSQL5[i].ColScale[9],&(CDataValueTOSQL5[i].DateValue),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(10),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[9],CDataValueTOSQL5[i].ColPrec[9],
																			CDataValueTOSQL5[i].ColScale[9],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_DEFAULT to SQL_TIME.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(11),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[10],CDataValueTOSQL5[i].ColPrec[10],
																			CDataValueTOSQL5[i].ColScale[10],&(CDataValueTOSQL5[i].TimeValue),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(11),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[10],CDataValueTOSQL5[i].ColPrec[10],
																			CDataValueTOSQL5[i].ColScale[10],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_DEFAULT to SQL_TIMESTAMP.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(12),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[11],CDataValueTOSQL5[i].ColPrec[11],
																			CDataValueTOSQL5[i].ColScale[11],&(CDataValueTOSQL5[i].TimestampValue),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(12),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[11],CDataValueTOSQL5[i].ColPrec[11],
																			CDataValueTOSQL5[i].ColScale[11],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_DEFAULT to SQL_LONGVARCHAR.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(13),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[12],CDataValueTOSQL5[i].ColPrec[12],
																			CDataValueTOSQL5[i].ColScale[12],CDataValueTOSQL5[i].LongVarCharValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(13),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[12],CDataValueTOSQL5[i].ColPrec[12],
																			CDataValueTOSQL5[i].ColScale[12],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_DEFAULT to SQL_BIGINT.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(14),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[13],CDataValueTOSQL5[i].ColPrec[13],
																			CDataValueTOSQL5[i].ColScale[13],&(CDataValueTOSQL5[i].BigintValue),NAME_LEN,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(14),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[13],CDataValueTOSQL5[i].ColPrec[13],
																			CDataValueTOSQL5[i].ColScale[13],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

            sprintf(Heading,"SQLBindParameter from SQL_C_DEFAULT to SQL_CHAR NCHAR.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(15),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[14],CDataValueTOSQL5[i].ColPrec[14],
																			CDataValueTOSQL5[i].ColScale[14],CDataValueTOSQL5[i].NCharValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(15),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[14],CDataValueTOSQL5[i].ColPrec[14],
																			CDataValueTOSQL5[i].ColScale[14],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

            sprintf(Heading,"SQLBindParameter from SQL_C_DEFAULT to SQL_VARCHAR NCHAR VARYING.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(16),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[15],CDataValueTOSQL5[i].ColPrec[15],
																			CDataValueTOSQL5[i].ColScale[15],CDataValueTOSQL5[i].NVarCharValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(16),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[15],CDataValueTOSQL5[i].ColPrec[15],
																			CDataValueTOSQL5[i].ColScale[15],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

            sprintf(Heading,"SQLBindParameter from SQL_C_DEFAULT to SQL_LONGVARCHAR LONG VARCHAR UCS2.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(17),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[16],CDataValueTOSQL5[i].ColPrec[16],
																			CDataValueTOSQL5[i].ColScale[16],CDataValueTOSQL5[i].NLongVarCharValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(17),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[16],CDataValueTOSQL5[i].ColPrec[16],
																			CDataValueTOSQL5[i].ColScale[16],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;
			// Finished binding.....

			// Now executing the insert statement.
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for Execute SQL_C_DEFAULT.\n");
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecute(hstmt);         // Execute statement with 
				if(!CHECKRC(CDataValueTOSQL5[i].PassFail,returncode,"SQLExecute"))
				{
                    LogMsg(NONE,"NUMERIC fails on CDataValueTOSQL5[%d]\n",i);
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for ExecDirect SQL_C_DEFAULT.\n");
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[4].InsTab,SQL_NTS);
				if(!CHECKRC(CDataValueTOSQL5[i].PassFail,returncode,"SQLExecDirect"))
				{
                    LogMsg(NONE,"NUMERIC fails on CDataValueTOSQL5[%d]\n",i);
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if(returncode == SQL_SUCCESS)
			{
				sprintf(Heading,"Setup for checking SQLBindParameter tests SQL_C_DEFAULT.\n");
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[4].SelTab,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					else
					{
						for (j = 0; j < MAX_BINDPARAM1; j++)
						{
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
                                LogMsg(NONE,"SQLBindParameter test:checking data for column c%d\n",j+1);
								TEST_FAILED;
								LogAllErrorsVer3(henv,hdbc,hstmt);
							}
							else
							{
								if (!CDataValueTOSQL5[i].NullData)
								{
/* Windows driver is UNICODE driver, SQL_C_DEFAULT for SQL_CHAR, SQL_VARCHAR,
 * etc is mapped to SQL_C_WCHAR and needs to be handled using the UNICODE _T(),
 * and _tcsxxx() functions.  That will be tested by the UNICODE version.  The
 * ANSI version will skip this testing.
 */
#ifndef unixcli /*  */
if (j != 14 && j != 15 && j != 16)
{
#endif /*  */
									if (_strnicmp(CDataValueTOSQL5[i].OutputValue[j],OutValue,strlen(CDataValueTOSQL5[i].OutputValue[j])) == 0)
									{
										//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueTOSQL5[i].OutputValue[j],OutValue);
									}	
									else
									{
                                        LogMsg(NONE,"SQLBindParameter test:checking data for column c%d\n",j+1);
										TEST_FAILED;	
										LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at line: %d\n",CDataValueTOSQL5[i].OutputValue[j],OutValue,__LINE__);
									}
#ifndef unixcli /* */
}
#endif /* */
								}
								else
								{
									if (OutValueLen == SQL_NULL_DATA)
									{
										//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQL_NULL_DATA,OutValueLen);
									}	
									else
									{
                                        LogMsg(NONE,"SQLBindParameter test:checking data for column c%d\n",j+1);
										TEST_FAILED;	
										LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at line: %d\n",SQL_NULL_DATA,OutValueLen,__LINE__);
									}
								}
							}
						} // end for loop
					}
				}
				TESTCASE_END;
			}
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			i++;
		}
	}
	SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[4].DrpTab,SQL_NTS);

//=================================================================================================================
// Testing Section #6: converting from cnumeric to sql

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		i = 0;
		while (CDataValueTOSQL6[i].CType != 999)
		{
			// Creating the table
			TESTCASE_BEGIN("Setup for SQLBindParameter tests to create table for SQL_C_NUMERIC.\n");
			//TESTCASE_BEGIN(Heading);
			
			SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[5].DrpTab,SQL_NTS);
			sprintf(InsStr,"%s %s",SQLStmt[5].CrtTab,CDataValueTOSQL6[i].CrtCol);
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
 			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrorsVer3(henv,hdbc,hstmt);
				TestMXSQLBindParamaterVer3_Cleanup(hstmt,"",tempType,InsStr,pTestInfo);
				TEST_FAILED;
				TEST_RETURN;
			}
			TESTCASE_END; 

			// Preparing for an insert into the table.
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for prepare SQL_C_NUMERIC.\n");
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLPrepare(hstmt,(SQLCHAR*)SQLStmt[5].InsTab,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					TestMXSQLBindParamaterVer3_Cleanup(hstmt,SQLStmt[5].DrpTab,tempType,InsStr,pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END; 
			}

			// Binding with all of the columns in the table.... this goes on for awhile.
			sprintf(Heading,"SQLBindParameter from SQL_C_NUMERIC to SQL_CHAR.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL6[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(1),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[0],CDataValueTOSQL6[i].ColPrec[0],
																			CDataValueTOSQL6[i].ColScale[0],&(CDataValueTOSQL6[i].NumericValue1),NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(1),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[0],CDataValueTOSQL6[i].ColPrec[0],
																			CDataValueTOSQL6[i].ColScale[0],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;
		
			sprintf(Heading,"SQLBindParameter from SQL_C_NUMERIC to SQL_VARCHAR.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL6[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(2),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[1],CDataValueTOSQL6[i].ColPrec[1],
																			CDataValueTOSQL6[i].ColScale[1],&(CDataValueTOSQL6[i].NumericValue2),NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(2),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[1],CDataValueTOSQL6[i].ColPrec[1],
																			CDataValueTOSQL6[i].ColScale[1],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_NUMERIC to SQL_DECIMAL.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL6[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(3),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[2],CDataValueTOSQL6[i].ColPrec[2],
																			CDataValueTOSQL6[i].ColScale[2],&(CDataValueTOSQL6[i].NumericValue3),NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(3),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[2],CDataValueTOSQL6[i].ColPrec[2],
																			CDataValueTOSQL6[i].ColScale[2],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_NUMERIC to SQL_NUMERIC.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL6[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(4),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[3],CDataValueTOSQL6[i].ColPrec[3],
																			CDataValueTOSQL6[i].ColScale[3],&(CDataValueTOSQL6[i].NumericValue4),NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(4),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[3],CDataValueTOSQL6[i].ColPrec[3],
																			CDataValueTOSQL6[i].ColScale[3],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_NUMERIC to SQL_SMALLINT.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL6[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(5),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[4],CDataValueTOSQL6[i].ColPrec[4],
																			CDataValueTOSQL6[i].ColScale[4],&(CDataValueTOSQL6[i].NumericValue5),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(5),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[4],CDataValueTOSQL6[i].ColPrec[4],
																			CDataValueTOSQL6[i].ColScale[4],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_NUMERIC to SQL_INTEGER.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL6[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(6),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[5],CDataValueTOSQL6[i].ColPrec[5],
																			CDataValueTOSQL6[i].ColScale[5],&(CDataValueTOSQL6[i].NumericValue6),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(6),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[5],CDataValueTOSQL6[i].ColPrec[5],
																			CDataValueTOSQL6[i].ColScale[5],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_NUMERIC to SQL_REAL.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL6[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(7),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[6],CDataValueTOSQL6[i].ColPrec[6],
																			CDataValueTOSQL6[i].ColScale[6],&(CDataValueTOSQL6[i].NumericValue7),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(7),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[6],CDataValueTOSQL6[i].ColPrec[6],
																			CDataValueTOSQL6[i].ColScale[6],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_NUMERIC to SQL_FLOAT.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL6[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(8),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[7],CDataValueTOSQL6[i].ColPrec[7],
																			CDataValueTOSQL6[i].ColScale[7],&(CDataValueTOSQL6[i].NumericValue8),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(8),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[7],CDataValueTOSQL6[i].ColPrec[7],
																			CDataValueTOSQL6[i].ColScale[7],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_NUMERIC to SQL_DOUBLE.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL6[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(9),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[8],CDataValueTOSQL6[i].ColPrec[8],
																			CDataValueTOSQL6[i].ColScale[8],&(CDataValueTOSQL6[i].NumericValue9),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(9),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[8],CDataValueTOSQL6[i].ColPrec[8],
																			CDataValueTOSQL6[i].ColScale[8],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_NUMERIC to SQL_LONGVARCHAR.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL6[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(10),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[9],CDataValueTOSQL6[i].ColPrec[9],
																			CDataValueTOSQL6[i].ColScale[9],&(CDataValueTOSQL6[i].NumericValue10),NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(10),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[9],CDataValueTOSQL6[i].ColPrec[9],
																			CDataValueTOSQL6[i].ColScale[9],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_NUMERIC to SQL_BIGINT.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL6[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(11),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[10],CDataValueTOSQL6[i].ColPrec[10],
																			CDataValueTOSQL6[i].ColScale[10],&(CDataValueTOSQL6[i].NumericValue11),NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(11),ParamType,CDataValueTOSQL6[i].CType,
																			CDataArgToSQL6.SQLType[10],CDataValueTOSQL6[i].ColPrec[10],
																			CDataValueTOSQL6[i].ColScale[10],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;
			// Finished binding.....

			// Now executing the insert statement.
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for Execute SQL_C_NUMERIC.\n");
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecute(hstmt);         // Execute statement with 
				if(!CHECKRC(CDataValueTOSQL6[i].PassFail,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for ExecDirect SQL_C_NUMERIC.\n");
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[5].InsTab,SQL_NTS);
				if(!CHECKRC(CDataValueTOSQL6[i].PassFail,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if(returncode == SQL_SUCCESS)
			{
				sprintf(Heading,"Setup for checking SQLBindParameter tests SQL_C_NUMERIC.\n");
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[5].SelTab,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					else
					{
						for (j = 0; j < MAX_BINDPARAM6; j++)
						{
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
                                LogMsg(NONE,"SQLBindParameter test: checking data for column c%d\n",j+1);
								TEST_FAILED;
								LogAllErrorsVer3(henv,hdbc,hstmt);
							}
							else
							{
								if (!CDataValueTOSQL6[i].NullData)
								{
									if (_strnicmp(CDataValueTOSQL6[i].OutputValue[j],OutValue,strlen(CDataValueTOSQL6[i].OutputValue[j])) == 0)
									{
										//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueTOSQL6[i].OutputValue[j],OutValue);
									}	
									else
									{
                                        LogMsg(NONE,"SQLBindParameter test: checking data for column c%d\n",j+1);
										TEST_FAILED;	
										LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at line: %d\n",CDataValueTOSQL6[i].OutputValue[j],OutValue,__LINE__);
									}
								}
								else
								{
									if (OutValueLen == SQL_NULL_DATA)
									{
										//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQL_NULL_DATA,OutValueLen);
									}	
									else
									{
                                        LogMsg(NONE,"SQLBindParameter test: checking data for column c%d\n",j+1);
										TEST_FAILED;	
										LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at line: %d\n",SQL_NULL_DATA,OutValueLen,__LINE__);
									}
								}
							}
						} // end for loop
					}
				}
				TESTCASE_END;
			}
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			i++;
		}
	}
	SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[5].DrpTab,SQL_NTS);

//=================================================================================================================
// Testing Section #7: converting from cdefault,c_char & c_timestamp to sql_timestamp

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		i = 0;
		while (CDataValueTOSQL7[i].CType != 999)
		{
			// Creating the table
			//TESTCASE_BEGIN("Setup for SQLBindParameter tests to create table for DATETIME.\n");
			
			SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[6].DrpTab,SQL_NTS);
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[6].CrtTab,SQL_NTS);
			/*if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}*/
			// Preparing for an insert into the table.
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for prepare DATETIME TESTS.\n");
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLPrepare(hstmt,(SQLCHAR*)SQLStmt[6].InsTab,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					//TestMXSQLBindParamaterVer3_Cleanup(hstmt,SQLStmt[6].,tempType,InsStr,pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END; 
			}

			// Binding with all of the columns in the table.... this goes on for awhile.
			sprintf(Heading,"SQLBindParameter from SQL_C_DEFAULT to SQL_TIMESTAMP.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL7[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(1),ParamType,CDataValueTOSQL7[i].CType,
																			CDataArgToSQL7.SQLType[0],CDataValueTOSQL7[i].ColPrec[0],
																			CDataValueTOSQL7[i].ColScale[0],&(CDataValueTOSQL7[i].TimestampValue1),NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(1),ParamType,CDataValueTOSQL7[i].CType,
																			CDataArgToSQL7.SQLType[0],CDataValueTOSQL7[i].ColPrec[0],
																			CDataValueTOSQL7[i].ColScale[0],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;
		
			sprintf(Heading,"SQLBindParameter from SQL_C_DEFAULT to SQL_TIMESTAMP.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL7[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(2),ParamType,CDataValueTOSQL7[i].CType,
																			CDataArgToSQL7.SQLType[1],CDataValueTOSQL7[i].ColPrec[1],
																			CDataValueTOSQL7[i].ColScale[1],&(CDataValueTOSQL7[i].TimestampValue2),NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(2),ParamType,CDataValueTOSQL7[i].CType,
																			CDataArgToSQL7.SQLType[1],CDataValueTOSQL7[i].ColPrec[1],
																			CDataValueTOSQL7[i].ColScale[1],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;
			// Finished binding.....

			// Now executing the insert statement.
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for Execute DATETIME.\n");
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecute(hstmt);         // Execute statement with 
				if(!CHECKRC(CDataValueTOSQL7[i].PassFail,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for ExecDirect DATETIME.\n");
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[6].InsTab,SQL_NTS);
				if(!CHECKRC(CDataValueTOSQL7[i].PassFail,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if(returncode == SQL_SUCCESS)
			{
				sprintf(Heading,"Setup for checking SQLBindParameter tests DATETIME.\n");
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[6].SelTab,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					else
					{
						for (j = 0; j < MAX_BINDPARAM7; j++)
						{
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
                                LogMsg(NONE,"SQLBindParameter test:checking data for column c%d\n",j+1);
								TEST_FAILED;
								LogAllErrorsVer3(henv,hdbc,hstmt);
							}
							else
							{
								if (!CDataValueTOSQL7[i].NullData)
								{
									if (_strnicmp(CDataValueTOSQL7[i].OutputValue[j],OutValue,strlen(CDataValueTOSQL7[i].OutputValue[j])) == 0)
									{
										//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueTOSQL7[i].OutputValue[j],OutValue);
									}	
									else
									{
                                        LogMsg(NONE,"SQLBindParameter test:checking data for column c%d\n",j+1);
										TEST_FAILED;	
										LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at line: %d\n",CDataValueTOSQL7[i].OutputValue[j],OutValue, __LINE__);
									}
								}
								else
								{
									if (OutValueLen == SQL_NULL_DATA)
									{
										//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQL_NULL_DATA,OutValueLen);
									}	
									else
									{
                                        LogMsg(NONE,"SQLBindParameter test:checking data for column c%d\n",j+1);
										TEST_FAILED;	
										LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at line: %d\n",SQL_NULL_DATA,OutValueLen, __LINE__);
									}
								}
							}
						} // end for loop
					}
				}
				TESTCASE_END;
			}
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			i++;
		}
	}
	SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[6].DrpTab,SQL_NTS);

//=================================================================================================================
// Testing Section #8
// converting from char to sql

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		i = 0;
		while (CDataValueTOSQL8[i].CType != 999)
		{
			// Creating the table
			TESTCASE_BEGIN("Setup for SQLBindParameter tests to create table for SQL_C_CHAR.\n");
			
			SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[7].DrpTab,SQL_NTS);
            sprintf(InsStr,"%s %s",SQLStmt[7].CrtTab,CDataValueTOSQL8[i].CrtCol);
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
 			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrorsVer3(henv,hdbc,hstmt);
				TestMXSQLBindParamaterVer3_Cleanup(hstmt,"",tempType,InsStr,pTestInfo);
				TEST_FAILED;
				TEST_RETURN;
			}
			TESTCASE_END; 

			// Preparing for an insert into the table.
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for prepare SQL_C_CHAR.\n");
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLPrepare(hstmt,(SQLCHAR*)SQLStmt[7].InsTab,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					TestMXSQLBindParamaterVer3_Cleanup(hstmt,SQLStmt[7].DrpTab,tempType,InsStr,pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END; 
			}

			// Binding with all of the columns in the table.... this goes on for awhile.
			sprintf(Heading,"SQLBindParameter from SQL_C_CHAR to SQL_CHAR.\n");
			TESTCASE_BEGIN(Heading);
			if (!CDataValueTOSQL8[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(1),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[0],CDataValueTOSQL8[i].ColPrec[0],
																			CDataValueTOSQL8[i].ColScale[0],CDataValueTOSQL8[i].CharValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(1),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[0],CDataValueTOSQL8[i].ColPrec[0],
																			CDataValueTOSQL8[i].ColScale[0],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;
		
			sprintf(Heading,"SQLBindParameter from SQL_C_CHAR to SQL_VARCHAR.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL8[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(2),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[1],CDataValueTOSQL8[i].ColPrec[1],
																			CDataValueTOSQL8[i].ColScale[1],CDataValueTOSQL8[i].VarCharValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(2),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[1],CDataValueTOSQL8[i].ColPrec[1],
																			CDataValueTOSQL8[i].ColScale[1],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_CHAR to SQL_DECIMAL.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL8[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(3),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[2],CDataValueTOSQL8[i].ColPrec[2],
																			CDataValueTOSQL8[i].ColScale[2],CDataValueTOSQL8[i].DecimalValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(3),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[2],CDataValueTOSQL8[i].ColPrec[2],
																			CDataValueTOSQL8[i].ColScale[2],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_CHAR to SQL_NUMERIC.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL8[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(4),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[3],CDataValueTOSQL8[i].ColPrec[3],
																			CDataValueTOSQL8[i].ColScale[3],CDataValueTOSQL8[i].NumericValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(4),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[3],CDataValueTOSQL8[i].ColPrec[3],
																			CDataValueTOSQL8[i].ColScale[3],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_CHAR to SQL_SMALLINT.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL8[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(5),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[4],CDataValueTOSQL8[i].ColPrec[4],
																			CDataValueTOSQL8[i].ColScale[4],CDataValueTOSQL8[i].ShortValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(5),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[4],CDataValueTOSQL8[i].ColPrec[4],
																			CDataValueTOSQL8[i].ColScale[4],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_CHAR to SQL_INTEGER.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL8[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(6),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[5],CDataValueTOSQL8[i].ColPrec[5],
																			CDataValueTOSQL8[i].ColScale[5],CDataValueTOSQL8[i].LongValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(6),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[5],CDataValueTOSQL8[i].ColPrec[5],
																			CDataValueTOSQL8[i].ColScale[5],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_CHAR to SQL_REAL.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL8[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(7),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[6],CDataValueTOSQL8[i].ColPrec[6],
																			CDataValueTOSQL8[i].ColScale[6],CDataValueTOSQL8[i].RealValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(7),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[6],CDataValueTOSQL8[i].ColPrec[6],
																			CDataValueTOSQL8[i].ColScale[6],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_CHAR to SQL_FLOAT.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL8[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(8),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[7],CDataValueTOSQL8[i].ColPrec[7],
																			CDataValueTOSQL8[i].ColScale[7],CDataValueTOSQL8[i].FloatValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(8),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[7],CDataValueTOSQL8[i].ColPrec[7],
																			CDataValueTOSQL8[i].ColScale[7],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_CHAR to SQL_DOUBLE.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL8[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(9),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[8],CDataValueTOSQL8[i].ColPrec[8],
																			CDataValueTOSQL8[i].ColScale[8],CDataValueTOSQL8[i].DoubleValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(9),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[8],CDataValueTOSQL8[i].ColPrec[8],
																			CDataValueTOSQL8[i].ColScale[8],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_CHAR to SQL_DATE.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL8[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(10),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[9],CDataValueTOSQL8[i].ColPrec[9],
																			CDataValueTOSQL8[i].ColScale[9],CDataValueTOSQL8[i].DateValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(10),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[9],CDataValueTOSQL8[i].ColPrec[9],
																			CDataValueTOSQL8[i].ColScale[9],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_CHART to SQL_TIME.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL8[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(11),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[10],CDataValueTOSQL8[i].ColPrec[10],
																			CDataValueTOSQL8[i].ColScale[10],CDataValueTOSQL8[i].TimeValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(11),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[10],CDataValueTOSQL8[i].ColPrec[10],
																			CDataValueTOSQL8[i].ColScale[10],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_CHAR to SQL_TIMESTAMP.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL8[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(12),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[11],CDataValueTOSQL8[i].ColPrec[11],
																			CDataValueTOSQL8[i].ColScale[11],CDataValueTOSQL8[i].TimestampValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(12),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[11],CDataValueTOSQL8[i].ColPrec[11],
																			CDataValueTOSQL8[i].ColScale[11],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_CHAR to SQL_LONGVARCHAR.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL8[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(13),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[12],CDataValueTOSQL8[i].ColPrec[12],
																			CDataValueTOSQL8[i].ColScale[12],CDataValueTOSQL8[i].LongVarCharValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(13),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[12],CDataValueTOSQL8[i].ColPrec[12],
																			CDataValueTOSQL8[i].ColScale[12],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			sprintf(Heading,"SQLBindParameter from SQL_C_CHAR to SQL_BIGINT.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL8[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(14),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[13],CDataValueTOSQL8[i].ColPrec[13],
																			CDataValueTOSQL8[i].ColScale[13],CDataValueTOSQL8[i].BigintValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(14),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[13],CDataValueTOSQL8[i].ColPrec[13],
																			CDataValueTOSQL8[i].ColScale[13],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

            sprintf(Heading,"SQLBindParameter from SQL_C_CHAR to SQL_CHAR NCHAR.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL8[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(15),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[14],CDataValueTOSQL8[i].ColPrec[14],
																			CDataValueTOSQL8[i].ColScale[14],CDataValueTOSQL8[i].NCharValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(15),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[14],CDataValueTOSQL8[i].ColPrec[14],
																			CDataValueTOSQL8[i].ColScale[14],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

            sprintf(Heading,"SQLBindParameter from SQL_C_CHAR to SQL_VARCHAR NCHAR VARYING.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL8[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(16),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[15],CDataValueTOSQL8[i].ColPrec[15],
																			CDataValueTOSQL8[i].ColScale[15],CDataValueTOSQL8[i].NVarCharValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(16),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[15],CDataValueTOSQL8[i].ColPrec[15],
																			CDataValueTOSQL8[i].ColScale[15],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

            sprintf(Heading,"SQLBindParameter from SQL_C_CHAR to SQL_LONGVARCHAR LONG VARCHAR UCS2.\n");
			TESTCASE_BEGIN(Heading);
			
			if (!CDataValueTOSQL8[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(17),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[16],CDataValueTOSQL8[i].ColPrec[16],
																			CDataValueTOSQL8[i].ColScale[16],CDataValueTOSQL8[i].NLongVarCharValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(17),ParamType,CDataValueTOSQL8[i].CType,
																			CDataArgToSQL8.SQLType[16],CDataValueTOSQL8[i].ColPrec[16],
																			CDataValueTOSQL8[i].ColScale[16],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;
			// Finished binding.....

			// Now executing the insert statement.
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for Execute SQL_C_CHAR.\n");
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecute(hstmt);         // Execute statement with 
				if(!CHECKRC(CDataValueTOSQL8[i].PassFail,returncode,"SQLExecute"))
				{
					//printf("failed i=%d %s\n", i , InsStr);
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for ExecDirect SQL_C_CHAR.\n");
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[7].InsTab,SQL_NTS);
				if(!CHECKRC(CDataValueTOSQL8[i].PassFail,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if(returncode == SQL_SUCCESS)
			{
				sprintf(Heading,"Setup for checking SQLBindParameter tests SQL_C_CHAR.\n");
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[7].SelTab,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					else
					{
						for (j = 0; j < MAX_BINDPARAM1; j++)
						{
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
                                LogMsg(NONE,"SQLBindParameter test:checking data for column c%d\n",j+1);
								TEST_FAILED;
								LogAllErrorsVer3(henv,hdbc,hstmt);
							}
							else
							{
								if (!CDataValueTOSQL8[i].NullData)
								{
									if (_strnicmp(CDataValueTOSQL8[i].OutputValue[j],OutValue,strlen(CDataValueTOSQL8[i].OutputValue[j])) == 0)
									{
										//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueTOSQL8[i].OutputValue[j],OutValue);
									}	
									else
									{
                                        LogMsg(NONE,"SQLBindParameter test:checking data for column c%d\n",j+1);
										TEST_FAILED;	
										LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at line: %d\n",CDataValueTOSQL8[i].OutputValue[j],OutValue,__LINE__);
									}
								}
								else
								{
									if (OutValueLen == SQL_NULL_DATA)
									{
										//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQL_NULL_DATA,OutValueLen);
									}	
									else
									{
                                        LogMsg(NONE,"SQLBindParameter test:checking data for column c%d\n",j+1);
										TEST_FAILED;	
										LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at line: %d\n",SQL_NULL_DATA,OutValueLen,__LINE__);
									}
								}
							}
						} // end for loop
					}
				}
				TESTCASE_END;
			}
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			i++;
		}
	}
	SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[7].DrpTab,SQL_NTS);

//=================================================================================================================
// Section #9: convert SQL_C_FLOAT to SQL_NUMERIC
    i = 0;
	while (CFloatToNumeric[i].PassFail != 999)
	{
		TESTCASE_BEGIN("SQLBindParameter tests to bind from SQL_C_FLOAT to SQL_NUMERIC.\n");
		SQLExecDirect(hstmt,(SQLCHAR*) SQLStmt[8].DrpTab,SQL_NTS);
        sprintf(InsStr, "%s %s", SQLStmt[8].CrtTab, CFloatToNumeric[i].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}

		returncode = SQLPrepare(hstmt,(SQLCHAR*)SQLStmt[8].InsTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}

        for(j = 0; j < MAX_BINDPARAM8; j++) {
            InValue = SQL_NTS;
		    returncode = SQLBindParameter(hstmt,(SWORD)(j+1),SQL_PARAM_INPUT,SQL_C_FLOAT,SQL_NUMERIC,
								    CFloatToNumeric[i].ColPrec[j],CFloatToNumeric[i].ColScale[j],
                                    &(CFloatToNumeric[i].FloatValue[j]),0,&InValue);
		    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		    {
			    TEST_FAILED;
			    LogAllErrors(henv,hdbc,hstmt);
		    }
        }

        returncode = SQLExecute(hstmt);
        if(!CHECKRC(CFloatToNumeric[i].PassFail,returncode,"SQLExecute"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
        if (returncode == SQL_SUCCESS || returncode ==  SQL_SUCCESS_WITH_INFO)
		{
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[8].SelTab,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				returncode = SQLFetch(hstmt);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (j = 0; j < MAX_BINDPARAM8; j++)
					{
						returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
						{
                            LogMsg(NONE,"SQLBindParameter test:checking data for column c%d\n",j+1);
							TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
						else
						{
							if (strncmp(CFloatToNumeric[i].OutputValue[j],OutValue,strlen(CFloatToNumeric[i].OutputValue[j])) == 0)
							{
								//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CFloatToNumeric[i].OutputValue[j],OutValue);
							}	
							else
							{
								LogMsg(NONE,"LABS: expect: %s	and actual: %s , at line %d\n",CFloatToNumeric[i].OutputValue[j], OutValue,__LINE__);
								if (fabsf((float)(atof(CFloatToNumeric[i].OutputValue[j]) - atof(OutValue))) > 0.000001)
								{
                                    LogMsg(NONE,"SQLBindParameter test:checking data for column c%d\n",j+1);
									TEST_FAILED;	
									//LogMsg(NONE,"Float input value: %f\n", CFloatToNumeric[i].FloatValue[j]);
									LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at line %d\n",CFloatToNumeric[i].OutputValue[j],OutValue,__LINE__);
								}
							}
						}
					} // end for loop
				}
			}
		}
		TESTCASE_END;
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
		SQLExecDirect(hstmt,(SQLCHAR*) SQLStmt[8].DrpTab,SQL_NTS);
		i++;
	}

//=================================================================================================================
// Section #10: convert SQL_C_DOUBLE to SQL_NUMERIC

    i = 0;
	while (CDoubleToNumeric[i].PassFail != 999)
	{
		TESTCASE_BEGIN("SQLBindParameter tests to bind from SQL_C_DOUBLE to SQL_NUMERIC.\n");
		SQLExecDirect(hstmt,(SQLCHAR*) SQLStmt[8].DrpTab,SQL_NTS);
        sprintf(InsStr, "%s %s", SQLStmt[8].CrtTab, CDoubleToNumeric[i].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}

		returncode = SQLPrepare(hstmt,(SQLCHAR*)SQLStmt[8].InsTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}

        for(j = 0; j < MAX_BINDPARAM8; j++) {
            InValue = SQL_NTS;
		    returncode = SQLBindParameter(hstmt,(SWORD)(j+1),SQL_PARAM_INPUT,SQL_C_DOUBLE,SQL_NUMERIC,
								    CDoubleToNumeric[i].ColPrec[j],CDoubleToNumeric[i].ColScale[j],
                                    &(CDoubleToNumeric[i].DoubleValue[j]),0,&InValue);
		    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		    {
			    TEST_FAILED;
			    LogAllErrors(henv,hdbc,hstmt);
		    }
        }

        returncode = SQLExecute(hstmt);
        if(!CHECKRC(CDoubleToNumeric[i].PassFail,returncode,"SQLExecute"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
        if (returncode == SQL_SUCCESS || returncode ==  SQL_SUCCESS_WITH_INFO)
		{
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[8].SelTab,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				returncode = SQLFetch(hstmt);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (j = 0; j < MAX_BINDPARAM8; j++)
					{
						returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
						{
                            LogMsg(NONE,"SQLBindParameter test:checking data for column c%d\n",j+1);
							TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
						else
						{
							if (strncmp(CDoubleToNumeric[i].OutputValue[j],OutValue,strlen(CDoubleToNumeric[i].OutputValue[j])) == 0)
							{
								//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDoubleToNumeric[i].OutputValue[j],OutValue);
							}	
							else
							{
								//LogMsg(NONE,"LABS: expect: %f and actual: %f at line %d\n",atof(CDoubleToNumeric[i].OutputValue[j]), atof(OutValue),__LINE__);
								if (fabs((double)(atof(CDoubleToNumeric[i].OutputValue[j]) - atof(OutValue))) > 0.000001)
								{
                                    LogMsg(NONE,"SQLBindParameter test:checking data for column c%d\n",j+1);
									TEST_FAILED;	
									//LogMsg(NONE,"Double input value: %f\n", CDoubleToNumeric[i].DoubleValue[j]);
									LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at line %d\n",CDoubleToNumeric[i].OutputValue[j],OutValue,__LINE__);
								}
							}
						}
					} // end for loop
				}
			}
		}
		TESTCASE_END;
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
		SQLExecDirect(hstmt,(SQLCHAR*) SQLStmt[8].DrpTab,SQL_NTS);
		i++;
	}
	//=================================================================================================================
	// Section #9: convert SQL_C_CHAR to SQL_NUMERIC/SQL_DECIMAL
	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		i = 0;
		while (CDataValueTOSQL9[i].SQLType != 999)
		{
			TESTCASE_BEGIN("Setup for SQLBindParameter tests to create table for SQL_C_CHAR/SQL_C_FLOAT/SQL_C_DOUBLE TO SQL_NUMERIC/SQL_DECIMAL\n");
			SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[9].DrpTab,SQL_NTS);
            sprintf(InsStr,"%s (%s %s",SQLStmt[9].CrtTab,ColName1,CDataValueTOSQL9[i].CrtCol);
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
			}

			//LogMsg(LINEBEFORE,"Test id = %d: %s, value=%s\n", i+1, InsStr, CDataValueTOSQL9[i].CharValue);
			for (j=0; j<3; j++)
			{
                if(j == 0) sprintf(tempType,"SQL_C_CHAR");
                else if (j == 1) sprintf(tempType,"SQL_C_FLOAT");
                else if (j == 2) sprintf(tempType,"SQL_C_DOUBLE");
                else sprintf(tempType,"UNKNOWN");
			
                returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[9].DelTab,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
				
				if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
				{
					//LogMsg(NONE,"Setup for SQLBindParameter tests for prepare %s TO SQL_NUMERIC.\n",tempType);
					returncode = SQLPrepare(hstmt,(SQLCHAR*)SQLStmt[9].InsTab,SQL_NTS);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
					{
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
					}
				}

                LogMsg(NONE,"SQLBindParameter from %s TO SQL_NUMERIC.\n",tempType);
				InValue = SQL_NTS;
				if (j == 0) //SQL_C_CHAR
				{
					returncode = SQLBindParameter(hstmt,(SWORD)(1),ParamType,SQL_C_CHAR,
																		CDataValueTOSQL9[i].SQLType,
																		CDataValueTOSQL9[i].ColPrec,
																		CDataValueTOSQL9[i].ColScale,
																		CDataValueTOSQL9[i].CharValue,NAME_LEN,
																		&InValue);
				}
				else if (j == 1) //SQL_C_FLOAT
				{
					returncode = SQLBindParameter(hstmt,(SWORD)(1),ParamType,SQL_C_FLOAT,
																		CDataValueTOSQL9[i].SQLType,
																		CDataValueTOSQL9[i].ColPrec,
																		CDataValueTOSQL9[i].ColScale,
																		&(CDataValueTOSQL9[i].FloatValue),0,
																		&InValue);
				}
				else if (j == 2) //SQL_C_DOUBLE
				{
					returncode = SQLBindParameter(hstmt,(SWORD)(1),ParamType,SQL_C_DOUBLE,
																		CDataValueTOSQL9[i].SQLType,
																		CDataValueTOSQL9[i].ColPrec,
																		CDataValueTOSQL9[i].ColScale,
																		&(CDataValueTOSQL9[i].DoubleValue),0,
																		&InValue);
				}
				else {}

				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			
				if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
				{
					//LogMsg(NONE,"Setup for SQLBindParameter tests for Execute %s TO NUMERIC/DECIMAL.\n",tempType);
					returncode = SQLExecute(hstmt);
					if (j == 0) //SQL_C_CHAR
					{
						if(!CHECKRC(CDataValueTOSQL9[i].PassFail,returncode,"SQLExecute"))
						{
							TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
					}
					else
					{
						if(returncode != CDataValueTOSQL9[i].PassFail1)
						{
                            if(!CHECKRC(CDataValueTOSQL9[i].PassFail1,returncode,"SQLExecute"))
							    TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
					}

				}
				if (loop_bindparam == BINDPARAM_EXECDIRECT)
				{
					//LogMsg(NONE,"Setup for SQLBindParameter tests for ExecDirect %s TO NUMERIC/DECIMAL.\n",tempType);
					returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[9].InsTab,SQL_NTS);
					if (j == 0) //SQL_C_CHAR
					{
						if(!CHECKRC(CDataValueTOSQL9[i].PassFail,returncode,"SQLExeDirect"))
						{
							TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
					}
					else
					{
						if(returncode != CDataValueTOSQL9[i].PassFail1)
						{
                            if(!CHECKRC(CDataValueTOSQL9[i].PassFail1,returncode,"SQLExecDirect"))
							    TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
					}
				}
				if(returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO)
				{
					//LogMsg(NONE,"Setup for checking SQLBindParameter tests %s TO NUMERIC/DECIMAL.\n",tempType);
					returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[9].SelTab,SQL_NTS);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					else
					{
						returncode = SQLFetch(hstmt);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
						{
							TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
						else
						{
							returncode = SQLGetData(hstmt,(SWORD)(1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
                                LogMsg(NONE,"SQLBindParameter test:checking data for column c1\n");
								TEST_FAILED;
								LogAllErrors(henv,hdbc,hstmt);
							}
							else
							{
								if (strcmp(CDataValueTOSQL9[i].OutputValue,OutValue) == 0)
								{
									//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueTOSQL9[i].OutputValue,OutValue);
								}	
								else
								{
									if (j == 0) {
                                        LogMsg(NONE,"SQLBindParameter test:checking data for column c1\n");
										TEST_FAILED;	
										LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at line %d\n",CDataValueTOSQL9[i].OutputValue,OutValue,__LINE__);
									}
									else if (j == 1) {
										LogMsg(NONE,"LABS: expect: %f	and actual: %f , at line %d\n",atof(CDataValueTOSQL9[i].OutputValue), atof(OutValue),__LINE__);
										if (fabsf((float)(atof(CDataValueTOSQL9[i].OutputValue) - atof(OutValue))) > 0.000001)
										{
                                            LogMsg(NONE,"SQLBindParameter test:checking data for column c1\n");
											TEST_FAILED;	
											//LogMsg(NONE,"Float input value: %f\n", CDataValueTOSQL9[i].FloatValue);
											LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at line %d\n",CDataValueTOSQL9[i].OutputValue,OutValue,__LINE__);
										}
									}
									else {
										LogMsg(NONE,"LABS: expect: %f	and actual: %f , at line %d\n",atof(CDataValueTOSQL9[i].OutputValue), atof(OutValue),__LINE__);
										if (fabs((double)(atof(CDataValueTOSQL9[i].OutputValue) - atof(OutValue))) > 0.000001)
										{
                                            LogMsg(NONE,"SQLBindParameter test:checking data for column c1\n");
											TEST_FAILED;	
											//LogMsg(NONE,"Double input value: %f\n", CDataValueTOSQL9[i].DoubleValue);
											LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at line %d\n",CDataValueTOSQL9[i].OutputValue,OutValue,__LINE__);
										}
									}
								}
							}
						}
					}
				}
				SQLFreeStmt(hstmt,SQL_CLOSE);
				SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			}//End For loop (SQL_C_CHAR, SQL_C_FLOAT,SQL_C_DOUBLE)

			i++;				
			TESTCASE_END;

		}//End While loop, for each testcase
	}
	SQLFreeStmt(hstmt,SQL_CLOSE);
	SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
	SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[9].DrpTab,SQL_NTS);

	//=================================================================================================================
	// Section #10: negative test to convert all CTypes to SQL_NUMERIC (Bignum)
	TESTCASE_BEGIN("Setup for SQLBindParameter negative tests to convert all CTypes to SQL_NUMERIC (Bignum)\n");
	SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[9].DrpTab,SQL_NTS);
    sprintf(InsStr,"%s (%s %s",SQLStmt[9].CrtTab,ColName1,NColDef);    
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		i = 0;
		while (CTypeAll[i] != 999)
		{

            LogMsg(LINEAFTER,"Test id = %d: ", i+1);
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				LogMsg(LINEAFTER,"Setup for SQLBindParameter negative tests for prepare to convert all CTypes to SQL_NUMERIC (Bignum)\n");
				returncode = SQLPrepare(hstmt,(SQLCHAR*)SQLStmt[9].InsTab,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}
			}

			InValue = SQL_NTS;
			LogMsg(NONE,"SQLBindParameter from to convert from %s to SQL_NUMERIC (Bignum)\n", SQLCTypeToChar(CTypeAll[i],InsStr));

			switch (CTypeAll[i]) {
				case SQL_C_WCHAR:
					returncode = SQLBindParameter(hstmt,(SWORD)(1),SQL_PARAM_INPUT,CTypeAll[i],SQL_NUMERIC,19,0,&WcharVal,NAME_LEN,&InValue);
					break;
				case SQL_C_BINARY:
					returncode = SQLBindParameter(hstmt,(SWORD)(1),SQL_PARAM_INPUT,CTypeAll[i],SQL_NUMERIC,19,0,BinaryVal,NAME_LEN,&InValue);
					break;
				case SQL_C_BIT:
					returncode = SQLBindParameter(hstmt,(SWORD)(1),SQL_PARAM_INPUT,CTypeAll[i],SQL_NUMERIC,19,0,&BitVal,0,&InValue);
					break;
				case SQL_C_SHORT:
				case SQL_C_SSHORT:
					returncode = SQLBindParameter(hstmt,(SWORD)(1),SQL_PARAM_INPUT,CTypeAll[i],SQL_NUMERIC,19,0,&ShortVal,0,&InValue);
					break;
				case SQL_C_USHORT:
					returncode = SQLBindParameter(hstmt,(SWORD)(1),SQL_PARAM_INPUT,CTypeAll[i],SQL_NUMERIC,19,0,&UShortVal,0,&InValue);
					break;
				case SQL_C_LONG:
				case SQL_C_SLONG:
					returncode = SQLBindParameter(hstmt,(SWORD)(1),SQL_PARAM_INPUT,CTypeAll[i],SQL_NUMERIC,19,0,&LongVal,0,&InValue);
					break;
				case SQL_C_ULONG:
					returncode = SQLBindParameter(hstmt,(SWORD)(1),SQL_PARAM_INPUT,CTypeAll[i],SQL_NUMERIC,19,0,&ULongVal,0,&InValue);
					break;
				case SQL_C_TINYINT:
				case SQL_C_STINYINT:
					returncode = SQLBindParameter(hstmt,(SWORD)(1),SQL_PARAM_INPUT,CTypeAll[i],SQL_NUMERIC,19,0,&TinyIntVal,0,&InValue);
					break;
				case SQL_C_UTINYINT:
					returncode = SQLBindParameter(hstmt,(SWORD)(1),SQL_PARAM_INPUT,CTypeAll[i],SQL_NUMERIC,19,0,&UTinyIntVal,0,&InValue);
					break;
				case SQL_C_SBIGINT:
					returncode = SQLBindParameter(hstmt,(SWORD)(1),SQL_PARAM_INPUT,CTypeAll[i],SQL_NUMERIC,19,0,&BigIntVal,0,&InValue);
					break;
				case SQL_C_UBIGINT:
					returncode = SQLBindParameter(hstmt,(SWORD)(1),SQL_PARAM_INPUT,CTypeAll[i],SQL_NUMERIC,19,0,&UBigIntVal,0,&InValue);
					break;
				case SQL_C_NUMERIC:
					returncode = SQLBindParameter(hstmt,(SWORD)(1),SQL_PARAM_INPUT,CTypeAll[i],SQL_NUMERIC,19,0,&NumericVal,0,&InValue);
					break;
				case SQL_C_INTERVAL_DAY:
				case SQL_C_INTERVAL_DAY_TO_HOUR:
				case SQL_C_INTERVAL_DAY_TO_MINUTE:
				case SQL_C_INTERVAL_DAY_TO_SECOND:
				case SQL_C_INTERVAL_HOUR:
				case SQL_C_INTERVAL_HOUR_TO_MINUTE:
				case SQL_C_INTERVAL_HOUR_TO_SECOND:
				case SQL_C_INTERVAL_MINUTE:
				case SQL_C_INTERVAL_MINUTE_TO_SECOND:
				case SQL_C_INTERVAL_SECOND:
				case SQL_C_INTERVAL_MONTH:
				case SQL_C_INTERVAL_YEAR:
				case SQL_C_INTERVAL_YEAR_TO_MONTH:
					IntevalVal.intval.year_month.year = 0;
					IntevalVal.intval.year_month.month = 1;
					IntevalVal.intval.day_second.day = 2;
					IntevalVal.intval.day_second.hour = 3;
					IntevalVal.intval.day_second.minute = 4;
					IntevalVal.intval.day_second.second = 5;
					IntevalVal.intval.day_second.fraction = 6;
					returncode = SQLBindParameter(hstmt,(SWORD)(1),SQL_PARAM_INPUT,CTypeAll[i],SQL_NUMERIC,19,0,&IntevalVal,0,&InValue);
					break;
				case SQL_C_DATE:
				case SQL_C_TYPE_DATE:
					returncode = SQLBindParameter(hstmt,(SWORD)(1),SQL_PARAM_INPUT,CTypeAll[i],SQL_NUMERIC,19,0,&CDATETOSQL,0,&InValue);
					break;
				case SQL_C_TIME:
				case SQL_C_TYPE_TIME:
					returncode = SQLBindParameter(hstmt,(SWORD)(1),SQL_PARAM_INPUT,CTypeAll[i],SQL_NUMERIC,19,0,&CTIMETOSQL,0,&InValue);
					break;
				case SQL_C_TIMESTAMP:
				case SQL_C_TYPE_TIMESTAMP:
					returncode = SQLBindParameter(hstmt,(SWORD)(1),SQL_PARAM_INPUT,CTypeAll[i],SQL_NUMERIC,19,0,&CTIMESTAMPTOSQL,0,&InValue);
					break;
				default:
					break;
			}

			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
		
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				LogMsg(LINEAFTER,"Setup for SQLBindParameter negative tests for Execute to convert all CTypes to SQL_NUMERIC (Bignum)\n");
				returncode = SQLExecute(hstmt); 
				if(!CHECKRC(SQL_ERROR,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				LogMsg(LINEAFTER,"Setup for SQLBindParameter negative tests for ExecDirect to convert all CTypes to SQL_NUMERIC (Bignum)\n");
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[9].InsTab,SQL_NTS);
				if(!CHECKRC(SQL_ERROR,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}

			//LogMsg(NONE,"RETCODE=%d\n", returncode);
			//LogAllErrors(henv,hdbc,hstmt);
			i++;
			
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
		}
	}
	TESTCASE_END;
	SQLFreeStmt(hstmt,SQL_CLOSE);
	SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
	SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[9].DrpTab,SQL_NTS);

	//=================================================================================================================
	free(tempType);
	free(InsStr);
	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => MX Specific SQLBindParameter.\n");
	free_list(var_list);
	TEST_RETURN;
}


void TestMXSQLBindParamaterVer3_Cleanup(SQLHANDLE hstmt, char* DrpTab, char* tempType,
										char* InsStr, TestInfo* pTestInfo)
{
	if (strcmp(DrpTab,"") != 0)
	{
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTab,SQL_NTS);
	}
	SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
	free(tempType);
	free(InsStr);
	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => MX Specific SQLBindParameter.\n");
}
