eel.expose(getPath);
async function getPath(x) {
    var btn = document.getElementById(x)

    if(x === 'roster') {
        var path = await eel.input_file()();
    }else if(x === 'export_btn') {
        var path = await eel.output_file()();
    }
    
    if(path) {
        console.log(path);
        var filename = path.replace(/^.*[\\\/]/, '')

        if(x === 'roster'){
            let out = `<span class="material-icons md-light">file_upload</span>
                        <h2>${filename}</h2>`;
            btn.innerHTML = out;
            console.log('ROSTER:\n' + filename);
            btn.style.backgroundColor = '#C2D076'
            btn.style.color = '#F0F7F4';
        }else if(x === 'export_btn') {
            let out = `<span class="material-icons md-light">assessment</span>`;
            btn.innerHTML = out + filename;
            console.log('EXPORT:\n' + filename);
            btn.style.backgroundColor = '#C2D076'
            btn.style.color = '#F0F7F4';
        }
    }
}


eel.expose(take_attendance);
async function take_attendance(x) {
    // let out_div = document.getElementById('output');
    // out_div.style.fontSize = "18px";
    // out_div.innerHTML = `Please Wait<br/>Admitting ${x}...`;
    
    let attendance = await eel.admit(x)();
    // out_div.innerHTML = attendance;

    console.log(attendance);
}


eel.expose(dashboard);
async function dashboard() {
    let container = document.getElementById('dashboard');
    let remote = document.getElementById('remote');

    container.style.display = "flex";
    remote.style.display = "none";
}


eel.expose(home);
async function home() {
    let container = document.getElementById('dashboard');
    let remote = document.getElementById('remote');
    
    container.style.display = "none";
    remote.style.display = "flex";
}


eel.expose(create_table);
function create_table(x) {
    var data = x;
    console.log("HELLO WORLD!");
    console.log(x);
    console.log(`USERS (${data.length} results)`);
    let table = document.getElementsByTagName("tbody")[0];
    table.innerHTML = `
        ${data.map(function(user) {
            return `
            <tr>
                <td>${user.id}</td>
                <td>${user.last}, ${user.first}${user.middle ? ' ' + user.middle : ''}</td>
                <td>${user.status ? user.status : 'UNKNOWN'}</td>
                <td>${user.date ?  user.date : 'NA'}</td>
                <td>
                </td>
            </tr>
            `
        }).join('')}
    `;
}


// FILTER
search.addEventListener("keyup", function(event) {
    let query = event.target.value.toLowerCase();
    let rows = document.querySelectorAll("tbody tr");
    
    rows.forEach(row => {
        var firstCol = row.querySelector("td").textContent.toLowerCase();
        var secondCol = row.querySelectorAll("td")[1].textContent.toLowerCase();
        var thirdCol = row.querySelectorAll("td")[2].textContent.toLowerCase();

        (firstCol.indexOf(query) > -1 || secondCol.indexOf(query) > -1 || thirdCol.indexOf(query) > -1)
        ? row.style.display = ""
        : row.style.display = "none";
    });
});


// TABLE SORT
/**
 * Sorts an HTML table.
 * 
 * @param {HTMLTableElement} table The table to sort
 * @param {number} column The index of the column to sort
 * @param {boolean} asc Determines if the sorting will be in ascending/descending
 */
function sortTableByColumn(table, column, asc=true) {
    const dirModifier = asc ? 1: -1;
    const tBody = table.tBodies[0];
    const rows = Array.from(tBody.querySelectorAll("tr"));

    const sortedRows = rows.sort((a, b) => {
        const aColText = a.querySelector(`td:nth-child(${column + 1})`).textContent.trim();
        const bColText = b.querySelector(`td:nth-child(${column + 1})`).textContent.trim();

        return aColText > bColText ? (1 * dirModifier) : (-1 * dirModifier);
    });

    while(tBody.firstChild) {
        tBody.removeChild(tBody.firstChild);
    }
    tBody.append(...sortedRows);

    table.querySelectorAll("th").forEach(th => th.classList.remove("th-sort-asc", "th-sort-desc"));
    table.querySelector(`th:nth-child(${column + 1})`).classList.toggle("th-sort-asc", asc);
    table.querySelector(`th:nth-child(${column + 1})`).classList.toggle("th-sort-desc", !asc);
}

document.querySelectorAll(".content-table th:not(:first-child):not(:last-child)").forEach(headerCell => {
    headerCell.addEventListener("click", () => {
        const tableElement = headerCell.parentElement.parentElement.parentElement;
        const headerIndex = Array.prototype.indexOf.call(headerCell.parentElement.children, headerCell);
        const currentIsAscending = headerCell.classList.contains("th-sort-asc");
        console.log(tableElement);
        sortTableByColumn(tableElement, headerIndex, !currentIsAscending);
    });
});