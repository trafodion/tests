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
		BOOL SetupClient(TestInfo *pTestInfo);
		INT DDLClient(TestInfo *pTestInfo);
		INT DMLClient(TestInfo *pTestInfo);
		BOOL GetAllInfo(TestInfo *pTestInfo);
		BOOL InsertClient(TestInfo *pTestInfo);	
		BOOL SelectClient(TestInfo *pTestInfo);	
		BOOL UpdateClient(TestInfo *pTestInfo);	
		BOOL DeleteClient(TestInfo *pTestInfo);	
		BOOL CatalogClient(TestInfo *pTestInfo);	
		BOOL CleanupClient(TestInfo *pTestInfo);
		BOOL FullDisconnect(TestInfo *pTestInfo);
		BOOL IndividualTransactClient(TestInfo *pTestInfo);
		BOOL CommonTransactClient(TestInfo *pTestInfo);
		BOOL CommonRandomClient(TestInfo *pTestInfo);
		BOOL FindError(char *FindMsg, TestInfo *pTestInfo);
		BOOL FindError(SDWORD FindMsg, TestInfo *pTestInfo);
		BOOL FindMultipleErrors(const char *FindMsg1, const char *FindMsg2, const char *FindMsg3, TestInfo *pTestInfo);
        void stripInfo(char* ConnectString);
        BOOL ConnectPoolClient(TestInfo *pTestInfo);

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
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("Unable to Allocate Envirnoment.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	WriteToLog("FullConnect function, Before SQLAllocConnect call. \n");
	returncode = SQLAllocConnect(henv,&hdbc);
	if (returncode != SQL_SUCCESS)
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
	if ((returncode != SQL_SUCCESS) && (returncode != SQL_SUCCESS_WITH_INFO))
	{
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
          	if (errOK &&
                   (diagRc == SQL_SUCCESS || diagRc == SQL_SUCCESS_WITH_INFO)
		   && strstr((char *) text, "error text:Too many open files."))
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
	
	WriteToLog("FullConnect function, Before SQLAllocStmt call. \n");
	returncode = SQLAllocStmt(hdbc,&hstmt);
	if (returncode != SQL_SUCCESS)
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
// SQLExecDirect
// SQLSetConnectOption
// SQLGetConnectOption
//#####################################################################################################
BOOL odbcCommon :: SetupClient(TestInfo *pTestInfo)
{
  RETCODE returncode;                        
	PTR			pvParam;
 	int			i;
//	int			j, k;
//	char		temp[300];

	returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("SetConnectOption: Unable to set access mode to read/write.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	returncode = SQLGetConnectOption(pTestInfo->hdbc,SQL_ACCESS_MODE,&pvParam);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("GetConnectOption: Unable to get access mode to read/write.\n");
	}
	
	if ((long)pvParam != SQL_MODE_READ_WRITE)
	{
		WriteToLog("GetConnectOption: Invalid access mode value for read/write returned.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_TXN_ISOLATION,SQL_TXN_READ_COMMITTED);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("SetConnectOption: Unable to set transaction isolation mode to read committed.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	returncode = SQLGetConnectOption(pTestInfo->hdbc,SQL_TXN_ISOLATION,&pvParam);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("GetConnectOption: Unable to get transaction isolation mode to read committed.\n");
	}

	if ((long)pvParam != SQL_TXN_READ_COMMITTED)
	{
		WriteToLog("GetConnectOption: Invalid access mode value for read/write returned.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	for (i = 0; i < Total_Number_Of_Tables; i++)
	{
		SQLExecDirect(pTestInfo->hstmt,(UCHAR *)SQLCommands(pTestInfo->Table[i],DROP_TABLE,0),SQL_NTS); // Cleanup
		returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)SQLCommands(pTestInfo->Table[i],CREATE_TABLE_MX,0),SQL_NTS);
		if (returncode != SQL_SUCCESS)
		{
			WriteToLog("ExecDirect: Unable to Create Table.\n");
			LogAllErrors(pTestInfo);		
			return(FALSE);
		}
	}

	return(TRUE);
}	

//#####################################################################################################
// This functions cover the following APIs:
// SQLExecDirect
//#####################################################################################################
BOOL odbcCommon :: CleanupClient(TestInfo *pTestInfo)
{
  RETCODE returncode;                        
	ULONG		pvParam;
	int			i;
//	char		temp[300];
	BOOL		TF = TRUE;

	returncode = SQLSetStmtOption(pTestInfo->hstmt,SQL_ASYNC_ENABLE,SQL_ASYNC_ENABLE_ON);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("SetStmtOption: Unable to set ASYNC mode to ENABLE.\n");
		LogAllErrors(pTestInfo);		
	}
	returncode = SQLGetStmtOption(pTestInfo->hstmt,SQL_ASYNC_ENABLE,&pvParam);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("GetStmtOption: Unable to get ASYNC mode to ENABLE.\n");
		LogAllErrors(pTestInfo);		
	}

	if (pvParam != SQL_ASYNC_ENABLE_ON)
	{
		WriteToLog("GetStmtOption: Invalid ASYNC mode value for ENABLE returned.\n");
		LogAllErrors(pTestInfo);		
	}

	for (i = 0; i < Total_Number_Of_Tables; i++)
	{
			returncode = SQL_STILL_EXECUTING;
			while (returncode == SQL_STILL_EXECUTING)
			{
				returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)SQLCommands(pTestInfo->Table[i],DROP_TABLE,0),SQL_NTS); 
				//Sleep(500);
			}
			if (returncode != SQL_SUCCESS)
			{
				WriteToLog("ExecDirect: Unable to Drop Table.\n");
				LogAllErrors(pTestInfo);		
				TF = FALSE;
			}
	}

	return(TF);
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
	if (returncode != SQL_SUCCESS)
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
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("Drivers: Unable to Fetch first driver.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	fFuncs = new char[SQL_MAX_DSN_LENGTH];
	returncode = SQLGetInfo(pTestInfo->hdbc, SQL_DATA_SOURCE_NAME, fFuncs, SQL_MAX_DSN_LENGTH, NULL);
	if (returncode != SQL_SUCCESS)
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

//#####################################################################################################
// This functions cover the following APIs:
// SQLNumResultCols
// SQLDescribeParam
// SQLExecute
// SQLBindParam
// SQLNumParams
// SQLSet/GetCursorName
//#####################################################################################################
BOOL odbcCommon :: SelectClient(TestInfo *pTestInfo)
{
	RETCODE						returncode;                        
	SWORD						numcols;
	int							icol;
	UCHAR						columnName[SQL_MAX_COLUMN_NAME_LEN];
	SWORD						columnLength, columnSQLDataType;
//	UDWORD						columnColDef;
	SQLULEN						columnColDef;
	SWORD						columnColScale,columnNull;
	char						temp[MAX_SQLSTRING_LEN];
	PTR							columnAttribute;
	SWORD						pcDesc;
//	SDWORD						pfDesc;
	SQLLEN						pfDesc;
	char						*CharOutput;
	char						*VarCharOutput;
	char						*DecimalOutput;
	char						*NumericOutput;
	SWORD						ShortOutput;
	SDWORD						LongOutput;
	SFLOAT						RealOutput;
	SDOUBLE						FloatOutput;
	SDOUBLE						DoubleOutput;
	DATE_STRUCT					DateOutput;
	TIME_STRUCT					TimeOutput;
	TIMESTAMP_STRUCT			TimestampOutput;
	char						*BigintOutput;
	SQLLEN						CharOutputLen;
	SQLLEN						VarCharOutputLen;
	SQLLEN						DecimalOutputLen;
	SQLLEN						NumericOutputLen;
	SQLLEN						ShortOutputLen;
	SQLLEN						LongOutputLen;
	SQLLEN						RealOutputLen;
	SQLLEN						FloatOutputLen;
	SQLLEN						DoubleOutputLen;
	SQLLEN						DateOutputLen;
	SQLLEN						TimeOutputLen;
	SQLLEN						TimestampOutputLen;
	SQLLEN						BigintOutputLen;
	SDWORD						i = 0;
	BOOL						Match = TRUE;
	
	returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_ONLY);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("SetConnectOption: Unable to set access mode to readonly.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_TXN_ISOLATION,SQL_TXN_READ_UNCOMMITTED);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("SetConnectOption: Unable to set transaction isolation mode to read uncommitted.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	CharOutput = new char[MAX_COLUMN_OUTPUT];
	VarCharOutput = new char[MAX_COLUMN_OUTPUT];
	DecimalOutput = new char[MAX_COLUMN_OUTPUT];
	NumericOutput = new char[MAX_COLUMN_OUTPUT];
	BigintOutput = new char[MAX_COLUMN_OUTPUT];

	sprintf(temp,"Selecting from Tables.\n"); 
#ifdef VERBOSE
	WriteToLog(temp);
#endif
	returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)SQLCommands("",SELECT_MULTIPLE_TABLE,0),SQL_NTS);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("ExecDirect: Unable to Select Table.\n");
		LogAllErrors(pTestInfo);		
		delete CharOutput;
		delete VarCharOutput;
		delete DecimalOutput;
		delete NumericOutput;
		delete BigintOutput;
		return(FALSE);
	}
	else
	{
		returncode = SQLNumResultCols(pTestInfo->hstmt,&numcols);
		if (returncode != SQL_SUCCESS)
		{
			WriteToLog("NumCols: Unable to return number of parameters for select statement.\n");
			LogAllErrors(pTestInfo);		
		}
		if (numcols != MAX_NUM_COLUMNS)
		{
			sprintf(temp,"NumCols: Number of columns doesn't match expected: %d and actual: %d",numcols,Actual_Num_Columns); 
			WriteToLog(temp);
		}
		for (icol = 0; icol < numcols; icol++)
		{
			returncode = SQLDescribeCol(pTestInfo->hstmt,icol+1,columnName,SQL_MAX_COLUMN_NAME_LEN,&columnLength,&columnSQLDataType,&columnColDef,&columnColScale,&columnNull);
			if (returncode != SQL_SUCCESS)
			{
				sprintf(temp,"DescribeCol: Unable to describe column %d after select statement.\n",icol+1); 
				WriteToLog(temp);
				LogAllErrors(pTestInfo);		
			}
			if ((ColumnInfo[icol].DataType != SQL_FLOAT) && (ColumnInfo[icol].DataType != SQL_DOUBLE))	// bug since SQL return DOUBLE for FLOAT also. May be we treat this as feature.
			{
				if ((_strnicmp((char *)columnName,ColumnInfo[icol].Name,columnLength) != 0) && (columnSQLDataType != ColumnInfo[icol].DataType))
				{
					sprintf(temp,"DescribeCol: Column %d doesn't match column name expected: %s and actual: %s and datatype expected: %d and actual: %d",icol+1,ColumnInfo[icol].Name,columnName,ColumnInfo[icol].DataType,columnSQLDataType); 
					WriteToLog(temp);
				}
			}
			columnAttribute = new char[SQL_MAX_COLUMN_NAME_LEN];
			returncode = SQLColAttributes(pTestInfo->hstmt,icol+1,SQL_COLUMN_NAME,columnAttribute,SQL_MAX_COLUMN_NAME_LEN,&pcDesc,&pfDesc);
			if (returncode != SQL_SUCCESS)
			{
				WriteToLog("ColumnAttribute: Unable to get column attribute name after select statement.\n");
				LogAllErrors(pTestInfo);		
			}
			if (_strnicmp(ColumnInfo[icol].Name,(char *)columnAttribute,pcDesc) != 0)
			{
				sprintf(temp,"ColumnAttribute: Column %d doesn't match column name expected: %s and actual: %s.\n",icol+1,ColumnInfo[icol].Name,columnAttribute); 
				WriteToLog(temp);
			}
			returncode = SQLColAttributes(pTestInfo->hstmt,icol+1,SQL_COLUMN_TYPE,columnAttribute,0,&pcDesc,&pfDesc);
			if (returncode != SQL_SUCCESS)
			{
				WriteToLog("ColumnAttribute: Unable to get column attribute type after select statement.\n");
				LogAllErrors(pTestInfo);		
			}
			if ((ColumnInfo[icol].DataType != SQL_FLOAT) && (ColumnInfo[icol].DataType != SQL_DOUBLE))	// bug since SQL return DOUBLE for FLOAT also. May be we treat this as feature.
			{
				if (ColumnInfo[icol].DataType != pfDesc)
				{
					sprintf(temp,"ColumnAttribute: Column %d doesn't match column type expected: %d and actual: %d.\n",icol+1,ColumnInfo[icol].DataType,pfDesc); 
					WriteToLog(temp);
				}
			}
			delete columnAttribute; 
		
			switch (ColumnInfo[icol].DataType)
			{
				case SQL_CHAR:
					returncode = SQLBindCol(pTestInfo->hstmt,icol+1,ColumnInfo[icol].CDataType,CharOutput,MAX_COLUMN_OUTPUT,&CharOutputLen);
					break;
				case SQL_VARCHAR:
					returncode = SQLBindCol(pTestInfo->hstmt,icol+1,ColumnInfo[icol].CDataType,VarCharOutput,MAX_COLUMN_OUTPUT,&VarCharOutputLen);
					break;
				case SQL_DECIMAL:
					returncode = SQLBindCol(pTestInfo->hstmt,icol+1,ColumnInfo[icol].CDataType,DecimalOutput,MAX_COLUMN_OUTPUT,&DecimalOutputLen);
					break;
				case SQL_NUMERIC:
					returncode = SQLBindCol(pTestInfo->hstmt,icol+1,ColumnInfo[icol].CDataType,NumericOutput,MAX_COLUMN_OUTPUT,&NumericOutputLen);
					break;
				case SQL_SMALLINT:
					returncode = SQLBindCol(pTestInfo->hstmt,icol+1,ColumnInfo[icol].CDataType,&ShortOutput,0,&ShortOutputLen);
					break;
				case SQL_INTEGER:
					returncode = SQLBindCol(pTestInfo->hstmt,icol+1,ColumnInfo[icol].CDataType,&LongOutput,0,&LongOutputLen);
					break;
				case SQL_REAL:
					returncode = SQLBindCol(pTestInfo->hstmt,icol+1,ColumnInfo[icol].CDataType,&RealOutput,0,&RealOutputLen);
					break;
				case SQL_FLOAT:
					returncode = SQLBindCol(pTestInfo->hstmt,icol+1,ColumnInfo[icol].CDataType,&FloatOutput,0,&FloatOutputLen);
					break;
				case SQL_DOUBLE:
					returncode = SQLBindCol(pTestInfo->hstmt,icol+1,ColumnInfo[icol].CDataType,&DoubleOutput,0,&DoubleOutputLen);
					break;
				case SQL_DATE:
					returncode = SQLBindCol(pTestInfo->hstmt,icol+1,ColumnInfo[icol].CDataType,&DateOutput,0,&DateOutputLen);
					break;
				case SQL_TIME:
					returncode = SQLBindCol(pTestInfo->hstmt,icol+1,ColumnInfo[icol].CDataType,&TimeOutput,0,&TimeOutputLen);
					break;
				case SQL_TIMESTAMP:
					returncode = SQLBindCol(pTestInfo->hstmt,icol+1,ColumnInfo[icol].CDataType,&TimestampOutput,0,&TimestampOutputLen);
					break;
				case SQL_BIGINT:
					returncode = SQLBindCol(pTestInfo->hstmt,icol+1,ColumnInfo[icol].CDataType,BigintOutput,MAX_COLUMN_OUTPUT,&BigintOutputLen);
					break;
			}
			if (returncode != SQL_SUCCESS)
			{
				sprintf(temp,"Unable to bind column %d after select statement.\n",icol); 
				WriteToLog(temp);
				LogAllErrors(pTestInfo);		
			}
		
		}
		returncode = SQLFetch(pTestInfo->hstmt);
		if ((returncode != SQL_SUCCESS) && (returncode != SQL_NO_DATA_FOUND))
		{
			WriteToLog("Fetch: Unable to fetch after bind column.\n");
			LogAllErrors(pTestInfo);		
		}

		if (returncode == SQL_SUCCESS)
		{
			Match = TRUE;
			for (icol = 0; icol < Total_Num_Rows; icol++)
			{
				// for future release you can loop here
				if (_strnicmp(InputOutputValues[icol].CharValue,CharOutput,strlen(InputOutputValues[icol].CharValue)) != 0)
				{
					Match = FALSE;
				}
				else
				{
					Match = TRUE;
					break;
				}
			}
			if (!Match)
			{
				sprintf(temp,"ERROR >> Column: %s output: %s doesn't match any one of the values: ",ColumnInfo[0].Name,CharOutput);
				for (icol = 0; icol < Total_Num_Rows; icol++)
				{
					strcat(temp,InputOutputValues[icol].CharValue);
					strcat(temp," OR ");
				}
				strcat(temp,".\n");
				WriteToLog(temp);
			}
			Match = TRUE;
			for (icol = 0; icol < Total_Num_Rows; icol++)
			{
				// for future release you can loop here
				if (_strnicmp(InputOutputValues[icol].VarCharValue,VarCharOutput,strlen(InputOutputValues[icol].VarCharValue)) != 0)
				{
					Match = FALSE;
				}
				else
				{
					Match = TRUE;
					break;
				}
			}
			if (!Match)
			{
				sprintf(temp,"ERROR >> Column: %s output: %s doesn't match any one of the values: ",ColumnInfo[1].Name,VarCharOutput);
				for (icol = 0; icol < Total_Num_Rows; icol++)
				{
					strcat(temp,InputOutputValues[icol].VarCharValue);
					strcat(temp," OR ");
				}
				strcat(temp,".\n");
				WriteToLog(temp);
			}
			Match = TRUE;
			for (icol = 0; icol < Total_Num_Rows; icol++)
			{
				// for future release you can loop here
				if (_strnicmp(InputOutputValues[icol].NumericValue,NumericOutput,strlen(InputOutputValues[icol].NumericValue)) != 0)
				{
					Match = FALSE;
				}
				else
				{
					Match = TRUE;
					break;
				}
			}
			if (!Match)
			{
				sprintf(temp,"ERROR >> Column: %s output: %s doesn't match any one of the values: ",ColumnInfo[3].Name,NumericOutput);
				for (icol = 0; icol < Total_Num_Rows; icol++)
				{
					strcat(temp,InputOutputValues[icol].NumericValue);
					strcat(temp," OR ");
				}
				strcat(temp,".\n");
				WriteToLog(temp);
			}
			Match = TRUE;
			for (icol = 0; icol < Total_Num_Rows; icol++)
			{
				// for future release you can loop here
				if (InputOutputValues[icol].ShortValue != ShortOutput)
				{
					Match = FALSE;
				}
				else
				{
					Match = TRUE;
					break;
				}
			}
			if (!Match)
			{
				sprintf(temp,"ERROR >> Column: %s output: %d doesn't match any one of the values: ",ColumnInfo[4].Name,ShortOutput);
				WriteToLog(temp);
				for (icol = 0; icol < Total_Num_Rows; icol++)
				{
					sprintf(temp,"%d OR ",InputOutputValues[icol].ShortValue);
				}
				WriteToLog(temp);
				sprintf(temp,".\n");
				WriteToLog(temp);
			}
			Match = TRUE;
			for (icol = 0; icol < Total_Num_Rows; icol++)
			{
				// for future release you can loop here
				if (InputOutputValues[icol].RealValue != RealOutput)
				{
					Match = FALSE;
				}
				else
				{
					Match = TRUE;
					break;
				}
			}
			if (!Match)
			{
				sprintf(temp,"ERROR >> Column: %s output: %f doesn't match any one of the values: ",ColumnInfo[6].Name,RealOutput);
				WriteToLog(temp);
				for (icol = 0; icol < Total_Num_Rows; icol++)
				{
					sprintf(temp,"%f OR ",InputOutputValues[icol].RealValue);
				}
				WriteToLog(temp);
				sprintf(temp,".\n");
				WriteToLog(temp);
			}
			Match = TRUE;
			for (icol = 0; icol < Total_Num_Rows; icol++)
			{
				// for future release you can loop here
				if (InputOutputValues[icol].FloatValue != FloatOutput)
				{
					Match = FALSE;
				}
				else
				{
					Match = TRUE;
					break;
				}
			}
			if (!Match)
			{
				sprintf(temp,"ERROR >> Column: %s output: %e doesn't match any one of the values: ",ColumnInfo[7].Name,FloatOutput);
				WriteToLog(temp);
				for (icol = 0; icol < Total_Num_Rows; icol++)
				{
					sprintf(temp,"%e OR ",InputOutputValues[icol].FloatValue);
				}
				WriteToLog(temp);
				sprintf(temp,".\n");
				WriteToLog(temp);
			}
			Match = TRUE;
			for (icol = 0; icol < Total_Num_Rows; icol++)
			{
				// for future release you can loop here
				if (InputOutputValues[icol].DoubleValue != DoubleOutput)
				{
					Match = FALSE;
				}
				else
				{
					Match = TRUE;
					break;
				}
			}
			if (!Match)
			{
				sprintf(temp,"ERROR >> Column: %s output: %e doesn't match any one of the values: ",ColumnInfo[8].Name,DoubleOutput);
				WriteToLog(temp);
				for (icol = 0; icol < Total_Num_Rows; icol++)
				{
					sprintf(temp,"%e OR ",InputOutputValues[icol].DoubleValue);
				}
				WriteToLog(temp);
				sprintf(temp,".\n");
				WriteToLog(temp);
			}
			Match = TRUE;
			for (icol = 0; icol < Total_Num_Rows; icol++)
			{
				// for future release you can loop here
				if ((InputOutputValues[icol].DateValue.month != DateOutput.month) && (InputOutputValues[icol].DateValue.day != DateOutput.day) && (InputOutputValues[icol].DateValue.year != DateOutput.year))
				{
					Match = FALSE;
				}
				else
				{
					Match = TRUE;
					break;
				}
			}
			if (!Match)
			{
				sprintf(temp,"ERROR >> Column: %s output: %d-%d-%d doesn't match any one of the values: ",ColumnInfo[9].Name,DateOutput.month,DateOutput.day,DateOutput.year);
				WriteToLog(temp);
				for (icol = 0; icol < Total_Num_Rows; icol++)
				{
					sprintf(temp,"%d-%d-%d OR ",InputOutputValues[icol].DateValue.month,InputOutputValues[icol].DateValue.day,InputOutputValues[icol].DateValue.year);
				}
				WriteToLog(temp);
				sprintf(temp,".\n");
				WriteToLog(temp);
			}
			Match = TRUE;
			for (icol = 0; icol < Total_Num_Rows; icol++)
			{
				// for future release you can loop here
				if ((InputOutputValues[icol].TimeValue.hour != TimeOutput.hour) && (InputOutputValues[icol].TimeValue.minute != TimeOutput.minute) && (InputOutputValues[icol].TimeValue.second != TimeOutput.second))
				{
					Match = FALSE;
				}
				else
				{
					Match = TRUE;
					break;
				}
			}
			if (!Match)
			{
				sprintf(temp,"ERROR >> Column: %s output: %d:%d:%d doesn't match any one of the values: ",ColumnInfo[10].Name,TimeOutput.hour,TimeOutput.minute,TimeOutput.second);
				WriteToLog(temp);
				for (icol = 0; icol < Total_Num_Rows; icol++)
				{
					sprintf(temp,"%d:%d:%d OR ",InputOutputValues[icol].TimeValue.hour,InputOutputValues[icol].TimeValue.minute,InputOutputValues[icol].TimeValue.second);
				}
				WriteToLog(temp);
				sprintf(temp,".\n");
				WriteToLog(temp);
			}
			Match = TRUE;
			for (icol = 0; icol < Total_Num_Rows; icol++)
			{
				// for future release you can loop here
				if ((InputOutputValues[icol].TimestampValue.month != TimestampOutput.month) && (InputOutputValues[icol].TimestampValue.day != TimestampOutput.day) && (InputOutputValues[icol].TimestampValue.year != TimestampOutput.year) && (InputOutputValues[icol].TimestampValue.hour != TimestampOutput.hour) && (InputOutputValues[icol].TimestampValue.minute != TimestampOutput.minute) && (InputOutputValues[icol].TimestampValue.second != TimestampOutput.second) && (InputOutputValues[icol].TimestampValue.fraction != TimestampOutput.fraction))
				{
					Match = FALSE;
				}
				else
				{
					Match = TRUE;
					break;
				}
			}
			if (!Match)
			{
				sprintf(temp,"ERROR >> Column: %s output: %d-%d-%d %d:%d:%d.%d doesn't match any one of the values: ",ColumnInfo[11].Name,TimestampOutput.month,TimestampOutput.day,TimestampOutput.year,TimestampOutput.hour,TimestampOutput.minute,TimestampOutput.second,TimestampOutput.fraction);
				WriteToLog(temp);
				for (icol = 0; icol < Total_Num_Rows; icol++)
				{
					sprintf(temp,"%d-%d-%d %d:%d:%d.%d OR ",InputOutputValues[icol].TimestampValue.month,InputOutputValues[icol].TimestampValue.day,InputOutputValues[icol].TimestampValue.year,InputOutputValues[icol].TimestampValue.hour,InputOutputValues[icol].TimestampValue.minute,InputOutputValues[icol].TimestampValue.second,InputOutputValues[icol].TimestampValue.fraction);
				}
				WriteToLog(temp);
				sprintf(temp,".\n");
				WriteToLog(temp);
			}
			Match = TRUE;
			for (icol = 0; icol < Total_Num_Rows; icol++)
			{
				// for future release you can loop here
				if (_strnicmp(InputOutputValues[icol].BigintValue,BigintOutput,strlen(InputOutputValues[icol].BigintValue)) != 0)
				{
					Match = FALSE;
				}
				else
				{
					Match = TRUE;
					break;
				}
			}
			if (!Match)
			{
				sprintf(temp,"ERROR >> Column: %s output: %s doesn't match any one of the values: ",ColumnInfo[12].Name,BigintOutput);
				WriteToLog(temp);
				for (icol = 0; icol < Total_Num_Rows; icol++)
				{
					sprintf(temp,"%s OR ",InputOutputValues[icol].BigintValue);
				}
				WriteToLog(temp);
				sprintf(temp,".\n");
				WriteToLog(temp);
			}
		}
		returncode = SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
		if (returncode != SQL_SUCCESS)
		{
			WriteToLog("FreeStmt: Unable to freestmt with CLOSE option.\n");
			LogAllErrors(pTestInfo);		
			delete CharOutput;
			delete VarCharOutput;
			delete DecimalOutput;
			delete NumericOutput;
			delete BigintOutput;
			return(FALSE);
		}
	}
	delete CharOutput;
	delete VarCharOutput;
	delete DecimalOutput;
	delete NumericOutput;
	delete BigintOutput;

	return(TRUE);
}

