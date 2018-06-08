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
	//TODO: Impliment line by line checking system

    char buffer[100];
    user_query(argv[1],&buffer);
    printf("\n%s\n",buffer);
    /*if (argv[1] == 'a') {
        append_user(argv[2],argv[3],argv[4]);
    }

    if (argv[1] = 'q'){
        char buffer[100];
        user_query(argv[2],&buffer);
        printf(buffer);
    }
    */
    return (0);
}

// Modifies the second parameter to the output genrated by the query */
// Returns 0 if the query is valid else 1
int user_query (char query[], char *ch) {
  FILE *fp;char *line = NULL;size_t len = 0;ssize_t read;
  fp = fopen ("asrar.txt", "r");if (fp == NULL)
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
    fp = fopen("asrar.txt", "a");
    char buffer[ ( ( last_usr()+1 )%10 ) + 1];
    //itoa(last_usr()+1, buffer, 10);
    fprintf(fp, "%s,%s,%s,%s", usr , pwd , auth  , buffer) ;
    fclose(fp);
    return 0;
}

//max username length is 50 characters
long unsigned int last_usr(void ) {
    FILE *fd;
    char filename[] = "asrar.txt";
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
