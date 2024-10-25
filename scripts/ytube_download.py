import yt_dlp
import os
from urllib.error import HTTPError, URLError


def download_video(url, output_path="downloads"):
    """Downloading YouTube video using yt-dlp"""
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # Save file with video title
            'format': 'best',  # Download the best quality available
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(url, download=True)
                print(f"Downloaded: {info_dict['title']}")
                print(f"Views: {info_dict['view_count']}")
                print(f"Duration: {info_dict['duration']} seconds")
                print(f"Rating: {info_dict.get('average_rating', 'N/A')}")

            except HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
            except URLError as url_err:
                print(f"URL error occurred: {url_err}")
            except KeyError as key_err:
                print(f"Missing key in response: {key_err}")
            except yt_dlp.utils.DownloadError as download_err:
                print(f"Download error occurred: {download_err}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    except FileExistsError:
        print(f"Output path {output_path} already exists but is not a directory.")
    except PermissionError:
        print("Permission denied: Unable to write to the specified directory.")
    except OSError as os_err:
        print(f"OS error occurred: {os_err}")
    except Exception as e:
        print(f"An unexpected error occurred during setup: {e}")


# Don't forget to pip install yt-dlp before running the script
if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    download_video(video_url)



