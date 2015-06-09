#include "defines.h"
#include "include.h"
#include "bitlib.h"
#include "table.h"
#include "struct.h"
#include "globals.h"

/*************************************************************************
** get_str()
**
** This function is a modified "gets()" in that it skips comment lines.
** In this case a comment line is a line that starts with '=='.
*************************************************************************/
char *get_str(char *str_ptr)
{
   char *status;

   /* loop until input line is not a comment line */
   do {
      status=get_s(str_ptr);
      } while((status!=NULL) && (strncmp(str_ptr,"==",2)==0));

   if(status==NULL) return(NULL);
   return(str_ptr);
   }

/**********************************************************************
** get_loop_items()
**
** This functions is recursive and will read in all command items for
** one loop.  If a nested loop is encountered (when <code>==0) then
** this function calls itself to handle getting all the command items
** for that nested loop.
**********************************************************************/
short get_loop_items(short loop_num)
{
   char input_line[255];
   list_desc *l_ptr;
   short i;
   short item_count;

   sscanf(get_str(input_line),"%hd ",&item_count);
   gpList[loop_num]=(list_desc *)malloc(sizeof(list_desc)+
                                ((item_count-1)*sizeof(struct item_desc)));
   l_ptr=gpList[loop_num];

   l_ptr->item_count=item_count;
   sscanf(get_str(input_line),"%hd ",&l_ptr->duration);

   for(i=0;i<item_count;i++){
      sscanf(get_str(input_line),"%hd ",&l_ptr->item[i].code);
      sscanf(get_str(input_line),"%hd ",&l_ptr->item[i].u1.number);
      if(l_ptr->item[i].code==0) get_loop_items(l_ptr->item[i].u1.number);
      }
   return(0);
   } /* end of get_loop_items() */

