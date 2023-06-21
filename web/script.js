// Get the element with id="defaultOpen" and click on it
document.getElementById("startOpen").click();

// show the loader
function showLoader() {
    document.getElementById("loader1").style.display = "block";
    console.log("showing loader")
    document.getElementById("results").style.display = "none";
}

// hide the loader
function hideLoader() {
    document.getElementById("loader1").style.display = "none";
    document.getElementById("results").style.display = "block";
}

function scrape_papers() {
    document.getElementById("defaultOpen").click();
    showLoader();
    // Get keyword input
    var inputElement = document.getElementById("keywordInput");
    var userInput = inputElement.value;
    // Get pages input
    var inputElement = document.getElementById("pagesInput");
    var pagesInput = inputElement.value;
    eel.scrape_papers(userInput, pagesInput)();
    load_csv(function () {
        hideLoader();
    });

}

// Function to initialize DataTables
function initializeDataTables() {
    $('#myTable').DataTable();
}

function LoadReadPapers() {

    eel.load_reading_list_csv("read_papers.csv", "readTable", "myreadTable")(function (content) {

        //load_reading_list_csv returns an array of html tables
        var tables = content;
        //console.log(tables)
        var parser = new DOMParser();

        for (i = 0; i < tables.length; i++) {

            console.log(i)
            // Get the class of the table
            //console.log(tables[i])
            var doc = parser.parseFromString(tables[i], 'text/html');
            var element = doc.querySelector('table');
            var GroupName = Array.from(element.classList);
            console.log(GroupName)



            // Clear the previous table in the corresponding collapsible

            var collapsible = document.querySelector("div." + String(GroupName[2]));
            if (collapsible == null) {
                // if the container doesnt exist yet, create it
                createGroup(GroupName[2], true);
                console.log("ma bite")
            }

            var collapsible = document.querySelector("div." + String(GroupName[2]));
            var contentContainer = collapsible.lastElementChild;
            // console.log(collapsible)
            contentContainer.innerHTML = "";

            // Update the table
            contentContainer.innerHTML = tables[i];

            //Add checkboxes specify which myreadTable is used
            var table = collapsible.getElementsByClassName("readTable")[0];
            var tbody = table.getElementsByTagName("tbody")[0];
            var rows = tbody.getElementsByTagName("tr");
            console.log("a")
            // Add checkboxes to each row
            for (var j = 0; j < rows.length; j++) {
                // Create a new cell for the checkbox
                var cell = document.createElement("td");

                // Create a checkbox element
                var checkbox = document.createElement("input");
                checkbox.type = "checkbox";
                checkbox.id = "myCheckbox";
                checkbox.checked = true;

                // Append the checkbox to the cell
                cell.appendChild(checkbox);

                // Add event handlers
                checkbox.addEventListener("change", handleCheckboxChange);

                // Insert the new cell as the first cell in the row
                rows[j].insertBefore(cell, rows[j].firstChild);
            }
            // Add header for the new column
            var headerRow = table.getElementsByTagName("thead")[0].getElementsByTagName("tr")[0];
            var headerCell = document.createElement("th");
            headerCell.textContent = "Reading";
            headerRow.insertBefore(headerCell, headerRow.firstChild);

            $(table).DataTable();
            console.log("b")
        }

    })
}

function load_csv(callback) {
    eel.load_csv("papers.csv", "table", "myTable")(function (content) {
        // Update the div 
        document.querySelector(".papers").innerHTML = content;

        //Add chckboxes
        var table = document.getElementById("myTable");
        var tbody = table.getElementsByTagName("tbody")[0];
        var rows = tbody.getElementsByTagName("tr");

        // Add checkboxes to each row
        for (var i = 0; i < rows.length; i++) {
            // Create a new cell for the checkbox
            var cell = document.createElement("td");

            // Create a checkbox element
            var checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.id = "myCheckbox";
            // Create the label for the checkbox
            //var label = document.createElement("label");
            //label.textContent = "Toggle Function";
            //label.htmlFor = "myCheckbox";

            // Append the checkbox to the cell
            cell.appendChild(checkbox);
            //cell.appendChild(label);

            // Add event handlers
            checkbox.addEventListener("change", handleCheckboxChange);

            // Insert the new cell as the first cell in the row
            rows[i].insertBefore(cell, rows[i].firstChild);
        }
        // Add header for the new column
        var headerRow = table.getElementsByTagName("thead")[0].getElementsByTagName("tr")[0];
        var headerCell = document.createElement("th");
        headerCell.textContent = "Add to reading list";
        headerRow.insertBefore(headerCell, headerRow.firstChild);
        initializeDataTables();
        callback();
    })
}