//#####################################################################################################
// This functions cover the following APIs:
// SQLTables
// SQLColumns
// SQLPrimaryKeys
// SQLStatistics
// SQLSpecialColumns
//#####################################################################################################
BOOL odbcCommon :: CatalogClient(TestInfo *pTestInfo)
{
  RETCODE	returncode;
 	char		temp[300];
	const char		*TableType = "TABLE";
	const char		*Remark = "";
	BOOL		TF = TRUE;
	SDWORD	i = 0, j = 0;

	i = RandomValue(Total_Number_Of_Tables-1);
	sprintf(temp,"The table is %s\n", pTestInfo->Table[i]);
#ifdef VERBOSE
	WriteToLog(temp	);
#endif
	returncode = SQLTables(pTestInfo->hstmt,(UCHAR *)pTestInfo->Catalog,(SWORD)strlen(pTestInfo->Catalog),(UCHAR *)pTestInfo->Schema,(SWORD)strlen(pTestInfo->Schema),(UCHAR *)pTestInfo->Table[i],(SWORD)strlen(pTestInfo->Table[i]),(UCHAR *)TableType,(SWORD)strlen(TableType));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("Tables: Catalog API Tables failed.\n");
		LogAllErrors(pTestInfo);		
		SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
		TF = FALSE;
	}
	returncode = SQLFetch(pTestInfo->hstmt);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("Fetch/Tables: Unable to fetch atleast one row after Tables API.\n");
		LogAllErrors(pTestInfo);		
		SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
		TF = FALSE;
	}
	returncode = SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("FreeStmt/Tables: Unable to freestmt with CLOSE option after Tables API.\n");
		LogAllErrors(pTestInfo);		
		TF = FALSE;
	}

	returncode = SQLColumns(pTestInfo->hstmt,(UCHAR *)pTestInfo->Catalog,(SWORD)strlen(pTestInfo->Catalog),(UCHAR *)pTestInfo->Schema,(SWORD)strlen(pTestInfo->Schema),(UCHAR *)pTestInfo->Table[i],(SWORD)strlen(pTestInfo->Table[i]),(UCHAR *)ColumnInfo[0].Name,(SWORD)strlen(ColumnInfo[0].Name));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("SQLColumns: Catalog API Columns failed.\n");
		LogAllErrors(pTestInfo);		
		SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
		TF = FALSE;
	}
	returncode = SQLFetch(pTestInfo->hstmt);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("Fetch/Tables: Unable to fetch atleast one row after Columns API.\n");
		LogAllErrors(pTestInfo);		
		SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
		TF = FALSE;
	}
	returncode = SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("FreeStmt/Columns: Unable to freestmt with CLOSE option after Columns API.\n");
		LogAllErrors(pTestInfo);		
		TF = FALSE;
	}

	returncode = SQLStatistics(pTestInfo->hstmt,(UCHAR *)pTestInfo->Catalog,(SWORD)strlen(pTestInfo->Catalog),(UCHAR *)pTestInfo->Schema,(SWORD)strlen(pTestInfo->Schema),(UCHAR *)pTestInfo->Table[i],(SWORD)strlen(pTestInfo->Table[i]),SQL_INDEX_UNIQUE,SQL_QUICK);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("SQLStatistics: Catalog API SQLStatistics failed.\n");
		LogAllErrors(pTestInfo);		
		SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
		TF = FALSE;
	}
	returncode = SQLFetch(pTestInfo->hstmt);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("Fetch/Tables: Unable to fetch atleast one row after SQLStatistics API.\n");
		LogAllErrors(pTestInfo);		
		SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
		TF = FALSE;
	}
	returncode = SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("FreeStmt/SQLStatistics: Unable to freestmt with CLOSE option after SQLStatistics API.\n");
		LogAllErrors(pTestInfo);		
		TF = FALSE;
	}

	returncode = SQLPrimaryKeys(pTestInfo->hstmt,(UCHAR *)pTestInfo->Catalog,(SWORD)strlen(pTestInfo->Catalog),(UCHAR *)pTestInfo->Schema,(SWORD)strlen(pTestInfo->Schema),(UCHAR *)pTestInfo->Table[i],(SWORD)strlen(pTestInfo->Table[i]));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("SQLPrimaryKeys: Catalog API SQLPrimaryKeys failed.\n");
		LogAllErrors(pTestInfo);		
		SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
		TF = FALSE;
	}
	returncode = SQLFetch(pTestInfo->hstmt);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("Fetch/Tables: Unable to fetch atleast one row after SQLPrimaryKeys API.\n");
		LogAllErrors(pTestInfo);		
		SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
		TF = FALSE;
	}
	returncode = SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("FreeStmt/SQLPrimaryKeys: Unable to freestmt with CLOSE option after SQLPrimaryKeys API.\n");
		LogAllErrors(pTestInfo);		
		TF = FALSE;
	}
				
	returncode = SQLSpecialColumns(pTestInfo->hstmt,SQL_BEST_ROWID,(UCHAR *)pTestInfo->Catalog,(SWORD)strlen(pTestInfo->Catalog),(UCHAR *)pTestInfo->Schema,(SWORD)strlen(pTestInfo->Schema),(UCHAR *)pTestInfo->Table[i],(SWORD)strlen(pTestInfo->Table[i]),SQL_SCOPE_TRANSACTION,SQL_NULLABLE);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("SQLSpecialColumns: Catalog API SQLSpecialColumns failed.\n");
		LogAllErrors(pTestInfo);		
		SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
		TF = FALSE;
	}
	returncode = SQLFetch(pTestInfo->hstmt);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("Fetch/Tables: Unable to fetch atleast one row after SQLSpecialColumns API.\n");
		LogAllErrors(pTestInfo);		
		SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
		TF = FALSE;
	}
	returncode = SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("FreeStmt/SQLSpecialColumns: Unable to freestmt with CLOSE option after SQLSpecialColumns API.\n");
		LogAllErrors(pTestInfo);		
		TF = FALSE;
	}

	return(TF);
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
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("SetConnectOption: Unable to set access mode to read/write.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_TXN_ISOLATION,SQL_TXN_READ_COMMITTED);
	if (returncode != SQL_SUCCESS)
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
				//Sleep(3000);

				sprintf(TableStr,"DROP TABLE %s_%s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber,tmpbuf);
				sprintf(Heading,"Dropping Table >> %s.\n",TableStr);
#ifdef VERBOSE
				WriteToLog(Heading);
#endif
				returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,strlen(TableStr));
				if (returncode != SQL_SUCCESS)
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
				returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,strlen(TableStr));
				if (returncode != SQL_SUCCESS)
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
			if (returncode != SQL_SUCCESS)
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
			if (returncode != SQL_SUCCESS)
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
			if (returncode != SQL_SUCCESS)
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
			returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,strlen(TableStr));
			if (returncode != SQL_SUCCESS)
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

