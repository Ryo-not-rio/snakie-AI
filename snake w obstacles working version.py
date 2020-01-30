import pygame as py
from operator import itemgetter
import random,time,copy,array
import matplotlib.pyplot as plt
import numpy as np

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

line=py.draw.line
randint=random.randint
randchoice=random.choice
deepcopy=copy.deepcopy
frender=font.render
dblit=display.blit


##creating the snake
snakelist=[]
squarenum=4   #has to be even
size=10
divide=2
start=0
for b in range(squarenum):
    if b==0:
        colour=red
    elif b==squarenum-1:
        colour=pink
    else:
        colour=[round(200/squarenum)*b,255,round(200/squarenum)*b]
    snakelist.append([start-size*2*b,round(displayheight/2),
                         colour])
orsnakelist=snakelist

creaturenum=10
inputlength=squarenum*2
outputlength=squarenum*2
l1length=inputlength
l2length=inputlength
weightlimits=10
aboveweight=1
weight1=[]
weight2=[]
weight3=[]
for i in range(creaturenum):
    weight1.append([])
    weight2.append([])
    weight3.append([])
for a in range(creaturenum):
    for i in range(inputlength*l1length):
        weight1[a].append(randint(-1*weightlimits,weightlimits)*(aboveweight/weightlimits))
    for i in range((l1length+1)*(l2length+1)):
        weight2[a].append(randint(-1*weightlimits,weightlimits)*(aboveweight/weightlimits))
    for i in range((l2length+1)*outputlength):
        weight3[a].append(randint(-1*weightlimits,weightlimits)*(aboveweight/weightlimits))


goalsize=20
goalx,goaly=displaywidth-goalsize*4,round(displayheight/2)

fitnesslist=[]
for i in range(creaturenum):
    fitnesslist.append(0)
    
def changerange(value,minimum,maxmovement,size):
    newvalue=(((value-minimum)*((maxmovement+size*2)*2))/(maximum-minimum))-maxmovement-size*2
    return round(newvalue,3)
    
def changer2(OldValue,OldMin,NewMin,OldMax,NewMax):
    NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
    return round(NewValue,3)
    
def output(inp,weights,layerlength,rounds):
    layer=[]
    count=0
    for a in range(layerlength):
        total=0
        for b in inp:  
            total+=b*weights[count]
            count+=1
        layer.append(round(total,rounds))
    return layer

def mutate(weights1,weights2):
    randint=random.randint
    randchoice=random.choice
    mutechoice=[0.8,0.5,0.07,0.1,0.07,0.05,0.3,0.01,0.01]
    muterate=mutechoice[muteindex%len(mutechoice)]
    weights=[]
    wappend=weights.append
    for i in range(len(weights1)):
        choice=randint(0,1000)
        if choice<=1000*muterate:
            if muterate<=0.1:
                choosing=randchoice([weights1,weights2])
                wappend(choosing[i]+((aboveweight/weightlimits)*randchoice([-1,1]*randint(1,3))))
            else:
                wappend(randint(-1*weightlimits,weightlimits)*(aboveweight/weightlimits))
        elif i%2==0:
            wappend(weights1[i])
        else:
            wappend(weights2[i])
    return weights

def evolve(fitnesslis,w1,w2,w3):
    newweight1=[x for _,x in sorted(zip(fitnesslis,w1))]
    newweight2=[x for _,x in sorted(zip(fitnesslis,w2))]
    newweight3=[x for _,x in sorted(zip(fitnesslis,w3))]
    newfitness=sorted(fitnesslis)
#     print(newfitness)
#     time.sleep(1)
    choosef=[]
    chooses=[]
    chooset=[]
    for i in range(round(len(newweight1)*0.8)):
        weightf=newweight1[i]
        weights=newweight2[i]
        weightt=newweight2[i]
        for j in range(len(newweight1)-i):
            choosef.append(weightf)
            chooses.append(weights)
            chooset.append(weightt)
    bye=[]
    for i in range(round(len(weight1))):
        for j in range(len(weight1)-1-i):
            bye.append(len(weight1)-1-i)
    for i in range(round(len(weight1)*0.5),len(newweight1)):
        choice=randint(0,len(choosef)-1)
        choice1=randint(0,len(choosef)-1)
        change=randchoice(bye)
        newweight1[change]=mutate(choosef[choice],choosef[choice1])
        newweight2[change]=mutate(chooses[choice],chooses[choice1])
        newweight3[change]=mutate(chooset[choice],chooset[choice1])
        while change in bye:
            bye.remove(change)
    return newweight1,newweight2,newweight3


