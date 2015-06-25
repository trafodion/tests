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
#include <stdlib.h>
#include <windows.h>
#include <sqlext.h>
#include <string.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define NAME_LEN			300
#define MAX_C_TYPES			13f
#define MAX_NUM1			27
#define MAX_NUM2			16
#define MAX_NUM3			6
#define MAX_NUM4			19
#define MAX_NUM5            13
#define	MAX_DATETIME		8
#define	MAX_TIMESTAMP		9

PassFail TestMXSQLGetData(TestInfo *pTestInfo)
{   

	TEST_DECLARE;
 	char				Heading[MAX_HEADING_SIZE];
	int					loop_bindparam;
 	RETCODE				returncode;
 	SQLHANDLE 			henv;
 	SQLHANDLE 			hdbc;
 	SQLHANDLE			hstmt;
    char                temp[MAX_STRING_SIZE];

	char				*TestSQLTypeChar[] = {
								"SQL_CHAR","SQL_VARCHAR","SQL_DECIMAL","SQL_NUMERIC","SQL_SMALLINT","SQL_SMALLINT UNSIGNED",
								"SQL_INTEGER","SQL_INTEGER UNSIGNED","SQL_REAL","SQL_FLOAT","SQL_DOUBLE","SQL_DATE",
								"SQL_TIME","SQL_TIMESTAMP","SQL_LONGVARCHAR","SQL_BIGINT",
								"SQL_NUMERIC","SQL_NUMERIC","SQL_NUMERIC","SQL_NUMERIC","SQL_NUMERIC","SQL_NUMERIC","SQL_NUMERIC","SQL_NUMERIC",
                                "SQL_CHAR","SQL_VARCHAR","SQL_LONGVARCHAR"};
	struct
	{
		SQLSMALLINT		CType;
		char			*CrtCol;
		char			*InsCol;
		char			*OutputValue[MAX_NUM1];
	} SQLDataValueTOC1[] = {// real, float and double precision to char has problem it returns 12345.0 values as 12345.
#ifndef _WM
		{SQL_C_CHAR,"--","--","--","--","1","2","-3","4","-5","6","7","8","9","1997-01-02","03:04:05","1997-06-07 08:09:10","--","10","1234567890123456789","1234567890123.456789","123456789012345678901234567890","0.12345678901234567890123456789","1234567890.12345678901234567890123456789012345678901234567890123456789","12340.56789","1234567890123.45678","12345678901234567890.0123456789","--","--","--"},
		{SQL_C_CHAR,"--","--","--","--","987.65","543.12","-987","654","-98765","65432","9876.543","345678.543","456789.543","1997-01-02","03:04:05","1997-06-07 08:09:10","--","9876543","-1234567890123456789","-1234567890123.456789","-123456789012345678901234567890","-0.12345678901234567890123456789","-1234567890.12345678901234567890123456789012345678901234567890123456789","12340.56789","1234567890123.45678","12345678901234567890.0123456789","--","--","--"},
		{SQL_C_CHAR,"--","--","--","--","1234.56789","5678.12345","-1234","6789","-12345","56789","12340","12300","12345670","1993-12-30","11:45:23","1992-12-31 23:45:23.123456","--","-9876543","1234567890123456789","123456.456789","123456789012345678901234567890","0.12345678901234567890123456789","1234567890123456789012345678901234567890123456789012345678901234.56789","12340.56789","123456789.45678","1234567890.0123456789","--","--","--"},
		{SQL_C_CHAR,"--","--","--","--","-1234.56789","-5678.12345","-1234","6789","-12345","56789","-12340","-12300","-12345670","1993-12-30","11:45:23","1992-12-31 23:45:23.123456","--","9876543","-1234567890123456789","-123456.456789","-123456789012345678901234567890","-0.12345678901234567890123456789","-1234567890123456789012345678901234567890123456789012345678901234.56789","12340.56789","123456789.45678","1234567890.0123456789","--","--","--"},
		{SQL_C_CHAR,"--","--","--","--","-0.5","-5678.12345","-1234","6789","-12345","56789","-12340","-12300","-12345670","1993-12-30","11:45:23","1992-12-31 23:45:23.123456","--","9876543","0.123456789012345678","0.1234567890123456789","123456789012345678901234567890","0.12345678901234567890123456789","1234567890.12345678901234567890123456789012345678901234567890123456789","12340.56789","1234567890123.45678","123456789.0123456789","--","--","--"},
		{SQL_C_CHAR,"--","--","--","--","0.5","-5678.12345","-1234","6789","-12345","56789","-12340","-12300","-12345670","1993-12-30","11:45:23","1992-12-31 23:45:23.123456","--","9876543","-0.123456789012345678","-0.1234567890123456789","-123456789012345678901234567890","-0.12345678901234567890123456789","-1234567890.12345678901234567890123456789012345678901234567890123456789","-12340.56789","-1234567890123.45678","-123456789.0123456789","--","--","--"},
		{SQL_C_CHAR,"--","--","--","--","-0.00001","-0.00001","-1234","6789","-12345","56789","-12340","-12300","-12345670","1993-12-30","11:45:23","1992-12-31 23:45:23.123456","--","9876543","0.123456789012345678","0.1234567890123456789","123456789012345678901234567890","0.12345678901234567890123456789","1234567890.12345678901234567890123456789012345678901234567890123456789","12340.56789","1234567890123.45678","123456789.0123456789","--","--","--"},
		{999}};
#else
		{SQL_C_CHAR,"--","--","--","--","1","2","-3","4","-5","6","7","8","9","97/01/02","03:04:05","1997-06-07 08:09:10","--","10","1234567890123456789","1234567890123.456789","123456789012345678901234567890","0.12345678901234567890123456789","1234567890.12345678901234567890123456789012345678901234567890123456789","12340.56789","1234567890123.45678","12345678901234567890.0123456789","--","--","--"},
		{SQL_C_CHAR,"--","--","--","--","987.65","543.12","-987","654","-98765","65432","9876.543","345678.543","456789.543","97/01/02","03:04:05","1997-06-07 08:09:10","--","9876543","-1234567890123456789","-1234567890123.456789","-123456789012345678901234567890","-0.12345678901234567890123456789","-1234567890.12345678901234567890123456789012345678901234567890123456789","12340.56789","1234567890123.45678","12345678901234567890.0123456789","--","--","--"},
		{SQL_C_CHAR,"--","--","--","--","1234.56789","5678.12345","-1234","6789","-12345","56789","12340","12300","12345670","93/12/30","11:45:23","1992-12-31 23:45:23.123456","--","-9876543","1234567890123456789","123456.456789","123456789012345678901234567890","0.12345678901234567890123456789","1234567890123456789012345678901234567890123456789012345678901234.56789","12340.56789","123456789.45678","1234567890.0123456789","--","--","--"},
		{SQL_C_CHAR,"--","--","--","--","-1234.56789","-5678.12345","-1234","6789","-12345","56789","-12340","-12300","-12345670","93/12/30","11:45:23","1992-12-31 23:45:23.123456","--","9876543","-1234567890123456789","-123456.456789","-123456789012345678901234567890","-0.12345678901234567890123456789","-1234567890123456789012345678901234567890123456789012345678901234.56789","12340.56789","123456789.45678","1234567890.0123456789","--","--","--"},
		{SQL_C_CHAR,"--","--","--","--","-0.5","-5678.12345","-1234","6789","-12345","56789","-12340","-12300","-12345670","93/12/30","11:45:23","1992-12-31 23:45:23.123456","--","9876543","0.123456789012345678","0.1234567890123456789","123456789012345678901234567890","0.12345678901234567890123456789","1234567890.12345678901234567890123456789012345678901234567890123456789","12340.56789","1234567890123.45678","123456789.0123456789","--","--","--"},
		{SQL_C_CHAR,"--","--","--","--","0.5","-5678.12345","-1234","6789","-12345","56789","-12340","-12300","-12345670","93/12/30","11:45:23","1992-12-31 23:45:23.123456","--","9876543","-0.123456789012345678","-0.1234567890123456789","-123456789012345678901234567890","-0.12345678901234567890123456789","-1234567890.12345678901234567890123456789012345678901234567890123456789","-12340.56789","-1234567890123.45678","-123456789.0123456789","--","--","--"},
		{SQL_C_CHAR,"--","--","--","--","-0.00001","-0.00001","-1234","6789","-12345","56789","-12340","-12300","-12345670","93/12/30","11:45:23","1992-12-31 23:45:23.123456","--","9876543","0.123456789012345678","0.1234567890123456789","123456789012345678901234567890","0.12345678901234567890123456789","1234567890.12345678901234567890123456789012345678901234567890123456789","12340.56789","1234567890123.45678","123456789.0123456789","--","--","--"},
		{999}};
