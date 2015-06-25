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

#include "stdafx.h"
#include <time.h>
#include <stdio.h>
#ifdef __linux
#define Sleep usleep
#else
#include <windows.h>
#endif
#include <sql.h>
#include <iostream>
#include <sys/timeb.h>
#include <sqlext.h>
#include <time.h>
#include <sys/types.h>
#include <string.h>
#include <stdlib.h>

#ifdef __linux
//typedef bool BOOL;
typedef int INT;
#undef HENV
#undef HSTMT
#undef HDBC
#define HENV SQLHANDLE
#define HSTMT SQLHANDLE
#define HDBC SQLHANDLE 
#define TRUE  true
#define FALSE false
#define MAX_COMPUTERNAME_LENGTH 1024
#define _timeb timeb
#define _ftime ftime
#define ExitProcess exit

static int _stricmp(const char *s1, const char *s2)
{
  int c1, c2;

  for (;;) 
    {
      if (*s1 != *s2) 
        {
          c1 = toupper((unsigned char)*s1);
          c2 = toupper((unsigned char)*s2);

          if (c2 != c1) 
            return c2 > c1 ? -1 : 1;
        } 
      else 
        {
          if (*s1 == '\0') 
             return 0;
        }
      ++s1;
      ++s2;
    }
}
#define stricmp _stricmp

static int _strnicmp(const char *s1, const char *s2, size_t n)
{
  int c1, c2;

  for (;;) 
    {
      if (n-- == 0) 
        return 0;

      if (*s1 != *s2) 
        {
          c1 = toupper((unsigned char)*s1);
          c2 = toupper((unsigned char)*s2);

          if (c2 != c1) 
            return c2 > c1 ? -1 : 1;
        } 
      else 
        {
          if (*s1 == '\0') 
            return 0;
        }
      ++s1;
      ++s2;
    }
}

#endif

#if (SIZEOF_LONG == 8)
typedef SQLULEN UDWORD
#endif

#define SQL_MAX_DB_NAME_LEN			256
#define MAX_CONNECT_STRING      256
#define MAX_SQLSTRING_LEN				4096
#define STATE_SIZE							6
#define SQL_MAX_DRIVER_LENGTH		300
#define MAX_NUM_COLUMNS					13
#define	MAX_COLUMN_OUTPUT				300
#define	SQL_MAX_TABLE_TYPE_LEN	10
#define	SQL_MAX_REMARK_LEN			60
#define DLL_CLIENT_TABLES				5
#define DML_CLIENT_COLUMNS			10
#define MAX_NUM_TABLES					40
#define MAX_NUM_DATAVOLS				20

#define CREATE_CATALOG					0
#define	CREATE_SCHEMA						1
#define CREATE_TABLE						2
#define	INSERT_TABLE_PARAMS			3
#define INSERT_TABLE_VALUES			4
#define UPDATE_TABLE_PARAMS			5
#define UPDATE_TABLE_VALUES			6
#define SELECT_TABLE						7
#define SELECT_MULTIPLE_TABLE		8
#define DELETE_TABLE_PARAMS			9
#define DELETE_TABLE_VALUES			10
#define DROP_TABLE							11
#define CREATE_TABLE_MX					13
#define CREATE_TABLE_MP					14
#define ADD_TABLE_MP						15
#define REMOVE_TABLE_MP					16
#define DROP_TABLE_MP						17

#define	SQL_DML_INSERT					0
#define	SQL_DML_UPDATE					1
#define	SQL_DML_DELETE					2

#define	SQL_RANDOM_MAX					32767
#define MAX_INSERT_ROW_VALUE		2147483648		

#define NULL_STRING							'\0'
#define END_LOOP								"END_LOOP"
#define	END_LOOP_INT						999
#define	NO_SUBVOL								"NA"

// global struct to be used everywhere in the program.
typedef struct TestInfo 
{
   char DataSource[SQL_MAX_DSN_LENGTH];
   char UserID[SQL_MAX_USER_NAME_LEN];
   char Password[SQL_MAX_USER_NAME_LEN];
   char Database[SQL_MAX_DB_NAME_LEN];
	 char Catalog[SQL_MAX_CATALOG_NAME_LEN];
	 char Schema[SQL_MAX_SCHEMA_NAME_LEN];
	 char *Table[MAX_NUM_TABLES];
//	 char *MPTable[MAX_NUM_TABLES];
   HENV henv;
   HDBC hdbc;
   HSTMT hstmt;
} TestInfo;

TestInfo		*pTestInfo, *pTestInfoDDL;


// max sql string that can be used in this program.
char	SQLStmt[MAX_SQLSTRING_LEN];
int		Actual_Num_Columns;