BOOL odbcCommon :: ConnectPoolClient(TestInfo *pTestInfo)
{   
 	RETCODE		returncode;
	char		Heading[MAX_SQLSTRING_LEN];
	time_t		starttime, endtime;
    int         i, j, max = 500;
    char        TempString[OUT_CONN_STR];
    char        ConnectString[OUT_CONN_STR];
    SQLSMALLINT ConnStrLength;
    char        OutConnStr[OUT_CONN_STR];
    SQLSMALLINT OutConnStrLen;
    SQLHENV     henv;
    SQLHDBC     hdbc;
    SQLHSTMT    hstmt;

	struct		
    {   
        char        str[OUT_CONN_STR];
        int         willBind;
        int         isSelect;
        int         isInsert;
    } execStr[] = {
        {"drop table conPool_%s%s cascade\n", FALSE, FALSE},
        {"create table conPool_%s%s (c1 int not null, c2 char(134), c3 date, primary key (c1))\n", FALSE, FALSE, FALSE},
        {"insert into conPool_%s%s values (%d, 'this_is_the_worst_test_I_have_ever_see', {d '1029-11-22'})\n", FALSE, FALSE, TRUE},
        {"insert into conPool_%s%s values (?, ?, ?)\n", TRUE, FALSE, FALSE},
        {"select * from conPool_%s%s\n", FALSE, TRUE, FALSE},
        //{"delete from conpool_%s%s\n", FALSE, FALSE, FALSE},
        {"endloop", FALSE, FALSE, FALSE}};

    struct
    {
        char        col1[10];
        char        col2[135];
        char        col3[20];
    } data[] = { 
        {"", "first prepare row", "1984-11-22"}, 
        {"", "second prepare row", "1983-11-22"}, 
        {"", "prepare third row", "1982-12-20"}, 
        {"", "prepare row fifth", "2008-10-15"},
        {"99", "", ""}
    };

    char        col1Out[10];
    SQLLEN  col1Len = SQL_NTS;
    char        col2Out[135];
    SQLLEN  col2Len = SQL_NTS;
    char        col3Out[20];
    SQLLEN  col3Len = SQL_NTS;

    time(&starttime);
	endtime = starttime;

    sprintf(Heading,"Starting Connection Pool Test >>>>>>>>>>>>>>>>>>>>>\n");
	WriteToLog(Heading);

    while(true) {

        returncode = SQLAllocHandle(SQL_HANDLE_ENV,(SQLHANDLE)NULL,&henv);

        returncode = SQLSetEnvAttr(henv, SQL_ATTR_ODBC_VERSION, (SQLPOINTER)SQL_OV_ODBC3, SQL_IS_INTEGER);

        returncode = SQLSetEnvAttr(henv, SQL_ATTR_CONNECTION_POOLING, (SQLPOINTER)SQL_CP_ONE_PER_HENV, 0);

        returncode = SQLSetEnvAttr(henv, SQL_ATTR_CP_MATCH, (SQLPOINTER) SQL_CP_RELAXED_MATCH, SQL_IS_INTEGER);

        i = 0;
	    while (stricmp(execStr[i].str,"endloop") != 0)
	    {
            sprintf(Heading,"Starting inner loop to start on generating connections\n");
	        WriteToLog(Heading);

            returncode = SQLAllocHandle(SQL_HANDLE_DBC, henv, &hdbc);

			sprintf(TempString,"DSN=%s;UID=%s;PWD=%s;",pTestInfo->DataSource, pTestInfo->UserID, pTestInfo->Password);
			//printf("%s\n",TempString);
			returncode = SQLDriverConnect(hdbc, NULL, (SQLCHAR*)TempString, strlen(TempString),
								(SQLCHAR*)OutConnStr,OUT_CONN_STR, &OutConnStrLen, SQL_DRIVER_NOPROMPT ); 

            returncode = SQLAllocHandle(SQL_HANDLE_STMT,hdbc,&hstmt);

            sprintf(Heading,"Starting executing queries\n");
	        WriteToLog(Heading);

            if(execStr[i].isInsert == TRUE) {
                for(j=0; j<max; j++) {
                    sprintf(TempString,execStr[i].str,ComputerName,ClientNumber,j);
                    //sprintf(TempString,execStr[i].str,j);
                    //WriteToLog(TempString);
                    returncode = SQLPrepare(hstmt, (SQLCHAR*)TempString, strlen(TempString));
                    returncode = SQLExecute(hstmt);
                    /*sprintf(Heading,"The returncode for FOR insert is %d\n", returncode);
                    WriteToLog(Heading);*/
                }
            } else {
                sprintf(TempString,execStr[i].str,ComputerName,ClientNumber);
                //WriteToLog(execStr[i].str);
                returncode = SQLPrepare(hstmt, (SQLCHAR*)TempString, strlen(execStr[i].str));

                if(execStr[i].willBind == FALSE){
                    returncode = SQLExecute(hstmt);
                } else {
                    j = 0;
				    col1Len = SQL_NTS;
				    col2Len = SQL_NTS;
				    col3Len = SQL_NTS;
                    while(stricmp(data[j].col1,"99") != 0) {
                        sprintf(data[i].col1,"%d", ++max);
                        returncode = SQLBindParameter(hstmt,(SWORD)1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_INTEGER, 10, 0, data[j].col1, 300, &col1Len);
                        returncode = SQLBindParameter(hstmt,(SWORD)2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR, 134, 0, data[j].col2, 300, &col2Len);
                        returncode = SQLBindParameter(hstmt,(SWORD)3, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_DATE, 0, 0, data[j].col3, 300, &col3Len);
                        returncode = SQLExecute(hstmt);
                        /*sprintf(Heading,"The returncode for BIND insert is %d\n", returncode);
                         WriteToLog(Heading);*/
                        j++;
                    }
                }
            }

            if(execStr[i].isSelect == TRUE) {
                returncode = SQLBindCol(hstmt, (SWORD)1, SQL_C_CHAR, &col1Out, 300, &col1Len); 
                returncode = SQLBindCol(hstmt, (SWORD)2, SQL_C_CHAR, &col2Out, 300, &col2Len); 
                returncode = SQLBindCol(hstmt, (SWORD)3, SQL_C_CHAR, &col3Out, 300, &col3Len);
                returncode = SQLFetch(hstmt);
                j = 1;
                while((returncode != SQL_NO_DATA_FOUND) && (returncode != SQL_ERROR)) {
                    returncode = SQLFetch(hstmt);
                    j++;
                }
                sprintf(Heading,"Number of rows fetched is: %d\n",j);
	            WriteToLog(Heading);
            }

            returncode = SQLDisconnect(hdbc);

            returncode = SQLFreeHandle(SQL_HANDLE_DBC, hdbc);

            i++;

            sprintf(Heading,"Ending the inner loop\n");
	        WriteToLog(Heading);
        }

        returncode = SQLFreeHandle(SQL_HANDLE_ENV, henv);

        sprintf(Heading,"Ending the timer loop\n");
	    WriteToLog(Heading);

        time(&endtime);
		if (((endtime - starttime)/60) > timeout)
			break;
    }

    sprintf(Heading,"Ending Connection Pool Test >>>>>>>>>>>>>>>>>>>>>\n\n");
	WriteToLog(Heading);

	return(TRUE);
}

