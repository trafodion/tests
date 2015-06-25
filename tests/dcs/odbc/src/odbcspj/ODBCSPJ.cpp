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

// ODBCSPJ.cpp : Defines the entry point for the console application.
//

#include "StdAfx.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define COLNAME_LEN_MAX	129
#define	RGB_MAX_LEN		256
#define	MAX_COLS		256
#define MAX_CHAR_LEN	256
#define MAX_WCHAR_LEN	256
#define MAX_BIT_LEN		256
#define MAX_TINY_LEN	256
#define MAX_UTINY_LEN	256
#define MAX_BINARY_LEN	256
#define MAX_TABLE_SIZE	4096
#define NAME_LEN		128
#define MAX_DATA_LEN	256
#define INTMAX          10
#define CHARMAX         256
#define VARCHARMAX      4096

#ifndef FALSE
#define FALSE               0
#endif

#ifndef TRUE
#define TRUE                1
#endif

#ifdef unixcli 
  #define stricmp strcasecmp 
  #define strnicmp strncasecmp
  #define _int64 long long int
  #define _uint64 unsigned long long int
  #define WCHAR wchar_t
#endif

bool	Connect ();
void	Disconnect ();
bool	ExecDirect ();
void	LogAllErrors (SQLHENV, SQLHDBC, SQLHSTMT);
void	EnvErrorHandler (SQLHENV);
void	DBCErrorHandler (SQLHDBC);
void	StmtErrorHandler (SQLHSTMT);
void	ODBCSPJResultSetTests ();
void	getCQD(char* cqd, char* buf);

//unsigned char DSN[] = "odbc_ds";
unsigned char DSN[20];
//unsigned char USR[] = "super.super";
//unsigned char PWD[] = "me";
unsigned char USR[20];
unsigned char PWD[20];

SQLHDBC		hdbc = NULL;
SQLHENV		henv = NULL;
SQLHSTMT	hstmt = NULL;
SQLRETURN	sqlret;

char		strSQL [1000]; 
char		cat[129];
char		sch[129];

struct{
	char sProcName[256];
	unsigned int numincols;
	unsigned int numoutcols;
	unsigned int numinoutcols;
	struct{
		char ColName[256];
		unsigned int OrdinalPos;
		unsigned int ColType;
		SWORD SQLDataType;
		unsigned int SQLDateTimeSub;
		unsigned int ColSize;
		unsigned int ColNullable;
		unsigned int BufferLen;
		unsigned int DecDigits;
	}proc_cols[256];
}struct_proc;

struct DateValue
{
	short int	year;
	unsigned short int	month;
	unsigned short int	day;
};
struct TimeValue
{
	unsigned short int	hour;
	unsigned short int	minute;
	unsigned short int	second;
};

struct TimestampValue
{
	short int	year;
	unsigned short int	month;
	unsigned short int	day;
	unsigned short int	hour;
	unsigned short int	minute;
	unsigned short int	second;
	unsigned long int	fraction;
};

FILE *logfile;
int iTestsFailed, iTestsRun;
unsigned char data[MAX_COLS][MAX_DATA_LEN];

struct 
{
	char *intData;
	char *charData;
	char *wcharData;
	char *numdecData;
	char *bitData;
	char *tinyintData;
	char *smallintData;
	char *bigintData;
	char *floatData;
	char *doubleData;
	char *binaryData;
	char *dateData;
	char *timeData;
	char *timestampData;
} DataArray[] = 
	{
		{"10", "SPJRSTBL", "SPJRSTBL", "10", "1", "10", "20", "2000", "123.45", "678.98", "1", "2006-12-12", "12:12:12", "2006-12-12 12:12:12.123456"},
		{"10", "testtab", "testtab", "10", "1", "10", "20", "2000", "123.45", "678.98", "1", "2006-12-12", "12:12:12", "2006-12-12 12:12:12.123456"},
		/*
		{"-10", "testtab", "testtab", "-10", "1", "-10", "-20", "-2000", "-123.45", "-678.98", "1", "date '12-12-2006'", "time '12:12:12'", "timestamp '12-12-2006 12:12:12'"},
		{"32767", "testtab", "testtab", "104567", "1", "125", "2000", "256000", "123456.45", "678123.98", "1", "date '12-12-2006'", "time '12:12:12'", "timestamp '12-12-2006 12:12:12'"},
		*/
		{"999", }
	};


int main(int argc, char* argv[])
{
	if (argc < 4)
	{
		printf ("Enter DataSource to be used: ");
		fgets ((char *)DSN, 20, stdin);
		printf ("Enter User ID to be used: ");
		fgets ((char *)USR, 20, stdin);
		printf ("Enter Password to be used: ");
		fgets ((char *)PWD, 20, stdin);
	}
	else
	{
		strcpy ((char *)DSN, argv[1]);
		strcpy ((char *)USR, argv[2]);
		strcpy ((char *)PWD, argv[3]);
	}
	printf("Starting ODBC SPJ Tests...\n");
	//ODBCSPJTests ();
	ODBCSPJResultSetTests ();
	return 0;
}

void CallSPJ (char *sProcName)
{
	sprintf (strSQL, "{call %s()}", sProcName);
//	fprintf (logfile, strSQL);

	sqlret = SQLPrepare (hstmt, (unsigned char *)strSQL, SQL_NTS);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
	//sqlret = SQLExecDirect (hstmt, (unsigned char *)strSQL, SQL_NTS);
	sqlret = SQLExecute (hstmt);
	iTestsRun++;

	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	unsigned long iRowCount = 0;
	SQLSMALLINT iNumResCols = 0;
	unsigned short iNumResultSets = 0;

	do
	{
		char strRowData[MAX_TABLE_SIZE], strHeadings[MAX_TABLE_SIZE];
		strcpy (strHeadings, "");
		while (TRUE) 
		{
			int		icol;
			char	sColName[COLNAME_LEN_MAX];
			SWORD	iColNameLength, iSQLType, iColScale, iNullable;
			SQLULEN iColPrec;
			SQLLEN	cbOutputLen[MAX_COLS];

			strcpy (strRowData, "");

			sqlret = SQLFetch(hstmt);
			if (sqlret == SQL_NO_DATA_FOUND)
			{
				printf ("%d row(s) fetched from %d column(s)\n\n", iRowCount, iNumResCols);
				iRowCount = 0;
				iNumResCols = 0;
				break;
			}
			if (sqlret != SQL_SUCCESS && sqlret != SQL_SUCCESS_WITH_INFO) 
			{
				LogAllErrors (henv, hdbc, hstmt);
				return;
			}
			iRowCount++;

			sqlret = SQLNumResultCols (hstmt, &iNumResCols);
			if (sqlret != SQL_SUCCESS)
			{
				LogAllErrors (henv, hdbc, hstmt);
				return;
			}
			for (icol = 1; icol <= iNumResCols; icol++)
			{
				SQLCHAR		rgbDesc[RGB_MAX_LEN];
				SQLSMALLINT	pcbDesc;
				SQLLEN		pfDesc;

		 		strcpy((char*)rgbDesc,"");
				pcbDesc = 0;
				pfDesc = 0;
				DATE_STRUCT	dateData;
				TIME_STRUCT	timeData;
				TIMESTAMP_STRUCT timestampData;
				SQL_INTERVAL_STRUCT intervalData;
				char charData [MAX_CHAR_LEN];
				WCHAR wcharData [MAX_WCHAR_LEN];
				unsigned char bitData[MAX_BIT_LEN];
				SQLSMALLINT	tinyintData, shortData;
				SQLUSMALLINT utinyintData, ushortData;
				unsigned long ulData;
				long lData;
				unsigned long long ubigintData;
				long long bigintData;
				float fData;
				double doubleData;
				char binaryData[MAX_BINARY_LEN];
				char strColData[MAX_CHAR_LEN];

				sqlret = SQLDescribeCol (hstmt, icol, (SQLCHAR*)sColName, COLNAME_LEN_MAX, &iColNameLength, &iSQLType, &iColPrec, &iColScale, &iNullable);
				if (sqlret != SQL_SUCCESS)
				{
					LogAllErrors (henv, hdbc, hstmt);
					return;
				}
				sqlret = SQLColAttribute(hstmt, icol, SQL_DESC_UNSIGNED, rgbDesc, RGB_MAX_LEN, &pcbDesc, &pfDesc);
				if (sqlret != SQL_SUCCESS)
				{
					LogAllErrors (henv, hdbc, hstmt);
					return;
				}
				if (iRowCount == 1)
				{
					strcat(strHeadings, sColName);
					strcat(strHeadings, " \t");
				}

				strcpy (strColData,"");
				switch (iSQLType)
				{
					case SQL_CHAR:	
					case SQL_VARCHAR:	
					case SQL_LONGVARCHAR:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_CHAR, charData, MAX_CHAR_LEN, &cbOutputLen[icol-1]);
						sprintf (strColData, "%s \t", charData);
						break;
					case SQL_WCHAR:	
					case SQL_WVARCHAR:	
					case SQL_WLONGVARCHAR:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_WCHAR, wcharData, MAX_WCHAR_LEN, &cbOutputLen[icol-1]);
						sprintf (strColData, "%s \t", wcharData);
						break;
					case SQL_NUMERIC:	
					case SQL_DECIMAL:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_CHAR, charData, MAX_CHAR_LEN, &cbOutputLen[icol-1]);
						sprintf (strColData, "%s \t", charData);
						break;
					case SQL_BIT:		
						sqlret = SQLGetData(hstmt, icol, SQL_C_BIT, bitData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", bitData);
						break;
					case SQL_TINYINT:	
						if (pfDesc)
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_UTINYINT, &utinyintData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%d \t", utinyintData);
						}
						else
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_STINYINT, &tinyintData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%d \t", tinyintData);
						}
						break;
					case SQL_SMALLINT:	
						if (pfDesc)
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_USHORT, &ushortData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%d \t", ushortData);
						}
						else
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_SSHORT, &shortData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%d \t", shortData);
						}
						break;
					case SQL_INTEGER:	
						if (pfDesc)
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_ULONG, &ulData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%ld \t", ulData);
						}
						else
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_SLONG, &lData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%ld \t", lData);
						}
						break;
					case SQL_BIGINT:	
						if (pfDesc)
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_UBIGINT, &ubigintData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%ld \t", ubigintData);
						}
						else
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_SBIGINT, &bigintData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%ld \t", bigintData);
						}
						break;
					case SQL_REAL:		
						sqlret = SQLGetData(hstmt, icol, SQL_C_FLOAT, &fData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%f \t", fData);
						break;
					case SQL_FLOAT:		
					case SQL_DOUBLE:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_DOUBLE, &doubleData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%e \t", doubleData);
						break;
					case SQL_BINARY:	
					case SQL_VARBINARY:		
					case SQL_LONGVARBINARY:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_BINARY, &binaryData, MAX_BINARY_LEN, &cbOutputLen[icol-1]);
						sprintf (strColData, "%s \t", binaryData);
						break;
					case SQL_DATE:		
					case SQL_TYPE_DATE:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_TYPE_DATE, &dateData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d %d %d \t", dateData.year, dateData.month, dateData.day);
						break;
					case SQL_TIME:		
					case SQL_TYPE_TIME:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_TYPE_TIME, &timeData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d %d %d \t", timeData.hour, timeData.minute, timeData.second);
						break;
					case SQL_TIMESTAMP:		
					case SQL_TYPE_TIMESTAMP: 
						sqlret = SQLGetData(hstmt, icol, SQL_C_TYPE_TIMESTAMP, &timestampData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d %d %d \t", timestampData.year, timestampData.month, timestampData.day);
						break;
					case SQL_INTERVAL_YEAR:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_YEAR, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_MONTH:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_MONTH, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_YEAR_TO_MONTH:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_YEAR_TO_MONTH, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_DAY:		
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_DAY, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_HOUR:		
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_HOUR, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_MINUTE:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_MINUTE, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_SECOND:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_SECOND, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_DAY_TO_HOUR:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_DAY_TO_HOUR, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_DAY_TO_MINUTE:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_DAY_TO_MINUTE, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_DAY_TO_SECOND:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_DAY_TO_SECOND, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_HOUR_TO_MINUTE:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_HOUR_TO_MINUTE, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_HOUR_TO_SECOND:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_HOUR_TO_SECOND, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_MINUTE_TO_SECOND:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_MINUTE_TO_SECOND, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					default:
						iSQLType = SQL_CHAR;
						sqlret = SQLGetData(hstmt, icol, SQL_C_CHAR, charData, MAX_CHAR_LEN, &cbOutputLen[icol-1]);
						printf ("%s\t", charData);
						sprintf (strColData, "%s \t", charData);
						break;
				}
				if (sqlret != SQL_SUCCESS)
				{
					LogAllErrors (henv, hdbc, hstmt);
					return;
				}
				strcat(strRowData, strColData);
			}
			if (iRowCount == 1)
				printf ("%s\n", strHeadings);
			printf ("%s\n", strRowData);
		}
		iNumResultSets++;
	} while ((sqlret = SQLMoreResults(hstmt)) != SQL_NO_DATA_FOUND);
	iTestsRun++;

	printf ("%d Resultset(s) fetched\n\n", iNumResultSets);

	sqlret = SQLFreeStmt (hstmt, SQL_UNBIND);
	sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
	sqlret = SQLFreeStmt (hstmt, SQL_CLOSE);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

}

