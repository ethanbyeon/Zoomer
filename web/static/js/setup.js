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
            let out = '<ion-icon name="people"></ion-icon><br/>CLASS ROSTER:<br/>';
            btn.innerHTML = out + filename;
            console.log('CLASS ROSTER:\n' + filename);
            btn.style.backgroundColor = '#C2D076'
            btn.style.color = '#F0F7F4';
        }else if(x === 'export_btn') {
            let out = '<ion-icon name="clipboard"></ion-icon><br/>ATTENDANCE SHEET:<br/>';
            btn.innerHTML = out + filename;
            console.log('ATTENDANCE SHEET:\n' + filename);
            btn.style.backgroundColor = '#C2D076'
            btn.style.color = '#F0F7F4';
        }
    }
}


eel.expose(take_attendance);
async function take_attendance(x) {
    let out_div = document.getElementById('output');
    out_div.style.fontSize = "18px";
    out_div.innerHTML = `Please Wait<br/>Admitting ${x}...`;
    
    let attendance = await eel.admit(x)();
    out_div.innerHTML = attendance;

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