/*
//MULTIPLE CONNECTS
INT odbcCommon :: DMLClient(TestInfo *pTestInfo)
{   
 	RETCODE		returncode;
	char		Heading[MAX_SQLSTRING_LEN];
	time_t		starttime, endtime;
	struct
	{
		char		*TableColdatatype;
		char		*TableScale;
		char		*TableColVal;
		char		*ColVal[DML_CLIENT_COLUMNS];
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
		char		*BaseTableName;
		char		*ColumnConDefn;
		char		*TableConDefn;
		char		*DefaultVal;
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
	
	//DISCONNECT
	if (!FullDisconnect(pTestInfo))
		MainWrite("ERROR: Unable to DISCONNECT.\n");
	else
		MainWrite("Successfully DISCONNECTED.\n");

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
			//CONNECT
			if (FullConnect(pTestInfo,connstr))
			{
				PassFail = TRUE;
				MainWrite("Successfully CONNECTED.\n");
			}
			else
			{
				MainWrite("ERROR: Unable to CONNECT.\n");
				PassFail = FALSE;
				j++;

				time(&endtime);
				if (((endtime - starttime)/60) > timeout)
				{
					free(tmpstr);
					free(TableStr);
					return(TRUE);
				}

				continue;
			}
			returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
			if (returncode != SQL_SUCCESS)
			{
				WriteToLog("SetConnectOption: Unable to set access mode to read/write.\n");
				LogAllErrors(pTestInfo);		
				return(FALSE);
			}

			returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_TXN_ISOLATION,SQL_TXN_READ_COMMITTED);
			if (returncode != SQL_SUCCESS)
			{
				WriteToLog("SetConnectOption: Unable to set transaction isolation mode to read committed.\n");
				LogAllErrors(pTestInfo);		
				return(FALSE);
			}
	
			sprintf(TableStr,"DROP TABLE %s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber);
			SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,SQL_NTS);
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
			}
			strcat(TableStr,")");

			sprintf(Heading,"Creating Table >> %s.\n",TableStr);
			WriteToLog(Heading);
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
				WriteToLog(Heading);
				returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,strlen(TableStr));
				if (returncode != SQL_SUCCESS)
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
			WriteToLog(Heading);
			returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,strlen(TableStr));
			if (returncode != SQL_SUCCESS)
			{
				sprintf(Heading,"Unable to Select Table.\n");
				WriteToLog(Heading);
				LogAllErrors(pTestInfo);		
			}
			SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);

			sprintf(TableStr,"DELETE FROM %s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber);
			sprintf(Heading,"Delete Table >> %s.\n",TableStr);
			WriteToLog(Heading);
			returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,strlen(TableStr));
			if (returncode != SQL_SUCCESS)
			{
				sprintf(Heading,"Unable to Delete Table.\n");
				WriteToLog(Heading);
				LogAllErrors(pTestInfo);		
			}

			sprintf(TableStr,"SELECT * FROM %s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber);
			sprintf(Heading,"Select Table >> %s.\n",TableStr);
			WriteToLog(Heading);
			returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,strlen(TableStr));
			if (returncode != SQL_SUCCESS)
			{
				sprintf(Heading,"Unable to Select Table.\n");
				WriteToLog(Heading);
				LogAllErrors(pTestInfo);		
			}
			SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);

			//Sleep(3000);

			sprintf(TableStr,"DROP TABLE %s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber);
			sprintf(Heading,"Dropping Table >> %s.\n",TableStr);
			WriteToLog(Heading);
			returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,strlen(TableStr));
			if (returncode != SQL_SUCCESS)
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
			//DISCONNECT
			if (!FullDisconnect(pTestInfo))
				MainWrite("ERROR: Unable to DISCONNECT.\n");
			else
				MainWrite("Successfully DISCONNECTED.\n");
		}
		i++;
	}
	delete tmpstr;
	delete TableStr;
	//CONNECT
	if (FullConnect(pTestInfo, connstr))
	{
		PassFail = TRUE;
		MainWrite("Successfully CONNECTED.\n");
	}
	else
	{
		MainWrite("ERROR: Unable to CONNECT.\n");
		PassFail = FALSE;
	}
	return(TRUE);
}
*/


