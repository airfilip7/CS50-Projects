document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email('','','',''));
  document.querySelector("#compose-form").onsubmit = () => {
    recipients = document.querySelector("#compose-recipients").value;
    subject = document.querySelector("#compose-subject").value;
    body = document.querySelector("#compose-body").value;

    fetch('/emails', {
            method: 'POST',
            body: JSON.stringify({
                recipients: recipients,
                subject: subject,
                body: body,
            })
        })
    .then(response => response.json())
    .then(result => {
        // Print result
        if (result.error) {
          document.querySelector('#message').className = "alert alert-danger"
          document.querySelector('#message').innerText = result.error
        } else {
          document.querySelector('#message').className = "alert alert-success"
          document.querySelector('#message').innerText = result.message
          setTimeout(clear_compose, 3000);      
        }
        console.log(result);
    });


    return false;
  };
  
  // By default, load the inbox
  load_mailbox('inbox');
    
});

function compose_email(recipients, subject, body, timestamp) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;

}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3 id='inbox'>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch('/emails/'+mailbox)
  .then(response => response.json())
  .then(emails => { 
    // Print emails
  
    // ... do something else with emails ...
    emails.forEach(mail => {
      const email = document.createElement('div')
      let to_or_from = 'From: ' + mail.sender
      if (mailbox === 'sent')
        to_or_from = 'To: ' + mail.recipients
      email.className = `card`;
      email.innerHTML = `
      <div class="card-header">
        ${to_or_from}
        <span style='float: right'>${mail.timestamp}</span>
      </div>
      <div class="card-body">
        <h5 class="card-title">${mail.subject}</h5>
        <p class="card-text">${mail.body}</p>
      </div>`
      if (mail.read == true) {
        email.style.backgroundColor = "lightgray";
      }
      document.querySelector("#emails-view").appendChild(email)
      email.addEventListener('click', () => {
        view_e(mail.id)
      })
    })

    });

}

function view_e(id) {
  document.querySelector('#emails-view').innerHTML = ''

  fetch('/emails/' + id)
    .then(response => response.json())
    .then(email => {
      // Print email
     
      let body = email.body 
      body = JSON.stringify(body)
      body = body.replaceAll(/\\n/g, '</br>')
      email.body = JSON.parse(body)

      is_archived = "Archive"
      if (email.archived)
        is_archived = "Unarchive"

      // ... do something else with email ...
      mail = document.createElement('div')
      mail.innerHTML = `
      <strong>From: </strong> ${email.sender} </br>
      <strong> To: </strong> ${email.recipients} </br>
      <strong> Subject: </strong> ${email.subject} </br> </br>
      ${email.timestamp}  </br> </br>
      <button id="reply" type="button" class="btn btn-outline-primary">Reply</button>
      <button id="archive" type="button" class="btn btn-outline-secondary">${is_archived}</button>
      <hr>
      ${email.body}
      `
      document.querySelector("#emails-view").appendChild(mail);

      user = document.querySelector('h2').innerText
      if (email.sender == user) {
        document.querySelector('#archive').style.display = 'none'
      }

      document.querySelector('#archive').addEventListener('click', () => {
        if (email.archived == false) {
          document.querySelector("#archive").innerText = "Unarchive"
        } else {
           document.querySelector("#archive").innerText = "Archive"
        }
         archive(email.id, email.archived)
      })
      
      document.querySelector('#reply').addEventListener('click', () => {
        reply(email.sender, email.subject, email.body, email.timestamp)
      })
    });

    fetch('/emails/' + id, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    })
}

function archive(id, t_or_f) {
  fetch('/emails/' + id, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !t_or_f
    })
  })
}

function reply(sender, subject, body, timestamp) {
  let _subject = ""
  if (subject.startsWith("Re: ")) {
    _subject = subject
  } else {
    _subject = "Re: " + subject
  }
  body = body.replaceAll("</br>", '\n')
  let _body =' \n\n' + 'On ' + timestamp + ' ' + sender + ' wrote: ' + '\n' + body
  compose_email(sender, _subject, _body, timestamp)
}

function clear_compose() {
  document.querySelector('#compose-recipients').value = "";
  document.querySelector('#compose-subject').value = "";
  document.querySelector('#compose-body').value = "";
  document.querySelector('#message').className = ""
  document.querySelector('#message').innerText = ""
}
