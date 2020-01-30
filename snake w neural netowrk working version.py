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
squarenum=2   #has to be even
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
orsnakelist=snakelist

creaturenum=15
inputlength=squarenum*2
outputlength=squarenum*2
l1length=inputlength*5
weightlimits=10
aboveweight=1
weight1=[]
weight2=[]
tweight1=[]
tweight2=[]
for i in range(creaturenum):
    weight1.append([])
    weight2.append([])
    tweight1.append([])
    tweight2.append([])
for a in range(creaturenum):
    for i in range(inputlength*l1length):
        weight1[a].append(random.randint(-1*weightlimits,weightlimits)*(aboveweight/weightlimits))
        tweight1[a].append(1)
    for i in range((l1length+1)*outputlength):
        weight2[a].append(random.randint(-1*weightlimits,weightlimits)*(aboveweight/weightlimits))
        tweight2[a].append(1)


goalsize=20
goalx,goaly=displaywidth-goalsize*4,round(displayheight/2)

fitnesslist=[]
for i in range(creaturenum):
    fitnesslist.append(0)
    
def changerange(value):
    newvalue=(((value-minimum)*((maxmovement+size*2)*2))/(maximum-minimum))-maxmovement-size*2
    return newvalue
    
def output(inp,weights,layerlength,rounds):
    layer=[]
    count=0
    for a in range(layerlength):
        total=0
        for b in range(len(inp)):  
#             print(len(weights),count)
            total+=inp[b]*weights[count]
            count+=1
        layer.append(round(total,rounds))
    return layer

def mutate(weight1,weight2):
    weights1,weights2=weight1,weight2
    divide=5
    mutechoice=[0.5,0.1,0.3,0.1,0.07,0.3,0.05,0.02,0.01]
    if round((generation/divide)*0.01)<=len(mutechoice)-1:
        muterate=mutechoice[round((generation/divide)*0.01)]
    else:
        muterate=random.choice(mutechoice)
    weights=[]
    for i in range(len(weights1)):
        choice=random.randint(0,1000)
        if choice<=1000*muterate:
            if muterate<=0.07:
                choosing=random.choice([weights1,weights2])
                weights.append(copy.deepcopy(choosing[i])+((aboveweight/weightlimits)*random.choice([-1,1]*random.randint(1,3))))
            else:
                weights.append(random.randint(-1*weightlimits,weightlimits)*(aboveweight/weightlimits))
        elif i%2==0:
            weights.append(weights1[i])
        else:
            weights.append(weights2[i])
    return weights

def evolve(fitnesslis,w1,w2):
    newweight1=[x for _,x in sorted(zip(fitnesslis,w1))]
    newweight2=[x for _,x in sorted(zip(fitnesslis,w2))]
    newfitness=sorted(fitnesslis)
#     print(newfitness)
#     time.sleep(1)
    choosef=[]
    chooses=[]
    for i in range(round(len(newweight1)*0.8)):
        weightf=newweight1[i]
        weights=newweight2[i]
        for j in range(len(newweight1)-i):
            choosef.append(weightf)
            chooses.append(weights)
    bye=[]
    for i in range(round(len(weight1)*0.5)):
        bye.append(len(weight1)-1-i)
    done=[]
    for i in range(round(len(weight1)*0.5),len(newweight1)):
        choice=random.randint(0,len(choosef)-1)
        choice1=random.randint(0,len(choosef)-1)
        change=random.choice(bye)
        while change in done:
            change=random.choice(bye)
        newweight1[change]=mutate(choosef[choice],choosef[choice1])
        newweight2[change]=mutate(chooses[choice],chooses[choice1])
        done.append(change)
    return newweight1,newweight2


##distance(x1,y1,x2,y2)
def distance(a,b,c,d):
    dist=round(((a-c)**2+(d-b)**2)**0.5,3)   
    return dist

def calcaverage(lists):
    total=0
    for i in lists:
        total+=i
    return round(total/len(lists),3)
def calcaverage2(lists):
    total=0
    for i in lists:
        total+=abs(i)
    return round(total/len(lists),3)

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