/*
INT odbcCommon :: DMLClient(TestInfo *pTestInfo)
{   
 	RETCODE		returncode;
	char		Heading[MAX_SQLSTRING_LEN];
	time_t		starttime, endtime;
	struct
	{
		char		*TableColdatatype;
		char		*TableScale;
		char		*TableColVal;
		char		*ColVal[DML_CLIENT_COLUMNS];
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
		char		*BaseTableName;
		char		*ColumnConDefn;
		char		*TableConDefn;
		char		*DefaultVal;
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

	//CONNECT
	HENV	henvDDL;
	HDBC	hdbcDDL;
	HSTMT	hstmtDDL;

	returncode = SQLAllocEnv(&henvDDL);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("Unable to Allocate Envirnoment.\n");
		return(TRUE);
	}

	WriteToLog("FullConnect function, Before SQLAllocConnect call DDL. \n");
	returncode = SQLAllocConnect(henvDDL,&hdbcDDL);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("Unable to Allocate Connect DDL.\n");
		SQLFreeEnv(henvDDL);
		henvDDL = NULL;
		return(TRUE);
	}
  
	WriteToLog("FullConnect function, Before SQLDriverConnect call DDL. \n");
	returncode = SQLConnect(hdbcDDL,(UCHAR*)"n",SQL_NTS,
                                (UCHAR*)"super.super",SQL_NTS,
								(UCHAR*)"me",SQL_NTS);
	if ((returncode != SQL_SUCCESS) && (returncode != SQL_SUCCESS_WITH_INFO))
	{
		WriteToLog("Unable to Connect DDL.\n");
		SQLFreeConnect(hdbcDDL);
		SQLFreeEnv(henvDDL);
		hdbcDDL = NULL;
		henvDDL = NULL;
		return(TRUE);
	}
	
	WriteToLog("FullConnect function, Before SQLAllocStmt call. \n");
	returncode = SQLAllocStmt(hdbcDDL,&hstmtDDL);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("Unable to Allocate Statement.\n");
		SQLDisconnect(hdbcDDL);
		SQLFreeConnect(hdbcDDL);
		SQLFreeEnv(henvDDL);
		hdbcDDL = NULL;
		henvDDL = NULL;
		return(TRUE);
	}

	while (_stricmp(TableType[i].TableColdatatype,"endloop") != 0)
	{
		j = 0;
		while (_stricmp(TableConfig[j].BaseTableName,"endloop") != 0)
		{

			returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
			if (returncode != SQL_SUCCESS)
			{
				WriteToLog("SetConnectOption: Unable to set access mode to read/write.\n");
				LogAllErrors(pTestInfo);		
				return(FALSE);
			}

			returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_TXN_ISOLATION,SQL_TXN_READ_COMMITTED);
			if (returncode != SQL_SUCCESS)
			{
				WriteToLog("SetConnectOption: Unable to set transaction isolation mode to read committed.\n");
				LogAllErrors(pTestInfo);		
				return(FALSE);
			}
	
			returncode = SQLSetConnectOption(hdbcDDL,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
			if (returncode != SQL_SUCCESS)
			{
				WriteToLog("SetConnectOption: Unable to set access mode to read/write for DDL.\n");
				return(FALSE);
			}

			returncode = SQLSetConnectOption(hdbcDDL,SQL_TXN_ISOLATION,SQL_TXN_READ_COMMITTED);
			if (returncode != SQL_SUCCESS)
			{
				WriteToLog("SetConnectOption: Unable to set transaction isolation mode to read committed for DDL.\n");
				return(FALSE);
			}

			sprintf(TableStr,"DROP TABLE %s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber);
			SQLExecDirect(hstmtDDL,(UCHAR *)TableStr,SQL_NTS);
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
			}
			strcat(TableStr,")");

			sprintf(Heading,"Creating Table >> %s.\n",TableStr);
			WriteToLog(Heading);
			returncode = SQLExecDirect(hstmtDDL,(UCHAR *)TableStr,strlen(TableStr));
			if (returncode != SQL_SUCCESS)
			{
				sprintf(Heading,"Unable to Create Table.\n");
				WriteToLog(Heading);
			}
			for (k = 0; k < DML_CLIENT_COLUMNS; k++)
			{
				sprintf(TableStr,"INSERT INTO %s_%s_%s values (%s)",TableConfig[j].BaseTableName,ComputerName,ClientNumber,TableType[i].ColVal[k]);
				sprintf(Heading,"Inserting into Table >> %s.\n",TableStr);
				WriteToLog(Heading);
				returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,strlen(TableStr));
				if (returncode != SQL_SUCCESS)
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
			WriteToLog(Heading);
			returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,strlen(TableStr));
			if (returncode != SQL_SUCCESS)
			{
				sprintf(Heading,"Unable to Select Table.\n");
				WriteToLog(Heading);
				LogAllErrors(pTestInfo);		
			}
			SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);

			sprintf(TableStr,"DELETE FROM %s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber);
			sprintf(Heading,"Delete Table >> %s.\n",TableStr);
			WriteToLog(Heading);
			returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,strlen(TableStr));
			if (returncode != SQL_SUCCESS)
			{
				sprintf(Heading,"Unable to Delete Table.\n");
				WriteToLog(Heading);
				LogAllErrors(pTestInfo);		
			}

			sprintf(TableStr,"SELECT * FROM %s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber);
			sprintf(Heading,"Select Table >> %s.\n",TableStr);
			WriteToLog(Heading);
			returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)TableStr,strlen(TableStr));
			if (returncode != SQL_SUCCESS)
			{
				sprintf(Heading,"Unable to Select Table.\n");
				WriteToLog(Heading);
				LogAllErrors(pTestInfo);		
			}
			SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);

			//Sleep(3000);

			sprintf(TableStr,"DROP TABLE %s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber);
			sprintf(Heading,"Dropping Table >> %s.\n",TableStr);
			WriteToLog(Heading);
			returncode = SQLExecDirect(hstmtDDL,(UCHAR *)TableStr,strlen(TableStr));
			if (returncode != SQL_SUCCESS)
			{
				sprintf(Heading,"Unable to Drop Table.\n");
				WriteToLog(Heading);
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
	SQLDisconnect(hdbcDDL);
	SQLFreeConnect(hdbcDDL);
	SQLFreeEnv(henvDDL);
	hdbcDDL = NULL;
	henvDDL = NULL;

	delete tmpstr;
	delete TableStr;
	return(TRUE);
}
*/
/*
INT odbcCommon :: BAD_DMLClient(TestInfo *pTestInfo) //THIS ONE LEAKS HANDLES
{   
 	RETCODE		returncode;
	char		Heading[MAX_SQLSTRING_LEN];
	time_t		starttime, endtime;
	struct
	{
		char		*TableColdatatype;
		char		*TableScale;
		char		*TableColVal;
		char		*ColVal[DML_CLIENT_COLUMNS];
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
		char		*BaseTableName;
		char		*ColumnConDefn;
		char		*TableConDefn;
		char		*DefaultVal;
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
	HSTMT			hstmt_local;
	
	returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("SetConnectOption: Unable to set access mode to read/write.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_TXN_ISOLATION,SQL_TXN_READ_COMMITTED);
	if (returncode != SQL_SUCCESS)
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

			//returncode = SQLAllocStmt(pTestInfo->hdbc,&hstmt_1000[((i+1)*j)]);
			returncode = SQLAllocStmt(pTestInfo->hdbc,&hstmt_local);
			if (returncode != SQL_SUCCESS)
			{
				WriteToLog("Unable to Allocate Statement.\n");
				return(FALSE);
			}

			char tmpbuf[21];
			time_t ltime;
			time( &ltime );
			sprintf(tmpbuf, "%ld", ltime);

			sprintf(TableStr,"DROP TABLE %s_%s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber,tmpbuf);
			//SQLExecDirect(&hstmt_local,(UCHAR *)TableStr,SQL_NTS);
			SQLExecDirect(hstmt_local,(UCHAR *)TableStr,SQL_NTS);
			sprintf(TableStr,"CREATE TABLE %s_%s_%s_%s (%s%d %s%s %s",TableConfig[j].BaseTableName,ComputerName,ClientNumber,tmpbuf,TableConfig[j].BaseTableName,i+1,TableType[i].TableColdatatype,TableType[i].TableScale,TableConfig[j].ColumnConDefn);
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
			}
			strcat(TableStr,")");

			sprintf(Heading,"Creating Table >> %s.\n",TableStr);
			WriteToLog(Heading);
			returncode = SQLExecDirect(hstmt_local,(UCHAR *)TableStr,strlen(TableStr));
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
				//LogAllErrors(pTestInfo);
				LogStmtErrors(hstmt_local);
			}
			for (k = 0; k < DML_CLIENT_COLUMNS; k++)
			{
				sprintf(TableStr,"INSERT INTO %s_%s_%s_%s values (%s)",TableConfig[j].BaseTableName,ComputerName,ClientNumber,tmpbuf,TableType[i].ColVal[k]);
				sprintf(Heading,"Inserting into Table >> %s.\n",TableStr);
				WriteToLog(Heading);
				returncode = SQLExecDirect(hstmt_local,(UCHAR *)TableStr,strlen(TableStr));
				if (returncode != SQL_SUCCESS)
				{
				 	if (!FindError(8411,pTestInfo))
					{
						sprintf(Heading,"Unable to Insert into Table.\n");
						WriteToLog(Heading);
						//LogAllErrors(pTestInfo);
						LogStmtErrors(hstmt_local);
					}  
				}
			}

			sprintf(TableStr,"SELECT * FROM %s_%s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber,tmpbuf);
			sprintf(Heading,"Select Table >> %s.\n",TableStr);
			WriteToLog(Heading);
			returncode = SQLExecDirect(hstmt_local,(UCHAR *)TableStr,strlen(TableStr));
			if (returncode != SQL_SUCCESS)
			{
				sprintf(Heading,"Unable to Select Table.\n");
				WriteToLog(Heading);
				//LogAllErrors(pTestInfo);
				LogStmtErrors(hstmt_local);
			}
			SQLFreeStmt(hstmt_local,SQL_CLOSE);

			sprintf(TableStr,"DELETE FROM %s_%s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber,tmpbuf);
			sprintf(Heading,"Delete Table >> %s.\n",TableStr);
			WriteToLog(Heading);
			returncode = SQLExecDirect(hstmt_local,(UCHAR *)TableStr,strlen(TableStr));
			if (returncode != SQL_SUCCESS)
			{
				sprintf(Heading,"Unable to Delete Table.\n");
				WriteToLog(Heading);
				//LogAllErrors(pTestInfo);
				LogStmtErrors(hstmt_local);
			}

			sprintf(TableStr,"SELECT * FROM %s_%s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber,tmpbuf);
			sprintf(Heading,"Select Table >> %s.\n",TableStr);
			WriteToLog(Heading);
			returncode = SQLExecDirect(hstmt_local,(UCHAR *)TableStr,strlen(TableStr));
			if (returncode != SQL_SUCCESS)
			{
				sprintf(Heading,"Unable to Select Table.\n");
				WriteToLog(Heading);
				//LogAllErrors(pTestInfo);
				LogStmtErrors(hstmt_local);

			}
			SQLFreeStmt(hstmt_local,SQL_CLOSE);

			//Sleep(3000);

			sprintf(TableStr,"DROP TABLE %s_%s_%s_%s",TableConfig[j].BaseTableName,ComputerName,ClientNumber,tmpbuf);
			sprintf(Heading,"Dropping Table >> %s.\n",TableStr);
			WriteToLog(Heading);
			returncode = SQLExecDirect(hstmt_local,(UCHAR *)TableStr,strlen(TableStr));
			if (returncode != SQL_SUCCESS)
			{
				sprintf(Heading,"Unable to Drop Table.\n");
				WriteToLog(Heading);
				//LogAllErrors(pTestInfo);
				LogStmtErrors(hstmt_local);
			}
			time(&endtime);
			if (((endtime - starttime)/60) > timeout)
			{
				delete tmpstr;
				delete TableStr;
				return(TRUE);
			}
			j++;
			//freestmt drop
		}
		i++;
	}
	delete tmpstr;
	delete TableStr;
	return(TRUE);
}
*/
//#####################################################################################################
// This functions cover the following APIs:
// SQLPrepare
// SQLDescribeParam
// SQLExecute
// SQLBindParam
// SQLNumParams
//#####################################################################################################
BOOL odbcCommon :: InsertClient(TestInfo *pTestInfo)
{
    RETCODE	returncode;                        
	SWORD	numparams;
	char	temp[50];
	int		iparam;
	SWORD	paramSQLDataType;
	SQLULEN	paramColDef;
	SWORD	paramColScale,paramColNull;
	SQLLEN	i = 0, j = 0;
	SQLLEN  InsertUniqueValue;

	returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("SetConnectOption: Unable to set access mode to read/write.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_TXN_ISOLATION,SQL_TXN_READ_COMMITTED);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("SetConnectOption: Unable to set transaction isolation mode to read committed.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	i = RandomValue(Total_Number_Of_Tables-1);
	sprintf(temp,"Inserting into Table => %s.\n",pTestInfo->Table[i]); 
#ifdef VERBOSE
	WriteToLog(temp);
#endif

	returncode = SQLPrepare(pTestInfo->hstmt,(UCHAR *)SQLCommands(pTestInfo->Table[i],INSERT_TABLE_PARAMS,0),SQL_NTS);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("Prepare: Unable to prepare insert Table.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	returncode = SQLNumParams(pTestInfo->hstmt,&numparams);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("NumParams: Unable to return number of parameters for insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	if (numparams != MAX_NUM_COLUMNS)
	{
		sprintf(temp,"NumParams: Number of parameters doesn't match expected: %d and actual: %d.\n",numparams,Actual_Num_Columns); 
		WriteToLog(temp);
		return(FALSE);
	}

// Begin of bind parameter
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR, MAX_SQLSTRING_LEN, 0, InputOutputValues[j].CharValue, 0, &(InputOutputValues[j].InValue));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_CHAR to SQL_CHAR during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j= RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, MAX_SQLSTRING_LEN, 0, InputOutputValues[j].VarCharValue, 0, &(InputOutputValues[j].InValue));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_CHAR to SQL_VARCHAR during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j= RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 3, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_DECIMAL, 0, 0, InputOutputValues[j].DecimalValue, 0, &(InputOutputValues[j].InValue));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_CHAR to SQL_DECIMAL during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 4, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_NUMERIC, 0, 0, InputOutputValues[j].NumericValue, 0, &(InputOutputValues[j].InValue));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_CHAR to SQL_CHAR during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 5, SQL_PARAM_INPUT, SQL_C_SHORT, SQL_SMALLINT, 0, 0, &(InputOutputValues[j].ShortValue), 0, &(InputOutputValues[j].InValue1));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_SHORT to SQL_CHAR during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
//	InsertValue[i] = InsertValue[i] + 1;
	InsertUniqueValue = RandomValue(SQL_RANDOM_MAX);
