import random
pieceScore ={"K":0,"Q":10,"R":5,"N":3,"B":3,"P":1}
CHECKMATE =1000
STALEMATE =0
DEPTH =4
counter=0
Tcounter=0
Tcounter1=0
transpositionTable =dict()
knightSocres=[[1,1,1,1,1,1,1,1],
              [1,2,2,2,2,2,2,1],
              [1,2,3,3,3,3,2,1],
              [1,2,3,4,4,3,3,1],
              [1,2,3,4,4,3,3,1],
              [1,2,3,3,3,3,2,1],
              [1,2,2,2,2,2,2,1],
              [1,1,1,1,1,1,1,1]]

bishopScores=[[4,3,2,1,1,2,3,4],
              [3,4,3,2,2,3,4,3],
              [2,3,4,3,3,4,3,2],
              [1,2,3,4,4,3,2,1],
              [1,2,3,4,4,3,2,1],
              [2,3,4,3,3,4,3,2],
              [3,4,3,2,2,3,4,3],
              [4,3,2,1,1,2,3,4]] 
              
queenScores =[[1,1,1,3,1,1,3,1] ,
              [1,2,3,3,3,1,1,1],
              [1,4,3,3,3,4,2,1],
              [1,2,3,3,3,2,2,1],
              [1,2,3,3,3,2,2,1],
              [1,4,3,3,3,4,2,1],
              [1,1,2,3,3,1,1,1],
              [1,1,1,3,1,1,3,1]]    
              
rookScores= [[4,3,4,4,4,4,3,4],
              [4,4,4,4,4,4,4,4],
              [1,1,2,3,3,2,1,1],
              [1,2,3,4,4,3,2,1],
              [1,2,3,4,4,3,2,1],
              [1,1,2,3,3,2,1,1],
              [4,4,4,4,4,4,4,4],
              [4,3,4,4,4,4,3,4]]

whitePawnScores=[[8,8,8,8,8,8,8,8],
                 [8,8,8,8,8,8,8,8],
                 [5,6,6,7,7,6,6,5],
                 [2,3,3,5,5,3,3,2],
                 [1,2,3,4,4,3,2,1],
                 [1,1,2,3,3,2,1,1],
                 [1,1,1,0,0,1,1,1],
                 [0,0,0,0,0,0,0,0]]  
                 
blackPawnScores=[[0,0,0,0,0,0,0,0],
                  [1,1,1,0,0,1,1,1],
                  [1,1,2,3,3,2,1,1],
                  [1,2,3,4,4,3,2,1],
                  [2,3,3,5,5,3,3,2],
                  [5,6,6,7,7,6,6,5],
                  [8,8,8,8,8,8,8,8],
                 [8,8,8,8,8,8,8,8]]
                  
              
kingneScores=[  [1,1,3,1,1,1,3,1],
              [1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1],
              [1,1,3,1,1,1,3,1]] 
kingScores= [
    [  2.0,  2.0,  3.0,  0.0,  0.0,  1.0,  3.0,  2.0 ] ,
    [  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0 ], 
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0 ],
    [  2.0,  2.0,  3.0,  0.0,  0.0,  1.0,  3.0,  2.0 ] ]             
scoreList =[]      
     
piecePositionScores={"N": knightSocres,"B":bishopScores,"K":kingScores,"R":rookScores,"Q":queenScores,"wP":whitePawnScores,"bP":blackPawnScores}            
def findRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]
    
# def findBestMove(gs,validMoves):
   # turnMultiplier = 1 if gs.whiteMove else -1
   
   # #maxScore =CHECKMATE
   # opponentMinMaxScore=CHECKMATE 
   # bestPlayerMove =None
   # random.shuffle(validMoves     )
   # for playerMove in validMoves:
     # gs.makeMove(playerMove)
     # opponentsMoves =gs.getValidMoves()
     # if gs.stalemate:
        # opponentMaxScore=STALEMATE
     # elif gs.checkmate:
        # opponentMaxScore=-CHECKMATE     
    
     # else: 
      # opponentMaxScore =-CHECKMATE
      # for opponentsMove in opponentsMoves:
       # gs.makeMove(opponentsMove)
       # gs.getValidMoves()
       # if gs.checkmate:
        # score =-turnMultiplier*CHECKMATE
       # elif gs.stalemate:
        # score =STALEMATE
       # else :   
        # score =-turnMultiplier *scoreMaterial(gs.board)
       # if score>opponentMaxScore:
         # opponentMaxScore=score
     # #  bestPlayerMove =playerMove
       # gs.undoMove()
     # if opponentMaxScore< opponentMinMaxScore:
       # opponentMinMaxScore=opponentMaxScore
       # bestPlayerMove=playerMove
     # gs.undoMove()  
   # return bestPlayerMove

#def findBestMove(gs,validMoves):
 #'''helper method to make first recursive callable'''
 
