#!/bin/sh
# lucas series
if [ -z "$COUNT" ]
then
    /bin/echo -n "COUNT is empty"
else
    N=$COUNT
    a=2
    b=1  
    i=0
    while [ "$i" -lt "$N" ] 
    do
        /bin/echo -n "$a "
        fn=$(( a + b )) 
        a=$b
        b=$fn
        i=$(( i + 1 ))
    done
fi