//	returncode = SQLBindParameter(pTestInfo->hstmt, 6, SQL_PARAM_INPUT, SQL_C_LONG, SQL_INTEGER, 0, 0, &(InputOutputValues[num_rows_insert].LongValue), 0, &(InputOutputValues[num_rows_insert].InValue1));
//	sprintf(temp,"%d value insert into table %s.\n",InsertValue[i],pTestInfo->Table[i]); 
	sprintf(temp,"%d value insert into table %s.\n",InsertUniqueValue,pTestInfo->Table[i]); 
#ifdef VERBOSE
	WriteToLog(temp);
#endif
	returncode = SQLBindParameter(pTestInfo->hstmt, 6, SQL_PARAM_INPUT, SQL_C_LONG, SQL_INTEGER, 0, 0, &(InsertUniqueValue), 0, &(InputOutputValues[0].InValue1));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_LONG to SQL_INTEGER during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 7, SQL_PARAM_INPUT, SQL_C_FLOAT, SQL_REAL, 0, 0, &(InputOutputValues[j].RealValue), 0, &(InputOutputValues[j].InValue1));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_FLOAT to SQL_REAL during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 8, SQL_PARAM_INPUT, SQL_C_DOUBLE, SQL_FLOAT, 0, 0, &(InputOutputValues[j].FloatValue), 0, &(InputOutputValues[j].InValue1));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_DOUBLE to SQL_FLOAT during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 9, SQL_PARAM_INPUT, SQL_C_DOUBLE, SQL_DOUBLE, 0, 0, &(InputOutputValues[j].DoubleValue), 0, &(InputOutputValues[j].InValue1));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_DOUBLE to SQL_DOUBLE during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 10, SQL_PARAM_INPUT, SQL_C_DATE, SQL_DATE, 0, 0, &(InputOutputValues[j].DateValue), 0, &(InputOutputValues[j].InValue1));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_DATE to SQL_DATE during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 11, SQL_PARAM_INPUT, SQL_C_TIME, SQL_TIME, 0, 0, &(InputOutputValues[j].TimeValue), 0, &(InputOutputValues[j].InValue1));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_TIME to SQL_TIME during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 12, SQL_PARAM_INPUT, SQL_C_TIMESTAMP, SQL_TIMESTAMP, 0, 0, &(InputOutputValues[j].TimestampValue), 0, &(InputOutputValues[j].InValue1));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_TIMESTAMP to SQL_TIMESTAMP during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 13, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_BIGINT, MAX_SQLSTRING_LEN, 0, InputOutputValues[j].BigintValue, 0, &(InputOutputValues[j].InValue));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_CHAR to SQL_BIGINT during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
// End of bind parameter

	returncode = SQLExecute(pTestInfo->hstmt);
	if (returncode == SQL_ERROR)
	{
			if (!FindError(8102,pTestInfo))
			{
				WriteToLog("Execute: Unable to execute the insert statement after bind parameter.\n");
				LogAllErrors(pTestInfo);	
				return(FALSE);
			}
	}
	else
	{
//				WriteToLog("Inserted a row Successfully.\n");
	}

		for(iparam = 1; iparam <= numparams; iparam++)
		{
			returncode = SQLDescribeParam(pTestInfo->hstmt,iparam,&paramSQLDataType,&paramColDef,&paramColScale,&paramColNull);
			if (returncode != SQL_SUCCESS)
			{
				WriteToLog("DescribeParam: Unable to execute describe parameter after insert.\n");
				LogAllErrors(pTestInfo);		
				return(FALSE);
			}
			if (iparam != 8)	// bug since SQL return DOUBLE for FLOAT also.
			{
				if (paramSQLDataType != ColumnInfo[iparam-1].DataType)
				{
					sprintf(temp,"DescribeParam: Parameter %d doesn't match expected: %d and actual: %d.\n",iparam,paramSQLDataType,ColumnInfo[iparam-1].DataType); 
					WriteToLog(temp);
					return(FALSE);
				}
			}
		} // end of for loop 

	return(TRUE);
}


//#####################################################################################################
// This functions cover the following APIs:
// SQLPrepare
// SQLDescribeParam
// SQLExecute
// SQLBindParam
// SQLNumParams
//#####################################################################################################
BOOL odbcCommon :: UpdateClient(TestInfo *pTestInfo)
{
  RETCODE	returncode;                        
	SWORD		numparams;
	SDWORD	TotalRows = 0, UpdateRow = 0, UpdateColumn = 0;
	SQLLEN	TotalRowsLen, UpdateColumnLen;
	char		temp[50];
	SDWORD	i = 0, j = 0, k = 0, l = 0;

	returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("SetConnectOption: Unable to set access mode to read/write.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_TXN_ISOLATION,SQL_TXN_READ_COMMITTED);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("SetConnectOption: Unable to set transaction isolation mode to read committed.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	while (l == 0)
	{
		i = RandomValue(Total_Number_Of_Tables-1);
		sprintf(temp,"Select count(*) from %s",pTestInfo->Table[i]); 
		returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)temp,SQL_NTS);
		if (returncode == SQL_SUCCESS)
		{
			returncode = SQLBindCol(pTestInfo->hstmt,1,SQL_C_LONG,&TotalRows,300,&TotalRowsLen); // Bug in MP driver for 300 buffer len NO NEED TO SPECIFY
			if (returncode == SQL_SUCCESS)
			{
				returncode = SQLFetch(pTestInfo->hstmt);
				if (returncode == SQL_SUCCESS)
				{
					if (TotalRows > 0)
					{
						while (UpdateRow == 0)
						{
							UpdateRow = RandomValue(TotalRows);
						}
						sprintf(temp,"UpdateRow = %d TotalRows = %d.\n",UpdateRow,TotalRows); 
#ifdef VERBOSE
						WriteToLog(temp);
#endif
						SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
						sprintf(temp,"Select %s from %s",ColumnInfo[5].Name,pTestInfo->Table[i]); 
						returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)temp,SQL_NTS);
						if (returncode == SQL_SUCCESS)
						{
							returncode = SQLBindCol(pTestInfo->hstmt,1,SQL_C_LONG,&UpdateColumn,0,&UpdateColumnLen);
							if (returncode == SQL_SUCCESS)
							{
								for (k = 0; k < UpdateRow; k++)
								{
									returncode = SQLFetch(pTestInfo->hstmt);
									if (returncode != SQL_SUCCESS)
									{
										break;
									}
									else
									{
										l = 1;
 										sprintf(temp,"UpdateColumn = %d.\n",UpdateColumn); 
#ifdef VERBOSE
WriteToLog(temp);
#endif
									}
								}
							}
						}
						SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
					}
				}
			}
		}
		SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
	}

	sprintf(temp,"Updating Table => %s.\n",pTestInfo->Table[i]); 
#ifdef VERBOSE
	WriteToLog(temp);
