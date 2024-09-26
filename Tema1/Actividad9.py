def area(lado1, lado2):
    res = lado1 * lado2;
    return res;

num1 = int(input("Introduce un lado del rectangulo: "));
num2 = int(input("Introduce el otro lado: "));

print("El area del rectangulo es de ", area(num1, num2))
