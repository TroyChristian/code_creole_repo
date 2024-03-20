function scrollToComments() {
    document.getElementById("commentSection").scrollIntoView({ behavior: 'smooth' });
  }


  let likeCount = 0; // Initial like count

  function incrementLike() {
      likeCount++; // Increment the like count
      document.getElementById("likeCount").innerText = likeCount; // Update the display
  }