def findBestMove(gs,validMoves,returnQueue):
     global nextMove,counter,scoreList,Tcounter,Tcounter1
     random.shuffle(validMoves)
     nextMove=None
     counter=0
     #findMoveMax(gs,validMoves,DEPTH,gs.whiteMove)
     #findMoveNegaMax(gs,validMoves,DEPTH,1 if gs.whiteMove else -1)
     scoreT=findMoveNegaMaxAlphaBeta(gs,validMoves,DEPTH,-CHECKMATE,CHECKMATE,1 if gs.whiteMove else -1)     
     
     print(scoreT)
     print(counter,Tcounter,Tcounter1)
     returnQueue.put(nextMove)     
def findMoveMinMax(gs,validMoves,depth,whiteMove):
    global nextMoves
        
    if depth==0:

      return scoreMaterial(gs.board)
    if whiteMove:
      
       maxScore =-CHECKMATE
       for move in validMoves:
         gs.makeMove(move)
         nextMoves=gs.getValidMoves()
         score=findMoveMinMax(gs,nextMoves,depth -1,False)
         if score> maxScore:
           maxScore =score
           if depth==DEPTH:
            nextMove =move
         gs.undoMove() 
       return maxScore  
              
    else:
        minScore =CHECKMATE
        for move in validMoves:
          gs.makeMove(move)
          nextMoves=gs.getValidMoves()
          score= findMoveMinMax(gs,nextMoves,depth-1,True)
          if score< minScore:
            minScore =score
            if depth==DEPTH:
             nextMove =move
             #random.shuffle(validMoves     )
          gs.undoMove()
        return minScore          
    
def findMoveNegaMax(gs,validMoves,depth,turnMultiplier):
  global nextMove,counter
  counter+=1
  if depth==0:
     return turnMultiplier*scoreBoard(gs)
  maxScore=-CHECKMATE
  for move in validMoves:
    gs.makeMove(move)
    nextMoves=gs.getValidMoves()
    score=-findMoveNegaMax(gs,nextMoves,depth-1,-turnMultiplier)
    if score> maxScore:
      maxScore=score 
      if depth==DEPTH:
        nextMove=move
        
    gs.undoMove()
  return maxScore  
       
def findMoveNegaMaxAlphaBeta (gs,validMoves,depth,alpha,beta,turnMultiplier):
  global nextMove,counter,Tcounter,Tcounter1,transpositionTable
  counter+=1
  if depth==0:
     
     temp=gs.fen()
     transpositionTable[temp]=nextMove
     return turnMultiplier*scoreBoard(gs)
  #move ordering -future implementation
 
  Tcounter1=len(transpositionTable)   
  maxScore=-CHECKMATE
  for move in validMoves:
    if  gs.fen() in transpositionTable.keys():  
      nextMove=transpositionTable[gs.fen()]
      print("use of trnasp",nextMove)
      print(gs.fen())
      Tcounter+=1
      return turnMultiplier*scoreBoard(gs)
    gs.makeMove(move)
    nextMoves=gs.getValidMoves()
   
    score=-findMoveNegaMaxAlphaBeta(gs,nextMoves,depth-1,-beta,-alpha,-turnMultiplier)
    if score> maxScore:
      maxScore=score 
      if depth==DEPTH:
        #temp=gs.fen()
        #transpositionTable[temp]=move
        #print(temp)
        nextMove=move
        #nextMove=transpositionTable[temp]
        print(move,score)
        
    gs.undoMove()
    if maxScore> alpha: #pruning
      alpha =maxScore
    if alpha>=beta:
       break    
  
  return maxScore  
             

'''
a positive score is good for white and a negative is for black'''

def scoreBoard(gs):
    if gs.checkmate:
      if gs.whiteMove:
         return -CHECKMATE #black wins
      else:
         return CHECKMATE
    elif gs.stalemate:
      return STALEMATE    
       
    
    score =0
    for row in range(len(gs.board)):
       for col in range(len(gs.board[row])):
          square=gs.board[row][col]
          if square !="--":
           #score it positionally
           piecePositionScore=0
           if square[1]=="P":  
             piecePositionScore =piecePositionScores[square][row][col]   
                  
                     
           else: 
            piecePositionScore =piecePositionScores[square[1]][row][col] 
          
           if square[0] =='w':
           
              score+=pieceScore[square[1]]+piecePositionScore*0.1
            
           elif square[0] =='b':
              score= score-(pieceScore[square[1]]+piecePositionScore *0.1)
            
    return score
'''
Score board based on material'''
def scoreMaterial(board):
    score =0
    for row in board:
       for square in row :
          if square[0] =='w':
            score+=pieceScore[square[1]]
          elif square[0] =='b':
            score-= pieceScore[square[1]]  
            
    return score 

def scoreReturn():
   global scoreList
   return scoreList
   
   

def newScoreMaterial(board):
   return
   
     