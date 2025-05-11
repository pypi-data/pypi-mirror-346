# Import necessary libraries
#import google_colab_selenium as gs
import chromedriver_installer # This package avoids the need to manually pass a Chromedriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from lxml import html
import re
import time


# Image extraction - Libraries
from PIL import Image, ExifTags
import psutil
from urllib.error import URLError, HTTPError
from http.client import IncompleteRead
import requests
from lxml import html
from io import BytesIO
import re
from urllib.parse import urlparse
import os
import zipfile # Zip file library
from tqdm import tqdm  # For the progressbar


#__________________________________________________

# 1) Create frunctions for tasks.
## 1.1) Auto-install correct ChromeDriver version for ease of use.

# Function to attempt chromedriver installation with retries
def install_chromedriver(retries=3, delay=5):
    """
    Installs Chromedriver with retry attempts.

    Parameters:
    retries (int): Number of retry attempts (default: 3).
    delay (int): Delay between attempts in seconds (default: 5).

    Raises:
    RuntimeError: If installation fails after all retries.
    """

    for attempt in range(retries):
        try:
            chromedriver_installer.install_chromedriver()  # Check and install chromedriver
            print("Chromedriver installed successfully.")
            return
        except (URLError, HTTPError, IncompleteRead) as e:
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    raise RuntimeError("Failed to install chromedriver after multiple attempts.")



#__________________________________________________

## 1.2) Open browser and navigate to url.

# [FINAL]
# Functions to load existing profile into the chrome browser and access MS Teams.
# Function to check if the browser is already open
def is_browser_open(process_name='chrome'):
    """
    Check if the specified browser process is currently running.

    Parameters:
    process_name (str): The name of the browser process to check (default: 'chrome').

    Returns:
    bool: True if the browser is open, False otherwise.
    """
        
    for proc in psutil.process_iter(['pid', 'name']):
        if process_name in proc.info['name'].lower():
            return True
    return False

#__________________________________________________

# Function to open the browser if not open and navigate to a URL with a saved profile
def open_browser_with_profile_and_navigate(url, isHeadless, scalefactor, window_height, window_width, headless_scalefactor, headless_height, headless_width):
    """
    Open the browser with a specified user profile and navigate to a URL.

    Parameters:
    url (str): The URL to navigate to.
    user_data_dir (str): The directory where user data is stored.
    profile_directory (str): The specific profile directory to load.
    isHeadless (bool): True for headless mode, False for UI mode.
    scalefactor (float): Scale factor for the UI mode.
    window_height (int): Height of the browser window in UI mode.
    window_width (int): Width of the browser window in UI mode.
    headless_scalefactor (float): Scale factor for headless mode.
    headless_height (int): Height of the browser window in headless mode.
    headless_width (int): Width of the browser window in headless mode.

    Returns:
    WebDriver: The Chrome WebDriver instance.
    """

    options = webdriver.ChromeOptions()
    options.add_argument("--high-dpi-support=1")

    if isHeadless:

        print("WARNING 1: If the new chats are not exported, please use the Browser UI and click on the sign in button on Teams UI banner.")
        print("\nWARNING 2: The TEAMS CHANNEL navigation button should be pinned to the sidebar, pin it - if it is unpinned.")
        print("\nHeadless browser mode initiated - NO Browser UI will be displayed.")
        print("To view the browser UI, pass the arguments (isHeadless = False).\n")
        
        options.add_argument("--headless")
        # options.add_argument("--force-device-scale-factor=0.3")
        # options.add_argument("--window-size=2400,19900")
        options.add_argument(f"--force-device-scale-factor={headless_scalefactor}")
        options.add_argument(f"--window-size={headless_width},{headless_height}")  
    
    else:
        print("WARNING 1: If the new chats are not exported, please use the Browser UI and click on the sign in button on Teams UI banner.")
        print("\nWARNING 2: The TEAMS CHANNEL navigation button should be pinned to the sidebar, pin it - if it is unpinned.")
        print("\nUI browser mode initiated - Browser UI will be displayed.")
        print("To use a Headless browser, pass the arguments (isHeadless = True).\n")
        print("\nPlease ensure ZOOM Level in UI = 70 percent or less.\n")

        options.add_argument(f"--window-size={window_width},{window_height}")
        # options.add_argument("--window-size=2000,20000")  
        options.add_argument(f"--force-device-scale-factor={scalefactor}")

    
    if is_browser_open():
        print("Browser is already open. Skipping new browser launch.")
        # driver = webdriver.Chrome(service=ChromeService(driver_path), options=options)

        # Auto fetch and use ChromeDriver.
        # Attempt to install chromedriver with retry logic
        install_chromedriver()
        driver = webdriver.Chrome(options=options)

        driver.get(url)
        print(f"Navigated to {url}")

    else:
        #options.add_argument("--window-size=1280,800")
        # driver = webdriver.Chrome(service=ChromeService(driver_path), options=options)
        
        # Auto fetch and use ChromeDriver.
        # Attempt to install chromedriver with retry logic
        install_chromedriver()
        driver = webdriver.Chrome(options=options)

        driver.get(url)
        print(f"Navigated to {url}")
    
    return driver


