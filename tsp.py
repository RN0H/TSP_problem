import random
import matplotlib.pyplot as plt
plt.ion() #interactive mode
fig = plt.figure()
plt.axis([0,50,0,50])
random.seed(1)
cities = []
groups = []
gen = []
def create_cities(n,population_size):
    random.shuffle(cities)
    cities.extend([(random.randint(1,random.randint(1,20)),random.randint(1,random.randint(1,20))) for _ in range(n)])
    if len(set(cities))<n:
         return create_cities(n-len(set(cities)),population_size)
    return create_groups(cities,population_size)

def create_groups(cities,population_size):
    random.shuffle(groups)
    for _ in range(population_size):
         dup = cities.copy()
         random.shuffle(dup)
         groups.append(tuple(dup))
    if len(set(groups))<population_size:
               return create_groups(cities,population_size-len(set(groups)))
    return groups

def fit(group):
    fit = 0
    for i in range(1,len(group)):
         fit+=(abs((group[i-1][0]-group[i][0])**2)+(abs(group[i-1][1]-group[i][1])**2))**0.5
    return fit

def cross(gen):
    p1 = random.choice(gen)
    p2 = random.choice(gen)
    child = []
    if p1==p2:
          dup = gen.copy()
          if random.random()<0.5:
              dup.remove(p1)
              p2 = random.choice(dup)
          else:
                dup.remove(p2)
                p1 = random.choice(dup)
    for k,v in zip(p1,p2):
            if random.random()<0.3 and v not in child:
                  child.append(v)
            elif random.random()<0.6 and k not in child:
                  child.append(k)
            else:
                  child.append(random.choice(random.choice(gen)))
    if len(set(child))<len(p1):
              return cross(gen)
    else:
              return tuple(child)


def driver(n):
        population_size = 10
        gen = create_cities(n,population_size)
        epoch = 0
        while epoch<1000:
            gen = sorted(gen,key=lambda group:fit(group))
            print("route is {}    total distance of {}km     epoch {} ".format(gen[0],round(fit(gen[0]),5),epoch))
            x = [k for k,v in gen[0]]
            y = [v for k,v in gen[0]]
            plt.cla()
            plt.plot(x,y,color= 'green',linestyle = 'dashed',marker='o')
            plt.show()
            plt.pause(0.001)
            new_gen = []
            new_gen.extend(tuple(gen[0:population_size//4]))
            for _ in range(population_size-population_size//4):
                  new_gen.append(cross(gen))
            gen = new_gen
            epoch+=1
