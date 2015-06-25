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

/**************************************************************
** common.c
**
** This file contains all the common functions used by the 
** functions which do ODBC 2.0 testing.
**************************************************************/
#include <stdlib.h>    
#include <stdio.h> 
#include <string.h>
#include <windows.h>
#include <sqlext.h>
#include <assert.h>
#include <time.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#ifdef unixcli
#define PLATFORM
#define far
#endif

/****************************************************************
** Global data
****************************************************************/
BOOL g_Trace=FALSE;
TEST_GLOBALS;
/* new stuff */
CRITICAL_SECTION error_process_mutex;
int critical_count;
BOOL g_MPSyntax = FALSE;
/* end new stuff */

char	column_string[1000];
char	ColumnDefinition[100];

char	charset_file[256];
int		myLogID;

BOOL    isCharSet = FALSE;
BOOL    isUCS2 = FALSE;
char	*secondaryRole = "";

//char    secondaryRole[SQL_MAX_ROLENAME_LEN] = "odbc2";

/****************************************************************
** blank_pad()
** pads a string with blanks
****************************************************************/
void blank_pad( char *s, int len )
{
	int i;
	for ( i=strlen(s); i<(len-1); i++)
		s[i] = ' ';
	s[len-1] = '\0';
}


//************************************************************
// BufferToHex()
// This function will format a buffer to be displayed as a hex
// string.
//************************************************************
VOID BufferToHex( char *In
                , char *Out
                , int Length )
{
	int i;
	static char HexChars[] = "0123456789ABCDEF";
	
	if(Length <= 0 ){
		*Out='\0';
		return;
		}
	
	// convert the input bytes to hex
	for( i = 0; i < Length; i++ ){
		*Out++ = HexChars[(*In) >> 4];
		*Out++ = HexChars[(*In++) & 0X0F];
		}
	
	*Out = '\0';
	return;
	}  // end of BufferToHex


//************************************************************
// FormatHexOutput()
// This function will format a buffer to be displayed as a hex
// string followed by its ascii representation, if possible.
//************************************************************
VOID FormatHexOutput( char *In
                    , char *Out
                    , int Length )
{
	int i;
	char far *InBase = In;
	static char HexChars[] = "0123456789ABCDEF";
	
	if(Length <= 0 ){
		*Out='\0';
		return;
		}
	
	// format offset to 4 hex digits
	//*Out++ = HexChars[Offset >> 12];
	//*Out++ = HexChars[(Offset & 0X0FFF) >>  8];
	//*Out++ = HexChars[(Offset & 0X00FF) >>  4];
	//*Out++ = HexChars[ Offset & 0X000F];
	//*Out++ = ' ';
	//*Out++ = ' ';
	
	// convert the input bytes to hex
	for( i = 0; i < Length; i++ ){
		*Out++ = HexChars[(*In) >> 4];
		*Out++ = HexChars[(*In++) & 0X0F];
		*Out++ = ' ';
		}
	
	*Out++ = ' ';
	
	// Align the ascii to 16 data bytes
	//for( i = 0; i < (16-Length); i++ ){
		//*Out++ = ' ';
		//*Out++ = ' ';
		//*Out++ = ' ';
		//}
	
	// output the original data
	In = InBase;
	for( i = 0; i < Length; i++ ){
		if( isprint( *In ) )
			*Out++ = *In++;
		else{
			*Out++ = '.';
			++In;
			}
		}
	//*Out++ = '\n';
	*Out = '\0';
	
	return;
	
	}  // end of FormatHexOutput


/****************************************************************
** ReturncodeToChar()
**
** This function will attempt to convert a returncode from an
** ODBC function call into a more user friendly character string.
** If the returncode isn't one of the standard errors then this
** function converts the returncode into a numeric string.
****************************************************************/
char *ReturncodeToChar(RETCODE retcode, char *buf)
{
   switch (retcode) {
      case SQL_SUCCESS:
         strcpy (buf, "SQL_SUCCESS");
         break;
      case SQL_ERROR:
         strcpy (buf, "SQL_ERROR");
         break;
      case SQL_SUCCESS_WITH_INFO:
         strcpy (buf, "SQL_SUCCESS_WITH_INFO");
         break;
      case SQL_NO_DATA_FOUND:
         strcpy (buf, "SQL_NO_DATA_FOUND");
         break;
      case SQL_NEED_DATA:
         strcpy (buf, "SQL_NEED_DATA");
         break;
      case SQL_INVALID_HANDLE:
         strcpy (buf, "SQL_INVALID_HANDLE");
         break;
      case SQL_STILL_EXECUTING:
         strcpy (buf, "SQL_STILL_EXECUTING");
         break;
      default:
         _itoa(retcode,buf,10);
	}
	return buf;
}

