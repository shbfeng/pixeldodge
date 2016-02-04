import pygame,random,sys

class Player(object):
  def __init__(self,pos,color):
    self.pos=pos
    self.color=color
    self.lives=3
    self.dir=[0,2]
    self.score=0
    self.speedtime=0
    self.invincibletime=0
    self.bullets=0
  def draw(self):
    pygame.draw.rect(window,self.color,[self.pos[0]-1,self.pos[1]-1,3,3])
  def spawn(self,enemies):
    found=False
    while True:
      self.pos=[random.randint(100,600),random.randint(100,400)]
      for enemy in enemies:
        if dist(self,enemy)>150:found=True
      if found:break
  def move(self):
    self.pos[0]+=self.dir[0]
    self.pos[1]+=self.dir[1]
    if self.speedtime:
      self.speedtime-=1
      self.pos[0]+=self.dir[0]
      self.pos[1]+=self.dir[1]
  def dists(self,enemy):
     return [abs(enemy.pos[0]-self.pos[0]),abs(enemy.pos[1]-self.pos[1])]
  def test(self,enemies):
     for enemy in enemies:
        dists=self.dists(enemy)
        mindist={Chaser:4,Dasher:5}[enemy.__class__]
        if dists[0]<mindist and dists[1]<mindist:return True
  def shoot(self,bullets):
    if self.bullets:
      self.bullets-=1
      bullets+=[Bullet(self.pos[:],self.dir[:])]

class Enemy(object):
  def __init__(self,players):
    None
  def dists(self,player):
    return [player.pos[0]-self.pos[0],player.pos[1]-self.pos[1]]

class Chaser(Enemy):
  def __init__(self,players):
    self.spawn(players)
    self.time=50
    self.dir=[0,-3]
  def ai(self,players):
    self.time-=1
    if self.time==0:
      dists=[]
      for player in players:
        if not player.lives:dists+=[10000];continue
        dists+=[dist(self,player)]
      target=players[dists.index(min(dists))]
      xdist=self.dists(target)[0]
      ydist=self.dists(target)[1]
      if abs(xdist)<abs(ydist):
        if ydist<0:self.dir=[0,-3]
        else:self.dir=[0,3]
      else:
        if xdist<0:self.dir=[-3,0]
        else:self.dir=[3,0]
      self.time=50
  def spawn(self,players):
    while True:
      found=True
      self.pos=[random.randint(1,700),random.randint(1,500)]
      for player in players:
        if dist(self,player)<100:found=False
      if found:break
  def draw(self):
    pygame.draw.rect(window,[255,0,0],[self.pos[0]-2,self.pos[1]-2,5,5])

class Dasher(Enemy):
  def __init__(self,players):
    self.spawn(players)
    self.dir=[0,3]
  def spawn(self,players):
    while True:
      found=True
      side=random.choice(['top','bottom','left','right'])
      if side=='top':self.pos=[random.randint(1,700),0];self.dir=[0,8]
      if side=='bottom':self.pos=[random.randint(1,700),500];self.dir=[0,-8]
      if side=='left':self.pos=[0,random.randint(1,700)];self.dir=[8,0]
      if side=='right':self.pos=[700,random.randint(1,700)];self.dir=[-8,0]
      for player in players:
        if dist(self,player)<100:found=False
      if found:break
  def draw(self):
    pygame.draw.rect(window,[255,127,0],[self.pos[0]-3,self.pos[1]-3,7,7])

class Powerup(object):
  def __init__(self,players):
    self.spawn(players)
    self.type=random.choice(['life','speed','time stop','bullet'])
    self.time=800
  def spawn(self,players):
    while True:
      found=True
      self.pos=[random.randint(1,700),random.randint(1,500)]
      for player in players:
        if dist(self,player)<100:found=False
      if found:break
  def draw(self):
    if self.type=='life':pygame.draw.circle(window,[0,255,0],self.pos,5,0)
    if self.type=='speed':pygame.draw.circle(window,[255,255,0],self.pos,5,0)
    if self.type=='time stop':pygame.draw.circle(window,[0,0,255],self.pos,5,0)
    if self.type=='bullet':pygame.draw.circle(window,[127,127,127],self.pos,5,0)
  def test(self,players):
    for player in players:
      dists=player.dists(self)
      if dists[0]<7 and dists[1]<7:return player

