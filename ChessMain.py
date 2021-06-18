import pygame as p
import time
import sqlite3
import ChessEng
import SmartMoveFinder
from multiprocessing import Process,Queue
BOARD_WIDTH =BOARD_HEIGHT =512
MOVE_LOG_PANEL_WIDTH=250
MOVE_LOG_PANEL_HEIGHT=512
DIMENSION =8
colors=[]
SQ_SIZE =BOARD_HEIGHT//DIMENSION
MAX_FPS=15
IMAGES =dict()
moveFlag=0
moveTexts =[]
conn = sqlite3.connect('Chess.db')
cur = conn.cursor()

#cur.execute('''CREATE TABLE results( statement Text )''');

printFLag=0# global variable used in isprintflag
def LoadImage():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(  piece + ".png"), (SQ_SIZE, SQ_SIZE))
def main():
    global printFLag
    
    Choice=""
    p.init()
    

    
    screen = p.display.set_mode((BOARD_WIDTH+MOVE_LOG_PANEL_WIDTH+100 , BOARD_HEIGHT+15))
  
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    
    moveLogFont =p.font.SysFont("Arial",14,True,False)
    gs=ChessEng.GameState()
    #fen=str(input("Enter fen"))
   # gs.ReverseFen(fen)
    validMoves =gs.getValidMoves()
    moveMade =False #flag for whenn a move is made
    animate =True#flag variable 
    print(gs.board)
    LoadImage()#only onces efor loop
    
    running =True
    sqSelected =()
    playerClicks = []
    
    gameOver=False
    playerOne =True# if human is playing white this is true if ai is playing whie false
    playerTwo =True#same for black
    AIThinking =False
    moveFinderProcess =None
    moveUndone =False
    
    while running:
       humanTurn =(gs.whiteMove and playerOne) or (not gs.whiteMove and playerTwo)
       
       for e in p.event.get():
         if e.type ==p.QUIT:
           running =False
         #mouse handler
         elif e.type == p.MOUSEBUTTONDOWN:
           if not gameOver:          
            location =p.mouse.get_pos() 
            col = location[0]// SQ_SIZE
            row = location[1]// SQ_SIZE
            if sqSelected==(row,col) or col >=8 or row>=8:#the user clciked the same square twice or user clicked moves log
               sqSelected =()                 #col is <8 and row <8 for board 
               playerClicks =[]
            else:
                sqSelected =(row,col)
                playerClicks.append(sqSelected)
            moveMade=False 
                 
            if  (len(playerClicks) ==2)and  humanTurn:
                move =ChessEng.Move(playerClicks[0],playerClicks[1],gs.board)
            #    print(move.getChessNotation())
                for i in range (len(validMoves)):
                 if move == validMoves[i]:
                     gs.makeMove(validMoves[i])
                     print(gs.fen())
                     moveMade =True
                    # animate =True
                     sqSelected =()
                     playerClicks=[]   
                if not moveMade:
                   playerClicks =[sqSelected]                
         elif e.type ==p.KEYDOWN:
           if e.key ==p.K_1:
             Choice=1
           if e.key ==p.K_2:
             Choice=2  
           if e.key ==p.K_3:
              Choice=3  
             
           if e.key ==p.K_z : 
            gs.undoMove() 
            movemade =False
            sqSelected=()
            playerClicks=[]
            gameOver=False
            if AIThinking:
              moveFinderProcess.terminate()
              AIThinking=False
            moveUndone=True  
              
           if e.key ==p.K_r :
                 gs= ChessEng.GameState()
                 validMoves=gs.getValidMoves()
                 sqSlected =()
                 moveMade =False  
                 animate =False  
                 gameOver =False
                 printFLag=0
                 if AIThinking:
                  moveFinderProcess.terminate()
                  AIThinking=False
                 moveUndone=True
           if e.key ==p.K_b :
                   playerTwo =not playerTwo
           if e.key ==p.K_w:  
                    playerOne=not playerOne  
                 
                                 
       
       #AI move Finder Logic
       if not gameOver and not humanTurn and not moveUndone:
         if not AIThinking :
           AIThinking=True
           print("Thinking ...")
           returnQueue =Queue()
           moveFinderProcess=Process(target=SmartMoveFinder.findBestMove,args=(gs,validMoves,returnQueue))           
           moveFinderProcess.start() #call finbedtMoves,valid moves return wueue
          # AIMove =SmartMoveFinder.findBestMove(gs,validMoves)
           text=str(SmartMoveFinder.scoreReturn())
           print("GOod",text)
         if not moveFinderProcess.is_alive():
            print("done ")
            AIMove=returnQueue.get()
            print("about to make")
            if AIMove is None:
              AIMove =SmartMoveFinder.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade =True 
            AIThinking=False
         # animate =True          
       if moveMade:
          if animate == True:
           animateMove(gs.moveLog[-1],screen,gs.board,clock)
          
          validMoves =gs.getValidMoves()
          movemade =False
          animate =False  
          moveUndone=False 
       drawGameState(screen,gs,validMoves,sqSelected,moveLogFont,playerOne,playerTwo,Choice) 
            
       

       if isInsufficient(gs.board):
            gameOver =True
                         
            result="Draw by insufficient pieces"
            
            drawEndGameText(screen,result)
            isPrintFlag(result)
           
       if gs.checkmate or gs.stalemate:
            gameOver=True
            result="Stalemate" if gs.stalemate else 'Black wins by checkmate' if gs.whiteMove else "white wins by checkmate"
            drawEndGameText(screen,result)
            isPrintFlag(result) 
               
              
                
       
       clock.tick(MAX_FPS)
       p.display.flip()
    
    cur.close() 

