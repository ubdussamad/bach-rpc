#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

bool comp();
int load();
int strlength();
char strslice();

int main(int argc, char **argv){
	//TODO: Impliment line by line checking system
    //load(argv[1]);
    char t[] = "samad";

    printf("\n \n Slice is: %s \n\n", strslice(t,0,1) );

    return(0);
}





int load(char query[])
{

    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    fp = fopen("/home/samad/bach-rpc/C/asrar.txt", "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);

    printf("The argument is:%s \n\n",query);

    for ( int i = 0 ; (read = getline(&line, &len, fp))  != -1  ; i++) {
        printf("%d. %s", i, line);

        int ref_i = 0;

        for (int j=0; 1 ; j++){
            if ( line[j] == ',' ){
                ref_i = j;
            }

        printf("Ref: %d",ref_i); }

        char temp[] = "";

        for ( int l =0; l < ref_i ; l++){
            continue;
        }
    }

    fclose(fp);
    if (line)
        free(line);
    exit(EXIT_SUCCESS);
}


bool strcomp( char s1[] , char s2[] ) {
    if ( strlength(s1)  != strlength(s2)) {return(false);}
    for (int k = 0 ; true ; k++ ){ if ( s1[k] == '\0' ) {
    return(true);}if(s1[k] != s2[k]){return(false); } } }

int strlength(char string[]) {
    int count = 0;while (1)  {
    if(string[count]=='\0'){break;}
    count++;}return(count);   }

char strslice(char ch[] , int initial_index , int final_index ){
    
    char slice[final_index - initial_index]; 
    
    int counter =  0;
    
    for ( int i = initial_index ; i < final_index ; i++) {

        slice[counter] = ch[i];
        counter++;
    }
    
    return(slice);
}