##distance(x1,y1,x2,y2)
def distance(a,b,c,d):
    dist=round(((a-c)**2+(d-b)**2)**0.5,3)   
    return dist

def calcaverage(lists):
    total=0
    for i in lists:
        total+=i
    return round(total/len(lists),3)

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
        label=frender("generation:"+str(generation),False,white)
        dblit(label,(100,50))
        label=frender("best:"+str(best[len(best)-1]),False,white)
        dblit(label,(100,100))
        label=frender("average:"+str(fitnesses[len(fitnesses)-1]),False,white)
        dblit(label,(100,150))
        line(display,white,[i*xgap,beforefit],[(i+1)*xgap,fit],3)
        line(display,blue,[i*xgap,befbes],[(i+1)*xgap,bes],3)
    py.display.update()


gameexit=False
fps=0
contracted=False
instcount=0
change=0
maxmovement=40
minmovement=10
snakecount=0
generation=1
show=False
changelimit=110
fitnesslist=[]
generations=[]
fitnesses=[]
best=[]
instr=[]
starttime=time.time()
count=0
gencount=0
framelimit=150
changed=True
fpschanged=False
new=False
orframelimit=framelimit
maximum=0
minimum=0
changelim=50
muteindex=0
mindexchange=600
obsnum=0
obsradius=80
obstacles=[[120,round(displayheight/2)]]
imin=1
imax=0