/****************************************************************
** SQLTypeToChar()
**
** This function will attempt to convert a SQLType value from an
** ODBC function call into a more user friendly character string.
** If the SQLType isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
char *SQLTypeToChar(SWORD SQLType, char *buf)
{
   switch (SQLType) {
		case SQL_CHAR:		strcpy (buf,"SQL_CHAR");break;
		case SQL_WCHAR:		strcpy (buf,"SQL_WCHAR");break;
		case SQL_NUMERIC:	strcpy (buf,"SQL_NUMERIC");break;
		case SQL_DECIMAL:	strcpy (buf,"SQL_DECIMAL");break;
		case SQL_INTEGER:	strcpy (buf,"SQL_INTEGER");break;
		case SQL_SMALLINT:	strcpy (buf,"SQL_SMALLINT");break;
		case SQL_FLOAT:		strcpy (buf,"SQL_FLOAT");break;
		case SQL_REAL:		strcpy (buf,"SQL_REAL");break;
		case SQL_DOUBLE:	strcpy (buf,"SQL_DOUBLE");break;
		case SQL_VARCHAR:	strcpy (buf,"SQL_VARCHAR");break;
		case SQL_WVARCHAR:	strcpy (buf,"SQL_WVARCHAR");break;
		case SQL_DATE:		strcpy (buf,"SQL_DATE");break;
		case SQL_TYPE_DATE:	strcpy (buf,"SQL_DATE");break;
		case SQL_TIME:		strcpy (buf,"SQL_TIME");break;
		case SQL_TYPE_TIME:	strcpy (buf,"SQL_TIME");break;
		case SQL_BINARY:	strcpy (buf,"SQL_BINARY");break;
		case SQL_BIGINT:	strcpy (buf,"SQL_BIGINT");break;
		case SQL_TINYINT:	strcpy (buf,"SQL_TINYINT");break;
		case SQL_BIT:		strcpy (buf,"SQL_BIT");break;
		case SQL_TIMESTAMP:		strcpy (buf,"SQL_TIMESTAMP");break;
		case SQL_TYPE_TIMESTAMP: strcpy (buf,"SQL_TIMESTAMP");break;
		case SQL_LONGVARCHAR:	strcpy (buf,"SQL_LONGVARCHAR");break;
		case SQL_WLONGVARCHAR:	strcpy (buf,"SQL_WLONGVARCHAR");break;
		case SQL_VARBINARY:		strcpy (buf,"SQL_VARBINARY");break;
		case SQL_LONGVARBINARY:	strcpy (buf,"SQL_LONGVARBINARY");break;
		case SQL_INTERVAL_YEAR:	strcpy (buf,"SQL_INTERVAL_YEAR");break;
		case SQL_INTERVAL_MONTH:	strcpy (buf,"SQL_INTERVAL_MONTH");break;
		case SQL_INTERVAL_YEAR_TO_MONTH:	strcpy (buf,"SQL_INTERVAL_YEAR_TO_MONTH");break;
		case SQL_INTERVAL_DAY:		strcpy (buf,"SQL_INTERVAL_DAY");break;
		case SQL_INTERVAL_HOUR:		strcpy (buf,"SQL_INTERVAL_HOUR");break;
		case SQL_INTERVAL_MINUTE:	strcpy (buf,"SQL_INTERVAL_MINUTE");break;
		case SQL_INTERVAL_SECOND:	strcpy (buf,"SQL_INTERVAL_SECOND");break;
		case SQL_INTERVAL_DAY_TO_HOUR:	strcpy (buf,"SQL_INTERVAL_DAY_TO_HOUR");break;
		case SQL_INTERVAL_DAY_TO_MINUTE:	strcpy (buf,"SQL_INTERVAL_DAY_TO_MINUTE");break;
		case SQL_INTERVAL_DAY_TO_SECOND:	strcpy (buf,"SQL_INTERVAL_DAY_TO_SECOND");break;
		case SQL_INTERVAL_HOUR_TO_MINUTE:	strcpy (buf,"SQL_INTERVAL_HOUR_TO_MINUTE");break;
		case SQL_INTERVAL_HOUR_TO_SECOND:	strcpy (buf,"SQL_INTERVAL_HOUR_TO_SECOND");break;
		case SQL_INTERVAL_MINUTE_TO_SECOND:	strcpy (buf,"SQL_INTERVAL_MINUTE_TO_SECOND");break;
      default:
         _itoa(SQLType,buf,10);
	}
	return buf;
}

/****************************************************************
** SQLTypeToChar()
**
** This function will attempt to convert a character string SQLType
** value from an ODBC function call into SQLType.
** If the SQLType isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
SWORD	CharToSQLType(char *buffer)
{
	SWORD	SQLType = 999;
	
	if (_stricmp(buffer,"SQL_CHAR") == 0)
	{
		SQLType = SQL_CHAR;
	}
	else if (_stricmp(buffer,"SQL_NUMERIC") == 0)
	{
		SQLType = SQL_NUMERIC;
	}
	else if (_stricmp(buffer,"SQL_DECIMAL") == 0)
	{
		SQLType = SQL_DECIMAL;
	}
	else if (_stricmp(buffer,"SQL_INTEGER") == 0)
	{
		SQLType = SQL_INTEGER;
	}
	else if (_stricmp(buffer,"SQL_SMALLINT") == 0)
	{
		SQLType = SQL_SMALLINT;
	}
	else if (_stricmp(buffer,"SQL_FLOAT") == 0)
	{
		SQLType = SQL_FLOAT;
	}
	else if (_stricmp(buffer,"SQL_REAL") == 0)
	{
		SQLType = SQL_REAL;
	}
	else if (_stricmp(buffer,"SQL_DOUBLE") == 0)
	{
		SQLType = SQL_DOUBLE;
	}
	else if (_stricmp(buffer,"SQL_VARCHAR") == 0)
	{
		SQLType = SQL_VARCHAR;
	}
	else if (_stricmp(buffer,"SQL_DATE") == 0)
	{
		SQLType = SQL_DATE;
	}
	else if (_stricmp(buffer,"SQL_TIME") == 0)
	{
		SQLType = SQL_TIME;
	}
	else if (_stricmp(buffer,"SQL_BINARY") == 0)
	{
		SQLType = SQL_BINARY;
	}
	else if (_stricmp(buffer,"SQL_BIGINT") == 0)
	{
		SQLType = SQL_BIGINT;
	}
	else if (_stricmp(buffer,"SQL_TINYINT") == 0)
	{
		SQLType = SQL_TINYINT;
	}
	else if (_stricmp(buffer,"SQL_BIT") == 0)
	{
		SQLType = SQL_BIT;
	}
	else if (_stricmp(buffer,"SQL_TIMESTAMP") == 0)
	{
		SQLType = SQL_TIMESTAMP;
	}
	else if (_stricmp(buffer,"SQL_LONGVARCHAR") == 0)
	{
		SQLType = SQL_LONGVARCHAR;
	}
	else if (_stricmp(buffer,"SQL_VARBINARY") == 0)
	{
		SQLType = SQL_VARBINARY;
	}
	else if (_stricmp(buffer,"SQL_LONGVARBINARY") == 0)
	{
		SQLType = SQL_LONGVARBINARY;
	}
		else if (_stricmp(buffer,"SQL_INTERVAL_YEAR") == 0)
	{
		SQLType = SQL_INTERVAL_YEAR;
	}
	else if (_stricmp(buffer,"SQL_INTERVAL_MONTH") == 0)
	{
		SQLType = SQL_INTERVAL_MONTH;
	}
	else if (_stricmp(buffer,"SQL_INTERVAL_DAY") == 0)
	{
		SQLType = SQL_INTERVAL_DAY;
	}
	else if (_stricmp(buffer,"SQL_INTERVAL_HOUR") == 0)
	{
		SQLType = SQL_INTERVAL_HOUR;
	}
	else if (_stricmp(buffer,"SQL_INTERVAL_MINUTE") == 0)
	{
		SQLType = SQL_INTERVAL_MINUTE;
	}
	else if (_stricmp(buffer,"SQL_INTERVAL_SECOND") == 0)
	{
		SQLType = SQL_INTERVAL_SECOND;
	}
	else if (_stricmp(buffer,"SQL_INTERVAL_YEAR_TO_MONTH") == 0)
	{
		SQLType = SQL_INTERVAL_YEAR_TO_MONTH;
	}
	else if (_stricmp(buffer,"SQL_INTERVAL_DAY_TO_HOUR") == 0)
	{
		SQLType = SQL_INTERVAL_DAY_TO_HOUR;
	}
	else if (_stricmp(buffer,"SQL_INTERVAL_DAY_TO_MINUTE") == 0)
	{
		SQLType = SQL_INTERVAL_DAY_TO_MINUTE;
	}
	else if (_stricmp(buffer,"SQL_INTERVAL_DAY_TO_SECOND") == 0)
	{
		SQLType = SQL_INTERVAL_DAY_TO_SECOND;
	}
	else if (_stricmp(buffer,"SQL_INTERVAL_HOUR_TO_MINUTE") == 0)
	{
		SQLType = SQL_INTERVAL_HOUR_TO_MINUTE;
	}
	else if (_stricmp(buffer,"SQL_INTERVAL_HOUR_TO_SECOND") == 0)
	{
		SQLType = SQL_INTERVAL_HOUR_TO_SECOND;
	}
	else if (_stricmp(buffer,"SQL_INTERVAL_MINUTE_TO_SECOND") == 0)
	{
		SQLType = SQL_INTERVAL_MINUTE_TO_SECOND;
	}
	
	return SQLType;
}

/****************************************************************
** SQLNullToChar()
**
** This function will attempt to convert a null state value from an
** ODBC function call into a more user friendly character string.
** If the null state isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
char *SQLNullToChar(SWORD NullState, char *buf)
{
   switch (NullState) {
		case SQL_NO_NULLS:			strcpy (buf,"SQL_NO_NULLS");break;
		case SQL_NULLABLE:			strcpy (buf,"SQL_NULLABLE");break;
		case SQL_NULLABLE_UNKNOWN:	strcpy (buf,"SQL_NULLABLE_UNKNOWN");break;
      default:
         _itoa(NullState,buf,10);
	}
	return buf;
}

/****************************************************************
** CatalogLocationToString()
**
** This function will attempt to convert a catalog location value
** into a more user friendly character string.
** If the catalog location value isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
char *CatalogLocationToString(SWORD CatLoc, char *buf)
{
   switch (CatLoc) {
		case SQL_CL_START:			strcpy (buf,"SQL_CL_START");break;
		case SQL_CL_END:				strcpy (buf,"SQL_CL_END");break;
      default:
         _itoa(CatLoc,buf,10);
	}
	return buf;
}

/****************************************************************
** SQLDescToChar()
**
** This function will attempt to convert a column description value from an
** ODBC function call into a more user friendly character string.
** If the column description isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
char *SQLDescToChar(SWORD Desc, char *buf)
{
   switch (Desc) {
		case SQL_COLUMN_COUNT:strcpy (buf,"SQL_COLUMN_COUNT");break;
		case SQL_COLUMN_NAME:strcpy (buf,"SQL_COLUMN_NAME");break;
		case SQL_COLUMN_TYPE:strcpy (buf,"SQL_COLUMN_TYPE");break;
		case SQL_COLUMN_LENGTH:strcpy (buf,"SQL_COLUMN_LENGTH");break;
		case SQL_COLUMN_PRECISION:strcpy (buf,"SQL_COLUMN_PRECISION");break;
		case SQL_COLUMN_SCALE:strcpy (buf,"SQL_COLUMN_SCALE");break;
		case SQL_COLUMN_DISPLAY_SIZE:strcpy (buf,"SQL_COLUMN_DISPLAY_SIZE");break;
		case SQL_COLUMN_NULLABLE:strcpy (buf,"SQL_COLUMN_NULLABLE");break;
		case SQL_COLUMN_UNSIGNED:strcpy (buf,"SQL_COLUMN_UNSIGNED");break;
		case SQL_COLUMN_MONEY:strcpy (buf,"SQL_COLUMN_MONEY");break;
		case SQL_COLUMN_UPDATABLE:strcpy (buf,"SQL_COLUMN_UPDATABLE");break;
		case SQL_COLUMN_AUTO_INCREMENT:strcpy (buf,"SQL_COLUMN_AUTO_INCREMENT");break;
		case SQL_COLUMN_CASE_SENSITIVE:strcpy (buf,"SQL_COLUMN_CASE_SENSITIVE");break;
		case SQL_COLUMN_SEARCHABLE:strcpy (buf,"SQL_COLUMN_SEARCHABLE");break;
		case SQL_COLUMN_TYPE_NAME:strcpy (buf,"SQL_COLUMN_TYPE_NAME");break;
		case SQL_COLUMN_TABLE_NAME:strcpy (buf,"SQL_COLUMN_TABLE_NAME");break;
		case SQL_COLUMN_OWNER_NAME:strcpy (buf,"SQL_COLUMN_OWNER_NAME");break;
		case SQL_COLUMN_QUALIFIER_NAME:strcpy (buf,"SQL_COLUMN_QUALIFIER_NAME");break;
		case SQL_COLUMN_LABEL:strcpy (buf,"SQL_COLUMN_LABEL");break;
      default:
         _itoa(Desc,buf,10);
	}
	return buf;
}

//----------------------------------------------------------------------------
/****************************************************************
** SQLDescAttrToChar()
**
** This function will attempt to convert a column description value from an
** ODBC function call into a more user friendly character string.
** If the column description isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
char *SQLDescAttrToChar(SWORD Desc, char *buf)
{
   switch (Desc) {
		case SQL_DESC_AUTO_UNIQUE_VALUE:strcpy (buf,"SQL_DESC_AUTO_UNIQUE_VALUE");break;
		case SQL_DESC_CASE_SENSITIVE:strcpy (buf,"SQL_DESC_CASE_SENSITIVE");break;
		case SQL_DESC_COUNT:strcpy (buf,"SQL_DESC_COUNT");break;
		case SQL_DESC_DISPLAY_SIZE:strcpy (buf,"SQL_DESC_DISPLAY_SIZE");break;
		case SQL_DESC_LENGTH:strcpy (buf,"SQL_DESC_LENGTH");break;
		case SQL_DESC_FIXED_PREC_SCALE:strcpy (buf,"SQL_DESC_FIXED_PREC_SCALE");break;
		case SQL_DESC_NULLABLE:strcpy (buf,"SQL_DESC_NULLABLE");break;
		case SQL_DESC_PRECISION:strcpy (buf,"SQL_DESC_PRECISION");break;
		case SQL_DESC_SCALE:strcpy (buf,"SQL_DESC_SCALE");break;
		case SQL_DESC_SEARCHABLE:strcpy (buf,"SQL_DESC_SEARCHABLE");break;
		case SQL_DESC_TYPE:strcpy (buf,"SQL_DESC_TYPE");break;
		case SQL_DESC_CONCISE_TYPE:strcpy (buf,"SQL_DESC_CONCISE_TYPE");break;
		case SQL_DESC_UNSIGNED:strcpy (buf,"SQL_DESC_UNSIGNED");break;
		case SQL_DESC_UPDATABLE:strcpy (buf,"SQL_DESC_UPDATABLE");break;
		case SQL_DESC_NAME:strcpy (buf,"SQL_DESC_NAME");break;
		case SQL_DESC_TYPE_NAME:strcpy (buf,"SQL_DESC_TYPE_NAME");break;
		case SQL_DESC_SCHEMA_NAME:strcpy (buf,"SQL_DESC_SCHEMA_NAME");break;
		case SQL_DESC_CATALOG_NAME:strcpy (buf,"SQL_DESC_CATALOG_NAME");break;
		case SQL_DESC_TABLE_NAME:strcpy (buf,"SQL_DESC_TABLE_NAME");break;
		case SQL_DESC_LABEL:strcpy (buf,"SQL_DESC_LABEL");break;
      default:
         _itoa(Desc,buf,10);
	}
	return buf;
}

//----------------------------------------------------------------------------
char * StatementOptionToChar( long Option, char *buf )
{
	switch (Option) 
	{
		case SQL_QUERY_TIMEOUT:		sprintf(buf,"SQL_QUERY_TIMEOUT(%ld)",Option);break;
		case SQL_MAX_ROWS:			sprintf(buf,"SQL_MAX_ROWS(%ld)",Option);break;
		case SQL_NOSCAN:			sprintf(buf,"SQL_NOSCAN(%ld)",Option);break;
		case SQL_MAX_LENGTH:		sprintf(buf,"SQL_MAX_LENGTH(%ld)",Option);break;
		case SQL_ASYNC_ENABLE:		sprintf(buf,"SQL_ASYNC_ENABLE(%ld)",Option);break;
		case SQL_BIND_TYPE:			sprintf(buf,"SQL_BIND_TYPE(%ld)",Option);break;
		case SQL_CURSOR_TYPE:		sprintf(buf,"SQL_CURSOR_TYPE(%ld)",Option);break;
		case SQL_CONCURRENCY:		sprintf(buf,"SQL_CONCURRENCY(%ld)",Option);break;
		case SQL_KEYSET_SIZE:		sprintf(buf,"SQL_KEYSET_SIZE(%ld)",Option);break;
		case SQL_ROWSET_SIZE:		sprintf(buf,"SQL_ROWSET_SIZE(%ld)",Option);break;
		case SQL_SIMULATE_CURSOR:	sprintf(buf,"SQL_SIMULATE_CURSOR(%ld)",Option);break;
		case SQL_RETRIEVE_DATA:		sprintf(buf,"SQL_RETRIEVE_DATA(%ld)",Option);break;
		case SQL_USE_BOOKMARKS:		sprintf(buf,"SQL_USE_BOOKMARKS(%ld)",Option);break;
		case SQL_GET_BOOKMARK:		sprintf(buf,"SQL_GET_BOOKMARK(%ld)",Option);break;
		case SQL_ROW_NUMBER:		sprintf(buf,"SQL_ROW_NUMBER(%ld)",Option);break;
		case SQL_ATTR_CURSOR_SCROLLABLE:	sprintf(buf,"SQL_CURSOR_SCROLLABLE(%ld)",Option);break;
		case SQL_ATTR_CURSOR_SENSITIVITY:	sprintf(buf,"SQL_CURSOR_SENSITIVITY(%ld)",Option);break;
		case SQL_ATTR_ENABLE_AUTO_IPD:	sprintf(buf,"SQL_ROW_ARRAY_SIZE(%ld)",Option);break;
		case SQL_ATTR_ROW_ARRAY_SIZE:	sprintf(buf,"SQL_ENABLE_AUTO_IPD(%ld)",Option);break;
		case SQL_ATTR_METADATA_ID:		sprintf(buf,"SQL_METADATA_ID(%ld)",Option);break;
		default:
            sprintf(buf,"%ld",Option);
			break;
	}
	return buf;
}

//****************************************************************************
char *StatementParamToChar( long Option, long Param, char *buf )
{
	switch (Option) 
	{
		case SQL_QUERY_TIMEOUT:		
			sprintf(buf,"%ld seconds",Param);
			break;

		case SQL_NOSCAN:
			switch (Param)
			{
			case SQL_NOSCAN_OFF:		sprintf(buf,"SQL_NOSCAN_OFF(%ld)",Param);break;
			case SQL_NOSCAN_ON:			sprintf(buf,"SQL_NOSCAN_ON(%ld)",Param);break;
			}
			break;

		case SQL_ASYNC_ENABLE:
			switch (Param)
			{
			case SQL_ASYNC_ENABLE_OFF:		sprintf(buf,"SQL_ASYNC_ENABLE_OFF(%ld)",Param);break;
			case SQL_ASYNC_ENABLE_ON:		sprintf(buf,"SQL_ASYNC_ENABLE_ON(%ld)",Param);break;
			}
			break;

		case SQL_BIND_TYPE:
			if( Param == SQL_BIND_BY_COLUMN) sprintf(buf,"SQL_BIND_BY_COLUMN(%ld)",Param);
			break;

		case SQL_CURSOR_TYPE:
			switch (Param)
			{
			case SQL_CURSOR_FORWARD_ONLY:	sprintf(buf,"SQL_CURSOR_FORWARD_ONLY(%ld)",Param);break;
			case SQL_CURSOR_KEYSET_DRIVEN:	sprintf(buf,"SQL_CURSOR_KEYSET_DRIVEN(%ld)",Param);break;
			case SQL_CURSOR_DYNAMIC:		sprintf(buf,"SQL_CURSOR_DYNAMIC(%ld)",Param);break;
			case SQL_CURSOR_STATIC:			sprintf(buf,"SQL_CURSOR_STATIC(%ld)",Param);break;
			}
			break;

		case SQL_CONCURRENCY:
			switch (Param)
			{
			case SQL_CONCUR_READ_ONLY:		sprintf(buf,"SQL_CONCUR_READ_ONLY(%ld)",Param);break;
			case SQL_CONCUR_LOCK:			sprintf(buf,"SQL_CONCUR_LOCK(%ld)",Param);break;
			case SQL_CONCUR_ROWVER:			sprintf(buf,"SQL_CONCUR_ROWVER(%ld)",Param);break;
			case SQL_CONCUR_VALUES:			sprintf(buf,"SQL_CONCUR_VALUES(%ld)",Param);break;
			}
			break;

		case SQL_SIMULATE_CURSOR:
			switch (Param)
			{
			case SQL_SC_NON_UNIQUE:			sprintf(buf,"SQL_SC_NON_UNIQUE(%ld)",Param);break;
			case SQL_SC_TRY_UNIQUE:			sprintf(buf,"SQL_SC_TRY_UNIQUE(%ld)",Param);break;
			case SQL_SC_UNIQUE:				sprintf(buf,"SQL_SC_UNIQUE(%ld)",Param);break;
			}
			break;

		case SQL_RETRIEVE_DATA:
			switch (Param)
			{
			case SQL_RD_OFF:				sprintf(buf,"SQL_RD_OFF(%ld)",Param);break;
			case SQL_RD_ON:					sprintf(buf,"SQL_RD_ON(%ld)",Param);break;
			}
			break;

		case SQL_USE_BOOKMARKS:
			switch (Param)
			{
			case SQL_UB_OFF:				sprintf(buf,"SQL_UB_OFF(%ld)",Param);break;
			case SQL_UB_ON:					sprintf(buf,"SQL_UB_ON(%ld)",Param);break;
			}
			break;

		case SQL_ATTR_CURSOR_SENSITIVITY:
			switch (Param)
			{
			case SQL_INSENSITIVE:			sprintf(buf,"SQL_INSENSITIVE(%ld)",Param);break;
			case SQL_SENSITIVE:				sprintf(buf,"SQL_SENSITIVE(%ld)",Param);break;
			case SQL_UNSPECIFIED:			sprintf(buf,"SQL_UNSPECIFIED(%ld)",Param);break;
			}
			break;

		case SQL_ATTR_ENABLE_AUTO_IPD:
		case SQL_ATTR_METADATA_ID:
			switch (Param)
			{
			case SQL_FALSE:					sprintf(buf,"SQL_FALSE(%ld)",Param);break;
			case SQL_TRUE:					sprintf(buf,"SQL_TRUE(%ld)",Param);break;
			}
			break;

		case SQL_GET_BOOKMARK:
		case SQL_ROW_NUMBER:
		case SQL_MAX_ROWS:
		case SQL_MAX_LENGTH:
		case SQL_KEYSET_SIZE:
		case SQL_ROWSET_SIZE:
			sprintf(buf,"%ld",Param);
			break;

		default:
			sprintf(buf,"%ld",Param);
            break;
	}
	return buf;
}

//----------------------------------------------------------------------------
char * ConnectionOptionToChar( long Option, char *buf )
{
	switch (Option) 
	{
		case SQL_ACCESS_MODE:				sprintf(buf,"SQL_ACCESS_MODE(%ld)",Option);break;
		case SQL_AUTOCOMMIT:				sprintf(buf,"SQL_AUTOCOMMIT(%ld)",Option);break;
		case SQL_LOGIN_TIMEOUT:				sprintf(buf,"SQL_LOGIN_TIMEOUT(%ld)",Option);break;
		case SQL_OPT_TRACE:					sprintf(buf,"SQL_OPT_TRACE(%ld)",Option);break;
		case SQL_TRANSLATE_OPTION:			sprintf(buf,"SQL_TRANSLATE_OPTION(%ld)",Option);break;
		case SQL_TXN_ISOLATION:				sprintf(buf,"SQL_TXN_ISOLATION(%ld)",Option);break;
		case SQL_ODBC_CURSORS:				sprintf(buf,"SQL_ODBC_CURSORS(%ld)",Option);break;
		case SQL_PACKET_SIZE:				sprintf(buf,"SQL_PACKET_SIZE(%ld)",Option);break;

		case SQL_ATTR_ODBC_VERSION:			sprintf(buf,"SQL_ATTR_ODBC_VERSION(%ld)",Option);break;
		case SQL_ATTR_CONNECTION_POOLING:	sprintf(buf,"SQL_ATTR_CONNECTION_POOLING(%ld)",Option);break;
		case SQL_ATTR_CP_MATCH:				sprintf(buf,"SQL_ATTR_CP_MATCH(%ld)",Option);break;
		case SQL_ATTR_OUTPUT_NTS:			sprintf(buf,"SQL_ATTR_OUTPUT_NTS(%ld)",Option);break;
		default:
            sprintf(buf,"Unknown SQL option: %ld", Option);
			//_ltoa(Option,buf,10);
	}
	return buf;
}

//****************************************************************************
char *ConnectionParamToChar( long Option, long Param, char *buf )
{
	switch (Option) 
	{
		case SQL_ACCESS_MODE:			
			switch (Param)
			{
				case SQL_MODE_READ_WRITE:	sprintf(buf,"SQL_MODE_READ_WRITE%ld seconds",Param);break;
				case SQL_MODE_READ_ONLY:	sprintf(buf,"SQL_MODE_READ_ONLY%ld seconds",Param);break;
			}
			break;

		case SQL_AUTOCOMMIT:
			switch (Param)
			{
				case SQL_AUTOCOMMIT_OFF:			sprintf(buf,"SQL_AUTOCOMMIT_OFF(%ld)",Param);break;
				case SQL_AUTOCOMMIT_ON:				sprintf(buf,"SQL_AUTOCOMMIT_ON(%ld)",Param);break;
			}
			break;

		case SQL_LOGIN_TIMEOUT:
			sprintf(buf,"%ld seconds",Param);
			break;

		case SQL_OPT_TRACE:
			switch (Param)
			{
				case SQL_OPT_TRACE_OFF:				sprintf(buf,"SQL_OPT_TRACE_OFF(%ld)",Param);break;
				case SQL_OPT_TRACE_ON:				sprintf(buf,"SQL_OPT_TRACE_ON(%ld)",Param);break;
			}
			break;

		case SQL_TRANSLATE_OPTION:
			sprintf(buf,"%ld seconds",Param);
			break;

		case SQL_TXN_ISOLATION:
			switch (Param)
			{
				case SQL_TXN_READ_UNCOMMITTED:	sprintf(buf,"SQL_TXN_READ_UNCOMMITTED(%ld)",Param);break;
				case SQL_TXN_READ_COMMITTED:		sprintf(buf,"SQL_TXN_READ_COMMITTED(%ld)",Param);break;
				case SQL_TXN_REPEATABLE_READ:		sprintf(buf,"SQL_TXN_REPEATABLE_READ(%ld)",Param);break;
				case SQL_TXN_SERIALIZABLE:			sprintf(buf,"SQL_TXN_SERIALIZABLE(%ld)",Param);break;
			}
			break;

		case SQL_ODBC_CURSORS:
			switch (Param)
			{
			case SQL_CUR_USE_IF_NEEDED:			sprintf(buf,"SQL_CUR_USE_IF_NEEDED(%ld)",Param);break;
			case SQL_CUR_USE_ODBC:					sprintf(buf,"SQL_CUR_USE_ODBC(%ld)",Param);break;
			case SQL_CUR_USE_DRIVER:				sprintf(buf,"SQL_CUR_USE_DRIVER(%ld)",Param);break;
			}
			break;

		case SQL_PACKET_SIZE:
			sprintf(buf,"%ld seconds",Param);
			break;

		case SQL_GET_BOOKMARK:
            sprintf(buf,"SQL_GET_BOOKMARK(%ld)",Param);break;
		case SQL_ROW_NUMBER:
            sprintf(buf,"SQL_ROW_NUMBER(%ld)",Param);break;
		case SQL_MAX_ROWS:
            sprintf(buf,"SQL_MAX_ROWS(%ld)",Param);break;
		case SQL_MAX_LENGTH:
            sprintf(buf,"SQL_MAX_LENGTH(%ld)",Param);break;
		case SQL_KEYSET_SIZE:
            sprintf(buf,"SQL_KEYSET_SIZE(%ld)",Param);break;
		case SQL_ROWSET_SIZE:
            sprintf(buf,"SQL_ROWSET_SIZE(%ld)",Param);break;
			//_ltoa(Param,buf,10);

		default:
            sprintf(buf,"Unknown SQL Parameter(%ld)",Param);break;
			//_ltoa(Param,buf,10);
	}
	return buf;
}

/****************************************************************
** SQLCTypeToChar()
**
** This function will attempt to convert a SQLType value from an
** ODBC function call into a more user friendly character string.
** If the CType isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
char *SQLCTypeToChar(SWORD CType, char *buf)
{
   switch (CType) {
      case SQL_C_CHAR:			sprintf (buf,"SQL_C_CHAR(%d)",CType);break;
	  case SQL_C_LONG:			sprintf (buf,"SQL_C_LONG(%d)",CType);break;
      case SQL_C_SHORT:			sprintf (buf,"SQL_C_SHORT(%d)",CType);break;
      case SQL_C_FLOAT:			sprintf (buf,"SQL_C_FLOAT(%d)",CType);break;
      case SQL_C_DOUBLE:		sprintf (buf,"SQL_C_DOUBLE(%d)",CType);break;
      case SQL_C_NUMERIC:		sprintf (buf,"SQL_C_NUMERIC(%d)",CType);break;
      case SQL_C_DEFAULT:		sprintf (buf,"SQL_C_DEFAULT(%d)",CType);break;
      case SQL_C_DATE:			sprintf (buf,"SQL_C_DATE(%d)",CType);break;
      case SQL_C_TIME:			sprintf (buf,"SQL_C_TIME(%d)",CType);break;
      case SQL_C_TIMESTAMP:			sprintf (buf,"SQL_C_TIMESTAMP(%d)",CType);break;
      case SQL_C_TYPE_DATE:			sprintf (buf,"SQL_C_TYPE_DATE(%d)",CType);break;
      case SQL_C_TYPE_TIME:			sprintf (buf,"SQL_C_TYPE_TIME(%d)",CType);break;
      case SQL_C_TYPE_TIMESTAMP:		sprintf (buf,"SQL_C_TYPE_TIMESTAMP(%d)",CType);break;
      case SQL_C_INTERVAL_YEAR:		sprintf (buf,"SQL_C_INTERVAL_YEAR(%d)",CType);break;
      case SQL_C_INTERVAL_MONTH:		sprintf (buf,"SQL_C_INTERVAL_MONTH(%d)",CType);break;
      case SQL_C_INTERVAL_DAY:		sprintf (buf,"SQL_C_INTERVAL_DAY(%d)",CType);break;
      case SQL_C_INTERVAL_HOUR:		sprintf (buf,"SQL_C_INTERVAL_HOUR(%d)",CType);break;
      case SQL_C_INTERVAL_MINUTE:	sprintf (buf,"SQL_C_INTERVAL_MINUTE(%d)",CType);break;
      case SQL_C_INTERVAL_SECOND:	sprintf (buf,"SQL_C_INTERVAL_SECOND(%d)",CType);break;
      case SQL_C_INTERVAL_YEAR_TO_MONTH:		sprintf (buf,"SQL_C_INTERVAL_YEAR_TO_MONTH(%d)",CType);break;
      case SQL_C_INTERVAL_DAY_TO_HOUR:			sprintf (buf,"SQL_C_INTERVAL_DAY_TO_HOUR(%d)",CType);break;
      case SQL_C_INTERVAL_DAY_TO_MINUTE:		sprintf (buf,"SQL_C_INTERVAL_DAY_TO_MINUTE(%d)",CType);break;
      case SQL_C_INTERVAL_DAY_TO_SECOND:		sprintf (buf,"SQL_C_INTERVAL_DAY_TO_SECOND(%d)",CType);break;
      case SQL_C_INTERVAL_HOUR_TO_MINUTE:		sprintf (buf,"SQL_C_INTERVAL_HOUR_TO_MINUTE(%d)",CType);break;
      case SQL_C_INTERVAL_HOUR_TO_SECOND:		sprintf (buf,"SQL_C_INTERVAL_HOUR_TO_SECOND(%d)",CType);break;
      case SQL_C_INTERVAL_MINUTE_TO_SECOND:	sprintf (buf,"SQL_C_INTERVAL_MINUTE_TO_SECOND(%d)",CType);break;
      case SQL_C_BINARY:		sprintf (buf,"SQL_C_BINARY(%d)",CType);break;
      case SQL_C_BIT:			sprintf (buf,"SQL_C_BIT(%d)",CType);break;
      case SQL_C_SBIGINT:		sprintf (buf,"SQL_C_SBIGINT(%d)",CType);break;
      case SQL_C_UBIGINT:		sprintf (buf,"SQL_C_UBIGINT(%d)",CType);break;
      case SQL_C_TINYINT:		sprintf (buf,"SQL_C_TINYINT(%d)",CType);break;
      case SQL_C_SLONG:			sprintf (buf,"SQL_C_SLONG(%d)",CType);break;
      case SQL_C_SSHORT:		sprintf (buf,"SQL_C_SSHORT(%d)",CType);break;
      case SQL_C_STINYINT:		sprintf (buf,"SQL_C_STINYINT(%d)",CType);break;
      case SQL_C_ULONG:			sprintf (buf,"SQL_C_ULONG(%d)",CType);break;
      case SQL_C_USHORT:		sprintf (buf,"SQL_C_USHORT(%d)",CType);break;
      case SQL_C_UTINYINT:		sprintf (buf,"SQL_C_UTINYINT(%d)",CType);break;
      case SQL_C_WCHAR:			sprintf (buf,"SQL_C_WCHAR(%d)",CType);break;
      default:
         _itoa(CType,buf,10);
	}
	return buf;
}


/****************************************************************
** CharToSQLCType()
**
** This function will attempt to convert a SQLType value from an
** ODBC function call into a more user friendly character string.
** If the CType isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
SWORD	CharToSQLCType(char *buffer)
{
	SWORD	SQLCType = 999;
	
	if (_stricmp(buffer,"SQL_C_CHAR") == 0)
	{
		SQLCType = SQL_C_CHAR;
	}
	else if (_stricmp(buffer,"SQL_C_LONG") == 0)
	{
		SQLCType = SQL_C_LONG;
	}
	else if (_stricmp(buffer,"SQL_C_SHORT") == 0)
	{
		SQLCType = SQL_C_SHORT;
	}
	else if (_stricmp(buffer,"SQL_C_FLOAT") == 0)
	{
		SQLCType = SQL_C_FLOAT;
	}
	else if (_stricmp(buffer,"SQL_C_DOUBLE") == 0)
	{
		SQLCType = SQL_C_DOUBLE;
	}
	else if (_stricmp(buffer,"SQL_C_NUMERIC") == 0)
	{
		SQLCType = SQL_C_NUMERIC;
	}
	else if (_stricmp(buffer,"SQL_C_DEFAULT") == 0)
	{
		SQLCType = SQL_C_DEFAULT;
	}
	else if (_stricmp(buffer,"SQL_C_DATE") == 0)
	{
		SQLCType = SQL_C_DATE;
	}
	else if (_stricmp(buffer,"SQL_C_TIME") == 0)
	{
		SQLCType = SQL_C_TIME;
	}
	else if (_stricmp(buffer,"SQL_C_TIMESTAMP") == 0)
	{
		SQLCType = SQL_C_TIMESTAMP;
	}
	else if (_stricmp(buffer,"SQL_C_TYPE_DATE") == 0)
	{
		SQLCType = SQL_C_TYPE_DATE;
	}
	else if (_stricmp(buffer,"SQL_C_TYPE_TIME") == 0)
	{
		SQLCType = SQL_C_TYPE_TIME;
	}
	else if (_stricmp(buffer,"SQL_C_TYPE_TIMESTAMP") == 0)
	{
		SQLCType = SQL_C_TYPE_TIMESTAMP;
	}
	else if (_stricmp(buffer,"SQL_C_INTERVAL_YEAR") == 0)
	{
		SQLCType = SQL_C_INTERVAL_YEAR;
	}
	else if (_stricmp(buffer,"SQL_C_INTERVAL_MONTH") == 0)
	{
		SQLCType = SQL_C_INTERVAL_MONTH;
	}
	else if (_stricmp(buffer,"SQL_C_INTERVAL_DAY") == 0)
	{
		SQLCType = SQL_C_INTERVAL_DAY;
	}
	else if (_stricmp(buffer,"SQL_C_INTERVAL_HOUR") == 0)
	{
		SQLCType = SQL_C_INTERVAL_HOUR;
	}
	else if (_stricmp(buffer,"SQL_C_INTERVAL_MINUTE") == 0)
	{
		SQLCType = SQL_C_INTERVAL_MINUTE;
	}
	else if (_stricmp(buffer,"SQL_C_INTERVAL_SECOND") == 0)
	{
		SQLCType = SQL_C_INTERVAL_SECOND;
	}
	else if (_stricmp(buffer,"SQL_C_INTERVAL_YEAR_TO_MONTH") == 0)
	{
		SQLCType = SQL_C_INTERVAL_YEAR_TO_MONTH;
	}
	else if (_stricmp(buffer,"SQL_C_INTERVAL_DAY_TO_HOUR") == 0)
	{
		SQLCType = SQL_C_INTERVAL_DAY_TO_HOUR;
	}
	else if (_stricmp(buffer,"SQL_C_INTERVAL_DAY_TO_MINUTE") == 0)
	{
		SQLCType = SQL_C_INTERVAL_DAY_TO_MINUTE;
	}
	else if (_stricmp(buffer,"SQL_C_INTERVAL_DAY_TO_SECOND") == 0)
	{
		SQLCType = SQL_C_INTERVAL_DAY_TO_SECOND;
	}
	else if (_stricmp(buffer,"SQL_C_INTERVAL_HOUR_TO_MINUTE") == 0)
	{
		SQLCType = SQL_C_INTERVAL_HOUR_TO_MINUTE;
	}
	else if (_stricmp(buffer,"SQL_C_INTERVAL_HOUR_TO_SECOND") == 0)
	{
		SQLCType = SQL_C_INTERVAL_HOUR_TO_SECOND;
	}
	else if (_stricmp(buffer,"SQL_C_INTERVAL_MINUTE_TO_SECOND") == 0)
	{
		SQLCType = SQL_C_INTERVAL_MINUTE_TO_SECOND;
	}
	else if (_stricmp(buffer,"SQL_C_BINARY") == 0)
	{
		SQLCType = SQL_C_BINARY;
	}
	else if (_stricmp(buffer,"SQL_C_BIT") == 0)
	{
		SQLCType = SQL_C_BIT;
	}
	else if (_stricmp(buffer,"SQL_C_SBIGINT") == 0)
	{
		SQLCType = SQL_C_SBIGINT;
	}
	else if (_stricmp(buffer,"SQL_C_UBIGINT") == 0)
	{
		SQLCType = SQL_C_UBIGINT;
	}
	else if (_stricmp(buffer,"SQL_C_TINYINT") == 0)
	{
		SQLCType = SQL_C_TINYINT;
	}
	else if (_stricmp(buffer,"SQL_C_SLONG") == 0)
	{
		SQLCType = SQL_C_SLONG;
	}
	else if (_stricmp(buffer,"SQL_C_SSHORT") == 0)
	{
		SQLCType = SQL_C_SSHORT;
	}
	else if (_stricmp(buffer,"SQL_C_STINYINT") == 0)
	{
		SQLCType = SQL_C_STINYINT;
	}
	else if (_stricmp(buffer,"SQL_C_ULONG") == 0)
	{
		SQLCType = SQL_C_LONG;
	}
	else if (_stricmp(buffer,"SQL_C_USHORT") == 0)
	{
		SQLCType = SQL_C_USHORT;
	}
	else if (_stricmp(buffer,"SQL_C_UTINYINT") == 0)
	{
		SQLCType = SQL_C_UTINYINT;
	}
	return SQLCType;
}


/****************************************************************
** InfoTypeToChar()
**
** This function will attempt to convert a SQLGetInfoType value
** into a more user friendly character string.
** If the SQLGetInfoType isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
char *InfoTypeToChar( long InfoType, char *buf )
{
	switch( InfoType )
	{
	case SQL_ACTIVE_CONNECTIONS:		sprintf(buf,"SQL_ACTIVE_CONNECTIONS(%ld)",InfoType);break;
	case SQL_ACTIVE_STATEMENTS:         sprintf(buf,"SQL_ACTIVE_STATEMENTS(%ld)",InfoType);break;
	case SQL_ASYNC_MODE:				sprintf(buf,"SQL_ASYNC_MODE(%ld)",InfoType);break;
	case SQL_CATALOG_NAME:		        sprintf(buf,"SQL_CATALOG_NAME(%ld)",InfoType);break;
	case SQL_CATALOG_NAME_SEPARATOR:	sprintf(buf,"SQL_CATALOG_NAME_SEPARATOR(%ld)",InfoType);break;
	case SQL_CATALOG_TERM:				sprintf(buf,"SQL_CATALOG_TERM(%ld)",InfoType);break;
	case SQL_COLLATION_SEQ:             sprintf(buf,"SQL_COLLATION_SEQ(%ld)",InfoType);break;
	case SQL_CURSOR_SENSITIVITY:        sprintf(buf,"SQL_CURSOR_SENSITIVITY(%ld)",InfoType);break;
	case SQL_DATA_SOURCE_NAME:          sprintf(buf,"SQL_DATA_SOURCE_NAME(%ld)",InfoType);break;
	case SQL_DESCRIBE_PARAMETER:		sprintf(buf,"SQL_DESCRIBE_PARAMETER(%ld)",InfoType);break;
	case SQL_DM_VER:				    sprintf(buf,"SQL_DM_VER(%ld)",InfoType);break;
	case SQL_DRIVER_HDBC:				sprintf(buf,"SQL_DRIVER_HDBC(%ld)",InfoType);break;
	case SQL_DRIVER_HENV:				sprintf(buf,"SQL_DRIVER_HENV(%ld)",InfoType);break;
	case SQL_DRIVER_HLIB:				sprintf(buf,"SQL_DRIVER_HLIB(%ld)",InfoType);break;
	case SQL_DRIVER_HSTMT:				sprintf(buf,"SQL_DRIVER_HSTMT(%ld)",InfoType);break;
	case SQL_DRIVER_NAME:               sprintf(buf,"SQL_DRIVER_NAME(%ld)",InfoType);break;
	case SQL_DRIVER_VER:                sprintf(buf,"SQL_DRIVER_VER(%ld)",InfoType);break;
	case SQL_DYNAMIC_CURSOR_ATTRIBUTES1:sprintf(buf,"SQL_DYNAMIC_CURSOR_ATTRIBUTES1(%ld)",InfoType);break;
	case SQL_DYNAMIC_CURSOR_ATTRIBUTES2:sprintf(buf,"SQL_DYNAMIC_CURSOR_ATTRIBUTES2(%ld)",InfoType);break;
	case SQL_FETCH_DIRECTION:           sprintf(buf,"SQL_FETCH_DIRECTION(%ld)",InfoType);break;
	case SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES1:sprintf(buf,"SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES1(%ld)",InfoType);break;
	case SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES2:sprintf(buf,"SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES2(%ld)",InfoType);break;
	case SQL_KEYSET_CURSOR_ATTRIBUTES1: sprintf(buf,"SQL_KEYSET_CURSOR_ATTRIBUTES1(%ld)",InfoType);break;
	case SQL_KEYSET_CURSOR_ATTRIBUTES2:	sprintf(buf,"SQL_KEYSET_CURSOR_ATTRIBUTES2(%ld)",InfoType);break;
	case SQL_ODBC_API_CONFORMANCE:      sprintf(buf,"SQL_ODBC_API_CONFORMANCE(%ld)",InfoType);break;
	case SQL_ODBC_VER:                  sprintf(buf,"SQL_ODBC_VER(%ld)",InfoType);break;
	case SQL_ROW_UPDATES:               sprintf(buf,"SQL_ROW_UPDATES(%ld)",InfoType);break;
	case SQL_ODBC_SAG_CLI_CONFORMANCE:  sprintf(buf,"SQL_ODBC_SAG_CLI_CONFORMANCE(%ld)",InfoType);break;
	case SQL_SERVER_NAME:               sprintf(buf,"SQL_SERVER_NAME(%ld)",InfoType);break;
	case SQL_SEARCH_PATTERN_ESCAPE:     sprintf(buf,"SQL_SEARCH_PATTERN_ESCAPE(%ld)",InfoType);break;
	case SQL_ODBC_SQL_CONFORMANCE:      sprintf(buf,"SQL_ODBC_SQL_CONFORMANCE(%ld)",InfoType);break;
	case SQL_DBMS_NAME:                 sprintf(buf,"SQL_DBMS_NAME(%ld)",InfoType);break;
	case SQL_DBMS_VER:                  sprintf(buf,"SQL_DBMS_VER(%ld)",InfoType);break;
	case SQL_ACCESSIBLE_TABLES:         sprintf(buf,"SQL_ACCESSIBLE_TABLES(%ld)",InfoType);break;
	case SQL_ACCESSIBLE_PROCEDURES:     sprintf(buf,"SQL_ACCESSIBLE_PROCEDURES(%ld)",InfoType);break;
	case SQL_PROCEDURES:                sprintf(buf,"SQL_PROCEDURES(%ld)",InfoType);break;
	case SQL_CONCAT_NULL_BEHAVIOR:      sprintf(buf,"SQL_CONCAT_NULL_BEHAVIOR(%ld)",InfoType);break;
	case SQL_CURSOR_COMMIT_BEHAVIOR:    sprintf(buf,"SQL_CURSOR_COMMIT_BEHAVIOR(%ld)",InfoType);break;
	case SQL_CURSOR_ROLLBACK_BEHAVIOR:  sprintf(buf,"SQL_CURSOR_ROLLBACK_BEHAVIOR(%ld)",InfoType);break;
	case SQL_DATA_SOURCE_READ_ONLY:     sprintf(buf,"SQL_DATA_SOURCE_READ_ONLY(%ld)",InfoType);break;
	case SQL_DATABASE_NAME:				sprintf(buf,"SQL_DATABASE_NAME(%ld)",InfoType);break;
	case SQL_DEFAULT_TXN_ISOLATION:     sprintf(buf,"SQL_DEFAULT_TXN_ISOLATION(%ld)",InfoType);break;
	case SQL_EXPRESSIONS_IN_ORDERBY:    sprintf(buf,"SQL_EXPRESSIONS_IN_ORDERBY(%ld)",InfoType);break;
	case SQL_IDENTIFIER_CASE:           sprintf(buf,"SQL_IDENTIFIER_CASE(%ld)",InfoType);break;
	case SQL_IDENTIFIER_QUOTE_CHAR:     sprintf(buf,"SQL_IDENTIFIER_QUOTE_CHAR(%ld)",InfoType);break;
	case SQL_MAX_ASYNC_CONCURRENT_STATEMENTS:sprintf(buf,"SQL_MAX_ASYNC_CONCURRENT_STATEMENTS(%ld)",InfoType);break;
	case SQL_MAX_COLUMN_NAME_LEN:       sprintf(buf,"SQL_MAX_COLUMN_NAME_LEN(%ld)",InfoType);break;
	case SQL_MAX_CURSOR_NAME_LEN:       sprintf(buf,"SQL_MAX_CURSOR_NAME_LEN(%ld)",InfoType);break;
	case SQL_MAX_IDENTIFIER_LEN:        sprintf(buf,"SQL_MAX_IDENTIFIER_LEN(%ld)",InfoType);break;
	case SQL_MAX_SCHEMA_NAME_LEN:       sprintf(buf,"SQL_MAX_SCHEMA_NAME_LEN(%ld)",InfoType);break;
	case SQL_MAX_PROCEDURE_NAME_LEN:    sprintf(buf,"SQL_MAX_PROCEDURE_NAME_LEN(%ld)",InfoType);break;
	case SQL_MAX_CATALOG_NAME_LEN:		sprintf(buf,"SQL_MAX_CATALOG_NAME_LEN(%ld)",InfoType);break;
	case SQL_MAX_TABLE_NAME_LEN:        sprintf(buf,"SQL_MAX_TABLE_NAME_LEN(%ld)",InfoType);break;
	case SQL_MULT_RESULT_SETS:          sprintf(buf,"SQL_MULT_RESULT_SETS(%ld)",InfoType);break;
	case SQL_MULTIPLE_ACTIVE_TXN:       sprintf(buf,"SQL_MULTIPLE_ACTIVE_TXN(%ld)",InfoType);break;
	case SQL_OUTER_JOINS:               sprintf(buf,"SQL_OUTER_JOINS(%ld)",InfoType);break;
	case SQL_SCHEMA_TERM:               sprintf(buf,"SQL_SCHEMA_TERM(%ld)",InfoType);break;
	case SQL_PROCEDURE_TERM:            sprintf(buf,"SQL_PROCEDURE_TERM(%ld)",InfoType);break;
	case SQL_SCROLL_CONCURRENCY:        sprintf(buf,"SQL_SCROLL_CONCURRENCY(%ld)",InfoType);break;
	case SQL_SCROLL_OPTIONS:            sprintf(buf,"SQL_SCROLL_OPTIONS(%ld)",InfoType);break;
	case SQL_STATIC_CURSOR_ATTRIBUTES1: sprintf(buf,"SQL_STATIC_CURSOR_ATTRIBUTES1(%ld)",InfoType);break;
	case SQL_STATIC_CURSOR_ATTRIBUTES2: sprintf(buf,"SQL_STATIC_CURSOR_ATTRIBUTES2(%ld)",InfoType);break;
	case SQL_TABLE_TERM:                sprintf(buf,"SQL_TABLE_TERM(%ld)",InfoType);break;
	case SQL_TXN_CAPABLE:               sprintf(buf,"SQL_TXN_CAPABLE(%ld)",InfoType);break;
	case SQL_USER_NAME:                 sprintf(buf,"SQL_USER_NAME(%ld)",InfoType);break;
	case SQL_CONVERT_FUNCTIONS:         sprintf(buf,"SQL_CONVERT_FUNCTIONS(%ld)",InfoType);break;
	case SQL_NUMERIC_FUNCTIONS:         sprintf(buf,"SQL_NUMERIC_FUNCTIONS(%ld)",InfoType);break;
	case SQL_STRING_FUNCTIONS:          sprintf(buf,"SQL_STRING_FUNCTIONS(%ld)",InfoType);break;
	case SQL_SYSTEM_FUNCTIONS:          sprintf(buf,"SQL_SYSTEM_FUNCTIONS(%ld)",InfoType);break;
	case SQL_TIMEDATE_FUNCTIONS:        sprintf(buf,"SQL_TIMEDATE_FUNCTIONS(%ld)",InfoType);break;
	case SQL_CONVERT_BIGINT:            sprintf(buf,"SQL_CONVERT_BIGINT(%ld)",InfoType);break;
	case SQL_CONVERT_BIT:               sprintf(buf,"SQL_CONVERT_BIT(%ld)",InfoType);break;
	case SQL_CONVERT_CHAR:              sprintf(buf,"SQL_CONVERT_CHAR(%ld)",InfoType);break;
	case SQL_CONVERT_DATE:              sprintf(buf,"SQL_CONVERT_DATE(%ld)",InfoType);break;
	case SQL_CONVERT_DECIMAL:           sprintf(buf,"SQL_CONVERT_DECIMAL(%ld)",InfoType);break;
	case SQL_CONVERT_DOUBLE:            sprintf(buf,"SQL_CONVERT_DOUBLE(%ld)",InfoType);break;
	case SQL_CONVERT_FLOAT:             sprintf(buf,"SQL_CONVERT_FLOAT(%ld)",InfoType);break;
	case SQL_CONVERT_INTEGER:           sprintf(buf,"SQL_CONVERT_INTEGER(%ld)",InfoType);break;
	case SQL_CONVERT_INTERVAL_DAY_TIME: sprintf(buf,"SQL_CONVERT_INTERVAL_DAY_TIME(%ld)",InfoType);break;
	case SQL_CONVERT_INTERVAL_YEAR_MONTH:sprintf(buf,"SQL_CONVERT_INTERVAL_YEAR_MONTH(%ld)",InfoType);break;
	case SQL_CONVERT_LONGVARCHAR:       sprintf(buf,"SQL_CONVERT_LONGVARCHAR(%ld)",InfoType);break;
	case SQL_CONVERT_NUMERIC:           sprintf(buf,"SQL_CONVERT_NUMERIC(%ld)",InfoType);break;
	case SQL_CONVERT_REAL:              sprintf(buf,"SQL_CONVERT_REAL(%ld)",InfoType);break;
	case SQL_CONVERT_SMALLINT:          sprintf(buf,"SQL_CONVERT_SMALLINT(%ld)",InfoType);break;
	case SQL_CONVERT_TIME:              sprintf(buf,"SQL_CONVERT_TIME(%ld)",InfoType);break;
	case SQL_CONVERT_TIMESTAMP:         sprintf(buf,"SQL_CONVERT_TIMESTAMP(%ld)",InfoType);break;
	case SQL_CONVERT_TINYINT:           sprintf(buf,"SQL_CONVERT_TINYINT(%ld)",InfoType);break;
	case SQL_CONVERT_VARCHAR:           sprintf(buf,"SQL_CONVERT_VARCHAR(%ld)",InfoType);break;
	case SQL_CONVERT_BINARY:            sprintf(buf,"SQL_CONVERT_BINARY(%ld)",InfoType);break;
	case SQL_CONVERT_VARBINARY:         sprintf(buf,"SQL_CONVERT_VARBINARY(%ld)",InfoType);break;
	case SQL_CONVERT_LONGVARBINARY:     sprintf(buf,"SQL_CONVERT_LONGVARBINARY(%ld)",InfoType);break;
	case SQL_CONVERT_WCHAR:             sprintf(buf,"SQL_CONVERT_WCHAR(%ld)",InfoType);break;
	case SQL_CONVERT_WLONGVARCHAR:      sprintf(buf,"SQL_CONVERT_WLONGVARCHAR(%ld)",InfoType);break;
	case SQL_CONVERT_WVARCHAR:          sprintf(buf,"SQL_CONVERT_WVARCHAR(%ld)",InfoType);break;
	case SQL_TXN_ISOLATION_OPTION:      sprintf(buf,"SQL_TXN_ISOLATION_OPTION(%ld)",InfoType);break;
	case SQL_ODBC_SQL_OPT_IEF:          sprintf(buf,"SQL_ODBC_SQL_OPT_IEF(%ld)",InfoType);break;
	case SQL_CORRELATION_NAME:          sprintf(buf,"SQL_CORRELATION_NAME(%ld)",InfoType);break;
	case SQL_NON_NULLABLE_COLUMNS:      sprintf(buf,"SQL_NON_NULLABLE_COLUMNS(%ld)",InfoType);break;
	case SQL_DRIVER_ODBC_VER:           sprintf(buf,"SQL_DRIVER_ODBC_VER(%ld)",InfoType);break;
	case SQL_LOCK_TYPES:                sprintf(buf,"SQL_LOCK_TYPES(%ld)",InfoType);break;
	case SQL_POS_OPERATIONS:            sprintf(buf,"SQL_POS_OPERATIONS(%ld)",InfoType);break;
	case SQL_POSITIONED_STATEMENTS:     sprintf(buf,"SQL_POSITIONED_STATEMENTS(%ld)",InfoType);break;
	case SQL_GETDATA_EXTENSIONS:        sprintf(buf,"SQL_GETDATA_EXTENSIONS(%ld)",InfoType);break;
	case SQL_BOOKMARK_PERSISTENCE:      sprintf(buf,"SQL_BOOKMARK_PERSISTENCE(%ld)",InfoType);break;
	case SQL_STATIC_SENSITIVITY:        sprintf(buf,"SQL_STATIC_SENSITIVITY(%ld)",InfoType);break;
	case SQL_FILE_USAGE:                sprintf(buf,"SQL_FILE_USAGE(%ld)",InfoType);break;
	case SQL_NULL_COLLATION:            sprintf(buf,"SQL_NULL_COLLATION(%ld)",InfoType);break;
	case SQL_ALTER_TABLE:               sprintf(buf,"SQL_ALTER_TABLE(%ld)",InfoType);break;
	case SQL_COLUMN_ALIAS:              sprintf(buf,"SQL_COLUMN_ALIAS(%ld)",InfoType);break;
	case SQL_GROUP_BY:                  sprintf(buf,"SQL_GROUP_BY(%ld)",InfoType);break;
	case SQL_KEYWORDS:                  sprintf(buf,"SQL_KEYWORDS(%ld)",InfoType);break;
	case SQL_ORDER_BY_COLUMNS_IN_SELECT:sprintf(buf,"SQL_ORDER_BY_COLUMNS_IN_SELECT(%ld)",InfoType);break;
	case SQL_SCHEMA_USAGE:              sprintf(buf,"SQL_SCHEMA_USAGE(%ld)",InfoType);break;
	case SQL_CATALOG_USAGE:				sprintf(buf,"SQL_CATALOG_USAGE(%ld)",InfoType);break;
	case SQL_QUOTED_IDENTIFIER_CASE:    sprintf(buf,"SQL_QUOTED_IDENTIFIER_CASE(%ld)",InfoType);break;
	case SQL_SPECIAL_CHARACTERS:        sprintf(buf,"SQL_SPECIAL_CHARACTERS(%ld)",InfoType);break;
	case SQL_SUBQUERIES:                sprintf(buf,"SQL_SUBQUERIES(%ld)",InfoType);break;
	case SQL_UNION:                     sprintf(buf,"SQL_UNION(%ld)",InfoType);break;
	case SQL_MAX_COLUMNS_IN_GROUP_BY:   sprintf(buf,"SQL_MAX_COLUMNS_IN_GROUP_BY(%ld)",InfoType);break;
	case SQL_MAX_COLUMNS_IN_INDEX:      sprintf(buf,"SQL_MAX_COLUMNS_IN_INDEX(%ld)",InfoType);break;
	case SQL_MAX_COLUMNS_IN_ORDER_BY:   sprintf(buf,"SQL_MAX_COLUMNS_IN_ORDER_BY(%ld)",InfoType);break;
	case SQL_MAX_COLUMNS_IN_SELECT:     sprintf(buf,"SQL_MAX_COLUMNS_IN_SELECT(%ld)",InfoType);break;
	case SQL_MAX_COLUMNS_IN_TABLE:      sprintf(buf,"SQL_MAX_COLUMNS_IN_TABLE(%ld)",InfoType);break;
	case SQL_MAX_INDEX_SIZE:            sprintf(buf,"SQL_MAX_INDEX_SIZE(%ld)",InfoType);break;
	case SQL_MAX_ROW_SIZE_INCLUDES_LONG:sprintf(buf,"SQL_MAX_ROW_SIZE_INCLUDES_LONG(%ld)",InfoType);break;
	case SQL_MAX_ROW_SIZE:              sprintf(buf,"SQL_MAX_ROW_SIZE(%ld)",InfoType);break;
	case SQL_MAX_STATEMENT_LEN:         sprintf(buf,"SQL_MAX_STATEMENT_LEN(%ld)",InfoType);break;
	case SQL_MAX_TABLES_IN_SELECT:      sprintf(buf,"SQL_MAX_TABLES_IN_SELECT(%ld)",InfoType);break;
	case SQL_MAX_USER_NAME_LEN:         sprintf(buf,"SQL_MAX_USER_NAME_LEN(%ld)",InfoType);break;
	case SQL_MAX_CHAR_LITERAL_LEN:      sprintf(buf,"SQL_MAX_CHAR_LITERAL_LEN(%ld)",InfoType);break;
	case SQL_TIMEDATE_ADD_INTERVALS:    sprintf(buf,"SQL_TIMEDATE_ADD_INTERVALS(%ld)",InfoType);break;
	case SQL_TIMEDATE_DIFF_INTERVALS:   sprintf(buf,"SQL_TIMEDATE_DIFF_INTERVALS(%ld)",InfoType);break;
	case SQL_NEED_LONG_DATA_LEN:        sprintf(buf,"SQL_NEED_LONG_DATA_LEN(%ld)",InfoType);break;
	case SQL_MAX_BINARY_LITERAL_LEN:    sprintf(buf,"SQL_MAX_BINARY_LITERAL_LEN(%ld)",InfoType);break;
	case SQL_LIKE_ESCAPE_CLAUSE:        sprintf(buf,"SQL_LIKE_ESCAPE_CLAUSE(%ld)",InfoType);break;
	case SQL_CATALOG_LOCATION:			sprintf(buf,"SQL_CATALOG_LOCATION(%ld)",InfoType);break;
	case SQL_OJ_CAPABILITIES:			sprintf(buf,"SQL_OJ_CAPABILITIES(%ld)",InfoType);break;
	case SQL_ACTIVE_ENVIRONMENTS:		sprintf(buf,"SQL_ACTIVE_ENVIRONMENTS(%ld)",InfoType);break;
	case SQL_ALTER_DOMAIN:				sprintf(buf,"SQL_ALTER_DOMAIN(%ld)",InfoType);break;
	case SQL_SQL_CONFORMANCE:			sprintf(buf,"SQL_SQL_CONFORMANCE(%ld)",InfoType);break;
	case SQL_DATETIME_LITERALS:			sprintf(buf,"SQL_DATETIME_LITERALS(%ld)",InfoType);break;
	case SQL_BATCH_ROW_COUNT:			sprintf(buf,"SQL_BATCH_ROW_COUNT(%ld)",InfoType);break;
	case SQL_BATCH_SUPPORT:				sprintf(buf,"SQL_BATCH_SUPPORT(%ld)",InfoType);break;
	case SQL_CREATE_ASSERTION:			sprintf(buf,"SQL_CREATE_ASSERTION(%ld)",InfoType);break;
	case SQL_CREATE_CHARACTER_SET:		sprintf(buf,"SQL_CREATE_CHARACTER_SET(%ld)",InfoType);break;
	case SQL_CREATE_COLLATION:			sprintf(buf,"SQL_CREATE_COLLATION(%ld)",InfoType);break;
	case SQL_CREATE_DOMAIN:				sprintf(buf,"SQL_CREATE_DOMAIN(%ld)",InfoType);break;
	case SQL_CREATE_SCHEMA:				sprintf(buf,"SQL_CREATE_SCHEMA(%ld)",InfoType);break;
	case SQL_CREATE_TABLE:				sprintf(buf,"SQL_CREATE_TABLE(%ld)",InfoType);break;
	case SQL_CREATE_TRANSLATION:		sprintf(buf,"SQL_CREATE_TRANSLATION(%ld)",InfoType);break;
	case SQL_CREATE_VIEW:				sprintf(buf,"SQL_CREATE_VIEW(%ld)",InfoType);break;
	case SQL_DRIVER_HDESC:				sprintf(buf,"SQL_DRIVER_HDESC(%ld)",InfoType);break;
	case SQL_DROP_ASSERTION:			sprintf(buf,"SQL_DROP_ASSERTION(%ld)",InfoType);break;
	case SQL_DROP_CHARACTER_SET:		sprintf(buf,"SQL_DROP_CHARACTER_SET(%ld)",InfoType);break;
	case SQL_DROP_COLLATION:			sprintf(buf,"SQL_DROP_COLLATION(%ld)",InfoType);break;
	case SQL_DROP_DOMAIN:				sprintf(buf,"SQL_DROP_DOMAIN(%ld)",InfoType);break;
	case SQL_DROP_SCHEMA:				sprintf(buf,"SQL_DROP_SCHEMA(%ld)",InfoType);break;
	case SQL_DROP_TABLE:				sprintf(buf,"SQL_DROP_TABLE(%ld)",InfoType);break;
	case SQL_DROP_TRANSLATION:			sprintf(buf,"SQL_DROP_TRANSLATION(%ld)",InfoType);break;
	case SQL_DROP_VIEW:					sprintf(buf,"SQL_DROP_VIEW(%ld)",InfoType);break;
	case SQL_INDEX_KEYWORDS:			sprintf(buf,"SQL_INDEX_KEYWORDS(%ld)",InfoType);break;
	case SQL_INFO_SCHEMA_VIEWS:			sprintf(buf,"SQL_INFO_SCHEMA_VIEWS(%ld)",InfoType);break;
	case SQL_ODBC_INTERFACE_CONFORMANCE:sprintf(buf,"SQL_ODBC_INTERFACE_CONFORMANCE(%ld)",InfoType);break;
	case SQL_PARAM_ARRAY_ROW_COUNTS:	sprintf(buf,"SQL_PARAM_ARRAY_ROW_COUNTS(%ld)",InfoType);break;
	case SQL_PARAM_ARRAY_SELECTS:		sprintf(buf,"SQL_PARAM_ARRAY_SELECTS(%ld)",InfoType);break;
	case SQL_SQL92_DATETIME_FUNCTIONS:	sprintf(buf,"SQL_SQL92_DATETIME_FUNCTIONS(%ld)",InfoType);break;
	case SQL_SQL92_FOREIGN_KEY_DELETE_RULE:sprintf(buf,"SQL_SQL92_FOREIGN_KEY_DELETE_RULE(%ld)",InfoType);break;
	case SQL_SQL92_FOREIGN_KEY_UPDATE_RULE:sprintf(buf,"SQL_SQL92_FOREIGN_KEY_UPDATE_RULE(%ld)",InfoType);break;
	case SQL_SQL92_GRANT:				sprintf(buf,"SQL_SQL92_GRANT(%ld)",InfoType);break;
	case SQL_SQL92_NUMERIC_VALUE_FUNCTIONS:sprintf(buf,"SQL_SQL92_NUMERIC_VALUE_FUNCTIONS(%ld)",InfoType);break;
	case SQL_SQL92_PREDICATES:			sprintf(buf,"SQL_SQL92_PREDICATES(%ld)",InfoType);break;
	case SQL_SQL92_RELATIONAL_JOIN_OPERATORS:sprintf(buf,"SQL_SQL92_RELATIONAL_JOIN_OPERATORS(%ld)",InfoType);break;
	case SQL_SQL92_REVOKE:				sprintf(buf,"SQL_SQL92_REVOKE(%ld)",InfoType);break;
	case SQL_SQL92_ROW_VALUE_CONSTRUCTOR:sprintf(buf,"SQL_SQL92_ROW_VALUE_CONSTRUCTOR(%ld)",InfoType);break;
	case SQL_SQL92_STRING_FUNCTIONS:	sprintf(buf,"SQL_SQL92_STRING_FUNCTIONS(%ld)",InfoType);break;
	case SQL_SQL92_VALUE_EXPRESSIONS:	sprintf(buf,"SQL_SQL92_VALUE_EXPRESSIONS(%ld)",InfoType);break;
	case SQL_STANDARD_CLI_CONFORMANCE:	sprintf(buf,"SQL_STANDARD_CLI_CONFORMANCE(%ld)",InfoType);break;
	case SQL_AGGREGATE_FUNCTIONS:		sprintf(buf,"SQL_AGGREGATE_FUNCTIONS(%ld)",InfoType);break;
	case SQL_DDL_INDEX:					sprintf(buf,"SQL_DDL_INDEX(%ld)",InfoType);break;
	case SQL_INSERT_STATEMENT:			sprintf(buf,"SQL_INSERT_STATEMENT(%ld)",InfoType);break;
	case SQL_XOPEN_CLI_YEAR:			sprintf(buf,"SQL_XOPEN_CLI_YEAR(%ld)",InfoType);break;
	default:
		_ltoa(InfoType,buf,10);
	}
	return buf;
}

/****************************************************************
** StrFunctionToString()
**
** This function will attempt to convert a String Fuction bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
char *StrFunctionToString(long StrFunction, char *buf)
{
	char TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(StrFunction&SQL_FN_STR_ASCII){
		strcat (buf,"SQL_FN_STR_ASCII ");
		StrFunction=StrFunction^SQL_FN_STR_ASCII;
		}
	if(StrFunction&SQL_FN_STR_BIT_LENGTH){
		strcat (buf,"SQL_FN_STR_BIT_LENGTH ");
		StrFunction=StrFunction^SQL_FN_STR_BIT_LENGTH;
		}
	if(StrFunction&SQL_FN_STR_CHAR){
		strcat (buf,"SQL_FN_STR_CHAR ");
		StrFunction=StrFunction^SQL_FN_STR_CHAR;
		}
	if(StrFunction&SQL_FN_STR_CHAR_LENGTH){
		strcat (buf,"SQL_FN_STR_CHAR_LENGTH ");
		StrFunction=StrFunction^SQL_FN_STR_CHAR_LENGTH;
		}
	if(StrFunction&SQL_FN_STR_CHARACTER_LENGTH){
		strcat (buf,"SQL_FN_STR_CHARACTER_LENGTH ");
		StrFunction=StrFunction^SQL_FN_STR_CHARACTER_LENGTH;
		}
	if(StrFunction&SQL_FN_STR_CONCAT){
		strcat (buf,"SQL_FN_STR_CONCAT ");
		StrFunction=StrFunction^SQL_FN_STR_CONCAT;
		}
	if(StrFunction&SQL_FN_STR_DIFFERENCE){
		strcat (buf,"SQL_FN_STR_DIFFERENCE ");
		StrFunction=StrFunction^SQL_FN_STR_DIFFERENCE;
		}
	if(StrFunction&SQL_FN_STR_INSERT){
		strcat (buf,"SQL_FN_STR_INSERT ");
		StrFunction=StrFunction^SQL_FN_STR_INSERT;
		}
	if(StrFunction&SQL_FN_STR_LCASE){
		strcat (buf,"SQL_FN_STR_LCASE ");
		StrFunction=StrFunction^SQL_FN_STR_LCASE;
		}
	if(StrFunction&SQL_FN_STR_LEFT){
		strcat (buf,"SQL_FN_STR_LEFT ");
		StrFunction=StrFunction^SQL_FN_STR_LEFT;
		}
	if(StrFunction&SQL_FN_STR_LENGTH){
		strcat (buf,"SQL_FN_STR_LENGTH ");
		StrFunction=StrFunction^SQL_FN_STR_LENGTH;
		}
	if(StrFunction&SQL_FN_STR_LOCATE){
		strcat (buf,"SQL_FN_STR_LOCATE ");
		StrFunction=StrFunction^SQL_FN_STR_LOCATE;
		}
	if(StrFunction&SQL_FN_STR_LOCATE_2){
		strcat (buf,"SQL_FN_STR_LOCATE_2 ");
		StrFunction=StrFunction^SQL_FN_STR_LOCATE_2;
		}
	if(StrFunction&SQL_FN_STR_LTRIM){ 
		strcat (buf,"SQL_FN_STR_LTRIM ");
		StrFunction=StrFunction^SQL_FN_STR_LTRIM;
		}
	if(StrFunction&SQL_FN_STR_OCTET_LENGTH){ 
		strcat (buf,"SQL_FN_STR_OCTET_LENGTH ");
		StrFunction=StrFunction^SQL_FN_STR_OCTET_LENGTH;
		}
	if(StrFunction&SQL_FN_STR_POSITION){
		strcat (buf,"SQL_FN_STR_POSITION ");
		StrFunction=StrFunction^SQL_FN_STR_POSITION;
		}
	if(StrFunction&SQL_FN_STR_REPEAT){
		strcat (buf,"SQL_FN_STR_REPEAT ");
		StrFunction=StrFunction^SQL_FN_STR_REPEAT;
		}
	if(StrFunction&SQL_FN_STR_REPLACE){
		strcat (buf,"SQL_FN_STR_REPLACE ");
		StrFunction=StrFunction^SQL_FN_STR_REPLACE;
		}
	if(StrFunction&SQL_FN_STR_RIGHT){
		strcat (buf,"SQL_FN_STR_RIGHT ");
		StrFunction=StrFunction^SQL_FN_STR_RIGHT;
		}
	if(StrFunction&SQL_FN_STR_RTRIM){
		strcat (buf,"SQL_FN_STR_RTRIM ");
		StrFunction=StrFunction^SQL_FN_STR_RTRIM;
		}
	if(StrFunction&SQL_FN_STR_SOUNDEX){
		strcat (buf,"SQL_FN_STR_SOUNDEX ");
		StrFunction=StrFunction^SQL_FN_STR_SOUNDEX;
		}
	if(StrFunction&SQL_FN_STR_SPACE){
		strcat (buf,"SQL_FN_STR_SPACE ");
		StrFunction=StrFunction^SQL_FN_STR_SPACE;
		}
	if(StrFunction&SQL_FN_STR_SUBSTRING){
		strcat (buf,"SQL_FN_STR_SUBSTRING ");
		StrFunction=StrFunction^SQL_FN_STR_SUBSTRING;
		}
	if(StrFunction&SQL_FN_STR_UCASE){
		strcat (buf,"SQL_FN_STR_UCASE ");
		StrFunction=StrFunction^SQL_FN_STR_UCASE;
		}
	
	// Should be zero unless there are undefined bits
	if(StrFunction){
		sprintf(TempBuf,"<UndefinedBits:0x%08lX>",StrFunction);
		strcat(buf,TempBuf);
		}

	return buf;
	}
		
/****************************************************************
** TimeFunctionToString()
**
** This function will attempt to convert a Time Function bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
char *TimeFunctionToString(long TimeFunction, char *buf)
{
	char TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
if(TimeFunction&SQL_FN_TD_CURRENT_DATE){
		strcat (buf,"SQL_FN_TD_CURRENT_DATE ");
		TimeFunction=TimeFunction^SQL_FN_TD_CURRENT_DATE;
		}
if(TimeFunction&SQL_FN_TD_CURRENT_TIME){
		strcat (buf,"SQL_FN_TD_CURRENT_TIME ");
		TimeFunction=TimeFunction^SQL_FN_TD_CURRENT_TIME;
		}
if(TimeFunction&SQL_FN_TD_CURRENT_TIMESTAMP){
		strcat (buf,"SQL_FN_TD_CURRENT_TIMESTAMP ");
		TimeFunction=TimeFunction^SQL_FN_TD_CURRENT_TIMESTAMP;
		}
if(TimeFunction&SQL_FN_TD_CURDATE){
		strcat (buf,"SQL_FN_TD_CURDATE ");
		TimeFunction=TimeFunction^SQL_FN_TD_CURDATE;
		}
if(TimeFunction&SQL_FN_TD_CURTIME){ 
		strcat (buf,"SQL_FN_TD_CURTIME ");
		TimeFunction=TimeFunction^SQL_FN_TD_CURTIME;
		}
if(TimeFunction&SQL_FN_TD_DAYNAME){
		strcat (buf,"SQL_FN_TD_DAYNAME ");
		TimeFunction=TimeFunction^SQL_FN_TD_DAYNAME;
		}
if(TimeFunction&SQL_FN_TD_DAYOFMONTH){
		strcat (buf,"SQL_FN_TD_DAYOFMONTH ");
		TimeFunction=TimeFunction^SQL_FN_TD_DAYOFMONTH;
		}
if(TimeFunction&SQL_FN_TD_DAYOFWEEK){
		strcat (buf,"SQL_FN_TD_DAYOFWEEK ");
		TimeFunction=TimeFunction^SQL_FN_TD_DAYOFWEEK;
		}
if(TimeFunction&SQL_FN_TD_DAYOFYEAR){ 
		strcat (buf,"SQL_FN_TD_DAYOFYEAR ");
		TimeFunction=TimeFunction^SQL_FN_TD_DAYOFYEAR;
		}
if(TimeFunction&SQL_FN_TD_EXTRACT){
		strcat (buf,"SQL_FN_TD_EXTRACT ");
		TimeFunction=TimeFunction^SQL_FN_TD_EXTRACT;
		}
if(TimeFunction&SQL_FN_TD_HOUR){
		strcat (buf,"SQL_FN_TD_HOUR ");
		TimeFunction=TimeFunction^SQL_FN_TD_HOUR;
		}
if(TimeFunction&SQL_FN_TD_MINUTE){
		strcat (buf,"SQL_FN_TD_MINUTE ");
		TimeFunction=TimeFunction^SQL_FN_TD_MINUTE;
		}
if(TimeFunction&SQL_FN_TD_MONTH){
		strcat (buf,"SQL_FN_TD_MONTH ");
		TimeFunction=TimeFunction^SQL_FN_TD_MONTH;
		}
if(TimeFunction&SQL_FN_TD_MONTHNAME){
		strcat (buf,"SQL_FN_TD_MONTHNAME ");
		TimeFunction=TimeFunction^SQL_FN_TD_MONTHNAME;
		}
if(TimeFunction&SQL_FN_TD_NOW){
		strcat (buf,"SQL_FN_TD_NOW ");
		TimeFunction=TimeFunction^SQL_FN_TD_NOW;
		}
if(TimeFunction&SQL_FN_TD_QUARTER){
		strcat (buf,"SQL_FN_TD_QUARTER ");
		TimeFunction=TimeFunction^SQL_FN_TD_QUARTER;
		}
if(TimeFunction&SQL_FN_TD_SECOND){
		strcat (buf,"SQL_FN_TD_SECOND ");
		TimeFunction=TimeFunction^SQL_FN_TD_SECOND;
		}
if(TimeFunction&SQL_FN_TD_TIMESTAMPADD){
		strcat (buf,"SQL_FN_TD_TIMESTAMPADD ");
		TimeFunction=TimeFunction^SQL_FN_TD_TIMESTAMPADD;
		}
if(TimeFunction&SQL_FN_TD_TIMESTAMPDIFF){
		strcat (buf,"SQL_FN_TD_TIMESTAMPDIFF ");
		TimeFunction=TimeFunction^SQL_FN_TD_TIMESTAMPDIFF;
		}
if(TimeFunction&SQL_FN_TD_WEEK){
		strcat (buf,"SQL_FN_TD_WEEK ");
		TimeFunction=TimeFunction^SQL_FN_TD_WEEK;
		}
if(TimeFunction&SQL_FN_TD_YEAR){
		strcat (buf,"SQL_FN_TD_YEAR ");
		TimeFunction=TimeFunction^SQL_FN_TD_YEAR;
		}

	// Should be zero unless there are undefined bits
	if(TimeFunction){
		sprintf(TempBuf,"<UndefinedBits:0x%08lX>",TimeFunction);
		strcat(buf,TempBuf);
		}

	return buf;
	}

/****************************************************************
** TimeIntToString()
**
** This function will attempt to convert a Time Interval bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
char *TimeIntToString(long TimeInt, char *buf)
{
	char TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(TimeInt&SQL_FN_TSI_FRAC_SECOND){
		strcat (buf,"SQL_FN_TSI_FRAC_SECOND ");
		TimeInt=TimeInt^SQL_FN_TSI_FRAC_SECOND;
		}
	if(TimeInt&SQL_FN_TSI_SECOND){
		strcat (buf,"SQL_FN_TSI_SECOND ");
		TimeInt=TimeInt^SQL_FN_TSI_SECOND;
		}
	if(TimeInt&SQL_FN_TSI_MINUTE){
		strcat (buf,"SQL_FN_TSI_MINUTE ");
		TimeInt=TimeInt^SQL_FN_TSI_MINUTE;
		}
	if(TimeInt&SQL_FN_TSI_HOUR){
		strcat (buf,"SQL_FN_TSI_HOUR ");
		TimeInt=TimeInt^SQL_FN_TSI_HOUR;
		}
	if(TimeInt&SQL_FN_TSI_DAY){
		strcat (buf,"SQL_FN_TSI_DAY ");
		TimeInt=TimeInt^SQL_FN_TSI_DAY;
		}
	if(TimeInt&SQL_FN_TSI_WEEK){
		strcat (buf,"SQL_FN_TSI_WEEK ");
		TimeInt=TimeInt^SQL_FN_TSI_WEEK;
		}
	if(TimeInt&SQL_FN_TSI_MONTH){
		strcat (buf,"SQL_FN_TSI_MONTH ");
		TimeInt=TimeInt^SQL_FN_TSI_MONTH;
		}
	if(TimeInt&SQL_FN_TSI_QUARTER){
		strcat (buf,"SQL_FN_TSI_QUARTER ");
		TimeInt=TimeInt^SQL_FN_TSI_QUARTER;
		}
	if(TimeInt&SQL_FN_TSI_YEAR){
		strcat (buf,"SQL_FN_TSI_YEAR ");
		TimeInt=TimeInt^SQL_FN_TSI_YEAR;
		}

	// Should be zero unless there are undefined bits
	if(TimeInt){
		sprintf(TempBuf,"<UndefinedBits:0x%08lX>",TimeInt);
		strcat(buf,TempBuf);
		}

	return buf;
	}

/****************************************************************
** OJToString()
**
** This function will attempt to convert an Outer Join Capabilities bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
char *OJToString(long OJ, char *buf)
{
	char TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(OJ&SQL_OJ_LEFT){
		strcat (buf,"SQL_OJ_LEFT ");
		OJ=OJ^SQL_OJ_LEFT;
		}
	if(OJ&SQL_OJ_RIGHT){
		strcat (buf,"SQL_OJ_RIGHT ");
		OJ=OJ^SQL_OJ_RIGHT;
		}
	if(OJ&SQL_OJ_FULL){
		strcat (buf,"SQL_OJ_FULL ");
		OJ=OJ^SQL_OJ_FULL;
		}
	if(OJ&SQL_OJ_NESTED){
		strcat (buf,"SQL_OJ_NESTED ");
		OJ=OJ^SQL_OJ_NESTED;
		}
	if(OJ&SQL_OJ_NOT_ORDERED){
		strcat (buf,"SQL_OJ_NOT_ORDERED ");
		OJ=OJ^SQL_OJ_NOT_ORDERED;
		}
	if(OJ&SQL_OJ_INNER){
		strcat (buf,"SQL_OJ_INNER ");
		OJ=OJ^SQL_OJ_INNER;
		}
	if(OJ&SQL_OJ_ALL_COMPARISON_OPS){ 
		strcat (buf,"SQL_OJ_ALL_COMPARISON_OPS ");
		OJ=OJ^SQL_OJ_ALL_COMPARISON_OPS;
		}

	// Should be zero unless there are undefined bits
	if(OJ){
		sprintf(TempBuf,"<UndefinedBits:0x%08lX>",OJ);
		strcat(buf,TempBuf);
		}

	return buf;
	}

/****************************************************************
** GDExtToString()
**
** This function will attempt to convert a GetData Extensions bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
char *GDExtToString(long GDExt, char *buf)
{
	char TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(GDExt&SQL_GD_ANY_COLUMN){
		strcat (buf,"SQL_GD_ANY_COLUMN ");
		GDExt=GDExt^SQL_GD_ANY_COLUMN;
		}
	if(GDExt&SQL_GD_ANY_ORDER){
		strcat (buf,"SQL_GD_ANY_ORDER ");
		GDExt=GDExt^SQL_GD_ANY_ORDER;
		}
	if(GDExt&SQL_GD_BLOCK){
		strcat (buf,"SQL_GD_BLOCK ");
		GDExt=GDExt^SQL_GD_BLOCK;
		}
	if(GDExt&SQL_GD_BOUND){
		strcat (buf,"SQL_GD_BOUND ");
		GDExt=GDExt^SQL_GD_BOUND;
		}

	// Should be zero unless there are undefined bits
	if(GDExt){
		sprintf(TempBuf,"<UndefinedBits:0x%08lX>",GDExt);
		strcat(buf,TempBuf);
		}

	return buf;
	}

/****************************************************************
** NumFunctionToString()
**
** This function will attempt to convert a Numeric Fuction bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
char *NumFunctionToString(long NumFunction, char *buf)
{
	char TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(NumFunction&SQL_FN_NUM_ABS){
		strcat (buf,"SQL_FN_NUM_ABS ");
		NumFunction=NumFunction^SQL_FN_NUM_ABS;
		}
	if(NumFunction&SQL_FN_NUM_ACOS){
		strcat (buf,"SQL_FN_NUM_ACOS ");
		NumFunction=NumFunction^SQL_FN_NUM_ACOS;
		}
	if(NumFunction&SQL_FN_NUM_ASIN){
		strcat (buf,"SQL_FN_NUM_ASIN ");
		NumFunction=NumFunction^SQL_FN_NUM_ASIN;
		}
	if(NumFunction&SQL_FN_NUM_ATAN){
		strcat (buf,"SQL_FN_NUM_ATAN ");
		NumFunction=NumFunction^SQL_FN_NUM_ATAN;
		}
	if(NumFunction&SQL_FN_NUM_ATAN2){
		strcat (buf,"SQL_FN_NUM_ATAN2 ");
		NumFunction=NumFunction^SQL_FN_NUM_ATAN2;
		}
	if(NumFunction&SQL_FN_NUM_CEILING){
		strcat (buf,"SQL_FN_NUM_CEILING ");
		NumFunction=NumFunction^SQL_FN_NUM_CEILING;
		}
	if(NumFunction&SQL_FN_NUM_COS){
		strcat (buf,"SQL_FN_NUM_COS ");
		NumFunction=NumFunction^SQL_FN_NUM_COS;
		}
	if(NumFunction&SQL_FN_NUM_COT){
		strcat (buf,"SQL_FN_NUM_COT ");
		NumFunction=NumFunction^SQL_FN_NUM_COT;
		}
	if(NumFunction&SQL_FN_NUM_DEGREES){
		strcat (buf,"SQL_FN_NUM_DEGREES ");
		NumFunction=NumFunction^SQL_FN_NUM_DEGREES;
		}
	if(NumFunction&SQL_FN_NUM_EXP){
		strcat (buf,"SQL_FN_NUM_EXP ");
		NumFunction=NumFunction^SQL_FN_NUM_EXP;
		}
	if(NumFunction&SQL_FN_NUM_FLOOR){
		strcat (buf,"SQL_FN_NUM_FLOOR ");
		NumFunction=NumFunction^SQL_FN_NUM_FLOOR;
		}
	if(NumFunction&SQL_FN_NUM_LOG){
		strcat (buf,"SQL_FN_NUM_LOG ");
		NumFunction=NumFunction^SQL_FN_NUM_LOG;
		}
	if(NumFunction&SQL_FN_NUM_LOG10){
		strcat (buf,"SQL_FN_NUM_LOG10 ");
		NumFunction=NumFunction^SQL_FN_NUM_LOG10;
		}
	if(NumFunction&SQL_FN_NUM_MOD){
		strcat (buf,"SQL_FN_NUM_MOD ");
		NumFunction=NumFunction^SQL_FN_NUM_MOD;
		}
	if(NumFunction&SQL_FN_NUM_PI){
		strcat (buf,"SQL_FN_NUM_PI ");
		NumFunction=NumFunction^SQL_FN_NUM_PI;
		}
	if(NumFunction&SQL_FN_NUM_POWER){
		strcat (buf,"SQL_FN_NUM_POWER ");
		NumFunction=NumFunction^SQL_FN_NUM_POWER;
		}
	if(NumFunction&SQL_FN_NUM_RADIANS){
		strcat (buf,"SQL_FN_NUM_RADIANS ");
		NumFunction=NumFunction^SQL_FN_NUM_RADIANS;
		}
	if(NumFunction&SQL_FN_NUM_RAND){
		strcat (buf,"SQL_FN_NUM_RAND ");
		NumFunction=NumFunction^SQL_FN_NUM_RAND;
		}
	if(NumFunction&SQL_FN_NUM_ROUND){
		strcat (buf,"SQL_FN_NUM_ROUND ");
		NumFunction=NumFunction^SQL_FN_NUM_ROUND;
		}
	if(NumFunction&SQL_FN_NUM_SIGN){
		strcat (buf,"SQL_FN_NUM_SIGN ");
		NumFunction=NumFunction^SQL_FN_NUM_SIGN;
		}
	if(NumFunction&SQL_FN_NUM_SIN){
		strcat (buf,"SQL_FN_NUM_SIN ");
		NumFunction=NumFunction^SQL_FN_NUM_SIN;
		}
	if(NumFunction&SQL_FN_NUM_SQRT){
		strcat (buf,"SQL_FN_NUM_SQRT ");
		NumFunction=NumFunction^SQL_FN_NUM_SQRT;
		}
	if(NumFunction&SQL_FN_NUM_TAN){
		strcat (buf,"SQL_FN_NUM_TAN ");
		NumFunction=NumFunction^SQL_FN_NUM_TAN;
		}
	if(NumFunction&SQL_FN_NUM_TRUNCATE){
		strcat (buf,"SQL_FN_NUM_TRUNCATE ");
		NumFunction=NumFunction^SQL_FN_NUM_TRUNCATE;
		}

	// Should be zero unless there are undefined bits
	if(NumFunction){
		sprintf(TempBuf,"<UndefinedBits:0x%08lX>",NumFunction);
		strcat(buf,TempBuf);
		}

	return buf;
	}
		
/****************************************************************
** CatalogUsageToString()
**
** This function will attempt to convert a catalog usage bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
char *CatalogUsageToString(long CatUsage, char *buf)
{
	char TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(CatUsage&SQL_CU_DML_STATEMENTS){
		strcat (buf,"SQL_CU_DML_STATEMENTS ");
		CatUsage=CatUsage^SQL_CU_DML_STATEMENTS;
		}
	if(CatUsage&SQL_CU_PROCEDURE_INVOCATION){
		strcat (buf,"SQL_CU_PROCEDURE_INVOCATION ");
		CatUsage=CatUsage^SQL_CU_PROCEDURE_INVOCATION;
		}
	if(CatUsage&SQL_CU_TABLE_DEFINITION){
		strcat (buf,"SQL_CU_TABLE_DEFINITION ");
		CatUsage=CatUsage^SQL_CU_TABLE_DEFINITION;
		}
	if(CatUsage&SQL_CU_INDEX_DEFINITION){
		strcat (buf,"SQL_CU_INDEX_DEFINITION ");
		CatUsage=CatUsage^SQL_CU_INDEX_DEFINITION;
		}
	if(CatUsage&SQL_CU_PRIVILEGE_DEFINITION){
		strcat (buf,"SQL_CU_PRIVILEGE_DEFINITION ");
		CatUsage=CatUsage^SQL_CU_PRIVILEGE_DEFINITION;
		}

	// Should be zero unless there are undefined bits
	if(CatUsage){
		sprintf(TempBuf,"<UndefinedBits:0x%08lX>",CatUsage);
		strcat(buf,TempBuf);
		}

	return buf;
}

/****************************************************************
** SchemaUsageToString()
**
** This function will attempt to convert a schema usage bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
char *SchemaUsageToString(long SchemaUsage, char *buf)
{
	char TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(SchemaUsage&SQL_SU_DML_STATEMENTS){
		strcat (buf,"SQL_SU_DML_STATEMENTS ");
		SchemaUsage=SchemaUsage^SQL_SU_DML_STATEMENTS;
		}
	if(SchemaUsage&SQL_SU_PROCEDURE_INVOCATION){
		strcat (buf,"SQL_SU_PROCEDURE_INVOCATION ");
		SchemaUsage=SchemaUsage^SQL_SU_PROCEDURE_INVOCATION;
		}
	if(SchemaUsage&SQL_SU_TABLE_DEFINITION){
		strcat (buf,"SQL_SU_TABLE_DEFINITION ");
		SchemaUsage=SchemaUsage^SQL_SU_TABLE_DEFINITION;
		}
	if(SchemaUsage&SQL_SU_INDEX_DEFINITION){
		strcat (buf,"SQL_SU_INDEX_DEFINITION ");
		SchemaUsage=SchemaUsage^SQL_SU_INDEX_DEFINITION;
		}
	if(SchemaUsage&SQL_SU_PRIVILEGE_DEFINITION){
		strcat (buf,"SQL_SU_PRIVILEGE_DEFINITION ");
		SchemaUsage=SchemaUsage^SQL_SU_PRIVILEGE_DEFINITION;
		}

	// Should be zero unless there are undefined bits
	if(SchemaUsage){
		sprintf(TempBuf,"<UndefinedBits:0x%08lX>",SchemaUsage);
		strcat(buf,TempBuf);
		}

	return buf;
}

/****************************************************************
** GroupByToString()
**
** This function will attempt to convert a Group By value
** into a more user friendly character string.
** If the value isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
char *GroupByToString(SWORD GroupBy, char *buf)
{
   switch (GroupBy) {
		case SQL_GB_COLLATE:							strcpy (buf,"SQL_GB_COLLATE");break;
		case SQL_GB_NOT_SUPPORTED:					strcpy (buf,"SQL_GB_NOT_SUPPORTED");break;
		case SQL_GB_GROUP_BY_EQUALS_SELECT:		strcpy (buf,"SQL_GB_GROUP_BY_EQUALS_SELECT");break;
		case SQL_GB_GROUP_BY_CONTAINS_SELECT:	strcpy (buf,"SQL_GB_GROUP_BY_CONTAINS_SELECT");break;
		case SQL_GB_NO_RELATION:					strcpy (buf,"SQL_GB_NO_RELATION");break;
      default:
         _itoa(GroupBy,buf,10);
		}
	return buf;
}


/****************************************************************
** CaseToString()
**
** This function will attempt to convert an Identifier Case value
** into a more user friendly character string.
** If the value isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
char *CaseToString(SWORD CaseValue, char *buf)
{
   switch (CaseValue) {
		case SQL_IC_UPPER:		strcpy (buf,"SQL_IC_UPPER");break;
		case SQL_IC_LOWER:		strcpy (buf,"SQL_IC_LOWER");break;
		case SQL_IC_SENSITIVE:	strcpy (buf,"SQL_IC_SENSITIVE");break;
		case SQL_IC_MIXED:		strcpy (buf,"SQL_IC_MIXED");break;
      default:
         _itoa(CaseValue,buf,10);
		}
	return buf;
}

/****************************************************************
** ConcatNullToString()
**
** This function will attempt to convert a concat null behavior value
** into a more user friendly character string.
** If the concat null behavior value isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
char *ConcatNullToString(SWORD ConcatNull, char *buf)
{
   switch (ConcatNull) {
		case SQL_CB_NULL:			strcpy (buf,"SQL_CB_NULL");break;
		case SQL_CB_NON_NULL:	strcpy (buf,"SQL_CB_NON_NULL");break;
      default:
         _itoa(ConcatNull,buf,10);
		}
	return buf;
}

/****************************************************************
** CA1ToString()
**
** This function will attempt to convert a Cursor Attribute bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
char *CA1ToString(long CAValue, char *buf)
{
	char TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(CAValue&SQL_CA1_NEXT){
		strcat(buf,"SQL_CA1_NEXT ");
		CAValue=CAValue^SQL_CA1_NEXT;
		}
	if(CAValue&SQL_CA1_ABSOLUTE){
		strcat(buf,"SQL_CA1_ABSOLUTE ");
		CAValue=CAValue^SQL_CA1_ABSOLUTE;
		}
	if(CAValue&SQL_CA1_RELATIVE){
		strcat(buf,"SQL_CA1_RELATIVE ");
		CAValue=CAValue^SQL_CA1_RELATIVE;
		}
	if(CAValue&SQL_CA1_BOOKMARK){
		strcat(buf,"SQL_CA1_BOOKMARK ");
		CAValue=CAValue^SQL_CA1_BOOKMARK;
		}
	if(CAValue&SQL_CA1_LOCK_NO_CHANGE){
		strcat(buf,"SQL_CA1_LOCK_NO_CHANGE ");
		CAValue=CAValue^SQL_CA1_LOCK_NO_CHANGE;
		}
	if(CAValue&SQL_CA1_LOCK_EXCLUSIVE){
		strcat(buf,"SQL_CA1_LOCK_EXCLUSIVE ");
		CAValue=CAValue^SQL_CA1_LOCK_EXCLUSIVE;
		}
	if(CAValue&SQL_CA1_LOCK_UNLOCK){
		strcat(buf,"SQL_CA1_LOCK_UNLOCK ");
		CAValue=CAValue^SQL_CA1_LOCK_UNLOCK;
		}
	if(CAValue&SQL_CA1_POS_POSITION){
		strcat(buf,"SQL_CA1_POS_POSITION ");
		CAValue=CAValue^SQL_CA1_POS_POSITION;
		}
	if(CAValue&SQL_CA1_POS_UPDATE){
		strcat(buf,"SQL_CA1_POS_UPDATE ");
		CAValue=CAValue^SQL_CA1_POS_UPDATE;
		}
	if(CAValue&SQL_CA1_POS_DELETE){
		strcat(buf,"SQL_CA1_POS_DELETE ");
		CAValue=CAValue^SQL_CA1_POS_DELETE;
		}
	if(CAValue&SQL_CA1_POS_REFRESH){
		strcat(buf,"SQL_CA1_POS_REFRESH ");
		CAValue=CAValue^SQL_CA1_POS_REFRESH;
		}
	if(CAValue&SQL_CA1_POSITIONED_UPDATE){
		strcat(buf,"SQL_CA1_POSITIONED_UPDATE ");
		CAValue=CAValue^SQL_CA1_POSITIONED_UPDATE;
		}
	if(CAValue&SQL_CA1_POSITIONED_DELETE){
		strcat(buf,"SQL_CA1_POSITIONED_DELETE ");
		CAValue=CAValue^SQL_CA1_POSITIONED_DELETE;
		}
	if(CAValue&SQL_CA1_SELECT_FOR_UPDATE){
		strcat(buf,"SQL_CA1_SELECT_FOR_UPDATE ");
		CAValue=CAValue^SQL_CA1_SELECT_FOR_UPDATE;
		}
	if(CAValue&SQL_CA1_BULK_ADD){
		strcat(buf,"SQL_CA1_BULK_ADD ");
		CAValue=CAValue^SQL_CA1_BULK_ADD;
		}
	if(CAValue&SQL_CA1_BULK_UPDATE_BY_BOOKMARK){
		strcat(buf,"SQL_CA1_BULK_UPDATE_BY_BOOKMARK ");
		CAValue=CAValue^SQL_CA1_BULK_UPDATE_BY_BOOKMARK;
		}
	if(CAValue&SQL_CA1_BULK_DELETE_BY_BOOKMARK){
		strcat(buf,"SQL_CA1_BULK_DELETE_BY_BOOKMARK ");
		CAValue=CAValue^SQL_CA1_BULK_DELETE_BY_BOOKMARK;
		}
	if(CAValue&SQL_CA1_BULK_FETCH_BY_BOOKMARK){
		strcat(buf,"SQL_CA1_BULK_FETCH_BY_BOOKMARK ");
		CAValue=CAValue^SQL_CA1_BULK_FETCH_BY_BOOKMARK;
		}
	
	// Should be zero unless there are undefined bits
	if(CAValue){
		sprintf(TempBuf,"<UndefinedBits:0x%08lX>",CAValue);
		strcat(buf,TempBuf);
		}

	return buf;
}

/****************************************************************
** CA2ToString()
**
** This function will attempt to convert a Cursor Attribute bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
char *CA2ToString(long CAValue, char *buf)
{
	char TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(CAValue&SQL_CA2_READ_ONLY_CONCURRENCY){
		strcat(buf,"SQL_CA2_READ_ONLY_CONCURRENCY ");
		CAValue=CAValue^SQL_CA2_READ_ONLY_CONCURRENCY;
		}
	if(CAValue&SQL_CA2_LOCK_CONCURRENCY){
		strcat(buf,"SQL_CA2_LOCK_CONCURRENCY ");
		CAValue=CAValue^SQL_CA2_LOCK_CONCURRENCY;
		}
	if(CAValue&SQL_CA2_OPT_ROWVER_CONCURRENCY){
		strcat(buf,"SQL_CA2_OPT_ROWVER_CONCURRENCY ");
		CAValue=CAValue^SQL_CA2_OPT_ROWVER_CONCURRENCY;
		}
	if(CAValue&SQL_CA2_OPT_VALUES_CONCURRENCY){
		strcat(buf,"SQL_CA2_OPT_VALUES_CONCURRENCY ");
		CAValue=CAValue^SQL_CA2_OPT_VALUES_CONCURRENCY;
		}
	if(CAValue&SQL_CA2_SENSITIVITY_ADDITIONS){
		strcat(buf,"SQL_CA2_SENSITIVITY_ADDITIONS ");
		CAValue=CAValue^SQL_CA2_SENSITIVITY_ADDITIONS;
		}
	if(CAValue&SQL_CA2_SENSITIVITY_DELETIONS){
		strcat(buf,"SQL_CA2_SENSITIVITY_DELETIONS ");
		CAValue=CAValue^SQL_CA2_SENSITIVITY_DELETIONS;
		}
	if(CAValue&SQL_CA2_SENSITIVITY_UPDATES){
		strcat(buf,"SQL_CA2_SENSITIVITY_UPDATES ");
		CAValue=CAValue^SQL_CA2_SENSITIVITY_UPDATES;
		}
	if(CAValue&SQL_CA2_MAX_ROWS_SELECT){
		strcat(buf,"SQL_CA2_MAX_ROWS_SELECT ");
		CAValue=CAValue^SQL_CA2_MAX_ROWS_SELECT;
		}
	if(CAValue&SQL_CA2_MAX_ROWS_INSERT){
		strcat(buf,"SQL_CA2_MAX_ROWS_INSERT ");
		CAValue=CAValue^SQL_CA2_MAX_ROWS_INSERT;
		}
	if(CAValue&SQL_CA2_MAX_ROWS_DELETE){
		strcat(buf,"SQL_CA2_MAX_ROWS_DELETE ");
		CAValue=CAValue^SQL_CA2_MAX_ROWS_DELETE;
		}
	if(CAValue&SQL_CA2_MAX_ROWS_UPDATE){
		strcat(buf,"SQL_CA2_MAX_ROWS_UPDATE ");
		CAValue=CAValue^SQL_CA2_MAX_ROWS_UPDATE;
		}
	if(CAValue&SQL_CA2_MAX_ROWS_CATALOG){
		strcat(buf,"SQL_CA2_MAX_ROWS_CATALOG ");
		CAValue=CAValue^SQL_CA2_MAX_ROWS_CATALOG;
		}
	if(CAValue&SQL_CA2_MAX_ROWS_AFFECTS_ALL){
		strcat(buf,"SQL_CA2_MAX_ROWS_AFFECTS_ALL ");
		CAValue=CAValue^SQL_CA2_MAX_ROWS_AFFECTS_ALL;
		}
	if(CAValue&SQL_CA2_CRC_EXACT){
		strcat(buf,"SQL_CA2_CRC_EXACT ");
		CAValue=CAValue^SQL_CA2_CRC_EXACT;
		}
	if(CAValue&SQL_CA2_CRC_APPROXIMATE){
		strcat(buf,"SQL_CA2_CRC_APPROXIMATE ");
		CAValue=CAValue^SQL_CA2_CRC_APPROXIMATE;
		}
	if(CAValue&SQL_CA2_SIMULATE_NON_UNIQUE){
		strcat(buf,"SQL_CA2_SIMULATE_NON_UNIQUE ");
		CAValue=CAValue^SQL_CA2_SIMULATE_NON_UNIQUE;
		}
	if(CAValue&SQL_CA2_SIMULATE_TRY_UNIQUE){
		strcat(buf,"SQL_CA2_SIMULATE_TRY_UNIQUE ");
		CAValue=CAValue^SQL_CA2_SIMULATE_TRY_UNIQUE;
		}
	if(CAValue&SQL_CA2_SIMULATE_UNIQUE){
		strcat(buf,"SQL_CA2_SIMULATE_UNIQUE ");
		CAValue=CAValue^SQL_CA2_SIMULATE_UNIQUE;
		}
	
	// Should be zero unless there are undefined bits
	if(CAValue){
		sprintf(TempBuf,"<UndefinedBits:0x%08lX>",CAValue);
		strcat(buf,TempBuf);
		}

	return buf;
}

/****************************************************************
** ConvertValueToString()
**
** This function will attempt to convert a Convert Value bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
char *ConvertValueToString(long ConvertValue, char *buf)
{
	char TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(ConvertValue&SQL_CVT_BIGINT){
		strcat(buf,"SQL_CVT_BIGINT ");
		ConvertValue=ConvertValue^SQL_CVT_BIGINT;
		}
	if(ConvertValue&SQL_CVT_BINARY){
		strcat(buf,"SQL_CVT_BINARY ");
		ConvertValue=ConvertValue^SQL_CVT_BINARY;
		}
	if(ConvertValue&SQL_CVT_BIT){
		strcat(buf,"SQL_CVT_BIT "); 
		ConvertValue=ConvertValue^SQL_CVT_BIT;
		}
	if(ConvertValue&SQL_CVT_CHAR){
		strcat(buf,"SQL_CVT_CHAR "); 
		ConvertValue=ConvertValue^SQL_CVT_CHAR;
		}
	if(ConvertValue&SQL_CVT_DATE){
		strcat(buf,"SQL_CVT_DATE ");
		ConvertValue=ConvertValue^SQL_CVT_DATE;
		}
	if(ConvertValue&SQL_CVT_DECIMAL){
		strcat(buf,"SQL_CVT_DECIMAL ");
		ConvertValue=ConvertValue^SQL_CVT_DECIMAL;
		}
	if(ConvertValue&SQL_CVT_DOUBLE){
		strcat(buf,"SQL_CVT_DOUBLE ");
		ConvertValue=ConvertValue^SQL_CVT_DOUBLE;
		}
	if(ConvertValue&SQL_CVT_FLOAT){
		strcat(buf,"SQL_CVT_FLOAT ");
		ConvertValue=ConvertValue^SQL_CVT_FLOAT;
		}
	if(ConvertValue&SQL_CVT_INTEGER){
		strcat(buf,"SQL_CVT_INTEGER ");
		ConvertValue=ConvertValue^SQL_CVT_INTEGER;
		}
	if(ConvertValue&SQL_CVT_INTERVAL_YEAR_MONTH){
		strcat(buf,"SQL_CVT_INTERVAL_YEAR_MONTH ");
		ConvertValue=ConvertValue^SQL_CVT_INTERVAL_YEAR_MONTH;
		}
	if(ConvertValue&SQL_CVT_INTERVAL_DAY_TIME){
		strcat(buf,"SQL_CVT_INTERVAL_DAY_TIME ");
		ConvertValue=ConvertValue^SQL_CVT_INTERVAL_DAY_TIME;
		}
	if(ConvertValue&SQL_CVT_LONGVARBINARY){
		strcat(buf,"SQL_CVT_LONGVARBINARY ");
		ConvertValue=ConvertValue^SQL_CVT_LONGVARBINARY;
		}
	if(ConvertValue&SQL_CVT_LONGVARCHAR){
		strcat(buf,"SQL_CVT_LONGVARCHAR ");
		ConvertValue=ConvertValue^SQL_CVT_LONGVARCHAR;
		}
	if(ConvertValue&SQL_CVT_NUMERIC){
		strcat(buf,"SQL_CVT_NUMERIC ");
		ConvertValue=ConvertValue^SQL_CVT_NUMERIC;
		}
	if(ConvertValue&SQL_CVT_REAL){
		strcat(buf,"SQL_CVT_REAL ");
		ConvertValue=ConvertValue^SQL_CVT_REAL;
		}
	if(ConvertValue&SQL_CVT_SMALLINT){
		strcat(buf,"SQL_CVT_SMALLINT ");
		ConvertValue=ConvertValue^SQL_CVT_SMALLINT;
		}
	if(ConvertValue&SQL_CVT_TIME){
		strcat(buf,"SQL_CVT_TIME ");
		ConvertValue=ConvertValue^SQL_CVT_TIME;
		}
	if(ConvertValue&SQL_CVT_TIMESTAMP){
		strcat(buf,"SQL_CVT_TIMESTAMP ");
		ConvertValue=ConvertValue^SQL_CVT_TIMESTAMP;
		}
	if(ConvertValue&SQL_CVT_TINYINT){
		strcat(buf,"SQL_CVT_TINYINT ");
		ConvertValue=ConvertValue^SQL_CVT_TINYINT;
		}
	if(ConvertValue&SQL_CVT_VARBINARY){
		strcat(buf,"SQL_CVT_VARBINARY ");
		ConvertValue=ConvertValue^SQL_CVT_VARBINARY;
		}
	if(ConvertValue&SQL_CVT_VARCHAR){
		strcat(buf,"SQL_CVT_VARCHAR ");
		ConvertValue=ConvertValue^SQL_CVT_VARCHAR;
		}
	if(ConvertValue&SQL_CVT_WCHAR){
		strcat(buf,"SQL_CVT_WCHAR ");
		ConvertValue=ConvertValue^SQL_CVT_WCHAR;
		}
	if(ConvertValue&SQL_CVT_WLONGVARCHAR){
		strcat(buf,"SQL_CVT_WLONGVARCHAR ");
		ConvertValue=ConvertValue^SQL_CVT_WLONGVARCHAR;
		}
	if(ConvertValue&SQL_CVT_WVARCHAR){
		strcat(buf,"SQL_CVT_WVARCHAR ");
		ConvertValue=ConvertValue^SQL_CVT_WVARCHAR;
		}

	// Should be zero unless there are undefined bits
	if(ConvertValue){
		sprintf(TempBuf,"<UndefinedBits:0x%08lX>",ConvertValue);
		strcat(buf,TempBuf);
		}

	return buf;
}

/****************************************************************
** CvtFunctionToString()
**
** This function will attempt to convert a Convert Function bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
char *CvtFunctionToString(long CvtFunction, char *buf)
{
	char TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(CvtFunction&SQL_FN_CVT_CAST){
		strcat (buf,"SQL_FN_CVT_CAST ");
		CvtFunction=CvtFunction^SQL_FN_CVT_CAST;
		}
	if(CvtFunction&SQL_FN_CVT_CONVERT){
		strcat(buf,"SQL_FN_CVT_CONVERT ");
		CvtFunction=CvtFunction^SQL_FN_CVT_CONVERT;
		}

	// Should be zero unless there are undefined bits
	if(CvtFunction){
		sprintf(TempBuf,"<UndefinedBits:0x%08lX>",CvtFunction);
		strcat(buf,TempBuf);
		}
	return buf;
}

/****************************************************************
** AggregateTableToString()
**
** This function will attempt to convert an Aggregate Funcions option bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
char *AggregateToString(long AggregateOption, char *buf)
{
	char TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(AggregateOption&SQL_AF_AVG){
		strcat(buf,"SQL_AF_AVG ");
		AggregateOption=AggregateOption^SQL_AF_AVG;
		}
	if(AggregateOption&SQL_AF_COUNT){
		strcat(buf,"SQL_AF_COUNT ");
		AggregateOption=AggregateOption^SQL_AF_COUNT;
		}
	if(AggregateOption&SQL_AF_MAX){
		strcat(buf,"SQL_AF_MAX ");
		AggregateOption=AggregateOption^SQL_AF_MAX;
		}
	if(AggregateOption&SQL_AF_MIN){
		strcat(buf,"SQL_AF_MIN ");
		AggregateOption=AggregateOption^SQL_AF_MIN;
		}
	if(AggregateOption&SQL_AF_SUM){
		strcat(buf,"SQL_AF_SUM ");
		AggregateOption=AggregateOption^SQL_AF_SUM;
		}
	if(AggregateOption&SQL_AF_DISTINCT){
		strcat(buf,"SQL_AF_DISTINCT ");
		AggregateOption=AggregateOption^SQL_AF_DISTINCT;
		}
	if(AggregateOption&SQL_AF_ALL){
		strcat(buf,"SQL_AF_ALL ");
		AggregateOption=AggregateOption^SQL_AF_ALL;
		}

	// Should be zero unless there are undefined bits
	if(AggregateOption){
		sprintf(TempBuf,"<UndefinedBits:0x%08lX>",AggregateOption);
		strcat(buf,TempBuf);
		}

	return buf;
}

/****************************************************************
** AlterTableToString()
**
** This function will attempt to convert an Alter Table option bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
char *AlterTableToString(long AlterOption, char *buf)
{
	char TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(AlterOption&SQL_AT_ADD_COLUMN){
		strcat(buf,"SQL_AT_ADD_COLUMN ");
		AlterOption=AlterOption^SQL_AT_ADD_COLUMN;
		}
	if(AlterOption&SQL_AT_DROP_COLUMN){
		strcat(buf,"SQL_AT_DROP_COLUMN ");
		AlterOption=AlterOption^SQL_AT_DROP_COLUMN;
		}
	if(AlterOption&SQL_AT_CONSTRAINT_NON_DEFERRABLE){
		strcat(buf,"SQL_AT_CONSTRAINT_NON_DEFERRABLE ");
		AlterOption=AlterOption^SQL_AT_CONSTRAINT_NON_DEFERRABLE;
		}
	if(AlterOption&SQL_AT_CONSTRAINT_DEFERRABLE){
		strcat(buf,"SQL_AT_CONSTRAINT_DEFERRABLE ");
		AlterOption=AlterOption^SQL_AT_CONSTRAINT_DEFERRABLE;
		}
	if(AlterOption&SQL_AT_CONSTRAINT_INITIALLY_IMMEDIATE){
		strcat(buf,"SQL_AT_CONSTRAINT_INITIALLY_IMMEDIATE ");
		AlterOption=AlterOption^SQL_AT_CONSTRAINT_INITIALLY_IMMEDIATE;
		}
	if(AlterOption&SQL_AT_CONSTRAINT_INITIALLY_DEFERRED){
		strcat(buf,"SQL_AT_CONSTRAINT_INITIALLY_DEFERRED ");
		AlterOption=AlterOption^SQL_AT_CONSTRAINT_INITIALLY_DEFERRED;
		}
	if(AlterOption&SQL_AT_CONSTRAINT_NAME_DEFINITION){
		strcat(buf,"SQL_AT_CONSTRAINT_NAME_DEFINITION ");
		AlterOption=AlterOption^SQL_AT_CONSTRAINT_NAME_DEFINITION;
		}
	if(AlterOption&SQL_AT_DROP_TABLE_CONSTRAINT_RESTRICT){
		strcat(buf,"SQL_AT_DROP_TABLE_CONSTRAINT_RESTRICT ");
		AlterOption=AlterOption^SQL_AT_DROP_TABLE_CONSTRAINT_RESTRICT;
		}
	if(AlterOption&SQL_AT_DROP_TABLE_CONSTRAINT_CASCADE){
		strcat(buf,"SQL_AT_DROP_TABLE_CONSTRAINT_CASCADE ");
		AlterOption=AlterOption^SQL_AT_DROP_TABLE_CONSTRAINT_CASCADE;
		}
	if(AlterOption&SQL_AT_ADD_TABLE_CONSTRAINT){
		strcat(buf,"SQL_AT_ADD_TABLE_CONSTRAINT ");
		AlterOption=AlterOption^SQL_AT_ADD_TABLE_CONSTRAINT;
		}
	if(AlterOption&SQL_AT_DROP_COLUMN_RESTRICT){
		strcat(buf,"SQL_AT_DROP_COLUMN_RESTRICT ");
		AlterOption=AlterOption^SQL_AT_DROP_COLUMN_RESTRICT;
		}
	if(AlterOption&SQL_AT_DROP_COLUMN_CASCADE){
		strcat(buf,"SQL_AT_DROP_COLUMN_CASCADE ");
		AlterOption=AlterOption^SQL_AT_DROP_COLUMN_CASCADE;
		}
	if(AlterOption&SQL_AT_DROP_COLUMN_DEFAULT){
		strcat(buf,"SQL_AT_DROP_COLUMN_DEFAULT ");
		AlterOption=AlterOption^SQL_AT_DROP_COLUMN_DEFAULT;
		}
	if(AlterOption&SQL_AT_SET_COLUMN_DEFAULT){
		strcat(buf,"SQL_AT_SET_COLUMN_DEFAULT ");
		AlterOption=AlterOption^SQL_AT_SET_COLUMN_DEFAULT;
		}
	if(AlterOption&SQL_AT_ADD_COLUMN_COLLATION){
		strcat(buf,"SQL_AT_ADD_COLUMN_COLLATION ");
		AlterOption=AlterOption^SQL_AT_ADD_COLUMN_COLLATION;
		}
	if(AlterOption&SQL_AT_ADD_COLUMN_DEFAULT){
		strcat(buf,"SQL_AT_ADD_COLUMN_DEFAULT ");
		AlterOption=AlterOption^SQL_AT_ADD_COLUMN_DEFAULT;
		}
	if(AlterOption&SQL_AT_ADD_COLUMN_SINGLE){
		strcat(buf,"SQL_AT_ADD_COLUMN_SINGLE ");
		AlterOption=AlterOption^SQL_AT_ADD_COLUMN_SINGLE;
		}
	if(AlterOption&SQL_AT_ADD_CONSTRAINT){
		strcat(buf,"SQL_AT_ADD_CONSTRAINT ");
		AlterOption=AlterOption^SQL_AT_ADD_CONSTRAINT;
		}

	// Should be zero unless there are undefined bits
	if(AlterOption){
		sprintf(TempBuf,"<UndefinedBits:0x%08lX>",AlterOption);
		strcat(buf,TempBuf);
		}

	return buf;
}

/****************************************************************
** CorrelationToString()
**
** This function will attempt to convert a Correlation Name value
** into a more user friendly character string.
** If the concat null behavior value isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
char *CorrelationToString(SWORD Correl, char *buf)
{
   switch (Correl) {
		case SQL_CN_NONE:			strcpy (buf,"SQL_CN_NONE");break;
		case SQL_CN_DIFFERENT:	strcpy (buf,"SQL_CN_DIFFERENT");break;
		case SQL_CN_ANY:			strcpy (buf,"SQL_CN_ANY");break;
      default:
         _itoa(Correl,buf,10);
		}
	return buf;
}

/****************************************************************
** CursorBehaviorToString()
**
** This function will attempt to convert a Cursor Behavior value
** into a more user friendly character string.
** If the concat null behavior value isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
char *CursorBehaviorToString(SWORD CursorB, char *buf)
{
   switch (CursorB) {
		case SQL_CB_DELETE:		strcpy (buf,"SQL_CB_DELETE");break;
		case SQL_CB_CLOSE:		strcpy (buf,"SQL_CB_CLOSE");break;
		case SQL_CB_PRESERVE:	strcpy (buf,"SQL_CB_PRESERVE");break;
      default:
         _itoa(CursorB,buf,10);
		}
	return buf;
}

/****************************************************************
** TxnIsolationToString()
**
** This function will attempt to convert a Transaction Isolation
** value into a more user friendly character string.
** If the value isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
char *TxnIsolationToString(SDWORD TxnIsolation, char *buf)
{
   switch (TxnIsolation) {
		case SQL_TXN_READ_UNCOMMITTED:	strcpy (buf,"SQL_TXN_READ_UNCOMMITTED");break;
		case SQL_TXN_READ_COMMITTED:		strcpy (buf,"SQL_TXN_READ_COMMITTED");break;
		case SQL_TXN_REPEATABLE_READ:		strcpy (buf,"SQL_TXN_REPEATABLE_READ");break;
		case SQL_TXN_SERIALIZABLE:			strcpy (buf,"SQL_TXN_SERIALIZABLE");break;
      default:
         _itoa(TxnIsolation,buf,10);
		}
	return buf;
}

/****************************************************************
** FileUsageToString()
**
** This function will attempt to convert a File Usage
** value into a more user friendly character string.
** If the value isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
char *FileUsageToString(SDWORD FileUsage, char *buf)
{
   switch (FileUsage) {
		case SQL_FILE_NOT_SUPPORTED:	strcpy (buf,"SQL_FILE_NOT_SUPPORTED");break;
		case SQL_FILE_TABLE:			strcpy (buf,"SQL_FILE_TABLE");break;
		case SQL_FILE_CATALOG:			strcpy (buf,"SQL_FILE_CATALOG");break;
        default:						_itoa(FileUsage,buf,10);
		}
	return buf;
}
              
/**************************************************************
** CheckReturnCode()
**
** This function is used to compare an actual return code from
** an ODBC function to an expected value.  It will log a message
** if the expected return code was not correct. It should never 
** be called directly.  It should always be invoked through the
** CHECKRC macro found in "common.h".
***************************************************************/
TrueFalse CheckReturnCode(
   RETCODE expected,
   RETCODE actual,
   char *FunctionName,
   char *SourceFile,
   short LineNum)
{
	char exp[30];
	char act[30];
    // this is a fix for freestatement since SQL returns SQL_SUCCESS_WITH_INFO for more than one stmt while closing.
	if ((actual == SQL_SUCCESS_WITH_INFO) && (expected == SQL_SUCCESS))
			actual = SQL_SUCCESS;
    // end change.

   if(expected==actual) return(TRUE);
   LogMsg(NONE,"");
   LogMsg(ERRMSG+SHORTTIMESTAMP,"%s: Expected: %s Actual: %s\n",
		FunctionName,ReturncodeToChar(expected,exp),ReturncodeToChar(actual,act));
   LogMsg(NONE,"   File: %s   Line: %d\n",SourceFile,LineNum);
   return(FALSE);
}

