import pyxel
import copy
import numpy as np
import math
import random
import json


BLOCK_W = 16 #block width
BLOCK_H = 16 #block height


CANBAS_W = 192 #size x
CANBAS_H = 240 #size y

SHIFT_X = 16 #shift x
SHIFT_Y = 0 #shift y

SHIFT_I = SHIFT_X // BLOCK_W #shift i
SHIFT_J = SHIFT_Y // BLOCK_H #shift j

BOARD_W = 8 #size i
BOARD_H = 15  #size j

RICE_NUM = 6
OJAMA = 7

GAME_START_INTERVAL = 15
BUTTON_INTERVAL = 4
SUPRISED_FACE_EFFECT_TIME = 5
ANGLY_FACE_EFFECT_TIME = 5

LEVEL_UP_EFFECT_TIME = 30




stage_dic = {"Main":[0,0,CANBAS_W,CANBAS_H], #texture: x,y,w,h
             "Title":[CANBAS_W,0,CANBAS_W,CANBAS_H]
            }




rice_base_dic = {"Normal"   :[0,0,16,16,0,0,16,16,1], #texture: x,y,w,h, colision: x,y,w,h, transcolor
                 "BoundX"   :[16,0,16,16,0,0,16,16,1],
                 "BoundY"   :[32,0,16,16,0,0,16,16,1],
                 "Surprised":[48,0,16,16,0,0,16,16,1],
                 "Angly"    :[64,0,16,16,0,0,16,16,1],
                 "None"    :[80,0,16,16,0,0,16,16,1],
                 }


rice_type_dic = {"None": [-1,-1], 
                "Yellow":[0,16], #texture shift x,y
                "Peach": [0,32],
                "White": [0,48],
                "Green": [0,64],
                "Blue" : [0,80],
                "Bronw": [0,240],
                "Nakami":[0,0],
}

rice_dic = {}
rice_type_list = []

for key in rice_type_dic:
    rice_type_list.append(key)
    rice_dic[key] = copy.deepcopy(rice_base_dic)
    for rkey in rice_dic[key]:
        rice_dic[key][rkey][0] += rice_type_dic[key][0]
        rice_dic[key][rkey][1] += rice_type_dic[key][1]
        
         
                

omu_dic = {"Stand"    :[0,96,16,16,6], #texture: x,y,w,h, transcolor
           "Punch"    :[16,96,16,16,6],
           "HandsDown":[32,96,16,16,6],
           "HandsUp"  :[48,96,16,16,6],
           "HandsWave":[64,96,16,16,6],
           "Back"     :[80,96,16,16,6],
           "Right"    :[96,96,16,16,6]
           }

item_dic = {"Left":[0,224,8,8,1],
            "Right":[8,224,8,8,1],
            "Up":[0,232,8,8,1],
            "Down":[8,232,8,8,1],
            }

donats_gage_list = [[0 ,208,16,16,6], #texture: x,y,w,h, transcolor}
                    [16,208,16,16,6],
                    [32,208,16,16,6],
                    [48,208,16,16,6]]
DONATS_GAGE_NUM = 4

sound_dic ={"Down":0,
            "Pop":1,
            "GageFull":2,
            "GameOver":3,
            "Garbage":4
            }

nextrice_cell = [8,3,8,4]

gauge_pos = [2,142]
gauge_outer_pos = [0,16,16,128]

omu_pos = [152,192]

start_frame = 0
def setStartFrame():
    global start_frame
    start_frame = pyxel.frame_count


fall_interval = 12
def setFallInterval(val):
    global fall_interval
    fall_interval = val



def getRiceDirectory(type):
    return rice_dic[rice_type_list[type]]

def getDirectedItem(key,dic,dirx=1,diry=1):
    v = copy.deepcopy(dic[key])
    
    if dirx<0:
        v[2]*=-1
    if diry<0:
        v[3]*=-1
    return v[:4] + [v[-1]]



def xy2ij(x,y):
    i = x//BLOCK_W - SHIFT_I
    j = y//BLOCK_H - SHIFT_J
    return i,j

def ij2xy(i,j):
    x = i*BLOCK_W + SHIFT_X
    y = j*BLOCK_H + SHIFT_Y
    return x,y

        

           