/*************************************************************************
** get_commands()
**
** This function opens the command file (stdin) and reads in all the
** info needed for a process's specific run.
*************************************************************************/
short get_commands()
{
   char input_line[100];
   char table_bitmap_filename[80];
   FILE *BitmapFp;
   short i,j;
   key_info *kptr;
   char KeyHexStr[SQL_MAX_KEY_LENGTH*2+1];
	FILE *Mystdin;
	short rc;

	char DontCare_file_type;
	short DontCare_key_type;

   rc=SUCCESS;

	/* no need to reopen the command file since "stdin" is automatically... */
   /* ...opened when the program starts running. */
	Mystdin=freopen(gCommandFile, "r", stdin );
//>>>>Mystdin is NULL for some reason
	if(Mystdin==NULL){
		LogMsg(ERRMSG,"unable to open command file '%s'\n",gCommandFile);
		LogMsg(NONE,"     %s\n",strerror(errno));
		return(FAILURE);
	}

   sscanf(get_str(input_line),"%ld ",&gVersion);
   if(gVersion!=VERSION){
	   LogMsg(ERRMSG,"Version mismatch: Master version = %ld, Worker version=%d\n",
		   gVersion,VERSION);
       return(FAILURE);
   }

   sscanf(get_str(input_line),"%s ",g_testid_dir);
   sprintf(gStartFile,"%s/START.txt",g_testid_dir);
   sprintf(gStopFile,"%s/STOP.txt",g_testid_dir);

   sscanf(get_str(input_line),"%s ",g_status_file);

   sscanf(get_str(input_line),"%s ",gDataSource);
   sscanf(get_str(input_line),"%s ",gUID);
	if(strcmp(gUID,"NULL")==0) gUID[0]=NULL;
   sscanf(get_str(input_line),"%s ",gPWD);
	if(strcmp(gPWD,"NULL")==0) gPWD[0]=NULL;

   sscanf(get_str(input_line),"%ld ",&gMasterSeed);
   sscanf(get_str(input_line),"%ld ",&gSeed);
   srand(gSeed);    /* initialize the pseudo-random number generator */

   sscanf(get_str(input_line),"%ld ",&gCheckInterval);
   gCheckInterval*=60;     /* convert from minutes to seconds */

   sscanf(get_str(input_line),"%d ",&gStopOnError);

	sscanf(get_str(input_line),"%ld ",&gTableCount);
   for(i=0;i<gTableCount;i++){
      gpTableDesc[i]=(table_description *)malloc(sizeof(table_description));
      sscanf(get_str(input_line),"%s ",gpTableDesc[i]->TableName);
      sscanf(get_str(input_line),"%hd ",&gpTableDesc[i]->process_count);

		sscanf(get_str(input_line),"%c ",&DontCare_file_type);
		switch(DontCare_file_type){
			case 'K': gpTableDesc[i]->Organization=KEY_SEQ; break;
			case 'R': gpTableDesc[i]->Organization=RELATIVE_TABLE; break;
			case 'E': gpTableDesc[i]->Organization=ENTRY_SEQ; break;
			default:gpTableDesc[i]->Organization=KEY_SEQ; break;
			}

      sscanf(get_str(input_line),"%ld ",&gpTableDesc[i]->max_records);

		gpTableDesc[i]->BitmapPtr=QACreateBitmap(gpTableDesc[i]->max_records);

		sscanf(get_str(input_line),"%s ",table_bitmap_filename);
      BitmapFp=fopen(table_bitmap_filename,"rb");
		if(BitmapFp==NULL){
			LogMsg(ERRMSG,"unable to open bitmap file '%s'\n",table_bitmap_filename);
			rc=FAILURE;
			}
		else{
			fread(gpTableDesc[i]->BitmapPtr->MapPtr,gpTableDesc[i]->BitmapPtr->MapLen/8+1,1,BitmapFp);
		   fclose(BitmapFp);
			}
      sscanf(get_str(input_line),"%hd ",&gpTableDesc[i]->key_column_count);

      gpTableDesc[i]->key_ptr=(key_info *)malloc(sizeof(key_info)*
                                               gpTableDesc[i]->key_column_count);
      kptr=gpTableDesc[i]->key_ptr;
      for(j=0;j<gpTableDesc[i]->key_column_count;j++){
         sscanf(get_str(input_line),"%hd ",&kptr->ColNum);
         sscanf(get_str(input_line),"%s ",KeyHexStr);
         kptr->DefaultValue=HexStrToBytes(KeyHexStr);
         kptr++;
         }


      sscanf(get_str(input_line),"%hd ",&gpTableDesc[i]->key_column_used);
      sscanf(get_str(input_line),"%hd ",&DontCare_key_type);
      sscanf(get_str(input_line),"%hd ",&gpTableDesc[i]->zerosum_column);
      sscanf(get_str(input_line),"%hd ",&gpTableDesc[i]->abort_column);
      sscanf(get_str(input_line),"%hd ",&gpTableDesc[i]->last_process_id_column);
      sscanf(get_str(input_line),"%ld ",&gpTableDesc[i]->min_range);
      sscanf(get_str(input_line),"%ld ",&gpTableDesc[i]->max_range);
      if(gpTableDesc[i]->max_range==0){
         gpTableDesc[i]->min_range=0;
         gpTableDesc[i]->max_range=gpTableDesc[i]->max_records-1;
         }
      }

   sscanf(get_str(input_line),"%ld ",&min_subset_size);
   sscanf(get_str(input_line),"%ld ",&max_subset_size);
   sscanf(get_str(input_line),"%ld ",&min_vsbb_size);
   sscanf(get_str(input_line),"%ld ",&max_vsbb_size);

   sscanf(get_str(input_line),"%ld ",&abort_trans);
   sscanf(get_str(input_line),"%ld ",&dtc_trans);
   sscanf(get_str(input_line),"%ld ",&min_concurrent_trans);
   sscanf(get_str(input_line),"%ld ",&max_concurrent_trans);
   sscanf(get_str(input_line),"%ld ",&min_actions_per_trans);
   sscanf(get_str(input_line),"%ld ",&max_actions_per_trans);

   sscanf(get_str(input_line),"%ld ",&gTrace);
   sscanf(get_str(input_line),"%ld ",&gDebug);

   /* now read in the list(s) of actions to be executed */
   get_loop_items(0);

	fclose(Mystdin);

   return(rc);
   } /* end of get_commands() */