TrueFalse DriverConnectNoPrompt(TestInfo *pTestInfo)
{
   RETCODE returncode;
   char ConnectStringOut[MAX_CONNECT_STRING];
   short ConnStrLengthOut;
   char ConnectStringIn[MAX_CONNECT_STRING];
   char *pString;
   char *pTempString;
   char TempString[MAX_CONNECT_STRING];
   SQLHANDLE henv;
   SQLHANDLE hdbc;

   // Initialize the basic handles needed by ODBC 
   returncode = SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &henv);
   if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle")) return(FALSE);

   returncode = SQLSetEnvAttr(henv, SQL_ATTR_ODBC_VERSION, (SQLPOINTER) SQL_OV_ODBC3, 0);
   if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetEnvAttr"))
   {
	   // Cleanup. No need to check return codes since we are already failing
	   SQLFreeHandle(SQL_HANDLE_ENV, henv);
	   return (FALSE);
   }

   returncode = SQLAllocHandle(SQL_HANDLE_DBC, henv, &hdbc);
   if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
   {
	   // Cleanup.  No need to check return codes since we are already failing
	   SQLFreeHandle(SQL_HANDLE_ENV, henv);
	   return(FALSE);
   }

#ifdef _LDAP
   returncode = SQLSetConnectAttr(hdbc,SQL_ATTR_ROLENAME,(SQLPOINTER)secondaryRole,SQL_NTS);
   if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectAttr(SQL_ATTR_ROLENAME)")) {
	   LogMsg(NONE,"unable to set the SQL_ATTR_ROLENAME\n");
   }