#endif

	char	*CCharOutput[MAX_NUM1];
	SQLLEN	OutputLen1[MAX_NUM1]; //  

	char	*TestSQLType[] = {
				        "SQL_CHAR","SQL_VARCHAR","SQL_DECIMAL","SQL_NUMERIC","SQL_SMALLINT","SQL_SMALLINT UNSIGNED",
				        "SQL_INTEGER","SQL_INTEGER UNSIGNED","SQL_REAL","SQL_FLOAT","SQL_DOUBLE",
				        "SQL_LONGVARCHAR","SQL_BIGINT","SQL_CHAR","SQL_VARCHAR","SQL_LONGVARCHAR"};
	struct
	{
		SQLSMALLINT		CType;
		char			*CrtCol;
		char			*InsCol;
		unsigned char	OutputValue[MAX_NUM2];
	} SQLDataValueTOC2A[] = {
						{SQL_C_BIT,"--","('1','0',1.0,0.0,1,1,1,1,1,0,1,'1',1,_UCS2'1',_UCS2'0',_UCS2'1')",1,0,1,0,1,1,1,1,1,0,1,1,1,1,0,1},
						{SQL_C_UTINYINT,"--","('123','123',123,123,123,123,123,123,123,123,123,'123',123,_UCS2'123',_UCS2'123',_UCS2'123')",123,123,123,123,123,123,123,123,123,123,123,123,123,123,123,123},
						{999,}};
	struct
	{
		SQLSMALLINT CType;
		char		*CrtCol;
		char		*InsCol;
		signed char	OutputValue[MAX_NUM2];
	} SQLDataValueTOC2B[] = {
						{SQL_C_STINYINT,"--","('123','123',123,123,-123,123,-123,123,123,123,123,'123',123,_UCS2'123',_UCS2'123',_UCS2'123')",123,123,123,123,-123,123,-123,123,123,123,123,123,123,123,123,123},
						{SQL_C_STINYINT,"--","('-123','-123',-123,-123,-123,123,-123,123,-123,-123,-123,'-123',-123,_UCS2'-123',_UCS2'-123',_UCS2'-123')",-123,-123,-123,-123,-123,123,-123,123,-123,-123,-123,-123,-123,-123,-123,-123},
						{SQL_C_TINYINT,"--","('123','123',123,123,-123,123,-123,123,123,123,123,'123',123,_UCS2'123',_UCS2'123',_UCS2'123')",123,123,123,123,-123,123,-123,123,123,123,123,123,123,123,123,123},
						{SQL_C_TINYINT,"--","('-123','-123',-123,-123,-123,123,-123,123,-123,-123,-123,'-123',-123,_UCS2'-123',_UCS2'-123',_UCS2'-123')",-123,-123,-123,-123,-123,123,-123,123,-123,-123,-123,-123,-123,-123,-123,-123},
						{999,}};
	unsigned char		CBitOutput[MAX_NUM2];
	signed char			CSTinyintOutput[MAX_NUM2];
	unsigned char		CUTinyintOutput[MAX_NUM2];
	signed char			CTinyintOutput[MAX_NUM2];

	struct
	{
		SQLSMALLINT CType;
		char		*CrtCol;
		char		*InsCol;
		short int	OutputValue[MAX_NUM2];
	} SQLDataValueTOC3A[] = {
						{SQL_C_SSHORT,"--","('1234','5678',1234,5678,-1234,6789,-2345,6789,3456,6789,4567,'9012',-3456,_UCS2'1234',_UCS2'5678',_UCS2'9012')",1234,5678,1234,5678,-1234,6789,-2345,6789,3456,6789,4567,9012,-3456,1234,5678,9012},
						{SQL_C_SSHORT,"--","('-1234','-5678',-1234,-5678,-1234,6789,-2345,6789,-3456,-6789,-4567,'-9012',-3456,_UCS2'-1234',_UCS2'-5678',_UCS2'-9012')",-1234,-5678,-1234,-5678,-1234,6789,-2345,6789,-3456,-6789,-4567,-9012,-3456,-1234,-5678,-9012},
						{SQL_C_SHORT,"--","('1234','5678',1234,5678,-1234,6789,-2345,6789,3456,6789,4567,'9012',-3456,_UCS2'1234',_UCS2'5678',_UCS2'9012')",1234,5678,1234,5678,-1234,6789,-2345,6789,3456,6789,4567,9012,-3456,1234,5678,9012},
						{SQL_C_SHORT,"--","('-1234','-5678',-1234,-5678,-1234,6789,-2345,6789,-3456,-6789,-4567,'-9012',-3456,_UCS2'-1234',_UCS2'-5678',_UCS2'-9012')",-1234,-5678,-1234,-5678,-1234,6789,-2345,6789,-3456,-6789,-4567,-9012,-3456,-1234,-5678,-9012},
						{999,}};
	struct
	{
		SQLSMALLINT			CType;
		char				*CrtCol;
		char				*InsCol;
		unsigned short int	OutputValue[MAX_NUM2];
	} SQLDataValueTOC3B[] = {
						{SQL_C_USHORT,"--","('1234','5678',1234,5678,1234,6789,2345,6789,3456,6789,4567,'9012',3456,_UCS2'1234',_UCS2'5678',_UCS2'9012')",1234,5678,1234,5678,1234,6789,2345,6789,3456,6789,4567,9012,3456,1234,5678,9012},
						{999,}};
	struct
	{
		SQLSMALLINT CType;
		char		*CrtCol;
		char		*InsCol;
		long int	OutputValue[MAX_NUM2];
	} SQLDataValueTOC3C[] = {
						{SQL_C_SLONG,"--","('123456','567890',12345,56789,-1234,6789,-23456,67890,34567,67890,45678,'12345',345678,_UCS2'123456',_UCS2'567890',_UCS2'12345')",123456,567890,12345,56789,-1234,6789,-23456,67890,34567,67890,45678,12345,345678,123456,567890,12345},
						{SQL_C_SLONG,"--","('-123456','-567890',-12345,-56789,-1234,6789,-23456,67890,-34567,-67890,-45678,'-12345',-345678,_UCS2'-123456',_UCS2'-567890',_UCS2'-12345')",-123456,-567890,-12345,-56789,-1234,6789,-23456,67890,-34567,-67890,-45678,-12345,-345678,-123456,-567890,-12345},
						{SQL_C_LONG,"--","('123456','567890',12345,56789,-1234,6789,-23456,67890,34567,67890,45678,'12345',345678,_UCS2'123456',_UCS2'567890',_UCS2'12345')",123456,567890,12345,56789,-1234,6789,-23456,67890,34567,67890,45678,12345,345678,123456,567890,12345},
						{SQL_C_LONG,"--","('-123456','-567890',-12345,-56789,-1234,6789,-23456,67890,-34567,-67890,-45678,'-12345',-345678,_UCS2'-123456',_UCS2'-567890',_UCS2'-12345')",-123456,-567890,-12345,-56789,-1234,6789,-23456,67890,-34567,-67890,-45678,-12345,-345678,-123456,-567890,-12345},
						{999,}};
	struct
	{
		SQLSMALLINT			CType;
		char				*CrtCol;
		char				*InsCol;
		unsigned long int	OutputValue[MAX_NUM2];
	} SQLDataValueTOC3D[] = {
						{SQL_C_ULONG,"--","('123456','567890',12345,56789,1234,6789,23456,67890,34567,67890,45678,'123456',456789,_UCS2'123456',_UCS2'567890',_UCS2'123456')",123456,567890,12345,56789,1234,6789,23456,67890,34567,67890,45678,123456,456789,123456,567890,123456},
						{999,}};
	short int			CSShortOutput[MAX_NUM2];
	unsigned short int	CUShortOutput[MAX_NUM2];
	short int			CShortOutput[MAX_NUM2];
	int					CSLongOutput[MAX_NUM2]; //  
	unsigned int		CULongOutput[MAX_NUM2]; //  
	int					CLongOutput[MAX_NUM2]; //  

	struct
	{
		SQLSMALLINT CType;
		char		*CrtCol;
		char		*InsCol;
		float		OutputValue[MAX_NUM2];
	} SQLDataValueTOC4A[] = {
						{SQL_C_FLOAT,"--","('1234.56','5678.90',1234.56789,5678.12345,1234,6789,2345,6789,3456.12,6789.34,4567.56,'3456.89',6789,_UCS2'1234.56',_UCS2'5678.90',_UCS2'3456.89')",(float)1234.56,(float)5678.90,(float)1234.56789,(float)5678.12345,(float)1234.0,(float)6789.0,(float)2345.0,(float)6789.0,(float)3456.12,(float)6789.34,(float)4567.56,(float)3456.89,(float)6789.0,(float)1234.56,(float)5678.90,(float)3456.89},
						{SQL_C_FLOAT,"--","('-1234.56','-5678.90',-1234.56789,-5678.12345,-1234,6789,-2345,6789,-3456.12,-6789.34,-4567.56,'-3456.89',-6789,_UCS2'-1234.56',_UCS2'-5678.90',_UCS2'-3456.89')",(float)-1234.56,(float)-5678.90,(float)-1234.56789,(float)-5678.12345,(float)-1234.0,(float)6789.0,(float)-2345.0,(float)6789.0,(float)-3456.12,(float)-6789.34,(float)-4567.56,(float)-3456.89,(float)-6789.0,(float)-1234.56,(float)-5678.90,(float)-3456.89},
						{999,}};
	struct
	{
		SQLSMALLINT CType;
		char		*CrtCol;
		char		*InsCol;
		double		OutputValue[MAX_NUM2];
	} SQLDataValueTOC4B[] = {
						{SQL_C_DOUBLE,"--","('1234.56','5678.90',1234.56789,5678.12345,1234,6789,2345,6789,3456.12,6789.34,4567.56,'34567.89',67890,_UCS2'1234.56',_UCS2'5678.90',_UCS2'34567.89')",1234.56,5678.90,1234.56789,5678.12345,1234.0,6789.0,2345.0,6789.0,3456.12,6789.34,4567.56,34567.89,67890.0,1234.56,5678.90,34567.89},
						{SQL_C_DOUBLE,"--","('-1234.56','-5678.90',-1234.56789,-5678.12345,-1234,6789,-2345,6789,-3456.12,-6789.34,-4567.56,'-34567.89',-67890,_UCS2'-1234.56',_UCS2'-5678.90',_UCS2'-34567.89')",-1234.56,-5678.90,-1234.56789,-5678.12345,-1234.0,6789.0,-2345.0,6789.0,-3456.12,-6789.34,-4567.56,-34567.89,-67890.0,-1234.56,-5678.90,-34567.89},
						{999,}};

	float		CFloatOutput[MAX_NUM2];
	double		CDoubleOutput[MAX_NUM2];
	SQLLEN		OutputLen2[MAX_NUM2];

	char	*TestSQLType1[] = {"SQL_CHAR","SQL_VARCHAR","SQL_DATE","SQL_TIMESTAMP","SQL_LONGVARCHAR","SQL_CHAR","SQL_VARCHAR","SQL_LONGVARCHAR"};
	struct
	{
		SQLSMALLINT CType;
		char		*InsCol;
		int			yr[MAX_DATETIME];
		int			mn[MAX_DATETIME];
		int			dt[MAX_DATETIME];
	} SQLDataValueTOC5[] = 
						{
							{
								SQL_C_DATE,
								"('1997-10-11','1999-01-01',{d '1993-12-30'},{ts '1992-12-31 00:00:00'},'1998-04-23',_UCS2'1997-10-11',_UCS2'1999-01-01',_UCS2'1998-04-23')",
#ifndef _WM
								1997,1999,1993,1992,1998,1997,1999,1998,
#else
								1997,1999,93,1992,1998,1997,1999,1998,
#endif
								10,01,12,12,04,10,01,04,
								11,01,30,31,23,11,01,23
							},
							{
								999,
							}
						};
	DATE_STRUCT	CDateOutput[MAX_DATETIME];

	char	*TestSQLType2[] = {"SQL_CHAR","SQL_VARCHAR","SQL_TIME","SQL_TIMESTAMP","SQL_LONGVARCHAR","SQL_CHAR","SQL_VARCHAR","SQL_LONGVARCHAR"};
	struct
	{
		SQLSMALLINT CType;
		char	*InsCol;
		int		hr[MAX_DATETIME];
		int		mn[MAX_DATETIME];
		int		sc[MAX_DATETIME];
	} SQLDataValueTOC6[] = 
		{
			{
				SQL_C_TIME,
				"('03:45:04','15:29:42',{t '10:11:12'},{ts '1992-12-31 23:45:23.123456'},'12:30:56',_UCS2'03:45:04',_UCS2'15:29:42',_UCS2'12:30:56')",
				3,15,10,23,12,3,15,12,
				45,29,11,45,30,45,29,30,
				4,42,12,23,56,4,42,56
			},
			{
				999,
			}
		};
	TIME_STRUCT	CTimeOutput[MAX_DATETIME];
	
	char	*TestSQLType3[] = {"SQL_CHAR","SQL_VARCHAR","SQL_DATE","SQL_TIME","SQL_TIMESTAMP","SQL_LONGVARCHAR","SQL_CHAR","SQL_VARCHAR","SQL_LONGVARCHAR"};
	struct
	{
		SQLSMALLINT CType;
		char		*InsCol;
		SWORD		yr[MAX_TIMESTAMP];
		UWORD		mon[MAX_TIMESTAMP];
		UWORD		dt[MAX_TIMESTAMP];
		UWORD		hr[MAX_TIMESTAMP];
		UWORD		min[MAX_TIMESTAMP];
		UWORD		sc[MAX_TIMESTAMP];
		SQLULEN		fr[MAX_TIMESTAMP];
	} SQLDataValueTOC7[] = 
			{
				{
					SQL_C_TIMESTAMP,
					"('1997-10-11 03:45:04.34','1999-01-01 15:29:42.321',{d '1993-12-30'},{t '10:11:12'},{ts '1992-12-31 23:45:23.123456'},'1998-12-23 10:49:02.654321',_UCS2'1997-10-11 03:45:04.34',_UCS2'1999-01-01 15:29:42.321',_UCS2'1998-12-23 10:49:02.654321')",
#ifndef _WM
					1997,1999,1993,0,1992,1998,1997,1999,1998,
#else
					1997,1999,93,0,1992,1998,1997,1999,1998,
#endif
					10,01,12,0,12,12,10,01,12,
					11,01,30,0,31,23,11,01,23,
					3,15,0,10,23,10,3,15,10,
					45,29,0,11,45,49,45,29,49,
					4,42,0,12,23,02,4,42,02,
					340000000,321000000,0,0,123456000,654321000,340000000,321000000,654321000
				},
				{
					999,
				}
			};

	TIMESTAMP_STRUCT	CTimestampOutput[MAX_TIMESTAMP];

    char				*TestSQLTypeCharDef[] = {
								"SQL_CHAR","SQL_VARCHAR","SQL_DECIMAL","SQL_NUMERIC","SQL_SMALLINT","SQL_SMALLINT UNSIGNED",
								"SQL_INTEGER","SQL_INTEGER UNSIGNED","SQL_REAL","SQL_FLOAT","SQL_DOUBLE","SQL_DATE",
								"SQL_TIME","SQL_TIMESTAMP","SQL_LONGVARCHAR","SQL_BIGINT",
								"SQL_CHAR","SQL_VARCHAR","SQL_LONGVARCHAR"};

	struct
	{
		SQLSMALLINT					CType;
		char						*CrtCol;
		char						*InsCol;
		char						*OutputCharDef;
		char						*OutputVCharDef;
		char						*OutputDecDef;
		char						*OutputNumDef;
		signed short int			OutputSSintDef;
		unsigned short int			OutputUSintDef;
		signed long int				OutputSLintDef;
//		unsigned long int			OutputULintDef;
		char 						*OutputULintDef;
		float						OutputRealDef;
		double						OutputFloatDef;
		double						OutputDoubleDef;
		struct						tagDATE_STRUCT
		{
			signed short int	year;
			unsigned short int	month;
			unsigned short int	day;
		} OutputDateDef;
		struct					tagTIME_STRUCT
		{
			unsigned short int	hour;
			unsigned short int	minute;
			unsigned short int	second;
		} OutputTimeDef;
		struct					tagTIMESTAMP_STRUCT
		{
			signed short int	year;
			unsigned short int	month;
			unsigned short int	day;
			unsigned short int	hour;
			unsigned short int	minute;
			unsigned short int	second;
			unsigned int		fraction; //  
		} OutputTimestampDef;
		char					*OutputLVCharDef;
		char					*OutputBigintDef;
        char                    *OutputNCharDef;
        char                    *OutputNVCharDef;
        char                    *OutputNLVCharDef;
	} SQLDataValueTOCDef[] = {// real, float and double precision to char has problem it returns 12345.0 values as 12345.
			{SQL_C_DEFAULT,"--","--","--","--","1","2",-3,4,-5,"6",7,8,9,{1997,1,2},{3,4,5},{1997,6,7,8,9,10,0},"--","10","--","--","--"},
			{SQL_C_DEFAULT,"--","--","--","--","9876.54321","9876.54321",-1234,6789,-12345,"56789",(float)1234.56,98765.432,1234567.891,{1993,12,30},{11,45,23},{1992,12,31,23,45,23,123456000},"--","-9876543","--","--","--"},
			{SQL_C_DEFAULT,"--","--","--","--","1234.56789","5678.12345",-1234,6789,-12345,"56789",12340,12300,12345670,{1993,12,30},{11,45,23},{1992,12,31,23,45,23,123456000},"--","-9876543","--","--","--"},
			{SQL_C_DEFAULT,"--","--","--","--","-1234.56789","-5678.12345",-1234,6789,-12345,"56789",-12340,-12300,-12345670,{1993,12,30},{11,45,23},{1992,12,31,23,45,23,123456000},"--","9876543","--","--","--"},
			{999}};

	char					*CharDefOutput;
	char					*VCharDefOutput;
	char					*DecDefOutput;
	char					*NumDefOutput;
	signed short int		SSintDefOutput;
	unsigned short int		USintDefOutput;
	signed int				SLintDefOutput; //  