// SQL Datatype
struct
{
	const char	*DataTypestr;
	SWORD	DataType;
	SWORD	CDataType;
	const char	*Name;				// column name
	BOOL	PriKey;				// primary key
	const char	*Description;
	const char	*Precision;
	const char	*Scale;
} ColumnInfo[] = 
{
	{"SQL_CHAR",SQL_CHAR,SQL_C_CHAR,"Column_Char",FALSE,"char","254",""},
//	{END_LOOP,}, use for testing
	{"SQL_VARCHAR",SQL_VARCHAR,SQL_C_CHAR,"Column_Varchar",FALSE,"varchar","254",""},
	{"SQL_DECIMAL",SQL_DECIMAL,SQL_C_CHAR,"Column_Decimal",FALSE,"decimal","18","6"},
	{"SQL_NUMERIC",SQL_NUMERIC,SQL_C_CHAR,"Column_Numeric",FALSE,"numeric","18","6"},
	{"SQL_SMALLINT",SQL_SMALLINT,SQL_C_SHORT,"Column_Smallint",FALSE,"smallint","",},
	{"SQL_INTEGER",SQL_INTEGER,SQL_C_LONG,"Column_Integer",TRUE,"integer","",},
	{"SQL_REAL",SQL_REAL,SQL_C_FLOAT,"Column_Real",FALSE,"real","",},
	{"SQL_FLOAT",SQL_FLOAT,SQL_C_DOUBLE,"Column_Float",FALSE,"float","",},
	{"SQL_DOUBLE",SQL_DOUBLE,SQL_C_DOUBLE,"Column_Double",FALSE,"double precision","",},
	{"SQL_DATE",SQL_DATE,SQL_C_DATE,"Column_Date",FALSE,"date","",},
	{"SQL_TIME",SQL_TIME,SQL_C_TIME,"Column_Time",FALSE,"time","",},
	{"SQL_TIMESTAMP",SQL_TIMESTAMP,SQL_C_TIMESTAMP,"Column_Timestamp",FALSE,"timestamp","",},
	{"SQL_BIGINT",SQL_BIGINT,SQL_C_CHAR,"Column_Bint",FALSE,"bigint","",},
	{END_LOOP,}
};

// Datatypes below are used for datatype conversion from
// SQL_C_TYPE to SQL_TYPE and viceversa.
struct 
{
	char							CharValue[254];
	char							VarCharValue[254];
	char							DecimalValue[20];
	char							NumericValue[20];
	SWORD							ShortValue;
	SQLLEN						LongValue;
	SFLOAT						RealValue;
	SDOUBLE						FloatValue;
	SDOUBLE						DoubleValue;
	DATE_STRUCT				DateValue;
	TIME_STRUCT				TimeValue;
	TIMESTAMP_STRUCT	TimestampValue;
	char							BigintValue[20];
	SQLLEN						InValue;
	SQLLEN						InValue1;
} InputOutputValues[] = 
{
	{"a","a","0","0",0,0,0,0,0,{1992,01,01},{00,00,01},{1992,01,01,00,00,01,0},"0",SQL_NTS,0},
	{"ABCDEFGHI","ABCDEFGHI","1.0","1.0",1,1,1.0,1.0,1.0,{1993,02,02},{00,01,00},{1993,02,02,00,01,00,1},"1",SQL_NTS,0},
	{"ABCDEFGHIJ","ABCDEFGHIJ","-1.0","-1.0",-1,-1,-1.0,-1.0,-1.0,{1993,03,03},{00,02,00},{1993,03,03,00,03,00,1},"-1",SQL_NTS,0},
	{"abcdefghijklmnopqrst","abcdefghijklmnopqrst","0.1","0.1",12,12,12.0,12.0,12.0,{1994,04,04},{00,04,0},{1994,04,04,00,04,00,12},"12",SQL_NTS,0},
	{"abcdefghijklmnopqrstuvwxyz","abcdefghijklmnopqrstuvwxyz","-0.1","-0.1",-12,-12,-12.0,-12.0,-12.0,{1994,05,05},{00,05,00},{1994,05,05,00,05,00,12},"-12",SQL_NTS,0},
	{"Insert Character data for row","Insert Varchar data for row","1234567.89","9876543.21",9999,0,98765.0,987654.0,98765432.0,{2000,01,01},{11,45,23},{1999,12,31,12,00,00,000000},"9876543",SQL_NTS,0},
	{END_LOOP,}
};