gameexit=False
fps=0
contracted=False
instcount=0
change=0
maxmovement=30
minmovement=10
snakecount=0
generation=1
show=False
changelimit=150
fitnesslist=[]
generations=[]
fitnesses=[]
best=[]
instr=[]
starttime=time.time()
count=0
gencount=0
framelimit=100
changed=True
fpschanged=False
new=False
orframelimit=framelimit
maximum=0
minimum=0
rangelim=50

while not gameexit:
    count+=1 
    gencount+=1
    if len(generations)>200:
        removing=[]
        counting=len(generations)-1
        for i in range(len(fitnesses)):
            if (i+1)%2==0:
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
            if event.key==py.K_r:
                instcount=0
                change=0
                changed=True
                new=True
                squarenum+=2
                snakecount=0
                count=0
                inputlength=squarenum*2
                outputlength=squarenum*2
                l1length+=2
                for a in range(creaturenum):
                    while len(weight1[a])<inputlength*l1length:
                        weight1[a].append(random.choice(weight1[a]))
                    while len(weight2[a])<l1length*outputlength:
                        weight2[a].append(random.choice(weight2[a]))
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
                orsnakelist=copy.deepcopy(snakelist)
    if not new: 
        if instcount<=creaturenum-1:
            if count<framelimit:
                if changed:
                    changed=False
                    w1=weight1[instcount]
                    w2=weight2[instcount]
                    inputted=[]
                    inputted.append(0)
                    inputted.append(0)
                    for a in range(1,len(snakelist),1):
                        for b in range(0,len(snakelist[a])-2):
                            inputted.append((snakelist[a-1][b]-snakelist[a][b]))
                    l1=output(copy.deepcopy(inputted),copy.deepcopy(w1),l1length,3)
                    l1.append(1)
                    finish=copy.deepcopy(output(copy.deepcopy(l1),copy.deepcopy(w2),outputlength,3))

                    if maximum<max(finish) and generation%100==0 or generation<5:
                        maximum=max(finish)
                    if min(finish)<minimum and generation%100==0 or generation<5:
                        minimum=min(finish)    
                    
                    for i in range(0,round(len(finish)),2):
                        instr.append([changerange(finish[i]),changerange(finish[i+1])])
                        #instr.append([finish[i],finish[i+1]])
                        
                for a in range(len(snakelist)):
                    inst=instr[a]
                    instx,insty=copy.deepcopy(inst[0]),copy.deepcopy(inst[1])
                    if distance(instx,insty,0,0)>minmovement:
                        snake=snakelist[a]
                        x,y=copy.deepcopy(snake[0]),copy.deepcopy(snake[1])
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
                        label=font.render("time:"+str(framelimit-count),False,white)
                        display.blit(label,(200,displayheight-150))
                        label=font.render("fitness:"+str(fitness),False,white)
                        display.blit(label,(200,displayheight-120))
                        label=font.render("generation:"+str(generation),False,white)
                        display.blit(label,(200,displayheight-90))
                        label=font.render("creature:"+str(snakecount),False,white)
                        display.blit(label,(200,displayheight-60))
                        label=font.render("fps:"+str(fps),False,white)
                        display.blit(label,(200,displayheight-30))
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
                                py.draw.line(display,blue,[x,y],[leftx,lefty],3)
                        
                        if fps>100 and not fpschanged:
                            fpschanged=True
                            fps=100
                        py.draw.circle(display,yellow,[goalx,goaly],goalsize)
                        py.draw.line(display,white,[start,0],[start,displayheight],2)
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
                snakelist=copy.deepcopy(orsnakelist)
        else:
            count=0
            change=0
            changed=True
            snakecount=0
            generation+=1
            weight1,weight2=evolve(copy.deepcopy(fitnesslist), copy.deepcopy(weight1), copy.deepcopy(weight2))
            fitnesslist=sorted(fitnesslist)
            averaged=calcaverage(fitnesslist)
            #print(averaged)
            generations.append(gencount)
            best.append(fitnesslist[0])
            fitnesses.append(averaged)
            instcount=0
            if not show:
                drawgraph(fitnesses,generations,best)
            fitnesslist=[]
    else:
        new=False    
    
    
py.quit()