class Bullet(object):
  def __init__(self,pos,dir):
    self.pos=pos
    self.dir=dir
    if self.dir[0]==0:
      if self.dir[1]>0:self.dir[1]+=1
      else:self.dir[1]-=1
    else:
      if self.dir[0]>0:self.dir[0]+=1
      else:self.dir[0]-=1
  def draw(self):
    window.set_at(self.pos,[127,127,127])
  def move(self,enemies):
    kill=self.test(enemies)
    self.pos[0]+=self.dir[0]
    self.pos[1]+=self.dir[1]
    if not kill:self.test(enemies)
  def test(self,enemies):
    for enemy in enemies:
      mindist={Chaser:4,Dasher:5}[enemy.__class__]
      if dist(self,enemy)<mindist:
        if enemy.__class__==Chaser:del chasers[chasers.index(enemy)]
        if enemy.__class__==Dasher:del dashers[dashers.index(enemy)]
        del bullets[bullets.index(self)]
        return True

def dist(e1,e2):
  return abs(e1.pos[0]-e2.pos[0])+abs(e1.pos[1]-e2.pos[1])

pygame.init()
window=pygame.display.set_mode((700,500))

players=[Player([150,250],[0,0,255]),Player([250,250],[255,255,0]),Player([350,250],[255,255,255]),Player([450,250],[0,255,0])]
chasers=[Chaser(players),Chaser(players),Chaser(players),Chaser(players)]
dashers=[Dasher(players),Dasher(players),Dasher(players),Dasher(players)]
powerups=[]
bullets=[]
clock=pygame.time.Clock()

poweruptimer=200
enemyspawntimer=500
timestop=0

alive=True
while alive:
  poweruptimer-=1
  if poweruptimer==0:
    powerups+=[Powerup(players)]
    poweruptimer=200
  enemyspawntimer-=1
  if enemyspawntimer==0:
    type=random.randint(1,2)
    if type==1:chasers+=[Chaser(players)]
    if type==2:dashers+=[Dasher(players)]
    enemyspawntimer=500
  if timestop:
    timestop-=1
    enemyspawntimer+=1
    for powerup in powerups:
      powerup.time+=1
  enemies=chasers+dashers
  clock.tick(35)
  for event in pygame.event.get():
    if event.type==pygame.QUIT:sys.exit()
    if event.type==pygame.KEYDOWN:
      if event.key==pygame.K_UP:players[0].dir=[0,-2]
      if event.key==pygame.K_DOWN:players[0].dir=[0,2]
      if event.key==pygame.K_LEFT:players[0].dir=[-2,0]
      if event.key==pygame.K_RIGHT:players[0].dir=[2,0]
      if event.key==pygame.K_PAGEUP:players[0].shoot(bullets)
      if event.key==pygame.K_w:players[1].dir=[0,-2]
      if event.key==pygame.K_s:players[1].dir=[0,2]
      if event.key==pygame.K_a:players[1].dir=[-2,0]
      if event.key==pygame.K_d:players[1].dir=[2,0]
      if event.key==pygame.K_q:players[1].shoot(bullets)
      if event.key==pygame.K_t:players[2].dir=[0,-2]
      if event.key==pygame.K_g:players[2].dir=[0,2]
      if event.key==pygame.K_f:players[2].dir=[-2,0]
      if event.key==pygame.K_h:players[2].dir=[2,0]
      if event.key==pygame.K_r:players[2].shoot(bullets)
      if event.key==pygame.K_i:players[3].dir=[0,-2]
      if event.key==pygame.K_k:players[3].dir=[0,2]
      if event.key==pygame.K_j:players[3].dir=[-2,0]
      if event.key==pygame.K_l:players[3].dir=[2,0]
      if event.key==pygame.K_u:players[3].shoot(bullets)
  window.fill([0,0,0])
  for chaser in chasers:chaser.ai(players)
  for enemy in enemies:
    if not timestop:
      enemy.pos[0]+=enemy.dir[0]
      enemy.pos[1]+=enemy.dir[1]
    enemy.draw()
  alive=False
  for player in players:
    if player.lives<=0:continue
    player.score+=1
    alive=True
    player.move()
    if player.pos[0]<0 or player.pos[0]>700 or player.pos[1]<0 or player.pos[1]>500:
      player.lives-=1
      player.spawn(enemies)
    if player.test(enemies):
      player.lives-=1
      if player.lives:player.spawn(enemies)
    if player.lives:player.draw()
  for dasher in dashers:
    if dasher.pos[0]<0 or dasher.pos[0]>700 or dasher.pos[1]<0 or dasher.pos[1]>500:
      dasher.spawn(players)
  for powerup in powerups:
    powerup.draw()
    player=powerup.test(players)
    if player:
      if powerup.type=='life':player.lives+=1
      if powerup.type=='speed':player.speedtime+=200
      if powerup.type=='time stop':timestop+=100
      if powerup.type=='bullet':player.bullets+=3
      del powerups[powerups.index(powerup)]
  for bullet in bullets:
    bullet.move(enemies)
    bullet.draw()
  pygame.display.flip()

for player in players:
  print(player.score,player.color)
