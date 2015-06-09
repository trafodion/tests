#include "defines.h"
#include "include.h"
#include "table.h"
#include "mstruct.h"
#include "globals.h"

/***********************************************************************/
/* Local Globals (global to only the functions within this source file */
/***********************************************************************/
char lg_line_buffer[255];
char *lg_line_ptr;

/***********************************************************************
** get_next_line()
**
** This function gets the next line from the input file and resets the
** local global pointers at the beginning of the new line.  If there
** are not any more lines to read in then EOF is returned.
************************************************************************/
short get_next_line()
{
   /* loop until the line is not a comment line */
   do{

      /* get next line and check for end-of-file */
      lg_line_ptr=get_s(lg_line_buffer);
      if(lg_line_ptr==NULL) {
         if(feof(stdin)) return(EOF);
         return((short)ferror(stdin));
         }

      /* display the line */
      printf("%s\n",lg_line_ptr);

      /* skip over any leading blanks or tabs */
      while((*lg_line_ptr==BLANK)||(*lg_line_ptr==TAB)) lg_line_ptr++;

      } while((strncmp(lg_line_ptr,"==",2)==0)||
              (*lg_line_ptr=='!')||
              (strlen(lg_line_ptr)==0));

   /* convert it to upper case and strip out underscores */
//>>> try not skipping underscores, means we can't have "_" in keywords anymore
//   remove_char(toupper_s(lg_line_buffer),(char)'_');

   /* convert it to upper case */
   toupper_s(lg_line_buffer);

   /* if trace option set, print line */
   if(gTrace&TRACE_TOKENS) printf("get_next_line(): %s\n",lg_line_ptr);

   return(0);
   } /* end: get_next_line() */


/**********************************************************************
** next_token()
**
** This function gets the next token (as defined by the token table)
** and returns its value.  It also sets <g_current_token> to that value
** and <g_token_string> to the character string of that token.  This
** function provides a constant stream of tokens until EOF is reached.
** next_token() will handle reading in the next line when end-of-line
** is reached.
***********************************************************************/
short next_token()
{
   char *str_ptr;           /* pointer to <g_token_string> buffer */
   short i;
   #include "Tokens.c"       /* token table declarations */

   /* skip over any blanks */
   while(*lg_line_ptr==BLANK) lg_line_ptr++;

   /* if at end-of-line, then get next line */
   if(*lg_line_ptr==NULL) {
      if(get_next_line()==EOF){
         g_current_token=EOF;
         g_token_string[0]=NULL;

         /* if trace option set, print token info */
         if(gTrace&TRACE_TOKENS) printf("next_token(): g_current_token=%d  "
                                         "g_token_string=<EOF>\n",
                                         g_current_token);
         return(g_current_token);
         }
      }

   /************************************************/
   /* peel off next token string into token buffer */
   /************************************************/
   /* set pointer to beginning of token string buffer ready to copy... */
   /* ... token string into it */
   str_ptr=g_token_string;

   /* if first character is a letter (or a "$" to handle filenames)... */
   /* ...then copy until it is not a letter or number (or a "." to... */
   /* ...handle filenames as well as "_" to handle ANSI names ) */
   if(isalpha(*lg_line_ptr)||*lg_line_ptr=='$'){
      *str_ptr++=*lg_line_ptr++;
      while(isalnum(*lg_line_ptr)||*lg_line_ptr=='.'||*lg_line_ptr=='_'){
         *str_ptr++=*lg_line_ptr++;
         }
      }

   /* if first character is a number then copy until it is not a number */
   else if(isdigit(*lg_line_ptr)){
      while(isdigit(*lg_line_ptr)) *str_ptr++=*lg_line_ptr++;

      /* put a NULL on the end of the token string buffer */
      *str_ptr=NULL;
      g_current_token=NUMBER;

      /* if trace option set, print token info */
      if(gTrace&TRACE_TOKENS) printf("next_token(): g_current_token=%d  "
                                      "g_token_string='%s'\n",g_current_token,
                                      g_token_string);

      return(g_current_token);
      }

   /* if first character is '#' then it must be the beginning of a ... */
   /* ...variable name.  Copy until it is not a letter or number */
   else if(*lg_line_ptr=='#'){
      *str_ptr++=*lg_line_ptr++;
      while(isalnum(*lg_line_ptr)) *str_ptr++=*lg_line_ptr++;
      }

   /* if first character is any other punctuaction character then ... */
   /* copy just that character */
   else if(ispunct(*lg_line_ptr)) *str_ptr++=*lg_line_ptr++;

   /* if not any of the above then it must be an invalid character */
   else {
      *str_ptr++=*lg_line_ptr++;
      *str_ptr=NULL;
      g_current_token=INVALID_CHARACTER;

      /* if trace option set, print token info */
      if(gTrace&TRACE_TOKENS) printf("next_token(): g_current_token=%d  "
                                      "g_token_string='%s'\n",g_current_token,
                                      g_token_string);

      return(g_current_token);
      }

   /* put a NULL on the end of the token string buffer */
   *str_ptr=NULL;

   /* search for a match in the token table */
   for(i=0;i<NUMBER_OF_TOKENS;i++){

      /* if found return token value */
      if(strcmp(g_token_string,token[i].string)==0) {
         g_current_token=token[i].value;

         /* if trace option set, print token info */
         if(gTrace&TRACE_TOKENS) printf("next_token(): g_current_token=%d  "
                                   "g_token_string='%s'\n",g_current_token,
                                   g_token_string);

         return(g_current_token);
         }
      }

   /* if not a standard token then it might be a #TABLEn or #PROCESSn... */
   /* ...identifier, which is handled as a special token */
   if(g_token_string[0]=='#') {
      if(strncmp(g_token_string,"#TABLE",6)==0) {
         g_current_token=TABLE_N;
         }
      else if(strncmp(g_token_string,"#PROCESS",8)==0) {
         g_current_token=PROCESS_N;
         }
      else {
         printf("%s unknown variable '%s'\n",g_errstr,g_token_string);
         return(FAILURE);
         }

      /* if trace option set, print token info */
      if(gTrace&TRACE_TOKENS) printf("next_token(): g_current_token=%d  "
                                      "g_token_string='%s'\n",g_current_token,
                                      g_token_string);
      return(g_current_token);
      }

   /* if not a standard or variable-name token then return... */
   /* ...token value of STRING */
   g_current_token=STRING;

   /* if trace option set, print token info */
   if(gTrace&TRACE_TOKENS) printf("next_token(): g_current_token=%d  "
                                   "g_token_string='%s'\n",g_current_token,
                                   g_token_string);
   return(g_current_token);

   } /* end: next_token() */

