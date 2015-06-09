#include "defines.h"
#include "include.h"
#include "ODBCcommon.h"
#include "table.h"
#include "struct.h"
#include "status.h"
#include "globals.h"

/******************
** Local Globals
******************/
time_t lg_previous_time;

typedef struct Counter Counter;
struct Counter {
   short Code;
   short ExtraCode;
   short count;
   Counter *NextPtr;
   };
Counter *lgCounterPtr=NULL;

/***********************************************************************
** check_for_stop()
**
** This function will check if the STOP file exists.  If it does then
** all open files are flushed, a message is posted to the process's
** status file, and the process ends.  Any active transaction are
** left for the system to abort.  If the STOP file does not exist, the
** function simply returns to its caller.
************************************************************************/
void check_for_stop()
{
   FILE *fp;

   /* flush all open files, just to be safe */
   fflush(NULL);

   /* see if we should stop, if not just return */
   fp=fopen(gStopFile,"r");
   if(fp==NULL) return;

   /* we've been told to stop, so do a little clean-up work then end */
   fclose(fp);
   post_status(USER_REQUESTED_STOP);
   LogMsg(0,"*** This process stopping because user requested it\n\n");
   exit(EXIT_SUCCESS);
   } /* end: check_for_stop() */

/***********************************************************************
** stop_on_error()
**
** This function will flush all open files and then post a message
** to the process's status file, and the process ends.  Any active
** transaction are left for the system to abort.
************************************************************************/
void stop_on_error()
{
   /* flush all open files, just to be safe */
   fflush(NULL);

   post_status(ERROR_STOP);
   LogMsg(0,"*** This process stopping because 'stop on error' was set\n\n");
   exit(EXIT_FAILURE);
   } /* end: check_for_stop() */


/***********************************************************************
** BuildErrorCountsString()
**
** This function will build a string containing the counts of the various
** errors/warnings which occurred (if any)
************************************************************************/
char *BuildErrorCountsString(ReturnStatus **RSPtr)
{
   Counter *TempPtr;
   char *StringPtr;
   char buffer[2000];
   char *BufferPtr;

   *RSPtr=NULL;

   TempPtr=lgCounterPtr;
   strcpy(buffer,"   SQL     FS\n"
                 "   Error   Error   Count\n"
                 "   ------  ------  -----\n");
   BufferPtr=buffer+strlen(buffer);
   while(TempPtr!=NULL){

      if(TempPtr->ExtraCode==0){
         sprintf(BufferPtr,"%6d          %5d\n",TempPtr->Code,TempPtr->count);
         }
      else{
         sprintf(BufferPtr,"%6d  %6d  %5d\n",TempPtr->Code,TempPtr->ExtraCode,
                 TempPtr->count);
         }

      BufferPtr=buffer+strlen(buffer);
      TempPtr=TempPtr->NextPtr;
      }
   *BufferPtr=NULL;

   StringPtr=malloc(strlen(buffer)+1);
   if(StringPtr==NULL) {
      *RSPtr=BuildReturnStatusMALLOC;
      return(NULL);
      }
   strcpy(StringPtr,buffer);
   return(StringPtr);
   } /* end: BuildErrorCountsString() */


