#include <stdio.h>
#include <math.h>
int main() {
    int choice;
    double temperature, convertedTemperature;

    printf("Temperature Converter\n");
    printf("1. Fahrenheit to Celsius\n");
    printf("2. Celsius to Fahrenheit\n");
    printf("Enter your choice (1/2): ");
    scanf("%d", &choice);

    if (choice == 1) {
        printf("Enter temperature in Fahrenheit: ");
        scanf("%lf", &temperature);
        convertedTemperature = (temperature - 32) * 5.0 / 9.0;
        printf("Temperature in Celsius: %.2lf\n", convertedTemperature);
    } else if (choice == 2) {
        printf("Enter temperature in Celsius: ");
        scanf("%lf", &temperature);
        convertedTemperature = (temperature * 9.0 / 5.0) + 32;
        printf("Temperature in Fahrenheit: %.2lf\n", convertedTemperature);
    } else {
        printf("Invalid choice. Please enter 1 or 2.\n");
    }

    return 0;
}
