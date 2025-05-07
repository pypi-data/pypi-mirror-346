def calculate_area():
    print("1. Square")
    print("2. Rectangle")
    choice = input("Enter your choice (1/2): ")

    if choice == "1":
        side = float(input("Enter side length of square: "))
        area = side ** 2
        print(f"Area of square: {area}")
    elif choice == "2":
        length = float(input("Enter length of rectangle: "))
        width = float(input("Enter width of rectangle: "))
        area = length * width
        print(f"Area of rectangle: {area}")
    else:
        print("Invalid choice")

calculate_area()