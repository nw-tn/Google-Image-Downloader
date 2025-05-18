import os
import time
import requests
import argparse


def download_images(query, total_images, api_key, cx, downloaded=0, save_dir='downloaded images/'):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print("Successfully created a 'downloaded images' folder for downloading the images...")
        
    start_index = 1
    downloaded = downloaded
    search_url = 'https://www.googleapis.com/customsearch/v1'
    
    while downloaded < total_images and start_index < 100:
        num_images = min(10, total_images - downloaded)

        params = {
            'q': query,
            'cx': cx,
            'key': api_key,
            'searchType': 'image',
            'num': num_images,
            'start': start_index
        }

        try:
            response = requests.get(search_url, params)
            results = response.json()
        except Exception as e:
            print(e)

        items = results.get('items')
        #print(items)

        if not items:
            print('No more images found/')
            break

        for item in items:
            img_url = item['link']
            try:
                img_data = requests.get(img_url).content
                file_path = os.path.join(save_dir, f'image_{downloaded + 1}.jpg')
                with open(file_path, 'wb') as f:
                    f.write(img_data)
                    print(f'Downloaded {file_path}')
                downloaded += 1
            except Exception as e:
                print(f'Could not download {img_url} - {e}')

        start_index += num_images
        time.sleep(1)
    
def main():
    while True:
        query = input("What's your search term?: ")
        total_images = int(input("How many images do you want to download?: "))
        api_key = input("Enter your Api Key: ")
        cx = input("Enter your Google CX ID: ")
        downloaded = int(input("How many samples do you have currently?: "))

        try:
            download_images(query, total_images, api_key, cx, downloaded)
            break
        except HTTPException:
            print("Check your internet connection and try again...")
            print("_"*30)
        except Exception as e:
            print(e)
            
if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="Google Image Downloader")
    
    argparser.add_argument("query", help="The query term")
    argparser.add_argument("total_images", type=int, help="Number of images you want downloaded")
    argparser.add_argument("api_key", help="Your Google Search API Key")
    argparser.add_argument("cx", help="Your Google CX ID")
    argparser.add_argument("-d", "--downloaded", type=int, default=0)
    
    args = argparser.parse_args()
    
    try:
        download_images(args.query, args.total_images, args.api_key, args.cx, args.downloaded)
        print("."*30 + "Download Completed" + "."*30)
    except HTTPException:
        print("Check your internet connection and try again...")
        print("_"*30)
    except Exception as e:
        print(e)
