#include "include.h"
#include "defines.h"
//#include "QALib.h"
#include "table.h"
#include "globals.h"
#include "sqlproc.h"

/*****************/
/* local globals */
/*****************/
FILE *fp;
char separator[]="================================================\n";


/***********************************************************************
** print_list_items()
**
** This function is recursive and will print out all command items for
** one list.  If a nested list is encountered (when <code>==0) then
** this function calls itself to handle writing all the command items
** for that nested list.
************************************************************************/
void print_list_items( list_desc *lptr )
{
   short i;
   item_desc *iptr;

   fprintf(fp,"%d        count of items in this list\n",lptr->item_count);
   fprintf(fp,"%d        run time (in minutes)\n",lptr->duration);
   fprintf(fp,separator);

   iptr=lptr->first_item_ptr;
   for(i=0;i<lptr->item_count;i++){
      fprintf(fp,"%d        action code\n",iptr->code);
      fprintf(fp,"%d        list number, percentage, or repetition count\n",
              iptr->number);
      fprintf(fp,separator);
      if(iptr->code==REPEAT_LOOP) print_list_items(iptr->list_ptr);
      iptr=iptr->next_ptr;
      } /* end: for(i=0... */

   } /* end: print_list_items() */

/***********************************************************************
** create_process_infiles()
**
** This function will create the infiles for each of the worker processes.
************************************************************************/
short create_process_infiles()
{
   char filename[_MAX_PATH];
   process_info *ptr;
   FILE *BitmapFp;
   TableDescription *temp_ptr;
   NomadInfo *NPtr;
   TableInfo *TPtr;
   table *tptr;
   key_info *kptr;
   short i,j,k;
   short VarLength;
   char *HexStrPtr;
   char ftype;
	short rc;

   /* first fill all tables used by the processes */
   for(j=0;j<g_info.table_count;j++){
      temp_ptr=g_info.table_ptr[j];
      NPtr=temp_ptr->NomadInfoPtr;
      TPtr=temp_ptr->TableInfoPtr;

      LogPrintf("NOMAD: Initializing #TABLE%d with %ld records\n",
             j,NPtr->InitialRecordCount);

		// set up a valid statement handle to use for this table
		temp_ptr->hstmt=ghstmt;

      rc=FillTable(temp_ptr);
		if(rc!=SUCCESS){
			LogPrintf("%s  Unable to initially fill table\n",g_errstr);
			return(FAILURE);
			}

      sprintf(filename,"%s/%s_NOMAD/%sBM.bin",g_info.work_volume,
              g_info.testid,TPtr->ShortTableName);

      BitmapFp=fopen(filename,"wb");
		if(BitmapFp==NULL){
			LogPrintf("%s  unable to create/open bitmap file '%s'\n",g_errstr,filename);
			LogPrintf("   %s\n",strerror(errno));
			return(FAILURE);
			}
      fwrite(NPtr->BitmapPtr->MapPtr,NPtr->BitmapPtr->MapLen/8+1,1,BitmapFp);
      fclose(BitmapFp);
      }

   /* loop for each process, writing out its commands to its infile */
   for(i=0;i<g_info.process_count;i++){

      ptr=g_info.process_ptr[i];

      /* create the infile's filename */
      sprintf(filename,"%s/%s_NOMAD/%s%03d.in",g_info.work_volume,
              g_info.testid,
              g_info.testid,i);
      fp=fopen(filename,"w");
		if(fp==NULL){
			LogPrintf("%s  unable to create/open proccess's command file '%s'\n",g_errstr,filename);
			LogPrintf("   %s\n",strerror(errno));
			return(FAILURE);
			}

      fprintf(fp,separator);
      fprintf(fp,"== WARNING: This file is programmatically generated.\n");
      fprintf(fp,"==          Edit this file manually at your own risk.\n");
      fprintf(fp,separator);
      fprintf(fp,"== Worker Command file\n");
      fprintf(fp,"== lines starting with '==' are comments\n");
      fprintf(fp,separator);

      fprintf(fp,"%d         version identifier\n",VERSION);
      fprintf(fp,"%s/%s_NOMAD   directory used for this testid\n",
              g_info.work_volume,g_info.testid);
      sprintf(filename,"%s/%s_NOMAD/%s%03d.status",
      		  g_info.work_volume,g_info.testid,g_info.testid,i);
      fprintf(fp,"%s   status file\n",filename);

      fprintf(fp,"%s         DataSource\n",gDataSource);
		if(gUID[0]==NULL) strcpy(gUID,"NULL");
      fprintf(fp,"%s         UID\n",gUID);
		if(gPWD[0]==NULL) strcpy(gPWD,"NULL");
      fprintf(fp,"%s         PWD\n",gPWD);

      fprintf(fp,"%u         master random number generator seed\n",
              g_info.RandomSeed);
      if(ptr->seed==0) ptr->seed=rand(); /* apply default user didn't... */
                                         /* ...specify anything */
      fprintf(fp,"%d         this process's random number generator seed\n",
              ptr->seed);
      fprintf(fp,"%d         time interval for checking consistency\n",
              ptr->consist_check);
      fprintf(fp,"%d         flag to stop on a consistency error\n",
              gStopOnError);

      fprintf(fp,separator);
      fprintf(fp,"== table information\n");
      fprintf(fp,separator);
      fprintf(fp,"%d         number of tables this process will use\n",
              ptr->table_count);
      tptr=ptr->table_ptr;
      for(j=0;j<ptr->table_count;j++){
         temp_ptr=g_info.table_ptr[tptr->num];
         TPtr=temp_ptr->TableInfoPtr;
         NPtr=temp_ptr->NomadInfoPtr;
         fprintf(fp,separator);
         fprintf(fp,"%s   table name, fully qualified\n",TPtr->TableName);
         fprintf(fp,"%d   count of processes using this table\n",
                 NPtr->process_count);
         switch(TPtr->Organization){
            case KEY_SEQ: ftype='K'; break;
            case ENTRY_SEQ: ftype='E'; break;
            case RELATIVE_TABLE: ftype='R'; break;
            }
         fprintf(fp,"%c   file type of table\n",ftype);
         fprintf(fp,"%ld         maximum number of rows\n",
                 NPtr->max_records);
         sprintf(filename,"%s/%s_NOMAD/%sBM.bin",g_info.work_volume,
                 g_info.testid,TPtr->ShortTableName);
         fprintf(fp,"%s   initial bitmap file of table\n",filename);

         fprintf(fp,"%d         count of columns in key\n",
                 NPtr->key_column_count);
         kptr=NPtr->key_ptr;
         for(k=0;k<NPtr->key_column_count;k++){
            fprintf(fp,"%d    #%d column number of key\n",kptr->ColNum,k);

            /* <var_ptr> does not always point to string data so... */
            /*...we'll print it out as a printable hex string */

            /* First, adjust the length if it is a SQL varchar data type */
            VarLength=(short)TPtr->ColPtr[kptr->ColNum].DataTypeLen;
            if((TPtr->ColPtr[kptr->ColNum].pTypeInfo->SQLDataType==SQL_CHAR)||
					(TPtr->ColPtr[kptr->ColNum].pTypeInfo->SQLDataType==SQL_VARCHAR)||
					(TPtr->ColPtr[kptr->ColNum].pTypeInfo->SQLDataType==SQL_LONGVARCHAR)){
                  VarLength+=2;
                  }
            HexStrPtr=atoh(kptr->DefaultValue,VarLength);
            fprintf(fp,"%s    fixed data value for this column\n",
                    HexStrPtr);
            free(HexStrPtr);
            kptr++;
            }

         fprintf(fp,"%d   key column used by NOMAD\n",
                 NPtr->key_column_used);

         fprintf(fp,"%d   key type (0-SYSKEY, 1-PRIMARY, 2-CLUSTERING\n",
                 TPtr->KeyType);

         fprintf(fp,"%d         column number to use for zerosum\n",
                 NPtr->zerosum_column);
         fprintf(fp,"%d         column number to use for abort flag\n",
                 NPtr->abort_column);
         fprintf(fp,"%d         column number to use for last process id\n",
                 NPtr->last_process_id_column);
         fprintf(fp,"%ld         minimum record number to use\n",
                 tptr->min_range);
         fprintf(fp,"%ld         maximum record number to use\n",
                 tptr->max_range);
         tptr=tptr->next_ptr;
         } /* end: for(j=0... */
      fprintf(fp,separator);

      fprintf(fp,"%d        smallest subset size\n",ptr->min_subset_size);
      fprintf(fp,"%d        largest subset size\n",ptr->max_subset_size);

      fprintf(fp,"%d        smallest VSBB size\n",ptr->min_vsbb_size);
      fprintf(fp,"%d        largest VSBB size\n",ptr->max_vsbb_size);

      fprintf(fp,separator);
      fprintf(fp,"== TMF parameters\n");
      fprintf(fp,separator);
      fprintf(fp,"%d        abort transaction percentage\n",
              ptr->abort_percent);
      fprintf(fp,"%d        DTC transaction percentage\n",
              ptr->dtc_percent);
      fprintf(fp,"%d        minimum number of concurrent transactions\n",
              ptr->min_concurrent_trans);
      fprintf(fp,"%d        maximum number of concurrent transactions\n",
              ptr->max_concurrent_trans);
      fprintf(fp,"%d        minimum number of actions per transaction\n",
              ptr->min_trans_size);
      fprintf(fp,"%d        maximum number of actions per transaction\n",
              ptr->max_trans_size);

      fprintf(fp,separator);
      fprintf(fp,"== Trace and Debug options\n");
      fprintf(fp,separator);
		//>>>>  fprintf(fp,"%d        trace flags\n",ptr->trace_options);
      fprintf(fp,"1         trace flags\n");

      if(gDebug) ptr->debug_options=TRUE;
      else ptr->debug_options=FALSE;

		//>>>>      fprintf(fp,"%d        debug flags\n",ptr->debug_options);
      fprintf(fp,"%d        debug flags\n",gDebug);

      fprintf(fp,separator);
      fprintf(fp,"== actions to be executed\n");
      fprintf(fp,separator);

      print_list_items(&ptr->list);

      fclose(fp);
      } /* end: for(i=0... */

	return(SUCCESS);
   } /* end: create_process_infiles() */

