import msvcrt
import sys
import time

class TimeoutExpired(Exception):
    pass

def input_with_timeout(prompt, timeout, timer=time.monotonic):
    print(prompt)
    endtime = timer() + timeout
    result = []
    while timer() < endtime:
        if msvcrt.kbhit():
            result.append(msvcrt.getwche()) #XXX can it block on multibyte characters?
            if result[-1] == '\r':
                return ''.join(result[:-1])
        time.sleep(0.04) # just to yield to other processes/threads
    raise TimeoutExpired

if __name__ == '__main__':
    try:
        answer = input_with_timeout("O número sorteado está na(S/N)?", 10) 
    except TimeoutExpired:
        print('Tempo esgotado')
    else:
        if answer == 'S':
            print('Você diz ver o número!')
        elif answer == 'N':
            print('Você disse não ver o número')