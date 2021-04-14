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
            btn.innerHTML = 'CLASS ROSTER:<br/>' + filename;
            console.log('CLASS ROSTER:\n' + filename);
            btn.style.backgroundColor = '#A3DE83'
            btn.style.color = '#F0F7F4';
        }else if(x === 'export_btn') {
            btn.innerHTML = 'ATTENDANCE SHEET:<br/>' + filename;
            console.log('ATTENDANCE SHEET:\n' + filename);
            btn.style.backgroundColor = '#A3DE83'
            btn.style.color = '#F0F7F4';
        }
    }
}


eel.expose(take_attendance);
async function take_attendance(x) {
    eel.admit(x);
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