//	unsigned long int		ULintDefOutput;
	char					*ULintDefOutput;
	float					RealDefOutput;
	double					FloatDefOutput;
	double					DoubleDefOutput;
	DATE_STRUCT				DateDefOutput;
	TIME_STRUCT				TimeDefOutput;
	TIMESTAMP_STRUCT		TimestampDefOutput;
	char					*LVCharDefOutput;
	char					*BigintDefOutput;
    char                    *NCharDefOutput;
    char                    *NVCharDefOutput;
    char                    *NLVCharDefOutput;
	SQLLEN					DefOutputLen[MAX_NUM4]; //  

	char					*TestforLessBuf[] = {"SQL_CHAR","SQL_VARCHAR","SQL_LONGVARCHAR","SQL_CHAR","SQL_VARCHAR","SQL_LONGVARCHAR"};
	struct
	{
		SQLSMALLINT CType;
		SQLINTEGER	OutputLen;
		char				*CrtCol;
		char				*InsCol;
		char				*OutputValue[MAX_NUM3];
	} SQLDataValueforLessBuf[] = {// real, float and double precision to char has problem it returns 12345.0 values as 12345.
						{SQL_C_CHAR,2,"--","--","--","--","--","--","--","--"},
						{SQL_C_CHAR,10,"--","--","--","--","--","--","--","--"},
						{999}};
	char	*COutputlessBuf[MAX_NUM3];
	SQLLEN	OutputLenlessbuf[MAX_NUM3]; //  
	int		i,k;
	char	InsStr[MAX_NOS_SIZE];
	char	TempCType[MAX_COLUMN_NAME];

//************************************************
// Data structures for Testing Section #9

	int j = 0;

    struct {
		RETCODE		PassFail;
		char		*CrtCol;
        char        *InputValue;
		SFLOAT		ExpectedFloatValue[MAX_NUM5];
    } CFloatToNumeric[] = {
        {
			SQL_SUCCESS, "--",
            "12345678, 0.123456, 12.345678, 12345678, 0.123456, 1.23456, 12345678, 12345678, 0.123456, 1.234567, 12345678, 0.123456, 12345678",
            {(float)12345678.0, (float)0.123456, (float)12.345678, (float)12345678.0, (float)0.123456, (float)1.23456, (float)12345678.0, (float)12345678, (float)0.123456, (float)1.234567, (float)12345678.0, (float)0.123456, (float)12345678.0},
        },
        {
			SQL_SUCCESS, "--",
            "-123456, -0.123456, -12.345678, -123456, -0.123456, -1.234567, -123456, -123456, -0.123456, -1.234567, -123456, -0.123456, -123456",
            {(float)(-123456.0), (float)(-0.123456), (float)(-12.345678), (float)(-123456.0), (float)(-0.123456), (float)(-1.234567), (float)(-123456.0), (float)(-123456), (float)(-0.123456), (float)(-1.234567), (float)(-123456.0), (float)(-0.123456), (float)(-123456.0)},
        },
        {
			SQL_SUCCESS, "--",
            "12345678, 0.123456, 12.345678, 12345678, 0.123456, 1.234567, 12345678, 12345678, 0.123456, 1.234567, 12345678, 0.123456, 12345678",
            {(float)12345678.0, (float)0.123456, (float)12.345678, (float)12345678.0, (float)0.123456, (float)1.234567, (float)12345678.0, (float)12345678, (float)0.123456, (float)1.234567, (float)12345678.0, (float)0.123456, (float)12345678.0},
        },
        {
			SQL_SUCCESS, "--",
            "-123456.0, -12345.6, -12345.06, -1.000006, -0.000006, -1234567.0, -0.0000007, 123456.0, 12345.6, 1.000006, 0.000006, 1234567.0, 0.0000007",
            {(float)(-123456.0), (float)(-12345.6), (float)( -12345.06), (float)(-1.000006), (float)(-0.000006), (float)(-1234567.0), (float)(-0.0000007), (float)(123456.0), (float)(12345.6), (float)(1.000006), (float)(0.000006), (float)(1234567.0), (float)(0.0000007)},
        },
        {999,
        }
    };

//************************************************
    struct {
		RETCODE		PassFail;
		char		*CrtCol;
        char        *InputValue;
		SDOUBLE		ExpectedDoubleValue[MAX_NUM5];
    } CDoubleToNumeric[] = {
        {
			SQL_SUCCESS, "--",
            "123456789123456, 0.123456789123456, 12.3456789123456, 123456789123456, 0.123456789123456, 1.2345678912345, 123456789123456, 123456789123456, 0.123456789123456, 1.23456789123456, 123456789123456, 0.1234567891, 123456789123456",
            {(double)123456789123456.0, (double)0.123456789123456, (double)12.3456789123456, (double)123456789123456.0, (double)0.123456789123456, (double)1.23456789123456, (double)123456789123456.0, (double)123456789123456, (double)0.123456789123456, (double)1.23456789123456, (double)123456789123456.0, (double)0.1234567891, (double)123456789123456.0},
        },
        {
			SQL_SUCCESS, "--",
            "-123456789123456, -0.123456789123456, -12.3456789123456, -123456789123456, -0.123456789123456, -1.23456789123456, -123456789123456, -123456789123456, -0.123456789123456, -1.23456789123456, -123456789123456, -0.1234567891, -123456789123456",
            {(double)-123456789123456.0, (double)-0.123456789123456, (double)-12.3456789123456, (double)-123456789123456.0, (double)-0.123456789123456, (double)-1.23456789123456, (double)-123456789123456.0, (double)-123456789123456, (double)-0.123456789123456, (double)-1.23456789123456, (double)-123456789123456.0, (double)-0.1234567891, (double)-123456789123456.0},
        },
        {
			SQL_SUCCESS, "--",
            "12345678, 0.12345678, 12.345678, 12345678, 0.123456, 1.234567, 12345678, 12345678, 0.123456, 1.234567, 12345678, 0.123456, 12345678",
            {(double)12345678.0, (double)0.12345678, (double)12.345678, (double)12345678.0, (double)0.123456, (double)1.234567, (double)12345678.0, (double)12345678, (double)0.123456, (double)1.234567, (double)12345678.0, (double)0.123456, (double)12345678.0},
        },
        {
			SQL_SUCCESS, "--",
            "-123456789123456.0, -12345678912345.6, -12345678912345.06, -1.00000000000006, -0.000000000000006, -123456789123456.0, -0.000000000000006, 123456789123456.0, 12345678912345.6, 1.00000000000006, 0.000000000000006, 123456789123456.0, 0.000000000000006",
            {(double)-123456789123456.0, (double)-12345678912345.6, (double)-12345678912345.06, (double)-1.00000000000006, (double)-0.000000000000006, (double)-123456789123456.0, (double)-0.000000000000006, (double)123456789123456.0, (double)12345678912345.6, (double)1.00000000000006, (double)0.000000000000006, (double)123456789123456.0, (double)0.000000000000006},
        },
        {999,
        }
    };

    SQLLEN		outSize[MAX_NUM5];
	SFLOAT		FloatOutValue[MAX_NUM5];
	SDOUBLE		DoubleOutValue[MAX_NUM5];

//===========================================================================================================
// UCS2 Columns Testing

	char    *UCS2Input = "--";

	char    UCS2Output[BUFF300];
	SQLLEN  StrLen_or_IndPtr;

	struct {
        char *str;
        int expLen;
        int col1S;
        int col2S;
    }SQLUCS2ColTest[] = {
        {"--",  200,    50, 50  },
        {"--",  150,    0,  0   },
        {"--",  200,    50, 50  },
        {"--",  150,    0,  0   },
        {"--",  -9999,  0,  0   }
    };

	//===========================================================================================================
	// Negative tests to convert BIGNUM to all CTypes
	char					*WcharVal = "";
	char					*BinaryVal = "";
	unsigned char			BitVal = 0;
	short int				ShortVal = 0;
	unsigned short int		UShortVal = 0;
	int						LongVal = 0;
	unsigned int			ULongVal = 0;
	signed char				TinyIntVal = 0;
	unsigned char			UTinyIntVal = 0;
	long long int			BigIntVal = 0;
	unsigned long long int	UBigIntVal = 0;
	SQL_INTERVAL_STRUCT		IntevalVal;
	SQL_NUMERIC_STRUCT		NumericVal;

	SQLSMALLINT CTypeAll[] = {
        999,
		SQL_C_WCHAR,
		SQL_C_BINARY, SQL_C_BIT, 
		SQL_C_SHORT, SQL_C_SSHORT, SQL_C_USHORT,
		SQL_C_LONG, SQL_C_SLONG, SQL_C_ULONG,
		SQL_C_TINYINT, SQL_C_STINYINT, SQL_C_UTINYINT,
		SQL_C_SBIGINT, SQL_C_UBIGINT,
		SQL_C_NUMERIC, 
		SQL_C_DATE, SQL_C_TIME, SQL_C_TIMESTAMP,
		SQL_C_INTERVAL_DAY, SQL_C_INTERVAL_DAY_TO_HOUR, SQL_C_INTERVAL_DAY_TO_MINUTE, SQL_C_INTERVAL_DAY_TO_SECOND,
		SQL_C_INTERVAL_HOUR, SQL_C_INTERVAL_HOUR_TO_MINUTE, SQL_C_INTERVAL_HOUR_TO_SECOND,
		SQL_C_INTERVAL_MINUTE, SQL_C_INTERVAL_MINUTE_TO_SECOND, SQL_C_INTERVAL_SECOND,
		SQL_C_INTERVAL_MONTH, SQL_C_INTERVAL_YEAR, SQL_C_INTERVAL_YEAR_TO_MONTH,
		999
	};

	TIMESTAMP_STRUCT	outputTimeStamp;
	DATE_STRUCT			outputDate;
	TIME_STRUCT			outputTime;
	SQLLEN				outputSize;

