import re
f = open("database.txt", "r")
f1 = open("demofile3.txt", "a")
flag=0
opening=dict()
i=0
for x in f:
   line =str(x)
   email=""
   if not (line.startswith('[Opening') or line.startswith('1')):
     continue
   if  (line.startswith('[Opening') ):
     if line in opening:
        flag=0
        continue
     else:
         opening.update(line=1)
         lin1=line
         flag=1
         i+=1
   if(flag==1):
       if line.startswith('1'):
          line =str(re.findall('[a-zA-Z0-9]+.+\S+\s+10',line))
          opening.update(lin1=line)
          f1.write(lin1)
          f1.write('\n')
          f1.write(line)
          f1.write('\n')
          print(line,lin1)
   
   if(i==500):
      break



f1.close()
f.close()


 if  gs.fen() in transpositionTable.keys():  
     nextMove=transpositionTable[gs.fen()]
     print("use of trnasp",nextMove)
     print(gs.fen())
     Tcounter+=1
     return turnMultiplier*scoreBoard(gs)