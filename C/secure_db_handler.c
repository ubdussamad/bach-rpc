#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

int append_user();
int user_query();
short strlength();
void slice_str();
long unsigned int last_usr();


int main(int argc, char **argv){

    if (strcmp(argv[1],"-a") == 0) {
        append_user(argv[2],argv[3],argv[4]);
    }

    else if (strcmp(argv[1],"-q") == 0){
        char buffer[100];
        user_query(argv[2],&buffer);
        printf("%s",buffer);
    }
    else if (strcmp(argv[1],"-help") == 0){
        printf("Usage: bach [OPTION]... [Args]...\nQuery/Append/Delete administrative database stored in local directory.\nOptions are sorted alphabetically\nArguments should be seprated by spaces.\n\n    OPTIONS |         ARGUMENTS       | DESCRIPTION\n\n      -q             [username]         Query the database for the \n                                        details of given username\n\n      -a      [username password auth]  Append new user to the \n                                        database.\n\nProject BachmanitY 2018.\nVisit : https://github.com/ubdussamad/bach-rpc for more details.\nAuthor: Ubdussamad <ubdussamad@gmail.com>.\nBach Simple Database Management System. \n");
    }
    else {
        printf("bach: invalid option \'%s\'\nTry 'bach -help' for more information.\n",argv[1]);
    }
    return (0);
}

// Modifies the second parameter to the output genrated by the query */
// Returns 0 if the query is valid else 1
int user_query (char query[], char *ch) {
  FILE *fp;char *line = NULL;size_t len = 0;ssize_t read;
  fp = fopen ("asrar.db", "r");if (fp == NULL)
  {exit (EXIT_FAILURE);}for (short i = 0; (read = getline (&line, &len,
  fp)) != -1; i++){short ref_i = 0; for (short j = 0; 1; j++){if (line[j] == ',')
  {ref_i = j;break;}} char buffer[ref_i + 1]; slice_str (line, buffer, 0,
  ref_i - 1);if (strcmp (query, buffer) == 0){int end = strlength (line);
  char temp[end - ref_i + 1];slice_str (line, &temp, ref_i + 1, end);
  strcpy(ch,temp); fclose (fp); if (line) { free (line); } return 0; } } 
  strcpy(ch,"Bad User.");fclose (fp); if (line) {free (line);} return 1; }

// Adds a new line to to the end of the file and return 0
int append_user (char usr[] , char pwd[] , char auth[]){
    FILE *fp;
    fp = fopen("asrar.db", "a");
    


    const int n = snprintf(NULL, 0, "%lu", last_usr()+1);
    char buf[n+1];
    int c = snprintf(buf, n+1, "%lu", last_usr()+1);



    fprintf(fp, "%s,%s,%s,%s\n", usr , pwd , auth  , buf) ;
    fclose(fp);
    return 0;
}

//max username length is 50 characters
long unsigned int last_usr(void ) {
    FILE *fd;
    char filename[] = "asrar.db";
    static const long max_len = 102;
    char buff[max_len + 1];
    if ((fd = fopen(filename, "rb")) != NULL)  {
        fseek(fd, -max_len, SEEK_END);
        fread(buff, max_len-1, 1, fd);
        fclose(fd);
        buff[max_len-1] = '\0';             
        char *last_newline = strrchr(buff, '\n'); 
        char *last_line = last_newline+1;
    short length = strlength(last_line);
    short index = 0;
    for ( short i = 0; i < length ; i++) {
        if (last_line[i] == ','){ index = i; } }
    char buffer[length - index + 1];
    slice_str(last_line , buffer , index+1 , length);
    return (strtol(buffer,NULL,10)); }}


// Returns the length of array of characters or srting
short strlength(char string[]) {
    short count = 0;while (1)  {
    if(string[count]=='\0'){break;}
    count++;}return(count);   }

// Modifies the buffer to the slice.
// Retuns Nothing.
void slice_str(const char * str, char * buffer, size_t start, size_t end) {
    size_t j = 0;
    for ( size_t i = start; i <= end; ++i ) {
    buffer[j++] = str[i]; } buffer[j] = 0; }
