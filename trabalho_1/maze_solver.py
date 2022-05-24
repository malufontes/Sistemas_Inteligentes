from ipaddress import collapse_addresses
from matplotlib.pyplot import grid


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

# print(inicial_row,inicial_col)

class Cell:
    def __init__(self,row,col,id):
        self.row, self.col = row, col
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.id = id
        self.visited = False
        self.check_walls()
    
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
        if(matrix[row][col]==1):
                pygame.draw.rect(screen, pygame.Color('white'), pygame.Rect((TILE*row),(TILE*col),TILE,TILE))
        if(matrix[row][col]==0):
                pygame.draw.rect(screen, pygame.Color('darkgray'), pygame.Rect((TILE*row),(TILE*col),TILE,TILE))
        if(matrix[row][col]==2):
                pygame.draw.rect(screen, pygame.Color('darkgreen'), pygame.Rect((TILE*row),(TILE*col),TILE,TILE))
        if(matrix[row][col]==3):
                pygame.draw.rect(screen, pygame.Color('darkred'), pygame.Rect((TILE*row),(TILE*col),TILE,TILE))

# criando as células dos labirintos
grid_cells = []
for x in range(0,nrows):
    grid_cells.append([])
    for y in range(0,ncolumns):
        grid_cells[x].append(Cell(x,y,matrix[x][y]))

print(grid_cells[0][0].id)

        
class Agente:
    def __init__(self,x,y):
        self.x, self.y = x, y

    def move(self):
        print("se movimentando")


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

    
    pygame.display.flip()  
    clock.tick(30)