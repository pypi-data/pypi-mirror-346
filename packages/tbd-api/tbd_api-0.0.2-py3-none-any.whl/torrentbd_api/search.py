from bs4 import BeautifulSoup
from .login import session, headers, check_login_status, login

def search_torrents(query: str, page: int = 1):
    if not check_login_status():
        login()

    url = "https://www.torrentbd.net/ajsearch.php"
    data = {
        "page": str(page),
        "kuddus_searchtype": "torrents",
        "kuddus_searchkey": query,
        "searchParams[sortBy]": "",
        "searchParams[secondary_filters_extended]": ""
    }

    try:
        response = session.post(url, headers=headers, data=data)
        response.raise_for_status()

        return parse_torrents_from_html(response.text)

    except Exception as e:
        # Return error in the same structure as success
        return {
            "torrents": [],
            "metadata": {
                "total_results": 0,
                "total_pages": 0,
                "error": str(e)
            }
        }

def parse_torrents_from_html(html: str):
    try:
        soup = BeautifulSoup(html, "html.parser")
        results = []
        
        # Base URL for constructing full links
        base_url = "https://www.torrentbd.net/"
        
        # Get total results count if available
        results_counter = soup.find("h6", class_="kuddus-results-counter")
        total_results = None
        if results_counter:
            counter_text = results_counter.get_text(strip=True)
            import re
            count_match = re.search(r'(\d+)', counter_text)
            if count_match:
                total_results = int(count_match.group(1))
        
        # Extract pagination info
        pagination = soup.find("div", class_="pagination-block")
        total_pages = None
        if pagination:
            pages = pagination.find_all("li", class_="aj-paginator")
            if pages:
                # Find the last page number
                page_numbers = [int(page.get_text(strip=True)) for page in pages if page.get_text(strip=True).isdigit()]
                if page_numbers:
                    total_pages = max(page_numbers)

        torrents = soup.find_all("tr")

        for torrent in torrents:
            try:
                # Skip rows without title
                title_tag = torrent.find("a", class_="ttorr-title")
                if not title_tag:
                    continue

                # Extract title and link
                title = title_tag.text.strip()
                link = title_tag.get('href', '').strip()
                if link and not link.startswith("http"):
                    link = base_url + link
                
                # Extract torrent ID from the link
                torrent_id = None
                if link:
                    import re
                    id_match = re.search(r'id=(\d+)', link)
                    if id_match:
                        torrent_id = id_match.group(1)
                
                # Extract download link
                download_link = None
                download_tag = torrent.find("a", href=lambda h: h and h.startswith("download.php"))
                if download_tag:
                    download_link = download_tag.get('href', '').strip()
                    if download_link and not download_link.startswith("http"):
                        download_link = base_url + download_link
                
                # Extract category
                category_img = torrent.find("img", class_="cat-pic-img")
                category = category_img.get('title', '') if category_img else "Unknown"
                
                # Check if it's a freeleech torrent
                is_freeleech = bool(torrent.find("img", class_="rel-icon", title=lambda t: t and "FreeLeech" in t))
                
                # Extract size
                size_tag = torrent.find("div", class_="blue100")
                size = size_tag.get_text(strip=True) if size_tag else "N/A"
                size = size.replace("insert_drive_file", "").strip()

                # Extract uploader information
                uploaded_by_div = torrent.find("div", class_="uploaded-by")
                uploaded_by = "Unknown"
                upload_time = "Unknown"
                
                if uploaded_by_div:
                    # Check if it's an anonymous upload
                    if "Anonymous" in uploaded_by_div.get_text():
                        uploaded_by = "Anonymous"
                    else:
                        uploader_tag = uploaded_by_div.find("a")
                        if uploader_tag and uploader_tag.find("span"):
                            uploaded_by = uploader_tag.find("span").get_text(strip=True)
                    
                    # Extract upload time
                    time_span = uploaded_by_div.find("span", title=lambda t: t and any(x in t for x in ["PM", "AM"]))
                    if time_span:
                        upload_time = time_span.get_text(strip=True)

                # Extract seeders, leechers, and completed counts from the stats div
                seeders = "0"
                leechers = "0"
                completed = "0"
                
                # First approach: Try finding the stats divs and extract their content more carefully
                try:
                    seeders_tag = torrent.find("div", class_="thc seed")
                    if seeders_tag:
                        # Try multiple approaches to extract the number
                        icon = seeders_tag.find("i", class_="material-icons")
                        if icon:
                            # Get the text that comes after the icon
                            if icon.next_sibling:
                                seeders = icon.next_sibling.strip()
                            # If that didn't work, try the full text
                            if not seeders or seeders == "0":
                                seeders_text = seeders_tag.get_text(strip=True)
                                # Remove known icon text and get remaining digits
                                seeders_text = seeders_text.replace("file_upload", "").strip()
                                if seeders_text:
                                    seeders = ''.join(filter(str.isdigit, seeders_text)) or "0"
                    
                    leechers_tag = torrent.find("div", class_="thc leech")
                    if leechers_tag:
                        icon = leechers_tag.find("i", class_="material-icons")
                        if icon:
                            # Get the text that comes after the icon
                            if icon.next_sibling:
                                leechers = icon.next_sibling.strip()
                            # If that didn't work, try the full text
                            if not leechers or leechers == "0":
                                leechers_text = leechers_tag.get_text(strip=True)
                                # Remove known icon text and get remaining digits
                                leechers_text = leechers_text.replace("file_download", "").strip()
                                if leechers_text:
                                    leechers = ''.join(filter(str.isdigit, leechers_text)) or "0"
                    
                    completed_tag = torrent.find("div", class_="thc completed")
                    if completed_tag:
                        icon = completed_tag.find("i", class_="material-icons")
                        if icon:
                            # Get the text that comes after the icon
                            if icon.next_sibling:
                                completed = icon.next_sibling.strip()
                            # If that didn't work, try the full text
                            if not completed or completed == "0":
                                completed_text = completed_tag.get_text(strip=True)
                                # Remove known icon text and get remaining digits
                                completed_text = completed_text.replace("done_all", "").strip()
                                if completed_text:
                                    completed = ''.join(filter(str.isdigit, completed_text)) or "0"
                except (AttributeError, TypeError) as e:
                    # Continue to the next approach if there's an error
                    pass
                
                # Second approach: Look for the structured pattern in the HTML
                if seeders == "0" and leechers == "0" and completed == "0":
                    try:
                        # Use a safer approach to find the container
                        # First, find all divs that might contain our stats
                        potential_containers = torrent.find_all("div")
                        stats_container = None
                        
                        # Check each potential container for thc class divs
                        for container in potential_containers:
                            try:
                                if container.find_all("div", class_="thc", recursive=False):
                                    stats_container = container
                                    break
                            except AttributeError:
                                # Skip if container is not a valid BS element
                                continue
                        
                        if stats_container:
                            # Get all the thc divs in order
                            thc_divs = stats_container.find_all("div", class_="thc")
                            if len(thc_divs) >= 3:
                                # Extract text from each div
                                seeders_text = thc_divs[0].get_text(strip=True)
                                seeders = ''.join(filter(str.isdigit, seeders_text)) or "0"
                                
                                leechers_text = thc_divs[1].get_text(strip=True)
                                leechers = ''.join(filter(str.isdigit, leechers_text)) or "0"
                                
                                completed_text = thc_divs[2].get_text(strip=True)
                                completed = ''.join(filter(str.isdigit, completed_text)) or "0"
                    except (IndexError, AttributeError) as e:
                        # Silently continue if there's an error
                        pass
                
                # Third approach: Use regex to extract numbers following specific patterns
                if seeders == "0" and leechers == "0" and completed == "0":
                    try:
                        # Get the full HTML of the row
                        row_html = str(torrent)
                        import re
                        
                        # Look for patterns like "file_upload</i> 5" or similar
                        seeders_match = re.search(r'file_upload[^>]*>\s*(\d+)', row_html)
                        if seeders_match:
                            seeders = seeders_match.group(1)
                            
                        leechers_match = re.search(r'file_download[^>]*>\s*(\d+)', row_html)
                        if leechers_match:
                            leechers = leechers_match.group(1)
                            
                        completed_match = re.search(r'done_all[^>]*>\s*(\d+)', row_html)
                        if completed_match:
                            completed = completed_match.group(1)
                    except Exception:
                        # Skip if there's any error during regex matching
                        pass
                                        
                # Convert to integers, defaulting to 0 if conversion fails
                try:
                    seeders = int(seeders)
                except (ValueError, TypeError):
                    seeders = 0
                    
                try:
                    leechers = int(leechers)
                except (ValueError, TypeError):
                    leechers = 0
                    
                try:
                    completed = int(completed)
                except (ValueError, TypeError):
                    completed = 0

                results.append({
                    "title": title,
                    "torrent_id": torrent_id,
                    "link": link,
                    "download_link": download_link,
                    "category": category,
                    "size": size,
                    "uploaded_by": uploaded_by,
                    "upload_time": upload_time,
                    "seeders": seeders,
                    "leechers": leechers,
                    "completed": completed,
                    "freeleech": is_freeleech
                })
            except Exception as e:
                # If processing a single torrent fails, continue with the rest
                continue

        # Return the result in a structured format
        return {
            "torrents": results,
            "metadata": {
                "total_results": total_results,
                "total_pages": total_pages
            }
        }
    except Exception as e:
        # If the entire parsing fails, return an error
        return {
            "torrents": [],
            "metadata": {
                "total_results": 0,
                "total_pages": 0,
                "error": f"Error parsing search results: {str(e)}"
            }
        }