//===========================================================================================================

    struct {
        char *DrpTab;
        char *CrtTab;
        char *InsTab;
        char *SelTab;
    } SQLStmt[9];

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLGetData", charset_file);
	if (var_list == NULL) return FAILED;

    i = 0;
    while (i < 9) {
        sprintf(temp,"SQLGetData_DrpTab_%d",i);
        SQLStmt[i].DrpTab = var_mapping(temp, var_list);
        sprintf(temp,"SQLGetData_CrtTab_%d",i);
        SQLStmt[i].CrtTab = var_mapping(temp, var_list);
        sprintf(temp,"SQLGetData_InsTab_%d",i);
        SQLStmt[i].InsTab = var_mapping(temp, var_list);
        sprintf(temp,"SQLGetData_SelTab_%d",i);
        SQLStmt[i].SelTab = var_mapping(temp, var_list);
        i++;
    }

    i = 0;
    while (SQLDataValueTOC1[i].CType != 999) {
        sprintf(temp,"SQLGetData_SQLDataValueTOC1_CrtCol_%d",i);
        SQLDataValueTOC1[i].CrtCol = var_mapping(temp, var_list);
        sprintf(temp,"SQLGetData_SQLDataValueTOC1_InsCol_%d",i);
        SQLDataValueTOC1[i].InsCol = var_mapping(temp, var_list);
        sprintf(temp,"SQLGetData_SQLDataValueTOC1_OutputValue0_%d",i);
        SQLDataValueTOC1[i].OutputValue[0] = var_mapping(temp, var_list);
        sprintf(temp,"SQLGetData_SQLDataValueTOC1_OutputValue1_%d",i);
        SQLDataValueTOC1[i].OutputValue[1] = var_mapping(temp, var_list);
        sprintf(temp,"SQLGetData_SQLDataValueTOC1_OutputValue14_%d",i);
        SQLDataValueTOC1[i].OutputValue[14] = var_mapping(temp, var_list);
        sprintf(temp,"SQLGetData_SQLDataValueTOC1_OutputValue24_%d",i);
        SQLDataValueTOC1[i].OutputValue[24] = var_mapping(temp, var_list);
        sprintf(temp,"SQLGetData_SQLDataValueTOC1_OutputValue25_%d",i);
        SQLDataValueTOC1[i].OutputValue[25] = var_mapping(temp, var_list);
        sprintf(temp,"SQLGetData_SQLDataValueTOC1_OutputValue26_%d",i);
        SQLDataValueTOC1[i].OutputValue[26] = var_mapping(temp, var_list);
        i++;
    }

	SQLDataValueTOC2A[0].CrtCol = var_mapping("SQLGetData_SQLDataValueTOC2A_CrtCol_0", var_list);
	SQLDataValueTOC2A[1].CrtCol = var_mapping("SQLGetData_SQLDataValueTOC2A_CrtCol_1", var_list);

	SQLDataValueTOC2B[0].CrtCol = var_mapping("SQLGetData_SQLDataValueTOC2B_CrtCol_0", var_list);
	SQLDataValueTOC2B[1].CrtCol = var_mapping("SQLGetData_SQLDataValueTOC2B_CrtCol_1", var_list);
	SQLDataValueTOC2B[2].CrtCol = var_mapping("SQLGetData_SQLDataValueTOC2B_CrtCol_2", var_list);
	SQLDataValueTOC2B[3].CrtCol = var_mapping("SQLGetData_SQLDataValueTOC2B_CrtCol_3", var_list);

	SQLDataValueTOC3A[0].CrtCol = var_mapping("SQLGetData_SQLDataValueTOC3A_CrtCol_0", var_list);
	SQLDataValueTOC3A[1].CrtCol = var_mapping("SQLGetData_SQLDataValueTOC3A_CrtCol_1", var_list);
	SQLDataValueTOC3A[2].CrtCol = var_mapping("SQLGetData_SQLDataValueTOC3A_CrtCol_2", var_list);
	SQLDataValueTOC3A[3].CrtCol = var_mapping("SQLGetData_SQLDataValueTOC3A_CrtCol_3", var_list);

	SQLDataValueTOC3B[0].CrtCol = var_mapping("SQLGetData_SQLDataValueTOC3B_CrtCol_0", var_list);

	SQLDataValueTOC3C[0].CrtCol = var_mapping("SQLGetData_SQLDataValueTOC3C_CrtCol_0", var_list);
	SQLDataValueTOC3C[1].CrtCol = var_mapping("SQLGetData_SQLDataValueTOC3C_CrtCol_1", var_list);
	SQLDataValueTOC3C[2].CrtCol = var_mapping("SQLGetData_SQLDataValueTOC3C_CrtCol_2", var_list);
	SQLDataValueTOC3C[3].CrtCol = var_mapping("SQLGetData_SQLDataValueTOC3C_CrtCol_3", var_list);

	SQLDataValueTOC3D[0].CrtCol = var_mapping("SQLGetData_SQLDataValueTOC3D_CrtCol_0", var_list);

	SQLDataValueTOC4A[0].CrtCol = var_mapping("SQLGetData_SQLDataValueTOC4A_CrtCol_0", var_list);
	SQLDataValueTOC4A[1].CrtCol = var_mapping("SQLGetData_SQLDataValueTOC4A_CrtCol_1", var_list);

	SQLDataValueTOC4B[0].CrtCol = var_mapping("SQLGetData_SQLDataValueTOC4B_CrtCol_0", var_list);
	SQLDataValueTOC4B[1].CrtCol = var_mapping("SQLGetData_SQLDataValueTOC4B_CrtCol_1", var_list);

    i = 0;
    while(SQLDataValueTOCDef[i].CType != 999) {
        sprintf(temp,"SQLGetData_SQLDataValueTOCDef_CrtCol_%d",i);              
        SQLDataValueTOCDef[i].CrtCol = var_mapping(temp, var_list);
        sprintf(temp,"SQLGetData_SQLDataValueTOCDef_InsCol_%d",i);
        SQLDataValueTOCDef[i].InsCol = var_mapping(temp, var_list);
        sprintf(temp,"SQLGetData_SQLDataValueTOCDef_OutputCharDef_%d",i);
        SQLDataValueTOCDef[i].OutputCharDef = var_mapping(temp, var_list);
        sprintf(temp,"SQLGetData_SQLDataValueTOCDef_OutputVCharDef_%d",i);
        SQLDataValueTOCDef[i].OutputVCharDef = var_mapping(temp, var_list);
        sprintf(temp,"SQLGetData_SQLDataValueTOCDef_OutputLVCharDef_%d",i);
        SQLDataValueTOCDef[i].OutputLVCharDef = var_mapping(temp, var_list);
        sprintf(temp,"SQLGetData_SQLDataValueTOCDef_OutputNCharDef_%d",i);
        SQLDataValueTOCDef[i].OutputNCharDef = var_mapping(temp, var_list);
        sprintf(temp,"SQLGetData_SQLDataValueTOCDef_OutputNVCharDef_%d",i);
        SQLDataValueTOCDef[i].OutputNVCharDef = var_mapping(temp, var_list);
        sprintf(temp,"SQLGetData_SQLDataValueTOCDef_OutputNLVCharDef_%d",i);
        SQLDataValueTOCDef[i].OutputNLVCharDef = var_mapping(temp, var_list);
        i++;
    }

	SQLDataValueforLessBuf[0].CrtCol = var_mapping("SQLGetData_SQLDataValueforLessBuf_CrtCol_0", var_list);
	SQLDataValueforLessBuf[0].InsCol = var_mapping("SQLGetData_SQLDataValueforLessBuf_InsCol_0", var_list);
	SQLDataValueforLessBuf[0].OutputValue[0] = var_mapping("SQLGetData_SQLDataValueforLessBuf_OutputValue0_0", var_list);
	SQLDataValueforLessBuf[0].OutputValue[1] = var_mapping("SQLGetData_SQLDataValueforLessBuf_OutputValue1_0", var_list);
	SQLDataValueforLessBuf[0].OutputValue[2] = var_mapping("SQLGetData_SQLDataValueforLessBuf_OutputValue2_0", var_list);
    SQLDataValueforLessBuf[0].OutputValue[3] = var_mapping("SQLGetData_SQLDataValueforLessBuf_OutputValue3_0", var_list);
	SQLDataValueforLessBuf[0].OutputValue[4] = var_mapping("SQLGetData_SQLDataValueforLessBuf_OutputValue4_0", var_list);
	SQLDataValueforLessBuf[0].OutputValue[5] = var_mapping("SQLGetData_SQLDataValueforLessBuf_OutputValue5_0", var_list);

	SQLDataValueforLessBuf[1].CrtCol = var_mapping("SQLGetData_SQLDataValueforLessBuf_CrtCol_1", var_list);
	SQLDataValueforLessBuf[1].InsCol = var_mapping("SQLGetData_SQLDataValueforLessBuf_InsCol_1", var_list);
	SQLDataValueforLessBuf[1].OutputValue[0] = var_mapping("SQLGetData_SQLDataValueforLessBuf_OutputValue0_1", var_list);
	SQLDataValueforLessBuf[1].OutputValue[1] = var_mapping("SQLGetData_SQLDataValueforLessBuf_OutputValue1_1", var_list);
	SQLDataValueforLessBuf[1].OutputValue[2] = var_mapping("SQLGetData_SQLDataValueforLessBuf_OutputValue2_1", var_list);
    SQLDataValueforLessBuf[1].OutputValue[3] = var_mapping("SQLGetData_SQLDataValueforLessBuf_OutputValue3_1", var_list);
	SQLDataValueforLessBuf[1].OutputValue[4] = var_mapping("SQLGetData_SQLDataValueforLessBuf_OutputValue4_1", var_list);
	SQLDataValueforLessBuf[1].OutputValue[5] = var_mapping("SQLGetData_SQLDataValueforLessBuf_OutputValue5_1", var_list);

	CFloatToNumeric[0].CrtCol = var_mapping("SQLGetData_CFloatToNumeric_0", var_list);
	CFloatToNumeric[1].CrtCol = var_mapping("SQLGetData_CFloatToNumeric_1", var_list);
	CFloatToNumeric[2].CrtCol = var_mapping("SQLGetData_CFloatToNumeric_2", var_list);
	CFloatToNumeric[3].CrtCol = var_mapping("SQLGetData_CFloatToNumeric_3", var_list);

	CDoubleToNumeric[0].CrtCol = var_mapping("SQLGetData_CDoubleToNumeric_0", var_list);
	CDoubleToNumeric[1].CrtCol = var_mapping("SQLGetData_CDoubleToNumeric_1", var_list);
	CDoubleToNumeric[2].CrtCol = var_mapping("SQLGetData_CDoubleToNumeric_2", var_list);
	CDoubleToNumeric[3].CrtCol = var_mapping("SQLGetData_CDoubleToNumeric_3", var_list);

    SQLUCS2ColTest[0].str = var_mapping("SQLGetData_SQLUCS2ColTest_0", var_list);
    SQLUCS2ColTest[1].str = var_mapping("SQLGetData_SQLUCS2ColTest_1", var_list);
    SQLUCS2ColTest[2].str = var_mapping("SQLGetData_SQLUCS2ColTest_2", var_list);
    SQLUCS2ColTest[3].str = var_mapping("SQLGetData_SQLUCS2ColTest_3", var_list);

    UCS2Input = var_mapping("SQLGetData_UCS2Input", var_list);

//===========================================================================================================

	if(isUCS2) {
		k = sizeof(SQLDataValueforLessBuf)/sizeof(SQLDataValueforLessBuf[0]);
		for(i = 0; i < k; i++) {
			SQLDataValueforLessBuf[i].OutputLen = SQLDataValueforLessBuf[i].OutputLen * 2;
		}
		i = 0;
		k = 0;
	}

//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API =>SQLGetData | SQLGetData | getdata.c\n");

	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLGetData tests\n");
	if(!FullConnect(pTestInfo))
	{
		LogMsg(NONE,"Unable to connect\n");
		TEST_FAILED;
		TEST_RETURN;
	}
	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
    returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	TESTCASE_END;  // end of setup

//=============================================================================================================

	k = 0;
	while (SQLDataValueTOC1[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[0].DrpTab,SQL_NTS);
		sprintf(InsStr,"%s %s",SQLStmt[0].CrtTab,SQLDataValueTOC1[k].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		strcpy(InsStr,"");
		strcat(InsStr,SQLStmt[0].InsTab);
		strcat(InsStr,SQLDataValueTOC1[k].InsCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
            LogMsg(NONE,"CrtTab: %s\nInsTab: %s\n",SQLDataValueTOC1[k].CrtCol,InsStr);
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[0].SelTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		TESTCASE_BEGIN("SQLGetData: Positive test fetch from sql to SQL_C_CHAR.\n");
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			for (i = 0; i < MAX_NUM1; i++)
			{  
				sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched.\n",i+1,TestSQLTypeChar[i],SQLCTypeToChar(SQLDataValueTOC1[k].CType,TempCType));
				TESTCASE_BEGIN(Heading);
				CCharOutput[i] = (char *)malloc(NAME_LEN);
				returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOC1[k].CType,CCharOutput[i],NAME_LEN,&OutputLen1[i]);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					if (_strnicmp(SQLDataValueTOC1[k].OutputValue[i],CCharOutput[i],strlen(SQLDataValueTOC1[k].OutputValue[i])) == 0)
					{
						//LogMsg(NONE,"expect: %s and actual: %s are matched\n",SQLDataValueTOC1[k].OutputValue[i],CCharOutput[i]);
					}	
					else
					{
						if (labs((long)(atof(SQLDataValueTOC1[k].OutputValue[i])-atof(CCharOutput[i]))) > 0.001)
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at %d \n",SQLDataValueTOC1[k].OutputValue[i],CCharOutput[i],__LINE__);
						}
					}
					TESTCASE_END;
					free(CCharOutput[i]);
				}
			}
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[0].DrpTab,SQL_NTS);
		k++;
	}

//=============================================================================================================

	k = 0;
	while (SQLDataValueTOC2A[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
		sprintf(InsStr,"%s %s",SQLStmt[1].CrtTab,SQLDataValueTOC2A[k].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		
		strcpy(InsStr,"");
		strcat(InsStr,SQLStmt[1].InsTab);
		strcat(InsStr,SQLDataValueTOC2A[k].InsCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].SelTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLDataValueTOC2A[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			for (i = 0; i < MAX_NUM2; i++)
			{  
//				RS: 7/21/05: Removed column name since no parameter provided, runtime error
				sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched.\n",i+1,TestSQLType[i],SQLCTypeToChar(SQLDataValueTOC2A[k].CType,TempCType));
				TESTCASE_BEGIN(Heading);
				switch (SQLDataValueTOC2A[k].CType)
				{
					case SQL_C_BIT:
						returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOC2A[k].CType,&CBitOutput[i],0,&OutputLen2[i]);
						break;
					case SQL_C_UTINYINT:
						returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOC2A[k].CType,&CUTinyintOutput[i],0,&OutputLen2[i]);
						break;
					default: ;
				}
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					switch (SQLDataValueTOC2A[k].CType)
					{
						case SQL_C_BIT:
							if (CBitOutput[i] == SQLDataValueTOC2A[k].OutputValue[i])
							{
								//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC2A[k].OutputValue[i],CBitOutput[i]);
							}	
							else
							{
								TEST_FAILED;	
								LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOC2A[k].OutputValue[i],CBitOutput[i],__LINE__);
							}
							break;
						case SQL_C_UTINYINT:
							if (CUTinyintOutput[i] == SQLDataValueTOC2A[k].OutputValue[i])
							{
								//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC2A[k].OutputValue[i],CUTinyintOutput[i]);
							}	
							else
							{
								TEST_FAILED;	
								LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOC2A[k].OutputValue[i],CUTinyintOutput[i],__LINE__);
							}
							break;
						default: ;
					}
				}
				TESTCASE_END;
			}
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
		k++;
	}	 

