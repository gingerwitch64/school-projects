var localRoot = window.location.href
console.log(localRoot)
var mainList = document.getElementById("todoli")
if (localStorage.getItem("autosave") === null) {localStorage.setItem("autosave","On")}
document.getElementById("autosave_button").value = "Autosave: ".concat(localStorage.getItem("autosave"))
console.log(document.getElementById("autosave_button").value)

window.addEventListener("load", function(e){
    document.getElementById("new_item_name").setAttribute('size',document.getElementById("new_item_name").getAttribute('placeholder').length);
    loadList()
})
    
function appendItem() {
    // Create node
    var node = document.createElement("li");
    var textnode = document.createTextNode(
        document.getElementById("new_item_name").value
    );
    node.appendChild(textnode);
    node.addEventListener("dblclick",markItem);
    mainList.appendChild(node);
    determineAutosave()
}
    
function markItem() {
    if (this.classList.contains("completed")) {
        this.classList.remove("completed")
    } else {
        this.classList.add("completed")
    }
    determineAutosave()
}

function clearCompleted() {
    var compItems = mainList.getElementsByClassName("completed")
    while (compItems.length > 0) {
        compItems.item(0).remove()
    }
    determineAutosave()
}

function saveList() {
    var exportItems = []; // JSON Object
    var domItems = mainList.children
    for (var i = 0; i < domItems.length; i++) {
        let currentItem = domItems.item(i)
        exportItems.push({"text":currentItem.innerText,"completed":currentItem.classList.contains("completed")})
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
        let textnode = document.createTextNode(currentItem.text);
        node.appendChild(textnode);
        node.addEventListener("dblclick",markItem);
        if (currentItem.completed) {
            node.classList.add("completed")
        }
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