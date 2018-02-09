""" 'symbol' 'dicword' '0-9' 'symbol' '00 - 99' """

""" number word(random cap letter) 3### number"""

#imports
import random 

#vaibles
word_file = "words.txt"
WORDS = open(word_file).read().splitlines()
""" Not used anymore
symbollist = ['!', '@', '#','$', '%', '^', '&', '*', '(', ')', '_', '+', '-',]
"""
start = 0

line = 0
# loop, this will currently create 3003 passwords that match the scheme. 1 password per line.
while start <= 10000:
        password = WORDS[random.randint(0, 25486)].title() + WORDS[random.randint(0, 25486)].title() + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
        file = open('password.txt','a') 
        file.write( password + "\n")
        file.write('Time Entered: __________' + '\t' +'\t' + 'Time Retired: __________ ' + "\n")
        file.write("---------------------------------------------------") 
        print(start)
        
        line +=1
        if line % 13 == 0:
            file.write(" " + '\n' + '\n') 
            print("LOOOOK ATTT MEEE")
            
        start += 1
    
#close file    
file.close() 