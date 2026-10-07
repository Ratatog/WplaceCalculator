from math import ceil

lvl = 0
pxs = 0

for i in range(1,24000):
    res = ceil( (lvl * (30**.65)) ** (1/.65) - pxs )
    print(f"{lvl} > {lvl+1}: {res}", pxs + res)
    pxs += res
    lvl += 1
    
    droplets = lvl*500+pxs
    time = str(round(pxs/2/60/24, 3))
    max_pxs = 60 + (lvl*7) + (pxs//500*5)
    
    if res >= 1000: 
        break
    
    
print(f'''
lvl: {lvl}
pixels: {pxs}
droplets: {droplets}
time: {time} days
max pixels: {max_pxs}
''')