#__________________________________________________

## 1.3) reusable functions.

# Dynamic wait to be used in all functions.
def wait_for_element_to_be_visible(driver, xpath, max_retries=3, wait_time=10):

    """
    Wait for an element to become visible on the page.

    This function attempts to locate an element specified by the 
    XPath and waits for it to be visible, retrying a specified 
    number of times if not found.

    Parameters:
    driver (WebDriver): The Selenium WebDriver instance.
    xpath (str): The XPath of the element to wait for.
    max_retries (int): Maximum number of retry attempts (default: 3).
    wait_time (int): Maximum wait time for each attempt in seconds (default: 10).

    Returns:
    WebElement: The visible element if found.

    Raises:
    TimeoutException: If the element is not visible after the maximum retries.
    """
        
    retries = 0
    while retries < max_retries:
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            return element
        except TimeoutException:
            retries += 1
            if retries == max_retries:
                raise
            print(f"Retrying... ({retries}/{max_retries})")



# Click on link.
def click_link(driver, xpath):
    """
    Click on a link identified by the specified XPath.

    This function waits for the link to become visible and attempts
    to click it. If the element is not found within the maximum 
    retry attempts, it handles the exception and prints an error message.

    Parameters:
    driver (WebDriver): The Selenium WebDriver instance.
    xpath (str): The XPath of the link to be clicked.

    Returns:
    WebDriver: The Selenium WebDriver instance after attempting to click the link.

    Raises:
    TimeoutException: If the element is not visible after the maximum retries.
    """

    # Implementing try and catch.
    try:
        link = wait_for_element_to_be_visible(driver, xpath, max_retries=5, wait_time=10)
        # link = driver.find_element(By.XPATH, xpath)
        link.click()
        return driver
    
    except TimeoutException:
        print("Element was not found after the maximum retries xpath - ", xpath)
    


#--------------------------------------------


# Function to extract image URLs from HTML content
def extract_image_urls(html_content, imageXpath, output_path):
    '''
    Extracts image URLs from the provided HTML content using the given XPath.
    '''
    parser = html.HTMLParser()
    tree = html.fromstring(html_content, parser=parser)
    hrefs = tree.xpath(imageXpath)

    # Ignore the first element in the list and keep the rest
    list_imageURLs = hrefs[1:]  # Ignoring the first href


    if output_path == "defaultlocationpreference":

      # name of the album.
      is_album_name = tree.xpath('//meta[@property="og:title"]/@content')
      if is_album_name:
        album_name = str(is_album_name[0]) + ".zip"
      else:
        album_name = "Compressed_GoogleAlbum.zip"

    else:
      # Use designated output_path
      album_name = output_path
    # Returning the hrefs.
    return list_imageURLs, album_name


#--------------------------------------------


def get_all_image_urls(driver, imageXpath, scroll_pause_time, output_path):
    '''
    Extracts all image URLs by scrolling to the bottom of the page using PAGE_DOWN key.
    Stops when no new URLs are found between consecutive scrolls.
    '''
    all_image_urls = set()  # To store unique image URLs
    previous_last_url = None  # Track the last URL from the previous scroll

    #print("Starting to scroll and extract image URLs.:")

    while True:
        # Extract image URLs from the current page source
        html_content = driver.page_source
        new_image_urls, output_path = extract_image_urls(html_content, imageXpath, output_path)
        print(f"Found {len(new_image_urls)} new image URLs.")
        all_image_urls.update(new_image_urls)  # Add new URLs to the set


        # Get the last URL from the current set of image URLs
        current_last_url = None
        if new_image_urls:
            current_last_url = list(new_image_urls)[-1]  # Get the last URL

        # Check if the last URL has not changed
        if current_last_url == previous_last_url:
            print("No new URLs found. Reached the end of the page.")
            break

        # Update the previous last URL
        previous_last_url = current_last_url

        # Scroll down using PAGE_DOWN key
        body_element = driver.find_element(By.TAG_NAME, "body")
        body_element.send_keys(Keys.PAGE_DOWN)
        time.sleep(scroll_pause_time)


    print(f"Total unique image URLs extracted: {len(all_image_urls)}")
    return list(all_image_urls), output_path


