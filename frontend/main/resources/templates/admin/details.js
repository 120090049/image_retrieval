document.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  const query = params.get('query');

  const goBackButton = document.getElementById('go-back-button');
  goBackButton.addEventListener('click', () => {
    window.history.back(); // This will take the user back to the previous page
  });
  // For the demo, just show a static movie. In a real application, you would search for the movie based on the query
  displayMovieDetails();
});

function displayMovieDetails() {
  // Hardcoded movie details for the demo
  const movieImage = document.getElementById('movie-image');
  const movieText = document.getElementById('movie-text');

  // Update these values with real data in a full implementation
  movieImage.src = 'https://m.media-amazon.com/images/M/MV5BMWU4N2FjNzYtNTVkNC00NzQ0LTg0MjAtYTJlMjFhNGUxZDFmXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SX300.jpg';
  movieText.innerHTML = `
      <p>12 Angry Men</p >
      <p>Crime, Drama</p >
      <p>America</p >
      <p>1957</p >
  `;
}