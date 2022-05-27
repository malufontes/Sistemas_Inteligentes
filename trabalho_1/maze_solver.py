from ctypes.wintypes import BOOL

import random
from socket import AF_UNIX


row1 = [2,0,0,0,0,0,0,0,0,0]
row2 = [1,0,0,0,0,0,0,0,0,0]
row3 = [1,0,0,0,0,0,0,0,0,0]
row4 = [1,1,1,1,1,1,1,1,0,0]
row5 = [0,0,0,1,0,1,0,1,0,0]
row6 = [0,0,0,1,0,1,0,1,0,0]
row7 = [0,0,1,1,1,1,0,1,0,0]
row8 = [0,0,1,0,0,0,0,1,0,0]
row9 = [0,0,1,0,0,0,0,1,0,0]
row10= [0,0,1,3,1,1,1,1,0,0]

matrix = []
matrix.append(row1)
matrix.append(row2)
matrix.append(row3)
matrix.append(row4)
matrix.append(row5)
matrix.append(row6)
matrix.append(row7)
matrix.append(row8)
matrix.append(row9)
matrix.append(row10)

# print(matrix)
nrows = len(matrix)
ncolumns = len(matrix[0])

print("numero de linhas =",nrows)
print("numero de colunas =",ncolumns)
# print(matrix[0][0])

TILE = 50

# procurando o "quadrado incial"
for row in range(0,nrows):
    for col in range(0,ncolumns):
        if(matrix[row][col]==2):
            inicial_row = row
            inicial_col = col

print(inicial_row,inicial_col)

class Cell:
    def __init__(self,row,col,id):
        self.row, self.col = row, col
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.id = id
        self.visited = False
        self.marked = False
        self.check_walls()

    def __str__(self):
        return "[" + str(self.row) + "][" + str(self.col) + "]"
    
    def check_walls(self):
        row, col = self.row, self.col
        # checando laterais
        if(row>0):
            if(matrix[row-1][col]==1):
                self.walls['left'] = False
        if(row<(nrows-1)):
            if(matrix[row+1][col]==1):
                self.walls['right'] = False
        # checando em cima e em baixo
        if(col>0):
            if(matrix[row][col-1]==1):
                self.walls['bottom'] = False
        if(col<(nrows-1)):
            if(matrix[row][col+1]==1):
                self.walls['top'] = False   

    def get_id(self):
        print(self.id)
    
    def draw(self):
        if(matrix[row][col]==0):
            pygame.draw.rect(screen, pygame.Color('black'), pygame.Rect((TILE*row),(TILE*col),TILE,TILE))
            return
        if(matrix[row][col]==2):
            pygame.draw.rect(screen, pygame.Color('darkgreen'), pygame.Rect((TILE*row),(TILE*col),TILE,TILE))
            return
        if(matrix[row][col]==3):
            pygame.draw.rect(screen, pygame.Color('darkred'), pygame.Rect((TILE*row),(TILE*col),TILE,TILE))
            return
        if(matrix[row][col]==1):
            if self.visited:
                pygame.draw.rect(screen, pygame.Color('darkgray'), pygame.Rect((TILE*row),(TILE*col),TILE,TILE))
                return
            if self.marked:
                pygame.draw.rect(screen, pygame.Color('lightgray'), pygame.Rect((TILE*row),(TILE*col),TILE,TILE))
                return
            pygame.draw.rect(screen, pygame.Color('white'), pygame.Rect((TILE*row),(TILE*col),TILE,TILE))
            return
        

# criando as células dos labirintos
grid_cells = []
for x in range(0,nrows):
    grid_cells.append([])
    for y in range(0,ncolumns):
        grid_cells[x].append(Cell(x,y,matrix[x][y]))

print(grid_cells[0][0].id)