#--------------------------------------------


# Function to fetch downloadable image URLs
def downloadable_image_url(image_url, url_prefix):
    '''
    This downloads the full resolution image from the Google photos individual image URL.
    Parameters - image URL
    Returns - Direct downloadable image URL.
    '''
    url = url_prefix + image_url
    response = requests.get(url)
    response.raise_for_status()
    tree = html.fromstring(response.content)
    script_contents = tree.xpath('//script[@class]/text()')
    list_image_urls = []

    image_url_pattern = r'(https:\/\/lh3\.googleusercontent\.com\/pw\/[-\w]+)'
    if script_contents:
        for content in script_contents:
            urls = re.findall(image_url_pattern, content)
            list_image_urls.extend(urls)

    return str(list_image_urls[0]) + "=s0-d-ip"


#--------------------------------------------


# Function to compress images with PIL and add original metadata.
def compress_image_PIL_with_metadata(image_url):
  '''
  Compress + Obtain real file name of an image using Pillow with a specified compression quality, overwriting existing metadata, and optionally saving without metadata.

  Args:
    image_url: URL to the input image.
    output_path: Path to save the compressed image.
    save_with_metadata (bool, optional): Whether to save the image with the provided metadata (default: True).

  Returns:
    Compressed image as BytesIO object,
    Original filename.
  '''

  # Send a GET request to the image URL
  # response = requests.get(image_url, allow_redirects=True)
  # response.raise_for_status()  # Ensure the request was successful

  # Send a GET request to the image URL
  try:
      response = requests.get(image_url, allow_redirects=True)
      response.raise_for_status()  # Ensure the request was successful
  except requests.exceptions.RequestException as e:
      print(f"Error downloading image: {e}")
      return None, None  # Return None if download fails

  #_________________

  # Obtaining the filename from the https requests.
  content_disposition = response.headers.get('content-disposition')

  # Proceeding if it exists.
  if content_disposition:
    # Content-Disposition: attachment; filename="example.jpg"
    filename = content_disposition.split('filename=')[-1].strip('"')

    # Conditionally processing only jpegs, further support for other formats will be added in the future.
    file_extension = filename.split(".")[-1]
  else:
    filename =  None

  if filename is None:
    # Fallback to URL-based filename extraction
    parsed_url = urlparse(image_url)
    filename = os.path.basename(parsed_url.path)

  #print(image_url)

  #_________________

  # Only process JPEG/JPG files
  if file_extension in ['jpg', 'jpeg']:

    # Obtain image as bytes in memory
    img_file_bytes = BytesIO(response.content)

    # Load the image into PIL from the response content
    image = Image.open(img_file_bytes)

    try:
        # Load the image into PIL
        image = Image.open(img_file_bytes)
    except OSError as e:
        print(f"Error opening image {filename}: {e}")
        #return None, None  # Return None if the image is corrupted or unsupported
        return img_file_bytes, filename

    # Handle images with transparency (e.g., PNG) by filling the alpha channel with a background color
    if image.mode == 'RGBA':
        # If the image has transparency (RGBA), fill it with white (or any other color)
        background = Image.new("RGB", image.size, (255, 255, 255))  # White background
        background.paste(image, (0, 0), image)  # Paste the image on top of the background
        img = background
    else:
        # Try converting to RGB if not already in RGB mode
        try:
            img = image.convert('RGB')
        except Exception as e:
            print(f"Error converting image {filename}: {e}")
            #return None, None  # Skip this image if conversion fails
            return img, filename

    # Initiating the variable
    compressed_img_bytes = BytesIO()

    # extracting the exif or metadata info.
    # exif = img.info['exif']

    if 'exif' in img.info:
      exif = img.info['exif']
      img.save(compressed_img_bytes, format="JPEG", quality=40, optimize=True, exif = exif)

    else:
      img.save(compressed_img_bytes, format="JPEG", quality=40, optimize=True)


    # Apply compression with a customizable quality parameter (adjust as needed)
    #img.save(output_path, quality=40, format='JPEG', optimize=True, exif = exif)

    # Apply compression with a customizable quality parameter (adjust as needed)
    # Store as bytes in memory.
    #compressed_img_bytes = BytesIO()
    #img.save(compressed_img_bytes, format="JPEG", quality=40, optimize=True, exif = exif)

    # Return compressed_img_bytes, filenme..
    return compressed_img_bytes, filename

  # else, print the filename and reason. In future, this will be added as a txt file to the zip.
  else:
    print("Skipped non-JPEG/ non-JPG file: ", str(filename))
    return BytesIO(response.content), filename



