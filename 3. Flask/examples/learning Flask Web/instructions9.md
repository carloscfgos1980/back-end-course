# Add and deleta notes
1. Add the script to handle javascript in order to delete the note. base.html
    <script type="text/javascript" src="{{ url_for('static', filename='index.js') }}"></script>

* At the end of body section

2. Add a form in home.html in order to add the notes
<form method="POST">
    <textarea name="note" id="note" class="form-control"></textarea>
    <br />
    <div align="center">
        <button type="submit" class="btn btn-primary">Add Note</button>
    </div>
</form>


3. Display the notes dynamicaly by looping <user.notes>
3.1 Create the <ul>:
<ul class="list-group list-group-flush" id="notes">

3.2 Loop thru user.notes:
    {% for note in user.notes %}
    <li class="list-group-item"> {{ note.data }}

3.3 add btn to delete the notes. Here is combine Javascript and Python
        <button type="button" class="close" onClick="deleteNote({{ note.id }})">
            <span aria-hidden="true">&times;</span>
        </button>
* onClick="deleteNote({{ note.id }}) is the Java method. We need to define a function in index.js for this to work.
* {{ note.id }} is python, this is give us the id number of the user that later on we will use in the delete-note javascript

* The whole thing look like this:
<ul class="list-group list-group-flush" id="notes">
    {% for note in user.notes %}
    <li class="list-group-item"> {{ note.data }}
        <button type="button" class="close" onClick="deleteNote({{ note.id }})">
            <span aria-hidden="true">&times;</span>
        </button>
    </li>
    {% endfor %}
</ul>

4. function <delete-note> index.js:
function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