/***********************************************************************
** post_status()
**
** This function will write various pieces of info to the process's
** status file.
************************************************************************/
void post_status(short msg_num)
{
   FILE *fp;
   time_t TempTime;
   struct tm *TimeBlockPtr;
   char msg[80];
   char *ErrorsPtr;
   ReturnStatus *RSPtr;
	short i;

   /* first flush all other open files, just to be safe */
   fflush(NULL);

   /* get appropriate status msg */
   switch(msg_num){
      case STARTED:
         strcpy(msg,"STARTED");
         break;
      case INIT_TABLES:
         strcpy(msg,"INITIALIZING TABLES (randomly filling with data)");
         break;
      case USER_REQUESTED_STOP:
         strcpy(msg,"STOPPED (user requested)");
         LogMsg(0,"%s\n",msg);
         break;
      case OK:
         strcpy(msg,"OK (continuing execution)");
         break;
      case FINISHED:
         strcpy(msg,"FINISHED (everything completed ok, as far as I can tell)");
         LogMsg(0,"%s\n",msg);
         break;
      case ERROR_STOP:
         strcpy(msg,"STOPPED (encountered error and user requested stop on error)");
         LogMsg(0,"%s\n",msg);
         break;
      default:
         strcpy(msg,"OH-OH! in post_status() <msg_num> is %d and that's"
                " not defined.");
      } /* end: switch(msg_num) */

   /* open the status file */
	fp=NULL;
	i=0;
	while((fp==NULL)&&(i<STATUS_RETRIES)){
		fp=fopen(g_status_file,"w");
		i++;
	}
	// if after many retries the file still can't be opened the log an error
	if(fp==NULL){
      LogMsg(ERRMSG+LINES,
             "unable to open status file '%s' for write access\n",
             g_status_file);
      return;
      }

   /* write out status, overwriting any previous status info */
   fprintf(fp,"===================================\n");
   fprintf(fp,"Process #%lu (pid %u)   %s\n",gProcessNumber,gPid,msg);
   TimeBlockPtr=localtime(&g_start_time);
   fprintf(fp,"   start_time:  %04d-%02d-%02d_%02d:%02d:%02d\n",
   		TimeBlockPtr->tm_year+1900,
         TimeBlockPtr->tm_mon+1,
         TimeBlockPtr->tm_mday,
         TimeBlockPtr->tm_hour,
         TimeBlockPtr->tm_min,
         TimeBlockPtr->tm_sec);
   TempTime=time(NULL);
   TimeBlockPtr=localtime(&TempTime);
   fprintf(fp,"   last_status: %04d-%02d-%02d_%02d:%02d:%02d\n",
   		TimeBlockPtr->tm_year+1900,
         TimeBlockPtr->tm_mon+1,
         TimeBlockPtr->tm_mday,
         TimeBlockPtr->tm_hour,
         TimeBlockPtr->tm_min,
         TimeBlockPtr->tm_sec);
   fprintf(fp,"   Actions:%ld  Transactions(commit:%ld abort:%ld)\n",
           g_action_count,g_trans_commit,g_trans_abort);
//   ErrorsPtr=BuildErrorCountsString(&RSPtr);
//   if(RSPtr!=NULL){
//      LogReturnStatus(RSPtr);
//      FreeReturnStatus(RSPtr);
//      }
//   else{
//      fprintf(fp,"%s",ErrorsPtr);
//      free(ErrorsPtr);
//      }

   fclose(fp);
   lg_previous_time=TempTime;
   } /* end: post_status() */