#--------------------------------------------


def zip_output(dict_compressedImages, output_path):
  '''
  Takes the dictionary of compressed images and the output_path and returns a zip file of the images.
  '''

  # Prepare ZIP file
  with zipfile.ZipFile(output_path, 'w') as zipf:
    # Loop and Write the images to the ZIP file.
    for filename, compressedimagebytes in dict_compressedImages.items():
      zipf.writestr(filename, compressedimagebytes.getvalue())


#--------------------------------------------



# Main function
def compress_GoogleAlbum_jpeg(Gphotos_url, scroll_pause_time = 0.5,  isHeadless = True, imageXpath = '//a[@tabindex="0"]/@href', url_prefix="https://photos.google.com/", output_path = "defaultlocationpreference", window_height="1080", window_width="1920", scalefactor = "0.70", headless_scalefactor = "0.3", headless_height = "19900", headless_width = "2400"):
    """
    Compresses images from a Google Photos album.

    This function automates the process of accessing a Google Photos album, extracting image URLs, 
    and compressing the images before packaging them into a zip file.

    Parameters:
        Gphotos_url (str): URL of the Google Photos album.
        scroll_pause_time (float, optional): Time to pause during scrolling for dynamic loading (default: 0.5).
        isHeadless (bool, optional): Whether to run the browser in headless mode (default: True).
        imageXpath (str, optional): XPath expression to locate image URLs (default: '//a[@tabindex="0"]/@href').
        url_prefix (str, optional): Prefix for image URLs (default: 'https://photos.google.com/').
        output_path (str, optional): Path where compressed images will be saved (default: 'defaultlocationpreference').
        window_height (str, optional): Browser window height in pixels (default: '1080').
        window_width (str, optional): Browser window width in pixels (default: '1920').
        scalefactor (str, optional): Scaling factor for images in normal mode (default: '0.70').
        headless_scalefactor (str, optional): Scaling factor for images in headless mode (default: '0.3').
        headless_height (str, optional): Browser height in pixels when in headless mode (default: '19900').
        headless_width (str, optional): Browser width in pixels when in headless mode (default: '2400').

    Returns:
        Produces a zip file with the compressed images.

    The function navigates to the specified Google Photos URL, extracts image URLs, compresses the images,
    and saves the compressed versions as a zip file. The Selenium WebDriver is closed at the end.
    """

    # example_url = "https://photos.google.com/u/4/share/AF1QipMtsII2o4GodHuQTYVSXJ4VgnK4KOo2GZbyR_akkytKmOsm8euQuxfgap87Ski_QQ?key=bW0tZl9hV3hWcncwYWQyVmJiRC1uVUJlaXFRQ2hR"

    # Launch the browser with the user profile.
    driver = open_browser_with_profile_and_navigate(Gphotos_url, isHeadless = isHeadless, scalefactor = scalefactor, window_height=window_height, window_width=window_width, headless_scalefactor = headless_scalefactor, headless_height = headless_height, headless_width = headless_width)

    # Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[@tabindex="0"]'))
    )

    # Extract all image URLs
    all_image_urls, output_path = get_all_image_urls(driver, imageXpath = imageXpath, scroll_pause_time = scroll_pause_time, output_path = output_path)

    # Ensure no duplicates in the URLs
    # unique_image_urls = list(set(all_image_urls))  # Remove duplicates just in case
    list_image_urls = list(set(all_image_urls))

    print(f"Extracted {len(list_image_urls)} unique image URLs.")

    # for url in unique_image_urls:
    #   print(downloadable_image_url(image_url=url, url_prefix = url_prefix))

    # Intiating an empty list, empty dict.
    # list_image_urls = []
    dict_compressedImages = {}

    # # Extracting the list of individual image urls.
    # list_image_urls, output_path = extract_image_urls(googleAlbumURL, imageXpath=imageXpath, output_path = output_path)

    # Using for loop to loop through the album.
    for image_url in tqdm(list_image_urls, desc = "Compressing Images"):

      # Intiating an empty string.
      download_url = ''

      # Obtaining the downloadable image url.
      download_url = downloadable_image_url(image_url, url_prefix = url_prefix)

      # Compressing the image in the download_url and obtaining the output.
      # Return compressed_image as BytesIO object, file name.
      compressed_image, file_name = compress_image_PIL_with_metadata(download_url)

      # Adding the returned variables to a dictionary -> Key = file_name , Value = Compressed image as ByteIO object.
      dict_compressedImages[file_name] = compressed_image


    zip_output(dict_compressedImages, output_path)

    # Close the driver
    driver.quit()

