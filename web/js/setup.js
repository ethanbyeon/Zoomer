async function getPath(x) {
    var btn = document.getElementById(x)

    if(x === 'roster') {
        var path = await eel.input_file()();
    }else if(x === 'attendance') {
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
        }else if(x === 'attendance') {
            btn.innerHTML = 'ATTENDANCE SHEET:<br/>' + filename;
            console.log('ATTENDANCE SHEET:\n' + filename);
            btn.style.backgroundColor = '#A3DE83'
            btn.style.color = '#F0F7F4';
            eel.export(filename)
        }
    }
}