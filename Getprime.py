'''
Descripttion: 
version: 
Author: Martin
FilePath: \Martin_Code\Python\密码学\getprime.py
Date: 2022-05-26 09:27:59
LastEditTime: 2022-05-26 10:36:20
'''
import math
from os import urandom          #系统随机的字符
import binascii         #二进制和ASCII之间转换

# 快速幂运算
def Fast_Mod(a,p,m):
        '''快速取模指数算法:计算 (a ^ p) % m 的值'''
        a,p,m=int(a),int(p),int(m)
        if (p == 0) :
                return 1
        r = a % m
        k = 1
        while (p > 1):
                if ((p & 1)!=0):
                        k = (k * r) % m
                r = (r * r) % m
                p >>= 1
        return (r * k) % m

# 获取随机数
def randint(n):
        """生成n字节的随机数（8位/字节）,返回16进制转为10进制整数返回"""
  
        randomdata = urandom(n)
        return int(binascii.hexlify(randomdata),16)    

# 小素数检验
def primality_testing_1(n):
        '''测试一，小素数测试，用100以内的小素数检测随机数x,
可以很大概率排除不是素数,#创建有25个素数的元组'''
        Sushubiao=(2,3,5,7,11,13,17,19,23,29,31,37,41
                   ,43,47,53,59,61,67,71,73,79,83,89,97)
        for y in Sushubiao:
                if n%y==0:
                        return False
        return True

# 大素数检验，rabin
def primality_testing_2(n, k):
        '''测试二,用miller_rabin算法对n进行k次检测'''
        if n < 2:
                return False
        d = n - 1
        r = 0
        while not (d & 1):
                r += 1
                d >>= 1
        for _ in range(k):
                a = randint(120)        #随机数
                x = pow(a, d, n)
                if x == 1 or x == n - 1:
                        continue
                for _ in range(r - 1):
                        x = pow(x, 2, n)
                if x == 1:
                        return False
                if x == n - 1:
                        break
        else:
                return False
        return True    

# 返回大素数
def getprime(byte):
        while True :
                n=randint(byte)    
                if primality_testing_1(n) :
                        if primality_testing_2(n, 10) :
                                pass
                        else :continue
                else : continue 
                return n

# 求因子返回因数列表
def factor(euler):
    ls=[]
    for i in range (2,int(math.sqrt(euler)+1)):
        if primality_testing_1(i):
                if primality_testing_2(i,10):
                        while euler%i==0:
                                ls.append(i)
                                euler/=i
    return list(set(ls))

# 求本原根
def getroot(p):
    a=2
    i=1
    euler=p-1
    factors=factor(euler)
    while a<p:
        flag=1
        for k in factors:
            n=int(euler/k)
            if Fast_Mod(a,n,p)==1:
                flag=0
                break
        if flag==1:
            return a
        a+=1