void GetResultsets ()
{
	unsigned long iRowCount = 0;
	SQLSMALLINT iNumResCols = 0;
	unsigned short iNumResultSets = 0;

	do
	{
		char strRowData[MAX_TABLE_SIZE], strHeadings[MAX_TABLE_SIZE];
		strcpy (strHeadings, "");
		while (TRUE) 
		{
			int		icol;
			char	sColName[COLNAME_LEN_MAX];
			SWORD	iColNameLength, iSQLType, iColScale, iNullable;
			SQLULEN iColPrec;
			SQLLEN	cbOutputLen[MAX_COLS];

			strcpy (strRowData, "");

			sqlret = SQLFetch(hstmt);
			if (sqlret == SQL_NO_DATA_FOUND)
			{
				printf ("%d row(s) fetched from %d column(s)\n\n", iRowCount, iNumResCols);
				iRowCount = 0;
				iNumResCols = 0;
				break;
			}
			if (sqlret != SQL_SUCCESS && sqlret != SQL_SUCCESS_WITH_INFO) 
			{
				LogAllErrors (henv, hdbc, hstmt);
				return;
			}
			iRowCount++;

			sqlret = SQLNumResultCols (hstmt, &iNumResCols);
			if (sqlret != SQL_SUCCESS)
			{
				LogAllErrors (henv, hdbc, hstmt);
				return;
			}
			for (icol = 1; icol <= iNumResCols; icol++)
			{
				SQLCHAR		rgbDesc[RGB_MAX_LEN];
				SQLSMALLINT	pcbDesc;
				SQLLEN		pfDesc;

		 		strcpy((char*)rgbDesc,"");
				pcbDesc = 0;
				pfDesc = 0;
				DATE_STRUCT	dateData;
				TIME_STRUCT	timeData;
				TIMESTAMP_STRUCT timestampData;
				SQL_INTERVAL_STRUCT intervalData;
				char charData [MAX_CHAR_LEN];
				WCHAR wcharData [MAX_WCHAR_LEN];
				unsigned char bitData[MAX_BIT_LEN];
				SQLSMALLINT	tinyintData, shortData;
				SQLUSMALLINT utinyintData, ushortData;
				unsigned long ulData;
				long lData;
				unsigned long long ubigintData;
				long long bigintData;
				float fData;
				double doubleData;
				char binaryData[MAX_BINARY_LEN];
				char strColData[MAX_CHAR_LEN];

				sqlret = SQLDescribeCol (hstmt, icol, (SQLCHAR*)sColName, COLNAME_LEN_MAX, &iColNameLength, &iSQLType, &iColPrec, &iColScale, &iNullable);
				if (sqlret != SQL_SUCCESS)
				{
					LogAllErrors (henv, hdbc, hstmt);
					return;
				}
				sqlret = SQLColAttribute(hstmt, icol, SQL_DESC_UNSIGNED, rgbDesc, RGB_MAX_LEN, &pcbDesc, &pfDesc);
				if (sqlret != SQL_SUCCESS)
				{
					LogAllErrors (henv, hdbc, hstmt);
					return;
				}
				if (iRowCount == 1)
				{
					strcat(strHeadings, sColName);
					strcat(strHeadings, " \t");
				}

	/*
				colname : sColName
				ColNameLen : iColNameLength
				SQLType : iSQLType
				ColPrec : iColPrec
				ColScale : iColScale
				ColNullable : iNullable
				SQLGetData(hstmt, 1, SQL_C_ULONG, &sCustID, 0, &cbCustID);
				SQLGetData(hstmt, 2, SQL_C_CHAR, szName, NAME_LEN, &cbName);
				SQLGetData(hstmt, 3, SQL_C_CHAR, szPhone, PHONE_LEN,&cbPhone);

				if pfDesc is 0 it is signed, if it is 1 datatype is unsigned.
	*/
				strcpy (strColData,"");
				switch (iSQLType)
				{
					case SQL_CHAR:	
					case SQL_VARCHAR:	
					case SQL_LONGVARCHAR:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_CHAR, charData, MAX_CHAR_LEN, &cbOutputLen[icol-1]);
						sprintf (strColData, "%s \t", charData);
						break;
					case SQL_WCHAR:	
					case SQL_WVARCHAR:	
					case SQL_WLONGVARCHAR:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_WCHAR, wcharData, MAX_WCHAR_LEN, &cbOutputLen[icol-1]);
						sprintf (strColData, "%s \t", wcharData);
						break;
					case SQL_NUMERIC:	
					case SQL_DECIMAL:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_CHAR, charData, MAX_CHAR_LEN, &cbOutputLen[icol-1]);
						sprintf (strColData, "%s \t", charData);
						break;
					case SQL_BIT:		
						sqlret = SQLGetData(hstmt, icol, SQL_C_BIT, bitData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", bitData);
						break;
					case SQL_TINYINT:	
						if (pfDesc)
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_UTINYINT, &utinyintData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%d \t", utinyintData);
						}
						else
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_STINYINT, &tinyintData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%d \t", tinyintData);
						}
						break;
					case SQL_SMALLINT:	
						if (pfDesc)
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_USHORT, &ushortData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%d \t", ushortData);
						}
						else
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_SSHORT, &shortData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%d \t", shortData);
						}
						break;
					case SQL_INTEGER:	
						if (pfDesc)
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_ULONG, &ulData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%ld \t", ulData);
						}
						else
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_SLONG, &lData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%ld \t", lData);
						}
						break;
					case SQL_BIGINT:	
						if (pfDesc)
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_UBIGINT, &ubigintData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%ld \t", ubigintData);
						}
						else
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_SBIGINT, &bigintData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%ld \t", bigintData);
						}
						break;
					case SQL_REAL:		
						sqlret = SQLGetData(hstmt, icol, SQL_C_FLOAT, &fData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%f \t", fData);
						break;
					case SQL_FLOAT:		
					case SQL_DOUBLE:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_DOUBLE, &doubleData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%e \t", doubleData);
						break;
					case SQL_BINARY:	
					case SQL_VARBINARY:		
					case SQL_LONGVARBINARY:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_BINARY, &binaryData, MAX_BINARY_LEN, &cbOutputLen[icol-1]);
						sprintf (strColData, "%s \t", binaryData);
						break;
					case SQL_DATE:		
					case SQL_TYPE_DATE:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_TYPE_DATE, &dateData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d %d %d \t", dateData.year, dateData.month, dateData.day);
						break;
					case SQL_TIME:		
					case SQL_TYPE_TIME:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_TYPE_TIME, &timeData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d %d %d \t", timeData.hour, timeData.minute, timeData.second);
						break;
					case SQL_TIMESTAMP:		
					case SQL_TYPE_TIMESTAMP: 
						sqlret = SQLGetData(hstmt, icol, SQL_C_TYPE_TIMESTAMP, &timestampData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d %d %d \t", timestampData.year, timestampData.month, timestampData.day);
						break;
					case SQL_INTERVAL_YEAR:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_YEAR, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_MONTH:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_MONTH, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_YEAR_TO_MONTH:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_YEAR_TO_MONTH, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_DAY:		
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_DAY, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_HOUR:		
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_HOUR, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_MINUTE:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_MINUTE, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_SECOND:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_SECOND, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_DAY_TO_HOUR:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_DAY_TO_HOUR, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_DAY_TO_MINUTE:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_DAY_TO_MINUTE, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_DAY_TO_SECOND:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_DAY_TO_SECOND, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_HOUR_TO_MINUTE:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_HOUR_TO_MINUTE, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_HOUR_TO_SECOND:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_HOUR_TO_SECOND, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_MINUTE_TO_SECOND:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_MINUTE_TO_SECOND, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					default:
						iSQLType = SQL_CHAR;
						sqlret = SQLGetData(hstmt, icol, SQL_C_CHAR, charData, MAX_CHAR_LEN, &cbOutputLen[icol-1]);
						printf ("%s\t", charData);
						sprintf (strColData, "%s \t", charData);
						break;
				}
				if (sqlret != SQL_SUCCESS)
				{
					LogAllErrors (henv, hdbc, hstmt);
					return;
				}
				strcat(strRowData, strColData);
			}
			if (iRowCount == 1)
				printf ("%s\n", strHeadings);
			printf ("%s\n", strRowData);
		}
		iNumResultSets++;
	} while ((sqlret = SQLMoreResults(hstmt)) != SQL_NO_DATA_FOUND);
	iTestsRun++;

	printf ("%d Resultset(s) fetched\n\n", iNumResultSets);

}

void CallSPJsWithDiffData ()
{
	int numcols = struct_proc.numincols + struct_proc.numinoutcols + struct_proc.numoutcols;
	if (numcols == 0)
	{
		printf("======>>>>>>NO PARAM: %s\n", struct_proc.sProcName);
		CallSPJ (struct_proc.sProcName);
	}
	else if ((struct_proc.numincols > 0) && (struct_proc.numinoutcols + struct_proc.numoutcols == 0))
	{
		int k = 0;
		char strCall[1000];
		while (TRUE)
		{	 //passing values for IN params
			if (strcmp (DataArray[k].intData, "999") == 0)
				break;
			sprintf (strCall, "call %s (", struct_proc.sProcName);
			bool first = TRUE;
			
			for (int i = 0; i < numcols; i++)
			{
				if (first == FALSE)
					strcat (strCall, ", ");
				else first = FALSE;
				if (struct_proc.proc_cols[i].ColType == SQL_PARAM_INPUT)
				{
						switch (struct_proc.proc_cols[i].SQLDataType)
						{
							case SQL_CHAR: 
							case SQL_VARCHAR:	
							case SQL_LONGVARCHAR:	
								strcat (strCall, "'");
								if (strcmp(struct_proc.sProcName, "N1336") == 0) {
									strcat (strCall, "testtab1");
								}
								else {
									strcat (strCall, DataArray[k].charData);
								}
								strcat (strCall, "'");
								break;
							case SQL_WCHAR:	
							case SQL_WVARCHAR:	
							case SQL_WLONGVARCHAR:	
								strcat (strCall, "'");
								strcat (strCall, DataArray[k].wcharData);
								strcat (strCall, "'");
								break;
							case SQL_NUMERIC:	
							case SQL_DECIMAL:	
								strcat (strCall, DataArray[k].numdecData);
								break;
							case SQL_BIT:		
								strcat (strCall, DataArray[k].bitData);
								break;
							case SQL_TINYINT:	
								strcat (strCall, DataArray[k].tinyintData);
								break;
							case SQL_SMALLINT:	
								strcat (strCall, DataArray[k].smallintData);
								break;
							case SQL_INTEGER:	
								strcat (strCall, DataArray[k].intData);
								break;
							case SQL_BIGINT:	
								strcat (strCall, DataArray[k].bigintData);
								break;
							case SQL_REAL:		
								strcat (strCall, DataArray[k].floatData);
								break;
							case SQL_FLOAT:		
							case SQL_DOUBLE:	
								strcat (strCall, DataArray[k].doubleData);
								break;
							case SQL_BINARY:	
							case SQL_VARBINARY:		
							case SQL_LONGVARBINARY:	
								strcat (strCall, DataArray[k].binaryData);
								break;
							case SQL_DATE:		
							case SQL_TYPE_DATE:	
								strcat (strCall, "Date '");
								strcat (strCall, DataArray[k].dateData);
								strcat (strCall, "'");
								break;
							case SQL_TIME:		
							case SQL_TYPE_TIME:	
								strcat (strCall, "Time '");
								strcat (strCall, DataArray[k].timeData);
								strcat (strCall, "'");
								break;
							case SQL_TIMESTAMP:		
							case SQL_TYPE_TIMESTAMP: 
								strcat (strCall, "Timestamp '");
								strcat (strCall, DataArray[k].timestampData);
								strcat (strCall, "'");
								break;
/*
							case SQL_INTERVAL:
								switch (struct_proc.proc_cols[i].SQLDateTimeSub)
								{
									case SQL_INTERVAL_YEAR:	
										break;
									case SQL_INTERVAL_MONTH:	
										break;
									case SQL_INTERVAL_YEAR_TO_MONTH:	
										break;
									case SQL_INTERVAL_DAY:		
										break;
									case SQL_INTERVAL_HOUR:		
										break;
									case SQL_INTERVAL_MINUTE:	
										break;
									case SQL_INTERVAL_SECOND:	
										break;
									case SQL_INTERVAL_DAY_TO_HOUR:	
										break;
									case SQL_INTERVAL_DAY_TO_MINUTE:	
										break;
									case SQL_INTERVAL_DAY_TO_SECOND:	
										break;
									case SQL_INTERVAL_HOUR_TO_MINUTE:	
										break;
									case SQL_INTERVAL_HOUR_TO_SECOND:	
										break;
									case SQL_INTERVAL_MINUTE_TO_SECOND:	
										break;
								}
								*/
						}
				}
				//else
				//	strcat (strCall, "?");
			}

			strcat (strCall, ")");

			printf("======>>>>>>INPARAM, NO OUTPARAM: %s\n", strCall);
			sqlret = SQLPrepare (hstmt, (SQLCHAR *)strCall, SQL_NTS);
			if (sqlret != SQL_SUCCESS)
			{
				LogAllErrors (henv, hdbc, hstmt);
				return;
			}
			sqlret = SQLExecute (hstmt);
			iTestsRun++;
			if (sqlret != SQL_SUCCESS)
			{
				LogAllErrors (henv, hdbc, hstmt);
				return;
			}
			//get resultsets
			GetResultsets ();
			sqlret = SQLFreeStmt (hstmt, SQL_UNBIND);
			sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
			sqlret = SQLFreeStmt (hstmt, SQL_CLOSE);
			if (sqlret != SQL_SUCCESS)
			{
				LogAllErrors (henv, hdbc, hstmt);
				return;
			}
			k++;
		}
	}
	else
	{
		SQLLEN	cb[MAX_COLS];

		//has in/out/inout params, bind all params
		char strCall[1000];
		bool first = TRUE;
		sprintf (strCall, "call %s (?", struct_proc.sProcName);

		for (int i = 0; i < numcols - 1; i++)
		{
			strcat (strCall, ", ?");
		}

		strcat (strCall, " )");

		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strCall, SQL_NTS);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		//sqlnumparams;
		SQLSMALLINT numparams = 0;
		sqlret = SQLNumParams (hstmt, &numparams);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		if (numparams != numcols)
		{
			printf ("SQLNumParams: %d and SQLProcedureColumns: %d count mismatch !!\n", numparams, numcols);
		}

		////describeparam ?

		//for(int i = 0; i < numparams; i++)
		//{
		//	//Binding as SQL_C_CHAR for now for all sql types. 
		//	sqlret = SQLBindParameter (hstmt, i+1, struct_proc.proc_cols[i].ColType, SQL_C_CHAR, struct_proc.proc_cols[i].SQLDataType, SQL_NTS, 0, data[i], 0, &cb[i]);
		//	if (sqlret != SQL_SUCCESS)
		//	{
		//		LogAllErrors (henv, hdbc, hstmt);
		//		return;
		//	}
		//}

		//loop: bind all params and execute
		unsigned int k = 0;
		while (TRUE)
		{	 //passing values for IN params
			if (strcmp (DataArray[k].intData, "999") == 0)
				break;

			printf("======>>>>>>BOTH INPARAM and OUTPARAM: %s\n", strCall);

			//sqlret = SQLPrepare (hstmt, (SQLCHAR *)strCall, SQL_NTS);
			//if (sqlret != SQL_SUCCESS)
			//{
			//	LogAllErrors (henv, hdbc, hstmt);
			//	return;
			//}
			//
			////sqlnumparams;
			//SQLSMALLINT numparams = 0;
			//sqlret = SQLNumParams (hstmt, &numparams);
			//if (sqlret != SQL_SUCCESS)
			//{
			//	LogAllErrors (henv, hdbc, hstmt);
			//	return;
			//}
			//if (numparams != numcols)
			//{
			//	printf ("SQLNumParams: %d and SQLProcedureColumns: %d count mismatch !!\r\n", numparams, numcols);
			//}

			for (int i = 0; i < numparams; i++)
			{
				cb[i] = SQL_NTS;
				if (struct_proc.proc_cols[i].ColType != SQL_PARAM_OUTPUT)
				{
					//assign values to in and inout params;
					switch (struct_proc.proc_cols[i].SQLDataType)
					{
						case SQL_CHAR:
						case SQL_VARCHAR:	
						case SQL_LONGVARCHAR:
							if (strcmp(struct_proc.sProcName, "N0122") == 0) {
								strcpy ((char *)data[i], DataArray[k].dateData);
							}
							else if (strcmp(struct_proc.sProcName, "N0124") == 0) {
								strcpy ((char *)data[i], DataArray[k].timestampData);
							}
							else {
								strcpy ((char *)data[i], DataArray[k].charData);
							}
							break;
						case SQL_WCHAR:	
						case SQL_WVARCHAR:	
						case SQL_WLONGVARCHAR:	
							strcpy ((char *)data[i], DataArray[k].wcharData);
							break;
						case SQL_NUMERIC:	
						case SQL_DECIMAL:	
							strcpy ((char *)data[i], DataArray[k].numdecData);
							switch(struct_proc.proc_cols[i].DecDigits)
							{
							case 0:
								break;
							case 1:
								strcat((char *)data[i], ".9");
								break;
							case 2:
								strcat((char *)data[i], ".89");
								break;
							default:
								strcat((char *)data[i], ".895");
								break;

							}
							break;
						case SQL_BIT:		
							strcpy ((char *)data[i], DataArray[k].bitData);
							break;
						case SQL_TINYINT:	
							strcpy ((char *)data[i], DataArray[k].tinyintData);
							break;
						case SQL_SMALLINT:	
							strcpy ((char *)data[i], DataArray[k].smallintData);
							break;
						case SQL_INTEGER:	
							strcpy ((char *)data[i], DataArray[k].intData);
							break;
						case SQL_BIGINT:	
							strcpy ((char *)data[i], DataArray[k].bigintData);
							break;
						/*
						case (SQL_TINYINT + SQL_SIGNED_OFFSET):	
							strcpy ((char *)data[i], DataArray[k].tinyintData);
							break;
						case (SQL_TINYINT + SQL_UNSIGNED_OFFSET):	
							strcpy ((char *)data[i], DataArray[k].tinyintData);
							break;
						case (SQL_SMALLINT + SQL_SIGNED_OFFSET):	
							strcpy ((char *)data[i], DataArray[k].smallintData);
							break;
						case (SQL_SMALLINT + SQL_UNSIGNED_OFFSET):	
							strcpy ((char *)data[i], DataArray[k].smallintData);
							break;
						case (SQL_INTEGER + SQL_SIGNED_OFFSET):	
							strcpy ((char *)data[i], DataArray[k].intData);
							break;
						case (SQL_INTEGER + SQL_UNSIGNED_OFFSET):	
							strcpy ((char *)data[i], DataArray[k].intData);
							break;
						case (SQL_BIGINT + SQL_SIGNED_OFFSET):	
							strcpy ((char *)data[i], DataArray[k].bigintData);
							break;
						case (SQL_BIGINT + SQL_UNSIGNED_OFFSET):	
							strcpy ((char *)data[i], DataArray[k].bigintData);
							break;
						*/
						case SQL_REAL:		
							strcpy ((char *)data[i], DataArray[k].floatData);
							break;
						case SQL_FLOAT:		
						case SQL_DOUBLE:	
							strcpy ((char *)data[i], DataArray[k].doubleData);
							break;
						case SQL_BINARY:	
						case SQL_VARBINARY:		
						case SQL_LONGVARBINARY:	
							strcpy ((char *)data[i], DataArray[k].binaryData);
							break;
						case SQL_DATE:		
						case SQL_TYPE_DATE:	
							strcpy ((char *)data[i], DataArray[k].dateData);
							break;
						case SQL_TIME:		
						case SQL_TYPE_TIME:	
							strcpy ((char *)data[i], DataArray[k].timeData);
							break;
						case SQL_TIMESTAMP:		
						case SQL_TYPE_TIMESTAMP: 
							strcpy ((char *)data[i], DataArray[k].timestampData);
							break;
/*
						case SQL_INTERVAL:
							switch (struct_proc.proc_cols[i].SQLDateTimeSub)
							{
								case SQL_INTERVAL_YEAR:	
									break;
								case SQL_INTERVAL_MONTH:	
									break;
								case SQL_INTERVAL_YEAR_TO_MONTH:	
									break;
								case SQL_INTERVAL_DAY:		
									break;
								case SQL_INTERVAL_HOUR:		
									break;
								case SQL_INTERVAL_MINUTE:	
									break;
								case SQL_INTERVAL_SECOND:	
									break;
								case SQL_INTERVAL_DAY_TO_HOUR:	
									break;
								case SQL_INTERVAL_DAY_TO_MINUTE:	
									break;
								case SQL_INTERVAL_DAY_TO_SECOND:	
									break;
								case SQL_INTERVAL_HOUR_TO_MINUTE:	
									break;
								case SQL_INTERVAL_HOUR_TO_SECOND:	
									break;
								case SQL_INTERVAL_MINUTE_TO_SECOND:	
									break;
							}
							*/
					}
					sqlret = SQLBindParameter (hstmt, i+1, struct_proc.proc_cols[i].ColType, SQL_C_CHAR, struct_proc.proc_cols[i].SQLDataType, 0, 0, data[i], CHARMAX, &cb[i]);
                    if (sqlret != SQL_SUCCESS)
					{
						LogAllErrors (henv, hdbc, hstmt);
						return;
					}
				}
				else
				{
					sqlret = SQLBindParameter (hstmt, i+1, struct_proc.proc_cols[i].ColType, SQL_C_CHAR, struct_proc.proc_cols[i].SQLDataType, 0, 0, data[i], CHARMAX, &cb[i]);
					if (sqlret != SQL_SUCCESS)
					{
						LogAllErrors (henv, hdbc, hstmt);
						return;
					}
				}
			}
			sqlret = SQLExecute (hstmt);
			if (sqlret != SQL_SUCCESS)
			{
				LogAllErrors (henv, hdbc, hstmt);
				return;
			}
			iTestsRun++;

			GetResultsets ();

			for (int i = 0; i < numcols; i++)
			{
				if (struct_proc.proc_cols[i].ColType != SQL_PARAM_INPUT)
				{
					printf ("OUT/INOUT PARAM # %d value : %s\n", i, data[i]);
				}
			}
			//sqlret = SQLFreeStmt (hstmt, SQL_UNBIND);
			//sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
			sqlret = SQLFreeStmt (hstmt, SQL_CLOSE);

            k++;
            //if(stricmp(struct_proc.sProcName,"RS4")==0)
            //    break;
		}
	}

	//sqlret = SQLFreeStmt (hstmt, SQL_UNBIND);
	//sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
	sqlret = SQLFreeStmt (hstmt, SQL_CLOSE);
}

