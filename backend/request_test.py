import requests

def get_movie_info(message):
    response = requests.post("http://localhost:5001/movie_info", json={"film_name": message})
    print(response.json())

if __name__ == "__main__":
    get_movie_info("The Shawshank Redemption")
