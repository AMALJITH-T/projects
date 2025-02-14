function convert() {
    var value = parseFloat(document.getElementById("value").value);
    var conversion = parseInt(document.getElementById("conversion").value);
    var resultElement = document.getElementById("result");
    var result = 0;

    switch (conversion) {
        case 1:
            result = value * 0.3048;
            resultElement.innerHTML = value + " Feet is " + result.toFixed(2) + " Meters";
            break;
        case 2:
            result = value * 3.28084;
            resultElement.innerHTML = value + " Meters is " + result.toFixed(2) + " Feet";
            break;
        case 3:
            result = value * 0.453592;
            resultElement.innerHTML = value + " Pounds is " + result.toFixed(2) + " Kilograms";
            break;
        case 4:
            result = value * 2.20462;
            resultElement.innerHTML = value + " Kilograms is " + result.toFixed(2) + " Pounds";
            break;
        case 5:
            result = value * 60000;
            resultElement.innerHTML = value + "Minutes is" + result.toFixed(2) + "Milliseconds";
        default:
            resultElement.innerHTML = "Invalid choice";
    }
}