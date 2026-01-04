def is_even(num):
    
    """ 
    finds odd or even
    """
    if num == 0:
        return -1
    if num % 2 ==0:
        print(f"This number {num} is even")
    else:
        print(f"This number {num} is odd")
        
    
if __name__ == "__main__":
    is_even(0)