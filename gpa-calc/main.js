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

function clearList() {
    var domItems = mainList.children
    while (domItems.length > 0) {
        domItems.item(0).remove()
    }
    determineAutosave()
}

function calcGPA() {
    var domItems = mainList.children
    classes = domItems.length
    var preTotal = 0.0
    for (var i = 0; i < domItems.length; i++) {
        let currentClasses = domItems.item(i).classList
        if (currentClasses.item(0) != "f") {
            switch (currentClasses.item(0)) {
                case "a": preTotal += 4; break;
                case "a-minus": preTotal += 3.7; break;
                case "b-plus": preTotal += 3.3; break;
                case "b": preTotal += 3; break;
                case "b-minus": preTotal += 2.7; break;
                case "c-plus": preTotal += 2.3; break;
                case "c": preTotal += 2; break;
                case "c-minus": preTotal += 1.7; break;
                case "d-plus": preTotal += 1.3; break;
                case "d": preTotal += 1; break;
            }
            switch (currentClasses.item(1)) {
                case "honors": preTotal += 0.5; break;
                case "college": preTotal += 1; break;
            }
        }
    }
    var gpa = (preTotal/classes).toFixed(2)
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
    clearList()
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