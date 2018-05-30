#include<stdio.h>


main()
{
	
	
FILE *fp;
fp = fopen("/home/samad/bach-rpc/C/cred.db", "r");
char e;
while (e != EOF) {

	fscanf(fp, "%s" , e);
	printf("1 : %s\n", e );
	
	
}





fclose(fp);
}