function handleCheckboxChange(event) {
    var checkbox = event.target;

    // Get the parent row of the checkbox
    var row = checkbox.parentNode.parentNode;

    // Get the title cell in the same row
    var titleCell = row.getElementsByTagName("td")[1];

    // Get the title text
    var title = titleCell.textContent;

    if (event.target.checked) {
        // Checkbox is checked, call functionA
        AddReadEntry(title);
    } else {
        // Checkbox is unchecked, call functionB
        RemoveReadEntry(title);
        uncheckCheckbox(title)
    }
    //update the table as well after 5 sec
    //function wait(callback) {
    //  setTimeout(callback, 5000); // 5 seconds
    // }
    //wait(function () {
    LoadReadPapers();

    //});


}
function AddReadEntry(title) {
    console.log("Adding read entry");
    // Get keyword input
    var inputElement = document.getElementById("keywordInput");
    var keyword = inputElement.value;
    // Get group name select input
    var group = document.getElementById("GroupNamesSelect");
    var GroupName = group.options[group.selectedIndex].text;
    eel.add_read_entry(keyword, GroupName, title);
}

function RemoveReadEntry(title) {
    console.log("Removing read entry");
    // Get keyword input
    var inputElement = document.getElementById("keywordInput");
    var keyword = inputElement.value;
    eel.remove_read_entry(keyword, title);
}

// Code for the tabs
function openCity(evt, cityName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}

function uncheckCheckbox(elementText) {
    //uncheck checkbox in the results table
    var table = document.getElementById("myTable");
    var rows = table.getElementsByTagName('tr');

    for (var i = 1; i < rows.length; i++) {
        var row = rows[i];
        console.log(row)
        var cells = row.getElementsByTagName('td');
        var checkbox = cells[0].querySelector('input[type="checkbox"]');
        var cellText = cells[1].textContent;
        if (cellText === elementText) {
            checkbox.checked = false;
            break;
        }
    }
    console.log("unchecked entry in results table")
}

// Function to delete parent div
function DeleteParent(element) {
    // Function to be executed when the button is clicked
    console.log('Deleted collapsible');
    var ParentDiv = element.parentNode;
    ParentDiv.remove();
    UpdateGroupSelect();
}


//code for the collapsible

function createGroup(GroupName = null, auto = false) {

    //Create the html
    var collapsibleDiv = document.createElement('div');
    collapsibleDiv.setAttribute("id", "collapsibleDiv");

    //Create the collapsible button
    var collapsibleButton = document.createElement('button');
    collapsibleButton.classList.add('collapsible');
    collapsibleButton.setAttribute("id", "collapsibleButton");
    collapsibleButton.addEventListener("click", function () {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }
    });
    // Create the input
    var input = document.createElement("input");
    input.type = "text";
    input.classList.add('input-field');
    input.placeholder = "Enter Group Name";
    input.addEventListener('input', function () {
        
        RenameClass(this);
        UpdateGroupSelect();
    });
    
    //Create the delete button
    var deleteButton = document.createElement('button');
    deleteButton.classList.add('deleteButton')
    deleteButton.setAttribute("id", "deleteButton")
    deleteButton.innerHTML = '<i class="fa fa-trash-o"></i>';

    // Delete the collapsible div on click
    deleteButton.addEventListener('click', function () {
        // Function to be executed when the button is clicked
        console.log('Deleted collapsible');
        DeleteParent(this);
    });


    //Create the content div
    var content = document.createElement('div');
    content.style.display = 'none';
    content.classList.add('content');

    content.innerHTML = '<div class="readpapers table-container" id="readpapers">';

    //Append to the tab section
    var container = document.getElementById('ReadPapers');
    container.appendChild(collapsibleDiv);
    collapsibleDiv.appendChild(deleteButton);
    collapsibleDiv.appendChild(collapsibleButton);
    collapsibleDiv.appendChild(content);
    collapsibleButton.appendChild(input);

    // to rename the class to the GroupName argument
    if (auto == true) {
        input.value = GroupName
    }
    
    // But we need to trigger an event in order to get the input to load

    // Create a new "input" event
    var inputEvent = new Event("input");

    // Dispatch the event on the input element
    input.dispatchEvent(inputEvent);


    //Manage the backend

}

function RenameClass(element) {
    //rename the collapsible class
    var newClassName = element.value;
    newClassName = newClassName.replace(/\s/g, "-");
    button = element.parentNode;
    div = button.parentNode;
    div.classList.remove(div.classList[0])
    div.classList.add(newClassName)

}

//Function to call scrape papers when enter is pressed on the input
function key_scrape_papers() {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent the default Enter key behavior
        scrape_papers();
    }
}

function UpdateGroupSelect() {
    selectContainer = document.getElementById("GroupNamesSelect")
    //clear the inner html
    selectContainer.innerHTML = "";
    groups = document.querySelectorAll("#collapsibleDiv");
    //go through all the groups and index them
    for (var i = 0; i < groups.length; i++) {
        var group = groups[i];
        var option = document.createElement('option')
        option.value = group.classList[0];
        option.innerHTML = group.classList[0];
        selectContainer.appendChild(option)
    }
    //LoadReadPapers();
}