//=============================================================================================================

	k = 0;
	while (SQLDataValueTOC2B[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
		sprintf(InsStr,"%s %s",SQLStmt[1].CrtTab,SQLDataValueTOC2B[k].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		
		strcpy(InsStr,"");
		strcat(InsStr,SQLStmt[1].InsTab);
		strcat(InsStr,SQLDataValueTOC2B[k].InsCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].SelTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLDataValueTOC2B[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			for (i = 0; i < MAX_NUM2; i++)
			{  
				sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched.\n",i+1,TestSQLType[i],SQLCTypeToChar(SQLDataValueTOC2B[k].CType,TempCType));
				TESTCASE_BEGIN(Heading);
				switch (SQLDataValueTOC2B[k].CType)
				{
					case SQL_C_STINYINT:
						returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOC2B[k].CType,&CSTinyintOutput[i],0,&OutputLen2[i]);
						break;
					case SQL_C_TINYINT:
						returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOC2B[k].CType,&CTinyintOutput[i],0,&OutputLen2[i]);
						break;
					default: ;
				}
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					switch (SQLDataValueTOC2B[k].CType)
					{
						case SQL_C_STINYINT:
							if (CSTinyintOutput[i] == SQLDataValueTOC2B[k].OutputValue[i])
							{
								//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC2B[k].OutputValue[i],CSTinyintOutput[i]);
							}	
							else
							{
								TEST_FAILED;	
								LogMsg(ERRMSG,"expect: %d and actual: %c are not matched at %d\n",SQLDataValueTOC2B[k].OutputValue[i],CSTinyintOutput[i],__LINE__);
							}
							break;
						case SQL_C_TINYINT:
							if (CTinyintOutput[i] == SQLDataValueTOC2B[k].OutputValue[i])
							{
								//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC2B[k].OutputValue[i],CTinyintOutput[i]);
							}	
							else
							{
								TEST_FAILED;	
								LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOC2B[k].OutputValue[i],CTinyintOutput[i],__LINE__);
							}
							break;
						default: ;
					}
				}
				TESTCASE_END;
			}
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
		k++;
	}	 

//=============================================================================================================

	k = 0;
	while (SQLDataValueTOC3A[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
		sprintf(InsStr,"%s %s",SQLStmt[1].CrtTab,SQLDataValueTOC3A[k].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		
		strcpy(InsStr,"");
		strcat(InsStr,SQLStmt[1].InsTab);
		strcat(InsStr,SQLDataValueTOC3A[k].InsCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].SelTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLDataValueTOC3A[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			for (i = 0; i < MAX_NUM2; i++)
			{  
				sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched.\n",i+1,TestSQLType[i],SQLCTypeToChar(SQLDataValueTOC3A[k].CType,TempCType));
				TESTCASE_BEGIN(Heading);
				switch (SQLDataValueTOC3A[k].CType)
				{
					case SQL_C_SSHORT:
						returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOC3A[k].CType,&CSShortOutput[i],0,&OutputLen2[i]);
						break;
					case SQL_C_SHORT:
						returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOC3A[k].CType,&CShortOutput[i],0,&OutputLen2[i]);
						break;
					default: ;
				}
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					switch (SQLDataValueTOC3A[k].CType)
					{
						case SQL_C_SSHORT:
							if (CSShortOutput[i] == SQLDataValueTOC3A[k].OutputValue[i])
							{
								//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC3A[k].OutputValue[i],CSShortOutput[i]);
							}	
							else
							{
								TEST_FAILED;	
								LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOC3A[k].OutputValue[i],CSShortOutput[i],__LINE__);
							}
							break;
						case SQL_C_SHORT:
							if (CShortOutput[i] == SQLDataValueTOC3A[k].OutputValue[i])
							{
								//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC3A[k].OutputValue[i],CShortOutput[i]);
							}	
							else
							{
								TEST_FAILED;	
								LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOC3A[k].OutputValue[i],CShortOutput[i],__LINE__);
							}
							break;
						default: ;
					}
				}
				TESTCASE_END;
			}
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
		k++;
	}

//=============================================================================================================

	k = 0;
	while (SQLDataValueTOC3B[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
		sprintf(InsStr,"%s %s",SQLStmt[1].CrtTab,SQLDataValueTOC3B[k].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		
		strcpy(InsStr,"");
		strcat(InsStr,SQLStmt[1].InsTab);
		strcat(InsStr,SQLDataValueTOC3B[k].InsCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].SelTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLDataValueTOC3B[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			for (i = 0; i < MAX_NUM2; i++)
			{  
				sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched.\n",i+1,TestSQLType[i],SQLCTypeToChar(SQLDataValueTOC3B[k].CType,TempCType));
				TESTCASE_BEGIN(Heading);
				switch (SQLDataValueTOC3B[k].CType)
				{
					case SQL_C_USHORT:
						returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOC3B[k].CType,&CUShortOutput[i],0,&OutputLen2[i]);
						break;
					default: ;
				}
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					switch (SQLDataValueTOC3B[k].CType)
					{
						case SQL_C_USHORT:
							if (CUShortOutput[i] == SQLDataValueTOC3B[k].OutputValue[i])
							{
								//LogMsg(NONE,"expect: %u and actual: %u are matched\n",SQLDataValueTOC3B[k].OutputValue[i],CUShortOutput[i]);
							}	
							else
							{
								TEST_FAILED;	
								LogMsg(ERRMSG,"expect: %u and actual: %u are not matched at %d \n",SQLDataValueTOC3B[k].OutputValue[i],CUShortOutput[i],__LINE__);
							}
							break;
						default: ;
					}
				}
				TESTCASE_END;
			}  
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
		k++;
	}
		 
//=============================================================================================================

	k = 0;
	while (SQLDataValueTOC3C[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
		sprintf(InsStr,"%s %s",SQLStmt[1].CrtTab,SQLDataValueTOC3C[k].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		
		strcpy(InsStr,"");
		strcat(InsStr,SQLStmt[1].InsTab);
		strcat(InsStr,SQLDataValueTOC3C[k].InsCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].SelTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLDataValueTOC3C[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			for (i = 0; i < MAX_NUM2; i++)
			{  
				sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched.\n",i+1,TestSQLType[i],SQLCTypeToChar(SQLDataValueTOC3C[k].CType,TempCType));
				TESTCASE_BEGIN(Heading);
				switch (SQLDataValueTOC3C[k].CType)
				{
					case SQL_C_SLONG:
						returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOC3C[k].CType,&CSLongOutput[i],0,&OutputLen2[i]);
						break;
					case SQL_C_LONG:
						returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOC3C[k].CType,&CLongOutput[i],0,&OutputLen2[i]);
						break;
					default: ;
				}
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					switch (SQLDataValueTOC3C[k].CType)
					{
						case SQL_C_SLONG:
							if (CSLongOutput[i] == SQLDataValueTOC3C[k].OutputValue[i])
							{
								//LogMsg(NONE,"expect: %ld and actual: %ld are matched\n",SQLDataValueTOC3C[k].OutputValue[i],CSLongOutput[i]);
							}	
							else
							{
								TEST_FAILED;	
								LogMsg(ERRMSG,"expect: %ld and actual: %ld are not matched at %d \n",SQLDataValueTOC3C[k].OutputValue[i],CSLongOutput[i],__LINE__);
							}
							break;
						case SQL_C_LONG:
							if (CLongOutput[i] == SQLDataValueTOC3C[k].OutputValue[i])
							{
								//LogMsg(NONE,"expect: %ld and actual: %ld are matched\n",SQLDataValueTOC3C[k].OutputValue[i],CLongOutput[i]);
							}	
							else
							{
								TEST_FAILED;	
								LogMsg(ERRMSG,"expect: %ld and actual: %ld are not matched at %d \n",SQLDataValueTOC3C[k].OutputValue[i],CLongOutput[i],__LINE__);
							}
							break;
						default: ;
					}
				}
				TESTCASE_END;
			}  
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
		k++;
	}

//=============================================================================================================

	k = 0;
	while (SQLDataValueTOC3D[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
		sprintf(InsStr,"%s %s",SQLStmt[1].CrtTab,SQLDataValueTOC3D[k].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		
		strcpy(InsStr,"");
		strcat(InsStr,SQLStmt[1].InsTab);
		strcat(InsStr,SQLDataValueTOC3D[k].InsCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].SelTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLDataValueTOC3D[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			for (i = 0; i < MAX_NUM2; i++)
			{  
				sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched.\n",i+1,TestSQLType[i],SQLCTypeToChar(SQLDataValueTOC3D[k].CType,TempCType));
				TESTCASE_BEGIN(Heading);
				switch (SQLDataValueTOC3D[k].CType)
				{
					case SQL_C_ULONG:
						returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOC3D[k].CType,&CULongOutput[i],0,&OutputLen2[i]);
						break;
					default: ;
				}
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					switch (SQLDataValueTOC3D[k].CType)
					{
						case SQL_C_ULONG:
							if (CULongOutput[i] == SQLDataValueTOC3D[k].OutputValue[i])
							{
								//LogMsg(NONE,"expect: %lu and actual: %lu are matched\n",SQLDataValueTOC3D[k].OutputValue[i],CULongOutput[i]);
							}	
							else
							{
								TEST_FAILED;	
								LogMsg(ERRMSG,"expect: %lu and actual: %lu are not matched at %d \n",SQLDataValueTOC3D[k].OutputValue[i],CULongOutput[i],__LINE__);
							}																				 
							break;
						default: ;
					}
				}
				TESTCASE_END;
			}  
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
		k++;
	}

//=============================================================================================================

	k = 0;
	while (SQLDataValueTOC4A[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
		sprintf(InsStr,"%s %s",SQLStmt[1].CrtTab,SQLDataValueTOC4A[k].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		
		strcpy(InsStr,"");
		strcat(InsStr,SQLStmt[1].InsTab);
		strcat(InsStr,SQLDataValueTOC4A[k].InsCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].SelTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLDataValueTOC4A[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			for (i = 0; i < MAX_NUM2; i++)
			{  
				sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched.\n",i+1,TestSQLType[i],SQLCTypeToChar(SQLDataValueTOC4A[k].CType,TempCType));
				TESTCASE_BEGIN(Heading);
				switch (SQLDataValueTOC4A[k].CType)
				{
					case SQL_C_FLOAT:
						returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOC4A[k].CType,&CFloatOutput[i],0,&OutputLen2[i]);
						break;
					default: ;
				}
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					switch (SQLDataValueTOC4A[k].CType)
					{
						case SQL_C_FLOAT:
							if (CFloatOutput[i] == SQLDataValueTOC4A[k].OutputValue[i])
							{
								//LogMsg(NONE,"expect: %f and actual: %f are matched\n",SQLDataValueTOC4A[k].OutputValue[i],CFloatOutput[i]);
							}	
							else
							{
								TEST_FAILED;	
								LogMsg(ERRMSG,"expect: %f and actual: %f are not matched at %d \n",SQLDataValueTOC4A[k].OutputValue[i],CFloatOutput[i],__LINE__);
							}
							break;
						default: ;
					}
				}
				TESTCASE_END;
			}  
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
		k++;
	} 

//=============================================================================================================

	k = 0;
	while (SQLDataValueTOC4B[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
		sprintf(InsStr,"%s %s",SQLStmt[1].CrtTab,SQLDataValueTOC4B[k].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		
		strcpy(InsStr,"");
		strcat(InsStr,SQLStmt[1].InsTab);
		strcat(InsStr,SQLDataValueTOC4B[k].InsCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].SelTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLDataValueTOC4B[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			for (i = 0; i < MAX_NUM2; i++)
			{  
				sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched.\n",i+1,TestSQLType[i],SQLCTypeToChar(SQLDataValueTOC4B[k].CType,TempCType));
				TESTCASE_BEGIN(Heading);
				switch (SQLDataValueTOC4B[k].CType)
				{
					case SQL_C_DOUBLE:
						returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOC4B[k].CType,&CDoubleOutput[i],0,&OutputLen2[i]);
						break;
					default: ;
				}
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					switch (SQLDataValueTOC4B[k].CType)
					{
						case SQL_C_DOUBLE:
							if (CDoubleOutput[i] == SQLDataValueTOC4B[k].OutputValue[i])
							{
								//LogMsg(NONE,"expect: %e and actual: %e are matched\n",SQLDataValueTOC4B[k].OutputValue[i],CDoubleOutput[i]);
							}	
							else																					
							{
								if (labs((long)(SQLDataValueTOC4B[k].OutputValue[i]-CDoubleOutput[i])) > 0.0001)
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,"expect: %e and actual: %e are not matched at %d \n",SQLDataValueTOC4B[k].OutputValue[i],CDoubleOutput[i],__LINE__);
								}
							}
							break;
						default: ;
					}
				}
				TESTCASE_END;
			}  
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
		k++;
	} 

//=============================================================================================================

	k = 0;
	while (SQLDataValueTOC5[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[2].DrpTab,SQL_NTS);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[2].CrtTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		sprintf(InsStr,"%s %s",SQLStmt[2].InsTab,SQLDataValueTOC5[k].InsCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[2].SelTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLDataValueTOC5[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			for (i = 0; i < MAX_DATETIME; i++)
			{  
				sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched.\n",i+1,TestSQLType1[i],SQLCTypeToChar(SQLDataValueTOC5[k].CType,TempCType));
				TESTCASE_BEGIN(Heading);
				returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOC5[k].CType,&CDateOutput[i],0,&OutputLen2[i]);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					if ((CDateOutput[i].year == SQLDataValueTOC5[k].yr[i]) && (CDateOutput[i].month == SQLDataValueTOC5[k].mn[i]) && (CDateOutput[i].day == SQLDataValueTOC5[k].dt[i]))
					{
						//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC5[k].yr[i],CDateOutput[i].year);
						//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC5[k].mn[i],CDateOutput[i].month);
						//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC5[k].dt[i],CDateOutput[i].day);
					}	
					else
					{
						TEST_FAILED;	
						LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOC5[k].yr[i],CDateOutput[i].year,__LINE__);
						LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOC5[k].mn[i],CDateOutput[i].month,__LINE__);
						LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOC5[k].dt[i],CDateOutput[i].day,__LINE__);
					}
				}
				TESTCASE_END;
			}  
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[2].DrpTab,SQL_NTS);
		k++;
	}
					 
