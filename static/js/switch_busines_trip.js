function checkFluency1() {
    let checkbox = document.getElementById('inputBusinessTrip');
    if(checkbox.checked!==true) {
        checkbox.value = `{{ False }}`
    } else {
        checkbox.value = `{{ True }}`
    }
}

function checkFluency2() {
    let checkbox = document.getElementById('inputBusinessTrip2');
    if(checkbox.checked!==true) {
        checkbox.value = `{{ False }}`
    } else {
        checkbox.value = `{{ True }}`
    }
}