document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#add_post').addEventListener('click', () => add_form());
    document.querySelector('#add_form').onsubmit = () => post();
    document.querySelector('#cancel-add').addEventListener('click', () => cancel_add())

    let edits = document.querySelectorAll('#edit');
    edits.forEach((elem) => {
        elem.addEventListener('click', () => edit(elem));
    });

    let edit_forms = document.querySelectorAll('.edit_form')
    edit_forms.forEach((form) => {
        form.onsubmit = () => update_edit()
    })

    let likes = document.querySelectorAll('#like')
    likes.forEach((like) => {
        like.addEventListener('click', () => like_add())
    })

    let cancel = document.querySelectorAll('#cancel');
    cancel.forEach((bttn) => {
        bttn.addEventListener('click', () => cancel_edit());
    })
}) 

function add_form() {
    document.querySelector('#exampleFormControlTextarea1').value = ""
    document.querySelector("#add").style.display = 'block'
}

function cancel_add() {
    document.querySelector('#add').style.display = 'none'
}

function post() {
    content = document.querySelector('#exampleFormControlTextarea1').value
    fetch('/add', {
        method: 'POST',
        body: JSON.stringify({
            content: content,
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        if (result.error) {
            document.querySelector('#message').className = "alert alert-danger rounded width_1"
            document.querySelector('#message').innerText = result.error
            document.querySelector("#message").style.display = 'block';
        } else {
            document.querySelector("#message").style.display = 'block';
            document.querySelector('#message').className = "alert alert-success rounded width_1"
            document.querySelector('#message').innerText = result.message
            setTimeout(function () {
                document.querySelector('#message').style.display = "none"
            }, 2500)
            setTimeout(function () {
                document.querySelector("#add").style.display = 'none';
            }, 500)
            update()
        }
    });
    return false;
}

function edit(elem) {
    let id = elem.getAttribute("data-pk");
    let div = document.querySelector('#edit_form_'+id)
    let init = document.querySelector('#post-content-'+id)

    div.style.display = "block"
    init.style.display = "none"

    return false;
}

function update_edit() {
    let pk = event.target.getAttribute("data-pk")
    let content = document.querySelector('#edit_'+pk).value
    let form = document.querySelector("#edit_form_" + pk)
    let init = document.querySelector('#post-content-' + pk)
    let message = document.querySelector("#post-message-" + pk)

    fetch('/edit', {
        "method": "PUT",
        "body": JSON.stringify({
            "content": content,
            "pk": pk,
        })
    })
    .then(response => response.json())
    .then(result => {
        if(result.error) {
            message.className = "alert alert-danger rounded width_1"
            message.innerText = result.error
            message.style.display = "block"
        } else {
            message.className = "alert alert-success rounded width_1"
            message.innerText = result.message
            message.style.display = "block"

            setTimeout(() => {
                message.style.display = "none"
            }, 2000)

            init.innerText = content
            form.style.display = "none"
            init.style.display = "block"
        }
    })
    return false;
}

function cancel_edit() {
    let elem = event.target
    pk = elem.getAttribute('data-pk')
    let div = document.querySelector('#edit_form_' + pk)
    let init = document.querySelector('#post-content-' + pk)

    div.style.display = "none"
    init.style.display = "block"

    return false;
}

function like_add() {
    elem = event.target
    pk = elem.getAttribute('data-pk')
    liked = elem.getAttribute('data-liked')
    count = document.querySelector('#like-count-' + pk)
    count_val = parseInt(count.innerText)

    if( elem.className == "fas fa-heart") {
        elem.className = "far fa-heart"
        count.innerText = count_val - 1

    } else {
        elem.className = "fas fa-heart"
        count.innerText = count_val + 1
    }

    if( liked == "no") {
        liked = false
        elem.setAttribute('data-liked', 'yes')
    } else if ( liked == "yes") {
        liked = true
         elem.setAttribute('data-liked', 'no')
    }
 
    fetch('/like', {
        "method": "PUT",
        "body": JSON.stringify({
            "pk": pk,
            "liked": !liked
        })
    })

    return false;
        
}

function update() {
    var request = new XMLHttpRequest();

    request.onreadystatechange = function () {
        if (this.status >= 200 && this.status < 400 && request.readyState == 4) {
            // Success!
            var resp = this.response;
            let div = document.createElement('div')
            div.innerHTML = resp
            let content = div.querySelector('#post-container').innerHTML
            let post = document.createElement('div')
            post.innerHTML = content
            let feed = document.querySelector('#feed')
            if (!feed) {
                return;
            }
            feed.insertAdjacentElement('afterbegin', post)

            onreload()
        } else {
            // We reached our target server, but it returned an error
            console.error(request.statusText);

        }
    };
    request.open('GET', '/', true);
    request.send();
}

function onreload() {
    let edit_ = document.querySelector('#edit');
    let edit_form = document.querySelector('.edit_form')
    let like = document.querySelector('#like')
    let cancel = document.querySelector('#cancel');

    edit_.addEventListener('click', () => edit(edit_))
    edit_form.onsubmit = () => update_edit()
    like.addEventListener('click', () => like_add())
    cancel.addEventListener('click', () => cancel_edit())

}
