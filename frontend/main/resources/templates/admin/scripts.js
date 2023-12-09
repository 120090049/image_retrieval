//document.addEventListener('DOMContentLoaded', () => {
//  // 选择所有的筛选按钮
//  const filterButtons = document.querySelectorAll('.filter-button');
//  filterButtons.forEach(button => {
//    button.addEventListener('click', () => handleFilterClick(button));
//  });
//
//  // 初始化电影列表
//  populateMovies();
//});
//
//function handleFilterClick(button) {
//  // 移除当前筛选组中其他按钮的active类
//  let siblingButtons = button.parentNode.querySelectorAll('.filter-button');
//  siblingButtons.forEach(btn => btn.classList.remove('active'));
//
//  // 添加active类到被点击的按钮
//  button.classList.add('active');
//
//  // 调用函数来根据新的筛选条件更新电影列表
//  updateMoviesDisplay();
//}
//
//function updateMoviesDisplay() {
//  // 获取所有活跃的筛选器值
//  const region = document.querySelector('#region-filter .active').dataset.value;
//  const type = document.querySelector('#type-filter .active').dataset.value;
//  const year = document.querySelector('#year-filter .active').dataset.value;
//
//  // 假设movies是从你的数据库或API获取的电影数组
//  // 下面是伪代码，表示根据筛选条件过滤电影列表的逻辑
//  const filteredMovies = movies.filter(movie => {
//    return (region === 'all' || movie.region === region) &&
//           (type === 'all' || movie.type === type) &&
//           (year === 'all' || movie.year === year);
//  });
//
//  // 清空当前的电影列表
//  const moviesDisplay = document.querySelector('.movies-display');
//  moviesDisplay.innerHTML = '';
//
//  // 添加过滤后的电影到列表中
//  filteredMovies.forEach(movie => {
//    const movieItem = document.createElement('div');
//    movieItem.className = 'movie-item';
//    movieItem.innerHTML = `
//      < img src="${movie.image}" alt="${movie.title}">
//      <h3>${movie.title}</h3>
//    `;
//    // 每个电影项添加点击事件
//    movieItem.addEventListener('click', () => {
//      // 这里应该是打开电影详情的逻辑
//    });
//    moviesDisplay.appendChild(movieItem);
//  });
//}
//
//// Dummy data for demonstration
//const movies = [
//  // 你需要替换以下对象为你的电影对象
//  { title: "电影1", image: "movie1.jpg", region: "china", type: "action", year: "2023", rating: "8.5", boxOffice: "100M" },
//  // ...更多电影对象...
//];

// 假定的电影数据

//接上db//动态
const movies = [
  { title: "The Shawshank Redemption", image: "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_SX300.jpg", region: "China", type: "Adventure", year: "2023", rating: "8.5", boxOffice: "100M" },
  { title: "The Godfather", image: "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg", region: "America", type: "Comedy", year: "2022", rating: "7.2", boxOffice: "200M" },
  { title: "The Dark Knight", image: "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg", region: "Korea", type: "Action", year: "2021", rating: "9.1", boxOffice: "150M" },
  { title: "The Godfather Part II", image: "https://m.media-amazon.com/images/M/MV5BMWMwMGQzZTItY2JlNC00OWZiLWIyMDctNDk2ZDQ2YjRjMWQ0XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg", region: "Japan", type: "Horror", year: "2020", rating: "6.5", boxOffice: "50M" },
  { title: "12 Angry Men", image: "https://m.media-amazon.com/images/M/MV5BMWU4N2FjNzYtNTVkNC00NzQ0LTg0MjAtYTJlMjFhNGUxZDFmXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SX300.jpg", region: "China", type: "Romance", year: "2019", rating: "8.0", boxOffice: "120M" },
  { title: "Schindler's List", image: "https://m.media-amazon.com/images/M/MV5BNDE4OTMxMTctNmRhYy00NWE2LTg3YzItYTk3M2UwOTU5Njg4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg", region: "China", type: "Comedy", year: "2023", rating: "8.5", boxOffice: "100M" },
  { title: "Pulp Fiction", image: "https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg", region: "America", type: "Comedy", year: "2022", rating: "7.2", boxOffice: "200M" },
  { title: "The Lord of the Rings: The Return of the King", image: "https://m.media-amazon.com/images/M/MV5BNzA5ZDNlZWMtM2NhNS00NDJjLTk4NDItYTRmY2EwMWZlMTY3XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg", region: "Korea", type: "Action", year: "2021", rating: "9.1", boxOffice: "150M" },
  { title: "The Good, the Bad and the Ugly", image: "https://m.media-amazon.com/images/M/MV5BNjJlYmNkZGItM2NhYy00MjlmLTk5NmQtNjg1NmM2ODU4OTMwXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_SX300.jpg", region: "Japan", type: "Horror", year: "2020", rating: "6.5", boxOffice: "50M" },
  { title: "Forrest Gump,Robert Zemeckis", image: "https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg", region: "China", type: "Romance", year: "2019", rating: "8.0", boxOffice: "120M" }
];

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', () => {
  // 初始化电影列表
  populateMovies();
});

