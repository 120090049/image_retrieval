# try.py
import sys

def main():
    
    if len(sys.argv) == 3:
        image_path = sys.argv[1]  # 图片文件名
        movie_name = sys.argv[2]  # 电影名称

        print(f"Image Path: {image_path}")
        print(f"Movie Name: {movie_name}")
    else:
        print("Incorrect number of arguments provided.")

if __name__ == "__main__":
    main()

