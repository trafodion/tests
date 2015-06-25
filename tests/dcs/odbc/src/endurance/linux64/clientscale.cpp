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

#include "clientscale.h"

// #define VERBOSE 1
#define OUT_CONN_STR 1024

char connstr[300];
BOOL	PassFail = FALSE;

class odbcCommon
{
	char	msgtxt[300];
	int		m;

	SDWORD RandomValue(int max)
	{
		SDWORD	i = 0;
   
		srand((unsigned)clock());
		i = rand()/(SQL_RANDOM_MAX/max);
		if (max == SQL_RANDOM_MAX)
		{
			srand((unsigned)clock());
			i = i * (rand()/(SQL_RANDOM_MAX/max));
		}
		return i;
	}

	char *RandomString(short length)
	{
		char *StringPtr;
		char *StringBeginningPtr;
		char Letters[64]={"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_"};
		int i;

		/* allocate space for the string */
		StringPtr=(char *)malloc(length+1);
		StringBeginningPtr=StringPtr;

		/* loop, randomly filling the string */
		for(i=0;i<length;i++)
		{
			*StringPtr=Letters[(rand()%63)];
			StringPtr++;
		}

		/* add NULL terminator */
		*StringPtr='\0';
		return(StringBeginningPtr);
	}

	void WriteToLog(const char *logstr)
	{
		time_t	LogTime;
		struct	tm	*LogTimePtr;
	    struct	_timeb tstruct;
		char		temp[MAX_SQLSTRING_LEN];

		LogTime = time(NULL);
		LogTimePtr = localtime(&LogTime);
		_ftime( &tstruct );
		sprintf(temp,"%02d:%02d:%02d.%u\t%s-%s\t%s\t%s",LogTimePtr->tm_hour, LogTimePtr->tm_min, LogTimePtr->tm_sec,tstruct.millitm,ComputerName,ClientNumber,ClientObjectiveNumber,logstr);
		printf(temp);
		fprintf(stream,temp);
		fflush(stream);
	}
	
