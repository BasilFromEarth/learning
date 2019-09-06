# Paste your code into this box
check = 'h'
low = 0
high = 100
print("Please think of a number between 0 and 100!")

while check != 'c':
    ans = int((low+high)/2)
    print("Is your secret number", ans,end='' "?")
    check = input("Enter 'h' to indicate the guess is too high. Enter 'l' to indicate the guess is too low. Enter 'c' to indicate I guessed correctly. ")
    if check == 'h':
        low = ans
    elif check == 'l':
        high = ans
    elif check == 'c':
        break
    else:
        print("Sorry, I did not understand your input.")
print("Game over. Your secret number was:", ans)     
      