#endif
   
   strcpy(ConnectStringIn,"");
   sprintf(ConnectStringIn, "DSN=%s;UID=%s;PWD=%s;",pTestInfo->DataSource,pTestInfo->UserID,pTestInfo->Password);
   // use SQLDriverConnect to let user select datasource and other info 
   returncode = SQLDriverConnect(hdbc,NULL,(SQLCHAR*)ConnectStringIn,sizeof(ConnectStringIn),
                                 (SQLCHAR*)ConnectStringOut,sizeof(ConnectStringOut),&ConnStrLengthOut,
                                 SQL_DRIVER_NOPROMPT);

   // changed this since some ODBC drivers return SQL_SUCCESS_WITH_INFO like SQLSERVER
   if ((returncode != SQL_SUCCESS) && (returncode != SQL_SUCCESS_WITH_INFO))
   {
	   LogAllErrors(henv,hdbc,(SQLHANDLE)NULL);
	   LogMsg(LINEAFTER,"\n   Returned ConnectString=\"%s\"\n",ConnectStringOut);
	   
	   // Cleanup.  No need to check return codes since we are already failing
	   SQLFreeHandle(SQL_HANDLE_DBC, hdbc);
	   SQLFreeHandle(SQL_HANDLE_ENV, henv);
	   return(FALSE);
   }                               
      
   // Strip out DSN from connection string. 
   pString = strstr(ConnectStringOut,"DSN=");
   if (pString != NULL)
   {
	   pString += 4;           // skip past 'DSN='
	   pTempString = TempString;
	   while((*pString != ';') && (*pString != (char)NULL)) 
	   {
		   *pTempString = *pString;
		   pTempString++;
		   pString++;
	   }
	   *pTempString = (char)NULL;
	   strcpy(pTestInfo->DataSource,TempString);
   }
   else
	   strcpy(pTestInfo->DataSource,"");
   
   // Strip out SERVER from connection string.
   pString = strstr(ConnectStringOut,"SERVER=");
   if (pString != NULL)
   {
	   pString += 7;           // skip past 'SERVER='
	   pTempString = TempString;
	   while((*pString != '/') && (*pString != (char)NULL))
	   {
		   *pTempString = *pString;
		   pTempString++;
		   pString++;
	   }
	   *pTempString = (char)NULL;
	   strcpy(pTestInfo->Server,TempString);
   }
   else
	   strcpy(pTestInfo->Server,"");

  // Strip out /PortNumber from connection string.
  pString = strstr(ConnectStringOut,"/");
  if (pString != NULL)
  {
      pString += 1;           // skip past '/'
      pTempString = TempString;
      while ((*pString != ';') && (*pString != (char)NULL)){
		  *pTempString = *pString;
		  pTempString++;
		  pString++;
	  }         
      *pTempString = (char)NULL;
      strcpy(pTestInfo->Port,TempString);
  }
  else 
	  strcpy(pTestInfo->Port,"");

   
   // Strip out UID from connection string.
   pString = strstr(ConnectStringOut,"UID=");
   if (pString != NULL)
   {
	   pString += 4;           // skip past 'UID='
	   pTempString = TempString;
	   while((*pString != ';') && (*pString != (char)NULL))
	   {
		   *pTempString = *pString;
		   pTempString++;
		   pString++;
	   }
	   *pTempString = (char)NULL;
	   strcpy(pTestInfo->UserID,TempString);
   }
   else
	   strcpy(pTestInfo->UserID,"");
   
   // Strip out PWD from connection string.
   pString = strstr(ConnectStringOut,"PWD=");
   if (pString != NULL)
   {
	   pString += 4;           // skip past 'PWD='
	   pTempString = TempString;
	   while((*pString != ';') && (*pString != (char)NULL))
	   {
		   *pTempString = *pString;
		   pTempString++;
		   pString++;
	   }
	   *pTempString = (char)NULL;
	   strcpy((char *)pTestInfo->Password,TempString);
   }
   else
	   strcpy((char *)pTestInfo->Password,"");
   
   // Strip out DBQ from connection string.
   pString = strstr(ConnectStringOut,"DBQ=");
   if (pString != NULL)
   {
	   pString += 4;           // skip past 'DBQ='
	   pTempString = TempString;
	   while ((*pString != ';') && (*pString != (char)NULL))
	  {
		  *pTempString = *pString;
		  pTempString++;
		  pString++;
	  }
	  *pTempString = (char)NULL;
	  strcpy((char *)pTestInfo->Database,TempString);
  }
  else
	  strcpy((char *)pTestInfo->Database,"MASTER");

  // Strip out CATALOG from connection string.
  pString = strstr(ConnectStringOut,"CATALOG=");
  if (pString != NULL)
  {
	  pString += 8;           // skip past 'CATALOG=' 
	  pTempString = TempString;
	   while((*pString != ';') && (*pString != (char)NULL))
	  {
		  *pTempString = *pString;
		  pTempString++;
		  pString++;
	  }
	  *pTempString = (char)NULL;
	   strcpy((char *)pTestInfo->Catalog,TempString);
  }
  else
	  strcpy((char *)pTestInfo->Catalog,"TRAFODION");

  // Strip out SCHEMA from connection string.
  pString = strstr(ConnectStringOut,"SCHEMA=");
  if (pString != NULL)
  {
	  pString += 7;           // skip past 'SCHEMA=' 
	  pTempString = TempString;
	  while((*pString != ';') && (*pString != (char)NULL))
	  {
		  *pTempString = *pString;
		  pTempString++;
		  pString++;
	  }
	  *pTempString = (char)NULL;
          /* Now check to see if there is catalog in the name */
          pString = strstr(TempString, ".");
          if (pString != NULL)
          {
             pString++; // skip catalog and ".".  Only take the schema part
             strcpy (TempString, pString);
          }

	   strcpy((char *)pTestInfo->Schema,TempString);
  }
  //else
  //	   strcpy((char *)pTestInfo->Schema,pTestInfo->Schema);

  // send the current handles to the caller 
  pTestInfo->henv = henv;
  pTestInfo->hdbc = hdbc;
  
  return(TRUE);
}