class AgenteBFS:
    def __init__(self,row,col):
        self.row, self.col = row, col
        self.sides = [False, False, False, False]
        self.visitedcells = []
        self.markedcells = []


    def visitar_no(self):
        if not self.teste_de_objetivo():
            print("visitando no", grid_cells[self.row][self.col])
            if (self.visited_cell(self.row,self.col) == -1):
                self.visitedcells.append(grid_cells[self.row][self.col])
                grid_cells[self.row][self.col].visited = True
                print("Células visitadas = ", len(self.visitedcells))
                self.print_visitedcells()
            if (self.marked_cell(self.row,self.col) == -1):
                self.markedcells.append(grid_cells[self.row][self.col])
                print("Células marcadas = ", len(self.markedcells))
                self.print_markedcells()
            if self.checar_lados():     # retorna true se todos os lados tiverem sidos checados
                print("***************************** PROX NO")
                self.prox_no()
        

    def checar_lados(self):
        # print("Checar lados")
        aux = random.randint(0,3)
        # print("aux = ", aux)
        contador = 0
        while self.sides[aux] == True:
            aux =  (aux+1)%4
            contador = contador+1
            if contador > 3:
                return True
        self.sides[aux] = True
        if aux == 0:
            self.checar_topo()
            return False
        if aux == 1:
            self.checar_direita()
            return False
        if aux == 2:
            self.checar_abaixo()
            return False
        if aux == 3:
            self.checar_esquerda()
            return False


    def checar_topo(self):
        print("Checar topo")
        if(self.row > 0):
            if(grid_cells[self.row-1][self.col].id > 0):
                if(self.marked_cell(self.row-1,self.col) == -1 and self.visited_cell(self.row-1,self.col) == -1):
                    self.markedcells.append(grid_cells[self.row-1][self.col])
                    grid_cells[self.row-1][self.col].marked = True
                    print("Célula marcada = ", len(self.markedcells))
                    self.print_markedcells()
                
    def checar_direita(self):
        print("Checar direita")
        if(self.col < ncolumns-1):
            if(grid_cells[self.row][self.col+1].id > 0):
                if(self.marked_cell(self.row,self.col+1) == -1 and self.visited_cell(self.row,self.col+1) == -1):
                    self.markedcells.append(grid_cells[self.row][self.col+1])
                    grid_cells[self.row][self.col+1].marked = True
                    print("Célula marcada = ", len(self.markedcells))
                    self.print_markedcells()

    def checar_abaixo(self):
        print("Checar abaixo")
        if(self.row < nrows-1):
            if(grid_cells[self.row+1][self.col].id > 0):
                if(self.marked_cell(self.row+1,self.col) == -1 and self.visited_cell(self.row+1,self.col) == -1):
                    self.markedcells.append(grid_cells[self.row+1][self.col])
                    grid_cells[self.row+1][self.col].marked = True
                    print("Célula marcada = ", len(self.markedcells))
                    self.print_markedcells()

    def checar_esquerda(self):
        print("Checar esquerda")
        if(self.col > 0):
            if(grid_cells[self.row][self.col-1].id > 0):
                if(self.marked_cell(self.row,self.col-1) == -1 and self.visited_cell(self.row,self.col-1) == -1):
                    self.markedcells.append(grid_cells[self.row][self.col-1])
                    grid_cells[self.row][self.col-1].marked = True
                    print("Célula marcada = ", len(self.markedcells))
                    self.print_markedcells()
        

    def prox_no(self):
        aux = self.marked_cell(self.row,self.col)
        self.markedcells.pop(aux)
        print("Célula marcada removida = ", len(self.markedcells))
        self.print_markedcells()
        if (len(self.markedcells) > 0):
            aux = random.randint(0,len(self.markedcells)-1)
            self.row = self.markedcells[aux].row
            self.col = self.markedcells[aux].col
            self.sides[0] = False
            self.sides[1] = False
            self.sides[2] = False
            self.sides[3] = False

    def visited_cell(self,row,col):
        for i in range(len(self.visitedcells)):
            if self.visitedcells[i].row == row and self.visitedcells[i].col == col:
                return i
        return -1   

    def marked_cell(self,row,col):
        for i in range(len(self.markedcells)):
            if self.markedcells[i].row == row and self.markedcells[i].col == col:
                return i
        return -1

    def print_visitedcells(self):
        for i in range(len(self.visitedcells)):
            print(self.visitedcells[i], " ", end= "")
        print()

    def print_markedcells(self):
        for i in range(len(self.markedcells)):
            print(self.markedcells[i], " ", end= "")
        print()        
        

    def teste_de_objetivo(self) -> bool: 
        if(grid_cells[self.row][self.col].id == 3):
            return True
        return False

    def draw(self):
        pygame.draw.rect(screen, pygame.Color('yellow'), pygame.Rect((TILE*self.row),(TILE*self.col),TILE,TILE))


