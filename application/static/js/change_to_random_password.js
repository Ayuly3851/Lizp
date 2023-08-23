function get_password() {

    var lenght = document.querySelector('#lenght-password').value;
    var symbols = document.querySelector('#symbols-password').value;
    var lowercase = document.querySelector('#lowercase-password').checked;
    var uppercase = document.querySelector('#uppercase-password').checked;
    var digits = document.querySelector('#digits-password').checked;
    var symbol = document.querySelector('#symbol-password').checked;

    const res = fetch("/password/generate_password", {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                lenght: lenght,
                symbols: symbols,
                lowercase: lowercase,
                uppercase: uppercase,
                digits: digits,
                symbol: symbol
            })
        })
        .then(r => r.json()
            .then(data => ({
                status: r.status,
                body: data
            }))
            .then(obj => {
                return obj.body.password
            })
        );
    return res
}

function change_to_pass(id) {
    var x = document.getElementById(id)
    const password = get_password()
    password.then(a => {
        x.value = a
    })
}

function copy_text(id){
	var copyText = document.getElementById(id);

  copyText.select();
  copyText.setSelectionRange(0, 99999);

  navigator.clipboard.writeText(copyText.value);
}