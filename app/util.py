"""
This module contains helper functions 
"""

import random 
import string 
  
def random_id(initial='i', size=8, chars=string.ascii_uppercase + string.digits): 
    """
    Generate a random string with an initial, mainly used to generate ids

    Args:
        initial (str, optional): first letter of the generated id. Defaults to 'i'.
        size (int, optional): Defaults to 8.
        chars ([type], optional): characters set to be used in generating the id. 
        Defaults to string.ascii_uppercase+string.digits.

    Returns:
        [str]: the generated id
    """
    return initial + ''.join(random.choice(chars) for _ in range(size)) 