/**************************************************************
** FullConnect()
** 
** This function will attempt to establish a full connection
** based upon the information within the structure passed in to it.
***************************************************************/                         
TrueFalse FullConnect(TestInfo *pTestInfo)
{
   RETCODE returncode;
   SQLHANDLE henv;
   SQLHANDLE hdbc;
   SQLUINTEGER onoff = 1;
   
   /* Initialize the basic handles needed by ODBC */
   returncode = SQLAllocEnv(&henv);
   if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")) return(FALSE);

   returncode = SQLAllocConnect(henv,&hdbc);
   if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
	   /* Cleanup.  No need to check return codes since we are already failing */
	   SQLFreeEnv(henv);
	   return(FALSE);
   }

   /* 6-5-00:
      Need to turn Autocommit off since MX will close all open cursors that are
      open if the end of ANY of the cursors is reached. */
   /*returncode = SQLSetConnectOption(hdbc, SQL_AUTOCOMMIT, SQL_AUTOCOMMIT_OFF);
   if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
	   // Cleanup.  No need to check return codes since we are already failing
	   SQLFreeEnv(henv);
	   return(FALSE);
   }*/

   //Turn fetch ahead feature 'ON'
   /*
   returncode = SQLSetConnectAttr(hdbc, SQL_ATTR_FETCHAHEAD, (SQLPOINTER)onoff, SQL_IS_POINTER);
   if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
	   // Cleanup.  No need to check return codes since we are already failing
	   SQLFreeEnv(henv);
	   return(FALSE);
   }
   */