'''
 fun for graphics'''   
def drawGameState(screen,gs,validMoves,sqSelected,moveLogFont,playerOne,playerTwo,choice=1): 

    
    
    drawBoard(screen,choice)#makes squares on the board
    drawStartGameText(screen,moveLogFont)
    highlightSquares(screen,gs,validMoves,sqSelected)
    drawPieces(screen,gs.board)#bring pieces on top of these squares
    drawMoveLog(screen,gs,moveLogFont)
    drawBound(screen,gs,moveLogFont,playerOne,playerTwo)
def colorBoard(choice=1):

   if choice==2:   
     return [p.Color(235, 235, 208), p.Color(119, 148, 85)]  
   if choice==3:
      
      return [p.Color(235, 235, 208),p.Color(38,36,33)]   

   else:
      
      return [p.Color(232, 235, 239),p.Color(125,135,150)]  
'''
 Draw squares on board .the top left square is always light'''
def drawBoard(screen,choice):
    global colors
    font =p.font.SysFont("Arial",14,True,False)
    #colors = [p.Color(235, 235, 208), p.Color(119, 148, 85)] 
    colors =colorBoard(choice)
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            
            p.draw.rect(screen, colors[((c + r) %2)], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE)) 
            if c==7 and r==0:
             num=8
            if r==7 and c==0:
             text='a'
             
            if r==7: 
             
             textObject =font.render(text,True,colors[((c + r+1) %2)]) 
             text =chr(ord(text) + 1)
             textLocation= p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE).move(1,50)
             screen.blit(textObject,textLocation)
            if c==7:
             textObject =font.render(str(num),True,colors[((c + r+1) %2)]) 
             num=num-1
             textLocation= p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE).move(51,1)
             screen.blit(textObject,textLocation)

'''
Highlight square selected and moves 
'''
def highlightSquares(screen,gs,validMoves,sqSelected):
   if sqSelected!=():
     r,c= sqSelected
     if gs.board[r][c][0] ==('w' if gs.whiteMove else 'b'): # selected square is a pieces
       #highlight selected square
       s=p.Surface((SQ_SIZE,SQ_SIZE))
       s.set_alpha(100) #transparency valude ->0 transparent 255 opaque
       s.fill(p.Color('blue'))
       screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
       s.fill(p.Color('yellow'))
       for move in validMoves:
         if move.startRow ==r and move.startCol ==c:
            screen.blit(s,(SQ_SIZE*move.endCol,move.endRow*SQ_SIZE))
        


''' if gs.checkmate or gs.stalemate and moveFlag==0:
       print(moveTexts)
       moveFlag=1'''     
    
def drawPieces(screen,board) :  
  
  for c in range(DIMENSION):
        for r in range(DIMENSION):
             piece =board[r][c]
             if piece !="--":
               screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))             