//=============================================================================================================

	k = 0;
	while (SQLDataValueTOC6[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[3].DrpTab,SQL_NTS);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[3].CrtTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		sprintf(InsStr,"%s %s",SQLStmt[3].InsTab,SQLDataValueTOC6[k].InsCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[3].SelTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLDataValueTOC6[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			for (i = 0; i < MAX_DATETIME; i++)
			{  
				sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched.\n",i+1,TestSQLType2[i],SQLCTypeToChar(SQLDataValueTOC6[k].CType,TempCType));
				TESTCASE_BEGIN(Heading);
				returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOC6[k].CType,&CTimeOutput[i],0,&OutputLen2[i]);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					if ((CTimeOutput[i].hour == SQLDataValueTOC6[k].hr[i]) && (CTimeOutput[i].minute == SQLDataValueTOC6[k].mn[i]) && (CTimeOutput[i].second == SQLDataValueTOC6[k].sc[i]))
					{
						//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC6[k].hr[i],CTimeOutput[i].hour);
						//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC6[k].mn[i],CTimeOutput[i].minute);
						//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC6[k].sc[i],CTimeOutput[i].second);
					}	
					else
					{
						TEST_FAILED;	
						LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOC6[k].hr[i],CTimeOutput[i].hour,__LINE__);
						LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOC6[k].mn[i],CTimeOutput[i].minute,__LINE__);
						LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOC6[k].sc[i],CTimeOutput[i].second,__LINE__);
					}
				}
				TESTCASE_END;
			}  
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[3].DrpTab,SQL_NTS);
		k++;
	}	

//=============================================================================================================

	k = 0;
	while (SQLDataValueTOC7[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[4].DrpTab,SQL_NTS);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[4].CrtTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		sprintf(InsStr,"%s %s",SQLStmt[4].InsTab,SQLDataValueTOC7[k].InsCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[4].SelTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLDataValueTOC7[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			for (i = 0; i < MAX_TIMESTAMP; i++)
			{  
				sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched.\n",i+1,TestSQLType3[i],SQLCTypeToChar(SQLDataValueTOC7[k].CType,TempCType));
				TESTCASE_BEGIN(Heading);
				returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOC7[k].CType,&CTimestampOutput[i],0,&OutputLen2[i]);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					if (i == 3) 
					{
						if ((CTimestampOutput[i].hour == SQLDataValueTOC7[k].hr[i]) 
							&& (CTimestampOutput[i].minute == SQLDataValueTOC7[k].min[i]) 
							&& (CTimestampOutput[i].second == SQLDataValueTOC7[k].sc[i])) 
						{
							//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC7[k].hr[i],CTimestampOutput[i].hour);
							//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC7[k].min[i],CTimestampOutput[i].minute);
							//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC7[k].sc[i],CTimestampOutput[i].second);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOC7[k].hr[i],CTimestampOutput[i].hour,__LINE__);
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOC7[k].min[i],CTimestampOutput[i].minute,__LINE__);
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOC7[k].sc[i],CTimestampOutput[i].second,__LINE__);
						}
					}
					else
					{
						if ((CTimestampOutput[i].year == SQLDataValueTOC7[k].yr[i]) 
							&& (CTimestampOutput[i].month == SQLDataValueTOC7[k].mon[i]) 
							&& (CTimestampOutput[i].day == SQLDataValueTOC7[k].dt[i]) 
							&& (CTimestampOutput[i].hour == SQLDataValueTOC7[k].hr[i]) 
							&& (CTimestampOutput[i].minute == SQLDataValueTOC7[k].min[i]) 
							&& (CTimestampOutput[i].second == SQLDataValueTOC7[k].sc[i]) 
							&& (CTimestampOutput[i].fraction == SQLDataValueTOC7[k].fr[i]))
						{
							/*
							LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC7[k].yr[i],CTimestampOutput[i].year);
							LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC7[k].mon[i],CTimestampOutput[i].month);
							LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC7[k].dt[i],CTimestampOutput[i].day);
							LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC7[k].hr[i],CTimestampOutput[i].hour);
							LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC7[k].min[i],CTimestampOutput[i].minute);
							LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOC7[k].sc[i],CTimestampOutput[i].second);
							LogMsg(NONE,"expect: %lu and actual: %lu are matched\n",SQLDataValueTOC7[k].fr[i],CTimestampOutput[i].fraction);
							*/
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOC7[k].yr[i],CTimestampOutput[i].year,__LINE__);
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOC7[k].mon[i],CTimestampOutput[i].month,__LINE__);
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOC7[k].dt[i],CTimestampOutput[i].day,__LINE__);
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOC7[k].hr[i],CTimestampOutput[i].hour,__LINE__);
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOC7[k].min[i],CTimestampOutput[i].minute,__LINE__);
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOC7[k].sc[i],CTimestampOutput[i].second,__LINE__);
							LogMsg(ERRMSG,"expect: %lu and actual: %lu are not matched at %d \n",SQLDataValueTOC7[k].fr[i],CTimestampOutput[i].fraction,__LINE__);
						}
					}
				}
				TESTCASE_END;
			}  
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[4].DrpTab,SQL_NTS);
		k++;
	}
	