/***********************************************************************
** start_processes()
**
** This function will start up all processes.  NOTE: all processes will
** not start doing any actual work until notified by the master process
** to start work.  This is done in an attempt to make all processes start
** executing their commands at the same time, allowing for better
** concurrency.
************************************************************************/
void start_processes()
{
	LogPrintf("Starting %d processes\n",g_info.process_count);
   char proc_name[200];
   char window_title[200];
   char infile[_MAX_PATH];
   char logfile[_MAX_PATH];
//   char errfile[_MAX_PATH];
   char filename[_MAX_PATH];
   short i;
   char CommandLine[200];
   pid_t pid;
   int status;

   /* first, delete any old START file that may have been left around */
   sprintf(filename,"%s/%s_NOMAD/START.txt",g_info.work_volume,
           g_info.testid);
   remove(filename);

   /* loop, creating each new process */
   for(i=0;i<g_info.process_count;i++){
     sprintf(proc_name,"%s%03d",g_info.testid,i);
      sprintf(infile,"%s/%s_NOMAD/%s.in",g_info.work_volume,
              g_info.testid,proc_name);
      sprintf(logfile,"%s/%s_NOMAD/%s.log",g_info.work_volume,
              g_info.testid,proc_name);
/*      sprintf(errfile,"%s.%s_NOMAD.%sERR%03d",g_info.work_volume,
              g_info.testid,g_info.testid,i);
*/
      LogPrintf("NOMAD: starting process '%s'\n",proc_name);
      sprintf(CommandLine,"%s %d %s %s",g_info.object_file,i,infile,logfile);
      LogPrintf("%s\n",CommandLine);
      pid=fork();
      if(pid < 0){
         LogPrintf("Error starting process '%s' using fork()\n",proc_name);
      }
      else if(pid == 0){

         // if pid is 0 then we are the child process from the fork
         // so we need to execute the nomad_worker program
         sprintf(CommandLine,"%d",i);
         execl(g_info.object_file,g_info.object_file,CommandLine,infile,logfile,NULL);

         // execl never returns unless there was an error
         LogPrintf("Error execl of '%s'\n",g_info.object_file);
         exit(-1);
      }
      LogPrintf("NomadWorker process %s started, pid = %d\n",proc_name,pid);
	} /* end: for(i=0... */
} /* end: start_processes() */

/***********************************************************************
** start_work()
**
** This function notifies all processes to start work by creating a file
** which all processes are waiting on.  Once a process sees that the
** file has been created it will begin executing its commands.
************************************************************************/
void start_work()
{
   char filename[_MAX_PATH];

   LogPrintf("NOMAD: notifying all processes to begin work\n");

   /* create the file which all processes are waiting for */
   sprintf(filename,"%s\\%s_NOMAD\\START.txt",g_info.work_volume,
           g_info.testid);
   fp=fopen(filename,"w");
   fclose(fp);
   } /* end: start_work() */
