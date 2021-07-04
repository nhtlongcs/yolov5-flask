function loginSubmit() {
    var request = new XMLHttpRequest()
    request.onload = function () {
        if (this.responseText == 'true')
            window.location = '/info.html'
        else
            window.location = '/404.html'
    }

    data = {}
    data.user = document.getElementById('user').value
    data.pswd = document.getElementById('pass').value

    request.open('POST', '/login', true)
    request.send(JSON.stringify(data))
}