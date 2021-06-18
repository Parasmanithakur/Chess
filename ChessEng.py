import numpy
class GameState():
   board=list()
   def __init__(self):
      
      ''' self.board= [['--','--','--','--','--','--','--','--'],
      ['--','--','--','--','--','--','--','--'],
      ['--','--','--','--','--','--','--','--'],
      ['--','--','--','--','--','--','--','--'],
      ['--','--','--','--','--','--','--','--'],
      ['--','--','--','--','--','--','--','--'],
      ['--','--','--','--','--','--','--','--'],
      ['--','--','--','--','--','--','--','--']] '''
      self.board= [ ['bR','bN','bB','bQ','bK','bB','bN','bR'],['bP','bP','bP','bP','bP','bP','bP','bP'],['--','--','--','--','--','--','--','--'],['--','--','--','--','--','--','--','--'],['--','--','--','--','--','--','--','--'],['--','--','--','--','--','--','--','--'],['wP','wP','wP','wP','wP','wP','wP','wP'],['wR','wN','wB','wQ','wK','wB','wN','wR']]
      
      self.moveFunctions ={'P':self.getPawnMoves,'R':self.getRookMoves,'Q':self.getQueenMoves,'K':self.getKingMoves,'B':self.getBishopMoves,'N':self.getKnightMoves}            
      self.whiteMove =True
      self.moveLog=[]
      self.whiteKingLocation =(7,4)
      self.blackKingLocation =(0,4)
      self.checkmate=False
      self.stalemate=False
      self.enpassantPossible=() #square of enpassnat possible
      self.enpassantPossibleLog =[self.enpassantPossible]
      self.currentCastlingRight=CastleRights(True,True,True,True)
      #self.currentCastlingRight=CastleRights(False,False,False,False)
      self.castleRightsLog =[CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,self.currentCastlingRight.wqs,self.currentCastlingRight.bqs)]
      self.fenS=""
   def makeMove(self,move): 
      self.board[move.startRow][move.startCol] ="--"
      self.board[move.endRow][move.endCol]= move.pieceMoved  
      self.moveLog.append(move)
      self.whiteMove =not self.whiteMove
      
      if move.pieceMoved =='wK':
         self.whiteKingLocation=(move.endRow,move.endCol)
      elif move.pieceMoved =='bK':
      
         self.blackKingLocation=(move.endRow,move.endCol)
      #pawn Promotion
      if move.isPawnPromotion:
           self.board[move.endRow][move.endCol]= move.pieceMoved[0] +'Q'      
      #enPassant move
      if move.isEnpassantMove:
         self.board[move.startRow][move.endCol]='--'
      #update enpassnat
      if( move.pieceMoved[1]=='P' and abs(move.startRow-move.endRow)==2):
        self.enpassantPossible =((move.startRow +move.endRow)//2,move.endCol)
      #  print(self.enpassantPossible)
      else :
        self.enpassantPossible=()  
      if move.isCastleMove:  
         if move.endCol-move.startCol==2: #king side castle
            self.board[move.endRow][move.endCol-1] =self.board[move.endRow][move.endCol+1]
            self.board[move.endRow][move.endCol+1]='--' #erase the rook
         else: #Queen Side castle
            self.board[move.endRow][move.endCol+1] =self.board[move.endRow][move.endCol-2]
            self.board[move.endRow][move.endCol-2]='--' #erase the rook
      self.enpassantPossibleLog.append(self.enpassantPossible)
      #updating CastleRights               
      self.updateCastleRights(move) 
      self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks
          ,self.currentCastlingRight.wqs,self.currentCastlingRight.bqs) )     
      
         
   def undoMove(self):
   
        if len(self.moveLog) != 0:#cant undo before first move
         move=self.moveLog.pop()
         self.board[move.startRow][move.startCol]=move.pieceMoved
         self.board[move.endRow][move.endCol]= move.pieceCaptured
         self.whiteMove = not self.whiteMove
         if move.pieceMoved =='wK':
           self.whiteKingLocation=(move.startRow,move.startCol)
         if move.pieceMoved =='bK':
           self.blackKingLocation=(move.startRow,move.startCol)
         #Undo En passant
         if move.isEnpassantMove:
           self.board[move.endRow][move.endCol]='--' #leaving landing square blank
           self.board[move.startRow][move.endCol]=move.pieceCaptured
         self.enpassantPossibleLog.pop()
         self.enpassantPossible =self.enpassantPossibleLog[-1]         
          # self.enpassantPossible=(move.endRow,move.endCol)
         #undo a 2 square pawn advance
         # if (move.pieceMoved[1]=='P' and abs (move.startRow-move.endRow)==2):
           # self.enpassantPossible=() 
         #undo castling Rights
         self.castleRightsLog.pop() #removing CRights of undo move
         newRights =self.castleRightsLog[-1]  #setting current castling right to now last move    
         self.currentCastlingRight =CastleRights(newRights.wks,newRights.bks,newRights.wqs,newRights.bqs)
         #undo Castle move
         if move.isCastleMove:
           if move.endCol-move.startCol==2:#king side  
             self.board[move.endRow][move.endCol+1] =self.board[move.endRow][move.endCol-1]
             self.board[move.endRow][move.endCol-1]='--'
           else: #queen Side
               self.board[move.endRow][move.endCol-2] =self.board[move.endRow][move.endCol+1]
               self.board[move.endRow][move.endCol+1]= '--'
         self.checkmate=False
         self.stalemate= False         
   def updateCastleRights(self,move):
     if move.pieceMoved =='wK':
        self.currentCastlingRight.wks =False
        self.currentCastlingRight.wqs =False
     elif move.pieceMoved =='bK':
        self.currentCastlingRight.bks =False
        self.currentCastlingRight.bqs =False
     elif move.pieceMoved == 'wR':
        if move.startRow ==7:
           if move.startCol ==0: #left rook
                     self.currentCastlingRight.wqs =False
           elif move.startCol ==7:
                   self.currentCastlingRight.wks =False
     elif move.pieceMoved == 'bR':
        if move.startRow ==0:
           if move.startCol ==0:#left rook
                     self.currentCastlingRight.bqs =False
           elif move.startCol ==7:#right rook
                   self.currentCastlingRight.bks =False
     #if a rook is captured
     if move.pieceCaptured=='wR':
       if move.endRow==7:
           if move.endCol==0:
               self.currentCastlingRight.wqs =False
           elif move.endCol==7:
               self.currentCastlingRight.wks=False
     elif move.pieceCaptured=='bR':
       if move.endRow==0:
           if move.endCol==0:
               self.currentCastlingRight.bqs =False
           elif move.endCol==7:
               self.currentCastlingRight.bks=False                
                        
        
   def getAllPossibleMoves(self):
      
      moves =[]
      
      for r in range(len(self.board)):
        for c in range(len(self.board[r])):
           turn =self.board[r][c][0]
           if(turn =='w' and self.whiteMove) or(turn =='b' and not self.whiteMove):   
             piece=self.board[r][c][1]
             self.moveFunctions[piece](r,c,moves)
                          
               
      return moves    
   def getValidMoves(self):
       '''for log in self.castleRightsLog:
       # print(log.wks,log.wqs,log.bks,log.bqs)
      #print()'''
       tempEnpassantPossible =self.enpassantPossible 
       tempCastleRights =CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,self.currentCastlingRight.wks,self.currentCastlingRight.bqs)
       #1 Genrate all possible moves
       moves= self.getAllPossibleMoves() 
       if self.whiteMove:
         self.getCastleMoves(self.whiteKingLocation[0],self.whiteKingLocation[1],moves)
       else: 
          self.getCastleMoves(self.blackKingLocation[0],self.blackKingLocation[1],moves)        
       #2 for each move,make the move       
       for i in range(len(moves)-1,-1,-1):
           self.makeMove(moves[i])
       #3 genrate all opnent move
       #4 for each such move check king is attack
           self.whiteMove=not self.whiteMove
           if self.inCheck():
             moves.remove(moves[i]) #removin invalid moves as king is attack
           self.whiteMove =not self.whiteMove
           self.undoMove()
       if len(moves) ==0:
          if self.inCheck():
             self.checkmate =True
          else:
             self.stalemate= True
       else:
          self.checkmate=False
          self.stalemate=False          
       self.enpassantPossible = tempEnpassantPossible 
       self.currentCastlingRight=tempCastleRights
       return moves    
       
   def inCheck(self):
     if self.whiteMove:
        return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
     else :
        return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])
        
    
   def squareUnderAttack(self,r,c):    
      self.whiteMove = not self.whiteMove
      oppMoves =self.getAllPossibleMoves()
      self.whiteMove =not self.whiteMove
      for move in oppMoves:
         if move.endRow ==r and move.endCol==c:
           return True
      return False     
      
   def getPawnMoves (self,r,c,moves):
       if self.whiteMove:
          if self.board[r-1][c] =="--": #one squre pawn move
            moves.append(Move((r,c),(r-1,c),self.board))
            if r==6 and self.board[r-2][c]=="--":
              moves.append(Move((r,c),(r-2,c),self.board))
          if c-1>=0:
            if self.board[r-1][c-1][0]=='b': #enemey piece
               
              
               moves.append(Move((r,c),(r-1,c-1),self.board))
            elif (r-1,c-1)==self.enpassantPossible:
             #print(r-1,c-1,"is WL")
               moves.append(Move((r,c),(r-1,c-1),self.board,isEnpassantMove=True) )          
          if c+1<=7:
                if self.board[r-1][c+1][0]=='b': #enemey piece
                  moves.append(Move((r,c),(r-1,c+1),self.board)) 
                elif (r-1,c+1)==self.enpassantPossible:
                  # print(r-1,c+1,"is WR")
                   moves.append(Move((r,c),(r-1,c+1),self.board,isEnpassantMove=True) )                   
       else:   #   
          if self.board[r+1][c] =="--": #one squre pawn move
            moves.append(Move((r,c),(r+1,c),self.board))
            if r==1 and self.board[r+2][c]=="--":
                 moves.append(Move((r,c),(r+2,c),self.board))
          if c-1>=0:
            if self.board[r+1][c-1][0]=='w': #enemey piece
               moves.append(Move((r,c),(r+1,c-1),self.board)) 
            elif (r+1,c-1)==self.enpassantPossible:
              #print(r+1,c-1,"is Bl")
              moves.append(Move((r,c),(r+1,c-1),self.board,isEnpassantMove=True) ) 
          if c+1<=7:
             if self.board[r+1][c+1][0]=='w': #enemey piece
                  moves.append(Move((r,c),(r+1,c+1),self.board)) 
             elif (r+1,c+1)==self.enpassantPossible:
                # print(r+1,c+1,"is BR")
                 moves.append(Move((r,c),(r+1,c+1),self.board,isEnpassantMove=True) )                     
   def getRookMoves(self,r,c,moves):
     directions =((-1,0),(0,-1),(1,0),(0,1))
     enemyColor ='b' if self.whiteMove else 'w'
     for d in directions:
       for i in range(1,8):
         endRow =r+d[0]*i
         endCol =c+d[1]*i
         if 0<=endRow <8 and 0<= endCol < 8:
           endPiece = self.board[endRow][endCol]
           if endPiece =="--":
             moves.append(Move((r,c),(endRow,endCol),self.board))
           elif endPiece[0] ==enemyColor:
              moves.append(Move((r,c),(endRow,endCol),self.board))           
              break
           else :
             break
         else:
          break         
   def getBishopMoves(self,r,c,moves):
     directions =((-1,-1),(1,-1),(-1,1),(1,1))
     enemyColor ='b' if self.whiteMove else 'w'
     for d in directions:
       for i in range(1,8):
         endRow =r+d[0]*i
         endCol =c+d[1]*i
         if 0<=endRow <8 and 0<= endCol < 8:
           endPiece = self.board[endRow][endCol]
           if endPiece =="--":
             moves.append(Move((r,c),(endRow,endCol),self.board))
           elif endPiece[0] ==enemyColor:
              moves.append(Move((r,c),(endRow,endCol),self.board))           
              break
           else :
             break
         else:
          break
   def getKnightMoves(self,r,c,moves):
       knightMoves =((-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1),(-2,-1))
       allyColor ='w' if self.whiteMove else 'b'
       for m in knightMoves:
         endRow =r+m[0]
         endCol =c+m[1]
         if 0<=endRow <8 and 0<=endCol <8:
          endPiece = self.board[endRow][endCol]
          if endPiece[0] !=allyColor:
             moves.append(Move((r,c),(endRow,endCol),self.board))
    
   def getQueenMoves(self,r,c,moves):
     directions =((-1,-1),(1,-1),(-1,1),(1,1))
     enemyColor ='b' if self.whiteMove else 'w'
     for d in directions:
       for i in range(1,8):
         endRow =r+d[0]*i
         endCol =c+d[1]*i
         if 0<=endRow <8 and 0<= endCol < 8:
           endPiece = self.board[endRow][endCol]
           if endPiece =="--":
             moves.append(Move((r,c),(endRow,endCol),self.board))
           elif endPiece[0] ==enemyColor:
              moves.append(Move((r,c),(endRow,endCol),self.board))           
              break
           else :
             break
         else:
          break
     directions =((-1,0),(0,-1),(1,0),(0,1))
     enemyColor ='b' if self.whiteMove else 'w'
     for d in directions:
       for i in range(1,8):
         endRow =r+d[0]*i
         endCol =c+d[1]*i
         if 0<=endRow <8 and 0<= endCol < 8:
           endPiece = self.board[endRow][endCol]
           if endPiece =="--":
             moves.append(Move((r,c),(endRow,endCol),self.board))
           elif endPiece[0] ==enemyColor:
              moves.append(Move((r,c),(endRow,endCol),self.board))           
              break
           else :
             break
         else:
          break    
             
   def getKingMoves(self,r,c,moves):
       kingMoves =((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
       allyColor ='w' if self.whiteMove else 'b'
       for i in range(8):
         endRow =r +kingMoves[i][0]
         endCol= c+ kingMoves[i][1]
         if 0<=endRow<8 and 0<=endCol<8:
          endPiece =self.board[endRow][endCol]
          if endPiece[0] !=allyColor:
            moves.append(Move((r,c),(endRow,endCol),self.board))          
   def fen(self):
       fens=""
       for r1 in range(0,8):
           counter=0
           for c1 in range (0,8):
              
              if self.board[r1][c1]=='--':
                  counter+=1
             
              elif  self.board[r1][c1][0]=='w':
                  fens+='' if counter==0 else str(counter) 
                  fens+=self.board[r1][c1][1]
                  counter=0
              elif self.board[r1][c1][0]=='b':
                  fens+='' if counter==0 else str(counter)
                  fens+=self.board[r1][c1][1].lower()
                  counter=0
              if c1==7:
                fens+='' if counter ==0 else  str(counter)    
           fens+='/'  
       fens+=' w ' if self.whiteMove else ' b '
       fens+='K' if self.castleRightsLog[-1].wks else ''
       fens+='Q' if self.castleRightsLog[-1].wqs else ''
       fens+='k' if self.castleRightsLog[-1].bks else ''
       fens+='q' if self.castleRightsLog[-1].bks else ''
       return fens    
   def ReverseFen(self,fens):
      r1=0
      c1=0
      i=0
      WK=BK=BQ=WQ=False
      print(len(fens))
      for i in range(0,len(fens)):
         if c1>=8:
             c1=0
         if fens[i].isnumeric()  :
             c1+=int(fens[i])
         elif fens[i]  == '/':
            r1+=1
            c1=0    
         elif fens[i].islower() :
            
             self.board[r1][c1]='b'+fens[i].upper()
             if fens[i] =='k':
                 self.blackKingLocation =(r1,c1)
             print(fens[i])        
             c1+=1  
         elif fens[i].isupper()   :
              
              self.board[r1][c1]='w'+fens[i]
              if fens[i] =='K':
                 self.whiteKingLocation =(r1,c1)
              print(fens[i])    
              c1+=1
        
         elif fens[i]==' ':
           i+=1   
           if fens[i] == 'w':
            self.whiteMove= True  
            break
           elif fens[i] =='b':
            self.whiteMove= False
            break
      i+=2   
      if i<len(fens):
         if fens[i]=='K':
            WK=True
            i=+1
         if fens[i]=='Q':
            WQ=True
            i=+1   
         if fens[i]=='k':
            BK=True
            i=+1
         if fens[i]=='q':
            BQ=True
            i=+1
         
            
      self.currentCastlingRight=CastleRights(WK,BK,WQ,BQ)
                 


   ''''
     Generate all valid castle moves for king at r,c, and color'''
   def getCastleMoves(self,r,c,moves):
      if self.squareUnderAttack(r,c):
        return 
      if (self.whiteMove and self.currentCastlingRight.wks) or (not self.whiteMove and self.currentCastlingRight.bks):
          self.getKingsideCastleMoves(r,c,moves)
      if (self.whiteMove and self.currentCastlingRight.wqs) or (not self.whiteMove and self.currentCastlingRight.bqs):
          self.getQueensideCastleMoves(r,c,moves)
                       
   def getKingsideCastleMoves(self,r,c,moves):
       if self.board[r][c+1] =='--' and self.board[r][c+2] =='--':
          if not self.squareUnderAttack(r,c+1) and not self.squareUnderAttack(r,c+2):
                moves.append(Move((r,c),(r,c+2),self.board,isCastleMove=True))
   def getQueensideCastleMoves(self,r,c,moves):   
       if self.board[r][c-1] =='--' and self.board[r][c-2] =='--' and self.board[r][c-3]=='--' and not self.squareUnderAttack(r,c-1) and not self.squareUnderAttack(r,c-2):
                moves.append(Move((r,c),(r,c-2),self.board,isCastleMove=True))    

          
   
  
class CastleRights():
    def __init__(self,wks,bks,wqs,bqs):
       self.wks=wks
       self.bks=bks 
       self.wqs=wqs
       self.bqs=bqs       
class Move():
  
   ranksToRows ={"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
   rowsToRanks={v:k for k,v in ranksToRows.items()}
   filesToCols={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
   colsToFiles ={v:k for k,v in filesToCols.items() }
   def __init__(self,startSq,endSq,board,isEnpassantMove =False,isCastleMove=False):
      self.startRow =startSq[0]
      self.startCol=startSq[1]
      self.endRow=endSq[0]
      self.endCol=endSq[1]
      self.pieceMoved=board[self.startRow][self.startCol]
      self.pieceCaptured=board[self.endRow][self.endCol]
      #pawnPromotion
      self.isPawnPromotion =( (self.pieceMoved =='wP' and self.endRow ==0) or (self.pieceMoved =='bP' and self.endRow ==7) )
         
      #Enpassanr  
      self.isEnpassantMove = isEnpassantMove  
      if self.isEnpassantMove:
         self.pieceCaptured ="wP" if self.pieceMoved =="bP" else  "bP"     
      #castle move
      self.isCastleMove=isCastleMove
      self.isCapture= self.pieceCaptured !='--'
      self.moveID =self.startRow*1000 +self.startCol*100 +self.endRow*10 +self.endCol
      
   def __eq__ (self,other):#overriding equal
      if isinstance(other,Move): 
         return self.moveID==other.moveID
      return False   
   def  getChessNotation(self):
      return self.getRankFile(self.startRow,self.startCol) +self.getRankFile(self.endRow,self.endCol)
      
   def getRankFile(self,r,c):
        return self.colsToFiles[c] +self.rowsToRanks[r]    
   
   def __str__(self):
       #castle move 
       if self.isCastleMove:
           return "O-O" if self.endCol ==6 else "O-O-O" 
          #"O-O" #king sidecastle
       endSquare =self.getRankFile(self.endRow,self.endCol)
       if self.pieceMoved[1]=='P'   :  
          if self.isCapture:
             return self.colsToFiles[self.startCol]+"x" +endSquare
          else:
             return endSquare          
     #pawn promtions
     #two of the same type of piece moving to same square like  Nbd2 
     #also adding + for check move and #for checkmate
     #piece moves
       moveString=self.pieceMoved[1]
       if self.isCapture:
         moveString+='x'
       return moveString +endSquare

class Fen():
   fenS=""
   def fen(self):
       self.fenS=""
       for r1 in range(0,8):
           for c1 in range (0,8):
              if  self.board[r1][c1][0]=='w':
                  self.fens+=self.board[r1][c1][1]
              elif self.board[r1][c1][0]=='b':
                  self.fens+=self.board[r1][c1][1].lower()
           self.fens+='/'   
       return self.fens   