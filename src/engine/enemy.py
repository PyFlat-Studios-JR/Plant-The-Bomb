import src.engine.entity as entity
import src.engine.block as block
import src.engine.textureLib as textureLib
import random
class enemy (entity.entity):
    def __init__(self, world, pos):
        super().__init__(world, pos)
        self.is_destructible = True
        self.allow_explosions = True
        self.is_alive = True
        self.path = []
        self.health = 0
        self.attack_pattern = []
        self.holding = block.air(self.world)
        self.init_textureindex(2)
    def pathfind_to_player(self):
        distance_map = [[-1]*25 for i in range (25)] #A map that maps all reachable tiles by distance from self
        self.path = []                              #A list of vertices, that the enemy has to walk to get to the player!
        frontiers = [(self.x,self.y,0)]             #A list of active vertices (outer vertices)
        visited = []                                #A list of all visited vertices
        step = 0                                    #A failsafe, that prevents infinite loops!
        distance_map[self.x][self.y] = 0
        while True:
            #This is the failsafe!
            step += 1
            if step > 625:
                print("This should not take 625 steps!")
                break
            #Record all newly created nodes here!
            new_frontiers = []
            #For each active node:
            while len(frontiers) > 0:
                x, y, d = frontiers.pop()
                #Iterate over all possible ways!
                for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx = x + dx
                    ny = y + dy
                    #Only walk if you can walk and the position is new & valid!
                    if nx in range (0, 24) and ny in range (0, 24) and not (nx,ny) in visited:
                        if self.world.blocks[nx][ny].is_walkable or (nx == self.world.player.x and ny==self.world.player.y):
                            distance_map[nx][ny] = d+1
                            new_frontiers.append((nx,ny,d+1))
                            visited.append((nx,ny))
            #Stop if all nodes are explored! Otherwise repeat
            if len(new_frontiers) > 0:
                frontiers = new_frontiers[:]
            else:
                break
        if distance_map[self.world.player.x][self.world.player.y] == -1:
            print("Enemy failed to find player...")
            return
        #that means the player somehow is in the distance map!!!!
        #now walk "backwards" from the player towards descending numbers!
        cx = self.world.player.x
        cy = self.world.player.y
        self.path = [(cx,cy)]
        while True:
            cx,cy = self.path[-1]
            mindist = ()
            minv = 999999
            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx = cx + dx
                ny = cy + dy
                if nx == self.x and ny == self.y:
                    self.path.pop(0)
                    return          
                if nx in range (0, 24) and ny in range (0,24):
                    if distance_map[nx][ny] < minv and distance_map[nx][ny] != -1:
                        mindist = (nx,ny)
                        minv = distance_map[nx][ny]
            self.path.append(mindist)

    def onTick(self):
        if random.randint(0,10) > 0:
            return
        self.pathfind_to_player()
        if self.path:
            x,y = self.path.pop()
            self.world.blocks[x][y] = self
            self.world.blocks[self.x][self.y] = block.air(self.world)
            self.x = x
            self.y = y
    def onDestroy(self):
        pass
    def onDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.world.blocks[self.x][self.y] = self.holding
        