void ODBCSPJResultSetTest1 ()
{
	unsigned int numprocs = 0;
	char opname[257];
	SQLLEN opnamelen;
	char ProcNames[257][257];

	char		oColName[NAME_LEN];
	SWORD		oColType;
	SWORD		oColDataType;
	char		oColTypeName[NAME_LEN];
	SDWORD		oColSize;
	SDWORD		oBufferLen;
	SWORD		oDecDigits;
	SWORD		oColRadix;
	SWORD		oColNullable;
	char		oColDef[NAME_LEN];
	SWORD		oSQLDataType;
	SWORD		oSQLDateTimeSub;
	SDWORD		oCharOctetLen;
	SDWORD		oOrdinalPos;
	SQLLEN		oColNamelen;
	SQLLEN		oColTypelen;
	SQLLEN		oColDataTypelen;
	SQLLEN		oColTypeNamelen;
	SQLLEN		oColSizelen;
	SQLLEN		oBufferLenlen;
	SQLLEN		oDecDigitslen;
	SQLLEN		oColRadixlen;
	SQLLEN		oColNullablelen;
	SQLLEN		oColDeflen;
	SQLLEN		oSQLDataTypelen;
	SQLLEN		oSQLDateTimeSublen;
	SQLLEN		oCharOctetLenlen;
	SQLLEN		oOrdinalPoslen;

	sqlret = SQLProcedures(hstmt, (SQLCHAR*)cat, SQL_NTS, (SQLCHAR*)sch, SQL_NTS, SQL_NULL_HANDLE, 0);
	//printf("RETCODE is: %d Cat: %s Sch: %s\n", sqlret, cat, sch);

	iTestsRun++;

	if (sqlret == SQL_SUCCESS)
	{
		strcpy (opname, "");
		sqlret = SQLBindCol (hstmt, 3, SQL_C_CHAR, opname, NAME_LEN, &opnamelen);
		while (sqlret == SQL_SUCCESS)
		{
			sqlret = SQLFetch(hstmt);
			if (sqlret == SQL_NO_DATA_FOUND) 
				break;
			if (sqlret != SQL_SUCCESS)
			{
				LogAllErrors (henv, hdbc, hstmt);
				return;
			}
			strcpy (ProcNames[numprocs], opname);
			strcpy(opname,"");
			numprocs++;
		} // while
	}
	if (numprocs == 0)
	{
		printf("No SPJs found in the schema specified in the datasource\n");
		return;
	}

	//SQLProcedureColumns
    for (int i = 0; i < numprocs; i++)
	{
		int numcols = 0;
		memset (&struct_proc, 0, sizeof(struct_proc));
		strcpy (struct_proc.sProcName, ProcNames[i]);
		struct_proc.numincols = 0;
		struct_proc.numoutcols = 0;
		struct_proc.numinoutcols = 0;

		/*if(stricmp(ProcNames[i],(char*)"RS0")==0)
			printf("Breaking\n");*/

		sqlret = SQLProcedureColumns (hstmt, (SQLCHAR *)cat, SQL_NTS, (SQLCHAR *)sch, SQL_NTS, (SQLCHAR *) ProcNames[i], SQL_NTS, SQL_NULL_HANDLE, 0);

		iTestsRun++;
		if (sqlret != SQL_SUCCESS)
		{
			printf("SQLProcedureColumns(hsmt, %s, 0, %s, 0, %s, SQL_NTS, SQL_NULL_HANDLE, 0)\n", cat, sch, ProcNames[i]);
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		if (sqlret == SQL_SUCCESS)
		{
			strcpy(oColName,"");
			oColType = 0;
			oColDataType = 0;
			strcpy(oColTypeName,"");
			oColSize = 0;
			oBufferLen = 0;
			oDecDigits = 0;
			oColRadix = 0;
			oColNullable = 0;
			strcpy(oColDef,"");
			oSQLDataType = 0;
			oSQLDateTimeSub = 0;
			oCharOctetLen = 0;
			oOrdinalPos = 0;
			SQLBindCol(hstmt,4,SQL_C_CHAR,oColName,NAME_LEN,&oColNamelen);
			SQLBindCol(hstmt,5,SQL_C_SHORT,&oColType,0,&oColTypelen);
			SQLBindCol(hstmt,6,SQL_C_SHORT,&oColDataType,0,&oColDataTypelen);
			SQLBindCol(hstmt,7,SQL_C_CHAR,oColTypeName,NAME_LEN,&oColTypeNamelen);
			SQLBindCol(hstmt,8,SQL_C_LONG,&oColSize,0,&oColSizelen);
			SQLBindCol(hstmt,9,SQL_C_LONG,&oBufferLen,0,&oBufferLenlen);
			SQLBindCol(hstmt,10,SQL_C_SHORT,&oDecDigits,0,&oDecDigitslen);
			SQLBindCol(hstmt,11,SQL_C_SHORT,&oColRadix,0,&oColRadixlen);
			SQLBindCol(hstmt,12,SQL_C_SHORT,&oColNullable,0,&oColNullablelen);
			SQLBindCol(hstmt,14,SQL_C_CHAR,oColDef,NAME_LEN,&oColDeflen);
			SQLBindCol(hstmt,15,SQL_C_SHORT,&oSQLDataType,0,&oSQLDataTypelen);
			SQLBindCol(hstmt,16,SQL_C_SHORT,&oSQLDateTimeSub,0,&oSQLDateTimeSublen);
			SQLBindCol(hstmt,17,SQL_C_LONG,&oCharOctetLen,0,&oCharOctetLenlen);
			SQLBindCol(hstmt,18,SQL_C_LONG,&oOrdinalPos,0,&oOrdinalPoslen);
			while (sqlret == SQL_SUCCESS)
			{
				sqlret = SQLFetch(hstmt);
				if (sqlret == SQL_NO_DATA_FOUND) break;
				if (sqlret != SQL_SUCCESS)
				{
					LogAllErrors (henv, hdbc, hstmt);
					return;
				}

				switch(oColType)
				{
					case SQL_PARAM_INPUT:
						struct_proc.numincols++;
						break;
					case SQL_PARAM_OUTPUT:
						struct_proc.numoutcols++;
						break;
					case SQL_PARAM_INPUT_OUTPUT:
						struct_proc.numinoutcols++;
						break;
				}
				strcpy (struct_proc.proc_cols[numcols].ColName, oColName);
				struct_proc.proc_cols[numcols].OrdinalPos = oOrdinalPos;
				struct_proc.proc_cols[numcols].ColType = oColType;
				//struct_proc.proc_cols[numcols].SQLDataType = oSQLDataType;
				struct_proc.proc_cols[numcols].SQLDataType = oColDataType;
				struct_proc.proc_cols[numcols].SQLDateTimeSub = oSQLDateTimeSub;
				struct_proc.proc_cols[numcols].ColSize = oColSize;
				struct_proc.proc_cols[numcols].ColNullable = oColNullable;
				struct_proc.proc_cols[numcols].BufferLen = oBufferLen;
				struct_proc.proc_cols[numcols].DecDigits = oDecDigits;

				numcols++;

				strcpy(oColName,"");
				oColType = 0;
				oColDataType = 0;
				strcpy(oColTypeName,"");
				oColSize = 0;
				oBufferLen = 0;
				oDecDigits = 0;
				oColRadix = 0;
				oColNullable = 0;
				strcpy(oColDef,"");
				oSQLDataType = 0;
				oSQLDateTimeSub = 0;
				oCharOctetLen = 0;
				oOrdinalPos = 0;
				
			} // while
		}
		printf ("\n%s has %d params\n", struct_proc.sProcName, numcols);
		printf ("numincols: %d\n", struct_proc.numincols);
		printf ("numoutcols: %d\n", struct_proc.numoutcols);
		printf ("numinoutcols: %d\n", struct_proc.numinoutcols);
		printf ("\n");
		for (int j = 0; j < numcols;j++)
		{
			printf ("Column Name : %s\n", struct_proc.proc_cols[j].ColName);
			printf ("Ordinal Pos : %d\n", struct_proc.proc_cols[j].OrdinalPos);
			printf ("ColType : %d\n", struct_proc.proc_cols[j].ColType);
			printf ("SQLDataType : %d\n", struct_proc.proc_cols[j].SQLDataType);
			printf ("SQLDateTimeSub : %d\n", struct_proc.proc_cols[j].SQLDateTimeSub);
			printf ("ColSize : %d\n", struct_proc.proc_cols[j].ColSize);
			printf ("ColNullable : %d\n", struct_proc.proc_cols[j].ColNullable);
			printf ("BufferLen : %d\n", struct_proc.proc_cols[j].BufferLen);
			printf ("DecDigits : %d\n", struct_proc.proc_cols[j].DecDigits);
			printf ("\n");
		}
		printf ("\n");

		//sqlret = SQLFreeStmt (hstmt, SQL_UNBIND);
		//sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		sqlret = SQLFreeStmt (hstmt, SQL_CLOSE);

		//call the SPJ with diff data, skip RSBIG
		if ((stricmp (struct_proc.sProcName, "RSBIG")) != 0)
			CallSPJsWithDiffData ();
	}
	//sqlret = SQLFreeStmt (hstmt, SQL_UNBIND);
	//sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
	sqlret = SQLFreeStmt (hstmt, SQL_CLOSE);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
}

void ODBCSPJResultSetTest_Rowsets ()
{
	typedef struct _table_rowset {
		SQLCHAR             dt_integer_s[INTMAX];          SQLLEN ptr_integer_s;
		SQLCHAR             dt_char_iso[CHARMAX];           SQLLEN ptr_char_iso;
		SQLCHAR             dt_varchar_iso[VARCHARMAX];        SQLLEN ptr_varchar_iso;
	} table_rowset;
	table_rowset *rowset;            // Where we will store the data prior to inserting it into the database.
	SQLUSMALLINT *rowsetStatusArray; // Array showing the status of each row after running SQLExecute().
	SQLUSMALLINT *rowsetOperationArray; // Array showing which rows to process when running SQLExecute().
	SQLULEN       rowsProcessed;     // The number of rows processed after running SQLExecute().

	printf ("\nNote: This set of tests require the RSBig SPJ to exist.\n");

	//int ins_rows[] = {10,1000,10000,50000,-1};
	//int fetch_rowset_size[] = {100,1000,10000,10000};
	int ins_rows[] = {10,500,1000,5000,-1};
	int fetch_rowset_size[] = {10,500,1000,5000};
	
	/*
	call RSBig(10); //insert 10 rows and fetch with rowset sizeof 100
	call RSBig(1000); //insert 1000 rows and fetch with rowset size of 1000
	call RSBig(10000); //insert 10000 rows and fetch with rowset size of 10000
	call RSBig(50000); //insert 50000 rows and fetch with rowset size of 10000
	*/

	int ii = 0;
	char strcall[100];
	while(ins_rows[ii] != -1)
	{
		sprintf(strcall, "call RSBig(%d)", ins_rows[ii]);
		//BindCols;
		rowset = (table_rowset *)malloc( fetch_rowset_size[ii] * sizeof( table_rowset ) );
	    rowsetStatusArray = (SQLUSMALLINT *)malloc ( fetch_rowset_size[ii] * sizeof( SQLUSMALLINT ) );
	    rowsetOperationArray  = (SQLUSMALLINT *)malloc ( fetch_rowset_size[ii] * sizeof( SQLUSMALLINT ) );
    
		// We want all the rows processed.
		for( int loop = 0; loop < fetch_rowset_size[ii]; loop++ )
		{
			rowsetOperationArray[ loop ] = SQL_PARAM_PROCEED;
		}

	    // We need to preset the pointers. 
		for( int loop = 0; loop < fetch_rowset_size[ii]; loop++ )
		{
            rowset[ loop ].ptr_integer_s = SQL_NTS;
			rowset[ loop ].ptr_char_iso = SQL_NTS;
            rowset[ loop ].ptr_varchar_iso = SQL_NTS;
	    }
        sqlret = SQLSetStmtAttr( hstmt, SQL_ATTR_ROW_BIND_TYPE, (void *)sizeof( table_rowset ), 0 );
		if (sqlret != SQL_SUCCESS)
			goto bailout;
	    sqlret = SQLSetStmtAttr( hstmt, SQL_ATTR_ROW_ARRAY_SIZE, (void *)fetch_rowset_size[ii], 0 );
		if (sqlret != SQL_SUCCESS)
			goto bailout;
		sqlret = SQLSetStmtAttr( hstmt, SQL_ATTR_ROW_STATUS_PTR, rowsetStatusArray, 0 );
		if (sqlret != SQL_SUCCESS)
			goto bailout;
		sqlret = SQLSetStmtAttr( hstmt, SQL_ATTR_ROWS_FETCHED_PTR, &rowsProcessed, 0 );
		if (sqlret != SQL_SUCCESS)
			goto bailout;

        sqlret = SQLBindCol( hstmt, 1,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_integer_s, INTMAX,
                                  &rowset[ 0 ].ptr_integer_s );
		if (sqlret != SQL_SUCCESS)
			goto bailout;
        sqlret = SQLBindCol( hstmt, 2,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_char_iso, CHARMAX,
                                  &rowset[ 0 ].ptr_char_iso );
		if (sqlret != SQL_SUCCESS)
			goto bailout;
		sqlret = SQLBindCol( hstmt, 3,  SQL_C_CHAR,
                                  (SQLPOINTER) rowset[ 0 ].dt_varchar_iso, VARCHARMAX,
                                  &rowset[ 0 ].ptr_varchar_iso );                                  
		if (sqlret != SQL_SUCCESS)
			goto bailout;

		sqlret = SQLExecDirect(hstmt, (SQLCHAR *)strcall, SQL_NTS);

		iTestsRun++;

		if (sqlret != SQL_SUCCESS && sqlret != SQL_SUCCESS_WITH_INFO)
			goto bailout;
		int total_rows = 0;
		while (sqlret != SQL_NO_DATA_FOUND)
		{
			sqlret = SQLFetch(hstmt);
			if (sqlret == SQL_ERROR)
				goto bailout;

			//printf ("\n\n==>>%s\n\n", rowset[ 0 ].dt_integer_s);
			//printf ("\n\n==>>%s\n\n", rowset[ 0 ].dt_char_iso);
			//printf ("\n\n==>>%s\n\n", rowset[ 0 ].dt_varchar_iso);

			total_rows += rowsProcessed;
		}

		printf("Rows inserted : %d\nRowset size : %d\nTotal Rows Fetched: %d\n\n\n", ins_rows[ii], fetch_rowset_size[ii], total_rows);

        free( (table_rowset *)rowset ); 
	    free( rowsetStatusArray );
	    free( rowsetOperationArray );

		sqlret = SQLFreeStmt (hstmt, SQL_UNBIND);
		sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		sqlret = SQLFreeStmt (hstmt, SQL_CLOSE);

		ii++;
	}

	sqlret = SQLFreeStmt (hstmt, SQL_UNBIND);
	sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
	sqlret = SQLFreeStmt (hstmt, SQL_CLOSE);
	return;

bailout:
    free( (table_rowset *)rowset ); 
    free( rowsetStatusArray );
    free( rowsetOperationArray );

	LogAllErrors (henv, hdbc, hstmt);

	sqlret = SQLFreeStmt (hstmt, SQL_UNBIND);
	sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
	sqlret = SQLFreeStmt (hstmt, SQL_CLOSE);
}


void ODBCSPJResultSetTestAll ()
{
	//sprintf (strSQL, "{CALL CAT.SCH.N0001()}");
	//sprintf (strSQL, "{call TRAFODION.ODBC_SPJRS.RSAll()}");
	sprintf (strSQL, "{call RSAll()}");
//	fprintf (logfile, "RS0\n");

	sqlret = SQLPrepare (hstmt, (unsigned char *)strSQL, SQL_NTS);
	//sqlret = SQLExecDirect (hstmt, (unsigned char *)strSQL, SQL_NTS);
	sqlret = SQLExecute (hstmt);

	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	unsigned long iRowCount = 0;
	SQLSMALLINT iNumResCols = 0;
	unsigned short iNumResultSets = 0;

	do
	{
		char strRowData[MAX_TABLE_SIZE], strHeadings[MAX_TABLE_SIZE];
		strcpy (strHeadings, "");
		while (TRUE) 
		{
			int		icol;
			char	sColName[COLNAME_LEN_MAX];
			SWORD	iColNameLength, iSQLType, iColScale, iNullable;
			SQLULEN iColPrec;
			SQLLEN	cbOutputLen[MAX_COLS];

			strcpy (strRowData, "");

			sqlret = SQLFetch(hstmt);
			if (sqlret == SQL_NO_DATA_FOUND)
			{
				printf ("%d row(s) fetched from %d column(s)\n\n", iRowCount, iNumResCols);
				iRowCount = 0;
				iNumResCols = 0;
				break;
			}
			if (sqlret != SQL_SUCCESS && sqlret != SQL_SUCCESS_WITH_INFO) 
			{
				LogAllErrors (henv, hdbc, hstmt);
				return;
			}
			iRowCount++;

			sqlret = SQLNumResultCols (hstmt, &iNumResCols);
			for (icol = 1; icol <= iNumResCols; icol++)
			{
				SQLCHAR		rgbDesc[RGB_MAX_LEN];
				SQLSMALLINT	pcbDesc;
				SQLLEN		pfDesc;

		 		strcpy((char*)rgbDesc,"");
				pcbDesc = 0;
				pfDesc = 0;
				DATE_STRUCT	dateData;
				TIME_STRUCT	timeData;
				TIMESTAMP_STRUCT timestampData;
				SQL_INTERVAL_STRUCT intervalData;
				char charData [MAX_CHAR_LEN];
				WCHAR wcharData [MAX_WCHAR_LEN];
				unsigned char bitData[MAX_BIT_LEN];
				SQLSMALLINT	tinyintData, shortData;
				SQLUSMALLINT utinyintData, ushortData;
				unsigned long ulData;
				long lData;
				unsigned long long ubigintData;
				long long bigintData;
				float fData;
				double doubleData;
				char binaryData[MAX_BINARY_LEN];
				char strColData[MAX_CHAR_LEN];

				sqlret = SQLDescribeCol (hstmt, icol, (SQLCHAR*)sColName, COLNAME_LEN_MAX, &iColNameLength, &iSQLType, &iColPrec, &iColScale, &iNullable);
				sqlret = SQLColAttribute(hstmt, icol, SQL_DESC_UNSIGNED, rgbDesc, RGB_MAX_LEN, &pcbDesc, &pfDesc);
				if (iRowCount == 1)
				{
					strcat(strHeadings, sColName);
					strcat(strHeadings, " \t");
				}

	/*
				colname : sColName
				ColNameLen : iColNameLength
				SQLType : iSQLType
				ColPrec : iColPrec
				ColScale : iColScale
				ColNullable : iNullable
				SQLGetData(hstmt, 1, SQL_C_ULONG, &sCustID, 0, &cbCustID);
				SQLGetData(hstmt, 2, SQL_C_CHAR, szName, NAME_LEN, &cbName);
				SQLGetData(hstmt, 3, SQL_C_CHAR, szPhone, PHONE_LEN,&cbPhone);

				if pfDesc is 0 it is signed, if it is 1 datatype is unsigned.
	*/
				strcpy (strColData,"");
				switch (iSQLType)
				{
					case SQL_CHAR:	
					case SQL_VARCHAR:	
					case SQL_LONGVARCHAR:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_CHAR, charData, MAX_CHAR_LEN, &cbOutputLen[icol-1]);
						sprintf (strColData, "%s \t", charData);
						break;
					case SQL_WCHAR:	
					case SQL_WVARCHAR:	
					case SQL_WLONGVARCHAR:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_WCHAR, wcharData, MAX_WCHAR_LEN, &cbOutputLen[icol-1]);
						sprintf (strColData, "%s \t", wcharData);
						break;
					case SQL_NUMERIC:	
					case SQL_DECIMAL:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_CHAR, charData, MAX_CHAR_LEN, &cbOutputLen[icol-1]);
						sprintf (strColData, "%s \t", charData);
						break;
					case SQL_BIT:		
						sqlret = SQLGetData(hstmt, icol, SQL_C_BIT, bitData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", bitData);
						break;
					case SQL_TINYINT:	
						if (pfDesc)
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_UTINYINT, &utinyintData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%d \t", utinyintData);
						}
						else
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_STINYINT, &tinyintData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%d \t", tinyintData);
						}
						break;
					case SQL_SMALLINT:	
						if (pfDesc)
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_USHORT, &ushortData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%d \t", ushortData);
						}
						else
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_SSHORT, &shortData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%d \t", shortData);
						}
						break;
					case SQL_INTEGER:	
						if (pfDesc)
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_ULONG, &ulData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%ld \t", ulData);
						}
						else
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_SLONG, &lData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%ld \t", lData);
						}
						break;
					case SQL_BIGINT:	
						if (pfDesc)
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_UBIGINT, &ubigintData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%ld \t", ubigintData);
						}
						else
						{
							sqlret = SQLGetData(hstmt, icol, SQL_C_SBIGINT, &bigintData, 0, &cbOutputLen[icol-1]);
							sprintf (strColData, "%ld \t", bigintData);
						}
						break;
					case SQL_REAL:		
						sqlret = SQLGetData(hstmt, icol, SQL_C_FLOAT, &fData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%f \t", fData);
						break;
					case SQL_FLOAT:		
					case SQL_DOUBLE:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_DOUBLE, &doubleData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%e \t", doubleData);
						break;
					case SQL_BINARY:	
					case SQL_VARBINARY:		
					case SQL_LONGVARBINARY:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_BINARY, &binaryData, MAX_BINARY_LEN, &cbOutputLen[icol-1]);
						sprintf (strColData, "%s \t", binaryData);
						break;
					case SQL_DATE:		
					case SQL_TYPE_DATE:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_TYPE_DATE, &dateData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d %d %d \t", dateData.year, dateData.month, dateData.day);
						break;
					case SQL_TIME:		
					case SQL_TYPE_TIME:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_TYPE_TIME, &timeData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d %d %d \t", timeData.hour, timeData.minute, timeData.second);
						break;
					case SQL_TIMESTAMP:		
					case SQL_TYPE_TIMESTAMP: 
						sqlret = SQLGetData(hstmt, icol, SQL_C_TYPE_TIMESTAMP, &timestampData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d %d %d \t", timestampData.year, timestampData.month, timestampData.day);
						break;
					case SQL_INTERVAL_YEAR:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_YEAR, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_MONTH:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_MONTH, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_YEAR_TO_MONTH:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_YEAR_TO_MONTH, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_DAY:		
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_DAY, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_HOUR:		
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_HOUR, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_MINUTE:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_MINUTE, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_SECOND:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_SECOND, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_DAY_TO_HOUR:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_DAY_TO_HOUR, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_DAY_TO_MINUTE:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_DAY_TO_MINUTE, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_DAY_TO_SECOND:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_DAY_TO_SECOND, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_HOUR_TO_MINUTE:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_HOUR_TO_MINUTE, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_HOUR_TO_SECOND:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_HOUR_TO_SECOND, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					case SQL_INTERVAL_MINUTE_TO_SECOND:	
						sqlret = SQLGetData(hstmt, icol, SQL_C_INTERVAL_MINUTE_TO_SECOND, &intervalData, 0, &cbOutputLen[icol-1]);
						sprintf (strColData, "%d \t", intervalData.intval);
						break;
					default:
						iSQLType = SQL_CHAR;
						sqlret = SQLGetData(hstmt, icol, SQL_C_CHAR, charData, MAX_CHAR_LEN, &cbOutputLen[icol-1]);
						printf ("%s\t", charData);
						sprintf (strColData, "%s \t", charData);
						break;
				}
				strcat(strRowData, strColData);
			}
			if (iRowCount == 1)
				printf ("%s\n", strHeadings);
			printf ("%s\n", strRowData);
		}
		iNumResultSets++;
	} while ((sqlret = SQLMoreResults(hstmt)) != SQL_NO_DATA_FOUND);

	printf ("%d Resultset(s) fetched\n\n", iNumResultSets);

	sqlret = SQLFreeStmt (hstmt, SQL_UNBIND);
	sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
	sqlret = SQLFreeStmt (hstmt, SQL_CLOSE);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

}

