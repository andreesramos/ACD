def mayor(num1, num2):
    if num1>num2:
        return num1;
    else:
        return num2;

num1 = int(input("Introduce un numero: "));
num2 = int(input("Introduce otro: "));

print("El mayor numero es ", mayor(num1, num2));