class AgenteDFS:
    def __init__(self,row,col):
        self.row, self.col = row, col
        self.last_row, self.last_col = row, col
        self.lista = []
        self.lista_checkpoint = []
        self.sucess = False

    def expandir_no(self):
        
        row = self.row
        col = self.col
        ##self.teste_de_objetivo(row,col)
        print("DFS se movimentando")

        self.testa_lados()
        

    def testa_lados(self): 
        embaralhador=  random.randint(0,3) #gera um numero aleatorio
        contador=4                         # contador ate 4 para testar 4 lados 

        #print ("Numero da vez:", embaralhador)  
        while(contador>0):                  #while testa os 4 lados e nao permite voltar 
            if embaralhador == 0:
                if(self.teste_direita()):
                    return
            if embaralhador == 1:
                if(self.teste_esquerda()):
                    return
            if embaralhador == 2:
                if(self.teste_cima()):
                    return
            if embaralhador == 3:
                if(self.teste_baixo()):
                    return
            
            contador = contador -1
            embaralhador = (embaralhador+1) % 4 #encrementa o embaralhador e zera caso passe de 3
            
        ##------------------  caso estaja em um beco sem saida sera necessario voltar, entao apos testar os 4 lados sem sucesso a funcao permite voltar
        contador = 4
        while(contador>0):
            if embaralhador == 0:
                if(self.teste_direita(True)):
                    return
            if embaralhador == 1:
                if(self.teste_esquerda(True)):
                    return
            if embaralhador == 2:
                if(self.teste_cima(True)):
                    return
            if embaralhador == 3:
                if(self.teste_baixo(True)):
                    return

            contador = contador -1
            embaralhador = (embaralhador+1) % 4
            
            
    
                 
    def teste_direita(self, voltapermitida = False):
        print("Volta permitida direita", voltapermitida)     
        if(self.row<(nrows-1) and not self.sucess): ## se a linha nao for maior que o o numero maximo menos 1 pra nao acessar area inexistente da matriz 
                if(grid_cells[self.row+1][self.col].id ==1):
                    if(voltapermitida or self.row+1 != self.last_row ): ## se a volta for permitida ou se nao estiver voltando
                        print("DIREITA")
                        print("linha", self.row, "colula :", self.col , "row + 1:", self.row+1 ,  "self last row ", self.last_row)
                        self.teste_de_objetivo(self.row+1,self.col)
                        #self.expandir_no()
                        return(True)
        return(False)
                    

    def teste_baixo(self,voltapermitida = False):
        if(self.col<(nrows-1) and not self.sucess): ## coluna menor que o num maximo menos 1 numero de rows eh igual ao numero de cols
            if(grid_cells[self.row][self.col+1].id ==1):
                if(voltapermitida or self.col+1 != self.last_col):
                    print("BAIXO")
                    print("linha", self.row, "colula :", self.col ,"col + 1:", self.col+1 , "self last col ", self.last_col)
                    self.teste_de_objetivo(self.row,self.col+1)
                    #self.expandir_no()
                    return(True)
        return(False)
                
    def teste_esquerda(self, voltapermitida = False):
        if(self.row > 0 and not self.sucess): ## se a linha nao for menor que zero ou seja se nao tenar acessar algo que nao existe
            if(grid_cells[self.row-1][self.col].id ==1):
                if(voltapermitida or self.row-1 != self.last_row):
                    print("ESQUERDA")
                    print("linha", self.row, "colula :", self.col ,"row - 1:", self.row-1 , "self last row ", self.last_row)
                    self.teste_de_objetivo(self.row-1,self.col)
                    #self.expandir_no()
                    return(True)
        return(False)

    def teste_cima(self,voltapermitida = False):
        if(self.col>0 and not self.sucess):  ## coluna maior que zero 
            if(grid_cells[self.row][self.col-1].id ==1 ):
                if(voltapermitida or  self.col-1 != self.last_col):
                    print("CIMA")
                    print("linha", self.row, "colula :", self.col ,"col - 1:", self.col-1 , "self last col ", self.last_col)
                    self.teste_de_objetivo(self.row,self.col-1)
                    #self.expandir_no()
                    return(True) 
        return(False)

    def teste_de_objetivo(self, row, col):
        self.last_col = self.col
        self.last_row = self.row
        self.row = row
        self.col = col
        if(grid_cells[self.row-1][self.col].id ==3):
            self.sucess = True

    def draw(self):
        pygame.draw.rect(screen, pygame.Color('yellow'), pygame.Rect((TILE*self.row),(TILE*self.col),TILE,TILE))

## ------------------------- Execução 
modo = input("Selecione BFS[1] ou DFS[2]")        

if modo == "1":
    agente = AgenteBFS(inicial_row,inicial_col)
if modo == "2":
    agente = AgenteDFS(inicial_row,inicial_col)

import pygame  
  
pygame.init()  
screen = pygame.display.set_mode((ncolumns*TILE,nrows*TILE))  
clock = pygame.time.Clock()
done = False  
  
while not done:  
    screen.fill(pygame.Color('black'))

    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            done = True  


    for row in range(0,nrows):
        for col in range(0,ncolumns):
            grid_cells[row][col].draw()

    agente.draw()

    if modo == "1":
        agente.visitar_no()
    if modo == "2":
        agente.expandir_no()
    
    pygame.display.flip()  
    clock.tick(10)