#endif
	returncode = SQLPrepare(pTestInfo->hstmt,(UCHAR *)SQLCommands(pTestInfo->Table[i],UPDATE_TABLE_PARAMS,UpdateColumn),SQL_NTS);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("Prepare: Unable to prepare update Table.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	returncode = SQLNumParams(pTestInfo->hstmt,&numparams);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("NumParams: Unable to return number of parameters for insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	if (numparams != (MAX_NUM_COLUMNS-1))
	{
		sprintf(temp,"NumParams: Number of parameters doesn't match expected: %d and actual: %d.\n",numparams,Actual_Num_Columns); 
		WriteToLog(temp);
		return(FALSE);
	}

// Begin of bind parameter
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR, MAX_SQLSTRING_LEN, 0, InputOutputValues[j].CharValue, 0, &(InputOutputValues[j].InValue));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_CHAR to SQL_CHAR during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, MAX_SQLSTRING_LEN, 0, InputOutputValues[j].VarCharValue, 0, &(InputOutputValues[j].InValue));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_CHAR to SQL_VARCHAR during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 3, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_DECIMAL, 0, 0, InputOutputValues[j].DecimalValue, 0, &(InputOutputValues[j].InValue));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_CHAR to SQL_DECIMAL during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 4, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_NUMERIC, 0, 0, InputOutputValues[j].NumericValue, 0, &(InputOutputValues[j].InValue));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_CHAR to SQL_CHAR during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 5, SQL_PARAM_INPUT, SQL_C_SHORT, SQL_SMALLINT, 0, 0, &(InputOutputValues[j].ShortValue), 0, &(InputOutputValues[j].InValue1));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_SHORT to SQL_CHAR during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
/*		sprintf(temp,"%d value insert into table %s.\n",InsertValue[i],pTestInfo->Table[i]); 
	WriteToLog(temp);
	returncode = SQLBindParameter(pTestInfo->hstmt, 6, SQL_PARAM_INPUT, SQL_C_LONG, SQL_INTEGER, 0, 0, &(InsertValue[i]), 0, &(InputOutputValues[num_rows_insert].InValue1));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_LONG to SQL_INTEGER during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
*/
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 6, SQL_PARAM_INPUT, SQL_C_FLOAT, SQL_REAL, 0, 0, &(InputOutputValues[j].RealValue), 0, &(InputOutputValues[j].InValue1));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_FLOAT to SQL_REAL during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 7, SQL_PARAM_INPUT, SQL_C_DOUBLE, SQL_FLOAT, 0, 0, &(InputOutputValues[j].FloatValue), 0, &(InputOutputValues[j].InValue1));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_DOUBLE to SQL_FLOAT during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 8, SQL_PARAM_INPUT, SQL_C_DOUBLE, SQL_DOUBLE, 0, 0, &(InputOutputValues[j].DoubleValue), 0, &(InputOutputValues[j].InValue1));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_DOUBLE to SQL_DOUBLE during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 9, SQL_PARAM_INPUT, SQL_C_DATE, SQL_DATE, 0, 0, &(InputOutputValues[j].DateValue), 0, &(InputOutputValues[j].InValue1));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_DATE to SQL_DATE during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 10, SQL_PARAM_INPUT, SQL_C_TIME, SQL_TIME, 0, 0, &(InputOutputValues[j].TimeValue), 0, &(InputOutputValues[j].InValue1));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_TIME to SQL_TIME during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 11, SQL_PARAM_INPUT, SQL_C_TIMESTAMP, SQL_TIMESTAMP, 0, 0, &(InputOutputValues[j].TimestampValue), 0, &(InputOutputValues[j].InValue1));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_TIMESTAMP to SQL_TIMESTAMP during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	j = RandomValue(Total_Num_Rows);
	returncode = SQLBindParameter(pTestInfo->hstmt, 12, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_BIGINT, MAX_SQLSTRING_LEN, 0, InputOutputValues[j].BigintValue, 0, &(InputOutputValues[j].InValue));
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("BindParam: Unable to convert from SQL_C_CHAR to SQL_BIGINT during insert statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
// End of bind parameter

	returncode = SQLExecute(pTestInfo->hstmt);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("Execute: Unable to execute update statement.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	else
	{
//				WriteToLog("updated a row Successfully.\n");
	}

	return(TRUE);
}

BOOL odbcCommon :: IndividualTransactClient(TestInfo *pTestInfo)
{                  
  RETCODE			returncode;
	char				TransactTableName[60];
	char				temp[MAX_SQLSTRING_LEN];
	UWORD				fType[] = 
							{
								SQL_ROLLBACK,SQL_COMMIT,END_LOOP_INT
							};
	const char				*TypeDesc[] = 
							{
								"SQL_ROLLBACK","SQL_COMMIT"
							};
	char				*Output;
	SQLLEN	OutputLen;
	struct
	{
		SWORD	Command;
		const char	*CommandDesc;	
		SWORD	ExeRes[2];
		SWORD	FetchRes[2];
	} CheckRes[] =	
							{
								{CREATE_TABLE,"CREATE_TABLE",SQL_ERROR,SQL_SUCCESS,SQL_NO_DATA_FOUND,SQL_NO_DATA_FOUND},
								{INSERT_TABLE_VALUES,"INSERT_TABLE_VALUES",SQL_SUCCESS,SQL_SUCCESS,SQL_NO_DATA_FOUND,SQL_SUCCESS},
								{UPDATE_TABLE_VALUES,"UPDATE_TABLE_VALUES",SQL_SUCCESS,SQL_SUCCESS,SQL_SUCCESS,SQL_SUCCESS},
								{DELETE_TABLE_VALUES,"DELETE_TABLE_VALUES",SQL_SUCCESS,SQL_SUCCESS,SQL_SUCCESS,SQL_NO_DATA_FOUND},
								{DROP_TABLE,"DROP_TABLE",SQL_SUCCESS,SQL_ERROR,SQL_NO_DATA_FOUND,SQL_NO_DATA_FOUND},
								{END_LOOP_INT,}
							};
	int		i = 0, j = 0, icol = 0;
	BOOL	Match;
	time_t	starttime, endtime;

	returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("SetConnectOption: Unable to set access mode to read/write.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_TXN_ISOLATION,SQL_TXN_READ_COMMITTED);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("SetConnectOption: Unable to set transaction isolation mode to read committed.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	time(&starttime);
	endtime = starttime;	// intial value

	sprintf(TransactTableName,"TransactTable%s%s",ComputerName,ClientNumber);
	SQLExecDirect(pTestInfo->hstmt,(UCHAR *)SQLCommands(TransactTableName,DROP_TABLE,0),SQL_NTS); // Cleanup
	sprintf(temp,"Set Transact mode to SQL_AUTOCOMMIT_OFF.\n"); 
	WriteToLog(temp);
	returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_AUTOCOMMIT,SQL_AUTOCOMMIT_OFF);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("Transact: Unable to set Transact mode to SQL_AUTOCOMMIT_OFF.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	
	while (CheckRes[i].Command != END_LOOP_INT)
	{
		j = 0;
		while ( fType[j] != END_LOOP_INT)
		{
//			sprintf(temp,"Test Positive Functionality of SQLTransact while executing %s & %s.\n",SQLCommands(TransactTableName,CheckRes[i].Command,0),TypeDesc[j]);
			sprintf(temp,"Test Positive Functionality of SQLTransact while executing %s & %s.\n",CheckRes[i].CommandDesc,TypeDesc[j]);
#ifdef VERBOSE
			WriteToLog(temp);
#endif
			if ((CheckRes[i].Command == UPDATE_TABLE_VALUES) && (CheckRes[i].Command == DELETE_TABLE_VALUES))
			{
				returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)SQLCommands(TransactTableName,CheckRes[i].Command,0),SQL_NTS);
			}
			else if(CheckRes[i].Command == CREATE_TABLE)
			{
					returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)SQLCommands(TransactTableName,CREATE_TABLE_MX,0),SQL_NTS);
					if (returncode != SQL_SUCCESS)
					{
						WriteToLog("ExecDirect: Unable to Create Table.\n");
						LogAllErrors(pTestInfo);	
						SQLTransact(pTestInfo->henv,pTestInfo->hdbc,SQL_ROLLBACK);
						//Sleep(2000);	
						return(FALSE);
					}
			}
			else
			{
				returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)SQLCommands(TransactTableName,CheckRes[i].Command,0),SQL_NTS);
			}
			if (returncode != SQL_SUCCESS)
			{
//				sprintf(temp,"Unable to execute %s statement.\n",SQLCommands(TransactTableName,CheckRes[i].Command,0));
				sprintf(temp,"Unable to execute %s statement.\n",CheckRes[i].CommandDesc);
				WriteToLog(temp);
				LogAllErrors(pTestInfo);
				SQLTransact(pTestInfo->henv,pTestInfo->hdbc,SQL_ROLLBACK);
				//Sleep(2000);
				return(FALSE);
			}
			else
			{
				returncode=SQLTransact(pTestInfo->henv,pTestInfo->hdbc,fType[j]);
				//Sleep(2000);																// tmf rollback is slower.
				if (returncode != SQL_SUCCESS)
				{
					sprintf(temp,"Unable to SQLTransact => %s.\n",TypeDesc[j]);
					WriteToLog(temp);
					LogAllErrors(pTestInfo);
					SQLTransact(pTestInfo->henv,pTestInfo->hdbc,SQL_ROLLBACK);
				//	Sleep(2000);
					return(FALSE);
				}
				if(((CheckRes[i].Command == CREATE_TABLE) && !j) || ((CheckRes[i].Command == DROP_TABLE) && j)) // Table would have removed, so skip the rest
				{
					++j;
					continue;
				}
				returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)SQLCommands(TransactTableName,SELECT_TABLE,0),SQL_NTS);
				if (returncode != CheckRes[i].ExeRes[j])
				{
					sprintf(temp,"ExecDirect : Unable to execute (Select) statement.\n");
					WriteToLog(temp);
					LogAllErrors(pTestInfo);
					SQLTransact(pTestInfo->henv,pTestInfo->hdbc,SQL_ROLLBACK);
					//Sleep(2000);
					return(FALSE);
				}
				else
				{
					if (returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO)
					{
						Output = new char[MAX_COLUMN_OUTPUT];
						returncode=SQLBindCol(pTestInfo->hstmt,1,SQL_C_CHAR,Output,MAX_COLUMN_OUTPUT,&OutputLen);
						if (returncode != SQL_SUCCESS)
						{
							WriteToLog("BindCol: Unable to bindcol 1.\n");
							LogAllErrors(pTestInfo);
							delete Output;
							SQLTransact(pTestInfo->henv,pTestInfo->hdbc,SQL_ROLLBACK);
							//Sleep(2000);
							return(FALSE);
						}
						else
						{
							returncode = SQLFetch(pTestInfo->hstmt);
							if (returncode != CheckRes[i].FetchRes[j])
							{
								WriteToLog("Fetch: Unable to fetch row.\n");
								LogAllErrors(pTestInfo);
								delete Output;
								SQLTransact(pTestInfo->henv,pTestInfo->hdbc,SQL_ROLLBACK);
							//	Sleep(2000);
								return(FALSE);
							}
							else
							{
								if (returncode != SQL_NO_DATA_FOUND && returncode != SQL_ERROR)
								{
									Match = TRUE;
									for (icol = 0; icol < Total_Num_Rows; icol++)
									{
										// for future release you can loop here
										if (_strnicmp(InputOutputValues[icol].CharValue,Output,strlen(InputOutputValues[icol].CharValue)) != 0)
										{
											Match = FALSE;
										}
										else
										{
											Match = TRUE;
											break;
										}
									}
									if (!Match)
									{
										sprintf(temp,"ERROR >> Column: %s output: %s doesn't match any one of the values: ",ColumnInfo[0].Name,Output);
										for (icol = 0; icol < Total_Num_Rows; icol++)
										{
											strcat(temp,InputOutputValues[icol].CharValue);
											strcat(temp," OR ");
										}
										strcat(temp,".\n");
										WriteToLog(temp);
									}
								}
							}
							delete Output;
							SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
						}
					}
				}
			}
			time(&endtime);
			if (((endtime - starttime)/60) > timeout)
			{
				sprintf(temp,"Set Transact mode back to SQL_AUTOCOMMIT_ON.\n"); 
#ifdef VERBOSE
				WriteToLog(temp);
#endif
				returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_AUTOCOMMIT,SQL_AUTOCOMMIT_ON);
				if (returncode != SQL_SUCCESS)
				{
					WriteToLog("Transact: Unable to set Transact mode back to SQL_AUTOCOMMIT_ON.\n");
					LogAllErrors(pTestInfo);		
					return(FALSE);
				}
				return(TRUE);
			}
			j++;
		} // end j loop 
		i++;
	} // end i loop 
	sprintf(temp,"Set Transact mode back to SQL_AUTOCOMMIT_ON.\n"); 
#ifdef VERBOSE
	WriteToLog(temp);
#endif
	returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_AUTOCOMMIT,SQL_AUTOCOMMIT_ON);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("Transact: Unable to set Transact mode back to SQL_AUTOCOMMIT_ON.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	return(TRUE);
}



