print("Welcome to Unity")
# The developer named me as Unity, a tool to convert all the units
# Note: I am still developing
print("\nLet's Go")
print("Type\n1 for Meter to Kilometer\n2 for Gram to Kilogram\n3 for Milliliters to Liters\n4 for Fahrenheit to Celsius\n5 for Minutes to Seconds\n6 for Joule to Kilojoule")

choice = int(input("Enter your choice: "))

if choice == 1:
    print("You have selected to convert Meter to Kilometer")
    m = float(input("Enter value in meter: "))
    km = m / 1000  # equation to convert meter to kilometer
    print(f"Kilometer= {km:.2f}")
elif choice == 2:
    print("You have selected to convert Gram to Kilogram")
    g = float(input("Enter the value in gram: "))
    kg = g / 1000  # equation for converting gram to kilogram
    print(f"Kilogram= {kg:.2f}")
elif choice == 3:
    print("You have selected to convert Milliliters to Liters")
    ml = float(input("Enter the value in milliliters: "))
    L = ml / 1000  # equation for converting milliliters to liters
    print(f"Liters= {L:.2f}")
elif choice == 4:
    print("You have selected to Convert Fahrenheit to Celsius")
    F = float(input("Enter the value in Fahrenheit: "))
    C = (F - 32) * 5 / 9  # equation for converting Fahrenheit to Celsius
    print(f"Celsius= {C:.2f}")
elif choice == 5:
    print("You have selected to convert Minutes to Seconds")
    min = float(input("Enter the value in Minutes: "))
    sec = min * 60  # equation for converting minutes to seconds
    print(f"Seconds= {sec:.2f}")
elif choice == 6:
    print("You have selected to convert Joule to Kilojoule")
    j = float(input("Enter the value in joule: "))
    kj = j / 1000  # equation for converting joule to kilojoule
    print(f"Kilojoule= {kj:.2f}")
else:
    print("Sorry, the selected choice is not available because I am still developing")
