function showHide(className) {
    let elements = document.getElementsByClassName(className);
    for (let i = 0; i < elements.length; i++) {
        let element = elements[i];
        const style = element.style;
        if (style.display == "none") {
            style.display = "";
        }
        else {
            style.display = "none";
        }
    }
}