//=============================================================================================================

	k = 0;
	while (SQLDataValueTOCDef[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[0].DrpTab,SQL_NTS);
		sprintf(InsStr,"%s %s",SQLStmt[6].CrtTab,SQLDataValueTOCDef[k].CrtCol);
		//LogMsg(NONE,"%s\n", InsStr);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		strcpy(InsStr,"");
		strcat(InsStr,SQLStmt[6].InsTab);
		strcat(InsStr,SQLDataValueTOCDef[k].InsCol);
		//LogMsg(NONE,"%s at k=%d\n", InsStr,k);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[6].SelTab,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  
			
		TESTCASE_BEGIN("SQLGetData: Positive test fetch from sql to SQL_C_DEFAULT.\n");
		
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		CharDefOutput = (char *)malloc(NAME_LEN);
		VCharDefOutput = (char *)malloc(NAME_LEN);
		DecDefOutput = (char *)malloc(NAME_LEN);
		NumDefOutput = (char *)malloc(NAME_LEN);
		LVCharDefOutput = (char *)malloc(NAME_LEN);
		BigintDefOutput = (char *)malloc(NAME_LEN);
		ULintDefOutput = (char *)malloc(NAME_LEN);
        NCharDefOutput = (char *)malloc(NAME_LEN);
		NVCharDefOutput = (char *)malloc(NAME_LEN);
        NLVCharDefOutput = (char *)malloc(NAME_LEN);

		for (i = 0; i < MAX_NUM4; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for converting %s to %s before fetch.\n",i+1,TestSQLTypeCharDef[i],SQLCTypeToChar(SQLDataValueTOCDef[k].CType,TempCType));
			TESTCASE_BEGIN(Heading);
	
			switch (i)
			{
				case 0:
					returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOCDef[k].CType,CharDefOutput,NAME_LEN,&DefOutputLen[i]);
					break;
				case 1:
					returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOCDef[k].CType,VCharDefOutput,NAME_LEN,&DefOutputLen[i]);
					break;
				case 2:
					returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOCDef[k].CType,DecDefOutput,NAME_LEN,&DefOutputLen[i]);
					break;
				case 3:
					returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOCDef[k].CType,NumDefOutput,NAME_LEN,&DefOutputLen[i]);
					break;
				case 4:
					returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOCDef[k].CType,&SSintDefOutput,0,&DefOutputLen[i]);
					break;
				case 5:
					returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOCDef[k].CType,&USintDefOutput,0,&DefOutputLen[i]);
					break;
				case 6:
					returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOCDef[k].CType,&SLintDefOutput,0,&DefOutputLen[i]);
					break;
				case 7:
					returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOCDef[k].CType,ULintDefOutput,NAME_LEN,&DefOutputLen[i]);
					break;
				case 8:
					returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOCDef[k].CType,&RealDefOutput,0,&DefOutputLen[i]);
					break;
				case 9:
					returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOCDef[k].CType,&FloatDefOutput,0,&DefOutputLen[i]);
					break;
				case 10:
					returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOCDef[k].CType,&DoubleDefOutput,0,&DefOutputLen[i]);
					break;
				case 11:
					returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOCDef[k].CType,&DateDefOutput,0,&DefOutputLen[i]);
					break;
				case 12:
					returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOCDef[k].CType,&TimeDefOutput,0,&DefOutputLen[i]);
					break;
				case 13:
					returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOCDef[k].CType,&TimestampDefOutput,0,&DefOutputLen[i]);
					break;
				case 14:
					returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOCDef[k].CType,LVCharDefOutput,NAME_LEN,&DefOutputLen[i]);
					break;
				case 15:
					returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOCDef[k].CType,BigintDefOutput,NAME_LEN,&DefOutputLen[i]);
					break;
                case 16:
					returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOCDef[k].CType,NCharDefOutput,NAME_LEN,&DefOutputLen[i]);
					break;
				case 17:
					returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOCDef[k].CType,NVCharDefOutput,NAME_LEN,&DefOutputLen[i]);
					break;
                case 18:
					returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueTOCDef[k].CType,NLVCharDefOutput,NAME_LEN,&DefOutputLen[i]);
					break;
				default: break;
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;  
		}  

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			for (i = 0; i < MAX_NUM4; i++)
			{  
				sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched.\n",i+1,TestSQLTypeCharDef[i],SQLCTypeToChar(SQLDataValueTOCDef[k].CType,TempCType));
				TESTCASE_BEGIN(Heading);
				switch (i)
				{
					case 0:
						if (_strnicmp(SQLDataValueTOCDef[k].OutputCharDef,CharDefOutput,strlen(SQLDataValueTOCDef[k].OutputCharDef)) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",SQLDataValueTOCDef[k].OutputCharDef,CharDefOutput);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at %d \n",SQLDataValueTOCDef[k].OutputCharDef,CharDefOutput,__LINE__);
						}
						break;
					case 1:
						if (stricmp(SQLDataValueTOCDef[k].OutputVCharDef,VCharDefOutput) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",SQLDataValueTOCDef[k].OutputVCharDef,VCharDefOutput);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at %d \n",SQLDataValueTOCDef[k].OutputVCharDef,VCharDefOutput,__LINE__);
						}
						break;
					case 2:
						if (strcmp(SQLDataValueTOCDef[k].OutputDecDef,DecDefOutput) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",SQLDataValueTOCDef[k].OutputDecDef,DecDefOutput);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at %d \n",SQLDataValueTOCDef[k].OutputDecDef,DecDefOutput,__LINE__);
						}
						break;
					case 3:
						if (strcmp(SQLDataValueTOCDef[k].OutputNumDef,NumDefOutput) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",SQLDataValueTOCDef[k].OutputNumDef,NumDefOutput);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at %d \n",SQLDataValueTOCDef[k].OutputNumDef,NumDefOutput,__LINE__);
						}
						break;
					case 4:
						if (SQLDataValueTOCDef[k].OutputSSintDef == SSintDefOutput)
						{
							//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOCDef[k].OutputSSintDef,SSintDefOutput);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOCDef[k].OutputSSintDef,SSintDefOutput,__LINE__);
						}
						break;
					case 5:
						if (SQLDataValueTOCDef[k].OutputUSintDef == USintDefOutput)
						{
							//LogMsg(NONE,"expect: %u and actual: %u are matched\n",SQLDataValueTOCDef[k].OutputUSintDef,USintDefOutput);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %u and actual: %u are not matched at %d \n",SQLDataValueTOCDef[k].OutputUSintDef,USintDefOutput,__LINE__);
						}
						break;
					case 6:
						if (SQLDataValueTOCDef[k].OutputSLintDef == SLintDefOutput)
						{
							//LogMsg(NONE,"expect: %ld and actual: %ld are matched\n",SQLDataValueTOCDef[k].OutputSLintDef,SLintDefOutput);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %ld and actual: %ld are not matched at %d \n",SQLDataValueTOCDef[k].OutputSLintDef,SLintDefOutput,__LINE__);
						}
						break;
					case 7:
						/*if (SQLDataValueTOCDef[k].OutputULintDef == ULintDefOutput)
						{
							LogMsg(NONE,"expect: %lu and actual: %lu are matched\n",SQLDataValueTOCDef[k].OutputULintDef,ULintDefOutput);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %lu and actual: %lu are not matched, LINE = %d\n",SQLDataValueTOCDef[k].OutputULintDef,ULintDefOutput);
						} */
						if (_strnicmp(SQLDataValueTOCDef[k].OutputULintDef,ULintDefOutput,strlen(SQLDataValueTOCDef[k].OutputULintDef)) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",SQLDataValueTOCDef[k].OutputULintDef,ULintDefOutput);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s and actual: %s are not matched, LINE = %d\n",SQLDataValueTOCDef[k].OutputULintDef,ULintDefOutput,__LINE__);
						}
						break;
					case 8:
						if (SQLDataValueTOCDef[k].OutputRealDef == RealDefOutput)
						{
							//LogMsg(NONE,"expect: %f and actual: %f are matched\n",SQLDataValueTOCDef[k].OutputRealDef,RealDefOutput);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %f and actual: %f are not matched at %d \n",SQLDataValueTOCDef[k].OutputRealDef,RealDefOutput,__LINE__);
						}
						break;
					case 9:
						if (SQLDataValueTOCDef[k].OutputFloatDef == FloatDefOutput)
						{
							//LogMsg(NONE,"expect: %e and actual: %e are matched\n",SQLDataValueTOCDef[k].OutputFloatDef,FloatDefOutput);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %e and actual: %e are not matched at %d \n",SQLDataValueTOCDef[k].OutputFloatDef,FloatDefOutput,__LINE__);
						}
						break;
					case 10:
						if (SQLDataValueTOCDef[k].OutputDoubleDef == DoubleDefOutput)
						{
							//LogMsg(NONE,"expect: %e and actual: %e are matched\n",SQLDataValueTOCDef[k].OutputDoubleDef,DoubleDefOutput);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %e and actual: %e are not matched at %d \n",SQLDataValueTOCDef[k].OutputDoubleDef,DoubleDefOutput,__LINE__);
						}
						break;
					case 11:
						if ((SQLDataValueTOCDef[k].OutputDateDef.year == DateDefOutput.year) && (SQLDataValueTOCDef[k].OutputDateDef.month == DateDefOutput.month) && (SQLDataValueTOCDef[k].OutputDateDef.day == DateDefOutput.day))
						{
							//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOCDef[k].OutputDateDef.year,DateDefOutput.year);
							//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOCDef[k].OutputDateDef.month,DateDefOutput.month);
							//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOCDef[k].OutputDateDef.day,DateDefOutput.day);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOCDef[k].OutputDateDef.year,DateDefOutput.year,__LINE__);
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOCDef[k].OutputDateDef.month,DateDefOutput.month,__LINE__);
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOCDef[k].OutputDateDef.day,DateDefOutput.day,__LINE__);
						}
						break;
					case 12:
						if ((SQLDataValueTOCDef[k].OutputTimeDef.hour == TimeDefOutput.hour) && (SQLDataValueTOCDef[k].OutputTimeDef.minute == TimeDefOutput.minute) && (SQLDataValueTOCDef[k].OutputTimeDef.second == TimeDefOutput.second))
						{
							//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOCDef[k].OutputTimeDef.hour,TimeDefOutput.hour);
							//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOCDef[k].OutputTimeDef.minute,TimeDefOutput.minute);
							//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOCDef[k].OutputTimeDef.second,TimeDefOutput.second);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOCDef[k].OutputTimeDef.hour,TimeDefOutput.hour,__LINE__);
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOCDef[k].OutputTimeDef.minute,TimeDefOutput.minute,__LINE__);
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOCDef[k].OutputTimeDef.second,TimeDefOutput.second,__LINE__);
						}
						break;
					case 13:
						if ((SQLDataValueTOCDef[k].OutputTimestampDef.year == TimestampDefOutput.year) && (SQLDataValueTOCDef[k].OutputTimestampDef.month == TimestampDefOutput.month) && (SQLDataValueTOCDef[k].OutputTimestampDef.day == TimestampDefOutput.day) && (SQLDataValueTOCDef[k].OutputTimestampDef.hour == TimestampDefOutput.hour) && (SQLDataValueTOCDef[k].OutputTimestampDef.minute == TimestampDefOutput.minute) && (SQLDataValueTOCDef[k].OutputTimestampDef.second == TimestampDefOutput.second) && (SQLDataValueTOCDef[k].OutputTimestampDef.fraction == TimestampDefOutput.fraction))
						{
							/*
							LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOCDef[k].OutputTimestampDef.year,TimestampDefOutput.year);
							LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOCDef[k].OutputTimestampDef.month,TimestampDefOutput.month);
							LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOCDef[k].OutputTimestampDef.day,TimestampDefOutput.day);
							LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOCDef[k].OutputTimestampDef.hour,TimestampDefOutput.hour);
							LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOCDef[k].OutputTimestampDef.minute,TimestampDefOutput.minute);
							LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLDataValueTOCDef[k].OutputTimestampDef.second,TimestampDefOutput.second);
							LogMsg(NONE,"expect: %lu and actual: %lu are matched\n",SQLDataValueTOCDef[k].OutputTimestampDef.fraction,TimestampDefOutput.fraction);
							*/
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %l and actual: %l are not matched at %d \n",SQLDataValueTOCDef[k].OutputTimestampDef.year,TimestampDefOutput.year,__LINE__);
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOCDef[k].OutputTimestampDef.month,TimestampDefOutput.month,__LINE__);
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOCDef[k].OutputTimestampDef.day,TimestampDefOutput.day,__LINE__);
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOCDef[k].OutputTimestampDef.hour,TimestampDefOutput.hour,__LINE__);
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOCDef[k].OutputTimestampDef.minute,TimestampDefOutput.minute,__LINE__);
							LogMsg(ERRMSG,"expect: %d and actual: %d are not matched at %d \n",SQLDataValueTOCDef[k].OutputTimestampDef.second,TimestampDefOutput.second,__LINE__);
							LogMsg(ERRMSG,"expect: %lu and actual: %lu are not matched at %d \n",SQLDataValueTOCDef[k].OutputTimestampDef.fraction,TimestampDefOutput.fraction,__LINE__);
						}
						break;
					case 14:
						if (stricmp(SQLDataValueTOCDef[k].OutputLVCharDef,LVCharDefOutput) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",SQLDataValueTOCDef[k].OutputLVCharDef,LVCharDefOutput);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at %d \n",SQLDataValueTOCDef[k].OutputLVCharDef,LVCharDefOutput,__LINE__);
						}
						break;
					case 15:
						if (strcmp(SQLDataValueTOCDef[k].OutputBigintDef,BigintDefOutput) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",SQLDataValueTOCDef[k].OutputBigintDef,BigintDefOutput);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s and actual: %s are not matched, LINE = %d\n",SQLDataValueTOCDef[k].OutputBigintDef,BigintDefOutput,__LINE__);
						}
						break;
                    case 16:
/* Windows driver is UNICODE driver, SQL_C_DEFAULT for SQL_CHAR, SQL_VARCHAR,
 * etc is mapped to SQL_C_WCHAR and needs to be handled using the UNICODE _T(),
 * and _tcsxxx() functions.  That will be tested by the UNICODE version.  The
 * ANSI version will skip this testing.
 */
#ifdef unixcli /* sq */
						if (_strnicmp(SQLDataValueTOCDef[k].OutputNCharDef,NCharDefOutput,strlen(SQLDataValueTOCDef[k].OutputNCharDef)) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",SQLDataValueTOCDef[k].OutputNCharDef,NCharDefOutput);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s and actual: %s are not matched, LINE = %d\n",SQLDataValueTOCDef[k].OutputNCharDef,NCharDefOutput,__LINE__);
						}
#endif /* sq */
						break;
					case 17:
/* Windows driver is UNICODE driver, SQL_C_DEFAULT for SQL_CHAR, SQL_VARCHAR,
 * etc is mapped to SQL_C_WCHAR and needs to be handled using the UNICODE _T(),
 * and _tcsxxx() functions.  That will be tested by the UNICODE version.  The
 * ANSI version will skip this testing.
 */
#ifdef unixcli /* sq */
						if (stricmp(SQLDataValueTOCDef[k].OutputNVCharDef,NVCharDefOutput) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",SQLDataValueTOCDef[k].OutputNVCharDef,NVCharDefOutput);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s and actual: %s are not matched, LINE = %d\n",SQLDataValueTOCDef[k].OutputNVCharDef,NVCharDefOutput,__LINE__);
						}
#endif /* sq */
						break;
                    case 18:
/* Windows driver is UNICODE driver, SQL_C_DEFAULT for SQL_CHAR, SQL_VARCHAR,
 * etc is mapped to SQL_C_WCHAR and needs to be handled using the UNICODE _T(),
 * and _tcsxxx() functions.  That will be tested by the UNICODE version.  The
 * ANSI version will skip this testing.
 */
#ifdef unixcli /* sq */
						if (stricmp(SQLDataValueTOCDef[k].OutputNLVCharDef,NLVCharDefOutput) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",SQLDataValueTOCDef[k].OutputNLVCharDef,NLVCharDefOutput);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s and actual: %s are not matched, LINE = %d\n",SQLDataValueTOCDef[k].OutputNLVCharDef,NLVCharDefOutput,__LINE__);
						}
#endif /* sq */
						break;
					default: break;
				}
				TESTCASE_END;
			}  
		}
		free(CharDefOutput);
		free(VCharDefOutput);
		free(DecDefOutput);
		free(NumDefOutput);
		free(LVCharDefOutput);
		free(BigintDefOutput);
		free(ULintDefOutput);
        free(NCharDefOutput);
		free(NVCharDefOutput);
        free(NLVCharDefOutput);
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[6].DrpTab,SQL_NTS);
		k++;
	}

//=============================================================================================================

	k = 0;
	while (SQLDataValueforLessBuf[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[5].DrpTab,SQL_NTS);
		sprintf(InsStr,"%s %s",SQLStmt[5].CrtTab,SQLDataValueforLessBuf[k].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		//LogMsg(NONE,"%s\n", InsStr);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect Create"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		strcpy(InsStr,"");
		strcat(InsStr,SQLStmt[5].InsTab);
		strcat(InsStr,SQLDataValueforLessBuf[k].InsCol);
		//LogMsg(NONE,"%s\n", InsStr);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect Insert"))
		{
            LogMsg(NONE,"CrtTab: %s\nInsTab: %s\n",SQLDataValueforLessBuf[k].CrtCol,SQLDataValueforLessBuf[k].InsCol);
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[5].SelTab,SQL_NTS);
		//LogMsg(NONE,"%s\n", SQLStmt[5].SelTab);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect Select"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		TESTCASE_BEGIN("SQLGetData: Positive test fetch from sql to SQL_C_CHAR.\n");
		
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		if (returncode == SQL_SUCCESS)
		{
			for (i = 0; i < MAX_NUM3; i++)
			{  
				sprintf(Heading,"SQLGetData: Positive test #%d for converting %s to %s after fetch and before compare.\n",i+1,TestforLessBuf[i],SQLCTypeToChar(SQLDataValueforLessBuf[k].CType,TempCType));
				TESTCASE_BEGIN(Heading);
				COutputlessBuf[i] = (char *)malloc(NAME_LEN);
				strcpy(COutputlessBuf[i],"");
				returncode = SQL_SUCCESS;
				//LogMsg(NONE,"SQLGetData(hstmt,%d,%d,'pointer',%d,%d)\n", (SWORD)(i+1),SQLDataValueforLessBuf[k].CType,SQLDataValueforLessBuf[k].OutputLen,OutputLenlessbuf[i]);
				while (returncode != SQL_NO_DATA_FOUND)
				{
					strcpy(InsStr,"");
					returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLDataValueforLessBuf[k].CType,InsStr,SQLDataValueforLessBuf[k].OutputLen,&OutputLenlessbuf[i]);
					if ( returncode != SQL_SUCCESS_WITH_INFO && returncode != SQL_SUCCESS && returncode != SQL_NO_DATA_FOUND)
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					else
						strcat(COutputlessBuf[i],InsStr);
				}
				TESTCASE_END;  
			}  
			for (i = 0; i < MAX_NUM3; i++)
			{  
				sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched and start to compare.\n",i+1,TestforLessBuf[i],SQLCTypeToChar(SQLDataValueforLessBuf[k].CType,TempCType));
				TESTCASE_BEGIN(Heading);
				if (strcmp(SQLDataValueforLessBuf[k].OutputValue[i],COutputlessBuf[i]) == 0)
				{
					//LogMsg(NONE,"expect: %s and actual: %s are matched\n",SQLDataValueforLessBuf[k].OutputValue[i],COutputlessBuf[i]);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at %d \n",SQLDataValueforLessBuf[k].OutputValue[i],COutputlessBuf[i],__LINE__);
				}
				TESTCASE_END;
				free(COutputlessBuf[i]);
			}  
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[5].DrpTab,SQL_NTS);
		k++;
	}