void ODBCSPJResultSetTests ()
{
	if (Connect ())
	{
		sqlret = SQLAllocHandle (SQL_HANDLE_STMT, hdbc, &hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			Disconnect ();
			//fprintf (logfile, "Error: SQLAllocHandle for STMT\n");
			printf ("Error: SQLAllocHandle for STMT\n");
			return;
		}
		getCQD((char*)"CATALOG",cat);
		getCQD((char*)"SCHEMA",sch);
		//ODBCSPJTest2 ();
		ODBCSPJResultSetTest1 ();	
		ODBCSPJResultSetTest_Rowsets ();	
		//ODBCSPJResultSetTestAll ();	// no params : TRAFODION.ODBC_SPJRS.RSAll
		Disconnect ();
	}
	printf ("Tests run: %d\nTests Failed: %d\n", iTestsRun, iTestsFailed);
        printf ("odbcspj TEST RESULT: %s\n", ((iTestsRun == 0 || iTestsFailed) ? "FAIL" : "PASS"));
}

long strtohextoval(SQL_NUMERIC_STRUCT NumStr)
{
	long val = 0, value = 0;
	int i = 1, last = 1, current;
	int a = 0, b = 0;

    for (i = 0; i <= 15; i++)
    {
		current = (int) NumStr.val[i];
		a = current % 16; //Obtain LSD
		b = current / 16; //Obtain MSD
			
		value += last * a;	
		last = last * 16;	
		value += last * b;
		last = last * 16;	
	}
 	return value;
}

