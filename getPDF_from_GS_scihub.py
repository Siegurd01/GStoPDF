import requests
from bs4 import BeautifulSoup
import time
import random
import os
import re
import subprocess

def sanitize_filename(filename):
    """Sanitize filenames by removing invalid characters and unwanted text like [PDF]."""
    filename = re.sub(r'\[PDF\]+', '', filename)  # Remove [PDF], [PDF][PDF], etc.
    filename = re.sub(r'\[HTML\]+', '', filename)  # Remove HTML, etc.
    filename = re.sub(r'\[CITATION]+', '', filename)  # Remove [CITATION], etc.
    filename = re.sub(r'\[C]+', '', filename)  # Remove [C], etc.
    filename = re.sub(r'\[BOOK]+', '', filename)  # Remove [BOOK], etc.
    filename = re.sub(r'\[B]+', '', filename)  # Remove [B], etc.
   
    return re.sub(r'[<>:"/\\|?*]', '', filename).strip()

def sanitize_folder_name(folder_name):
    """Sanitize the folder name to remove invalid characters."""
    return re.sub(r'[<>:"/\\|?*]', '_', folder_name).strip()

def download_pdf(pdf_url, title, authors, folder, literature_file, error_file):
    """Download a PDF from a given URL and save it with a sanitized title including authors."""
    filename = sanitize_filename(f"{title} - {authors}") + ".pdf"
    filepath = os.path.join(folder, filename)
    
    os.makedirs(folder, exist_ok=True)  # Ensure the folder exists

    try:
        response = requests.get(pdf_url, stream=True, timeout=10)
        if response.status_code == 200:
            with open(filepath, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Downloaded: {filename}")

            # Log success in literature.txt
            with open(literature_file, "a", encoding="utf-8") as lf:
                lf.write(f"{filename} | {pdf_url}\n")
            return True  # Download successful
        else:
            raise Exception(f"Status code {response.status_code}")
    except Exception as e:
        print(f"Error downloading from Google Scholar {title}: {e}")
        return False  # Download failed

def download_with_scidownl(title, authors, folder, literature_file, error_file):
    """Try downloading the paper with SciDownl if no direct PDF link is available."""
    filename = sanitize_filename(f"{title} - {authors}") + ".pdf"
    filepath = os.path.join(folder, filename)
    
    try:
        print(f"Trying to download '{title}' with SciDownl...")
        result = subprocess.run(
            ["scidownl", "download", "--title", title, "--out", filepath],
            capture_output=True,
            text=True
        )

        if result.returncode == 0 and os.path.exists(filepath):
            print(f"SciDownl download successful: {filepath}")
            with open(literature_file, "a", encoding="utf-8") as lf:
                lf.write(f"{filename} | SciDownl\n")
        else:
            print(f"SciDownl failed for: {title}")
            with open(error_file, "a", encoding="utf-8") as ef:
                ef.write(f"{title} | {authors} | SciDownl failed\n")
    except Exception as e:
        print(f"Error running SciDownl: {e}")
        with open(error_file, "a", encoding="utf-8") as ef:
            ef.write(f"{title} | {authors} | SciDownl error: {e}\n")

def parse_results(html):
    """Parse Google Scholar HTML results for titles, authors, and PDF links."""
    soup = BeautifulSoup(html, "html.parser")
    results = []
    
    for result in soup.find_all("div", class_="gs_r gs_or gs_scl"):
        title_tag = result.find("h3", class_="gs_rt")
        title = title_tag.get_text() if title_tag else "No title found"
        title = sanitize_filename(title)  # Clean title

        pdf_link = None
        pdf_div = result.find("div", class_="gs_or_ggsm")
        if pdf_div and pdf_div.find("a"):
            link_href = pdf_div.find("a").get("href", "")
            #if link_href.endswith(".pdf"):
            pdf_link = link_href

        # Extracting authors from the citation line
        citation_tag = result.find("div", class_="gs_a")
        authors = citation_tag.get_text().split(" - ")[0] if citation_tag else "Unknown authors"

        results.append({
            "title": title,
            "pdf_link": pdf_link,
            "authors": authors
        })
    
    return results

def main():
    search_query = input("Enter search query: ").strip()
    try:
        num_pages = int(input("Enter number of pages to search: "))
    except ValueError:
        print("Invalid number of pages.")
        return

    # Create search-specific folder
    folder_name = sanitize_folder_name(search_query)
    folder_path = os.path.join(os.getcwd(), folder_name + " PDFs")
    os.makedirs(folder_path, exist_ok=True)

    # Define literature files inside this folder
    literature_file = os.path.join(folder_path, "literature.txt")
    error_file = os.path.join(folder_path, "literature_errors.txt")

    # Clear or create literature files before starting
    open(literature_file, "w", encoding="utf-8").close()
    open(error_file, "w", encoding="utf-8").close()

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36"
    })

    BASE_URL = 'https://scholar.google.com/scholar'
    all_results = []

    for page_num in range(num_pages):
        print(f"Processing page {page_num + 1}/{num_pages}")
        params = {
            'start': page_num * 10,
            'q': search_query,
            'hl': 'en',
            'as_sdt': '0,5'
        }

        time.sleep(random.uniform(1, 3))  # Random delay to avoid blocking
        response = session.get(BASE_URL, params=params)
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code} for page {page_num + 1}")
            continue

        page_results = parse_results(response.text)
        all_results.extend(page_results)

    # Process results
    fileno = 0
    for item in all_results:
        fileno=fileno+1;
        print(f"Processing file {fileno}/{num_pages*10}")
        print("\nTitle:", item["title"])
        print("Authors:", item["authors"])

        if item["pdf_link"]:
            print("PDF Link:", item["pdf_link"])
            success = download_pdf(item["pdf_link"], item["title"], item["authors"], folder_path, literature_file, error_file)
            if not success:
                download_with_scidownl(item["title"], item["authors"], folder_path, literature_file, error_file)
        else:
            print("No PDF link found on Google Scholar, trying SciDownl...")
            download_with_scidownl(item["title"], item["authors"], folder_path, literature_file, error_file)
        
        print("-" * 70)

if __name__ == "__main__":
    main()
