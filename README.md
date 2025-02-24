# GStoPDF
Batch Search and Download Script for Scientific Articles from Google Scholar
![image](https://github.com/user-attachments/assets/5ef3eeb9-12d1-49e0-bd5c-89ca2419c6db)

Functionality:
* Performs keyword-based searches on Google Scholar, allowing users to specify the number of pages to search (as Google Scholar displays only 10 articles per page).
* If a direct PDF link is available, the script downloads the article directly from Google Scholar.
* If no PDF link is found or the link is broken, the script queries Sci-Hub by searching for the article title and downloads the file using scidownl.
* For each search query, a dedicated folder is created, containing:
  * All downloaded PDF files, named in a structured format (article title, author name, journal, and year).
  * Two text files:
    * A reference list with links to the sources from which the articles were downloaded (literature.txt).
    * A list of articles that could not be downloaded, allowing for manual retrieval (literature_errors.txt).
* Automaticly opens folder with search results
* Synchronizes files and a reference list in the same folder under new search conditions (expanding the number of pages for analysis, using VPN to access blocked sites). Thus, only new files will be downloaded and added to reference list. If, under new conditions, it was possible to download previously inaccessible file - it will be deleted from literature_errors.txt list.

# Batch Downloading Process:
Depending on the number of search pages specified, the script automates bulk downloading. For example, if set to 10 pages, it should retrieve up to 100 articles, organizing them neatly into a folder named after the search query, with an almost-ready bibliography inside.
![image](https://github.com/user-attachments/assets/6b7526f5-75b9-4c2b-87f1-2fdf17cebf19)

This tool would have been incredibly useful during my PhD years! 🚀

# Installation and Execution Guide (Windows)
## Step 1: Install Python.

Ensure that Python 3 is installed on your system. If not, download and install it from the official [Python website](https://www.python.org/downloads/). [Instruction](https://phoenixnap.com/kb/how-to-install-python-3-windows).

## Step 2: Create a Virtual Environment

  Open a terminal (PowerShell or Command Prompt) and run the following commands to create a virtual environment in the root of drive C:
  ```
  cd C:\
  python -m venv Google_Scholar_PDF_Downloader_venv
  ```

## Step 3: Activate the Virtual Environment

  Run the following command to activate the virtual environment:
  ```
  C:\Google_Scholar_PDF_Downloader_venv\Scripts\Activate.ps1
  ```
  (If you encounter a security restriction, you may need to enable script execution by running:
  `Set-ExecutionPolicy Unrestricted -Scope Process`
  before activating the environment.)
![image](https://github.com/user-attachments/assets/6374c78a-9224-40bc-95cb-51975e1434e6)

## Step 4: Install Required Libraries

  Once the virtual environment is activated, install the necessary dependencies:
  ```
  pip install requests beautifulsoup4 scidownl
  ```

## Step 5: Place the Script and Run It

  Move the script GStoPDF.py into the Google_Scholar_PDF_Downloader_venv folder.
  Navigate to the folder and run the script:
  ```
  cd C:\Google_Scholar_PDF_Downloader_venv
  python GStoPDF.py
  ```
## Step 6: Provide Search Parameters

The script will prompt you to enter:
* A search query
* The number of pages to search (each page contains 10 articles)

Example input:
```
Enter search query: machine learning
Enter number of pages to search: 5
```
![image](https://github.com/user-attachments/assets/006684a7-9717-4559-9670-c1d0877296b1)

## Step 7: Locate Downloaded Files

  All downloaded articles will be stored in a dedicated folder named after the search query. For the example above, the files will be located in:
  ```
  C:\Google_Scholar_PDF_Downloader_venv\chaos generator PDFs
  ```
![image](https://github.com/user-attachments/assets/f3ae80d7-e2ea-464f-8534-87c3666b3b81)

  A separate folder will be created for each unique search query.
  
Reference list and download error file list:
![image](https://github.com/user-attachments/assets/4b32894a-5c87-4683-95b1-5568847590d6)







