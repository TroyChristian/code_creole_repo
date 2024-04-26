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
