import math

def xy2degree(x,y):
    ans = 0
    if math.atan2(x,y)/math.pi*180 < 0:
        ans = math.atan2(x,y)/math.pi*180 + 360
    else:
        ans = math.atan2(x,y)/math.pi*180
    return(ans)
    
    
print(xy2degree(-1,-1)+90)