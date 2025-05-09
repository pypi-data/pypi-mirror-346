import roman

def select(options:list[str], squareBrackets = True) -> str:
    """Select from a list of options.
    When using first letter selctions please specify your own square brackets"""
    #check for duplicates
    if list(set(options)) != options:
        print("Invalid options, no duplicates")
    while True:
        print("Please choose a option:")
        for option in options:
            print(option)
        response = input(">>> ").lower()
        if squareBrackets:
            for option in options:
                curr = option[option.index('[')+1]
                for i in range(option.index('[')+2,len(option)):
                    if option[i] == "]":
                        break
                    curr += option[i]
                if response == curr.lower():
                    return curr.lower()
        else:
            for option in options:
                if response == option.lower():
                    return option
        print("Invalid option, please try again.")

def numbered_select(options:list[str], use_parens = False, roman_numerals = False) -> str:
    while True:
        print("Please choose a option:")
        for index, option in enumerate(options):
            if roman_numerals:
                if use_parens:
                    print(f"{roman.toRoman(index+1)}) {option}")
                else:
                    print(f"{roman.toRoman(index+1)}. {option}")
            else:
                if use_parens:
                    print(f"{index+1}) {option}")
                else:
                    print(f"{index+1}. {option}")
        response = input(">>> ").lower()
        if roman_numerals:
            for index, option in enumerate(options):
                if response == roman.toRoman(index+1).lower():
                    return option
        else:
            for index, option in enumerate(options):
                if response == str(index+1):
                    return option
        print("Invalid option, please try again.")

if __name__ == "__main__":
    print(select(["[R]ectangle","Rectangular [P]rism"]))