class Omu:
    def __init__(self):
        self.x = omu_pos[0]
        self.y = omu_pos[1]
        self.dx = 1
            
        
    def draw(self):
        self.dance_interval = 20
        dance_step = 22
        
        if ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 0:
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("Stand",omu_dic))
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 1:
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("Punch",omu_dic))
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 2:
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("Punch",omu_dic,-1))
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 3:
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("HandsDown",omu_dic))
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 4:
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("HandsUp",omu_dic))
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 5:
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("HandsWave",omu_dic))
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 6:
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("HandsWave",omu_dic,-1))
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 7:
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("HandsWave",omu_dic))
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 8:
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("HandsWave",omu_dic,-1))
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 9:
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("HandsWave",omu_dic))
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 10:
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("Punch",omu_dic))
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 11:
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("Punch",omu_dic,-1))
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 12:
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("Right",omu_dic))
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 13:    
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("Back",omu_dic))
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 14:    
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("Right",omu_dic,-1))
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 15:
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("Stand",omu_dic))
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 16:
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("HandsUp",omu_dic))
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 17:
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("HandsDown",omu_dic))    
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 18:
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("HandsUp",omu_dic))
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 19:
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("Punch",omu_dic))
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 20:
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("Punch",omu_dic,-1))            
        elif ((pyxel.frame_count - start_frame )// self.dance_interval) % dance_step == 21:
            pyxel.blt(self.x,self.y, 0, *getDirectedItem("Punch",omu_dic))



class RiceEffect:
    Normal = 0
    Bound = 1
    Surprised = 2
    Angly = 3
    
    
    


Player_Manual_Move = 0
Player_Ground_Effect = 1
Board_Put_Rice = 2
Board_Check_GameOver = 3
Board_Split = 4
Board_Split_Effect = 5
Board_Erase_Check = 6
Board_Erase_Effect = 7
Board_Erase = 8
Gauge_Check = 9
Board_Special_Event_Effect =10
Board_EMPTY_Event_Effect =11
Board_LevelUp_Effect = 12

game_scene = Player_Manual_Move

def setGameScene(scene):
    global game_scene
    game_scene = scene
    
    
    
TITLE = 0
GAME_PLAY = 1
GAME_OVER = 2

game_mode = 0

def setGameMode(mode):
    global game_mode
    game_mode = mode


class Gauge:
    def __init__(self):
        self.max = 8 * BLOCK_H -4
        self.reset()
        
    def reset(self):
        self.val = 0
        self.isFull = False
        self.isEmpty = False
        
    def update(self,v):
        self.val += v
        
        if self.val > self.max:
            self.val =  self.max
            self.isFull = True
            return True
        if self.val < 0:
            self.val = 0
            self.isEmpty = True
            return True
        
            
        return False

    def draw(self):
        y = gauge_pos[1]-self.val
        pyxel.rect(gauge_pos[0], y, BLOCK_W-4, self.val, 14)
        pyxel.bltm(gauge_outer_pos[0],gauge_outer_pos[1],0,*gauge_outer_pos,6)
        
            



class Rice:
    def __init__(self,t,i,j):

        self.setType(t)
        self.x,self.y = ij2xy(i,j)
        self.effect = RiceEffect.Normal
        self.effect_stime = 0
        
        self.isFloating = False
        self.isInEraseProc = False
        self.isTypeChanging = False
        self.enable = True
        
    def setType(self,t):
        self.type = t
        self.tex_dic = getRiceDirectory(self.type)
        
    
    def changeType(self,t):
        self.setType(t)
        self.setEffect(RiceEffect.Angly)
        self.isTypeChanging = True 
        
    def moveXY(self,x,y):
        self.x = x
        self.y = y
    def moveDxDy(self,dx,dy):
        self.x += dx
        self.y += dy
    def moveIJ(self,i,j):
        x,y = ij2xy(i,j)
        self.x = x
        self.y = y
        self.isFloating = False
        
    def checkGround(self,board):
        i,j = xy2ij(self.x,self.y)
        if board.board[j+1,i] != 0:
            return True
        return False
    
    def getGroundPos(self,board):
        i,j0 = xy2ij(self.x,self.y)
        
        for j in range(j0,BOARD_H):
                if board.board[j,i] != 0:
                    break
        return j-1
    
    
    def getXY(self):
        return self.x,self.y
    
    def getIJ(self):
        return xy2ij(self.x,self.y)
    
    def setEffect(self,e):
        self.effect = e
        self.effect_stime = pyxel.frame_count
        
        
    def setEraseFlag(self):
        self.setEffect(RiceEffect.Surprised)
        self.isInEraseProc = True
        
    def setBoundFlag(self):
        self.setEffect(RiceEffect.Bound)
        
        
    def isTarget(self,i,j):
        _i,_j =  xy2ij(self.x,self.y)
        return (_i==i and _j==j)
    
    def boundDraw(self):
        
        f = ((pyxel.frame_count-self.effect_stime)//2)%4
        if f==0:
            pyxel.blt(self.x, self.y, 0, *getDirectedItem("BoundY",self.tex_dic))
        elif f==1:
            pyxel.blt(self.x, self.y, 0, *getDirectedItem("Normal",self.tex_dic))
        elif f==2:
            pyxel.blt(self.x, self.y, 0, *getDirectedItem("BoundX",self.tex_dic))
        elif f==3:
            pyxel.blt(self.x, self.y, 0, *getDirectedItem("Normal",self.tex_dic))
            self.effect = RiceEffect.Normal
            self.isFloating = False
            
        return
    
    def surprisedDraw(self):

        f = ((pyxel.frame_count-self.effect_stime)//SUPRISED_FACE_EFFECT_TIME)%4
        
        if f==0:
            pyxel.blt(self.x, self.y, 0, *getDirectedItem("Surprised",self.tex_dic))
        elif f==1:
            pyxel.blt(self.x, self.y, 0, *getDirectedItem("None",self.tex_dic))
        elif f==2:
            pyxel.blt(self.x, self.y, 0, *getDirectedItem("Surprised",self.tex_dic))          
        elif f==3:
            pyxel.blt(self.x, self.y, 0, *getDirectedItem("None",self.tex_dic))
            #エフェクト終了後にDisableに
            self.effect = RiceEffect.Normal
            self.isInEraseProc = False
            self.enable = False
        
    def anglyDraw(self):
        
        f = ((pyxel.frame_count-self.effect_stime)//ANGLY_FACE_EFFECT_TIME)%4
        pyxel.blt(self.x, self.y, 0, *getDirectedItem("Angly",self.tex_dic))
    
        
        if f ==3:
            self.isTypeChanging = False
            self.effect = RiceEffect.Normal
    
    def draw(self):
        
        if self.effect == RiceEffect.Normal:        
            pyxel.blt(self.x, self.y, 0, *getDirectedItem("Normal",self.tex_dic))
        elif self.effect == RiceEffect.Bound:
            self.boundDraw()    
        elif self.effect == RiceEffect.Surprised:
            self.surprisedDraw()
        elif self.effect == RiceEffect.Angly:
            self.anglyDraw()
       
        
    
class BoardManage:
    def __init__(self):
        self.initialize()
        
        
    def initialize(self):
        self.gauge = Gauge()
        self.board = np.zeros((BOARD_H,BOARD_W)).astype(np.int32)
        self.initBoard()
        self.chainNum = 0
        self.eraseNum = 0
        self.level_up_score_max = 1000
        self.level_up_score = np.arange(50,self.level_up_score_max+1,50)
        self.hasLevelUp = False
        
     
    def initBoard(self):
        self.board[:,:] = 0
        self.board[:,0] = -1
        self.board[:,-1] = -1
        self.board[-1,:] = -1   
        self.rices = []
        self.gauge.reset()
        self.score = 0
        self.ojama_fall_interval = 20
        self.turn =0
        self.level = 0
        
    
    def colision(self,x,y):
        i,j = xy2ij(x,y)
        if self.board[j,i] != 0:
            return True
        i,j = xy2ij(x+BLOCK_W-1,y+BLOCK_H-1)
        if self.board[j,i] != 0:
            return True
        return False
    
    def getMovablePos(self,x,y,dx,dy):
        if not self.colision(x+dx,y+dy):
            return dx,dy
        
        find = False
        for d in range(BLOCK_H//2,dy+1,BLOCK_H//2):
            if self.colision(x+dx,y+d):
                find = True
                break
        if find:
            return dx,d-BLOCK_H//2
        
        return 0,0
            
        
    
    def checkGround(self,i,j):
        if self.board[j+1,i]!=0:
            return True
        return False

    
    def getIJRice(self,i,j):
        tmp = [r for r in self.rices if r.isTarget(i,j)]
        if len(tmp) == 0:
            return None
        return tmp[0]
        
        

    
    def setAroundOjama(self,i,j):
        pos = [[0,-1],[1,0],[0,1],[-1,0]]
        
        for p in pos:
            ii = i + p[0]
            jj = j + p[1]
            if self.board[jj,ii] == OJAMA:
                r = self.getIJRice(ii,jj)
                if r == None or r.isInEraseProc == False:
                    r.setEraseFlag()
                    continue

        
    
    def setRiceEraseProc(self,i,j):
        r = self.getIJRice(i,j)
        if r == None:
            return
        r.setEffect(RiceEffect.Surprised)
        self.setAroundOjama(i,j)
        
    
       
    def moveRice(self,si,sj,ti,tj):
        
        r = self.getIJRice(si,sj)
        if r == None:
            return
        r.setEffect(RiceEffect.Surprised)
        
        self.board[tj,ti] = self.board[sj,si]
        self.board[sj,si] = 0
        
        r.moveIJ(ti,tj)
        if self.checkGround(ti,tj):
            pyxel.play(3, 0)
            r.setBoundFlag()
        else:
            r.isFloating = True
            
        
    
    #盤面に配置されたライスのうち浮いているものを落下
    def splitRices(self):
        
        fallFlag = False
        
        for i in range(1,BOARD_W-1):
            pos_list = []
            for j in range(0,BOARD_H):
                if self.board[j,i] >0:
                    pos_list.append([j,i])
                elif self.board[j,i] ==0 and len(pos_list) != 0:
                    fallFlag = True
                    for n,t in enumerate(pos_list[::-1]):
                        self.moveRice(t[1],t[0],i,j-n)
                        pos_list = []
                        
        return fallFlag      
        
    
    def searchConnect(self,vs,board,label,lb,tgt,coords):
    
        idxs = [[0,-1],[-1,0],[1,0],[0,1]]
        
        for v in vs:
            label[v[1],v[0]] = lb
            coords.append(v)
            
        nvs = []
        for v in vs:
            for idx in idxs:
                i = v[0]+idx[0]
                j = v[1]+idx[1]
                if board[j,i]==tgt and label[j,i]==0:
                    nvs.append([i,j])
        
        if len(nvs)==0:
            return
        
        self.searchConnect(nvs,board,label,lb,tgt,coords)
    
    def eraseConnection(self):
        lb = 1
        coords_list = []
        label = np.zeros((BOARD_H,BOARD_W)).astype(np.int32)
        
        for j in range(BOARD_H-1):
            for i in range(1,BOARD_W-1):
                if self.board[j,i] > 0 and self.board[j,i] <= RICE_NUM and label[j,i] == 0:
                    coords = []
                    self.searchConnect([[i,j]],self.board,label,lb,self.board[j,i],coords)
                    lb += 1
                    coords_list.append(coords)
                    
        eraseNum = 0
        for coord in coords_list:
            if len(coord)<4:
                continue
            for v in coord:
                eraseNum += 1
                self.setRiceEraseProc(v[0],v[1])
        
        return eraseNum        
        
    
    def eraseDisableRices(self):
        erase_list = [r for r in self.rices if not r.enable]
        self.rices = [r for r in self.rices if r.enable]
        
        for r in erase_list:
            i,j = r.getIJ()
            self.board[j,i] = 0
        setGameScene(Board_Split)      
        
    
    def checkGameOver(self):
        return self.board[1,3] != 0
    
    
    def gaugeMax(self):
        print("GaugeMax")
        if len(self.rices)==0:
            return
        
        
        stype = random.randint(1, RICE_NUM)
        while stype not in self.board:
            stype = random.randint(1, RICE_NUM)

        etype = random.randint(1, RICE_NUM)
        while stype == etype:
            etype = random.randint(1, RICE_NUM)
        
        for j in range(BOARD_H-1):
            for i in range(1,BOARD_W-1):
                if self.board[j,i] == stype:
                    self.board[j,i] = etype
                    tmp = [r for r in self.rices if r.isTarget(i,j)][0]
                    tmp.changeType(etype)
        self.gauge.reset()
        setGameScene(Board_Special_Event_Effect)      
        
        
    def gaugeEvent(self):
        if self.gauge.isFull:
            self.gaugeMax()
    
    def getPushablePosList(self):
        
        pos_list = []
        for i in range(1,BOARD_W-1):
            for j in range(BOARD_H-2,0,-1):
                if self.board[j,i] == 0:
                    pos_list.append([i,j])
                    break
            
        return pos_list
    
    def setOjamaRice(self,i,j):
        if self.board[j,i] != 0:
            return False
        pyxel.play(3, 4)
        
        self.board[j,i] = OJAMA
        r = Rice(OJAMA,i,j)
        r.setBoundFlag()
        self.rices.append(r)
        return True

    def fallOjama(self,repeat,ojamaNum):
        
        if repeat<=0:
            return
        
        #まず1列分のおじゃまらいす
        pos_list = self.getPushablePosList()
        ojama_pos = []
        if ojamaNum<len(pos_list):
            ojama_pos += random.sample(pos_list, ojamaNum)
            ojamaNum = 0
        else:
            ojama_pos += copy.copy(pos_list)
            ojamaNum -= len(pos_list)

        for p in ojama_pos:
            self.setOjamaRice(p[0],p[1])
        
        self.fallOjama(repeat-1,ojamaNum)
        
        setGameScene(Board_EMPTY_Event_Effect)
        

       
                
    
    def increaseTurn(self):
        self.turn += 1
        
        if self.turn % self.ojama_fall_interval == (self.ojama_fall_interval-1):
            self.turn = 0
            ojamaNum = random.randint(2,12)
            self.fallOjama(2,ojamaNum)
            return True
        
        return False                    
        
    
    def setScore(self):
        self.score += self.chainNum*self.eraseNum
        if self.score>9999:
            self.score = 9999
        
        s = self.score
        if s>= self.level_up_score_max:
            s = self.level_up_score_max
            
            
        lv = np.argwhere(s<=self.level_up_score)[0][0]

        
        self.hasLevelUp

        fall_interval = 12 - ((lv+1)//2)*2
        self.ojama_fall_interval = 20 - ((lv)//2)
        
        if fall_interval<2:
            fall_interval = 2
        if self.ojama_fall_interval < 10:
            self.ojama_fall_interval = 10
            
        setFallInterval(fall_interval)
        if self.level < lv:
            self.hasLevelUp =True
            self.hasLevelUp_frame = pyxel.frame_count
            self.level = lv
            pyxel.play(3, 5)
            
            return True

        
        self.level = lv
        
        return False
            
            
    def update(self):
        
        #Scene 
        if game_scene == Board_Split_Effect:
            hasFloating = False
            for r in self.rices:
                if r.isFloating or r.effect != RiceEffect.Normal:
                    hasFloating = True
                    break
            if not hasFloating:
                if self.gauge.isFull:
                    pyxel.play(3, 2)
                    self.gaugeEvent()
                else:
                    setGameScene(Board_Erase_Check)
                
        elif game_scene == Board_Erase_Effect:
            hasErasing = False
            for r in self.rices:
                if r.isInEraseProc or r.effect != RiceEffect.Normal:
                    hasErasing = True
                    break
            if not hasErasing:
                if self.setScore():
                    setGameScene(Board_LevelUp_Effect)
                else:
                    self.gauge.update(self.chainNum*self.eraseNum)
                    setGameScene(Board_Erase)
        
        elif game_scene == Board_Special_Event_Effect:
            hasChanging = False
            for r in self.rices:
                if r.isTypeChanging or r.effect != RiceEffect.Normal:
                    hasChanging = True
                    break
            if not hasChanging:
                setGameScene(Board_Erase)
        elif game_scene == Board_EMPTY_Event_Effect:
            hasBounding = False
            for r in self.rices:
                if r.effect != RiceEffect.Normal:
                    hasBounding = True
                    break
            if not hasBounding:
                setGameScene(Player_Manual_Move)
                
        elif game_scene == Board_LevelUp_Effect:
            if pyxel.frame_count - self.hasLevelUp_frame > LEVEL_UP_EFFECT_TIME:
                self.hasLevelUp = False
                setGameScene(Board_Erase)            
            
        
        #Process
        elif game_scene == Board_Check_GameOver:
            if self.checkGameOver():
                pyxel.play(3, 3)
                setGameMode(GAME_OVER)
            else:
                setGameScene(Board_Split)
        elif game_scene == Board_Split:
            if not self.splitRices():
                setGameScene(Board_Split_Effect)
        elif game_scene == Board_Erase_Check:
            self.eraseNum = self.eraseConnection()
            if self.eraseNum > 0:
                pyxel.play(3, 1)
                self.chainNum += 1
                setGameScene(Board_Erase_Effect)                    
            else:
                self.increaseTurn()
                setGameScene(Player_Manual_Move)
                self.chainNum =0
                
        elif game_scene == Board_Erase:
              self.eraseDisableRices()
              
              
        return      
        
    def pushRice(self,rice):
        i,j = rice.getIJ()
        self.board[j,i] = rice.type
        self.rices.append(copy.copy(rice))
    

    
    def draw(self):
        
        for r in self.rices:
            r.draw()
        
        
        if game_scene == Board_LevelUp_Effect:
            pyxel.rect(60, 90, 40, 12, 0)
            pyxel.text(65,94,"LEVEL UP",10)
        elif game_scene == Board_Special_Event_Effect:
            pyxel.rect(60, 90, 40, 12, 0)
            pyxel.text(63,94,"GAUGE MAX",14)

        self.gauge.draw()
        #Draw Score
        pyxel.text(165,8,"SCORE",7)
        pyxel.text(166,9,"SCORE",0)
        pyxel.text(167,20,str(self.score).zfill(4),7)
        pyxel.text(168,21,str(self.score).zfill(4),0)

        pyxel.text(162,40,f"LEVEL"+str(self.level+1).zfill(2),7)
        pyxel.text(163,41,f"LEVEL"+str(self.level+1).zfill(2),0)
        
        
        return False      
 
        
        
      

class RicePlayer:
    
    def __init__(self,t0,t1,i=3,j=1):
        self.initialize(t0,t1,i,j)      
  
        
        
        
    def initialize(self,t0,t1,i=3,j=1):
        
        
        self.rotdirs = [[0,-1],[1,0],[0,1],[-1,0]]
        self.cur_rot = 0
        
        x,y = ij2xy(i,j)
        self.rice0 = Rice(t0,i,j)
        self.rice1 = Rice(t1,i + self.rotdirs[self.cur_rot][0],j + self.rotdirs[self.cur_rot][1])
        
        self.moving = False
        self.moving_stime = 0
        self.rotating = False
        self.rotating_stime = 0
        self.manualFall = False
        self.ground =False
        self.ground_stime = 0
        self.enable = True
    

    def forcedGround(self,board):
        

        i0,j0 = self.rice0.getIJ()
        i1,j1 = self.rice1.getIJ()
        
        ej0 = self.rice0.getGroundPos(board)
        ej1 = self.rice1.getGroundPos(board)

        ej = np.min([ej0,ej1])
            
        if j0==j1:
            ej0 = ej
            ej1 = ej   
        else:
            ej -=1
            
            if j0<j1:
                ej0 = ej
                ej1 = ej+1
            else:
                ej1 = ej
                ej0 = ej+1
        self.rice0.moveIJ(i0,ej0)
        self.rice1.moveIJ(i1,ej1)
        
        x0,y0 = self.rice0.getXY()
        x1,y1 = self.rice1.getXY()
        
        return
        
    
    
    def update(self,board):
        
        if not self.enable :
            return
            

        dx = 0
        dy = 0
        
        x0,y0 = self.rice0.getXY()
        x1,y1 = self.rice1.getXY()
        
        
            #左右移動
        if not self.moving and pyxel.btn(pyxel.KEY_LEFT):
            dx = -BLOCK_W
            self.moving = True
            self.moving_stime = pyxel.frame_count
        elif not self.moving and pyxel.btn(pyxel.KEY_RIGHT):   
            dx = BLOCK_W
            self.moving = True
            self.moving_stime = pyxel.frame_count
        
        #回転
        if not self.rotating and ( pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_X)):
            if pyxel.btn(pyxel.KEY_X):
                rot = self.cur_rot + 1
                rot %= 4
            elif pyxel.btn(pyxel.KEY_Z):
                rot = self.cur_rot - 1
                rot += 4
                rot %= 4
            
            nx1 = x0 + self.rotdirs[rot][0]*BLOCK_W
            ny1 = y0 + self.rotdirs[rot][1]*BLOCK_H
            if not board.colision(nx1,ny1):
                self.rice1.moveXY(nx1,ny1)
                self.cur_rot = rot
            #     #壁面に接触して回転しようとするとき反対方向に押し出す斥力を生じさせる
            # else:
            #     if self.rotdirs[rot][0]>0:
            #         if not board.colision(x0-BLOCK_W,y0):
            #             self.rice0.moveXY(x0-BLOCK_W,y0)
            #             self.rice1.moveXY(x0,y0)
            #             self.cur_rot = rot
            #     elif self.rotdirs[rot][0]<0:
            #         if not board.colision(x0+BLOCK_W,y0):
            #             self.rice0.moveXY(x0+BLOCK_W,y0)
            #             self.rice1.moveXY(x0,y0)
            #             self.cur_rot = rot
                
            self.rotating = True
            self.rotating_stime = pyxel.frame_count
        
        #強制接地
        if  pyxel.btn(pyxel.KEY_UP):
            self.forcedGround(board)

        #落下処理
        elif  self.manualFall or pyxel.frame_count%fall_interval ==0:
            if pyxel.btn(pyxel.KEY_DOWN):
                dy = BLOCK_H
                self.manualFall = True
            else:
                dy = BLOCK_H//2
                self.manualFall = False
            
        #連続移動しないように
        if self.moving:
            if pyxel.frame_count - self.moving_stime > BUTTON_INTERVAL:
                self.moving = False
        
        if self.rotating:
            if pyxel.frame_count - self.rotating_stime > BUTTON_INTERVAL:
                self.rotating = False
        
        
        #接触判定
        # dx0,dy0 = board.getMovablePos(x0,y0,dx,dy)
        # dx1,dy1 = board.getMovablePos(x0,y0,dx,dy)

        # xidx = np.argmin([np.abs(dx0),np.abs(dx1)])
        # if xidx==0:
        #     dx = dx0
        # else:
        #     dx = dx1
        # dy = np.min([dy0,dy1])
        # if dx!=0 or dy>0:
        #     self.rice0.moveDxDy(dx,dy)
        #     self.rice1.moveDxDy(dx,dy)
        
        
        if not board.colision(x0+dx,y0+dy) and not board.colision(x1+dx,y1+dy):
            self.rice0.moveDxDy(dx,dy)
            self.rice1.moveDxDy(dx,dy)
        elif dy == BLOCK_H:
            dy = BLOCK_H//2
            if not board.colision(x0+dx,y0+dy) and not board.colision(x1+dx,y1+dy):
                self.rice0.moveDxDy(dx,dy)
                self.rice1.moveDxDy(dx,dy)
        
    #接地判定
        if board.checkGround(*self.rice0.getIJ()):
            self.enable = False
            self.rice0.setBoundFlag()
            pyxel.play(3, 0)
            setGameScene(Player_Ground_Effect)
        if board.checkGround(*self.rice1.getIJ()):
            self.enable = False
            self.rice1.setBoundFlag()
            pyxel.play(3, 0)
            setGameScene(Player_Ground_Effect)
       
        return
    
        
    def draw(self):
        
        self.rice0.draw()
        self.rice1.draw()
        
        
        if game_scene==Player_Ground_Effect:
            if self.rice0.effect == RiceEffect.Normal and self.rice1.effect == RiceEffect.Normal:
                setGameScene(Board_Put_Rice)
                
        
        return
    

class App:
    def __init__(self):
        pyxel.init(CANBAS_W, CANBAS_H, title="Rice Puzzle")
        pyxel.load("assets/my_puzzle.pyxres")
        
   
        
        
        self.type0 = random.randint(1, RICE_NUM)
        self.type1 = random.randint(1, RICE_NUM)
        
        self.ntype0 = random.randint(1, RICE_NUM)
        self.ntype1 = random.randint(1, RICE_NUM)

        self.nRice0 = Rice(self.ntype0,nextrice_cell[0],nextrice_cell[1])
        self.nRice1 = Rice(self.ntype1,nextrice_cell[2],nextrice_cell[3])
        
        
        self.player = RicePlayer(self.type0,self.type1)
        self.board  = BoardManage()
        self.omu = Omu()
        
        
        self.isPlayerTurn = True

        pyxel.run(self.update, self.draw)


    def putRice(self):
        
        self.board.pushRice(self.player.rice0)
        self.board.pushRice(self.player.rice1)
        
        
        self.type0 = self.ntype0
        self.type1 = self.ntype1
        
        self.ntype0 = random.randint(1, RICE_NUM)
        self.ntype1 = random.randint(1, RICE_NUM)
        
        self.nRice0.setType(self.ntype0)
        self.nRice1.setType(self.ntype1)
        
        self.player.initialize(self.type0,self.type1)
        setGameScene(Board_Check_GameOver)
        
        
   
    def update(self):
        
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        
        if game_mode == TITLE:
            if pyxel.btn(pyxel.KEY_RETURN):
                setGameMode(GAME_PLAY)
                setStartFrame()         
        
        elif game_mode == GAME_PLAY:
            if pyxel.frame_count-start_frame <= GAME_START_INTERVAL:
                return
            if game_scene == Player_Manual_Move:
                self.player.update(self.board)
            elif game_scene == Board_Put_Rice:    
                self.putRice()
            else:
                self.board.update()
            
        elif game_mode == GAME_OVER:
            if pyxel.btn(pyxel.KEY_RETURN):
                self.board.initBoard()
                setGameScene(Player_Manual_Move)
                setGameMode(GAME_PLAY)
                setStartFrame()         
            
    
    def draw_gameover(self):
        score = self.board.score

        pyxel.cls(0)
        pyxel.bltm(0,0,0,CANBAS_W*2,0,CANBAS_W,CANBAS_H,1)
        
        
        pyxel.text(75, 78, "Game Over ", 6)
        pyxel.text(59, 94, "Your score is "+str(score).zfill(4), 10)
        pyxel.text(45, 110, "- PRESS ENTER to Restart -", 7)
    
    def draw_title(self):
        
        pyxel.cls(6)
        
        #背景
        pyxel.bltm(0,0,0,CANBAS_W,0,CANBAS_W,CANBAS_H,1)

        

        pyxel.text(74, 44, "RICE PUZZLE", 10)
        pyxel.text(73, 43, "RICE PUZZLE", 1)
        pyxel.text(67, 58, "- PRESS ENTER -", 7)
        pyxel.text(66, 57, "- PRESS ENTER -", 1)
        
        
        pyxel.blt(45,  144, 0, *getDirectedItem("Left",item_dic))
        pyxel.blt(55,  144, 0, *getDirectedItem("Right",item_dic))  
        pyxel.blt(55, 160, 0, *getDirectedItem("Down",item_dic))  
        pyxel.blt(55, 176, 0, *getDirectedItem("Up",item_dic))  
      
        pyxel.text(65, 144, " : Rice move", 1)
        pyxel.text(65, 160, " : Rice's down speed up", 1)
        pyxel.text(65, 176, " : Rice fall", 1)
        
        pyxel.text(61, 192, "z : Rice left rotate", 1)
        pyxel.text(61, 208, "x : Rice right rotate", 1)
        
             
    def draw_game(self):
        
        pyxel.cls(12)
        #背景
        pyxel.bltm(0,0,0,0,0,CANBAS_W,CANBAS_H)
        #装飾系
        self.nRice0.draw()
        self.nRice1.draw()
        self.omu.draw()
        
        self.player.draw()
        self.board.draw()            
            
        #背景上部だけ再描画
        pyxel.bltm(BLOCK_W,0,0,BLOCK_W,0,CANBAS_W-BLOCK_W*4,BLOCK_H*2)
        
    def draw(self):
        if game_mode == TITLE:
            self.draw_title()   
        elif game_mode == GAME_PLAY:
            self.draw_game() 
        elif game_mode == GAME_OVER:
            self.draw_gameover()   

App()
