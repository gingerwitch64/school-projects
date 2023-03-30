var localRoot = window.location.href
console.log(localRoot)
var mainList = document.getElementById("mainlist")
if (localStorage.getItem("autosave") === null) {localStorage.setItem("autosave","On")}
document.getElementById("autosave_button").value = "Autosave: ".concat(localStorage.getItem("autosave"))
console.log(document.getElementById("autosave_button").value)

window.addEventListener("load", function(e){loadList()})
    
function appendItem() {
    // Create node
    var node = document.createElement("li");
    node.classList.add(document.getElementById("grade-sel").value,document.getElementById("credit-sel").value)
    node.addEventListener("dblclick",removeMe);
    mainList.appendChild(node);
    determineAutosave()
}

function removeMe() {
    this.remove()
    determineAutosave()
}

function calcGPA() {
    var domItems = mainList.children
    classes = domItems.length
    preTotal = 0.0
    for (var i = 0; i < domItems.length; i++) {
        let currentClasses = domItems.item(i).classList
        if (currentClasses.item(0) != "f") {
            switch (currentClasses.item(0)) {
                case "a": preTotal += 4.0
                case "a-minus": preTotal += 3.7
                case "b-plus": preTotal += 3.3
                case "b": preTotal += 3.0
                case "b-minus": preTotal += 2.7
                case "c-plus": preTotal += 2.3
                case "c": preTotal += 2.0
                case "c-minus": preTotal += 1.7
                case "d-plus": preTotal += 1.3
                case "d": preTotal += 1.0
            }
            switch (currentClasses.item(1)) {
                case "honors": preTotal += 0.5
                case "college": preTotal += 1.0
            }
        }
    }
    gpa = preTotal/classes
    console.log(gpa)
    Math.round((gpa + Number.EPSILON) * 100) / 100
    console.log(gpa)
    document.getElementById("gpa").innerHTML = gpa
}

function saveList() {
    var exportItems = []; // JSON Object
    var domItems = mainList.children
    for (var i = 0; i < domItems.length; i++) {
        let currentItem = domItems.item(i)
        exportItems.push({"grade":currentItem.classList.item(0),"credit":currentItem.classList.item(1)})
    }
    localStorage.setItem("savedList",JSON.stringify(exportItems))
}

function loadList() {
    var domItems = mainList.children
    while (domItems.length > 0) {
        domItems.item(0).remove()
    }
    var importItems = JSON.parse(localStorage.getItem("savedList"))
    for (var i = 0; i < importItems.length; i++) {
        let currentItem = importItems[i]
        let node = document.createElement("li");
        node.addEventListener("dblclick",removeMe);
        node.classList.add(currentItem.grade,currentItem.credit)
        mainList.appendChild(node);
    }
    determineAutosave()
}

function determineAutosave() {
    if (localStorage.getItem("autosave") == "On") {saveList()}
}

function autosaveToggle() {
    autosavelocalstatus = localStorage.getItem("autosave")
    if (autosavelocalstatus == "On") {
        localStorage.setItem("autosave", "Off")
    } else {
        localStorage.setItem("autosave", "On")
    }
    document.getElementById("autosave_button").value = "Autosave: ".concat(localStorage.getItem("autosave"))
}