while not gameexit:
    if (generation+1)%100==0:
        muteindex+=1
    count+=1 
    gencount+=1
    if len(generations)>200:
        removing=[]
        counting=len(generations)-1
        for i in range(1,len(fitnesses),2):
            fitnesses[i]=False
            generations[counting]=False
            best[i]=False
            counting-=1
        while False in fitnesses or False in generations or False in best:
            fitnesses.remove(False)
            generations.remove(False)
            best.remove(False)
        gencount=generations[len(generations)-1]+2
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
            
    if not new: 
        if instcount<=creaturenum-1:
            if count<framelimit:
                if changed:
                    changed=False
                    w1=weight1[instcount]
                    w2=weight2[instcount]
                    w3=weight3[instcount]
                    inputted=[]
                    dists=[]
                    headx,heady=snakelist[0][0],snakelist[0][1]
                    for i in obstacles:
                        dists.append(distance(headx,heady,i[0],i[1]))
                    if obsnum>0:
                        if min(dists)<obsradius+10+50:
                            inputted.append(changer2((obstacles[dists.index(min(dists))][0]-headx),imin,-10,imax,10))
                            inputted.append(changer2((obstacles[dists.index(min(dists))][1]-heady),imin,-10,imax,10))
                        else:
                            inputted.append(changer2((headx/100),imin,-10,imax,10))
                            inputted.append(changer2((heady/100),imin,-10,imax,10))
                    else:
                        inputted.append(changer2(0,imin,-10,imax,10))
                        inputted.append(changer2(0,imin,-10,imax,10))
                    for a in range(1,len(snakelist),1):
                        for b in range(0,len(snakelist[a])-2):
                            inputted.append(changer2((snakelist[a-1][b]-snakelist[a][b]),imin,-10,imax,10))
                    if generation%20==0:
                        if imin>min(inputted):
                            imin=min(inputted)
                        if imax<max(inputted):
                            imax=max(inputted)
                    l1=output(inputted,deepcopy(w1),l1length,3)
                    l1.append(1)
                    l2=output(l1,deepcopy(w2),l2length,3)
                    l2.append(1)
                    finish=deepcopy(output(l2,deepcopy(w3),outputlength,3))

                    if maximum<max(finish) and generation%100==0 or generation<changelim:
                        maximum=max(finish)
                        muteindex=0
                    if min(finish)<minimum and generation%100==0 or generation<changelim:
                        minimum=min(finish)   
                        muteindex=0 
                    
                    for i in range(0,round(len(finish)),2):
                        instr.append([changerange(finish[i],minimum,maxmovement,size),changerange(finish[i+1],minimum,maxmovement,size)])
                        #instr.append([finish[i],finish[i+1]])
                        
                for a in range(len(snakelist)):
                    inst=instr[a]
                    instx,insty=inst[0],inst[1]
                    bumped=False
                    snake=snakelist[a]
                    x,y=deepcopy(snake[0]),deepcopy(snake[1])
                    for obs in obstacles:
                        if distance(obs[0],obs[1],x+instx,y+insty)<10+obsradius:
                            bumped=True
                    if distance(instx,insty,0,0)>minmovement and not bumped and y-insty>0 and y+insty<displayheight:
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
                        display.fill(black)
                        fitness=distance(goalx,goaly,snakelist[0][0],snakelist[0][1])
                        label=frender("time:"+str(framelimit-count),False,white)
                        dblit(label,(200,displayheight-150))
                        label=frender("fitness:"+str(fitness),False,white)
                        dblit(label,(200,displayheight-120))
                        label=frender("generation:"+str(generation),False,white)
                        dblit(label,(200,displayheight-90))
                        label=frender("creature:"+str(snakecount),False,white)
                        dblit(label,(200,displayheight-60))
                        label=frender("fps:"+str(fps),False,white)
                        dblit(label,(200,displayheight-30))
                        ##showing the snake
                        for a in range(len(snakelist)):
                            snake=snakelist[a]
                            x=snake[0]
                            y=snake[1]
                            colour=snake[2]
                            py.draw.circle(display,colour,[round(x),round(y)],size,1)
                            
                            if a!=len(snakelist)-1:
                                left=snakelist[a+1]
                                leftx,lefty=left[0],left[1]
                                line(display,blue,[x,y],[leftx,lefty],3)
                        for i in obstacles:
                            py.draw.circle(display,red,i,obsradius)
                        
                        if fps>100 and not fpschanged:
                            fpschanged=True
                            fps=100
                        py.draw.circle(display,yellow,[goalx,goaly],goalsize)
                        line(display,white,[start,0],[start,displayheight],2)
                        py.display.update()
                        clock.tick(fps)
                    else:
                        fps=0
                        fpschanged=False  
                            
                
                if change==changelimit:
                    changed=True
                    change=0
                change+=1
                
            else:
                instr=[]
                change=0
                changed=True
                head=snakelist[0]
                headx,heady=head[0],head[1]
                fitness=distance(headx,heady,goalx,goaly)
                fitnesslist.append(fitness)
                instcount+=1
                count=0
                snakecount+=1
                snakelist=deepcopy(orsnakelist)
        else:
            count=0
            change=0
            changed=True
            snakecount=0
            generation+=1
            weight1,weight2,weight3=evolve(deepcopy(fitnesslist), deepcopy(weight1), deepcopy(weight2),deepcopy(weight3))
            fitnesslist=sorted(fitnesslist)
            averaged=calcaverage(fitnesslist)
            #print(averaged)
            generations.append(gencount)
            best.append(fitnesslist[0])
            fitnesses.append(averaged)
            instcount=0
            fitnessesw=[]
            bestw=[]
            for i in fitnesses:
                fitnessesw.append(changer2(i,0,0,max(fitnesses),displayheight))
            for i in best:
                bestw.append(changer2(i, 0, 0, max(fitnesses), displayheight))
            instcount=0
            if not show:
                fps=0
                drawgraph(fitnessesw,generations,bestw)
            fitnesslist=[]
            if generation%15==0:
                obstacles=[]
                for i in range(obsnum):
                    obstacles.append([randint(80,displaywidth-80),randint(50,displayheight-50)])
    else:
        new=False    
    
    
py.quit()