    void LogStmtErrors(HSTMT hstmt)
    {
	    char		buf[MAX_SQLSTRING_LEN];
	    char		State[STATE_SIZE];
	    RETCODE	returncode;
	    BOOL		ERRTF = FALSE;

	    if (hstmt != NULL)
	    {
		    returncode = SQLError(NULL, NULL, hstmt, (UCHAR *)State, NULL, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
		    while((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		    {
			    sprintf(msgtxt," ERR>> STMT: %s, MSG: %s.",State,buf);
			    WriteToLog(msgtxt);
			    returncode = SQLError(NULL, NULL, hstmt, (UCHAR *)State, NULL, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
			    ERRTF = TRUE;
		    }
	    }
	    if (ERRTF)
	    {
		    sprintf(msgtxt,"\n");
		    WriteToLog(msgtxt);
	    }
    }

	void LogAllErrors(TestInfo *pTestInfo)
	{             
		char		buf[MAX_SQLSTRING_LEN];
		char		State[STATE_SIZE];
		RETCODE	returncode;
		BOOL		ERRTF = FALSE;

		/* Log any henv error messages */
		if (pTestInfo->henv != NULL)
		{
			strcpy(buf,"");
			strcpy(State,"");
			returncode = SQLError(pTestInfo->henv, NULL, NULL, (UCHAR *)State, NULL, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
			while((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
			{
				sprintf(msgtxt,"ERR>> ENV: %s, MSG: %s.",State,buf);
				WriteToLog(msgtxt);
				returncode = SQLError(pTestInfo->henv, NULL, NULL, (UCHAR *)State, NULL, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
				ERRTF = TRUE;
			}
		}

		 /* Log any hdbc error messages */
		if (pTestInfo->hdbc != NULL)
		{
			returncode = SQLError(NULL, pTestInfo->hdbc, NULL, (UCHAR *)State, NULL, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
			while((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
			{
				sprintf(msgtxt," ERR>> HDBC: %s, MSG: %s.",State,buf);
				WriteToLog(msgtxt);
				returncode = SQLError(NULL, pTestInfo->hdbc, NULL, (UCHAR *)State, NULL, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
				ERRTF = TRUE;
			}
		}

		 /* Log any hstmt error messages */
		if (pTestInfo->hstmt != NULL)
		{
			returncode = SQLError(NULL, NULL, pTestInfo->hstmt, (UCHAR *)State, NULL, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
			while((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
			{
				sprintf(msgtxt," ERR>> STMT: %s, MSG: %s.",State,buf);
				WriteToLog(msgtxt);
				returncode = SQLError(NULL, NULL, pTestInfo->hstmt, (UCHAR *)State, NULL, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
				ERRTF = TRUE;
			}
		}
		if (ERRTF)
		{
			sprintf(msgtxt,"\n");
			WriteToLog(msgtxt);
		}
	}                     

	char *SQLCommands(char *ObjName, int command, SDWORD SetValue) // ObjName is Catalog or Schema or Table name etc.
	{
		int		i;
		int		j;
		char	*pk;		// primary key string
		BOOL	YN = FALSE;
		char	*temp;
		BOOL	SelTableUsed[MAX_NUM_TABLES] = {FALSE,};

		sprintf(SQLStmt,"");
		switch (command)
		{
			case CREATE_CATALOG:
				sprintf(SQLStmt,"create catalog %s",ObjName);
				break;
			case CREATE_SCHEMA:
				sprintf(SQLStmt,"create schema %s",ObjName);
				break;
			case DROP_TABLE:
				sprintf(SQLStmt,"drop table %s",ObjName);
				break;
			case CREATE_TABLE:
				pk = new char[300];
				temp = new char[50];
				YN = FALSE;
				strcpy(pk,"");
				sprintf(SQLStmt,"create table %s (",ObjName);
				i = 0;
				while (strcmp(ColumnInfo[i].DataTypestr,END_LOOP) != 0)
				{
					if ((i != 0) && (strcmp(ColumnInfo[i].DataTypestr,END_LOOP) != 0))
						strcat(SQLStmt,",");
					strcat(SQLStmt,ColumnInfo[i].Name);
					strcat(SQLStmt," ");
					strcat(SQLStmt,ColumnInfo[i].Description);
					if (strcmp(ColumnInfo[i].Precision,"") != 0)
					{
						strcat(SQLStmt,"(");
						strcat(SQLStmt,ColumnInfo[i].Precision);
						if (strcmp(ColumnInfo[i].Scale,"") != 0)
						{
							strcat(SQLStmt,",");
							strcat(SQLStmt,ColumnInfo[i].Scale);
						}
						strcat(SQLStmt,")");
					}
					if (ColumnInfo[i].PriKey)
					{
						strcat(SQLStmt," NOT NULL");
						if (YN)
							strcat(pk,",");
						strcat(pk,ColumnInfo[i].Name);
  					YN = TRUE;
					}
					i++;
				}
				Actual_Num_Columns = i;
				if (strcmp(pk,"") != 0)
				{
					strcat(SQLStmt,", PRIMARY KEY (");
					strcat(SQLStmt,pk);
					strcat(SQLStmt,"))");
				}
				else
				{
					strcat(SQLStmt,")");
				}
				delete pk;
				pk = NULL;
				delete temp;
				temp = NULL;
				break;
			case CREATE_TABLE_MX:
				pk = new char[300];
				temp = new char[50];
				YN = FALSE;
				strcpy(pk,"");
				sprintf(SQLStmt,"create table %s (",ObjName);
				i = 0;
				while (strcmp(ColumnInfo[i].DataTypestr,END_LOOP) != 0)
				{
					if ((i != 0) && (strcmp(ColumnInfo[i].DataTypestr,END_LOOP) != 0))
						strcat(SQLStmt,",");
					strcat(SQLStmt,ColumnInfo[i].Name);
					strcat(SQLStmt," ");
					strcat(SQLStmt,ColumnInfo[i].Description);
					if (strcmp(ColumnInfo[i].Precision,"") != 0)
					{
						strcat(SQLStmt,"(");
						strcat(SQLStmt,ColumnInfo[i].Precision);
						if (strcmp(ColumnInfo[i].Scale,"") != 0)
						{
							strcat(SQLStmt,",");
							strcat(SQLStmt,ColumnInfo[i].Scale);
						}
						strcat(SQLStmt,")");
					}
					if (ColumnInfo[i].PriKey)
					{
						strcat(SQLStmt," NOT NULL");
						if (YN)
							strcat(pk,",");
						strcat(pk,ColumnInfo[i].Name);
  					YN = TRUE;
					}
					i++;
				}
				Actual_Num_Columns = i;
				if (strcmp(pk,"") != 0)
				{
					strcat(SQLStmt,", PRIMARY KEY (");
					strcat(SQLStmt,pk);
					strcat(SQLStmt,"))");
				}
				delete pk;
				pk = NULL;
				delete temp;
				temp = NULL;
				break;
			case INSERT_TABLE_PARAMS:
				sprintf(SQLStmt,"insert into %s (",ObjName);
				i = 0;
				while (strcmp(ColumnInfo[i].DataTypestr,END_LOOP) != 0)
				{
					if ((i != 0) && (strcmp(ColumnInfo[i].DataTypestr,END_LOOP) != 0))
						strcat(SQLStmt,",");
					strcat(SQLStmt,ColumnInfo[i].Name);
					i++;
				}
				strcat(SQLStmt,") values (");
				i = 0;
				while (strcmp(ColumnInfo[i].DataTypestr,END_LOOP) != 0)
				{
					if ((i != 0) && (strcmp(ColumnInfo[i].DataTypestr,END_LOOP) != 0))
						strcat(SQLStmt,",");
					strcat(SQLStmt,"?");
					i++;
				}
				strcat(SQLStmt,")");
				break;
			case INSERT_TABLE_VALUES:
				sprintf(SQLStmt,"insert into %s (",ObjName);
				i = 0;
				while (strcmp(ColumnInfo[i].DataTypestr,END_LOOP) != 0)
				{
					if ((i != 0) && (strcmp(ColumnInfo[i].DataTypestr,END_LOOP) != 0))
						strcat(SQLStmt,",");
					strcat(SQLStmt,ColumnInfo[i].Name);
					i++;
				}
				strcat(SQLStmt,") values (");
				i = 0;
				while (strcmp(ColumnInfo[i].DataTypestr,END_LOOP) != 0)
				{
					switch (ColumnInfo[i].DataType)
					{
						case SQL_CHAR:
							sprintf(SQLStmt,"%s '%s',",SQLStmt,InputOutputValues[i].CharValue);
							break;
						case SQL_VARCHAR:
							sprintf(SQLStmt,"%s '%s',",SQLStmt,InputOutputValues[i].VarCharValue);
							break;
						default :
							break;
					}
					i++;
				}
				i = 0;
				if (SetValue != 0)
					i = RandomValue(Total_Num_Rows);
				sprintf(SQLStmt,"%s %s,",SQLStmt,InputOutputValues[i].DecimalValue);
				sprintf(SQLStmt,"%s %s,",SQLStmt,InputOutputValues[i].NumericValue);
				sprintf(SQLStmt,"%s %d,",SQLStmt,InputOutputValues[i].ShortValue);
				sprintf(SQLStmt,"%s %d,",SQLStmt,InputOutputValues[i].LongValue);
				sprintf(SQLStmt,"%s %f,",SQLStmt,InputOutputValues[i].RealValue);
				sprintf(SQLStmt,"%s %e,",SQLStmt,InputOutputValues[i].FloatValue);
				sprintf(SQLStmt,"%s %e,",SQLStmt,InputOutputValues[i].DoubleValue);

				sprintf(SQLStmt,"%s {d '%d-",SQLStmt,InputOutputValues[i].DateValue.year);
				if (InputOutputValues[i].DateValue.month < 10)
					sprintf(SQLStmt,"%s0%d-",SQLStmt,InputOutputValues[i].DateValue.month);
				else
					sprintf(SQLStmt,"%s%d-",SQLStmt,InputOutputValues[i].DateValue.month);
				if (InputOutputValues[i].DateValue.day < 10)
					sprintf(SQLStmt,"%s0%d'},",SQLStmt,InputOutputValues[i].DateValue.day);
				else
					sprintf(SQLStmt,"%s%d'},",SQLStmt,InputOutputValues[i].DateValue.day);

				if (InputOutputValues[i].TimeValue.hour < 10)
					sprintf(SQLStmt,"%s {t '0%d:",SQLStmt,InputOutputValues[i].TimeValue.hour);
				else
					sprintf(SQLStmt,"%s {t '%d:",SQLStmt,InputOutputValues[i].TimeValue.hour);
				if (InputOutputValues[i].TimeValue.minute < 10)
					sprintf(SQLStmt,"%s0%d:",SQLStmt,InputOutputValues[i].TimeValue.minute);
				else
					sprintf(SQLStmt,"%s%d:",SQLStmt,InputOutputValues[i].TimeValue.minute);
				if (InputOutputValues[i].TimeValue.second < 10)
					sprintf(SQLStmt,"%s0%d'},",SQLStmt,InputOutputValues[i].TimeValue.second);
				else
					sprintf(SQLStmt,"%s%d'},",SQLStmt,InputOutputValues[i].TimeValue.second);

				sprintf(SQLStmt,"%s {ts '%d-",SQLStmt,InputOutputValues[i].TimestampValue.year);
				if (InputOutputValues[i].TimestampValue.month < 10)
					sprintf(SQLStmt,"%s0%d-",SQLStmt,InputOutputValues[i].TimestampValue.month);
				else
					sprintf(SQLStmt,"%s%d-",SQLStmt,InputOutputValues[i].TimestampValue.month);
				if (InputOutputValues[i].TimestampValue.day < 10)
					sprintf(SQLStmt,"%s0%d",SQLStmt,InputOutputValues[i].TimestampValue.day);
				else
					sprintf(SQLStmt,"%s%d",SQLStmt,InputOutputValues[i].TimestampValue.day);
				if (InputOutputValues[i].TimestampValue.hour < 10)
					sprintf(SQLStmt,"%s 0%d:",SQLStmt,InputOutputValues[i].TimestampValue.hour);
				else
					sprintf(SQLStmt,"%s %d:",SQLStmt,InputOutputValues[i].TimestampValue.hour);
				if (InputOutputValues[i].TimestampValue.minute < 10)
					sprintf(SQLStmt,"%s0%d:",SQLStmt,InputOutputValues[i].TimestampValue.minute);
				else
					sprintf(SQLStmt,"%s%d:",SQLStmt,InputOutputValues[i].TimestampValue.minute);
				if (InputOutputValues[i].TimestampValue.second < 10)
					sprintf(SQLStmt,"%s0%d",SQLStmt,InputOutputValues[i].TimestampValue.second);
				else
					sprintf(SQLStmt,"%s%d",SQLStmt,InputOutputValues[i].TimestampValue.second);
				if (InputOutputValues[i].TimestampValue.fraction == 0)
					sprintf(SQLStmt,"%s'},",SQLStmt);
				else
					sprintf(SQLStmt,"%s.%d'},",SQLStmt,InputOutputValues[i].TimestampValue.fraction);
				sprintf(SQLStmt,"%s %s",SQLStmt,InputOutputValues[i].BigintValue);
				strcat(SQLStmt,")");
				break;
			case SELECT_MULTIPLE_TABLE:
				sprintf(SQLStmt,"select ");
				i = 0;
				while (strcmp(ColumnInfo[i].DataTypestr,END_LOOP) != 0)
				{
					if ((i != 0) && (strcmp(ColumnInfo[i].DataTypestr,END_LOOP) != 0))
						strcat(SQLStmt,",");
					j = RandomValue(Total_Number_Of_Tables-1);
					strcat(SQLStmt,pTestInfo->Table[j]);
					SelTableUsed[j] = TRUE;
					strcat(SQLStmt,".");
					strcat(SQLStmt,ColumnInfo[i].Name);
					i++;
					//Sleep(500);
				}
				strcat(SQLStmt," from ");
				j = 0;
				for (i = 0; i < Total_Number_Of_Tables; i++)
				{
					if (SelTableUsed[i] == TRUE)
					{
						if ((j != 0) && (j != (Total_Number_Of_Tables-1)))
							strcat(SQLStmt,",");
							strcat(SQLStmt,pTestInfo->Table[i]);
						j++;
					}
				}
				break;
			case SELECT_TABLE:
				sprintf(SQLStmt,"select ");
				i = 0;
				while (strcmp(ColumnInfo[i].DataTypestr,END_LOOP) != 0)
				{
					if ((i != 0) && (strcmp(ColumnInfo[i].DataTypestr,END_LOOP) != 0))
						strcat(SQLStmt,",");
					strcat(SQLStmt,ColumnInfo[i].Name);
					i++;
				}
				strcat(SQLStmt," from ");
				strcat(SQLStmt,ObjName);
				break;
			case UPDATE_TABLE_PARAMS:
				temp = new char[50];
				sprintf(SQLStmt,"update %s set ",ObjName);
				i = 0;
				while (strcmp(ColumnInfo[i].DataTypestr,END_LOOP) != 0)
				{
					if (ColumnInfo[i].PriKey != TRUE)
					{
						if ((i != 0) && (strcmp(ColumnInfo[i].DataTypestr,END_LOOP) != 0))
							strcat(SQLStmt,",");
						strcat(SQLStmt,ColumnInfo[i].Name);
						strcat(SQLStmt," = ?");
					}
					i++;
				}
				strcat(SQLStmt," where ");
				strcat(SQLStmt,ColumnInfo[5].Name);
				strcat(SQLStmt," = ");
				sprintf(temp,"%d",SetValue);
				strcat(SQLStmt, temp);
				delete temp;
				temp = NULL;
				break;
			case UPDATE_TABLE_VALUES:
				temp = new char[50];
				sprintf(SQLStmt,"update %s set ",ObjName);
				if (SetValue != 0)
					i = RandomValue(Total_Num_Rows);
				else
					i = 1; // update first row
				sprintf(SQLStmt,"%s %s = '%s',",SQLStmt,ColumnInfo[0].Name,InputOutputValues[i].CharValue);
				sprintf(SQLStmt,"%s %s = '%s',",SQLStmt,ColumnInfo[1].Name,InputOutputValues[i].VarCharValue);
				sprintf(SQLStmt,"%s %s = %s,",SQLStmt,ColumnInfo[2].Name,InputOutputValues[i].DecimalValue);
				sprintf(SQLStmt,"%s %s = %s,",SQLStmt,ColumnInfo[3].Name,InputOutputValues[i].NumericValue);
				sprintf(SQLStmt,"%s %s = %d,",SQLStmt,ColumnInfo[4].Name,InputOutputValues[i].ShortValue);
				sprintf(SQLStmt,"%s %s = %f,",SQLStmt,ColumnInfo[6].Name,InputOutputValues[i].RealValue);
				sprintf(SQLStmt,"%s %s = %e,",SQLStmt,ColumnInfo[7].Name,InputOutputValues[i].FloatValue);
				sprintf(SQLStmt,"%s %s = %e,",SQLStmt,ColumnInfo[8].Name,InputOutputValues[i].DoubleValue);

				sprintf(SQLStmt,"%s %s = {d '%d-",SQLStmt,ColumnInfo[9].Name,InputOutputValues[i].DateValue.year);
				if (InputOutputValues[i].DateValue.month < 10)
					sprintf(SQLStmt,"%s0%d-",SQLStmt,InputOutputValues[i].DateValue.month);
				else
					sprintf(SQLStmt,"%s%d-",SQLStmt,InputOutputValues[i].DateValue.month);
				if (InputOutputValues[i].DateValue.day < 10)
					sprintf(SQLStmt,"%s0%d'},",SQLStmt,InputOutputValues[i].DateValue.day);
				else
					sprintf(SQLStmt,"%s%d'},",SQLStmt,InputOutputValues[i].DateValue.day);

				if (InputOutputValues[i].TimeValue.hour < 10)
					sprintf(SQLStmt,"%s %s = {t '0%d:",SQLStmt,ColumnInfo[10].Name,InputOutputValues[i].TimeValue.hour);
				else
					sprintf(SQLStmt,"%s %s = {t '%d:",SQLStmt,ColumnInfo[10].Name,InputOutputValues[i].TimeValue.hour);
				if (InputOutputValues[i].TimeValue.minute < 10)
					sprintf(SQLStmt,"%s0%d:",SQLStmt,InputOutputValues[i].TimeValue.minute);
				else
					sprintf(SQLStmt,"%s%d:",SQLStmt,InputOutputValues[i].TimeValue.minute);
				if (InputOutputValues[i].TimeValue.second < 10)
					sprintf(SQLStmt,"%s0%d'},",SQLStmt,InputOutputValues[i].TimeValue.second);
				else
					sprintf(SQLStmt,"%s%d'},",SQLStmt,InputOutputValues[i].TimeValue.second);

				sprintf(SQLStmt,"%s %s = {ts '%d-",SQLStmt,ColumnInfo[11].Name,InputOutputValues[i].TimestampValue.year);
				if (InputOutputValues[i].TimestampValue.month < 10)
					sprintf(SQLStmt,"%s0%d-",SQLStmt,InputOutputValues[i].TimestampValue.month);
				else
					sprintf(SQLStmt,"%s%d-",SQLStmt,InputOutputValues[i].TimestampValue.month);
				if (InputOutputValues[i].TimestampValue.day < 10)
					sprintf(SQLStmt,"%s0%d",SQLStmt,InputOutputValues[i].TimestampValue.day);
				else
					sprintf(SQLStmt,"%s%d",SQLStmt,InputOutputValues[i].TimestampValue.day);
				if (InputOutputValues[i].TimestampValue.hour < 10)
					sprintf(SQLStmt,"%s 0%d:",SQLStmt,InputOutputValues[i].TimestampValue.hour);
				else
					sprintf(SQLStmt,"%s %d:",SQLStmt,InputOutputValues[i].TimestampValue.hour);
				if (InputOutputValues[i].TimestampValue.minute < 10)
					sprintf(SQLStmt,"%s0%d:",SQLStmt,InputOutputValues[i].TimestampValue.minute);
				else
					sprintf(SQLStmt,"%s%d:",SQLStmt,InputOutputValues[i].TimestampValue.minute);
				if (InputOutputValues[i].TimestampValue.second < 10)
					sprintf(SQLStmt,"%s0%d",SQLStmt,InputOutputValues[i].TimestampValue.second);
				else
					sprintf(SQLStmt,"%s%d",SQLStmt,InputOutputValues[i].TimestampValue.second);
				if (InputOutputValues[i].TimestampValue.fraction == 0)
					sprintf(SQLStmt,"%s'},",SQLStmt);
				else
					sprintf(SQLStmt,"%s.%d'},",SQLStmt,InputOutputValues[i].TimestampValue.fraction);

				sprintf(SQLStmt,"%s %s = %s",SQLStmt,ColumnInfo[12].Name,InputOutputValues[i].BigintValue);
				strcat(SQLStmt," where ");
				strcat(SQLStmt,ColumnInfo[5].Name);
				strcat(SQLStmt," = ");
				sprintf(temp,"%d",SetValue);
				strcat(SQLStmt, temp);
				delete temp;
				temp = NULL;
				break;
			case DELETE_TABLE_PARAMS:
				sprintf(SQLStmt,"delete from %s where %s = %d",ObjName,ColumnInfo[5].Name,SetValue);
				break;
			case DELETE_TABLE_VALUES:
				sprintf(SQLStmt,"delete from %s where %s = %d",ObjName,ColumnInfo[5].Name,SetValue);
				break;
			default :
				break;
		}
		sprintf(msgtxt,"SQL Statement: %s.\n",SQLStmt); 
		WriteToLog(msgtxt);
		return (SQLStmt);
	}

	void ReleaseAll(TestInfo *pTestInfo)
	{
		SQLFreeStmt(pTestInfo->hstmt,/* SQL_DROP */ SQL_CLOSE);
		SQLDisconnect(pTestInfo->hdbc);
		SQLFreeConnect(pTestInfo->hdbc);
		SQLFreeEnv(pTestInfo->henv);
		pTestInfo->hstmt = NULL;
		pTestInfo->hdbc = NULL;
		pTestInfo->henv = NULL;
	}

	public:
		odbcCommon()
		{
			pTestInfo	= new TestInfo;
			pTestInfo->henv = (HENV) NULL;
			pTestInfo->hstmt = (HSTMT) NULL;
			pTestInfo->hdbc = (HDBC) NULL;
			for (m = 0; m < Total_Number_Of_Tables; m++)
			{
				pTestInfo->Table[m] = new char[SQL_MAX_DB_NAME_LEN];
			}
			while (strcmp(InputOutputValues[Total_Num_Rows].CharValue,END_LOOP) != 0)
			{ 
				Total_Num_Rows++;
			}

		}

		BOOL FullConnect(TestInfo *pTestInfo, char *cs, int *errOK);
		INT DDLClient(TestInfo *pTestInfo);
		INT DMLClient(TestInfo *pTestInfo);
		BOOL GetAllInfo(TestInfo *pTestInfo);
		BOOL FullDisconnect(TestInfo *pTestInfo);
		BOOL FindError(char *FindMsg, TestInfo *pTestInfo);
		BOOL FindError(SDWORD FindMsg, TestInfo *pTestInfo);
		BOOL FindMultipleErrors(const char *FindMsg1, const char *FindMsg2, const char *FindMsg3, TestInfo *pTestInfo);
	       void stripInfo(char* ConnectString);

		FILE *LogOpen(void)
		{
			FILE *LogFilePtr;
			int i;

			i=0;
			LogFilePtr=fopen(logfile,"a");
			while((LogFilePtr == NULL) && (i < 3))
			{
				LogFilePtr=fopen(logfile,"a");
				i++;
			}
			// if our logfile can't be opened then just return a NULL pointer
			// otherwise return the log file pointer
			return(LogFilePtr);
		}
		void MainWrite(const char *logstr)
		{
			WriteToLog(logstr);
		}
		~odbcCommon()
		{
			for (m = 0; m < Total_Number_Of_Tables; m++)
			{
				delete pTestInfo->Table[m];
			}
			delete pTestInfo;
			pTestInfo = NULL;
		}
};


BOOL odbcCommon :: FindError(SDWORD FindMsg, TestInfo *pTestInfo)
{                 
	char			buf[MAX_SQLSTRING_LEN];
	RETCODE		returncode;
	char			State[STATE_SIZE];
	SDWORD		NativeError;
	BOOL			found;
	BOOL			MsgDisplayed;

	found = FALSE;
	MsgDisplayed=FALSE;

	// Log any henv error messages 
	returncode = SQLError(pTestInfo->henv, NULL, NULL, (UCHAR *)State, &NativeError, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
	while((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
	{
		State[STATE_SIZE-1]=NULL_STRING;
		// scan henv, hdbc, and hstmt for errors of the specified state 
		MsgDisplayed=TRUE;
		if (-FindMsg == NativeError)
		{
			found = TRUE;
		}
		else
		{
			found = FALSE;
			sprintf(msgtxt,"ERR>> ENV: %s, NE: %ld, MSG: %s.",State,NativeError,buf);
			WriteToLog(msgtxt);
		}
		returncode = SQLError(pTestInfo->henv, NULL, NULL, (UCHAR *)State, &NativeError, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
	}

	 /* Log any hdbc error messages */
	returncode = SQLError(NULL, pTestInfo->hdbc, NULL, (UCHAR *)State, &NativeError, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
	while((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
	{
		State[STATE_SIZE-1]=NULL_STRING;
		MsgDisplayed=TRUE;
		// scan henv, hdbc, and hstmt for errors of the specified state 
		if (-FindMsg == NativeError)
		{
			found = TRUE;
		}
		else
		{
			found = FALSE;
			sprintf(msgtxt,"ERR>> HDBC: %s, NE: %ld, MSG: %s.",State,NativeError,buf);
			WriteToLog(msgtxt);
		}
		returncode = SQLError(NULL, pTestInfo->hdbc, NULL, (UCHAR *)State, &NativeError, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
	}

	 /* Log any hstmt error messages */
	returncode = SQLError(NULL, NULL, pTestInfo->hstmt, (UCHAR *)State, &NativeError, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
	while((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
	{
		State[STATE_SIZE-1]=NULL_STRING;
		MsgDisplayed=TRUE;
		// scan henv, hdbc, and hstmt for errors of the specified state 
		if (-FindMsg == NativeError)
		{
			found = TRUE;
		}
		else
		{
			found = FALSE;
			sprintf(msgtxt,"ERR>> STMT: %s, NE: %ld, MSG: %s.",State,NativeError,buf);
			WriteToLog(msgtxt);
		}
		returncode = SQLError(NULL, NULL, pTestInfo->hstmt, (UCHAR *)State, &NativeError, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
	}
	if (!found)
	{
		sprintf(msgtxt,"\n");
		WriteToLog(msgtxt);
	}

	/* if no error messages were displayed then display a message */
	if(!MsgDisplayed)
	{
		sprintf(msgtxt,"There were no error messages for SQLError() to display.\n");
		WriteToLog(msgtxt);
	}
	return (found);
}       

BOOL odbcCommon :: FindError(char *FindMsg, TestInfo *pTestInfo)
{                 
	char		buf[MAX_SQLSTRING_LEN];
	RETCODE		returncode;
	char		State[STATE_SIZE];
	SDWORD		NativeError;
	BOOL		found;
	BOOL		MsgDisplayed;

	found = FALSE;
	MsgDisplayed=FALSE;

	// Log any henv error messages 
	if (pTestInfo->henv != NULL)
	{
		returncode = SQLError(pTestInfo->henv, NULL, NULL, (UCHAR *)State, &NativeError, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
		while((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			State[STATE_SIZE-1]=NULL_STRING;
			// scan henv, hdbc, and hstmt for errors of the specified state 
			MsgDisplayed=TRUE;
			if (strstr(buf, FindMsg) != NULL)
			{
				found = TRUE;
			}
			else
			{
				found = FALSE;
				sprintf(msgtxt,"ERR>> ENV: %s, NE: %ld, MSG: %s.",State,NativeError,buf);
				WriteToLog(msgtxt);
			}
			returncode = SQLError(pTestInfo->henv, NULL, NULL, (UCHAR *)State, &NativeError, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
		}
	}

	 /* Log any hdbc error messages */
	if (pTestInfo->hdbc != NULL)
	{
		returncode = SQLError(NULL, pTestInfo->hdbc, NULL, (UCHAR *)State, &NativeError, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
		while((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			State[STATE_SIZE-1]=NULL_STRING;
			MsgDisplayed=TRUE;
			// scan henv, hdbc, and hstmt for errors of the specified state 
			if (strstr(buf, FindMsg) != NULL)
			{
				found = TRUE;
			}
			else
			{
				found = FALSE;
				sprintf(msgtxt,"ERR>> HDBC: %s, NE: %ld, MSG: %s.",State,NativeError,buf);
				WriteToLog(msgtxt);
			}
			returncode = SQLError(NULL, pTestInfo->hdbc, NULL, (UCHAR *)State, &NativeError, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
		}
	}

	 /* Log any hstmt error messages */
	if (pTestInfo->hstmt != NULL)
	{
		returncode = SQLError(NULL, NULL, pTestInfo->hstmt, (UCHAR *)State, &NativeError, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
		while((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			State[STATE_SIZE-1]=NULL_STRING;
			MsgDisplayed=TRUE;
			// scan henv, hdbc, and hstmt for errors of the specified state 
			if (strstr(buf, FindMsg) != NULL)
			{
				found = TRUE;
			}
			else
			{
				found = FALSE;
				sprintf(msgtxt,"ERR>> STMT: %s, NE: %ld, MSG: %s.",State,NativeError,buf);
				WriteToLog(msgtxt);
			}
			returncode = SQLError(NULL, NULL, pTestInfo->hstmt, (UCHAR *)State, &NativeError, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
		}
	}
	if (!found)
	{
		sprintf(msgtxt,"\n");
		WriteToLog(msgtxt);
	}

	/* if no error messages were displayed then display a message */
	if(!MsgDisplayed)
	{
		sprintf(msgtxt,"There were no error messages for SQLError() to display.\n");
		WriteToLog(msgtxt);
	}
	return (found);
}    

BOOL odbcCommon :: FindMultipleErrors(const char *FindMsg1, const char *FindMsg2, const char *FindMsg3, TestInfo *pTestInfo)
{                 
	char		buf[MAX_SQLSTRING_LEN];
	RETCODE		returncode;
	char		State[STATE_SIZE];
	SDWORD		NativeError;
	BOOL		found;
	BOOL		MsgDisplayed;

	found = FALSE;
	MsgDisplayed=FALSE;
	
	// Log any henv error messages 
	if (pTestInfo->henv != NULL)
	{
		returncode = SQLError(pTestInfo->henv, NULL, NULL, (UCHAR *)State, &NativeError, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
		while((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			State[STATE_SIZE-1]=NULL_STRING;
			// scan henv, hdbc, and hstmt for errors of the specified state 
			MsgDisplayed=TRUE;
			if ((strstr(buf, FindMsg1) != NULL) || (strstr(buf, FindMsg2) != NULL) || (strstr(buf, FindMsg3) != NULL))
			{
				found = TRUE;
			}
			else
			{
				found = FALSE;
				sprintf(msgtxt,"ERR>> ENV: %s, NE: %ld, MSG: %s.",State,NativeError,buf);
				WriteToLog(msgtxt);
			}
			returncode = SQLError(pTestInfo->henv, NULL, NULL, (UCHAR *)State, &NativeError, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
		}
	}

	 /* Log any hdbc error messages */
	if (pTestInfo->hdbc != NULL)
	{
		returncode = SQLError(NULL, pTestInfo->hdbc, NULL, (UCHAR *)State, &NativeError, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
		while((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			State[STATE_SIZE-1]=NULL_STRING;
			MsgDisplayed=TRUE;
			// scan henv, hdbc, and hstmt for errors of the specified state 
			if ((strstr(buf, FindMsg1) != NULL) || (strstr(buf, FindMsg2) != NULL) || (strstr(buf, FindMsg3) != NULL))
			{
				found = TRUE;
			}
			else
			{
				found = FALSE;
				sprintf(msgtxt,"ERR>> HDBC: %s, NE: %ld, MSG: %s.",State,NativeError,buf);
				WriteToLog(msgtxt);
			}
			returncode = SQLError(NULL, pTestInfo->hdbc, NULL, (UCHAR *)State, &NativeError, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
		}
	}

	 /* Log any hstmt error messages */
	if (pTestInfo->hstmt != NULL)
	{
		returncode = SQLError(NULL, NULL, pTestInfo->hstmt, (UCHAR *)State, &NativeError, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
		while((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			State[STATE_SIZE-1]=NULL_STRING;
			MsgDisplayed=TRUE;
			// scan henv, hdbc, and hstmt for errors of the specified state 
			if ((strstr(buf, FindMsg1) != NULL) || (strstr(buf, FindMsg2) != NULL) || (strstr(buf, FindMsg3) != NULL))
			{
				found = TRUE;
			}
			else
			{
				found = FALSE;
				sprintf(msgtxt,"ERR>> STMT: %s, NE: %ld, MSG: %s.",State,NativeError,buf);
				WriteToLog(msgtxt);
			}
			returncode = SQLError(NULL, NULL, pTestInfo->hstmt, (UCHAR *)State, &NativeError, (UCHAR *)buf, MAX_SQLSTRING_LEN, NULL);
		}
	}
	if (!found)
	{
		sprintf(msgtxt,"\n");
		WriteToLog(msgtxt);
	}

	/* if no error messages were displayed then display a message */
	if(!MsgDisplayed)
	{
		sprintf(msgtxt,"There were no error messages for SQLError() to display.\n");
		WriteToLog(msgtxt);
	}
	return (found);
}  

BOOL odbcCommon :: FullConnect(TestInfo *pTestInfo, char *cs, int *errOK=0) {

	RETCODE returncode;
	char	ConnectString[MAX_CONNECT_STRING];
	short	ConnStrLength;
#ifdef __linux
	void *  Myhwnd;
#else
	HWND	Myhwnd;
#endif
	HENV	henv;
	HDBC	hdbc;
	HSTMT	hstmt;

#ifdef __linux
#else
	Myhwnd = GetTopWindow((HWND)NULL);
#endif

	/* init the variable */
	if (errOK)
	  *errOK = 0;

    	WriteToLog("FullConnect function, Before SQLAllocEnv call. \n");
	returncode = SQLAllocEnv(&henv);
//	if (returncode != SQL_SUCCESS)
	if (!SQL_SUCCEEDED(returncode))
	{
		WriteToLog("Unable to Allocate Envirnoment.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	WriteToLog("FullConnect function, Before SQLAllocConnect call. \n");
	returncode = SQLAllocConnect(henv,&hdbc);
//	if (returncode != SQL_SUCCESS)
	if (!SQL_SUCCEEDED(returncode))
	{
		WriteToLog("Unable to Allocate Connect.\n");
		pTestInfo->henv = henv;
		LogAllErrors(pTestInfo);		
		SQLFreeEnv(henv);
		henv = NULL;
		return(FALSE);
	}
	
	WriteToLog("FullConnect function, Before SQLDriverConnect call. \n");
	returncode = SQLDriverConnect(hdbc,Myhwnd,(UCHAR*)cs,SQL_NTS,
                                 (UCHAR*)ConnectString,300,&ConnStrLength,
                                 SQL_DRIVER_NOPROMPT);
//	if ((returncode != SQL_SUCCESS) && (returncode != SQL_SUCCESS_WITH_INFO))
	if (!SQL_SUCCEEDED(returncode))
	{
		printf ("DriverConnect failed, return value is %d", returncode);
		SQLINTEGER native;
            	SQLCHAR state[6], text[SQL_MAX_MESSAGE_LENGTH];
          	SQLRETURN diagRc;
          	diagRc = SQLGetDiagRec(SQL_HANDLE_DBC, 
                                  hdbc, 1, state, &native, text,
                                  sizeof(text), NULL);
          	/* When there are too many connections, the target machine
           	 * may start to run out of resource. Some tests may want to
           	 * tolerant this error.
           	 */
          	if (errOK && (diagRc == SQL_SUCCESS || diagRc == SQL_SUCCESS_WITH_INFO) && strstr((char *) text, "error text:Too many open files."))
		  *errOK = 1;
		  
		WriteToLog("Unable to Connect.\n");
		pTestInfo->henv = henv;
		pTestInfo->hdbc = hdbc;
		LogAllErrors(pTestInfo);		
		SQLFreeConnect(hdbc);
		SQLFreeEnv(henv);
		hdbc = NULL;
		henv = NULL;
		return(FALSE);
	}
	
	puts ("AFTER DriverConnect");
	WriteToLog("FullConnect function, Before SQLAllocStmt call. \n");
	returncode = SQLAllocStmt(hdbc,&hstmt);
//	if (returncode != SQL_SUCCESS)
	if (!SQL_SUCCEEDED(returncode))
	{
		WriteToLog("Unable to Allocate Statement.\n");
		pTestInfo->henv = henv;
		pTestInfo->hdbc = hdbc;
		LogAllErrors(pTestInfo);		
		SQLDisconnect(hdbc);
		SQLFreeConnect(hdbc);
		SQLFreeEnv(henv);
		hdbc = NULL;
		henv = NULL;
		return(FALSE);
	}

   stripInfo(ConnectString);
      
   // send the current handles to the caller 
   pTestInfo->henv = henv;
   pTestInfo->hdbc = hdbc;
   pTestInfo->hstmt = hstmt;
   
   WriteToLog("FullConnect function, Before returning from FullConnect function. \n");
   return(TRUE);
}

//#####################################################################################################
// This functions is used to strip info from connection string
//#####################################################################################################
void odbcCommon :: stripInfo(char* ConnectString) {

    int     m;
    char	*pString;
	char	*pTempString;
	char	TempString[MAX_CONNECT_STRING];

    // Strip out DSN from connection string. 
	pString = strstr(ConnectString,"DSN=");
	pString += 4;           // skip past 'DSN=' 
	pTempString = TempString;
	while(*pString != ';')
	{
		*pTempString = *pString;
		pTempString++;
		pString++;
	}         
	*pTempString = (char)NULL;
	strcpy(pTestInfo->DataSource,TempString);

	// Strip out UID from connection string. 
	pString = strstr(ConnectString,"UID=");
	if (pString != NULL)
	{
		pString += 4;           // skip past 'UID=' 
		pTempString = TempString;
		while(*pString != ';')
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
	pString = strstr(ConnectString,"PWD=");
	if (pString != NULL)
	{
		pString += 4;           // skip past 'PWD=' 
		pTempString = TempString;
		while(*pString != ';')
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
	pString = strstr(ConnectString,"DBQ=");
	if (pString != NULL)
	{
		pString += 4;           // skip past 'DBQ=' 
		pTempString = TempString;
		while(*pString != ';')
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
	pString = strstr(ConnectString,"CATALOG=");
	if (pString != NULL)
	{
		pString += 8;           // skip past 'CATALOG=' 
		pTempString = TempString;
		while(*pString != ';')
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
	pString = strstr(ConnectString,"SCHEMA=");
	if (pString != NULL)
	{
		pString += 7;           // skip past 'SCHEMA=' 
		pTempString = TempString;
		while(*pString != ';')
		{
			*pTempString = *pString;
			pTempString++;
			pString++;
		}         
		*pTempString = (char)NULL;
		strcpy((char *)pTestInfo->Schema,TempString);
	}
	else
		strcpy((char *)pTestInfo->Schema,"ODBC_SCHEMA");

	for (m = 0; m < Total_Number_Of_Tables; m++)
	{
		char tmpbuf[21];
		time_t ltime;
		time( &ltime );
		sprintf(tmpbuf, "%ld", ltime);

		strcpy((char *)pTestInfo->Table[m],tablenamesused[m]);
		strcat((char *)pTestInfo->Table[m],tmpbuf);

	}
}

//#####################################################################################################
// This functions cover the following APIs:
// SQLDisconnect
// SQLFreeConnect
// SQLFreeEnv
//#####################################################################################################
BOOL odbcCommon :: FullDisconnect(TestInfo *pTestInfo)
{
  RETCODE returncode;                        
   
  WriteToLog("FullDisconnect function, Before SQLFreeStmt for hstmt. \n");
  returncode = SQLFreeStmt(pTestInfo->hstmt,/* SQL_DROP */ SQL_CLOSE);
//	if (returncode != SQL_SUCCESS)
	if (!SQL_SUCCEEDED(returncode))
	{
		// WriteToLog("Disconnect: Unable to FreeStmt with DROP.\n");
		WriteToLog("Disconnect: Unable to FreeStmt with SQL_CLOSE.\n");
		SQLDisconnect(pTestInfo->hdbc);
		SQLFreeConnect(pTestInfo->hdbc);
		SQLFreeEnv(pTestInfo->henv);
		pTestInfo->hdbc = NULL;
		pTestInfo->henv = NULL;
		return(FALSE);
	}

  WriteToLog("FullDisconnect function, Before SQLDisconnect. \n");
  returncode = SQLDisconnect(pTestInfo->hdbc);
	if (returncode != SQL_SUCCESS && returncode != SQL_SUCCESS_WITH_INFO)
	{
		WriteToLog("Disconnect: Unable to Disconnect.\n");
		LogAllErrors(pTestInfo);
		SQLDisconnect(pTestInfo->hdbc);
		SQLFreeConnect(pTestInfo->hdbc);
		SQLFreeEnv(pTestInfo->henv);
		pTestInfo->hdbc = NULL;
		pTestInfo->henv = NULL;
		return(FALSE);
	}
   
  WriteToLog("FullDisconnect function, Before SQLFreeConnect. \n");
  returncode = SQLFreeConnect(pTestInfo->hdbc);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("FreeConnect: Unable to FreeConnect.\n");
		SQLDisconnect(pTestInfo->hdbc);
		SQLFreeConnect(pTestInfo->hdbc);
		SQLFreeEnv(pTestInfo->henv);
		pTestInfo->hdbc = NULL;
		pTestInfo->henv = NULL;
		return(FALSE);
	}

   
  WriteToLog("FullDisconnect function, Before SQLFreeEnv. \n");
  returncode = SQLFreeEnv(pTestInfo->henv);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("FreeEnv: Unable to FreeEnvirnoment.\n");
		SQLDisconnect(pTestInfo->hdbc);
		SQLFreeConnect(pTestInfo->hdbc);
		SQLFreeEnv(pTestInfo->henv);
		pTestInfo->hdbc = NULL;
		pTestInfo->henv = NULL;
		return(FALSE);
	}
   
  WriteToLog("Before returning from FullDisconnect function. \n");
  return(TRUE);
}

//#####################################################################################################
// This functions cover the following APIs:
// SQLDatasources
// SQLDrivers
// SQLGetInfo
//#####################################################################################################
BOOL odbcCommon :: GetAllInfo(TestInfo *pTestInfo)
{
  RETCODE returncode;                        
	UCHAR		szDSN[SQL_MAX_DSN_LENGTH], szDESC[SQL_MAX_DSN_LENGTH];
	SWORD		cbDSN, pcbDESC;
	UCHAR		szDRVDESC[SQL_MAX_DRIVER_LENGTH], szDRVATTR[SQL_MAX_DRIVER_LENGTH];
	SWORD		cbDRVDESC, pcbDRVATTR;
	PTR			fFuncs;

	returncode = SQLDataSources(pTestInfo->henv, SQL_FETCH_FIRST, szDSN, SQL_MAX_DSN_LENGTH, &cbDSN, szDESC, SQL_MAX_DSN_LENGTH, &pcbDESC); 
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("DataSources: Unable to Fetch first datasource.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	returncode = SQLDrivers(pTestInfo->henv, SQL_FETCH_FIRST, szDRVDESC, SQL_MAX_DRIVER_LENGTH, &cbDRVDESC, szDRVATTR, SQL_MAX_DRIVER_LENGTH, &pcbDRVATTR); 
//	if (returncode != SQL_SUCCESS)
	if (!SQL_SUCCEEDED(returncode))
	{
		WriteToLog("Drivers: Unable to Fetch first driver.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	fFuncs = new char[SQL_MAX_DSN_LENGTH];
	returncode = SQLGetInfo(pTestInfo->hdbc, SQL_DATA_SOURCE_NAME, fFuncs, SQL_MAX_DSN_LENGTH, NULL);
//	if (returncode != SQL_SUCCESS)
	if (!SQL_SUCCEEDED(returncode))
	{
		WriteToLog("GetInfo: Unable to get active connections.\n");
	}
	if (strcmp((char *)fFuncs,pTestInfo->DataSource) != 0)
	{
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	delete fFuncs;

	return(TRUE);

}

INT odbcCommon :: DDLClient(TestInfo *pTestInfo)
{   
 	RETCODE		returncode;
	char			Heading[MAX_SQLSTRING_LEN];
	time_t		starttime, endtime;
	struct
	{
		const char		*TableColdatatype;
		const char		*TableScale[DLL_CLIENT_TABLES];
		const char		*TableColVal[DLL_CLIENT_TABLES];
	}	TableType[] = {
// Neelam - since default for char allows only 8 characters.
//							{"CHAR","(1)","(30)","(100)","(199)","(254)","'d'","'char'","'default char_1'","'default char123456'","'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'"},
//							{"VARCHAR","(1)","(30)","(100)","(199)","(254)","'d'","'varchar'","'default varchar_1'","'default varchar123456'","'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'"},
							{"CHAR","(1)","(30)","(100)","(199)","(254)","'d'","'char'","'defaultc'","'default4'","'Zavwx240'"},
							{"VARCHAR","(1)","(30)","(100)","(199)","(254)","'d'","'varchar'","'defaut_1'","'dvarchar'","'ABCDEFGH'"},
							{"DECIMAL","(1,0)","(1,1)","(5,2)","(10,5)","(15,15)","1","0.2","999.22","4562.234","0.123456"},
							{"NUMERIC","(1,0)","(1,1)","(5,2)","(10,5)","(15,15)","1","0.2","999.22","4562.234","0.123456"},
							{"SMALLINT","","","","","","1","11","500","1234","9999",},
							{"INTEGER","","","","","","1","23","666","3333","12345",},
							{"REAL","","","","","","1","88","10.32","321E02","7777.99",},
							{"FLOAT","","","","","","1","88","10.32","321E02","7777.99",},
							{"DOUBLE PRECISION","","","","","","1","88","10.32","321E02","7777.99",},
// Neelam - changed the format for specifying default for date, time and timestamp.
//							{"DATE","","","","","","{d '1997-09-30'}","{d '1995-11-30'}","{d '2000-01-01'}","{d '1997-01-01'}","{d '1999-12-12'}"},
//							{"TIME","","","","","","{t '00:01:00'}","{t '01:05:45'}","{t '13:05:45'}","{t '11:05:45'}","{t '23:59:59'}"},
//							{"TIMESTAMP","","","","","","{ts '1997-09-30 00:01:00'}","{ts '1995-11-30 01:05:45.000000'}","{ts '2000-01-01 13:05:45.301'}","{ts '1997-01-01 11:05:45.34'}","{ts '1999-12-12 23:59:59.123456'}"},
							{"DATE","","","","","","date '2004-01-05'","date '1995-11-30'","date '2000-01-01'","date '1997-01-01'","date '1999-12-12'"},
							{"TIME","","","","","","time '01:05:45'","time '01:05:45'","time '13:05:45'","time '11:05:45'","time '23:59:59'"},
							{"TIMESTAMP","","","","","","timestamp '2004-01-05:01:05:45.000000'","timestamp '1995-11-30:01:05:45.000000'","timestamp '2000-01-01:13:05:45.301000'","timestamp '1997-01-01:11:05:45.340000'","timestamp '1999-12-12:23:59:59.123456'"},
							{"endloop",}};
	struct
	{
		const char		*BaseTableName;
		const char		*ColumnConDefn;
		const char		*TableConDefn;
		const char		*DefaultVal;
	} TableConfig[] = {											// need to add check & reference
							{"Y","","","",},
							{"zyx","DEFAULT","",""},
							{"XYZ123","NOT NULL","","",},
						//	{"XYZzyx","NOT NULL UNIQUE","","",},
							{"XYZzyx","NOT NULL","","",},
						//	{"XYZzyx123","NOT NULL PRIMARY KEY","",""},
							{"XxYyZz","DEFAULT","","NOT NULL"},
						//	{"XYZ_xyz","DEFAULT","","NOT NULL UNIQUE"},
						//	{"XYZ_123","DEFAULT","","NOT NULL PRIMARY KEY"},
						//	{"ABCDEFGHIJKLMNOPQRSTUVWXYZ","DEFAULT","UNIQUE","NOT NULL"},
							{"zyxwvutsrqponmlkjihgfedcba","DEFAULT","PRIMARY KEY","NOT NULL"},
						//	{"Z_y_1","NOT NULL","UNIQUE",""},
							{"X1234567890","NOT NULL","PRIMARY KEY",""},
							{"endloop",}};

//	char			*TableColStr;
	char			*TableStr,*tmpstr;
	int				i,j,k;
	int				no_testcase = 1;
	
	returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
//	if (returncode != SQL_SUCCESS)
	if (!SQL_SUCCEEDED(returncode))
	{
		WriteToLog("SetConnectOption: Unable to set access mode to read/write.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_TXN_ISOLATION,SQL_TXN_READ_COMMITTED);
//	if (returncode != SQL_SUCCESS)
	if (!SQL_SUCCEEDED(returncode))
	{
		WriteToLog("SetConnectOption: Unable to set transaction isolation mode to read committed.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

//	TableColStr = (char *)malloc(MAX_NOS_SIZE);
	TableStr = new char[MAX_SQLSTRING_LEN];
	tmpstr = new char[10];
	time(&starttime);
	endtime = starttime;	// intial value
	i = 0;
	while (_stricmp(TableType[i].TableColdatatype,"endloop") != 0)
	{
		j = 0;
		while (_stricmp(TableConfig[j].BaseTableName,"endloop") != 0)
		{
			for (k = 0; k < DLL_CLIENT_TABLES; k++)
			{
				char tmpbuf[21];
				time_t ltime;
				time( &ltime );
				sprintf(tmpbuf, "%ld", ltime);

				sprintf(TableStr,"DROP TABLE %s_%s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber,tmpbuf);
				SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,SQL_NTS);
				sprintf(TableStr,"CREATE TABLE %s_%s_%s_%s (%s%d %s%s %s",TableConfig[j].BaseTableName,ComputerName,ClientNumber,tmpbuf,TableConfig[j].BaseTableName,i+1,TableType[i].TableColdatatype,TableType[i].TableScale[k],TableConfig[j].ColumnConDefn);
				if (_stricmp(TableConfig[j].ColumnConDefn,"DEFAULT") == 0)
				{
					strcat(TableStr," ");
					strcat(TableStr,TableType[i].TableColVal[k]);
				}
				strcat(TableStr," ");
				strcat(TableStr,TableConfig[j].DefaultVal);
				strcat(TableStr," ");
				if (_stricmp(TableConfig[j].TableConDefn,"") != 0)
				{
					strcat(TableStr,",");
					strcat(TableStr,TableConfig[j].TableConDefn);
					strcat(TableStr,"(");
					strcat(TableStr,TableConfig[j].BaseTableName);
					sprintf(tmpstr,"%d",i+1);
					strcat(TableStr,tmpstr);                // appends column name
					strcat(TableStr,")");
					strcat(TableStr,")");
				}
				else
				{
					strcat(TableStr,")");
					strcat (TableStr,"NO PARTITIONS");
				}

				sprintf(Heading,"Creating Table >> %s.\n",TableStr);
#ifdef VERBOSE
				WriteToLog(Heading);
#endif
				returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,strlen(TableStr));
			//	if (returncode != SQL_SUCCESS)
				if (!SQL_SUCCEEDED(returncode))
				{
					sprintf(Heading,"Unable to Create Table.\n");
					WriteToLog(Heading);
					if (FindMultipleErrors("Communication link failure","Communication Link failure","connection closed",pTestInfo))
					{
						WriteToLog("ERR>> *** FATAL ERROR *** Communication link failure.\n");
						LogAllErrors(pTestInfo);
						return (2);
					}
					LogAllErrors(pTestInfo);		
				}
				//Sleep(3000);

				sprintf(TableStr,"DROP TABLE %s_%s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber,tmpbuf);
				sprintf(Heading,"Dropping Table >> %s.\n",TableStr);
#ifdef VERBOSE
				WriteToLog(Heading);
#endif
				returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,strlen(TableStr));
			//	if (returncode != SQL_SUCCESS)
				if (!SQL_SUCCEEDED(returncode))
				{
					sprintf(Heading,"Unable to Drop Table.\n");
					WriteToLog(Heading);
					LogAllErrors(pTestInfo);		
				}
				time(&endtime);
				if (((endtime - starttime)/60) > timeout)
				{
					delete tmpstr;
					delete TableStr;
					return(TRUE);
				}
			}
			j++;
		}
		i++;
	}
	delete tmpstr;
	delete TableStr;
	return(TRUE);
}


INT odbcCommon :: DMLClient(TestInfo *pTestInfo)
{   
 	RETCODE		returncode;
	char		Heading[MAX_SQLSTRING_LEN];
	time_t		starttime, endtime;
	struct
	{
		const char		*TableColdatatype;
		const char		*TableScale;
		const char		*TableColVal;
		const char		*ColVal[DML_CLIENT_COLUMNS];
	}	TableType[] = {
						// Neelam - since default for char allows only 8 characters.
						//	{"CHAR","(254)","'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'","'a'","'ABCDEFGHIJ'","'abcdefghijklmnopqrst'","'ABCDEFGHIJKLMNOPQRST1234567890'","'12345678901234567890abcdefghijABCDEFGHIJabcdefghij'","'abcdefghij 1234567890 abcdefghij KLMNOPQRST 1234567890 1234567890'","'ABCDEFGHIJ_1234567890 abcdefghij KLMNOPQRST 1234567890 1234567890 UVWXYZ'","'ABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890_abcdefghij_KLMNOPQRST 1234567890_1234567890 UVWXYZ'","'ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 '","'ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 '"},
						//	{"VARCHAR","(254)","'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'","'a'","'ABCDEFGHIJ'","'abcdefghijklmnopqrst'","'ABCDEFGHIJKLMNOPQRST1234567890'","'12345678901234567890abcdefghijABCDEFGHIJabcdefghij'","'abcdefghij 1234567890 abcdefghij KLMNOPQRST 1234567890 1234567890'","'ABCDEFGHIJ_1234567890 abcdefghij KLMNOPQRST 1234567890 1234567890 UVWXYZ'","'ABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890_abcdefghij_KLMNOPQRST 1234567890_1234567890 UVWXYZ'","'ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 '","'ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 '"},
							{"CHAR","(254)","'ABxy4590'","'a'","'ABCDEFGHIJ'","'abcdefghijklmnopqrst'","'ABCDEFGHIJKLMNOPQRST1234567890'","'12345678901234567890abcdefghijABCDEFGHIJabcdefghij'","'abcdefghij 1234567890 abcdefghij KLMNOPQRST 1234567890 1234567890'","'ABCDEFGHIJ_1234567890 abcdefghij KLMNOPQRST 1234567890 1234567890 UVWXYZ'","'ABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890_abcdefghij_KLMNOPQRST 1234567890_1234567890 UVWXYZ'","'ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 '","'ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 '"},
							{"VARCHAR","(254)","'XYabd890'","'a'","'ABCDEFGHIJ'","'abcdefghijklmnopqrst'","'ABCDEFGHIJKLMNOPQRST1234567890'","'12345678901234567890abcdefghijABCDEFGHIJabcdefghij'","'abcdefghij 1234567890 abcdefghij KLMNOPQRST 1234567890 1234567890'","'ABCDEFGHIJ_1234567890 abcdefghij KLMNOPQRST 1234567890 1234567890 UVWXYZ'","'ABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890_abcdefghij_KLMNOPQRST 1234567890_1234567890 UVWXYZ'","'ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 '","'ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 ABCDEFGHIJKLMNOPQRSTUVWXYZ _ 1234567890 abcdefghijklmnopqrstuvwxyz _ 1234567890 '"},
							{"DECIMAL","(18,6)","987654.12345","0","1.0","-0.1","1234","-9876.123","0.98765","-44444.231","33333.12345","-987654321.12345","987654321.12345"},
							{"NUMERIC","(18,6)","123456.98765","0","1.0","-0.1","1234","-9876.123","0.98765","-44444.231","33333.12345","-987654321.12345","987654321.12345"},
							{"SMALLINT","","9999","0","-1","123","-456","12345","-67890","54545","-23012","987","-6789"},
							{"INTEGER","","12345","0","-1","123","-456","12345","-67890","54545","-23012","987","-6789"},
							{"REAL","","7777.99","0","1.0","-0.1","1234","-9876.123","0.98765","-44444.231","33333.12345","-987654321.12345","987654321.12345"},
							{"FLOAT","","7777.99","0","1.0","-0.1","1234","-9876.123","0.98765","-44444.231","33333.12345","-987654321.12345","987654321.12345"},
							{"DOUBLE PRECISION","","7777.99","0","1.0","-0.1","1234","-9876.123","0.98765","-44444.231","33333.12345","-987654321.12345","987654321.12345"},
// Neelam - changed the format for specifying default for date, time and timestamp.
//							{"DATE","","{d '1992-01-01'}","{d '1993-02-02'}","{d '1994-03-03'}","{d '1995-04-04'}","{d '1996-05-05'}","{d '1997-08-19'}","{d '1998-10-25'}","{d '1999-12-31'}","{d '2000-01-01'}"},
//							{"TIME","","{t '00:00:01'}","{t '00:01:00'}","{t '01:00:00'}","{t '02:05:00'}","{t '04:03:04'}","{t '12:00:59'}","{t '11:11:11'}","{t '18:33:44'}","{t '22:55:59'}","{t '23:59:59'}"},
//							{"TIMESTAMP","","{ts '1992-01-01 00:00:01'}","{ts '1993-02-02 00:01:00.1'}","{ts '1994-03-03 01:00:00.12'}","{ts '1995-04-04 02:05:00.123'}","{ts '1996-05-05 04:03:04.1234'}","{ts '1997-08-19 12:00:59.12345'}","{ts '1998-10-25 11:11:11.123456'}","{ts '1999-12-31 18:33:44.65432'}","{ts '1999-12-12 22:55:59.654321'}","{ts '2000-01-01 23:59:59.123456'}"},
							{"DATE","","date '1992-01-01'","date '1993-02-02'","date '1994-03-03'","date '1995-04-04'","date '1996-05-05'","date '1997-08-19'","date '1998-10-25'","date '1999-12-31'","date '2000-01-01'"},
							{"TIME","","time '00:00:01'","time '00:01:00'","time '01:00:00'","time '02:05:00'","time '04:03:04'","time '12:00:59'","time '11:11:11'","time '18:33:44'","time '22:55:59'","time '23:59:59'"},
							{"TIMESTAMP","","timestamp '1992-01-01:00:00:01.000000'","timestamp '1993-02-02:00:01:00.100000'","timestamp '1994-03-03:01:00:00.120000'","timestamp '1995-04-04:02:05:00.123000'","timestamp '1996-05-05:04:03:04.123400'","timestamp '1997-08-19:12:00:59.123450'","timestamp '1998-10-25:11:11:11.123456'","timestamp '1999-12-31:18:33:44.654320'","timestamp'1999-12-12:22:55:59.654321'","timestamp '2000-01-01:23:59:59.123456'"},
							{"endloop",}};
	struct
	{
		const char		*BaseTableName;
		const char		*ColumnConDefn;
		const char		*TableConDefn;
		const char		*DefaultVal;
	} TableConfig[] = {											// need to add check & reference
							{"Y","","","",},
							{"zyx","DEFAULT","",""},
							{"XYZ123","NOT NULL","","",},
						//	{"XYZzyx","NOT NULL UNIQUE","","",},
							{"XYZzyx","NOT NULL","","",},
						//	{"XYZzyx123","NOT NULL PRIMARY KEY","",""},
							{"XxYyZz","DEFAULT","","NOT NULL"},
						//	{"XYZ_xyz","DEFAULT","","NOT NULL UNIQUE"},
						//	{"XYZ_123","DEFAULT","","NOT NULL PRIMARY KEY"},
						//	{"ABCDEFGHIJKLMNOPQRSTUVWXYZ","DEFAULT","UNIQUE","NOT NULL"},
							{"zyxwvutsrqponmlkjihgfedcba","DEFAULT","PRIMARY KEY","NOT NULL"},
						//	{"Z_y_1","NOT NULL","UNIQUE",""},
							{"X1234567890","NOT NULL","PRIMARY KEY",""},
							{"endloop",}};

//	char			*TableColStr;
	char			*TableStr,*tmpstr;
	int				i,j,k;
	int				no_testcase = 1;
//	TableColStr = (char *)malloc(MAX_NOS_SIZE);
	TableStr = new char[MAX_SQLSTRING_LEN];
	tmpstr = new char[10];
	time(&starttime);
	endtime = starttime;	// intial value
	i = 0;
	while (_stricmp(TableType[i].TableColdatatype,"endloop") != 0)
	{
		j = 0;
		while (_stricmp(TableConfig[j].BaseTableName,"endloop") != 0)
		{
			returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
			puts ("IN DML CLIENT FUNCTION");

			if (returncode != SQL_SUCCESS)
			{
			puts ("IN DML CLIENT FUNCTION 1");

				WriteToLog("SetConnectOption: Unable to set access mode to read/write.\n");
				LogAllErrors(pTestInfo);		
				return(FALSE);
			}

			returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_TXN_ISOLATION,SQL_TXN_READ_COMMITTED);
			puts ("IN DML CLIENT FUNCTION 2");

			if (returncode != SQL_SUCCESS)
			{
			puts ("IN DML CLIENT FUNCTION 3");

				WriteToLog("SetConnectOption: Unable to set transaction isolation mode to read committed.\n");
				LogAllErrors(pTestInfo);		
				return(FALSE);
			}
	
			sprintf(TableStr,"DROP TABLE %s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber);
			puts ("IN DML CLIENT FUNCTION 4");

			SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,SQL_NTS);
			printf ("SQL STRING : %s", TableStr);

			puts ("IN DML CLIENT FUNCTION 5");

			sprintf(TableStr,"CREATE TABLE %s_%s_%s (%s%d %s%s %s",TableConfig[j].BaseTableName,ComputerName,ClientNumber,TableConfig[j].BaseTableName,i+1,TableType[i].TableColdatatype,TableType[i].TableScale,TableConfig[j].ColumnConDefn);
			if (_stricmp(TableConfig[j].ColumnConDefn,"DEFAULT") == 0)
			{
				strcat(TableStr," ");
				strcat(TableStr,TableType[i].TableColVal);
			}
			strcat(TableStr," ");
			strcat(TableStr,TableConfig[j].DefaultVal);
			strcat(TableStr," ");
			if (_stricmp(TableConfig[j].TableConDefn,"") != 0)
			{
				strcat(TableStr,",");
				strcat(TableStr,TableConfig[j].TableConDefn);
				strcat(TableStr,"(");
				strcat(TableStr,TableConfig[j].BaseTableName);
				sprintf(tmpstr,"%d",i+1);
				strcat(TableStr,tmpstr);                // appends column name
				strcat(TableStr,")");
				strcat(TableStr,")");
			}
			else
			{
				strcat(TableStr,")");
				strcat(TableStr," NO PARTITIONS");
			}

			sprintf(Heading,"Creating Table >> %s.\n",TableStr);
#ifdef VERBOSE
			WriteToLog(Heading);
#endif
			returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,strlen(TableStr));
			if (returncode != SQL_SUCCESS)
			{
				sprintf(Heading,"Unable to Create Table.\n");
				WriteToLog(Heading);
				if (FindMultipleErrors("Communication link failure","Communication Link failure","connection closed",pTestInfo))
				{
					WriteToLog("ERR>> *** FATAL ERROR *** Communication link failure.\n");
					LogAllErrors(pTestInfo);
					return (2);
				}
				LogAllErrors(pTestInfo);		
			}
			for (k = 0; k < DML_CLIENT_COLUMNS; k++)
			{
				sprintf(TableStr,"INSERT INTO %s_%s_%s values (%s)",TableConfig[j].BaseTableName,ComputerName,ClientNumber,TableType[i].ColVal[k]);
				sprintf(Heading,"Inserting into Table >> %s.\n",TableStr);
#ifdef VERBOSE
				WriteToLog(Heading);
#endif
				puts ("BEFORE INSERT");
				printf ("INSERT STRING: %s", TableStr);
				returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,strlen(TableStr));
				printf ("INSERT RETURNED: %d", returncode);
				if (!SQL_SUCCEEDED(returncode))
				{
				 	if (!FindError(8411,pTestInfo))
					{
						sprintf(Heading,"Unable to Insert into Table.\n");
						WriteToLog(Heading);
						LogAllErrors(pTestInfo);
					}  
				}
			}

			sprintf(TableStr,"SELECT * FROM %s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber);
			sprintf(Heading,"Select Table >> %s.\n",TableStr);
#ifdef VERBOSE
			WriteToLog(Heading);
#endif
			returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,strlen(TableStr));
			if (!SQL_SUCCEEDED(returncode))
			{
				sprintf(Heading,"Unable to Select Table.\n");
				WriteToLog(Heading);
				LogAllErrors(pTestInfo);		
			}
			SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);

			sprintf(TableStr,"DELETE FROM %s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber);
			sprintf(Heading,"Delete Table >> %s.\n",TableStr);
#ifdef VERBOSE
			WriteToLog(Heading);
#endif
			returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,strlen(TableStr));
			if (!SQL_SUCCEEDED(returncode))
			{
				sprintf(Heading,"Unable to Delete Table.\n");
				WriteToLog(Heading);
				LogAllErrors(pTestInfo);		
			}

			sprintf(TableStr,"SELECT * FROM %s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber);
			sprintf(Heading,"Select Table >> %s.\n",TableStr);
#ifdef VERBOSE
			WriteToLog(Heading);
#endif
			returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,strlen(TableStr));
			if (!SQL_SUCCEEDED(returncode))
			{
				sprintf(Heading,"Unable to Select Table.\n");
				WriteToLog(Heading);
				LogAllErrors(pTestInfo);		
			}
			SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);

			//Sleep(3000);

			sprintf(TableStr,"DROP TABLE %s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber);
			sprintf(Heading,"Dropping Table >> %s.\n",TableStr);
#ifdef VERBOSE
			WriteToLog(Heading);
#endif
			printf("DROP STMT: %s", TableStr);
			returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,strlen(TableStr));
			printf("DROP RETRUNED: %d", returncode);
			if (!SQL_SUCCEEDED(returncode))
			{
				sprintf(Heading,"Unable to Drop Table.\n");
				WriteToLog(Heading);
				LogAllErrors(pTestInfo);		
			}
			time(&endtime);
			if (((endtime - starttime)/60) > timeout)
			{
				free(tmpstr);
				free(TableStr);
				return(TRUE);
			}
			j++;
		}
		i++;
	}
	delete tmpstr;
	delete TableStr;
	return(TRUE);
}

// Main Program
// int main(int argc, char **argv)
#ifdef __linux
int main(int argc, char **argv)
#else
void main(int argc, char **argv)
#endif
{
	int		Retcode = FALSE;
	time_t		starttime, endtime;
	int		num_fail_times = 0, num_tolerated_fails = 0;
	DWORD		nSize = MAX_COMPUTERNAME_LENGTH+1;

	// Arguments required for clients to run:
	// 1.		Total time
	// 2.		Client Number
	// 3.		Connection String
	// 4.		Client Objective (like Connect/Disconnect, Insert, Update, etc,....)
	// 5.		Client Number for that Objective
	// 6.		Total Clients for the Objective
	// 7.		Total Number of tables used

	/* Open for write */

	if (argc != 8)
	{
		printf("ERROR: Error in arguments.\n");
		PassFail = FALSE;
		Retcode = FALSE;
		num_fail_times++;
		// goto done;
	}

#ifdef __linux
	strcpy (ComputerName, "SQ");
#else
	GetComputerName(ComputerName,&nSize);
#endif
	for (unsigned int i = 0; i < strlen(ComputerName); i++)
	{
		if (ComputerName[i] == '-')
			ComputerName[i] = '_';
	}
	
	strcpy(ClientNumber,argv[2]);										// Overall Client number
	Client_Number_Within_Operation = atoi(argv[5]);	// Client number for this objective (like insert, select, ...)
	Total_Clients_Per_Operation = atoi(argv[6]);	// Total number of clients for that objective
	Total_Number_Of_Tables = atoi(argv[7]);				// Total number of tables are used
	sprintf(ClientObjective,"%s",argv[4]);										
	sprintf(ClientObjectiveNumber,"%s%s",argv[4],argv[5]);										
	sprintf(logfile,"%s_%s.log",ComputerName,ClientObjectiveNumber);
	// log file name

	//5/27/2004: ARUNA: STORING CONNECTION STRING IN A VARIABLE
	strcpy (connstr, argv[3]);

//	if ((currentWindow = GetActiveWindow()) != NULL)
//	{
//		SetWindowText(NULL,ClientObjectiveNumber);
//	}

	odbcCommon	odbcobj;	// should be initialized here since it needs Total_Number_Of_Tables.

	if((stream = odbcobj.LogOpen()) == NULL )
	{
		printf("ERROR: Unable to open the file");
		PassFail = FALSE;
		Retcode = FALSE;
		num_fail_times++;
		goto done;
	}

	char tmp[200] ; 
	//aruna - 4/4/14 - DO NOT WANT TO WRITE THE PWD IN CLEAR TEXT!
 	//sprintf(tmp,"%s\t%s\t%s\t%s\t%s\t%s\t%s.\n",argv[1],argv[2],argv[3],argv[4],argv[5],argv[6],argv[7]); 
	//odbcobj.MainWrite(tmp);

	time(&starttime);
	endtime = starttime;	// intial value
	timeout = (int)atoi(argv[1]);
	
	if (stricmp(ClientObjective,"CONNECTION") != 0)
	{
        // following while loop should be removed when the bug is fixed in ASSOC. SRV.
		while (!PassFail)
		{
			PassFail = odbcobj.FullConnect(pTestInfo,argv[3]);  // uncomment the logallmsgs in FullConnect

			time(&endtime);
			if (((endtime - starttime)/60) > timeout && ! PassFail)
			  {
				num_fail_times++;
				goto done;
			  }
		}
		if (PassFail)
		{
			odbcobj.MainWrite("Successfully CONNECTED.\n");
			// Now let each client put the information about their servers in the log
			// This will help to figure out the real cause of an error frorm EMS messages
			char  Buf[60];
			RETCODE	returncode;
			SWORD	    OutSize;

			returncode=SQLGetInfo(pTestInfo->hdbc,SQL_SERVER_NAME,Buf,60,&OutSize);
			sprintf(tmp,"SQLGetInfo returncode is %d\n",returncode);
			odbcobj.MainWrite(tmp);
			odbcobj.MainWrite("----------------------------------------------------------------------------------\n");
			sprintf(tmp,"|    The ODBC Server Info is : %s |\n",Buf);
			odbcobj.MainWrite(tmp);
			odbcobj.MainWrite("----------------------------------------------------------------------------------\n");	
			Retcode = TRUE;
		}
		else
		{
			odbcobj.MainWrite("ERROR: Unable to CONNECT.\n");
			//fclose(stream);
			PassFail = FALSE;
			Retcode = FALSE;
		}
	}

		while(((endtime - starttime)/60) < timeout)
		{
			if (stricmp(ClientObjective,"CONNECTION") == 0)	// Clients whose JOBS are to connect, and then disconnect.
			{
				int errOK;
				errOK = 0;
				if (odbcobj.FullConnect(pTestInfo,argv[3],&errOK))
				{
					PassFail = TRUE;
					odbcobj.MainWrite("Successfully CONNECTED.\n");
/* sleep for 5 secs before disconnect */
#ifdef __linux
                                                //sleep (5);
#else
                                                //Sleep (5000);
#endif
					//sleep (5);
					//exit(0);
					if (!odbcobj.FullDisconnect(pTestInfo))
					{
						odbcobj.MainWrite("ERROR: Unable to DISCONNECT.\n");
					}
					else
					{
						
						odbcobj.MainWrite("Successfully DISCONNECTED.\n");
/* sleep for another 120 secs before next connect */
#ifdef __linux
                                                //sleep (120);
#else
                                                //Sleep (120000);
#endif
						sleep (1);
					}
				}
				else
				{
					if (errOK)
					  {
						PassFail = TRUE;
						odbcobj.MainWrite("INFO: Error is tolerated.\n");
						num_tolerated_fails++;
#ifdef __linux
						//sleep (120);
#else
						//Sleep (120000);
#endif
					  }
					else
					  {
						PassFail = FALSE;
						odbcobj.MainWrite("ERROR: Unable to CONNECT.\n");
						//fclose(stream);
						PassFail = FALSE;
					  }
				}
			}
			if (stricmp(ClientObjective,"DDL") == 0)
			{
				if (Retcode == TRUE)
				{
					Retcode = odbcobj.DDLClient(pTestInfo);
				}
				if (Retcode == TRUE)
				{
					odbcobj.MainWrite("Successfully CREATED DDLs.\n");
				}
				else if (Retcode == 2)
				{
					PassFail = FALSE;
					int no_retries = 0;
					while (!PassFail && (no_retries < 10))
					{
						no_retries++;
						sprintf(tmp,"Attempting to reconnect: %d.\n",no_retries);
						odbcobj.MainWrite(tmp);
						PassFail = odbcobj.FullConnect(pTestInfo,argv[3]);  // uncomment the logallmsgs in FullConnect
					}
					if (PassFail)
					{
						sprintf(tmp,"Successfully re-CONNECTED on attempt %d.\n",no_retries);
						odbcobj.MainWrite(tmp);
						// Now let each client put the information about their servers in the log
						// This will help to figure out the real cause of an error frorm EMS messages
						char  Buf[60];
						RETCODE	returncode;
						SWORD	    OutSize;

						returncode=SQLGetInfo(pTestInfo->hdbc,SQL_SERVER_NAME,Buf,60,&OutSize);
						sprintf(tmp,"SQLGetInfo returncode is %d\n",returncode);
						odbcobj.MainWrite(tmp);
						odbcobj.MainWrite("----------------------------------------------------------------------------------\n");
						sprintf(tmp,"|    The ODBC Server Info is : %s |\n",Buf);
						odbcobj.MainWrite(tmp);
						odbcobj.MainWrite("----------------------------------------------------------------------------------\n");	
						Retcode = TRUE;
					}
					else
					{
						sprintf(tmp,"ERROR: Unable to re-connect. Tried %d times.\n", no_retries);
						odbcobj.MainWrite(tmp);
						fclose(stream);
						PassFail = FALSE;
						num_fail_times++;
						// ExitProcess(PassFail);
						goto done;
					}
				} /* comm error */
				else
				{
					odbcobj.MainWrite("ERROR: Unable to CREATED DDLs.\n");
				}
			}
			if (stricmp(ClientObjective,"DML") == 0)
			{
				if (Retcode == TRUE)
				{
					Retcode = odbcobj.DMLClient(pTestInfo);
				}
				if (Retcode == TRUE)
				{
					odbcobj.MainWrite("Successfully in DML commands.\n");
				}
				else if (Retcode == 2)
				{
					PassFail = FALSE;
					int no_retries = 0;
					while (!PassFail && (no_retries < 10))
					{
						no_retries++;
						sprintf(tmp,"Attempting to reconnect: %d.\n",no_retries);
						odbcobj.MainWrite(tmp);
						PassFail = odbcobj.FullConnect(pTestInfo,argv[3]);  // uncomment the logallmsgs in FullConnect
					}
					if (PassFail)
					{
						sprintf(tmp,"Successfully re-CONNECTED on attempt %d.\n",no_retries);
						odbcobj.MainWrite(tmp);
						// Now let each client put the information about their servers in the log
						// This will help to figure out the real cause of an error frorm EMS messages
						char  Buf[60];
						RETCODE	returncode;
						SWORD	    OutSize;

						returncode=SQLGetInfo(pTestInfo->hdbc,SQL_SERVER_NAME,Buf,60,&OutSize);
						sprintf(tmp,"SQLGetInfo returncode is %d\n",returncode);
						odbcobj.MainWrite(tmp);
						odbcobj.MainWrite("----------------------------------------------------------------------------------\n");
						sprintf(tmp,"|    The ODBC Server Info is : %s |\n",Buf);
						odbcobj.MainWrite(tmp);
						odbcobj.MainWrite("----------------------------------------------------------------------------------\n");	
						Retcode = TRUE;
					}
					else
					{
						sprintf(tmp,"ERROR: Unable to re-connect. Tried %d times.\n", no_retries);
						odbcobj.MainWrite(tmp);
						fclose(stream);
						PassFail = FALSE;
						num_fail_times++;
						// ExitProcess(PassFail);
						goto done;
					}
				} /* comm error */
				else
				{
					odbcobj.MainWrite("ERROR: Unable to execute DML commands.\n");
				}
			}
			if (!PassFail)
			{
				num_fail_times = num_fail_times + 1;
				PassFail = TRUE;	// reset it back to try again.
			}
			/*  IT WILL KEEP TRYING TILL THE ENDTIME.
			if (num_fail_times > 5)
			{
				break;
			}
			*/
			time(&endtime);
		}
 
	if (stricmp(ClientObjective,"CONNECTION") != 0)
	{
		if (!odbcobj.FullDisconnect(pTestInfo))
		{
			odbcobj.MainWrite("ERROR: Unable to DISCONNECT.\n");
			num_fail_times++;
		}
		else
		{
			odbcobj.MainWrite("Successfully DISCONNECTED.\n");
		}
	}

done:
	if (num_fail_times == 0)
	  {
            if (num_tolerated_fails)
              sprintf (tmp, "TEST RESULT: PASS (tolerated failures: %d)\n", num_tolerated_fails);
            else
	      sprintf (tmp, "TEST RESULT: PASS\n");
	  }
	else
	  sprintf (tmp, "TEST RESULT: FAIL (failures: %d)\n", num_fail_times);

	odbcobj.MainWrite (tmp);
	fclose(stream);
	ExitProcess(PassFail);
}