//=================================================================================================================
// Convert SQL_C_FLOAT to SQL_NUMERIC

    i = 0;
	while (CFloatToNumeric[i].PassFail != 999)
	{
		TESTCASE_BEGIN("SQLBindColumn tests to bind from SQL_C_FLOAT to SQL_NUMERIC.\n");
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
        sprintf(InsStr, "%s %s", SQLStmt[1].CrtTab, CFloatToNumeric[i].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}

		sprintf(InsStr, "%s (%s)", SQLStmt[1].InsTab, CFloatToNumeric[i].InputValue);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecdirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}

		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].SelTab,SQL_NTS);
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
				for (j = 0; j < MAX_NUM5; j++)
				{
					returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_FLOAT,&(FloatOutValue[j]),0,&(outSize[j]));
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
					{
                        LogMsg(NONE,"SQLGetData test:checking data for column c%d\n",j+1);
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					else
					{
						if (fabsf(CFloatToNumeric[i].ExpectedFloatValue[j]-FloatOutValue[j]) < 0.000001)
						{
							//LogMsg(NONE,"expect: %lf and actual: %lf are matched\n",CFloatToNumeric[i].ExpectedFloatValue[j],FloatOutValue[j]);
						}	
						else
						{
                            LogMsg(NONE,"SQLGetData test:checking data for column c%d\n",j+1);
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %lf and actual: %lf are not matched at line %d\n",CFloatToNumeric[i].ExpectedFloatValue[j],FloatOutValue[j],__LINE__);
						}
					}
				} 
			}
		}
		TESTCASE_END;
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
		i++;
	}

//=================================================================================================================
// Convert SQL_C_DOUBLE to SQL_NUMERIC

    i = 0;
	while (CDoubleToNumeric[i].PassFail != 999)
	{
		TESTCASE_BEGIN("SQLBindColumn tests to bind from SQL_C_DOUBLE to SQL_NUMERIC.\n");
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
        sprintf(InsStr, "%s %s", SQLStmt[1].CrtTab, CDoubleToNumeric[i].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}

		sprintf(InsStr, "%s (%s)", SQLStmt[1].InsTab, CDoubleToNumeric[i].InputValue);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecdirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}

		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].SelTab,SQL_NTS);
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
				for (j = 0; j < MAX_NUM5; j++)
				{
					returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_DOUBLE,&(DoubleOutValue[j]),0,&(outSize[j]));
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
					{
                        LogMsg(NONE,"SQLGetData test:checking data for column c%d\n",j+1);
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					else
					{
						if (fabs(CDoubleToNumeric[i].ExpectedDoubleValue[j]-DoubleOutValue[j]) < 0.000001)
						{
							//LogMsg(NONE,"expect: %lf and actual: %lf are matched\n",CDoubleToNumeric[i].ExpectedDoubleValue[j],DoubleOutValue[j]);
						}	
						else
						{
                            LogMsg(NONE,"SQLGetData test:checking data for column c%d\n",j+1);
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %lf and actual: %lf are not matched at line %d\n",CDoubleToNumeric[i].ExpectedDoubleValue[j],DoubleOutValue[j],__LINE__);
						}
					}
				} 
			}
		}
		TESTCASE_END;
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
		SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[1].DrpTab,SQL_NTS);
		i++;
	}

	//=================================================================================================================
	// Negative test to convert SQL_NUMERIC (Bignum) to all CTypes 
	TESTCASE_BEGIN("Setup for SQLGetData negative tests to convert SQL_NUMERIC (Bignum) to all CTypes\n");
	SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[8].DrpTab,SQL_NTS);
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[8].CrtTab,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[8].InsTab,SQL_NTS);
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
            LogMsg(NONE,"Test id = %d: ", i+1);
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				LogMsg(LINEAFTER,"SQLGetData negative tests for prepare to convert SQL_NUMERIC (Bignum) to all CTypes\n");
				returncode = SQLPrepare(hstmt,(SQLCHAR*)SQLStmt[8].SelTab,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}

				LogMsg(LINEAFTER,"SQLGetData negative tests for Execute to convert SQL_NUMERIC (Bignum) to all CTypes\n");
				returncode = SQLExecute(hstmt); 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				LogMsg(LINEAFTER,"SQLGetData negative tests for ExecDirect to convert SQL_NUMERIC (Bignum) to all CTypes\n");
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[8].SelTab,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}

			LogMsg(LINEAFTER,"SQLGetData negative tests for Fetch to convert SQL_NUMERIC (Bignum) to all CTypes\n");
			returncode = SQLFetch(hstmt);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}

			LogMsg(NONE,"SQLGetData from to convert from SQL_NUMERIC (Bignum) to %s\n", SQLCTypeToChar(CTypeAll[i],InsStr));
			switch (CTypeAll[i]) {
				case SQL_C_WCHAR:
					returncode = SQLGetData(hstmt,(SWORD)(1),CTypeAll[i],&WcharVal, NAME_LEN,&outputSize);
					break;
				case SQL_C_BINARY:
					returncode = SQLGetData(hstmt,(SWORD)(1),CTypeAll[i],BinaryVal, NAME_LEN,&outputSize);
					break;
				case SQL_C_BIT:
					returncode = SQLGetData(hstmt,(SWORD)(1),CTypeAll[i],&BitVal, 0,&outputSize);
					break;
				case SQL_C_SHORT:
				case SQL_C_SSHORT:
					returncode = SQLGetData(hstmt,(SWORD)(1),CTypeAll[i],&ShortVal, 0,&outputSize);
					break;
				case SQL_C_USHORT:
					returncode = SQLGetData(hstmt,(SWORD)(1),CTypeAll[i],&UShortVal, 0,&outputSize);
					break;
				case SQL_C_LONG:
				case SQL_C_SLONG:
					returncode = SQLGetData(hstmt,(SWORD)(1),CTypeAll[i],&LongVal, 0,&outputSize);
					break;
				case SQL_C_ULONG:
					returncode = SQLGetData(hstmt,(SWORD)(1),CTypeAll[i],&ULongVal, 0,&outputSize);
					break;
				case SQL_C_TINYINT:
				case SQL_C_STINYINT:
					returncode = SQLGetData(hstmt,(SWORD)(1),CTypeAll[i],&TinyIntVal, 0,&outputSize);
					break;
				case SQL_C_UTINYINT:
					returncode = SQLGetData(hstmt,(SWORD)(1),CTypeAll[i],&UTinyIntVal, 0,&outputSize);
					break;
				case SQL_C_SBIGINT:
					returncode = SQLGetData(hstmt,(SWORD)(1),CTypeAll[i],&BigIntVal, 0,&outputSize);
					break;
				case SQL_C_UBIGINT:
					returncode = SQLGetData(hstmt,(SWORD)(1),CTypeAll[i],&UBigIntVal, 0,&outputSize);
					break;
				case SQL_C_NUMERIC:
					returncode = SQLGetData(hstmt,(SWORD)(1),CTypeAll[i],&NumericVal, 0,&outputSize);
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
					returncode = SQLGetData(hstmt,(SWORD)(1),CTypeAll[i],&IntevalVal, 0,&outputSize);
					break;
				case SQL_C_DATE:
					returncode = SQLGetData(hstmt,(SWORD)(1),CTypeAll[i],&outputDate, 0,&outputSize);
					break;
				case SQL_C_TIME:
					returncode = SQLGetData(hstmt,(SWORD)(1),CTypeAll[i],&outputTime, 0,&outputSize);
					break;
				case SQL_C_TIMESTAMP:
					returncode = SQLGetData(hstmt,(SWORD)(1),CTypeAll[i],&outputTimeStamp, 0,&outputSize);
					break;
				default:
					break;
			}

			if(!CHECKRC(SQL_ERROR,returncode,"SQLBindCol"))
			{
				TEST_FAILED;
            }

		    LogAllErrors(henv,hdbc,hstmt);

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
	SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[8].DrpTab,SQL_NTS);


//=============================================================================================================
// UCS2 Columns Testing

	LogMsg(NONE,"Testing for Less-buffer SQLGetData\n");
	i = 0;
	while(SQLUCS2ColTest[i].expLen!=-9999) {

		sprintf(InsStr, "Testing CharsetDB case %d\n", i);
		TESTCASE_BEGIN(InsStr);

		// Drop initial table
        returncode = SQLExecDirect(hstmt, (SQLCHAR*)SQLStmt[7].DrpTab, SQL_NTS);

        sprintf(InsStr, "%s(%s NOT NULL NOT DROPPABLE PRIMARY KEY)", SQLStmt[7].CrtTab, SQLUCS2ColTest[i].str);
        returncode = SQLExecDirect(hstmt, (SQLCHAR*) InsStr, SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")) {
            TEST_FAILED;
            LogAllErrors(henv,hdbc,hstmt);
        }

        sprintf(InsStr, "%s (_UCS2'%s', '%s')", SQLStmt[7].InsTab, UCS2Input, UCS2Input);
        returncode = SQLExecDirect(hstmt, (SQLCHAR*) InsStr, SQL_NTS);
        if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")) {
            TEST_FAILED;
            LogAllErrors(henv,hdbc,hstmt);
        }

        returncode = SQLExecDirect(hstmt, (SQLCHAR*)SQLStmt[7].SelTab, SQL_NTS);
        if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")) {
            TEST_FAILED;
            LogAllErrors(henv,hdbc,hstmt);
        }

        returncode = SQLFetch(hstmt);
        if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) {
            TEST_FAILED;
            LogAllErrors(henv,hdbc,hstmt);
			TEST_RETURN;
        }

		j = 0;
		while (returncode != SQL_NO_DATA_FOUND) {

			// Column 1
			//LogMsg(NONE,"column 1: loop %d\n", j);
			returncode = SQLGetData(hstmt,(SWORD)(1),SQL_C_CHAR,&UCS2Output,11,&StrLen_or_IndPtr);
            if (returncode != SQL_SUCCESS && returncode != SQL_NO_DATA_FOUND && returncode != SQL_SUCCESS_WITH_INFO) {
                LogAllErrors(henv, hdbc, hstmt);
                TEST_FAILED;
            } else if (returncode == SQL_NO_DATA_FOUND) {
                break;
            }

			if(StrLen_or_IndPtr != (SQLUCS2ColTest[i].expLen - 10*j)) {
				TEST_FAILED;
				LogMsg(ERRMSG,"Expected: %d and Actual: %d\n", SQLUCS2ColTest[i].expLen, StrLen_or_IndPtr);
			}

            sprintf(temp,"%-*s",SQLUCS2ColTest[i].expLen,UCS2Input);
			strcpy(InsStr, "");
			strncpy(InsStr, (temp + 10*j), 10);
			InsStr[10] = '\0';
			//LogMsg(NONE, "Data: expected: %s and actual: %s\n", InsStr, UCS2Output);
			if(strcmp(UCS2Output, InsStr) != 0) {
				TEST_FAILED;
				LogMsg(ERRMSG,"Expected: '%s' and Actual: '%s'", InsStr, UCS2Output);
			}
			j++;
		}

		j = 0;
		returncode = SQL_SUCCESS;
		while (returncode != SQL_NO_DATA_FOUND) {

			//LogMsg(NONE,"column 2: loop %d\n", j);
			// Column 2
			returncode = SQLGetData(hstmt,(SWORD)(2),SQL_C_CHAR,&UCS2Output,11,&StrLen_or_IndPtr);
            if (returncode != SQL_SUCCESS && returncode != SQL_NO_DATA_FOUND && returncode != SQL_SUCCESS_WITH_INFO) {
                LogAllErrors(henv, hdbc, hstmt);
                TEST_FAILED;
            } else if (returncode == SQL_NO_DATA_FOUND) {
                break;
            }

			if(StrLen_or_IndPtr != (SQLUCS2ColTest[i].expLen - 10*j)) {
				TEST_FAILED;
				LogMsg(ERRMSG,"Expected: %d and Actual: %d\n", SQLUCS2ColTest[i].expLen, StrLen_or_IndPtr);
			}

			strcpy(InsStr, "");
			strncpy(InsStr, (temp + 10*j), 10);
			InsStr[10] = '\0';
			//LogMsg(NONE, "Data: expected: %s and actual: %s\n", InsStr, UCS2Output);
			if(strcmp(UCS2Output, InsStr) != 0) {
				TEST_FAILED;
				LogMsg(ERRMSG,"Expected: '%s' and Actual: '%s'", InsStr, UCS2Output);
			}
			j++;
		}

        returncode = SQLFreeStmt(hstmt, SQL_CLOSE);

        i++;
		TESTCASE_END;
    }

	SQLExecDirect(hstmt,(SQLCHAR*)SQLStmt[7].DrpTab,SQL_NTS); /* CLEANUP */

//=============================================================================================================

	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLGetData.\n");
	free_list(var_list);
	TEST_RETURN;

}
