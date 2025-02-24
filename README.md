# GStoPDF
Batch Search and Download Script for Scientific Articles from Google Scholar

Functionality:
* Performs keyword-based searches on Google Scholar, allowing users to specify the number of pages to search (as Google Scholar displays only 10 articles per page).
* If a direct PDF link is available, the script downloads the article directly from Google Scholar.
* If no PDF link is found or the link is broken, the script queries Sci-Hub by searching for the article title and downloads the file using scidownl.
* For each search query, a dedicated folder is created, containing:
  * All downloaded PDF files, named in a structured format (article title, author name, journal, and year).
  * Two text files:
    * A reference list with links to the sources from which the articles were downloaded.
    * A list of articles that could not be downloaded, allowing for manual retrieval.

# Batch Downloading Process:
Depending on the number of search pages specified, the script automates bulk downloading. For example, if set to 10 pages, it should retrieve up to 100 articles, organizing them neatly into a folder named after the search query, with an almost-ready bibliography inside.

This tool would have been incredibly useful during my PhD years! 🚀

# Installation and Execution Guide (Windows)
Step 1: Install Python
  Ensure that Python 3 is installed on your system. If not, download and install it from the official [Python website](https://www.python.org/downloads/). [Instruction](https://phoenixnap.com/kb/how-to-install-python-3-windows).

Step 2: Create a Virtual Environment
  Open a terminal (PowerShell or Command Prompt) and run the following commands to create a virtual environment in the root of drive C:
  ```
  cd C:\
  python -m venv Google_Scholar_PDF_Downloader_venv
  ```

Step 3: Activate the Virtual Environment
  Run the following command to activate the virtual environment:
  ```
  C:\Google_Scholar_PDF_Downloader_venv\Scripts\Activate.ps1
  ```
  (If you encounter a security restriction, you may need to enable script execution by running:
  `Set-ExecutionPolicy Unrestricted -Scope Process`
  before activating the environment.)

Step 4: Install Required Libraries
  Once the virtual environment is activated, install the necessary dependencies:
  ```
  pip install requests beautifulsoup4 scidownl
  ```

Step 5: Place the Script and Run It
  Move the script getPDF_from_GS_scihub.py into the Google_Scholar_PDF_Downloader_venv folder.
  Navigate to the folder and run the script:
  ```
  cd C:\Google_Scholar_PDF_Downloader_venv
  python getPDF_from_GS_scihub.py
  ```
Step 6: Provide Search Parameters
  The script will prompt you to enter:
    * A search query
    * The number of pages to search (each page contains 10 articles)
  Example input:
    ```
    Enter search query: rucklidge chaos  
    Enter number of pages to search: 10
    ```
    
Step 7: Locate Downloaded Files
  All downloaded articles will be stored in a dedicated folder named after the search query. For the example above, the files will be located in:
  ```
  C:\Google_Scholar_PDF_Downloader_venv\rucklidge chaos PDFs
  ```
  A separate folder will be created for each search query.







