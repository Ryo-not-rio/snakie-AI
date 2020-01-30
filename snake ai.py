import pygame as py
from operator import itemgetter
import random,time,copy
import matplotlib.pyplot as plt

py.init()
displaywidth=1500
displayheight=800

display=py.display.set_mode((displaywidth,displayheight))
clock=py.time.Clock()
font=py.font.SysFont(None,40)

##colours
black=[0,0,0]
white=[255,255,255]
gray=[180,180,180]
green=[0,255,0]
red=[255,0,0]
pink=[255,0,255]
blue=[100,100,255]
yellow=[255,255,0]

##creating the snake
snakelist=[]
squarenum=8
size=10
divide=2
start=round(displaywidth/divide)
for b in range(squarenum):
    if b==0:
        colour=red
    elif b==squarenum-1:
        colour=pink
    else:
        colour=[round(200/squarenum)*b,255,round(200/squarenum)*b]
    snakelist.append([round(displaywidth/divide)-size*2*b,round(displayheight/2),
                         colour])

creaturenum=10
##creating instructions
instnum=150
instructions=[]
for j in range(creaturenum):
    instructions.append([])
for a in range(creaturenum):
    for i in range(instnum):
        instructions[a].append([])
for j in range(creaturenum):
    for a in range(instnum):
        for b in range(squarenum):
            x=random.randint(-200,200)*0.01
            y=random.randint(-200,200)*0.01
            instructions[j][a].append([x,y]) 
#time.sleep(100) 
##goal
goalsize=20
goalx,goaly=displaywidth-goalsize*4,round(displayheight/2)

fitnesslist=[]
for i in range(creaturenum):
    fitnesslist.append(0)

##distance(x1,y1,x2,y2)
def distance(a,b,c,d):
    dist=round(((a-c)**2+(d-b)**2)**0.5,3)   
    #print(dist)
    return dist


def mix(first,second):
    newinst=[]
    mutate=100*0.1
    for i in range(instnum):
        if i<instnum/2:
            newinst.append(first[i])
        else:
            newinst.append(second[i])
    for a in range(len(newinst)):
        for b in range(len(newinst[a])):
            for c in range(len(newinst[a][b])):
                choice=random.randint(1,100)
                if choice<=mutate:
                    newinst[a][b][c]=random.randint(-200,200)*0.01
    return newinst

def average(fitnesses):
    total=0
    for i in fitnesses:
        total+=i[0]
    return round(total/len(fitnesses),3)

def drawgraph(fitnesses,generations,best):
    display.fill(black)
    maxfitness,minfitness=max(fitnesses),min(fitnesses)
    xgap=(displaywidth-20)/len(generations)
    for i in range(1,len(generations)):
        gen=generations[i]
        fit=fitnesses[i]
        beforefit=fitnesses[i-1]
        bes=best[i]
        befbes=best[i-1]
        label=font.render("generation:"+str(generation),False,white)
        display.blit(label,(100,50))
        label=font.render("best:"+str(best[len(best)-1]),False,white)
        display.blit(label,(100,100))
        label=font.render("average:"+str(fitnesses[len(fitnesses)-1]),False,white)
        display.blit(label,(100,150))
        py.draw.line(display,white,[i*xgap,beforefit],[(i+1)*xgap,fit],3)
        py.draw.line(display,blue,[i*xgap,befbes],[(i+1)*xgap,bes],3)
    py.display.update()
# print(mix([[[1,2],[3,4]],[[2,1],[4,3]]],[[[5,6],[7,8]],[[6,5],[8,7]]]))
# time.sleep(100)
gameexit=False
fps=1000000000000000000
contracted=False
instcount=0
change=0
maxmovement=8
snakecount=0
generation=1
show=False
changelimit=size*1.5
fitnesslist=[]
generations=[]
fitnesses=[]
best=[]
starttime=time.time()
while not gameexit:
    for event in py.event.get():
            if event.type==py.QUIT:
                gameexit=True
            if event.type==py.KEYDOWN:
                if event.key==py.K_RETURN:
                    if show==True:
                        show=False
                    else:
                        show=True
                if event.key==py.K_w:
                    fps+=10
                if event.key==py.K_s:
                    fps-=10
                if event.key==py.K_e:
                    fps+=100
                if event.key==py.K_d:
                    fps-=100
    if show==True:
        display.fill(black)
    
    ##executing instructions!!!!!!!!!!
    if instcount<=len(instructions[snakecount])-1:
        instr=instructions[snakecount]
