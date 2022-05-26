'''
Descripttion: 
version: 
Author: Martin
FilePath: \Martin_Code\Python\密码学\DH_RSA.py
Date: 2022-05-18 19:26:48
LastEditTime: 2022-05-26 12:19:05
'''

from math import gcd
from Crypto.Util.number import bytes_to_long
import random
import sys
import Getprime

with open(r'E:\Martin_Code\Python\密码学\DH_RSA.txt','w') as fp:
    p=Getprime.getprime(3)
    #print(p)
    g=Getprime.getroot(p)

    class Alice:
        
        def __init__(self) -> None:
            self.p = Getprime.getprime(32)
            self.q = Getprime.getprime(32)
            self.n = self.q*self.p
            self.fn = (self.q-1)*(self.p-1)
            self.e = self.get_e()
            self.d,_,_ = self.get_d(self.e,self.fn)
            if self.d<0: 
                self.d +=self.fn

        # 获取ID
        def send_id(self):
            self.id = 'alice'
            fp.write('alice发起了请求,并表明了自己的身份\n')
            return self.id

        # 发送数据,返回A的 n,e,y,sign_id
        def send_data(self):
            self.alice_x = random.randint(1,35)
            self.alice_y = Getprime.Fast_Mod(g,self.alice_x,p)
            self.sign_e = Getprime.Fast_Mod(self.e,self.d,self.n)
            #对alice签名
            self.long_id = bytes_to_long('alice'.encode('utf-8'))
            self.sign_id = Getprime.Fast_Mod(self.long_id,self.d,self.n)
            fp.write('Alice产生了n={},公钥e={},随机数alice_x={},并将e,n,alice_y={},签名s={},签名后的e={}发送给bob\n'.format(self.n,self.e,self.alice_x,self.alice_y,self.sign_id,self.sign_e))
            return self.n,self.e,self.alice_y,self.sign_id,self.sign_e
            
        # 获取私钥d，
        def get_d(self,a,b):
        #扩展欧几里得算法     
            if b == 0:          
                return 1, 0, a     
            else:         
                x, y, gcd = self.get_d(b, a % b) #递归直至余数等于0(需多递归一层用来判断)        
                x, y = y, (x - (a // b) * y) #辗转相除法反向推导每层a、b的因子使得gcd(a,b)=ax+by成立         
                return x, y, gcd
        
        # 获取公钥e
        def get_e(self):
            e = 10
            while True:
                if gcd(e,self.fn)==1:
                    return e
                else:
                    e=e+1                
        
        # 验证对面的身份
        def verify(self,b_n,b_e,b_sign_id,bob_id,b_sign_e):
            bob_long_id = bytes_to_long(bob_id.encode('utf-8'))
            # 对面的公钥解密
            bob_ver_id = Getprime.Fast_Mod(b_sign_id,b_e,b_n)
            bob_ver_e = Getprime.Fast_Mod(b_sign_e,b_e,b_n)
            #print(b_e)
            #print(b_sign_e)
            #print(bob_ver_e)
            #print(bob_ver_id)
            #print(bob_long_id%b_n)
            if bob_ver_id == (bob_long_id%b_n):
                if (bob_ver_e%b_n) == (b_e%b_n):
                    return True
                else:
                    return False
            else:
                return False
        
        # 计算互相约定的K
        def get_k(self,b_y):
            self.k = (b_y**self.alice_x)%p
            fp.write('alice计算出的K={}\n'.format(self.k)) 
    
    class Bob:
        
        def __init__(self) -> None:
            self.p = Getprime.getprime(32)
            self.q = Getprime.getprime(32)
            self.n = self.q*self.p
            self.fn = (self.q-1)*(self.p-1)
            self.e = self.get_e()
            self.d,_,_ = self.get_d(self.e,self.fn)
            if self.d<0: 
                self.d +=self.fn

        # 获取ID
        def send_id(self):
            self.id = 'bob'
            fp.write('bob回应了请求,并表明了自己的身份\n')
            return self.id
        
        # 发送数据,返回B的 n,e,y,sign_id
        def send_data(self):
            self.bob_x = random.randint(1,35)
            self.bob_y = Getprime.Fast_Mod(g,self.bob_x,p)
            self.sign_e = Getprime.Fast_Mod(self.e,self.d,self.n)
            #对bob签名
            self.long_id = bytes_to_long('bob'.encode('utf-8'))
            self.sign_id = Getprime.Fast_Mod(self.long_id,self.d,self.n)
            #print(self.sign_e)
            #print('a',self.e)
            fp.write('Bob产生了n={},公钥e={},随机数bob_x={},并将e,n,bob_y={},签名s={},签名后的e={}发送给bob\n'.format(self.n,self.e,self.bob_x,self.bob_y,self.sign_id,self.sign_e))
            return self.n,self.e,self.bob_y,self.sign_id,self.sign_e
        
        # 获取私钥d
        def get_d(self,a,b):
        #扩展欧几里得算法     
            if b == 0:          
                return 1, 0, a     
            else:         
                x, y, gcd = self.get_d(b, a % b) #递归直至余数等于0(需多递归一层用来判断)        
                x, y = y, (x - (a // b) * y) #辗转相除法反向推导每层a、b的因子使得gcd(a,b)=ax+by成立         
                return x, y, gcd
        
        # 获取公钥e
        def get_e(self):
            e = 10
            while True:
                if gcd(e,self.fn)==1:
                    return e
                else:
                    e=e+1  
        
        # 验证对面的身份
        def verify(self,a_n,a_e,a_sign_id,alice_id,a_sign_e):
            alice_long_id = bytes_to_long(alice_id.encode('utf-8'))
            # 对面的公钥解密
            alice_ver_id = Getprime.Fast_Mod(a_sign_id,a_e,a_n)
            alice_ver_e = Getprime.Fast_Mod(a_sign_e,a_e,a_n)
            # print(a_e)
            # print(alice_ver_e)
            #print(alice_long_id%a_n)
            if alice_ver_id == (alice_long_id%a_n):
                if (alice_ver_e%a_n) == (a_e%a_n):
                    return True
                else:
                    return False
            else:
                return False

        # 计算互相约定的K
        def get_k(self,a_y):
            self.k = (a_y**self.bob_x)%p
            fp.write('bob计算出的K={}\n'.format(self.k)) 

    def main():
        fp.write('DH-RSA\n')
        
        # 双方请求相应
        alice = Alice()
        alice_id = alice.send_id()
        bob = Bob()
        bob_id = bob.send_id()
        fp.write('双方约定了大素数p={},本原根g={}\n'.format(p,g))

        # 双发互发n,d,y,sign_id，sign_e
        a_n,a_e,a_y,a_sign_id,a_sign_e = alice.send_data()
        b_n,b_e,b_y,b_sign_id,b_sign_e = bob.send_data()

        # 双方互相验证身份,失败则退出
        if alice.verify(b_n,b_e,b_sign_id,bob_id,b_sign_e) == False:
            print('alice验证bob身份失败')
            sys.exit()
        if bob.verify(a_n,a_e,a_sign_id,alice_id,a_sign_e) == False:
            print('bob验证alice身份失败')
            sys.exit()

        # 互相计算约定的K
        alice.get_k(b_y)
        bob.get_k(a_y)
        print('ok')

    if  __name__ == '__main__':
        main()