#ifdef _LDAP
   returncode = SQLSetConnectAttr(hdbc,SQL_ATTR_ROLENAME,(SQLPOINTER)secondaryRole,SQL_NTS);
   if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectAttr(SQL_ATTR_ROLENAME)")) {
	   LogMsg(NONE,"unable to set the SQL_ATTR_ROLENAME\n");
   }
#endif

   returncode = SQLConnect(hdbc,
                           (SQLCHAR*)pTestInfo->DataSource,(SWORD)strlen(pTestInfo->DataSource),
                           (SQLCHAR*)pTestInfo->UserID,(SWORD)strlen(pTestInfo->UserID),
                           (SQLCHAR*)pTestInfo->Password,(SWORD)strlen(pTestInfo->Password)
                           );
   if ((returncode != SQL_SUCCESS) && (returncode != SQL_SUCCESS_WITH_INFO))
   {
	   /* Cleanup.  No need to check return codes since we are already failing */
	   SQLFreeConnect(hdbc);
	   SQLFreeEnv(henv);
	   return(FALSE);
   }
   
   pTestInfo->henv = (SQLHANDLE)henv;
   pTestInfo->hdbc = (SQLHANDLE)hdbc;
   
   /* Connection established */
   return(TRUE);
}  /* FullConnect() */
   
