# 电影信息列表
movie_info_list = []

# 函数：将电影信息打印出来
def print_movie_info():
    for movie_info in movie_info_list:
        print(f"Name: {movie_info['name']}")
        print(f"Type: {movie_info['type']}")
        print(f"Year: {movie_info['year']}")
        print(f"Country: {movie_info['country']}")
        print()

if __name__ == '__main__':
    print_movie_info()


