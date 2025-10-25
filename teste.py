
from decimal import Decimal, getcontext
n1 = 0.2
n2 = 0.5

print(n1 + n2) 
print(f"{n1 + n2:.28f}") 


getcontext().prec = 28  
d1 = Decimal('0.2')
d2 = Decimal('0.5')
print(d1 + d2) 
print(f"{d1 + d2:.50f}")  
