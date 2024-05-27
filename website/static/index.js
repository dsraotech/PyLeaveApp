function deleteNote() {
    fetch("/delete-note", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ noteid: noteId })
    })
    .then((_res) => {
        window.location.href = "/";
    });
}

function deleteNote() {
    fetch("/deleteNote", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ noteid: noteId })
    })
    .then((_res) => {
        window.location.href = "/";
    });
}
