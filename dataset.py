import ChessMain as cm
import sqlite3
conn = sqlite3.connect('Chess.db')
cur = conn.cursor()

#cur.execute('''CREATE TABLE results( statement Text ,idn INT UNIQUE PRIMARY KEY)''');

for i in range (0,2):
    
  
  
  result=cm.main()
  e.type ==p.QUIT
  cur.execute('''INSERT OR REPLACE INTO results(statement,idn)
        VALUES ( ?, ? )''', ( result,1+i) )
    
  print("check")
  #print(GameData.gameOver)
 
  conn.commit()
  print("check2")  
cur.close()    



def findMoveMinMax(gs,validMoves,depth,whiteMove):
 
   

'''
 #if GameData.gameOver==True:
    print("check1")
    result=GameData.result
    
   # cur.execute(INSERT OR REPLACE INTO results(statement,idn)
        VALUES ( ?, ? ), ( result,1+i) )
    '''