/*	{"CHAR","(254)","'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'","'a'","'ABCDEFGHIJ'","'abcdefghijklmnopqrst'","'ABCDEFGHIJKLMNOPQRST1234567890'","'12345678901234567890abcdefghijABCDEFGHIJabcdefghij'","'abcdefghij 1234567890 abcdefghij KLMNOPQRST 1234567890 1234567890'","'ABCDEFGHIJ_1234567890 abcdefghij KLMNOPQRST 1234567890 1234567890 UVWXYZ'","'ABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890_abcdefghij_KLMNOPQRST 1234567890_1234567890 UVWXYZ'","'ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 '","'ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 '"},
							{"VARCHAR","(254)","'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'","'a'","'ABCDEFGHIJ'","'abcdefghijklmnopqrst'","'ABCDEFGHIJKLMNOPQRST1234567890'","'12345678901234567890abcdefghijABCDEFGHIJabcdefghij'","'abcdefghij 1234567890 abcdefghij KLMNOPQRST 1234567890 1234567890'","'ABCDEFGHIJ_1234567890 abcdefghij KLMNOPQRST 1234567890 1234567890 UVWXYZ'","'ABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890_abcdefghij_KLMNOPQRST 1234567890_1234567890 UVWXYZ'","'ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 '","'ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 '"},
							{"DECIMAL","(18,6)","987654.12345","0","1.0","-0.1","1234","-9876.123","0.98765","-44444.231","33333.12345","-987654321.12345","987654321.12345"},
							{"NUMERIC","(18,6)","123456.98765","0","1.0","-0.1","1234","-9876.123","0.98765","-44444.231","33333.12345","-987654321.12345","987654321.12345"},
							{"SMALLINT","","9999","0","-1","123","-456","12345","-67890","54545","-23012","987","-6789"},
							{"INTEGER","","12345","0","-1","123","-456","12345","-67890","54545","-23012","987","-6789"},
							{"REAL","","7777.99","0","1.0","-0.1","1234","-9876.123","0.98765","-44444.231","33333.12345","-987654321.12345","987654321.12345"},
							{"FLOAT","","7777.99","0","1.0","-0.1","1234","-9876.123","0.98765","-44444.231","33333.12345","-987654321.12345","987654321.12345"},
							{"DOUBLE PRECISION","","7777.99","0","1.0","-0.1","1234","-9876.123","0.98765","-44444.231","33333.12345","-987654321.12345","987654321.12345"},
							{"DATE","","{d '1992-01-01'}","{d '1993-02-02'}","{d '1994-03-03'}","{d '1995-04-04'}","{d '1996-05-05'}","{d '1997-08-19'}","{d '1998-10-25'}","{d '1999-12-31'}","{d '2000-01-01'}"},
							{"TIME","","{t '00:00:01'}","{t '00:01:00'}","{t '01:00:00'}","{t '02:05:00'}","{t '04:03:04'}","{t '12:00:59'}","{t '11:11:11'}","{t '18:33:44'}","{t '22:55:59'}","{t '23:59:59'}"},
							{"TIMESTAMP","","{ts '1992-01-01 00:00:01'}","{ts '1993-02-02 00:01:00.1'}","{ts '1994-03-03 01:00:00.12'}","{ts '1995-04-04 02:05:00.123'}","{ts '1996-05-05 04:03:04.1234'}","{ts '1997-08-19 12:00:59.12345'}","{ts '1998-10-25 11:11:11.123456'}","{ts '1999-12-31 18:33:44.65432'}","{ts '1999-12-12 22:55:59.654321'}","{ts '2000-01-01 23:59:59.123456'}"},
*/




//SDWORD	InsertValue[MAX_NUM_TABLES] = {0,};
//SDWORD	InitialValue[MAX_NUM_TABLES] = {10,429496739,858993469,1288490199,1717986928,};
const char		*tablenamesused[MAX_NUM_TABLES] = {"TODBC","TODBC2","T_ODBC_3","TABLEodbc4","Table_ODBC_5","z","A_a_2","B3","Cc4","Create_Table_ODBC_5","TODBC5","TODBC22","T_ODBC_32","TABLEodbc42","Table_ODBC_52","z2","A_a_22","B32","Cc42","Create_Table_ODBC_52","TODBC3","TODBC23","T_ODBC_33","TABLEodbc43","Table_ODBC_53","z3","A_a_23","B33","Cc43","Create_Table_ODBC_53","TODBC4","TODBC24","T_ODBC_34","TABLEodbc44","Table_ODBC_54","z4","A_a_24","B34","Cc44","Create_Table_ODBC_54"};
//char		*MPtablenamesused[MAX_NUM_TABLES] = {"TODBC1","TODBC2","TODBC3","TODBC4","TODBC5","TODBC6","TODBC7","TODBC8","TODBC9","TODBC10","TODBC11","TODBC12","TODBC13","TODBC14","TODBC15","TODBC16","TODBC17","TODBC18","TODBC19","TODBC20","TODBC21","TODBC22","TODBC23","TODBC24","TODBC25","TODBC26","TODBC27","TODBC28","TODBC29","TODBC30","TODBC31","TODBC32","TODBC33","TODBC34","TODBC35","TODBC36","TODBC37","TODBC38","TODBC39","TODBC40"};

int		Total_Number_Of_Tables = 1;
int		Total_Clients_Per_Operation = 1;
int		Client_Number_Within_Operation = 1;
int		Total_Num_Rows = 0;
//InputOutputValues	*pInputOutputValues;

char	logfile[100];
FILE	*stream;
char	ComputerName[MAX_COMPUTERNAME_LENGTH+1];  // address of name buffer
char	ClientNumber[10];
char	ClientObjective[20];
char	ClientObjectiveNumber[20];
int		timeout;