//#####################################################################################################
// This functions cover the following APIs:
// SQLExecDirect
//#####################################################################################################
BOOL odbcCommon :: DeleteClient(TestInfo *pTestInfo)
{
  RETCODE	returncode;                        
	SQLLEN	TotalRows = 0, DeleteRow = 0, DeleteColumn = 0;
	SQLLEN	TotalRowsLen, DeleteColumnLen;
	char		temp[50];
	SDWORD	i = 0, j = 0, k = 0, l = 0;

	returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_ACCESS_MODE,SQL_MODE_READ_WRITE);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("SetConnectOption: Unable to set access mode to read/write.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_TXN_ISOLATION,SQL_TXN_READ_COMMITTED);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("SetConnectOption: Unable to set transaction isolation mode to read committed.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}

	while (l == 0)
	{
		i = RandomValue(Total_Number_Of_Tables-1);
		sprintf(temp,"Select count(*) from %s",pTestInfo->Table[i]); 
		returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)temp,SQL_NTS);
		if (returncode == SQL_SUCCESS)
		{
			returncode = SQLBindCol(pTestInfo->hstmt,1,SQL_C_LONG,&TotalRows,300,&TotalRowsLen); // Bug in MP driver for 300 buffer len NO NEED TO SPECIFY
			if (returncode == SQL_SUCCESS)
			{
				returncode = SQLFetch(pTestInfo->hstmt);
				if (returncode == SQL_SUCCESS)
				{
					if (TotalRows > 0)
					{
						while (DeleteRow == 0)
						{
							DeleteRow = RandomValue(TotalRows);
						}
						sprintf(temp,"DeleteRow = %d TotalRows = %d.\n",DeleteRow,TotalRows); 
#ifdef VERBOSE
						WriteToLog(temp);
#endif
						SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
						sprintf(temp,"Select %s from %s",ColumnInfo[5].Name,pTestInfo->Table[i]); 
						returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)temp,SQL_NTS);
						if (returncode == SQL_SUCCESS)
						{
							returncode = SQLBindCol(pTestInfo->hstmt,1,SQL_C_LONG,&DeleteColumn,0,&DeleteColumnLen);
							if (returncode == SQL_SUCCESS)
							{
								for (k = 0; k < DeleteRow; k++)
								{
									returncode = SQLFetch(pTestInfo->hstmt);
									if (returncode != SQL_SUCCESS)
									{
										break;
									}
									else
									{
										l = 1;
//										sprintf(temp,"DeleteColumn = %d.\n",DeleteColumn); 
//										WriteToLog(temp);
									}
								}
							}
						}
						SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
					}
				}
			}
		}
		SQLFreeStmt(pTestInfo->hstmt,SQL_CLOSE);
	}

	sprintf(temp,"Deleting Table => %s.\n",pTestInfo->Table[i]); 
#ifdef VERBOSE
	WriteToLog(temp);
#endif
	returncode = SQLExecDirect(pTestInfo->hstmt,(UCHAR *)SQLCommands(pTestInfo->Table[i],DELETE_TABLE_PARAMS,DeleteColumn),SQL_NTS);
	if (returncode != SQL_SUCCESS)
	{
		WriteToLog("Prepare: Unable to Execute delete Table.\n");
		LogAllErrors(pTestInfo);		
		return(FALSE);
	}
	else
	{
	//				WriteToLog("delete a row Successfully.\n");
	}

	return(TRUE);
}

BOOL odbcCommon :: CommonTransactClient(TestInfo *pTestInfo)
{                  
	RETCODE	returncode;
	char		temp[MAX_SQLSTRING_LEN];
	BOOL		Res = FALSE;
	UWORD		fType[] = 
					{
						SQL_ROLLBACK,SQL_COMMIT
					};
	const char		*TypeDesc[] = 
					{
						"SQL_ROLLBACK","SQL_COMMIT"
					};
	int			i, j, k;

	i = RandomValue(10); // AUTOCOMMIT ON or OFF
	if (i < 5)
	{
		i = 0;
	}
	else
	{
		i = 1;
	}
	if (i == 0)
	{
		sprintf(temp,"Set Transact mode to SQL_AUTOCOMMIT_OFF.\n"); 
#ifdef VERBOSE
		WriteToLog(temp);
#endif
		returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_AUTOCOMMIT,SQL_AUTOCOMMIT_OFF);
		if (returncode != SQL_SUCCESS)
		{
			WriteToLog("Transact: Unable to set Transact mode to SQL_AUTOCOMMIT_OFF.\n");
			LogAllErrors(pTestInfo);		
			return(FALSE);
		}
	}
	else
	{
		sprintf(temp,"Set Transact mode to SQL_AUTOCOMMIT_ON.\n"); 
#ifdef VERBOSE
		WriteToLog(temp);
#endif
		returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_AUTOCOMMIT,SQL_AUTOCOMMIT_ON);
		if (returncode != SQL_SUCCESS)
		{
			WriteToLog("Transact: Unable to set Transact mode to SQL_AUTOCOMMIT_ON.\n");
			LogAllErrors(pTestInfo);		
			return(FALSE);
		}
	}

	for (j = 0; j < 3; j++)
	{
		switch (j)
		{
			case 0:
				Res = InsertClient(pTestInfo);
				break;
			case 1:
				Res = UpdateClient(pTestInfo);
				break;
			case 2:
				Res = DeleteClient(pTestInfo);
				break;
			default:
				break;
		}
		if ((Res) && (i == 0))
		{
			k = RandomValue(10); // AUTOCOMMIT ON or OFF
			if (k < 5)
			{
				k = 0;
			}
			else
			{
				k = 1;
			}
			sprintf(temp,"Transaction %s.\n",TypeDesc[k]); 
#ifdef VERBOSE
			WriteToLog(temp);
#endif
			returncode=SQLTransact(pTestInfo->henv,pTestInfo->hdbc,fType[k]);
			//Sleep(2000);																// tmf rollback is slower.
			if (returncode != SQL_SUCCESS)
			{
				sprintf(temp,"Unable to SQLTansact => %s.\n",TypeDesc[k]);
				WriteToLog(temp);
				LogAllErrors(pTestInfo);
				return(FALSE);
			}
		}
	}
	if (i == 0)
	{
		sprintf(temp,"Reset Transact mode back to SQL_AUTOCOMMIT_ON.\n"); 
#ifdef VERBOSE
		WriteToLog(temp);
#endif
		returncode = SQLSetConnectOption(pTestInfo->hdbc,SQL_AUTOCOMMIT,SQL_AUTOCOMMIT_ON);
		if (returncode != SQL_SUCCESS)
		{
			WriteToLog("Transact: Unable to set Transact mode back to SQL_AUTOCOMMIT_ON.\n");
			LogAllErrors(pTestInfo);		
			return(FALSE);
		}
	}
	return(TRUE);
}

BOOL odbcCommon :: CommonRandomClient(TestInfo *pTestInfo)
{                  
	BOOL		Res = FALSE;
	int			i;

	i = RandomValue(5); // clients INSERT or UPDATE or DELETE or SELECT or TRANSACT or CATALOG

	switch (i)
	{
		case 0:
			Res = InsertClient(pTestInfo);
			break;
		case 1:
			Res = UpdateClient(pTestInfo);
			break;
		case 2:
			Res = DeleteClient(pTestInfo);
			break;
		case 3:
			Res = SelectClient(pTestInfo);
			break;
		case 4:
			Res = CommonTransactClient(pTestInfo);
			break;
		case 5:
			Res = CatalogClient(pTestInfo);
			break;
		default:
			break;
	}

	return(Res);
}

// Main Program
// int main(int argc, char **argv)
#ifdef __linux
int main(int argc, char **argv)
#else
void main(int argc, char **argv)
#endif
{
	int			Retcode = FALSE;
	time_t		starttime, endtime;
	int			num_fail_times = 0, num_tolerated_fails = 0;
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

	if (stricmp(ClientObjective,"SETUP") == 0)
	{
		if(PassFail)
		{
			PassFail = odbcobj.SetupClient(pTestInfo);
		}
		if (PassFail)
		{
			odbcobj.MainWrite("Successfully Initialized.\n");
		}
		else
		{
			odbcobj.MainWrite("ERROR: Unable to Initialized.\n");
		}
	}
	else if (stricmp(ClientObjective,"CLEANUP") == 0)
	{
		if(PassFail)
		{
			PassFail = odbcobj.CleanupClient(pTestInfo);
		}
		if (PassFail)
		{
			odbcobj.MainWrite("Successfully Cleanup.\n");
		}
		else
		{
			odbcobj.MainWrite("ERROR: Unable to Cleanup.\n");
		}
	}
	else
	{
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
			if (stricmp(ClientObjective,"INSERT") == 0)
			{
				if(PassFail)
				{
					PassFail = odbcobj.InsertClient(pTestInfo);
				}
				if (PassFail)
				{
					odbcobj.MainWrite("Successfully INSERT DMLs.\n");
				}
				else
				{
					odbcobj.MainWrite("ERROR: Unable to INSERT DMLs.\n");
				}
			}
			if (stricmp(ClientObjective,"UPDATE") == 0)
			{
				//Sleep(60*1000);
				if(PassFail)
				{
					PassFail = odbcobj.UpdateClient(pTestInfo);
				}
				if (PassFail)
				{
					odbcobj.MainWrite("Successfully UPDATE DMLs.\n");
				}
				else
				{
					odbcobj.MainWrite("ERROR: Unable to UPDATE DMLs.\n");
				}
			}
			if (stricmp(ClientObjective,"SELECT") == 0)
			{
				//Sleep(60*1000);
				if(PassFail)
				{
					PassFail = odbcobj.SelectClient(pTestInfo);
				}
				if (PassFail)
				{
					odbcobj.MainWrite("Successfully SELECT DMLs.\n");
				}
				else
				{
					odbcobj.MainWrite("ERROR: Unable to SELECT DMLs.\n");
				}
			}
			if (stricmp(ClientObjective,"DELETE") == 0)
			{
				//Sleep(2*60*1000);
				if(PassFail)
				{
					PassFail = odbcobj.DeleteClient(pTestInfo);
				}
				if (PassFail)
				{
					odbcobj.MainWrite("Successfully DELETE DMLs.\n");
				}
				else
				{
					odbcobj.MainWrite("ERROR: Unable to DELETE DMLs.\n");
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
			if (stricmp(ClientObjective,"CATALOG") == 0)
			{
				//Sleep(60*1000);
				if(PassFail)
				{
					//Sleep(60*1000);
					PassFail = odbcobj.CatalogClient(pTestInfo);
				}
				if (PassFail)
				{
					odbcobj.MainWrite("Successfully CATALOG DMLs.\n");
				}
				else
				{
					odbcobj.MainWrite("ERROR: Unable to CATALOG DMLs.\n");
				}
			}
			if (stricmp(ClientObjective,"ITRANSACT") == 0)
			{
				if(PassFail)
				{
					PassFail = odbcobj.IndividualTransactClient(pTestInfo);
				}
				if (PassFail)
				{
					odbcobj.MainWrite("Successfully DDL+DML TRANSACTIONs.\n");
				}
				else
				{
					odbcobj.MainWrite("ERROR: Unable to execute DDL+DML TRANSACTIONs.\n");
				}
			}
			if (stricmp(ClientObjective,"CTRANSACT") == 0)
			{
				//Sleep(60*1000);
				if(PassFail)
				{
					PassFail = odbcobj.CommonTransactClient(pTestInfo);
				}
				if (PassFail)
				{
					odbcobj.MainWrite("Successfully DDL+DML TRANSACTIONs.\n");
				}
				else
				{
					odbcobj.MainWrite("ERROR: Unable to execute DDL+DML TRANSACTIONs.\n");
				}
			}
			if (stricmp(ClientObjective,"CRANDOM") == 0)
			{
				//Sleep(60*1000);
				if(PassFail)
				{
					PassFail = odbcobj.CommonRandomClient(pTestInfo);
				}
				if (PassFail)
				{
					odbcobj.MainWrite("Successfully Common Random clients.\n");
				}
				else
				{
					odbcobj.MainWrite("ERROR: Unable to execute Common clients.\n");
				}
			}
            if (stricmp(ClientObjective,"POOLING") == 0)
			{
				//Sleep(60*1000);
				if(PassFail)
				{
					//Sleep(60*1000);
					PassFail = odbcobj.ConnectPoolClient(pTestInfo);
				}
				if (PassFail)
				{
					odbcobj.MainWrite("Successfully Connect Pooling.\n");
				}
				else
				{
					odbcobj.MainWrite("ERROR: Unable to run Connect Pooling.\n");
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

