def lerp(a, b, t):
    if (a+(b-a)*t) == 0:
        return ((1-t)*a + t*b)
    return (((1-t)*a + t*b)/(a+(b-a)*t))

def ilerp(a, b, c):
    if (b-1) == 0:
        return (c-a)
    return ((c-a)/(b-1))

def remap(c, a, b, a2, b2):
    return lerp(a2, b2, ilerp(a, b, c))