'''
Draws the move log'''
def drawMoveLog(screen,gs,font):
     global moveTexts
     
     moveLogRect=p.Rect(BOARD_WIDTH,0,MOVE_LOG_PANEL_WIDTH,MOVE_LOG_PANEL_HEIGHT)
     p.draw.rect(screen,p.Color("black"),moveLogRect)     
     moveLog =gs.moveLog
     moveTexts =[]
     for i in range(0,len(moveLog),2):
       moveString = str(i//2+1) +"." + str(moveLog[i])+" "
       if i+1<len(moveLog):
            moveString+=str(moveLog[i+1])+" " 
       moveTexts.append(moveString)     
     #moveTexts =moveLog #in future change
    
     movesPerRow =3
     padding =5
     lineSpacing=3  
     textY=padding
     for i in range(0,len(moveTexts),movesPerRow):
        text=""
        for j in range(movesPerRow):
          if i+j <len(moveTexts):
            text+=moveTexts[i+j]
        textObject =font.render(text,True,p.Color('white'))
        textLocation =moveLogRect.move(padding,textY)
        screen.blit(textObject,textLocation)
        textY+= textObject.get_height()+lineSpacing       
     pass

def drawBound(screen,gs,font,playerOne,playerTwo):
   boundRect1=p.Rect(BOARD_HEIGHT,0,10,10)
   text=str(SmartMoveFinder.scoreReturn())
   p.draw.rect(screen,p.Color("cyan"),boundRect1) 
   textObject =font.render(text,True,p.Color('black')) 
   
   textLocation =boundRect1.move(0,0)
   
   
   screen.blit(textObject,textLocation)
   
   boundRect2=p.Rect(0,MOVE_LOG_PANEL_HEIGHT,BOARD_WIDTH,15)
   
   text="white " +( "(human)" if playerOne else " (AI) ")
   text+=" vs black " + ("(human)" if playerTwo else " (AI) ")
   text+=" **White to play** " if gs.whiteMove else " **Black to play**"
  
   p.draw.rect(screen,p.Color("cyan"),boundRect2)   
   
   textObject =font.render(text,True,p.Color('black')) 
   
   textLocation =boundRect2.move(0,0)
   
   
   screen.blit(textObject,textLocation)
   pass    
'''
animating move'''

def animateMove(move,screen,board,clock):
    global colors 
    #coords= []#list of coord of animation
    dR=move.endRow -move.startRow
    dC=move.endCol -move.startCol
    framesPerSquare =20#frames to move one square
    frameCount =(abs(dR)+abs(dC))* framesPerSquare
    for frame in range (frameCount+1):
      r,c=(move.startRow+dR*frame/frameCount,move.startCol +dC*frame/frameCount)
     # drawBoard(screen,choice)
      drawPieces(screen,board)
      #erase the piece moved from its ending square
      color=colors[(move.endRow+move.endCol)%2]
      endSquare =p.Rect(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
      p.draw.rect(screen,color,endSquare)
      if move.pieceCaptured!='--':
        if move.isEnpassantMove :
          enPassantRow =(move.endRow+1) if move.pieceCaptured[0] =='b' else move.endRow-1
          endSquare =p.Rect(move.endCol*SQ_SIZE,move.enPassantRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
        screen.blit(IMAGES[move.pieceCaptured],endSquare)
      if move.pieceCaptured!='--':
         screen.blit(IMAGES[move.pieceMoved],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
       
        
      
      p.display.flip()
      clock.tick(60)
      
def isInsufficient(board):
      count=0
      for row in board:
       for square in row :
         if  square[0]=='-':
          count+=1
      if count>=62:
       
        return 1
      else:   
        return 0      
def drawStartGameText(screen,font):
     boundRect=p.Rect(BOARD_WIDTH+MOVE_LOG_PANEL_WIDTH,0,100,MOVE_LOG_PANEL_HEIGHT)
     p.draw.rect(screen,p.Color("cyan"),boundRect) 
     text=["Select color"," press 1-2."]
     for  i in range(0,len(text)):
      textObject =font.render(text[i],True,p.Color('Black')) 

       
      textLocation =boundRect.move(0,10*i)
      screen.blit(textObject,textLocation) 
      
     

     
def drawEndGameText(screen,text):
     font =p.font.SysFont("Helvitca",32,True,False)
     textObject =font.render(text,0,p.Color('Black'))
     textLocation =p.Rect(0,0,BOARD_WIDTH,BOARD_HEIGHT).move(BOARD_WIDTH/2-textObject.get_width()/2,BOARD_HEIGHT/2-textObject.get_height()/2)
     screen.blit(textObject,textLocation) 
     textObject =font.render(text,0,p.Color("Black"))
     screen.blit(textObject,textLocation.move(2,2)) 
def isPrintFlag(result):
    global printFLag
    if printFLag==0:
             dataRecord(result)
             print(result) 
             printFLag=+1 
             for moveText in moveTexts:
               print(moveText)
def dataRecord(result):
    global cur,conn
    cur.execute('''INSERT OR REPLACE INTO results(statement)
        VALUES ( ?)''', (result,) )
    conn.commit()    
if __name__ =="__main__":        
  main()
    