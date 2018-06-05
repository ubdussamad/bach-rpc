#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

bool comp();
short load();
short strlength();
char * strslice();
void slice_str();


int main(int argc, char **argv){
	//TODO: Impliment line by line checking system
    load(argv[1]);
    return(0);
}





short load(char query[])
{

    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    fp = fopen("/home/samad/bach-rpc/C/s9.db", "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);
    //printf("The argument is:%s \n\n",query);
    for ( short i = 0 ; (read = getline(&line, &len, fp))  != -1  ; i++) {
        //printf("\n%d. %s", i, line);

        short ref_i = 0;

        for (short j=0; 1 ; j++){


            if ( line[j] == ',' ){
                ref_i = j;
                break;
            }
        } 
        
        char buffer[ref_i+1];

        slice_str( line , buffer , 0 , ref_i-1 );

        //printf("\n  Index: %s and Query is: %s \n", buffer ,query);

        //printf("\n %s \n",buffer);

        if ( strcmp( query , buffer ) == 0) {
            printf("\n User Exists \n");
        }
    }

    fclose(fp);
    if (line)
        free(line);
    exit(EXIT_SUCCESS);
}


bool strcomp( char s1[] , char s2[] ) {
    if ( strlength(s1)  != strlength(s2)) {return(false);}
    for (short k = 0 ; true ; k++ ){ if ( s1[k] == '\0' ) {
    return(true);}if(s1[k] != s2[k]){return(false); } } }

short strlength(char string[]) {
    short count = 0;while (1)  {
    if(string[count]=='\0'){break;}
    count++;}return(count);   }

char * strslice(char ch[] , int initial_index , int final_index ){
    char slice[final_index - initial_index]; 
    short counter =  0;
    for ( short i = initial_index ; i < final_index ; i++) {
        slice[counter] = ch[i]; counter++; }
    char *string = slice;
    return( string );
}


void slice_str(const char * str, char * buffer, size_t start, size_t end)
{
    size_t j = 0;
    for ( size_t i = start; i <= end; ++i ) {
        buffer[j++] = str[i];
    }
    buffer[j] = 0;
}