/************************************************************************
** consist_check(): Function to verify a table's consistency
*************************************************************************
**
** This function will add together all the values in the input specified
** zerosum and abort columns and verify both totals equal zero.  In the
** case of a single process running against the table, the record count
** is also compared to the bitmap count as a kind of sanity check.  If
** only one process is using the table both counts should always be the
** same.
**
************************************************************************/
short consist_check(table_description *table_ptr)
   {
   int error_found;
	char *zerosum_column_name;
   char *abort_column_name;
   long abortsum;
   long zerosum;
   long count;
   long bit_count;
   char command[SQL_MAX_COMMAND_LENGTH];   /* used to build SELECT in */
	HENV	henv;
	HDBC	hdbc;
	HSTMT	hstmt;
	RETCODE rc;
	SQLLEN countNullIndicator;
	SQLLEN zerosumNullIndicator;
	SQLLEN abortsumNullIndicator;

   henv=table_ptr->henv;
	hdbc=table_ptr->hdbc;
	hstmt=table_ptr->hstmt;

   abortsum=-1;
   zerosum=-1;
   count=-1;
// >>> these were added to work around SQLBindCol 32-bit problem
   abortsum=0;
   zerosum=0;
   count=0;
// >>>

   LogMsg(TIMESTAMP+INFOMSG,"Checking consistency...\n");

   /* get zerosum and abort column names */
   zerosum_column_name=table_ptr->pTable->ColPtr[table_ptr->zerosum_column].CName;
   abort_column_name=table_ptr->pTable->ColPtr[table_ptr->abort_column].CName;

   /* build SELECT statement for SQL */
   sprintf(command,"SELECT COUNT(*),SUM(%s),SUM(%s) FROM %s ",
           zerosum_column_name,abort_column_name,table_ptr->pTable->TableName);

   if(gTrace) LogMsg(0,"   %s\n",command);

	// just making sure we don't have any left over transactions from
	// other functions
	rc=SQLSetConnectOption(hdbc,SQL_AUTOCOMMIT,SQL_AUTOCOMMIT_ON);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLSetConnectOption")){
		LogAllErrors(henv,hdbc,hstmt);
      return(FAILURE);
      }

	rc=SQLPrepare(hstmt,command,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLPrepare")){
		LogAllErrors(henv,hdbc,hstmt);
      return(FAILURE);
      }

	// bind all result columns
	rc=SQLBindCol(hstmt,1,SQL_C_LONG,&count,0,&countNullIndicator);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindCol")){
		LogAllErrors(henv,hdbc,hstmt);
      return(FAILURE);
      }
	rc=SQLBindCol(hstmt,2,SQL_C_LONG,&zerosum,0,&zerosumNullIndicator);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindCol")){
		LogAllErrors(henv,hdbc,hstmt);
      return(FAILURE);
      }
	rc=SQLBindCol(hstmt,3,SQL_C_LONG,&abortsum,0,&abortsumNullIndicator);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindCol")){
		LogAllErrors(henv,hdbc,hstmt);
      return(FAILURE);
      }

	rc=SQLExecute(hstmt);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLExecute")){
		LogAllErrors(henv,hdbc,hstmt);
      return(FAILURE);
      }

	rc=SQLFetch(hstmt);
	if(countNullIndicator <0) count=0;
	if(zerosumNullIndicator <0) zerosum=0;
	if(abortsumNullIndicator <0) abortsum=0;
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLFetch")){
		LogAllErrors(henv,hdbc,hstmt);
		rc=SQLFreeStmt(hstmt,SQL_CLOSE);
      if(gDebug) assert(FALSE);
		return(FAILURE);
		}

	error_found=0;
	if(zerosum!=0){
		LogMsg(ERRMSG+TIMESTAMP,"ZEROSUM of %s = %ld\n",table_ptr->pTable->TableName,zerosum);
		error_found=TRUE;
	}
	if(abortsum!=0){
		LogMsg(ERRMSG+TIMESTAMP,"ABORTSUM of %s = %ld\n",table_ptr->pTable->TableName,abortsum);
		error_found=TRUE;
		}

	/* if we're the only process using this table then let's do... */
	/* ...a little consistancy check on the number of records */
	if(table_ptr->process_count==1){
		bit_count=CountBits(BIT_ON,table_ptr->BitmapPtr);
		if(count!=bit_count){
			LogMsg(TIMESTAMP,"%s internal bitmap out of sync with table.\n"
				"bit map count=%ld  actual count=%ld\n",
				table_ptr->pTable->TableName,bit_count,count);
			error_found=TRUE;
			if(gDebug) assert(FALSE);
			}
		}

	if(error_found){
		STOP_ON_ERROR;
	}

	fflush(NULL);
	if(gDebug) {
		if((zerosum!=0)||(abortsum!=0)) assert(FALSE);
		}

	rc=SQLFreeStmt(hstmt,SQL_CLOSE);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLFreeStmt")){
		LogAllErrors(henv,hdbc,hstmt);
      return(FAILURE);
      }

	LogMsg(TIMESTAMP+INFOMSG,"Table consistency is OK\n");

   return(0);
   }
