import random 
import string 
  
# defining function for random 
# string id with parameter 
def random_id(size=8, chars=string.ascii_uppercase + string.digits): 
    return ''.join(random.choice(chars) for x in range(size)) 
