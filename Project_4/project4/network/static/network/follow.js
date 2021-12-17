document.addEventListener('DOMContentLoaded', () => {
    username = document.querySelector('#username').innerText
    document.querySelector('#follow').addEventListener('click', () => follow(username));
});

function follow(username) {
    let fllw = document.querySelector('#follow').innerText
    let t_or_f
    if (fllw == "Follow") {
        t_or_f = false
        document.querySelector('#follow').innerHTML = "Unfollow"
    } else if(fllw = "Unfollow") {
        t_or_f = true
        document.querySelector('#follow').innerHTML = "Follow"
    }
    fetch (username+'/follow', {
        method: 'PUT',
        body: JSON.stringify({
            follow: !t_or_f
        })
    })
    .then(response => response.json())
    .then(result => {
        let count = result.followers.length
        document.querySelector('#fllwerscount').innerText = count
    })
}