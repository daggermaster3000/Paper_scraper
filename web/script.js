// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();

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
    eel.load_csv("read_papers.csv", "readTable", "myreadTable")(function (content) {
        // clear the div
        var myDiv = document.getElementById("readpapers");
        myDiv.innerHTML = "";

        // Update the div 
        document.querySelector(".readpapers").innerHTML = content;

        //Add checkboxes
        var table = document.getElementById("myreadTable");
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
            checkbox.checked = true;
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
        headerCell.textContent = "Reading";
        headerRow.insertBefore(headerCell, headerRow.firstChild);
        $('#myreadTable').DataTable();
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
    function wait(callback) {
        setTimeout(callback, 5000); // 5 seconds
    }
    wait(function () {
        LoadReadPapers();
    });


}
function AddReadEntry(title) {
    console.log("Adding read entry");
    // Get keyword input
    var inputElement = document.getElementById("keywordInput");
    var keyword = inputElement.value;
    eel.add_read_entry(keyword, title);
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
}


//code for the collapsible
let groupList = []
function createGroup() {
    // get the group name
    input = document.getElementById('groupInput')
    groupName = input.value;
    groupList.push(groupName)
    //Create the html
    var collapsibleDiv = document.createElement('div');
    collapsibleDiv.setAttribute("id", "collapsibleDiv")
    //Create the collapsible button
    var collapsibleButton = document.createElement('button');
    collapsibleButton.textContent = groupName;
    collapsibleButton.classList.add('collapsible');
    collapsibleButton.setAttribute("id", "collapsibleButton")
    collapsibleButton.innerHTML = '<input type="text" placeholder="Enter text" class="input-field">'

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



    var coll = document.getElementsByClassName("collapsible");
    var i;

    // Make the stuff collapsible
    for (i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function () {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
        });
    }
    //Manage the backend

}

//Function to call scrape papers when enter is pressed on the input
function key_scrape_papers() {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent the default Enter key behavior
        scrape_papers();
    }
}