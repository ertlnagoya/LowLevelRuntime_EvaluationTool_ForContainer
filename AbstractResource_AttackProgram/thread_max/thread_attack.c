#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
 
void *func_thread(void *args)
{
  int *p = (int *) args;
  printf("func_thread(): *p = %d\n", *p);
  sleep(100);
  
  return NULL;
}
 
int main(void)
{
  const int max_thread = 1000;
  int i,ret;
  pthread_t pthread_arr[max_thread];
  
  for (i = 0; i < max_thread; i++)
  {
    ret = pthread_create(&pthread_arr[i], NULL, &func_thread, &i);
    if (ret != 0) {
      fprintf(stderr, "pthread_create(): ret = %d\n", ret);
      //exit(1);
    }
  }
  
  for (i = 0; i < max_thread; i++)
  {
    ret = pthread_join(pthread_arr[i], NULL);
    if (ret != 0) {
      fprintf(stderr, "pthread_join(): ret = %d\n", ret);
      //exit(2);
    }
  }
  
  return 0;
}
