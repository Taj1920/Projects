import sqlite3
import random 
conn=sqlite3.connect('dom.db')
b=conn.cursor()
# b.execute('create table Domuser(name char,phno number,email char)')
# b.execute('create table cart(phno number,cartvalues char)')

class Dom:
    d={
        'veg':{'Margerita':129,'cheese_and_corn':169,'peppi_paneer':260,
               'veg_loaded':210,'tomato_tangi':170},
        'non_veg':{'pepper_barbeque':199,'non_veg_loaded':169,'chicken_sausage':200},
        'snacks':{'garlic_bread':120,'zingy':59,'cheese_balls':170,'french_fries':110},
        'desserts':{'choco_lava':100,'mousse_cake':169},
        'drinks':{'coke':90,'pepsi':78,'sprite':50}
    }

    def valid_phno(self,phno):
        s=str(phno)
        return len(s)==10 and '6'<=s[0]<='9' and s.isnumeric()
    
    def check_phno(self,phno):
        l=list(b.execute('select phno from Domuser'))
        return (phno,) in l
    def check_email(self,email):
        l=list(b.execute('select email from Domuser'))
        return (email,) in l
    
    def valid_email(self,e):
        return e.count("@")==1 and e.count('.')==1 and \
            e[-10:] in ['@gmail.com','@yahoo.com'] and 'a'<=e[0]<='z'
    
    def __init__(self):
        self.login_status=False
        self.cart={}
        self.mode=0
        self.pnum=0
        while True:
            print('--------WELCOME TO DOMINOS----------')
            print('Enter 1: signup')
            print('Enter 2: Login')
            print('Enter 3: Logout')
            print('Enter 4: order')
            print('Enter 5: Display bill')
            print('Enter 6: Exit')
            ch=int(input('Enter your choice: '))
            if ch==1:
                name=input('Enter name: ')
                while True:
                    phno=int(input('Enter phno: '))
                    if self.valid_phno(phno):
                        break
                    else:
                        print('Enter valid phno')

                while True:
                    email=input('Enter email: ')
                    if self.valid_email(email):
                        break
                    else:
                        print('Enter valid email')
                m,n=self.check_phno(phno),self.check_email(email)
                if m==False and n==False:
                    b.execute(f'insert into Domuser values("{name}","{phno}","{email}")')
                    conn.commit()
                    print('signup successfull')
                    self.name=name
                    self.phno=phno
                    self.email=email
                elif m==True:
                    print('Phno is already Exists')
                elif n==True:
                    print('Email already Exists')
            elif ch==2:
                self.login()
            elif ch==3:
                self.logout()
            elif ch==4:
                self.order()
            elif ch==5:
                self.disp_bill()
            elif ch==6:
                break
            a=input('Do you want to continue (y/n): ')
            if a.lower()=='y':
                continue
            else:
                print('Thank you!!!!')
                break

    def get_otp(self,a):
        while True:
            otp=random.randint(100000,999999)
            print('OTP to login is: ',otp)
            print('An otp has been sent to your ',a)
            tp=int(input('Enter OTP: '))
            if otp==tp:
                print('Logged in Successfully')
                self.login_status=True
                break
            else:
                print('Enter correct otp')

    def login(self):
        if self.login_status==True:
            print('you are already logged in')
        print('Enter 1: Login with Phno')
        print('Enter 2: Login with email')
        c=int(input('Enter your Login choice:'))
        if c==1:
            self.pnum=int(input('Enter phno: '))
            if self.check_phno(self.pnum):
                self.get_otp(self.pnum)
            else:
                print('Phone num doesnot Exists')
        elif c==2:
            email=input('Enter email: ')
            self.pnum=list(b.execute(f'select phno from Domuser where email="{email}"'))[0][0]
            if self.check_email(email):
                self.get_otp(email)
            else:
                print('Email doesnot Exists')
    def logout(self):
        self.login_status=False
        print('Logged out successfully')

    def order(self):
        if self.login_status==True:
            print('Enter 1: Dine in')
            print('Enter 2: Take away')
            print('Enter 3: Home Delivery')
            cho=int(input('Enter type of choice: '))
            self.mode=cho
            out={}
            print('Please go through the menu')
            di=list(self.d)
            while True:
                print('Enter 1: veg')
                print('Enter 2: non_veg')
                print('Enter 3: snacks')
                print('Enter 4: Desserts')
                print('Enter 5: Drinks')
                print('Enter 6: End')
                ch=int(input('Enter item choice: '))
                if 1<=ch<=6:
                    if ch==6:
                        break
                    m=list(self.d)[ch-1]
                    n=list(self.d[m])
                    for i in range(1,len(n)+1):
                        print(f'Enter {i}:  {n[i-1]}')
                    c=int(input('Enter choice: '))
                    q=int(input('Enter quantity: '))
                    if 1<=c<=len(n):
                        out[n[c-1]]=[q,q*self.d[di[ch-1]][n[c-1]]]
                        print('Item added')
                    else:
                        print('Invalid choice')
                else:
                    print('Invalid choice')
            self.cart.update(out)
            if self.cart!={}:
                b.execute(f'insert into cart values("{self.pnum}","{self.cart}")')
        else:
            print('Login is required')
            self.login()
    
    def disp_bill(self):
        if self.login_status==True:
            if self.mode==1:
                total_amt=0
            elif self.mode==2:
                print('parcel charges of 25 Rs. will be included')
                total_amt=25
            elif self.mode==3:
                print('parcel charges of 25 Rs. and delivery charges of 50Rs.\
                    will be included')
                total_amt=75
            print('item',' '*11,'quantity','       price')
            print(self.cart)
            for i in self.cart:
                print(i,' '*11,self.cart[i][0],self.cart[i][1])
                total_amt+=self.cart[i][1]
            
            print('Total bill',' '*11,total_amt)
        else:
            print('login is required')
        
                
ob=Dom()