#         if snakecount>0:
#             rightinst=instructions[snakecount-1]
#             if rightinst==instr:
#                 print("same")
        
        instruction=instr[instcount]
        for a in range(len(snakelist)):
            inst=instruction[a]
            instx,insty=inst[0],inst[1]
            snake=snakelist[a]
            x,y=snake[0],snake[1]
            if a!=0 and a!=len(snakelist)-1:
                right,left=snakelist[a-1],snakelist[a+1]
                rightx,righty,leftx,lefty=right[0],right[1],left[0],left[1]
                leftdist=distance(x+instx,y+insty,leftx,lefty)
                rightdist=distance(x+instx,y+insty,rightx,righty)
                if leftdist>=size*2 and leftdist<size*2+maxmovement:
                    if rightdist>=size*2 and rightdist<size*2+maxmovement:
                        snakelist[a][0]+=instx
                        snakelist[a][1]+=insty
            elif a==0:
                left=snakelist[a+1]
                leftx,lefty=left[0],left[1]
                leftdist=distance(x+instx,y+insty,leftx,lefty)
                if leftdist>=size*2 and leftdist<size*2+maxmovement:
                    snakelist[a][0]+=instx
                    snakelist[a][1]+=insty
            else:
                right=snakelist[a-1]
                rightx,righty=right[0],right[1]
                rightdist=distance(x+instx,y+insty,rightx,righty)
                if rightdist>=size*2 and rightdist<size*2+maxmovement:
                    snakelist[a][0]+=instx
                    snakelist[a][1]+=insty
            if show:
                fitness=distance(goalx,goaly,snakelist[0][0],snakelist[0][1])
                label=font.render("fitness:"+str(fitness),False,white)
                display.blit(label,(200,displayheight-120))
                label=font.render("generation:"+str(generation),False,white)
                display.blit(label,(200,displayheight-90))
                label=font.render("creature:"+str(snakecount),False,white)
                display.blit(label,(200,displayheight-60))
                label=font.render("fps:"+str(fps),False,white)
                display.blit(label,(200,displayheight-30))
                    
        change+=1
        if change==changelimit:
            change=0
            instcount+=1
    else:
        #end of a snake
        ##resetting snake!
        if snakecount<creaturenum-1:
            snake=snakelist[0]
            x,y=snake[0],snake[1]
            fitness=distance(goalx,goaly,x,y)
            fitnesslist.append([fitness,snakecount])
            snakecount+=1
#             if show==True:
#                 print(snakecount)
        else:
            #end of a generation
            fitnesslist=sorted(fitnesslist, key = itemgetter(0))
            averaged=average(fitnesslist)
            generations.append(generation)
            best.append(fitnesslist[0][0])
            fitnesses.append(averaged)
            newfitnesslist=[]
            for i in range(len(fitnesslist)):
                for b in range(len(fitnesslist)-i):
                    newfitnesslist.append(fitnesslist[i])
            delete=[]
            for i in range(round(len(fitnesslist)/2)):
                fitness=fitnesslist[len(fitnesslist)-i-1]
                delete.append(instructions[fitness[1]])
            while len(instructions)<creaturenum+len(delete):
                first=random.choice(newfitnesslist)
                second=random.choice(newfitnesslist)
                while second==first:
                    second=random.choice(newfitnesslist)
                newinstructions=copy.deepcopy(instructions)
                newfirst,newsecond=newinstructions[first[1]],newinstructions[second[1]]
                new=mix(newfirst,newsecond)
                instructions.append(new)
            for i in delete:
                instructions.remove(i)
                
            snakecount=0
            generation+=1
            fitnesslist=[]
            if not show:
                drawgraph(fitnesses,generations,best)
            
        instcount=0
        snakelist=[]
        for b in range(squarenum):
            if b==0:
                colour=red
            elif b==squarenum-1:
                colour=pink
            else:
                colour=[round(200/squarenum)*b,255,round(200/squarenum)*b]
            snakelist.append([round(displaywidth/divide)-size*2*b,round(displayheight/2),
                              colour])
            
    
    ##showing the snake
    for b in range(len(snakelist)):
        snake=snakelist[b]
        x=snake[0]
        y=snake[1]
        colour=snake[2]
        if show==True:
            py.draw.circle(display,colour,[round(x),round(y)],size,1)
        
        if b!=len(snakelist)-1:
            left=snakelist[b+1]
            leftx,lefty=left[0],left[1]
            if show==True:
                py.draw.line(display,blue,[x,y],[leftx,lefty],3)
    
    if show==True:
        if fps>1000:
            fps=1000
        py.draw.circle(display,yellow,[goalx,goaly],goalsize)
        py.draw.line(display,white,[start,0],[start,displayheight],2)
        py.display.update()
        clock.tick(fps)
    else:
        fps=10000000000000
#     endtime=time.time()
#     if endtime-starttime>=1800:
#         print(best[len(best)-1],fitnesses[len(fitnesses)-1])
#         gameexit=True
    
py.quit()