//// 用于填充电影列表的函数
//function populateMovies() {
//  const moviesDisplay = document.querySelector('.movies-display');
//  moviesDisplay.innerHTML = ''; // 清空当前电影列表
//
//  // 遍历电影数据数组，为每部电影创建DOM元素并添加到页面中
//  movies.forEach(movie => {
//    const movieItem = document.createElement('div');
//    movieItem.className = 'movie-item';
//    movieItem.innerHTML = `
//      < img src="${movie.image}" alt="${movie.title}" class="movie-image">
//      <div class="movie-info">
//        <h3>${movie.title}</h3>
//      </div>
//    `;
//    movieItem.addEventListener('click', () => {
//      // 点击电影项时的操作，例如可以用来打开电影详情页或者显示详情弹窗
//      // 这里可以根据具体需求来编写逻辑，例如：
//      // window.location.href = '/movie-detail-page?movieId=' + movie.id;
//    });
//    moviesDisplay.appendChild(movieItem);
//  });
//}
// 用于填充电影列表的函数
function populateMovies() {
  const moviesDisplay = document.querySelector('.movies-display');
  moviesDisplay.innerHTML = ''; // 清空当前电影列表

  // 遍历电影数据数组，为每部电影创建DOM元素并添加到页面中
  movies.forEach(movie => {
    const movieItem = document.createElement('div');
    movieItem.className = 'movie-item';
    // 确保 img 标签正确关闭，并去掉前面的空格
    movieItem.innerHTML = `
      <img src="${movie.image}" alt="${movie.title}" class="movie-image">
      <div class="movie-info">
        <h3>${movie.title}</h3>
      </div>
    `;
    // 添加点击事件监听器，用于导航到电影详情页或执行其他操作
    movieItem.addEventListener('click', () => {
      // 这里可以插入跳转到电影详细信息页的逻辑
    });
    // 将电影元素添加到页面中
    moviesDisplay.appendChild(movieItem);
  });
}


//// 筛选电影的函数（未实现，因为我们没有筛选逻辑）
//function updateMoviesDisplay() {
//  // ...根据筛选条件更新电影列表的逻辑...
//}
//
////// 筛选按钮点击事件处理函数（未实现，因为我们没有按钮点击逻辑）
////function handleFilterClick(button) {
////  // ...按钮点击逻辑...
////}
//// 筛选按钮点击事件处理函数
//// Existing code...

// Simplified handleFilterClick function for demo
// Simplified handleFilterClick function for demo
function handleFilterClick(clickedButton) {
  const buttons = clickedButton.parentNode.querySelectorAll('.filter-button');
  buttons.forEach(button => {
    button.classList.remove('active');
  });
  clickedButton.classList.add('active');

  // Only display Action movies when the Action button is clicked
  if(clickedButton.getAttribute('data-value') === 'action') {
    displayActionMoviesOnly();
  } else {
    populateMovies(); // Display all movies for other filters
  }
}


// Function to display only Chinese movies (movie3 and movie8)
// Function to display only Action movies
function displayActionMoviesOnly() {
  const moviesDisplay = document.querySelector('.movies-display');
  moviesDisplay.innerHTML = '';

  // Filter to display only Action movies
  const actionMovies = movies.filter(movie => movie.type === "Action");
  actionMovies.forEach(movie => {
    const movieItem = document.createElement('div');
    movieItem.className = 'movie-item';
    movieItem.innerHTML = `
      <img src="${movie.image}" alt="${movie.title}" class="movie-image">
      <div class="movie-info">
        <h3>${movie.title}</h3>
      </div>
    `;
    moviesDisplay.appendChild(movieItem);
  });
}


// Existing code for event listeners...

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', () => {
  // 选择所有的筛选按钮并绑定点击事件
  const filterButtons = document.querySelectorAll('.filter-button');
  filterButtons.forEach(button => {
    button.addEventListener('click', function() {
      handleFilterClick(this);
    });
  });

  // 初始化电影列表
  populateMovies();
});


function searchMovie() {
  const searchInput = document.getElementById('search-input').value;
  window.location.href = 'movie-details.html?query=' + encodeURIComponent(searchInput);
}