/**************************************************************
** FullConnectWithOptions()
** 
** This function will attempt to establish a full connection
** based upon the information within the structure passed in to it.
***************************************************************/                         
TrueFalse FullConnectWithOptions(TestInfo *pTestInfo, int Options)
{
	RETCODE returncode;
	SQLHANDLE henv;
	SQLHANDLE hdbc;

	assert( (Options&CONNECT_ODBC_VERSION_2) || (Options&CONNECT_ODBC_VERSION_3) );

	/* Initialize the basic handles needed by ODBC */
	if (Options&CONNECT_ODBC_VERSION_2)
	{
		returncode = SQLAllocEnv(&henv);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")) return(FALSE);
		
		returncode = SQLAllocConnect(henv,&hdbc);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
			/* Cleanup.  No need to check return codes since we are already failing */
			SQLFreeEnv(henv);
			return(FALSE);
		}
	}
	if (Options&CONNECT_ODBC_VERSION_3)
	{
		returncode = SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &henv);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle")) return(FALSE);

		returncode = SQLSetEnvAttr(henv, SQL_ATTR_ODBC_VERSION, (SQLPOINTER) SQL_OV_ODBC3, 0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetEnvAttr"))
		{
			/* Cleanup. No need to check return codes since we are already failing */
			SQLFreeHandle(SQL_HANDLE_ENV, henv);
			return (FALSE);
		}

		returncode = SQLAllocHandle(SQL_HANDLE_DBC, henv, &hdbc);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle")){
			/* Cleanup. No need to check return codes since we are already failing */
			SQLFreeHandle(SQL_HANDLE_ENV, henv);
			return(FALSE);
		}
	}

	// Handle Autocommit_Off Option
	if (Options&CONNECT_AUTOCOMMIT_OFF)
	{
		returncode = SQLSetConnectOption(hdbc, SQL_AUTOCOMMIT, SQL_AUTOCOMMIT_OFF);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
			// Cleanup.  No need to check return codes since we are already failing
			SQLFreeEnv(henv);
			return(FALSE);
		}
	}

#ifdef _LDAP
   returncode = SQLSetConnectAttr(hdbc,SQL_ATTR_ROLENAME,(SQLPOINTER)secondaryRole,SQL_NTS);
   if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectAttr(SQL_ATTR_ROLENAME)")) {
	   LogMsg(NONE,"unable to set the SQL_ATTR_ROLENAME\n");
   }
#endif

	returncode = SQLConnect(hdbc,
                           (SQLCHAR*)pTestInfo->DataSource,(SWORD)strlen(pTestInfo->DataSource),
                           (SQLCHAR*)pTestInfo->UserID,(SWORD)strlen(pTestInfo->UserID),
                           (SQLCHAR*)pTestInfo->Password,(SWORD)strlen(pTestInfo->Password)
                           );
	if ((returncode != SQL_SUCCESS) && (returncode != SQL_SUCCESS_WITH_INFO))
	{
		// Free up handles since we hit a problem.
		if (Options&CONNECT_ODBC_VERSION_2)
		{
			/* Cleanup.  No need to check return codes since we are already failing */
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			return(FALSE);
		}
		if (Options&CONNECT_ODBC_VERSION_3)
		{
			/* Cleanup.  No need to check return codes since we are already failing */		   
			SQLFreeHandle(SQL_HANDLE_DBC, hdbc);
			SQLFreeHandle(SQL_HANDLE_ENV, henv);
		}
	}

	pTestInfo->henv = (SQLHANDLE)henv;
	pTestInfo->hdbc = (SQLHANDLE)hdbc;
	
	/* Connection established */
	return(TRUE);
}  /* FullConnectWithOptions() */

TrueFalse FullDisconnectVer(TestInfo *pTestInfo, int iODBCVer)
{
	if (iODBCVer == SQL_OV_ODBC3)	// ODBC version 3.x
		return FullDisconnect3(pTestInfo);
	else // default for V2 and below (e.g. SQL_OV_ODBC2)
		return FullDisconnect(pTestInfo);
}

/**************************************************************
** FullDisconnect()
**
** This function disconnects a single connection based upon the
** information passed in to it.  If this function returns FALSE
** it does not always mean the disconnect did not happen.  For
** FALSE, the disconnect might have happened and there might have
** been some other error. For ODBC version 2.x and below.
***************************************************************/                         
TrueFalse FullDisconnect(TestInfo *pTestInfo)
{
  RETCODE returncode;                        
  TrueFalse Result;
  
  Result=TRUE;
   
  /* Disconnect from the data source.  If errors, still go on and */
  /* try to free the handles */
  returncode = SQLDisconnect((SQLHANDLE)pTestInfo->hdbc);
  if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDisconnect")) {
		Result=FALSE;	
		LogAllErrors(pTestInfo->henv,pTestInfo->hdbc,pTestInfo->hstmt);
	}
   
  /* Free up all handles used by this connection */
  returncode = SQLFreeConnect((SQLHANDLE)pTestInfo->hdbc);
  if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeConnect")) {
		Result=FALSE;	
		LogAllErrors(pTestInfo->henv,pTestInfo->hdbc,pTestInfo->hstmt);
	}

  returncode = SQLFreeEnv((SQLHANDLE)pTestInfo->henv);
  if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeEnv")) {
		Result=FALSE;	
		LogAllErrors(pTestInfo->henv,pTestInfo->hdbc,pTestInfo->hstmt);
	}
   
  return(Result);
}  /* FullDisconnect() */

/**************************************************************
** FullDisconnect3()
**
** This function disconnects a single connection based upon the
** information passed in to it.  If this function returns FALSE
** it does not always mean the disconnect did not happen.  For
** FALSE, the disconnect might have happened and there might have
** been some other error. For ODBC version 3.x.
***************************************************************/                         
TrueFalse FullDisconnect3(TestInfo *pTestInfo)
{
  RETCODE returncode;                        
  TrueFalse Result;
  
  Result=TRUE;
   
  /* Disconnect from the data source.  If errors, still go on and */
  /* try to free the handles */
  returncode = SQLDisconnect((SQLHANDLE)pTestInfo->hdbc);
  if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDisconnect")) {
		Result=FALSE;	
		LogAllErrors(pTestInfo->henv,pTestInfo->hdbc,pTestInfo->hstmt);
	}
   
  /* Free up all handles used by this connection */
  returncode = SQLFreeHandle(SQL_HANDLE_DBC, (SQLHANDLE)pTestInfo->hdbc);
  if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle")) {
		Result=FALSE;	
		LogAllErrors(pTestInfo->henv,pTestInfo->hdbc,pTestInfo->hstmt);
	}

  returncode = SQLFreeHandle(SQL_HANDLE_ENV, (SQLHANDLE)pTestInfo->henv);
  if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeEnv")) {
		Result=FALSE;	
		LogAllErrors(pTestInfo->henv,pTestInfo->hdbc,pTestInfo->hstmt);
	}
   
  return(Result);
}  /* FullDisconnect3() */

/**************************************************************
** LogAllErrors()
**                          
** This function loops through calls to SQLError() building strings
** for all error messages that might be there and writes them out
** the the log file.
***************************************************************/                         
void LogAllErrors(SQLHANDLE henv,
                  SQLHANDLE hdbc,
                  SQLHANDLE hstmt)
{             
    char	buf[MAX_STRING_SIZE];
    char	State[STATE_SIZE];
	SDWORD	NativeError;
    RETCODE returncode;
	BOOL MsgDisplayed;

	MsgDisplayed=FALSE;

   /* Log any henv error messages */
   returncode = SQLError((SQLHANDLE)henv, (SQLHANDLE)NULL, (SQLHANDLE)NULL, (SQLCHAR*)State, &NativeError, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
   while((returncode == SQL_SUCCESS) ||
         (returncode == SQL_SUCCESS_WITH_INFO)){
		State[STATE_SIZE-1]=NULL_STRING;
      LogPrintf("   State: %s\n"
							  "   Native Error: %ld\n"
                "   Error: %s\n",State,NativeError,buf);
		MsgDisplayed=TRUE;
      returncode = SQLError((SQLHANDLE)henv, (SQLHANDLE)NULL, (SQLHANDLE)NULL, (SQLCHAR*)State, &NativeError, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
   }

   /* Log any hdbc error messages */
   returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)hdbc, (SQLHANDLE)NULL, (SQLCHAR*)State, &NativeError, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
   while((returncode == SQL_SUCCESS) ||
         (returncode == SQL_SUCCESS_WITH_INFO)){
		State[STATE_SIZE-1]=NULL_STRING;
        LogPrintf("   State: %s\n"
							  "   Native Error: %ld\n"
                "   Error: %s\n",State,NativeError,buf);
		MsgDisplayed=TRUE;
      returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)hdbc, (SQLHANDLE)NULL, (SQLCHAR*)State, &NativeError, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
   }

   /* Log any hstmt error messages */
   returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)NULL, (SQLHANDLE)hstmt, (SQLCHAR*)State, &NativeError, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
   while((returncode == SQL_SUCCESS) ||
         (returncode == SQL_SUCCESS_WITH_INFO)){
		State[STATE_SIZE-1]=NULL_STRING;
        LogPrintf("   State: %s\n"
							  "   Native Error: %ld\n"
                "   Error: %s\n",State,NativeError,buf);
		MsgDisplayed=TRUE;
      returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)NULL, (SQLHANDLE)hstmt, (SQLCHAR*)State, &NativeError, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
   }

   /* if no error messages were displayed then display a message */
   if(!MsgDisplayed)
		LogMsg(NONE,"There were no error messages for SQLError() to display\n");
}                     

/**************************************************************
** LogAllErrorsver3()
**                          
** This function loops through calls to SQLError() building strings
** for all error messages that might be there and writes them out
** the the log file.
***************************************************************/        

void LogAllErrorsVer3(SQLHANDLE henv,
                  SQLHANDLE hdbc,
                  SQLHANDLE hstmt)
{             
  SQLCHAR		buf[MAX_STRING_SIZE];
  SQLCHAR		State[STATE_SIZE];
  SQLINTEGER	NativeError;
  RETCODE returncode;
  BOOL MsgDisplayed;
  SQLSMALLINT	ErrorMsglen;
  SQLSMALLINT i =1;

  MsgDisplayed=FALSE;
   /* Log any henv error messages */
   returncode = SQLGetDiagRec(SQL_HANDLE_ENV, (SQLHANDLE)henv,i, State, &NativeError, buf, MAX_STRING_SIZE, &ErrorMsglen);
   while((returncode == SQL_SUCCESS) ||
         (returncode == SQL_SUCCESS_WITH_INFO)){
		State[STATE_SIZE-1]=NULL_STRING;
      LogPrintf("   State: %s\n"
							  "   Native Error: %ld\n"
                "   Error: %s\n",State,NativeError,buf);
    	MsgDisplayed=TRUE;
		i++;
		returncode = SQLGetDiagRec(SQL_HANDLE_ENV, (SQLHANDLE)henv,i, State, &NativeError, buf, MAX_STRING_SIZE, &ErrorMsglen);
      }

   /* Log any hdbc error messages */
   i =1;
   returncode = SQLGetDiagRec(SQL_HANDLE_DBC, (SQLHANDLE)hdbc,i, State, &NativeError, buf, MAX_STRING_SIZE, &ErrorMsglen);
   while((returncode == SQL_SUCCESS) ||
         (returncode == SQL_SUCCESS_WITH_INFO)){
		State[STATE_SIZE-1]=NULL_STRING;
      LogPrintf("   State: %s\n"
							  "   Native Error: %ld\n"
                "   Error: %s\n",State,NativeError,buf);
		MsgDisplayed=TRUE;
		i++;
	   returncode = SQLGetDiagRec(SQL_HANDLE_DBC, (SQLHANDLE)hdbc,i, State, &NativeError, buf, MAX_STRING_SIZE, &ErrorMsglen);
      }

   /* Log any hstmt error messages */
   i =1;
   returncode = SQLGetDiagRec(SQL_HANDLE_STMT,(SQLHANDLE)hstmt,i, State, &NativeError, buf, MAX_STRING_SIZE, &ErrorMsglen);
   while((returncode == SQL_SUCCESS) ||
         (returncode == SQL_SUCCESS_WITH_INFO)){
		State[STATE_SIZE-1]=NULL_STRING;
	    LogPrintf("   State: %s\n"
							  "   Native Error: %ld\n"
                "   Error: %s\n",State,NativeError,buf);
		MsgDisplayed=TRUE;
		i++;
	  returncode = SQLGetDiagRec(SQL_HANDLE_STMT, (SQLHANDLE)hstmt,i, State, &NativeError, buf, MAX_STRING_SIZE, &ErrorMsglen);
      }

   /* if no error messages were displayed then display a message */
	if(!MsgDisplayed){
		LogMsg(NONE,"There were no error messages for SQLError() to display\n");
		}
	
	}                     

/**************************************************************
** FindError()
**                                         
** This function will loop through all possible errors that might
** have occurred looking to see if the one specified in <FindState>
** occurred or not. 
***************************************************************/                         
TrueFalse FindError(char *FindMsg, SQLHANDLE henv, SQLHANDLE hdbc, SQLHANDLE hstmt)
{                 
	char			buf[MAX_STRING_SIZE];
	RETCODE		returncode;
	char			State[STATE_SIZE];
	SDWORD		NativeError;
	TrueFalse found;
	BOOL			MsgDisplayed;

	found = FALSE;
	MsgDisplayed=FALSE;

  // Log any henv error messages 
  returncode = SQLError((SQLHANDLE)henv, (SQLHANDLE)NULL, (SQLHANDLE)NULL, (SQLCHAR*)State, &NativeError, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
  while(((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO)) && !found)
	{
		State[STATE_SIZE-1]=NULL_STRING;
		// scan henv, hdbc, and hstmt for errors of the specified state 
		MsgDisplayed=TRUE;
		if (strstr(FindMsg,State) != NULL)
		{
			found = TRUE;
		}
		else
		{
			found = FALSE;
			LogPrintf("   State: %s\nNativeError: %ld\n%s\n",State,NativeError,buf);
		}
		returncode = SQLError((SQLHANDLE)henv, (SQLHANDLE)NULL, (SQLHANDLE)NULL, (SQLCHAR*)State, &NativeError, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
	}

   /* Log any hdbc error messages */
  returncode = SQLError((SQLHANDLE)NULL,(SQLHANDLE)hdbc, (SQLHANDLE)NULL, (SQLCHAR*)State, &NativeError, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
  while(((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO)) && !found)
	{
		State[STATE_SIZE-1]=NULL_STRING;
		MsgDisplayed=TRUE;
		// scan henv, hdbc, and hstmt for errors of the specified state 
		if (strstr(FindMsg,State) != NULL)
		{
			found = TRUE;
		}
		else
		{
			found = FALSE;
			LogPrintf("   State: %s\nNativeError: %ld\n%s\n",State,NativeError,buf);
		}
		returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)hdbc, (SQLHANDLE)NULL, (SQLCHAR*)State, &NativeError, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
	}

   /* Log any hstmt error messages */
	returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)NULL, (SQLHANDLE)hstmt, (SQLCHAR*)State, &NativeError, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
  while(((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO)) && !found)
	{
		State[STATE_SIZE-1]=NULL_STRING;
		MsgDisplayed=TRUE;
		// scan henv, hdbc, and hstmt for errors of the specified state 
		if (strstr(FindMsg,State) != NULL)
		{
			found = TRUE;
		}
		else
		{
			found = FALSE;
			LogPrintf("   State: %s\nNativeError: %ld\n%s\n",State,NativeError,buf);
		}
		returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)NULL, (SQLHANDLE)hstmt, (SQLCHAR*)State, &NativeError, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
	}

   /* if no error messages were displayed then display a message */
	if(!MsgDisplayed)
	{
		LogMsg(ENDLINE,"There were no error messages for SQLError() to display\n");
	}
	return (found);
}       
              
/**************************************************************
** GetDataAll()
** fetches all the data returned from a statement
** and places it at address buf up to cbBuf characters
** 
** Number of 
** bytes of data available is placed in cbAvail.  
** NOTE: the return value will be true even if the buffer was 
** not large enough for all the data, so 'pRetCode' must be 
** examined to determine if the SQL_SUCCESS_WITH_INFO was 
** received and more data remains to be fetched.
****************************************************************/

TrueFalse GetDataAll( TestInfo* ti, void *buffer, SQLULEN cbBuf, 
			SQLULEN* pcbAvail, RETCODE *pRetCode, SQLULEN cbMaxCol)
{
	SWORD		iNumCols,	/* number of columns in table */
				iCol;	    /*	column index into table   */
	SQLULEN		cbColName;	/* actual number of bytes in column name*/
	SDWORD		iNumChars;	/* number of characters returned */
	SQLULEN		cbWritten = 0L;
	char		outStr[MAX_ROW_LEN];
    char		tempStr[MAX_STRING_SIZE];
	ColumnInfo* Cols;
	SQLULEN		i;
    char*		buf;
	
	FILE *fp = (FILE*)NULL;  /* NULL to write to buf instead */
	
	if (! cbBuf )
	    fp = (FILE*) buffer;	
    else
		buf = (char*)buffer;

	*pcbAvail = 0;
	/* get number of columns in result */
	*pRetCode = SQLNumResultCols( (SQLHANDLE)ti->hstmt, &iNumCols );
	
	/* allocate storage for ColumnInfo structures */
	if ( (void *)NULL == 
		 (Cols = (ColumnInfo *)malloc( iNumCols*sizeof( ColumnInfo ) ) ) )
	{
		sprintf( tempStr,
			"GetDataAll:Could not allocate memory for %d columns", iNumCols );
		LogMsg( ERRMSG, tempStr);
		return FALSE;
	}

	for (iCol = 0; iCol < iNumCols; iCol++ )
	{
		*pRetCode = SQLDescribeCol( (SQLHANDLE)ti->hstmt, 
			(UWORD)(iCol+1), Cols[iCol].Name,MAX_COLUMN_NAME, 
			(SWORD FAR*)&cbColName, &(Cols[iCol].SqlType),
			&(Cols[iCol].Prec),
			&(Cols[iCol].Scale), &(Cols[iCol].Nullable ));
	}

	/* now build string for header */
	strcpy( outStr,"" );
	for (iCol = 0; iCol < iNumCols; iCol++ )
	{
		sprintf( tempStr,"%s", Cols[iCol].Name );
	
		if (strlen( tempStr ) + strlen( outStr ) <
					MAX_ROW_LEN )
		{
			if (iCol)
				strcat( outStr, "," );
			strcat( outStr, tempStr );
		}   
		else
		{
			LogMsg( ERRMSG, "Row too long" );
			free (Cols);
			return FALSE;
		}
	}
	/* write Header string to file or buffer */
	
	if (fp)
		fputs( outStr, fp );
	else
	{
		sprintf( buf, "%s\n\n", outStr );
	}
	
	cbWritten += strlen(outStr);
	cbWritten++;	/*allow for newline char */

	/* build string for divider line */
	for (i = 0; i < cbWritten-1; i++)
		outStr[i] = '-';

	/* write divider line to file or buffer */
	if (fp)
	{
		fputs( outStr, fp );
		fputs( "\n", fp );
	}
	else
	{
		sprintf( buf+cbWritten, "%s\n", outStr );
	}
	cbWritten += cbWritten;
	/* new line character already allotted for in cbWritten value */
	/* while there are more rows fetch data   */
	/* fetch all SQL data types as SQL_C_CHAR */
	while ( SQLFetch((SQLHANDLE) ti->hstmt ) != SQL_NO_DATA_FOUND )
	{
	  strcpy(outStr, ""); /* new row */
	  /* build a row column by column */
	  for ( iCol = 0; iCol < iNumCols; iCol++ )
	  {
		    /* get data for column */
		  	*pRetCode = SQLGetData((SQLHANDLE) ti->hstmt, (UWORD)(iCol+1), 
				SQL_C_CHAR, tempStr, 
				MAX_STRING_SIZE-1, (SQLLEN*)&iNumChars ); 
			/* check for NULL data case */
			if  (iNumChars == SQL_NULL_DATA)
			{
				strcpy( tempStr, "<NULL>");
			}
			else if (( SQL_SUCCESS != *pRetCode ) && 
					 (SQL_SUCCESS_WITH_INFO != *pRetCode ) )
			{
				sprintf( tempStr, "GetDataAll:Col%d %s",
					iCol+1, Cols[iCol].Name );
				LogMsg( ERRMSG, tempStr);					
				free (Cols);
				return FALSE;
			}
          /* write column data to outStr if sufficient buffer space */
		  if( (!fp) && 
			  ( cbWritten + strlen(tempStr) > (SQLULEN)cbBuf ))
		  { /* out of buffer space */  
	 		cbBuf   =  0;
			*pcbAvail += (strlen(tempStr)+1);
		  } 
		  else
		  { 
			/* sufficient buffer space */
			if (iCol)
			{	
				strcat( outStr, "," );
				strcat( outStr, tempStr );
			}
			else
				strcpy( outStr, tempStr);   
		  } /* end else (sufficient buffer space) */
		}	/* end "for iCol", row completed */

		/* write row to file or buffer */
		if (fp)
		{
			/* write to file */
			fputs( outStr, fp );
			cbWritten += strlen(outStr);
			cbWritten++;
		}
		else	/* write to buffer, space permitting */
			if (cbBuf) 
			{
			    /* space left */
				sprintf( buf+cbWritten, "%s\n\n", outStr );
				cbWritten += strlen(outStr);
				cbWritten++;
			}
			else
			{
				/* no space left */
	
			}
	 }  /* end while SQLFetch not returning SQL_NO_DATA_FOUND */

*pcbAvail += cbWritten;/* add bytes written to total available */
/* cleanup */
free( Cols );

SQLFreeStmt((SQLHANDLE) ti->hstmt, SQL_CLOSE );
return TRUE;
}

