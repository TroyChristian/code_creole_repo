function scrollToComments() {
    document.getElementById("commentSection").scrollIntoView({ behavior: 'smooth' });
  }


  let likeCount = 0; // Initial like count

function incrementLike(articleId) {
    fetch(`/article/${articleId}/like/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Function to get CSRF token from cookie
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin' // Necessary for including CSRF token
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            document.getElementById(`like-count-${articleId}`).innerText = data.new_like_count;
        }
    })
    .catch(error => console.error('Error:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function editComment(commentId) {
    var commentTextElement = document.getElementById('comment-text-' + commentId);
    var textarea = document.getElementById('edit-textarea-' + commentId);
    var saveButton = document.getElementById('save-button-' + commentId);

    // Toggle the display of textarea and buttons if they already exist
    if (textarea && saveButton) {
        if (textarea.style.display === 'none') {
            // Show textarea with the original text
            textarea.style.display = 'block';
            saveButton.style.display = 'block';
            textarea.value = commentTextElement.getAttribute('data-original-text');  // Use the original text saved in an attribute
        } else {
            // Hide textarea and reset the text to original
            textarea.style.display = 'none';
            saveButton.style.display = 'none';
        }
    } else {
        // First time setup: add textarea and save button
        var currentText = commentTextElement.innerHTML;
        commentTextElement.setAttribute('data-original-text', currentText);  // Save the original text

        var textareaHTML = '<textarea id="edit-textarea-' + commentId + '" style="display:block;">' + currentText + '</textarea>';
        var saveButtonHTML = '<button id="save-button-' + commentId + '" onclick="saveComment(' + commentId + ')" style="display:block;">Save</button>';
        var cancelButtonHTML = '<button onclick="editComment(' + commentId + ')" style="display:block;">Cancel</button>';

        // Replace the paragraph with a textarea and add save and cancel buttons
        commentTextElement.innerHTML = textareaHTML + saveButtonHTML + cancelButtonHTML;
    }
}

function saveComment(commentId) {
    var editedText = document.getElementById('edit-textarea-' + commentId).value;
    var commentTextElement = document.getElementById('comment-text-' + commentId);

    // Prepare the AJAX request
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/save-comment/', true); // Adjust the URL as needed
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken')); // CSRF token for Django

    // Handle the response
    xhr.onload = function () {
        if (xhr.status === 200) {
            // Update the UI on successful save
            commentTextElement.innerHTML = editedText;
        } else {
            // Handle errors
            alert('Error saving comment: ' + xhr.responseText);
        }
    };

    // Send the request
    xhr.send(JSON.stringify({ commentId: commentId, text: editedText }));
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
