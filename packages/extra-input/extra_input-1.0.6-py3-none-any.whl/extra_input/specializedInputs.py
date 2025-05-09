def intput(text:str) -> int:
    """Gets input only allowing ints"""
    while True:
        response = input(text)
        try:
            return int(response)
        except ValueError:
            print("Please enter a valid int, try again.")
        except OverflowError:
            print("Please enter a smaller int, try again.")

def float_input(text:str) -> float:
    """Gets input only allowing floats"""
    while True:
        response = input(text)
        try:
            return float(response)
        except ValueError:
            print("Please enter a valid float, try again.")
        except OverflowError:
            print("Please enter a smaller float, try again.")

def custom_input(text:str, allowed:str, tellAllowed = True) -> str:
    """Gets input only allowing certain charecters"""
    while True:
        response = input(text)
        good = True
        for char in response:
            if char not in allowed:
                if tellAllowed:
                    print(f"Please enter text with only valid charecters:\n{allowed}")
                else:
                    print("Please enter text with only valid charecters.")
                good = False
                break
        if good:
            return response