void	ODBCSPJTest1 ()
{
	iTestsRun++;
	//sprintf (strSQL, "{CALL CAT.SCH.N0001()}");
	sprintf (strSQL, "{CALL N0001()}");
	fprintf (logfile, "N0001\n");

	sqlret = SQLExecDirect (hstmt, (unsigned char *)strSQL, SQL_NTS);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
	sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
}
/*
#define SQL_C_CHAR    SQL_CHAR             // CHAR, VARCHAR, DECIMAL, NUMERIC 
#define SQL_C_LONG    SQL_INTEGER          // INTEGER                      
#define SQL_C_SHORT   SQL_SMALLINT         // SMALLINT                     
#define SQL_C_FLOAT   SQL_REAL             // REAL                         
#define SQL_C_DOUBLE  SQL_DOUBLE           // FLOAT, DOUBLE                
#if (ODBCVER >= 0x0300)
#define	SQL_C_NUMERIC		SQL_NUMERIC
#endif
#define SQL_C_DEFAULT 99
*/

void	ODBCSPJTest2 ()
{
	sprintf (strSQL, "{CALL N0200(?,?)}");
	//fprintf (logfile, "N0200\n");
	printf ("N0200\n");

	char	sParm1[7][51] = {"Hello", "a", " ", "", "ABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJ", " hp "};
	char	sParm2[51];
	char	sExpVals[7][51] = {"Hello", "a", "", "", "ABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJ", " hp"};

	for (int i = 0; i < 6; i++)
	{
		iTestsRun++;
		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		SQLLEN	cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, 0, 0, sParm1[i], 51, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_VARCHAR, 0, 0, sParm2, 51, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		sqlret = SQLExecute (hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		if (strcmp(sParm2, sExpVals[i]))
		{
			//fprintf (logfile, "#%d: Output val different from expected val, outputval : %s\tExpected val : %s\n", i, sParm2, sExpVals[i]);
			printf ("#%d: Output val different from expected val, outputval : %s\tExpected val : %s\n", i, sParm2, sExpVals[i]);
			iTestsFailed++;
		}
		sqlret = SQLFreeStmt (hstmt, SQL_CLOSE);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
	}
}


/*
void	ODBCSPJTest2 ()
{
	sprintf (strSQL, "{CALL N0200(?,?)}");
	//fprintf (logfile, "N0200\n");
	printf ("N0200\n");

	char	sParm1[7][51] = {"Hello", "a", " ", "", "ABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJ", " hp "};
	char	sParm2[51];
	char	sExpVals[7][51] = {"Hello", "a", "", "", "ABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJ", " hp"};

	for (int i = 0; i < 6; i++)
	{
		iTestsRun++;
		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		SDWORD	cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, 0, 0, sParm1[i], 51, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_VARCHAR, 0, 0, sParm2, 51, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		sqlret = SQLExecute (hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		if (strcmp(sParm2, sExpVals[i]))
			//fprintf (logfile, "#%d: Output val different from expected val, outputval : %s\tExpected val : %s\n", i, sParm2, sExpVals[i]);
			printf ("#%d: Output val different from expected val, outputval : %s\tExpected val : %s\n", i, sParm2, sExpVals[i]);
		else
			iTestsPassed++;

		sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
	}
}
*/
void ODBCSPJTest3 ()
{
	fprintf (logfile, "N0302\n");
	sprintf (strSQL, "{CALL N0302(?,?,?)}");
	
	//signed: -2^31 <= n <= 2^31 - 1
	//unsigned: 0 <= n <= 2[32] - 1

	signed int	sParm1[10] = {123, 0, -456, -2147483648, -2147483647, 2147483647, 2147483646};
	signed int	sParm2[10] = {-256, 987, 0, 2147483647, 2147483646, -2147483648, -2147483647};
	signed int	sParm3 = 0;
	signed int	ExpVals2[10] = {123, 0, -456, -2147483648, -2147483647, 2147483647, 2147483646};
	signed int ExpVals3[10] = {-256, 987, 0, 2147483647, 2147483646, -2147483648, -2147483647};

	for (int i = 0; i < 7; i++)
	{
		iTestsRun++;
		SQLLEN	cbParm = SQL_NTS;

		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_LONG, SQL_INTEGER, 0, 0, &sParm1[i], 0, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_INPUT_OUTPUT, SQL_C_LONG, SQL_INTEGER, 0, 0, &sParm2[i], 0, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 3, SQL_PARAM_OUTPUT, SQL_C_LONG, SQL_INTEGER, 0, 0, &sParm3, 0, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		sqlret = SQLExecute (hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		if ((sParm2[i] != ExpVals2[i]) || (sParm3 != ExpVals3[i]))
		{
			if (sParm2[i] != ExpVals2[i])
				fprintf (logfile, "#%d: Output val different from expected val, outputval : %+d\tExpected val : %d\n", i, sParm2[i], ExpVals2[i]);
			if (sParm3 != ExpVals3[i])
				fprintf (logfile, "#%d: Output val different from expected val, outputval : %+d\tExpected val : %d\n", i, sParm3, ExpVals3[i]);
			iTestsFailed++;
		}

		sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
	}
}

void ODBCSPJTest3Char ()
{
	fprintf (logfile, "N0302 SQL_C_CHAR\n");
	sprintf (strSQL, "{CALL N0302(?,?,?)}");
	
	//signed: -2^31 <= n <= 2^31 - 1
	//unsigned: 0 <= n <= 2[32] - 1

	char sParm1[10][20] = {"123", "0", "-456", "-2147483648", "-2147483647", "2147483647", "2147483646"};
	char sParm2[10][20] = {"-256", "987", "0", "2147483647", "2147483646", "-2147483648", "-2147483647"};
	char sParm3[20];
	char ExpVals2[10][20] = {"123", "0", "-456", "-2147483648", "-2147483647", "2147483647", "2147483646"};
	char ExpVals3[10][20] = {"-256", "987", "0", "2147483647", "2147483646", "-2147483648", "-2147483647"};

	for (int i = 0; i < 7; i++)
	{
		iTestsRun++;
		SQLLEN cbParm = SQL_NTS;

		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_INTEGER, 0, 0, &sParm1[i], 20, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_INPUT_OUTPUT, SQL_C_CHAR, SQL_INTEGER, 0, 0, &sParm2[i], 20, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 3, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_INTEGER, 0, 0, &sParm3, 20, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		sqlret = SQLExecute (hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		if ((strcmp (sParm2[i], ExpVals2[i]) != 0) || (strcmp (sParm3, ExpVals3[i]) != 0))
		{
			if (strcmp (sParm2[i], ExpVals2[i]) != 0)
				fprintf (logfile, "#%d: Output val different from expected val, outputval : %s\tExpected val : %s\n", i, sParm2[i], ExpVals2[i]);
			if (strcmp (sParm3, ExpVals3[i]) != 0)
				fprintf (logfile, "#%d: Output val different from expected val, outputval : %s\tExpected val : %s\n", i, sParm3, ExpVals3[i]);
			iTestsFailed++;
		}

		sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
	}
}

void ODBCSPJTest5()
{
	fprintf (logfile, "N0101\n");
	sprintf (strSQL, "{CALL N0101(?)}");

	char	sParm1[10];
	SQLLEN	cbParm = SQL_NTS;

	iTestsRun++;
	sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
	strcpy (sParm1, "1234567");
	sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_DECIMAL, 0, 0, sParm1, 10, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
	
	sqlret = SQLExecute (hstmt);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
	sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
}


/*
SQL_C_TYPE_DATE
SQL_DATE_STRUCT 
struct tagDATE_STRUCT {
SQLSMALLINT year; 
SQLUSMALLINT month; 
SQLUSMALLINT day; 
} DATE_STRUCT; 
 
*/

void ODBCSPJTest6 ()
{
	fprintf (logfile, "N0122\n");
	sprintf (strSQL, "{CALL N0122(?,?,?)}");
	
	//char	sParm1[4][20] = {"2002-12-30", "0001-01-01", "9999-12-31"};
	char sParm1[4][20] = {"2002-12-30", "1001-01-01", "9999-12-31"};
	SQL_DATE_STRUCT sParm2[4];
	//SQL_DATE_STRUCT sParm3[4] = {{1001,11,11}, {9999,12,31}, {0001,01,01}};
	SQL_DATE_STRUCT sParm3[4] = {{1001,11,11}, {9999,12,31}, {1001,01,01}};
	//char ExpVals2[4][51] = {"1001-11-11", "9999-12-31", "0001-01-01"};
	char ExpVals2[4][51] = {"1001-11-11", "9999-12-31", "1001-01-01"};
	//char ExpVals3[4][51] = {"2002-12-30", "0001-01-01", "9999-12-31"};
	char ExpVals3[4][51] = {"2002-12-30", "1001-01-01", "9999-12-31"};
	SQLLEN	cbParm = SQL_NTS;

	for (int i = 0; i < 3; i++)
	{
		iTestsRun++;
		SQLLEN	cbParm = SQL_NTS;

		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, 0, 0, sParm1[i], 19, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_TYPE_DATE, SQL_DATE, 0, 0, &sParm2[i], 0, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 3, SQL_PARAM_INPUT_OUTPUT, SQL_C_TYPE_DATE, SQL_DATE, 0, 0, &sParm3[i], 0, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		sqlret = SQLExecute (hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		char p2[51], p3[51];

		sprintf (p2, "%d-%d-%d", sParm2[i].year, sParm2[i].month, sParm2[i].day);
		sprintf (p3, "%d-%d-%d", sParm3[i].year, sParm3[i].month, sParm3[i].day);

		if ((strcmp (p2, ExpVals2[i]) != 0) || (strcmp (p3, ExpVals3[i]) != 0))
		{
			if (strcmp (p2, ExpVals2[i]) != 0)
				fprintf (logfile, "#%d: Output val different from expected val, outputval : %s\tExpected val : %s\n", i, p2, ExpVals2[i]);
			if (strcmp (p3, ExpVals3[i]) != 0)
				fprintf (logfile, "#%d: Output val different from expected val, outputval : %s\tExpected val : %s\n", i, p3, ExpVals3[i]);
			iTestsFailed++;
		}

		sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
	}
}

void ODBCSPJTest6Char ()
{
	fprintf (logfile, "N0122 SQL_C_CHAR\n");
	sprintf (strSQL, "{CALL N0122(?,?,?)}");
	
	//char	sParm1[4][20] = {"2002-12-30", "0001-01-01", "9999-12-31"};
	char	sParm1[4][20] = {"2002-12-30", "1001-01-01", "9999-12-31"};
	char	sParm2[4][51];
	//char	sParm3[4][51] = {"1001-11-11", "9999-12-31", "0001-01-01"};
	char	sParm3[4][51] = {"1001-11-11", "9999-12-31", "1001-01-01"};
	//char	ExpVals2[4][51] = {"1001-11-11", "9999-12-31", "0001-01-01"};
	char	ExpVals2[4][51] = {"1001-11-11", "9999-12-31", "1001-01-01"};
	//char	ExpVals3[4][51] = {"2002-12-30", "0001-01-01", "9999-12-31"};
	char	ExpVals3[4][51] = {"2002-12-30", "1001-01-01", "9999-12-31"};
	SQLLEN	cbParm = SQL_NTS;

	for (int i = 0; i < 3; i++)
	{
		iTestsRun++;
		SQLLEN	cbParm = SQL_NTS;

		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, 0, 0, sParm1[i], 19, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_DATE, 0, 0, sParm2[i], 50, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 3, SQL_PARAM_INPUT_OUTPUT, SQL_C_CHAR, SQL_DATE, 0, 0, sParm3[i], 50, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		sqlret = SQLExecute (hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		if ((strcmp (sParm2[i], ExpVals2[i]) != 0) || (strcmp (sParm3[i], ExpVals3[i]) != 0))
		{
			if (strcmp (sParm2[i], ExpVals2[i]) != 0)
				fprintf (logfile, "#%d: Output val different from expected val, outputval : %s\tExpected val : %s\n", i, sParm2[i], ExpVals2[i]);
			if (strcmp (sParm3[i], ExpVals3[i]) != 0)
				fprintf (logfile, "#%d: Output val different from expected val, outputval : %s\tExpected val : %s\n", i, sParm3[i], ExpVals3[i]);
			iTestsFailed++;
		}

		sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
	}
}

/*
SQL_C_TYPE_TIMESTAMP
SQL_TIMESTAMP_STRUCT 
struct tagTIMESTAMP_STRUCT {
SQLSMALLINT year; 
SQLUSMALLINT month; 
SQLUSMALLINT day; 
SQLUSMALLINT hour; 
SQLUSMALLINT minute; 
SQLUSMALLINT second; 
SQLUINTEGER fraction;
} TIMESTAMP_STRUCT;
*/

void ODBCSPJTest7 ()
{
	fprintf (logfile, "N0124\n");
	sprintf (strSQL, "{CALL N0124(?,?,?)}");
	char sParm1[4][20] = {"2002-12-30 22:22:22", "1001-01-01 01:01:01", "9999-12-31 23:59:59"};
	SQL_TIMESTAMP_STRUCT sParm2[4];
	SQL_TIMESTAMP_STRUCT sParm3[4] = {{1001,11,11,10,11,11,0}, {9999,12,31,12,59,59,0}, {1001,1,1,0,0,0,0}};
	char ExpVals2[4][51] = {"1001-11-11 10:11:11.000000000", "9999-12-31 12:59:59.000000000", "1001-01-01 00:00:00.000000000"};
	char ExpVals3[4][51] = {"2002-12-30 22:22:22.000000000", "1001-01-01 01:01:01.000000000", "9999-12-31 23:59:59.000000000"};
	SQLLEN	cbParm = SQL_NTS;

	for (int i = 0; i < 3; i++)
	{
		iTestsRun++;
		SQLLEN	cbParm = SQL_NTS;

		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, 0, 0, sParm1[i], 19, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_TIMESTAMP, 0, 0, &sParm2[i], 0, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 3, SQL_PARAM_INPUT_OUTPUT, SQL_C_CHAR, SQL_TIMESTAMP, 0, 0, &sParm3[i], 0, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		sqlret = SQLExecute (hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		char p2[51], p3[51];
		sprintf (p2, "%4d-%02d-%02d %02d:%02d:%02d.%06d", sParm2[i].year, sParm2[i].month, sParm2[i].day, sParm2[i].hour, sParm2[i].minute, sParm2[i].second, sParm2[i].fraction);
		sprintf (p3, "%4d-%02d-%02d %02d:%02d:%02d.%06d", sParm3[i].year, sParm3[i].month, sParm3[i].day, sParm3[i].hour, sParm3[i].minute, sParm3[i].second, sParm3[i].fraction);

		if ((strcmp ((char *)p2[i], ExpVals2[i]) != 0) || (strcmp ((char *)p3[i], ExpVals3[i]) != 0))
		{
			if (strcmp ((char *)p2[i], ExpVals2[i]) != 0)
				fprintf (logfile, "#%d: Output val different from expected val, outputval : %s\tExpected val : %s\n", i, p2, ExpVals2[i]);
			if (strcmp ((char *)p3[i], ExpVals3[i]) != 0)
				fprintf (logfile, "#%d: Output val different from expected val, outputval : %s\tExpected val : %s\n", i, p3, ExpVals3[i]);
			iTestsFailed++;
		}

		sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
	}
}

void ODBCSPJTest7Char ()
{
	fprintf (logfile, "N0124 SQL_C_CHAR\n");
	sprintf (strSQL, "{CALL N0124(?,?,?)}");
	char	sParm1[4][20] = {"2002-12-30 22:22:22", "1001-01-01 01:01:01", "9999-12-31 23:59:59"};
	//char	sParm1[4][25] = {"2002-12-30 22:22:22.123", "1001-01-01 01:01:01.456", "9999-12-31 23:59:59.789"};
	char	sParm2[4][51];
	char	sParm3[4][51] = {"1001-11-11 10:11:11", "9999-12-31 12:59:59", "1001-01-01 00:00:00"};
	char	ExpVals2[4][51] = {"1001-11-11 10:11:11.000000", "9999-12-31 12:59:59.000000", "1001-01-01 00:00:00.000000"};
	char	ExpVals3[4][51] = {"2002-12-30 22:22:22.000000", "1001-01-01 01:01:01.000000", "9999-12-31 23:59:59.000000"};
	SQLLEN	cbParm = SQL_NTS;

	for (int i = 0; i < 3; i++)
	{
		iTestsRun++;
		SQLLEN	cbParm = SQL_NTS;

		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, 0, 0, sParm1[i], 25, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_TIMESTAMP, 0, 0, sParm2[i], 50, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 3, SQL_PARAM_INPUT_OUTPUT, SQL_C_CHAR, SQL_TIMESTAMP, 0, 0, sParm3[i], 50, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		sqlret = SQLExecute (hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		if ((strcmp (sParm2[i], ExpVals2[i]) != 0) || (strcmp (sParm3[i], ExpVals3[i]) != 0))
		{
			if (strcmp (sParm2[i], ExpVals2[i]) != 0)
				fprintf (logfile, "#%d: Output val different from expected val, outputval : %s\tExpected val : %s\n", i, sParm2[i], ExpVals2[i]);
			if (strcmp (sParm3[i], ExpVals3[i]) != 0)
				fprintf (logfile, "#%d: Output val different from expected val, outputval : %s\tExpected val : %s\n", i, sParm3[i], ExpVals3[i]);
			iTestsFailed++;
		}

		sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
	}
}

/*
SQL_C_NUMERIC 
SQL_NUMERIC_STRUCT 
struct tagSQL_NUMERIC_STRUCT {
SQLCHAR precision;
SQLSCHAR scale; 
SQLCHAR sign [g]; 
SQLCHAR
val[SQL_MAX_NUMERIC_LEN]; [e], [f] 
} SQL_NUMERIC_STRUCT; 
*/

void ODBCSPJTest8 ()
{
	fprintf (logfile, "N0202\n");
	sprintf (strSQL, "{CALL N0202(?,?)}");
	//char	sParm1[6][50] = {"78765412.98776", "0.00000", "-765.89000", "99999999.99999", "-9999999.99999"};
	//char	sParm2[6][50];

	// 7876541298776 is 729E6723858 in hex
	// 76589000 is 490A7C8 in hex
	// 9999999999999 is E8D4A50FFF in hex

	SQL_NUMERIC_STRUCT sParm1[6] = {{0,0,1,{0x58, 0x38, 0x72, 0xE6, 0x29, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}}, 
									{0,0,1,{0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}},
									{0,0,0,{0xC8, 0xA7, 0x90, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}},
									{0,0,1,{0xFF, 0x0F, 0xA5, 0xD4, 0xE8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}},
									{0,0,0,{0xFF, 0x0F, 0xA5, 0xD4, 0xE8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}}};
	
	SQL_NUMERIC_STRUCT sParm2[6];
	SQLLEN	cbParm = SQL_NTS;

	for (int i = 0; i < 5; i++)
	{
		iTestsRun++;
		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_NUMERIC, SQL_NUMERIC, 14, 5, &sParm1[i], 0, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_NUMERIC, SQL_NUMERIC, 14, 5, &sParm2[i], 0, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		sqlret = SQLExecute (hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		if (strtohextoval(sParm1[i]) != strtohextoval(sParm2[i]))
		{
			fprintf (logfile, "#%d: Output val different from expected val, outputval : %ld\tExpected val : %ld\n", i, strtohextoval(sParm2[i]), strtohextoval(sParm1[i]));
			iTestsFailed++;
		}

		sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
	}
}

void ODBCSPJTest8Char ()
{
	fprintf (logfile, "N0202 SQL_C_CHAR\n");
	sprintf (strSQL, "{CALL N0202(?,?)}");
	//char	sParm1[6][50] = {"78765412.98776", "0.00000", "-765.89000", "99999999.99999", "-9999999.99999"};
	char	sParm1[6][50] = {"78765412", "0", "-765", "99999999", "-9999999"};
	char	sParm2[6][50];
	SQLLEN	cbParm = SQL_NTS;

	for (int i = 0; i < 5; i++)
	{
		iTestsRun++;
		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_NUMERIC, 0, 0, sParm1[i], 50, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_NUMERIC, 0, 0, sParm2[i], 50, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		sqlret = SQLExecute (hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		if (strcmp (sParm1[i], sParm2[i]) != 0)
		{
			fprintf (logfile, "#%d: Output val different from expected val, outputval : %s\tExpected val : %s\n", i, sParm2[i], sParm1[i]);
			iTestsFailed++;
		}

		sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
	}
}

void ODBCSPJTest9 ()
{
	fprintf (logfile, "N0209\n");
	sprintf (strSQL, "{CALL N0209(?,?)}");
	short	sParm1[6] = {12345, 0, -1, -32768, +32767};
	short	sParm2[6];// = {12345, 0, -1, -32768, +32767};
	SQLLEN	cbParm = SQL_NTS;

	for (int i = 0; i < 5; i++)
	{
		iTestsRun++;
		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_SHORT, SQL_SMALLINT, 0, 0, &sParm1[i], 0, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_SHORT, SQL_SMALLINT, 0, 0, &sParm2[i], 0, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		sqlret = SQLExecute (hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		if (sParm1[i]!= sParm2[i])
		{
			fprintf (logfile, "#%d: Output val different from expected val, outputval : %+d\tExpected val : %+d\n", i, sParm2[i], sParm1[i]);
			iTestsFailed++;
		}

		sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
	}
}

void ODBCSPJTest9Char ()
{
	fprintf (logfile, "N0209 SQL_C_CHAR\n");
	sprintf (strSQL, "{CALL N0209(?,?)}");
	char sParm1[6][10] = {"12345", "0", "-1", "-32768", "32767"};
	char sParm2[6][10];// = {12345, 0, -1, -32768, +32767};
	SQLLEN	cbParm = SQL_NTS;

	for (int i = 0; i < 5; i++)
	{
		iTestsRun++;
		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_SMALLINT, 0, 0, sParm1[i], 10, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_SMALLINT, 0, 0, sParm2[i], 10, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		sqlret = SQLExecute (hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		if (strcmp (sParm1[i], sParm2[i]) != 0)
		{
			fprintf (logfile, "#%d: Output val different from expected val, outputval : %s\tExpected val : %s\n", i, sParm2[i], sParm1[i]);
			iTestsFailed++;
		}

		sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
	}
}

void ODBCSPJTest10 ()
{
	fprintf (logfile, "N0210\n");
	sprintf (strSQL, "{CALL N0210(?,?)}");
	int	sParm1[6] = {123456789, 0, -1, -2147483648, +2147483647};
	int	sParm2[6];// = {123456789, 0, -1, -2147483648, +2147483647};
	SQLLEN	cbParm = SQL_NTS;

	for (int i = 0; i < 5; i++)
	{
		iTestsRun++;
		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &sParm1[i], 0, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &sParm2[i], 0, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		sqlret = SQLExecute (hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		if (sParm1[i]!= sParm2[i])
		{
			fprintf (logfile, "#%d: Output val different from expected val, outputval : %+d\tExpected val : %+d\n", i, sParm2[i], sParm1[i]);
			iTestsFailed++;
		}

		sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
	}
}

void ODBCSPJTest10Char ()
{
	fprintf (logfile, "N0210 SQL_C_CHAR\n");
	sprintf (strSQL, "{CALL N0210(?,?)}");
	char sParm1[6][20] = {"123456789", "0", "-1", "-2147483648", "2147483647"};
	char sParm2[6][20];// = {123456789, 0, -1, -2147483648, +2147483647};
	SQLLEN	cbParm = SQL_NTS;

	for (int i = 0; i < 5; i++)
	{
		iTestsRun++;
		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_INTEGER, 0, 0, sParm1[i], 20, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_INTEGER, 0, 0, sParm2[i], 20, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		sqlret = SQLExecute (hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		if (strcmp (sParm1[i], sParm2[i]) != 0)
		{
			fprintf (logfile, "#%d: Output val different from expected val, outputval : %+s\tExpected val : %+s\n", i, sParm2[i], sParm1[i]);
			iTestsFailed++;
		}

		sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
	}
}

void ODBCSPJTest11 ()
{
	fprintf (logfile, "N0211\n");
	sprintf (strSQL, "{CALL N0211(?,?)}");
	//_int64 sParm1[7] = {123456789987654321, 
	//					0, 
	//					-1, 
	//					-9223372036854775807, 
	//					-9223372036854775808/*-2**63*/, 
	//					9223372036854775807/*2**63-1*/};
	_int64  sParm1[7] = { 123456789, 0, -1, -123456788, -123456789, 123456789 }; 
	_int64 	sParm2[7];
	SQLLEN	cbParm = SQL_NTS;

	for (int i = 0; i < 6; i++)
	{
		iTestsRun++;
		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_SBIGINT, SQL_BIGINT, 0, 0, &sParm1[i], 0, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_SBIGINT, SQL_BIGINT, 0, 0, &sParm2[i], 0, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		sqlret = SQLExecute (hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		if (sParm1[i]!= sParm2[i])
		{
			fprintf (logfile, "#%d: Output val different from expected val, outputval : %+I64d\tExpected val : %+I64d\n", i, sParm2[i], sParm1[i]);
			iTestsFailed++;
		}

		sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
	}
}

void ODBCSPJTest11Char ()
{
	fprintf (logfile, "N0211 SQL_C_CHAR\n");
	sprintf (strSQL, "{CALL N0211(?,?)}");
	char sParm1[7][30] = {"123456789987654321", "0", "-1", "-9223372036854775807", "-9223372036854775808"/*-2**63*/, "9223372036854775807"/*2**63-1*/};
	char sParm2[7][30];
	SQLLEN	cbParm = SQL_NTS;

	for (int i = 0; i < 6; i++)
	{
		iTestsRun++;
		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_BIGINT, 0, 0, sParm1[i], 30, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_BIGINT, 0, 0, sParm2[i], 30, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		sqlret = SQLExecute (hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		if (strcmp (sParm1[i], sParm2[i]) != 0)
		{
			fprintf (logfile, "#%d: Output val different from expected val, outputval : %s\tExpected val : %s\n", i, sParm2[i], sParm1[i]);
			iTestsFailed++;
		}

		sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
	}
}

void ODBCSPJTest12 ()
{
	fprintf (logfile, "N0212\n");
	sprintf (strSQL, "{CALL N0212(?,?)}"); //FLOAT(22)
	float	sParm1[6] = {12345.3447265, 0.0000000, -123.89567453, 1.0000000, 99999.9999999};
	float	sParm2[6];// = {12345.3447265, 0.0000000, -123.89567453, 1.0000000, 99999.9999999};
	SQLLEN	cbParm = SQL_NTS;

	for (int i = 0; i < 5; i++)
	{
		iTestsRun++;
		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_FLOAT, SQL_REAL, 0, 0, &sParm1[i], 0, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_FLOAT, SQL_REAL, 0, 0, &sParm2[i], 0, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		sqlret = SQLExecute (hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		if (fabs(sParm1[i] - sParm2[i]) > 0.005)
		{
			fprintf (logfile, "#%d: Output val different from expected val, outputval : %f\tExpected val : %f\n", i, sParm2[i], sParm1[i]);
			iTestsFailed++;
		}

		sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
	}
}

void ODBCSPJTest12Char ()
{
	fprintf (logfile, "N0212 SQL_C_CHAR\n");
	sprintf (strSQL, "{CALL N0212(?,?)}"); //FLOAT(22)
	char sParm1[6][20] = {"12345.3447265", "0.0000000", "-123.89567453", "1.0000000", "99999.9999999"};
	char sParm2[6][20];// = {12345.3447265, 0.0000000, -123.89567453, 1.0000000, 99999.9999999};
	SQLLEN	cbParm = SQL_NTS;

	for (int i = 0; i < 5; i++)
	{
		iTestsRun++;
		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_REAL, 0, 0, sParm1[i], 20, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_REAL, 0, 0, sParm2[i], 20, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		sqlret = SQLExecute (hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		if (strcmp (sParm1[i], sParm2[i]) != 0)
		{
			fprintf (logfile, "#%d: Output val different from expected val, outputval : %s\tExpected val : %s\n", i, sParm2[i], sParm1[i]);
			iTestsFailed++;
		}

		sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
	}
}

void ODBCSPJTest13 ()
{
	fprintf (logfile, "N0213\n");
	sprintf (strSQL, "{CALL N0213(?,?)}");
	long double	sParm1[6] = {123434345.3447265634472656, 0.000000000000000, -99999.9999999999, 99999.9999999999, -1234567.2345678};
	long double	sParm2[6];// = {123434345.3447265634472656, 0.000000000000000, -99999.9999999999, 99999.9999999999, -1234567.2345678};
	SQLLEN	cbParm = SQL_NTS;

	for (int i = 0; i < 5; i++)
	{
		iTestsRun++;
		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_DOUBLE, SQL_DOUBLE, 0, 0, &sParm1[i], 0, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_DOUBLE, SQL_DOUBLE, 0, 0, &sParm2[i], 0, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		sqlret = SQLExecute (hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		if (sParm1[i]!= sParm2[i])
		{
			fprintf (logfile, "#%d: Output val different from expected val, outputval : %lf\tExpected val : %lf\n", i, sParm2[i], sParm1[i]);
			iTestsFailed++;
		}

		sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
	}
}

void ODBCSPJTest13Char ()
{
	fprintf (logfile, "N0213 SQL_C_CHAR\n");
	sprintf (strSQL, "{CALL N0213(?,?)}");
	char sParm1[6][30] = {"123434345.3447265634472656", "0.000000000000000", "-99999.9999999999", "99999.9999999999", "-1234567.2345678"};
	char sParm2[6][30];// = {123434345.3447265634472656, 0.000000000000000, -99999.9999999999, 99999.9999999999, -1234567.2345678};
	SQLLEN	cbParm = SQL_NTS;

	for (int i = 0; i < 5; i++)
	{
		iTestsRun++;
		sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_DOUBLE, 0, 0, sParm1[i], 30, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		cbParm = SQL_NTS;
		sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_DOUBLE, 0, 0, sParm2[i], 30, &cbParm);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
		
		sqlret = SQLExecute (hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}

		if (strcmp (sParm1[i], sParm2[i]) != 0)
		{
			fprintf (logfile, "#%d: Output val different from expected val, outputval : %s\tExpected val : %s\n", i, sParm2[i], sParm1[i]);
			iTestsFailed++;
		}

		sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
		if (sqlret != SQL_SUCCESS)
		{
			LogAllErrors (henv, hdbc, hstmt);
			return;
		}
	}
}

/*
SQL_C_TYPE_TIME 
SQL_TIME_STRUCT 
struct tagTIME_STRUCT {
SQLUSMALLINT hour; 
SQLUSMALLINT minute; 
SQLUSMALLINT second; 
} TIME_STRUCT;
*/

void ODBCSPJTest14 ()
{
	fprintf (logfile, "N0216\n");
	sprintf (strSQL, "{CALL N0216(?,?)}");
 	SQL_TIME_STRUCT sParm1 = {12, 45, 34};;
	SQL_TIME_STRUCT sParm2;
	SQLLEN	cbParm = SQL_NTS;

	iTestsRun++;
	sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
	sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_TYPE_TIME, SQL_TIME, 0, 0, &sParm1, 0, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
	cbParm = SQL_NTS;
	sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_TYPE_TIME, SQL_TIME, 0, 0, &sParm2, 0, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
	
	sqlret = SQLExecute (hstmt);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char p1[20], p2[20];
	sprintf (p1, "%d:%d:%d", sParm1.hour, sParm1.minute, sParm1.second);
	sprintf (p2, "%d:%d:%d", sParm2.hour, sParm2.minute, sParm2.second);
	if (strcmp (p1, p2) != 0)
	{
		fprintf (logfile, "Output val different from expected val, outputval : %s\tExpected val : %s\n", p2, p1);
		iTestsFailed++;
	}

	sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
}

void ODBCSPJTest14Char ()
{
	fprintf (logfile, "N0216 SQL_C_CHAR\n");
	sprintf (strSQL, "{CALL N0216(?,?)}");
 	char	sParm1[50];
	char	sParm2[50];
	SQLLEN	cbParm = SQL_NTS;

	iTestsRun++;
	sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
	strcpy (sParm1, "12:45:34");
	sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_TIME, 0, 0, sParm1, 50, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
	cbParm = SQL_NTS;
	sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_TIME, 0, 0, sParm2, 50, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
	
	sqlret = SQLExecute (hstmt);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	if (strcmp (sParm1, sParm2) != 0)
	{
		fprintf (logfile, "Output val different from expected val, outputval : %s\tExpected val : %s\n", sParm2, sParm1);
		iTestsFailed++;
	}

	sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
}

void ODBCSPJTest15 ()
{
	fprintf (logfile, "N1336A\n");
	sprintf (strSQL, "{CALL N1336A(?,?)}");
 	short	sParm1 = 1234;
	short	sParm2;
	SQLLEN	cbParm = SQL_NTS;

	iTestsRun++;
	sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
	sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_SHORT, SQL_INTEGER, 0, 0, &sParm1, 0, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
	cbParm = SQL_NTS;
	sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_SHORT, SQL_INTEGER, 0, 0, &sParm2, 0, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
	
	sqlret = SQLExecute (hstmt);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	fprintf (logfile, "Param 2 OUT value = %d\n", sParm2);

	sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
}

void ODBCSPJTest15Char ()
{
	fprintf (logfile, "N1336A SQL_C_CHAR\n");
	sprintf (strSQL, "{CALL N1336A(?,?)}");
 	char sParm1[5] = "1234";
	char sParm2[5];
	SQLLEN	cbParm = SQL_NTS;

	iTestsRun++;
	sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
	sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_INTEGER, 0, 0, sParm1, 5, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
	cbParm = SQL_NTS;
	sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_INTEGER, 0, 0, sParm2, 5, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
	
	sqlret = SQLExecute (hstmt);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	fprintf (logfile, "Param 1 IN value = %s\n", sParm1);
	fprintf (logfile, "Param 2 OUT value = %s\n", sParm2);

	sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
}

void ODBCSPJTest4 ()
{
	fprintf (logfile, "N0226A\n");
	sprintf (strSQL, "{CALL N0226A(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)}");

	iTestsRun++;
	sqlret = SQLPrepare (hstmt, (SQLCHAR *)strSQL, strlen(strSQL));
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	SQLLEN cbParm = SQL_NTS;

	char Param1[100];
	//ipar, fParamType, fCTypes, fSqlType, cbColDef, ibScale, cbValueMax, *pcbValue, SQL_LEN_DATA_AT_EXEC, *rgbValue
	//1, SQL_PARAM_INPUT=1, SQL_C_CHAR=1, SQL_VARCHAR=12, 0, 0, 0, SQL_NTS=-3, FALSE, "hello" 
	strcpy (Param1, "hello");
	sqlret = SQLBindParameter (hstmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, 0, 0, Param1, 100, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	SQLSMALLINT Param2 = 123;
	//2, SQL_PARAM_INPUT=1, SQL_C_SHORT=5, SQL_INTEGER=4, 0, 0, 0, SQL_NTS=-3, FALSE, 123 
	sqlret = SQLBindParameter (hstmt, 2, SQL_PARAM_INPUT, SQL_C_SSHORT, SQL_INTEGER, 0, 0, &Param2, 0, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param3[100];
	//3, SQL_PARAM_INPUT=1, SQL_C_CHAR=1, SQL_CHAR=1, 0, 0, 0, SQL_NTS=-3, FALSE, "compapa" 
	strcpy (Param3, "compapa");
	sqlret = SQLBindParameter (hstmt, 3, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR, 0, 0, Param3, 100, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param4[100];
	//4, SQL_PARAM_INPUT=1, SQL_C_CHAR=1, SQL_VARCHAR=12, 0, 0, 0, SQL_NTS=-3, FALSE, "hp" 
	strcpy (Param4, "hp");
	sqlret = SQLBindParameter (hstmt, 4, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, 0, 0, Param4, 100, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param5[100];
	strcpy (Param5, "145.23");
	//5, SQL_PARAM_INPUT=1, SQL_C_NUMERIC=2, SQL_NUMERIC=2, 6, 2, 0, SQL_NTS=-3, FALSE, 145.23 
	sqlret = SQLBindParameter (hstmt, 5, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_NUMERIC, 6, 2, &Param5, 7, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	SQLSMALLINT Param6 = 2345;
	//6, SQL_PARAM_INPUT=1, SQL_C_SHORT=5, SQL_SMALLINT=5, 0, 0, 0, SQL_NTS=-3, FALSE, 2345 
	sqlret = SQLBindParameter (hstmt, 6, SQL_PARAM_INPUT, SQL_C_SHORT, SQL_SMALLINT, 0, 0, &Param6, 0, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param7[100];
	//7, SQL_PARAM_INPUT=1, SQL_C_CHAR=1, SQL_DATE=9, 0, 0, 0, SQL_NTS=-3, FALSE, "2002-12-12" 
	strcpy (Param7, "2002-12-12");
	sqlret = SQLBindParameter (hstmt, 7, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_DATE, 0, 0, &Param7, 100, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param8[100];
	//8, SQL_PARAM_INPUT=1, SQL_C_CHAR=1, SQL_TIME=10, 0, 0, 0, SQL_NTS=-3, FALSE, "12:45:45" 
	strcpy (Param8, "12:45:45");
	sqlret = SQLBindParameter (hstmt, 8, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_TIME, 0, 0, &Param8, 100, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param9[100];
	//9, SQL_PARAM_INPUT=1, SQL_C_CHAR=1, SQL_TIMESTAMP=11, 0, 0, 0, SQL_NTS=-3, FALSE, "2002-12-12 12:12:12.234" 
	strcpy (Param9, "2002-12-12 12:12:12.234");
	sqlret = SQLBindParameter (hstmt, 9, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_TIMESTAMP, 0, 0, &Param9, 100, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	long Param10 = 234561;
	//10, SQL_PARAM_INPUT=1, SQL_C_LONG=4, SQL_BIGINT=-5, 0, 0, 0, SQL_NTS=-3, FALSE, 234561 
	sqlret = SQLBindParameter (hstmt, 10, SQL_PARAM_INPUT, SQL_C_LONG, SQL_BIGINT, 0, 0, &Param10, 0, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	double Param11 = 123.345;
	//11, SQL_PARAM_INPUT=1, SQL_C_DOUBLE=8, SQL_FLOAT=6, 7, 3, 0, SQL_NTS=-3, FALSE, 123.345 
	sqlret = SQLBindParameter (hstmt, 11, SQL_PARAM_INPUT, SQL_C_DOUBLE, SQL_FLOAT, 7, 3, &Param11, 0, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
	
	float Param12 = 2345.64;
	//12, SQL_PARAM_INPUT=1, SQL_C_FLOAT=7, SQL_REAL=7, 7, 2, 0, SQL_NTS=-3, FALSE, 2345.64990234375 
	sqlret = SQLBindParameter (hstmt, 12, SQL_PARAM_INPUT, SQL_C_FLOAT, SQL_REAL, 7, 2, &Param12, 0, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
	
	double Param13 = 3452.78;
	//13, SQL_PARAM_INPUT=1, SQL_C_DOUBLE=8, SQL_DOUBLE=8, 7, 2, 0, SQL_NTS=-3, FALSE, 3452.7800000000002 
	sqlret = SQLBindParameter (hstmt, 13, SQL_PARAM_INPUT, SQL_C_DOUBLE, SQL_DOUBLE, 7, 2, &Param13, 0, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param14[100];
	//14, SQL_PARAM_INPUT=1, SQL_C_NUMERIC=2, SQL_NUMERIC=2, 5, 2, 0, SQL_NTS=-3, FALSE, 45.65 
	strcpy (Param14, "45.65");
	sqlret = SQLBindParameter (hstmt, 14, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_NUMERIC, 5, 2, &Param14, 6, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param15[100];
	//15, SQL_PARAM_INPUT=1, SQL_C_NUMERIC=2, SQL_NUMERIC=2, 6, 2, 0, SQL_NTS=-3, FALSE, 456.76 
	strcpy (Param15, "456.76");
	sqlret = SQLBindParameter (hstmt, 15, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_NUMERIC, 6, 2, &Param15, 7, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param16[100]; 
	strcpy (Param16, "6785");
	//16, SQL_PARAM_INPUT=1, SQL_C_NUMERIC=2, SQL_NUMERIC=2, 9, 0, 0, SQL_NTS=-3, FALSE, 6785 
	sqlret = SQLBindParameter (hstmt, 16, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_NUMERIC, 5, 0, &Param16, 5, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param17[100];
	strcpy (Param17, "54678");
	//17, SQL_PARAM_INPUT=1, SQL_C_NUMERIC=2, SQL_NUMERIC=2, 9, 0, 0, SQL_NTS=-3, FALSE, 54678 
	sqlret = SQLBindParameter (hstmt, 17, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_NUMERIC, 6, 0, &Param17, 6, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param18[100];
	//18, SQL_PARAM_OUTPUT=4, SQL_C_CHAR=1, SQL_VARCHAR=12, 0, 0, 300, 5, FALSE, "hello" 
	sqlret = SQLBindParameter (hstmt, 18, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_VARCHAR, 0, 0, Param18, 100, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	SQLSMALLINT Param19 = 0;
	//19, SQL_PARAM_OUTPUT=4, SQL_C_SHORT=5, SQL_INTEGER=4, 0, 0, 0, 2, FALSE, 123 
	sqlret = SQLBindParameter (hstmt, 19, SQL_PARAM_OUTPUT, SQL_C_SHORT, SQL_INTEGER, 0, 0, &Param19, 0, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param20[100];
	//20, SQL_PARAM_OUTPUT=4, SQL_C_CHAR=1, SQL_CHAR=1, 0, 0, 300, 15, FALSE, "compap         " 
	sqlret = SQLBindParameter (hstmt, 20, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_CHAR, 0, 0, Param20, 100, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param21[100];
	//21, SQL_PARAM_OUTPUT=4, SQL_C_CHAR=1, SQL_VARCHAR=12, 0, 0, 300, 2, FALSE, "hp" 
	sqlret = SQLBindParameter (hstmt, 21, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_VARCHAR, 0, 0, Param21, 100, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param22[100];
	//22, SQL_PARAM_OUTPUT=4, SQL_C_NUMERIC=2, SQL_NUMERIC=2, 6, 2, 0, 19, FALSE, 145.23 
	sqlret = SQLBindParameter (hstmt, 22, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_NUMERIC, 0, 0, &Param22, 100, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	SQLSMALLINT Param23 = 0;
	//23, SQL_PARAM_OUTPUT=4, SQL_C_SHORT=5, SQL_SMALLINT=5, 0, 0, 0, 2, FALSE, 2345 
	sqlret = SQLBindParameter (hstmt, 23, SQL_PARAM_OUTPUT, SQL_C_SHORT, SQL_SMALLINT, 0, 0, &Param23, 0, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param24[100];
	//24, SQL_PARAM_OUTPUT=4, SQL_C_CHAR=1, SQL_DATE=9, 0, 0, 300, 10, FALSE, "2002-12-12" 
	sqlret = SQLBindParameter (hstmt, 24, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_DATE, 0, 0, Param24, 100, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param25[100];
	//25, SQL_PARAM_OUTPUT=4, SQL_C_CHAR=1, SQL_TIME=10, 0, 0, 300, 8, FALSE, "12:45:45" 
	sqlret = SQLBindParameter (hstmt, 25, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_TIME, 0, 0, Param25, 100, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param26[100];
	//26, SQL_PARAM_OUTPUT=4, SQL_C_CHAR=1, SQL_TIMESTAMP=11, 0, 0, 300, 29, FALSE, "2002-12-12 12:12:12.234000000" 
	sqlret = SQLBindParameter (hstmt, 26, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_TIMESTAMP, 0, 0, Param26, 100, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	long Param27 = 0;
	//27, SQL_PARAM_OUTPUT=4, SQL_C_LONG=4, SQL_BIGINT=-5, 0, 0, 0, 4, FALSE, 234561 
	sqlret = SQLBindParameter (hstmt, 27, SQL_PARAM_OUTPUT, SQL_C_LONG, SQL_BIGINT, 0, 0, &Param27, 0, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	double Param28 = 0;
	//28, SQL_PARAM_OUTPUT=4, SQL_C_DOUBLE=8, SQL_FLOAT=6, 7, 3, 0, 8, FALSE, 123.345 
	sqlret = SQLBindParameter (hstmt, 28, SQL_PARAM_OUTPUT, SQL_C_DOUBLE, SQL_FLOAT, 7, 3, &Param28, 0, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	float Param29 = 0;
	//29, SQL_PARAM_OUTPUT=4, SQL_C_FLOAT=7, SQL_REAL=7, 7, 2, 0, 4, FALSE, 2345.64990234375 
	sqlret = SQLBindParameter (hstmt, 29, SQL_PARAM_OUTPUT, SQL_C_FLOAT, SQL_REAL, 7, 2, &Param29, 0, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	double Param30 = 0;
	//30, SQL_PARAM_OUTPUT=4, SQL_C_DOUBLE=8, SQL_DOUBLE=8, 7, 2, 0, 8, FALSE, 3452.7800000000002 
	sqlret = SQLBindParameter (hstmt, 30, SQL_PARAM_OUTPUT, SQL_C_DOUBLE, SQL_DOUBLE, 7, 2, &Param30, 0, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param31[100];
	//31, SQL_PARAM_OUTPUT=4, SQL_C_NUMERIC=2, SQL_NUMERIC=2, 5, 2, 0, 19, FALSE, 45.65000 
	sqlret = SQLBindParameter (hstmt, 31, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_NUMERIC, 0, 0, &Param31, 100, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param32[100];
	//32, SQL_PARAM_OUTPUT=4, SQL_C_NUMERIC=2, SQL_NUMERIC=2, 6, 2, 0, 19, FALSE, 456.76 
	sqlret = SQLBindParameter (hstmt, 32, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_NUMERIC, 0, 0, &Param32, 100, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param33[100];
	//33, SQL_PARAM_OUTPUT=4, SQL_C_NUMERIC=2, SQL_NUMERIC=2, 9, 0, 0, 19, FALSE, 6785 
	sqlret = SQLBindParameter (hstmt, 33, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_NUMERIC, 0, 0, &Param33, 100, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	char Param34[100];
	//34, SQL_PARAM_OUTPUT=4, SQL_C_NUMERIC=2, SQL_NUMERIC=2, 9, 0, 0, 19, FALSE, 54678 
	sqlret = SQLBindParameter (hstmt, 34, SQL_PARAM_OUTPUT, SQL_C_CHAR, SQL_NUMERIC, 0, 0, &Param34, 100, &cbParm);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
	sqlret = SQLExecute (hstmt);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}

	fprintf (logfile, "Param1 = %s\t\tParam18 = %s\n", Param1, Param18);
	fprintf (logfile, "Param2 = %d\t\tParam19 = %d\n", Param2, Param19);
	fprintf (logfile, "Param3 = %s\t\tParam20 = %s\n", Param3, Param20);
	fprintf (logfile, "Param4 = %s\t\tParam21 = %s\n", Param4, Param21);
	fprintf (logfile, "Param5 = %s\t\tParam22 = %s\n", Param5, Param22);
	fprintf (logfile, "Param6 = %d\t\tParam23 = %d\n", Param6, Param23);
	fprintf (logfile, "Param7 = %s\t\tParam24 = %s\n", Param7, Param24);
	fprintf (logfile, "Param8 = %s\t\tParam25 = %s\n", Param8, Param25);
	fprintf (logfile, "Param9 = %s\t\tParam26 = %s\n", Param9, Param26);
	fprintf (logfile, "Param10 = %ld\t\tParam27 = %ld\n", Param10, Param27);
	fprintf (logfile, "Param11 = %f\t\tParam28 = %f\n", Param11, Param28);
	fprintf (logfile, "Param12 = %f\t\tParam29 = %f\n", Param12, Param29);
	fprintf (logfile, "Param13 = %f\t\tParam30 = %f\n", Param13, Param30);
	fprintf (logfile, "Param14 = %s\t\tParam31 = %s\n", Param14, Param31);
	fprintf (logfile, "Param15 = %s\t\tParam32 = %s\n", Param15, Param32);
	fprintf (logfile, "Param16 = %s\t\tParam33 = %s\n", Param16, Param33);
	fprintf (logfile, "Param17 = %s\t\tParam34 = %s\n", Param17, Param34);

	sqlret = SQLFreeStmt (hstmt, SQL_RESET_PARAMS);
	if (sqlret != SQL_SUCCESS)
	{
		LogAllErrors (henv, hdbc, hstmt);
		return;
	}
}

void ODBCSPJTests (void)
{
	iTestsRun = iTestsFailed = 0;
	logfile = fopen( "spjs.log", "w" );
	if (Connect ())
	{
		sqlret = SQLAllocHandle (SQL_HANDLE_STMT, hdbc, &hstmt);
		if (sqlret != SQL_SUCCESS)
		{
			Disconnect ();
			fprintf (logfile, "Error: SQLAllocHandle for STMT\n");
			return;
		}
		
		ODBCSPJTest4 ();	//all datatypes : N0226A
		ODBCSPJTest1 ();	// no params : N0001
		
		ODBCSPJTest5 ();	//IN DECIMAL(9) : N0101
		ODBCSPJTest2 ();	//IN VARCHAR, OUT VARCHAR : N0200
		//ODBCSPJTest8 ();	//IN NUMERIC(14,5), OUT NUMERIC(14,5) : N0202 //CrtN0202S
		ODBCSPJTest8Char ();
		ODBCSPJTest9 ();	//IN SMALLINT, OUT SMALLINT : N0209
		ODBCSPJTest9Char ();
		ODBCSPJTest10 ();	//IN INTEGER, OUT INTEGER : N0210
		ODBCSPJTest10Char ();
		ODBCSPJTest11 ();	//IN LARGEINT, OUT LARGEINT : N0211
		ODBCSPJTest11Char ();
		ODBCSPJTest12 ();	//IN FLOAT(22), OUT FLOAT(22) : N0212
		ODBCSPJTest12Char ();
		ODBCSPJTest13 ();	//IN FLOAT(54), OUT FLOAT(54) : N0213
		ODBCSPJTest13Char ();
		ODBCSPJTest14 ();	//IN TIME(0), OUT TIME(0) : N0216
		//ODBCSPJTest14Char ();
		ODBCSPJTest15 ();	//IN INTEGER, OUT INTEGER, CONTAINS SQL : N1336A
		ODBCSPJTest15Char ();
		ODBCSPJTest3 ();	//IN INTEGER, INOUT INTEGER, OUT INTEGER : N0302
		//ODBCSPJTest3Char ();
		//ODBCSPJTest6 ();	//IN VARCHAR(19), OUT DATE, INOUT DATE : N0122
		ODBCSPJTest6Char ();
		//ODBCSPJTest7 ();	//IN VARCHAR(19), OUT TIMESTAMP(6), INOUT TIMESTAMP(6) : N0124
		ODBCSPJTest7Char ();
		
		ODBCSPJTest3Char ();

//		ODBCSPJResultSetTests ();
				
		Disconnect ();
//		fprintf (logfile, "TestsRun : %d\tTestsPassed : %d\n", iTestsRun, iTestsPassed);
		fclose (logfile);
	}
}

bool Connect ()
{
	SQLRETURN sqlret;
	sqlret = SQLAllocHandle (SQL_HANDLE_ENV, SQL_NULL_HANDLE, &henv);
	if (sqlret != SQL_SUCCESS)
	{
		printf ("Error: SQLAllocHandle for ENV\n");
		return false;
	}
	
	sqlret = SQLSetEnvAttr (henv, SQL_ATTR_ODBC_VERSION, (void *)SQL_OV_ODBC3, SQL_NTS);
	if (sqlret != SQL_SUCCESS)
	{
		SQLFreeHandle (SQL_HANDLE_ENV, henv);
		henv = NULL;
		printf ("Error: SQLSetEnvAttr\n");
		return false;
	}
	sqlret = SQLAllocHandle (SQL_HANDLE_DBC, henv, &hdbc);
	if (sqlret != SQL_SUCCESS)
	{
		SQLFreeHandle (SQL_HANDLE_ENV, henv);
		henv = NULL;
		printf ("Error: SQLAllocHandle for DBC\n");
		return false;
	}

	sqlret = SQLConnect (hdbc, DSN, SQL_NTS, USR, SQL_NTS, PWD, SQL_NTS);
	if (sqlret != SQL_SUCCESS && sqlret != SQL_SUCCESS_WITH_INFO)
	{
		EnvErrorHandler (henv);
		DBCErrorHandler (hdbc);
		SQLFreeHandle (SQL_HANDLE_DBC, hdbc);
		SQLFreeHandle (SQL_HANDLE_ENV, henv);
		hdbc = NULL;
		henv = NULL;
		printf ("Error: SQLConnect\n");
		return false;
	}
	return true;
}

void Disconnect ()
{
	if (hstmt != NULL)
		SQLFreeHandle (SQL_HANDLE_STMT, hstmt);
	if (hdbc != NULL)
	{
		SQLDisconnect(hdbc);
		SQLFreeHandle (SQL_HANDLE_DBC, hdbc);
	}
	if (henv != NULL)
		SQLFreeHandle (SQL_HANDLE_ENV, henv);
	hstmt = NULL;
	hdbc = NULL;
	henv = NULL;
}

bool ExecDirect ()
{
	sqlret = SQLExecDirect (hstmt, (unsigned char *)strSQL, SQL_NTS);
	if (sqlret != SQL_SUCCESS)
	{
		EnvErrorHandler (henv);
		DBCErrorHandler (hdbc);
		StmtErrorHandler (hstmt);
		Disconnect ();
		printf ("Error: SQLExecDirect\n");
		return false;
	}

	return true;
}

void EnvErrorHandler (SQLHENV henv)
{
	char buf[500];
	char State[6];
	SDWORD	NativeError;
	RETCODE returncode;
	int i = 1;

	returncode = SQLGetDiagRec (SQL_HANDLE_ENV, henv, i, (unsigned char *)State, &NativeError, (unsigned char *)buf, 500, NULL);
	while((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
	{
		i++;
		State[5]='\0';
		//fprintf(logfile, "   State: %s\n   Native Error: %ld\n   Error: %s\n",State,NativeError,buf);
		printf("   State: %s\n   Native Error: %ld\n   Error: %s\n",State,NativeError,buf);
		returncode = SQLGetDiagRec (SQL_HANDLE_ENV, henv, i, (unsigned char *)State, &NativeError, (unsigned char *)buf, 500, NULL);
	}
}

void DBCErrorHandler (SQLHDBC hdbc)
{
	char buf[500];
	char State[6];
	SDWORD	NativeError;
	RETCODE returncode;
	int i = 1;

	returncode = SQLGetDiagRec (SQL_HANDLE_DBC, hdbc, i, (unsigned char *)State, &NativeError, (unsigned char *)buf, 500, NULL);
	while((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
	{
		i++;
		State[5]='\0';
		//fprintf(logfile, "   State: %s\n   Native Error: %ld\n   Error: %s\n",State,NativeError,buf);
		printf("   State: %s\n   Native Error: %ld\n   Error: %s\n",State,NativeError,buf);
		returncode = SQLGetDiagRec (SQL_HANDLE_DBC, hdbc, i, (unsigned char *)State, &NativeError, (unsigned char *)buf, 500, NULL);
	}
}

void StmtErrorHandler (SQLHSTMT hstmt)
{
	char buf[500];
	char errbuf[600];
	char State[6];
	SDWORD	NativeError;
	RETCODE returncode;
	int i = 1;

	returncode = SQLGetDiagRec (SQL_HANDLE_STMT, hstmt, i, (unsigned char *)State, &NativeError, (unsigned char *)buf, 500, NULL);
	while((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
	{
		i++;
		State[5]='\0';
		//sprintf(errbuf, "   State: %s\n   Native Error: %ld\n   Error: %s\n",State,NativeError,buf);
		//fprintf (logfile, "%s", errbuf);
		printf("   State: %s\n   Native Error: %ld\n   Error: %s\n",State,NativeError,buf);
		returncode = SQLGetDiagRec (SQL_HANDLE_STMT, hstmt, i, (unsigned char *)State, &NativeError, (unsigned char *)buf, 500, NULL);
	}
}

void LogAllErrors (SQLHENV henv, SQLHDBC hdbc, SQLHSTMT hstmt)
{
	iTestsFailed++;
//	fprintf (logfile, "Error!\n");
	printf ("Error!\n");
	EnvErrorHandler (henv);
	DBCErrorHandler (hdbc);
	StmtErrorHandler (hstmt);
}

void getCQD(char* cqd, char* buf) {
	SQLRETURN ret;
	SQLLEN dataPtr = SQL_NTS;
	char temp[512];
	char tempb[129];

	ret = SQLExecDirect(hstmt, (SQLCHAR*)"CONTROL QUERY DEFAULT SHOWCONTROL_UNEXTERNALIZED_ATTRS 'ON'", SQL_NTS);
	sprintf(temp, "SHOWCONTROL DEFAULT %s, MATCH FULL, NO HEADER", cqd);
    ret = SQLExecDirect(hstmt, (SQLCHAR*)temp, SQL_NTS);
    ret = SQLBindCol(hstmt, 1, SQL_C_CHAR, (SQLPOINTER) tempb, 128, &dataPtr); 
    ret = SQLFetch(hstmt);
	strcpy(buf, tempb);
    ret = SQLFreeStmt(hstmt, SQL_UNBIND);
    ret = SQLFreeStmt(hstmt, SQL_CLOSE);
    ret = SQLExecDirect(hstmt, (SQLCHAR*)"CONTROL QUERY DEFAULT SHOWCONTROL_UNEXTERNALIZED_ATTRS 'OFF'", SQL_NTS);
}
