### Rotation Matrices
- anticlockwise rotation looking at origin, clockwise rotation of axis itself

```
Rx(a) = [1     0      0   ]
        [0  cos(a) -sin(a)]
        [0  sin(a)  cos(a)]
```
```
Ry(a) = [cos(a)  0   sin(a)]
        [0       1    0    ]
        [-sin(a) 0   cos(a)]
```
```
Rz(a) = [cos(a)  -sin(a)  0]
        [sin(a)  cos(a)   0]
        [0       0        1]
```     
### Matrix to ZYZ Euler angles                                                  
```                                                                             
RZ(a) then RY(b) then RZ(c) = [cos(c)  -sin(c)  0] [cos(b)  0   sin(b)]  [cos(a)  -sin(a)  0] 
                              [sin(c)  cos(c)   0] [0       1    0    ]  [sin(a)  cos(a)   0] 
                              [0       0        1] [-sin(b) 0   cos(b)]  [0       0        1] 
```                                                   
```
[cos(b)  0   sin(b)]  [cos(a)  -sin(a)  0]   [cos(b)cos(a) -cos(b)sin(a) sin(b)]
[0       1    0    ]  [sin(a)  cos(a)   0] = [sin(a)       cos(a)        0     ]
[-sin(b) 0   cos(b)]  [0       0        1]   [-sin(b)cos(a) sin(b)sin(a) cos(b)]

```                          

```
[cos(c)  -sin(c)  0] [cos(b)cos(a) -cos(b)sin(a) sin(b)]    [cos(c)cos(b)cos(a)-sin(b)sin(a)    -cos(c)cos(b)sin(a)-sin(c)cos(a) cos(c)sin(b)]
[sin(c)  cos(c)   0] [sin(a)       cos(a)        0     ]  = [sin(c)cos(b)cos(a)+cos(c)sin(a)    -sin(c)cos(b)sin(a)+cos(c)cos(a) sin(c)sin(b)]
[0       0        1] [-sin(b)cos(a) sin(b)sin(a) cos(b)]    [-sin(b)cos(a)                      sin(b)sin(a)                     cos(b)      ]
``` 

```
R(3,3) = cos(b)
b1 = cos-1(b)
b2 = b1 = pi
```    

```
R(2,3) / R(1,3) = sin(c) / cos(c) = tan(c)
c = atan2(R(2,3), R(1,3))
```

```
R(3,2) / R(3,1) = sin(a)/ -cos(a) = -tan(a)
a = atan2(R(3,2), -R(3,1))
```

### Matrix to ZXZ Euler angles
```
RZ(a) then RX(b) then RZ(c) = [cos(c)  -sin(c)  0] [1     0      0   ] [cos(a)  -sin(a)  0]    
                              [sin(c)  cos(c)   0] [0  cos(b) -sin(b)] [sin(a)  cos(a)   0]    
                              [0       0        1] [0  sin(b)  cos(b)] [0       0        1]   
```  

```
[1     0      0   ] [cos(a)  -sin(a)  0]      [cos(a)             -sin(a)       0 ]
[0  cos(b) -sin(b)] [sin(a)  cos(a)   0]   =  [cos(b)sin(a)  cos(b)cos(a)  -sin(b)]
[0  sin(b)  cos(b)] [0       0        1]      [sin(b)sin(a)  sin(b)cos(a)   cos(b)]
[cos(c)  -sin(c)  0] [cos(a)             -sin(a)       0 ]    [cos(c)cos(a)-sin(c)cos(b)sin(a)  -cos(c)sin(a)-sin(c)cos(b)cos(a)    sin(c)sin(b) ]
[sin(c)  cos(c)   0] [cos(b)sin(a)  cos(b)cos(a)  -sin(b)] =  [sin(c)cos(a)+cos(c)cos(b)sin(a)  -sin(c)sin(a)-cos(c)cos(b)cos(a)    -cos(c)sin(b)]
[0       0        1] [sin(b)sin(a)  sin(b)cos(a)   cos(b)]    [sin(b)sin(a)                     sin(b)cos(a)                        cos(b)       ]  
```  

```
R(3,3) = cos(b)
b1 = cos-1(R(3,3))
b2 = b1 - pi 
``` 

```
R(3,1) / R(3,2) = sin(a)/cos(a) = tan(a)
a = atan2(R(3,1),R(3,2))
```
where atan2(y,x) is arc tangent of the two variablesxandy. It is similar tocalculating the arc tangent ofy/x, 
except that the signs of both arguments areused to determine the quadrant of the result, which lies in the range [−π,π]
One must be careful in interpreting Equation 2. If cos(θ)>0, thenψ=atan2(R32,R33). 
However, when cos(θ)<0,ψ= atan2(−R32,−R33). A simpleway to handle this is to use the equation

```
R(1,3) / R(2,3) = -sin(c)/cos(c) = -tan(c)
c = atan2(-R(1,3), R(2,3))
```