/*************************************************
**   LogDataAll()
**   Performs GetDataAll and writes results to log
**   pointed to by hlog.  If hlog is -1, then writes
**   to main log file
****************************************************/
#define BUF_SIZE 10000
TrueFalse LogDataAll( TestInfo *ti, HLOGT hlog )
{	
	char		*buf;
	TrueFalse	rslt;
	SQLULEN		cbAvail;
	RETCODE		retcode;

	    /* try GetDataAll with a buffer of BUF_SIZE */
	    if( !(buf = (char *)malloc( BUF_SIZE*sizeof(char) )))
		{
			LogMsg( ERRMSG, "LogDataAll:Memory Allocation error");
			return FALSE;
		}
		rslt = GetDataAll( ti, buf, BUF_SIZE, 
					&cbAvail, &retcode, MAX_COLUMN_NAME );

		if (!rslt)
		{
			LogMsg( ERRMSG, "GetDataAll returned FALSE" );
			return FALSE;
		}
		if ( cbAvail > BUF_SIZE )
		{	
			/* need to allocate larger buffer */
			free(buf);
			if (!(buf = (char *)malloc( cbAvail*sizeof(char) )))
			{
				LogMsg( ERRMSG, "Memory Allocation error" );
				return FALSE;
			}
			rslt = GetDataAll( ti, buf, BUF_SIZE, 
					&cbAvail, &retcode, MAX_COLUMN_NAME );
			if (!rslt)
			{
				LogMsg( ERRMSG, "GetDataAll returned FALSE" );
				return FALSE;
			}
		}	/*end if cbAvail > BUF_SIZE */
//			if ( hlog == (HLOGT)(-1) )
			/* print to main log */
			LogPrintf( "%s", buf );
//		else
//		{
//			AuxLogPrintf( hlog, "%s", buf );
//		}

	return TRUE;
}

SQLCHAR *StmtQueries(long QueryType, char *name, char *buf )
{

	switch (QueryType) 
	{
		case CREATE_TABLE:						sprintf(buf,"create table %s (c1 char(10),c2 varchar(10),c3 decimal(10,5),c4 numeric(10,5),c5 smallint,c6 integer,c7 real,c8 float,c9 double precision,c10 date,c11 time,c12 timestamp,c13 bigint) NO PARTITION",name);break;
		case DROP_TABLE:							sprintf(buf,"drop table %s",name);break;
		case INSERT_TABLE:						sprintf(buf,"insert into %s values ('0123456789','0123456789',1234.56789,1234.56789,1200,12000,123.45E2,123.45E3,123.45E4,{d '1993-07-01'},{t '09:45:30'},{ts '1993-08-02 08:44:31.001'},120000)",name);break;
		case INSERT_TABLE_WITH_PARAM:	sprintf(buf,"insert into %s values (?,?,?,?,?,?,?,?,?,?,?,?,?)",name);break;
		case SELECT_TABLE:						sprintf(buf,"select c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13 from %s",name);break;
		default:
			sprintf(buf,"invalid QueryType %s",name);
	}

	return (SQLCHAR*)buf;
}

char *CreateTableForConversion(int SQLDataType, char *TableName, char *cprec, char *vcprec, char *lvcprec,char *decprec, char *numprec, char *buf )
{
	switch (SQLDataType)
	{
		case MX_DT_ALL:
			sprintf(buf,"create table %s (c1 char(%s),c2 varchar(%s),c3 long varchar,c4 decimal(%s),c5 numeric(%s),c6 smallint,c7 integer,c8 bigint,c9 real,c10 float,c11 double precision,c12 date,c13 time,c14 timestamp) NO PARTITION",TableName,cprec,vcprec,decprec,numprec);
			break;
		case MP_DT_ALL:
			sprintf(buf,"create table %s (c1 char(%s),c2 varchar(%s),c3 long varchar(%s),c4 decimal(%s),c5 numeric(%s),c6 bit,c7 tinyint,c8 smallint,c9 integer,c10 bigint,c11 real,c12 float,c13 double precision,c14 date,c15 time,c16 timestamp,c17 binary(%s),c18 varbinary(%s),c19 long varbinary(%s)) NO PARTITION",TableName,cprec,vcprec,lvcprec,decprec,numprec,cprec,vcprec,lvcprec);
			break;
		case MX_DT_EXCEPT_DATETIME:
			sprintf(buf,"create table %s (c1 char(%s),c2 varchar(%s),c3 long varchar,c4 decimal(%s),c5 numeric(%s),c6 smallint,c6 integer,c7 bigint,c8 real,c9 float,c10 double precision) NO PARTITION",TableName,cprec,vcprec,decprec,numprec);
			break;
		case MP_DT_EXCEPT_DATETIME:
			sprintf(buf,"create table %s (c1 char(%s),c2 varchar(%s),c3 long varchar(%s),c4 decimal(%s),c5 numeric(%s),c6 bit,c7 tinyint,c8 smallint,c9 integer,c10 bigint,c11 real,c12 float,c13 double precision,c14 binary(%s),c15 varbinary(%s),c16 long varbinary(%s)) NO PARTITION",TableName,cprec,vcprec,lvcprec,decprec,numprec,cprec,vcprec,lvcprec);
			break;
		case MX_DT_DATE:
			sprintf(buf,"create table %s (c1 char(%s),c2 varchar(%s),c3 long varchar,c4 date,c5 timestamp) NO PARTITION",TableName,cprec,vcprec);
			break;
		case MX_DT_TIME:
			sprintf(buf,"create table %s (c1 char(%s),c2 varchar(%s),c3 long varchar,c4 time,c6 timestamp) NO PARTITION",TableName,cprec,vcprec);
			break;
		case MX_DT_TIMESTAMP:
			sprintf(buf,"create table %s (c1 char(%s),c2 varchar(%s),c3 long varchar,c4 date,c5 time,c6 timestamp) NO PARTITION",TableName,cprec,vcprec);
			break;
		case MP_DT_DATE:
			sprintf(buf,"create table %s (c1 char(%s),c2 varchar(%s),c3 long varchar(%s),c4 date,c5 timestamp) NO PARTITION",TableName,cprec,vcprec,lvcprec);
			break;
		case MP_DT_TIME:
			sprintf(buf,"create table %s (c1 char(%s),c2 varchar(%s),c3 long varchar(%s),c4 time,c6 timestamp) NO PARTITION",TableName,cprec,vcprec,lvcprec);
			break;
		case MP_DT_TIMESTAMP:
			sprintf(buf,"create table %s (c1 char(%s),c2 varchar(%s),c3 long varchar(%s),c4 date,c5 time,c6 timestamp) NO PARTITION",TableName,cprec,vcprec,lvcprec);
			break;
		default:
			sprintf(buf,"invalid QueryType");
			break;
	}

	return buf;
}

char *PerformanceQueries(long QueryType, char *name, char *buf )
{

	switch (QueryType) 
	{
		case CREATE_TABLE:						sprintf(buf,"create table %s (c1 char(10),c2 varchar(10),c3 decimal(10,5),c4 numeric(10,5),c5 smallint,c6 integer,c7 real,c8 float,c9 double precision) NO PARTITION",name);break;
		case DROP_TABLE:							sprintf(buf,"drop table %s",name);break;
		case INSERT_TABLE:						sprintf(buf,"insert into %s values ('0123456789','0123456789',1234.56789,1234.56789,1200,12000,123.45E2,123.45E3,123.45E4)",name);break;
		case INSERT_TABLE_WITH_PARAM:	sprintf(buf,"insert into %s values (?,?,?,?,?,?,?,?,?)",name);break;
		case SELECT_TABLE:						sprintf(buf,"select c1,c2,c3,c4,c5,c6,c7,c8,c9 from %s",name);break;
		default:
			sprintf(buf,"invalid QueryType %s",name);
	}

	return buf;
}

void LogResultsTest(char *ProcName)
{
        LogMsg(LINEBEFORE+LINEAFTER,"%-35s TEST RESULT: %s Cases=%d Failed=%d\n", ProcName, ((_gTestFailedCount - _gTestFailedIndvCount) ? "FAIL" : "PASS"), _gTestCount - _gTestIndvCount, _gTestFailedCount - _gTestFailedIndvCount);
        _gTestIndvCount = _gTestCount;
        _gTestFailedIndvCount = _gTestFailedCount;
}

char *ReturnColumnDefinition(char *InsStr, short ColNum)
{
	char	colseps[]   = ",";
	char	*coltoken;
	char    TmpCrtCol[4050] = " ";

	strcpy(TmpCrtCol, InsStr);

	ColumnDefinition[0] = '\0';
	if (ColNum == 0)
	{
		if (strstr(_strupr(TmpCrtCol),"CREATE") != NULL)
			strcpy(column_string,strchr(TmpCrtCol,'('));
		else
			strcpy(column_string,TmpCrtCol);
		coltoken = strtok(column_string, colseps);
	}
	else
	{
		coltoken = strtok(NULL, colseps);
	}

	if(coltoken != NULL)
	{
		if ((strstr(_strupr(coltoken),"NUMERIC") != NULL) || (strstr(_strupr(coltoken),"DECIMAL") != NULL))
		{
			strcpy(ColumnDefinition,coltoken);
			strcat(ColumnDefinition,",");
			coltoken = strtok(NULL, colseps);
			if(coltoken != NULL)
				strcat(ColumnDefinition,coltoken);
		}
		else
			strcpy(ColumnDefinition,coltoken);
	}
	else
	{
		strcpy(ColumnDefinition,"INVALID COLUMN DEFINITION");
	}
	return (ColumnDefinition);

}

void LogInfo(TestInfo *pTestInfo)
{
 	RETCODE				returncode;
 	SQLHANDLE 			henv;
 	SQLHANDLE 			hdbc;
 	SQLHANDLE			hstmt;
	SQLLEN cbData;
	char szData[500];
	char temp[256];
    char *ShowCntl = "SHOWCONTROL ALL";
	//Log DSN Info
	LogMsg(NONE, "Data Source : %s\n", pTestInfo->DataSource);
	LogMsg(NONE, "Server : %s\n", pTestInfo->Server);
	LogMsg(NONE, "Port : %s\n", pTestInfo->Port);
	LogMsg(NONE, "UserID : %s\n", pTestInfo->UserID);
	LogMsg(NONE, "Database : %s\n", pTestInfo->Database);
	LogMsg(NONE, "Catalog : %s\n", pTestInfo->Catalog);
	LogMsg(NONE, "Schema : %s\n", pTestInfo->Schema);

	//Log SHOWCONTROL ALL OUTPUT
	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
	returncode = SQLExecDirect(hstmt,(SQLCHAR*) ShowCntl, SQL_NTS);
	if (returncode != SQL_ERROR)
	{
		while (returncode != SQL_NO_DATA_FOUND)
  		{
   			returncode = SQLFetch(hstmt);
   			if (returncode != SQL_NO_DATA_FOUND) {
       			if ( returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO )
   				{
    					returncode=SQLGetData(hstmt, 1, SQL_C_CHAR, szData, 200, &cbData);
    					LogMsg(NONE, "%s\n", szData);
   				} else
   				{
      					LogMsg(NONE, "An unexpected error occurred when calling SQLFetch() in common.c. \n" );
      					LogMsg(NONE, "Log SHOWCONTROL ALL error. Expected SQL_SUCCESS, returned %d\n", returncode);
					LogAllErrors(henv,hdbc,hstmt);
					break;
   				}
			}
  		}
	}
	returncode=SQLFreeStmt(hstmt,SQL_CLOSE);
	/* SEAQUSET isUCS2 = specialMode(hstmt, (char*)"ISO_MAPPING", (char*)"UTF8"); */ isUCS2 = FALSE;

	sprintf(temp, "CREATE SCHEMA \"%s\".\"%s\"", pTestInfo->Catalog, pTestInfo->Schema);
	returncode = SQLExecDirect(hstmt,(SQLCHAR*) temp, SQL_NTS);

	returncode=SQLFreeStmt(hstmt,SQL_CLOSE);
}


/*There functions are added for Character Sets testing
Added by HP
*/

int next_line(char *lineOut, FILE *scriptFD) {
	int p = 0, c = 0;
	char buff[5120];
	strcpy(lineOut,"");
	while (fgets (buff , 5119 , scriptFD) != NULL) {
		//trim
		p = strlen(buff)-1;
		while (buff[p] == ' ' || buff[p] == '\n' || buff[p] == '\r' || buff[p] == '\t') p--;
		buff[p+1] = '\0';

		p = 0;
		while (buff[p] == ' ' || buff[p] == '\n'  || buff[p] == '\r' || buff[p] == '\t') p++;
		if (buff[p] == '\0') continue;
		if (buff[p] == '-' && buff[p+1] == '-') continue;


		//copy to buffer
		c = 0;
		do {
			lineOut[c++] = buff[p];
		}
		while (buff[p++] != '\0');

		return TRUE;
	}
	return FALSE;
}

var_list_t* load_api_vars(char *api, char *textFile) {
	char		line[5120];
	FILE		*scriptFD;
	var_list_t  *my_var_list = NULL;
	int i, p, num_vars = 0;
	int found = FALSE;
	char strAPI[256];
	char seps[]   = "\"";
	char *token;

	if ((scriptFD = fopen(textFile, "r")) == NULL) {
		printf("Error open script file %s\n", textFile);
		return NULL;
	}

	//Find the API block in text file
	sprintf(strAPI, "[%s ", api);
	while (next_line(line, scriptFD)) {
		if (_strnicmp(strAPI, line, strlen(strAPI)) == 0) {
			num_vars = atoi(line + strlen(strAPI));
			found = TRUE;
			break;
		}
	}
	if (!found) {
		fclose(scriptFD);
		printf("Could not find API name %s in the text file %s!\n", api, textFile);
		return NULL;
	}

	if (!found || num_vars == 0) {
		fclose(scriptFD);
		printf("Can not find API %s. Or number of variables is %d\n", api, num_vars);
		return NULL;
	}

	//Allocate mem for variables
	my_var_list = (var_list_t*)malloc(num_vars*sizeof(var_list_t));
	if (my_var_list == NULL) {
		fclose(scriptFD);
		printf("Malloc memory error!\n");
		return NULL;
	}

	//Scan each vars and load to memory
	sprintf(strAPI, "[END]");
	i = 0; found = FALSE;
	while (next_line(line, scriptFD)) {
        if(i > num_vars) {
            fclose(scriptFD);
		    printf("The number specified for API %s is LESS THAN the number of variables declared!\n", api);
		    return NULL;
        }

		if (_strnicmp(strAPI, line, strlen(strAPI)) == 0) {
			found = TRUE;
			break;
		}
		if (i>=num_vars) {
			i++;
			break;
		}

		token = strtok(strdup(line), seps);
		my_var_list[i].value = strdup(line + strlen(token) + 1);
		p = strlen(my_var_list[i].value)-1;
		if (my_var_list[i].value[p] == '"') {
			my_var_list[i].value[p] = '\0';
		}
		else {
			fclose(scriptFD);
			printf("File format error! Variable string must be ended by a double quote. :::%c:::\n", my_var_list[i].value[p]);
			printf("File name: %s\nAPI block: %s\nVariable ID: %s\n", textFile, api, token);
			return NULL;
		}
		
		p = strlen(token)-1;
		while (token[p] == ' ' || token[p] == '\t') p--;
		token[p+1] = '\0';
		my_var_list[i].var_name = strdup(token);

		if (i == (num_vars-1)) my_var_list[i].last = TRUE;
		else my_var_list[i].last = FALSE;

		i++;
	}

	if (!found) {
		fclose(scriptFD);
		printf("The variable block of API %s is not teminated by a marker [END]."
				" OR the text file %s is in wrong format!\n", api, textFile);
		return NULL;
	}

	fclose(scriptFD);
	return my_var_list;
}

void print_list (var_list_t *var_list) {
	int i=0;
	if (var_list == NULL) return;
	do {
		printf("Name: :%s:\n", var_list[i].var_name);
		printf("Value: :%s:\n", var_list[i].value);
		printf("Last: %i\n", var_list[i].last);
	} while(!var_list[i++].last);
	printf("=============================================\n");
}

void free_list (var_list_t *var_list) {
	int i=0;
	if (var_list == NULL) return;
	do {
		free(var_list[i].var_name);
		free(var_list[i].value);
	} while(!var_list[i++].last);

	free(var_list);
}

char* var_mapping(char *var_name, var_list_t *var_list) {
	int i=0;
	if (var_list == NULL) return NULL;
	do {
		if(stricmp(var_name, var_list[i].var_name) == 0) {
			return var_list[i].value;
		}
	} while(!var_list[i++].last);
	printf("Mapping error: Can not find variable name %s\n", var_name);
	return NULL;
}

/*
 *  Charset adaptive strcmp and stricmp for COAST
 */
int cstrcmp(char* str1, char* str2, BOOL ignoreCase, BOOL isCS) {
	int ret = -1;
	if(isCS == TRUE) {
	    if((strstr(str1,str2) != NULL && strlen(str1) == (strlen(str2)+2)) || 
			(strstr(str2,str1) != NULL && strlen(str2) == (strlen(str1)+2)) ||
			strcmp(str1,str2) == 0) 
			ret = 0;
	} else {
		if(ignoreCase == TRUE) 
			ret = stricmp(str1, str2);
		else                   
			ret = strcmp (str1, str2);
	}
	return ret;
}

/*
 *  Charset adaptive strncmp and strnicmp for COAST
 */
int cstrncmp(char* expect, char* actual, BOOL ignoreCase, BOOL isCS, int size) {
	int ret = -1;
	char act[300];
	char exp[300];
	if((isCS==TRUE) && (strlen(actual) != strlen(expect))) {
		strncpy(act, actual, size-2);
		act[size-2]='\0';
		strncpy(exp, expect+1,size-2); 
		exp[size-2]='\0';
		ret = strcmp(exp,act);
	} else {
		if(ignoreCase == TRUE)
			ret = strnicmp(expect, actual, size);
		else
			ret = strncmp (expect, actual, size);
	}
	return ret;
}

char* printSymbol(char* input, char* output) {
	char temp[2048];
	int i = 0, j = 0, len = 0;
	if(input != NULL) {
		output = removeQuotes(input,output);
		len = strlen(output);
		if(len > 0) {
			while(j<len) {
				if(output[j]!='%')
					temp[i++] = output[j++];
				else {
					temp[i++] = output[j];
					temp[i++] = output[j++];
				}
			}
			temp[i] = '\0';
			strcpy (output,temp);
        } else if (len == 0 ) {
			sprintf(output, (char*)"<empty>");
		} else {
            strcpy (output,input);
        }
        return output;
    } else {
	    return NULL;
    }
}

char* removeQuotes(char* in, char* output) {
	char temp[2048];
	int len = 0;
	if(in != NULL) {
		len = strlen(in);
		if( (((in[0]=='"') && (in[len-1]=='"')) || ((in[0]=='\'') && (in[len-1]=='\''))) 
            && (len > 2) ) {
			strncpy(temp,in+1,len-2);
			temp[len-2] = '\0';
            strcpy(output, temp);
		} else {
            strcpy(output,in);
		}
        return output;
    } else {
	    return NULL;
    }
}

BOOL specialMode(SQLHANDLE hstmt, char* cqd, char* mode) {
    SQLRETURN ret;
    char data[256];
    SQLLEN dataPtr = SQL_NTS;
	char temp[1024];

    ret = SQLExecDirect(hstmt, (SQLCHAR*)"CONTROL QUERY DEFAULT SHOWCONTROL_UNEXTERNALIZED_ATTRS 'ON'", SQL_NTS);
	sprintf(temp, "SHOWCONTROL DEFAULT %s, MATCH FULL, NO HEADER", cqd);
    ret = SQLExecDirect(hstmt, (SQLCHAR*)temp, SQL_NTS);
    ret = SQLBindCol(hstmt, 1, SQL_C_CHAR, (SQLPOINTER) data, 256, &dataPtr); 
    ret = SQLFetch(hstmt);
    if (ret == SQL_SUCCESS || ret == SQL_SUCCESS_WITH_INFO) {
        if(strcmp(data, mode) == 0) {
			ret = SQLFreeStmt(hstmt, SQL_CLOSE);
            ret = SQLExecDirect(hstmt, (SQLCHAR*)"CONTROL QUERY DEFAULT SHOWCONTROL_UNEXTERNALIZED_ATTRS 'OFF'", SQL_NTS);
			return TRUE;
        }
    }
    ret = SQLFreeStmt(hstmt, SQL_CLOSE);
    ret = SQLExecDirect(hstmt, (SQLCHAR*)"CONTROL QUERY DEFAULT SHOWCONTROL_UNEXTERNALIZED_ATTRS 'OFF'", SQL_NTS);
    return FALSE;
}

void get_time(char* tmpbuf, int mode) {
	char tmpbuf1[100];
	struct tm *newtime;
	time_t long_time;

	time( &long_time );	// Get time as long integer. 
	newtime = localtime( &long_time );	// Convert to local time. 
	strcpy(tmpbuf,"");
	//day
	strcpy(tmpbuf1,"");
	_itoa(newtime->tm_mday,tmpbuf1,10);
	if (strlen(tmpbuf1) ==  1)
		strcat(tmpbuf,"0");
	strcat(tmpbuf,tmpbuf1);
	//month
	if (mode == 0) strcat(tmpbuf,".");
	strcpy(tmpbuf1,"");
	_itoa(newtime->tm_mon+1,tmpbuf1,10);
	if (strlen(tmpbuf1) ==  1)
		strcat(tmpbuf,"0");
	strcat(tmpbuf,tmpbuf1);
	//year
	if (mode == 0) strcat(tmpbuf,".");
	strcpy(tmpbuf1,"");
	_itoa(newtime->tm_year+1900,tmpbuf1,10);
	strcat(tmpbuf,tmpbuf1);
	//hour
	strcat(tmpbuf,"_");
	strcpy(tmpbuf1,"");
	_itoa(newtime->tm_hour,tmpbuf1,10);
	if (strlen(tmpbuf1) ==  1)
		strcat(tmpbuf,"0");
	strcat(tmpbuf,tmpbuf1);
	//minute
	if (mode == 0) strcat(tmpbuf,".");
	strcpy(tmpbuf1,"");
	_itoa(newtime->tm_min,tmpbuf1,10);
	if (strlen(tmpbuf1) ==  1)
		strcat(tmpbuf,"0");
	strcat(tmpbuf,tmpbuf1);
	//minute
	if (mode == 0) strcat(tmpbuf,".");
	strcpy(tmpbuf1,"");
	_itoa(newtime->tm_sec,tmpbuf1,10);
	if (strlen(tmpbuf1) ==  1)
		strcat(tmpbuf,"0");
	strcat(tmpbuf,tmpbuf1);
}

void get_time_std (char* tmpbuf) {
	get_time(tmpbuf, 0);
}

void get_time_special (char* tmpbuf) {
	get_time(tmpbuf, 1);
}

char *replace_str(char *str, char *orig, char *rep) {
  char *p;

  if(strlen(orig) == strlen(rep)) {
      while(p = strstr(str, orig)) {  // Is 'orig' even in 'str'?
        strncpy(p, rep, strlen(orig)); // Copy characters from 'str' start to 'orig' st$
      }
  } else {
    //LogMsg(NONE,"Error in replace_str function of common.c where size of orig != size of rep\n");
  }
  
  return str;
}

