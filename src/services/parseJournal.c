#include <string.h>
#include <systemd/sd-journal.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

//

int main(int argc, char **argv){
  sd_journal *j;
  const void *data;
  //char field[] = "MESSAGE";
  //const char *field;

  size_t length;
  int i;

  char *(match[]) = {
    "_PID=1",
    //argv[1]
    "UNIT=httpd.service"
    //"UNIT=bluetooth.service"
  };
  char newline[]="\n";
  sd_journal_open(&j,0);
  
  for(i=0;i<sizeof(match)/sizeof(char *);++i){
      sd_journal_add_match(j,match[i],strlen(match[i]));
  }

  while(sd_journal_next(j)>0){

      while(sd_journal_enumerate_data(j,&data,&length)){
        write(1,data,length);
        write(1,newline,1);
      }
      write(1,newline,1);
  }

  return 0;
}
