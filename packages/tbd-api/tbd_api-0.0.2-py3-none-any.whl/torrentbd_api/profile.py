from bs4 import BeautifulSoup
import re
from .login import session, headers, check_login_status, login

def get_user_profile():
    if not check_login_status():
        login()

    url = "https://www.torrentbd.net/account-details.php"
    
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        return {"result": parse_profile_from_html(response.text)}
    except Exception as e:
        return {
            "result": {
                "success": False,
                "error": str(e)
            }
        }

def parse_profile_from_html(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        
        # Check for error page
        error_div = soup.find("div", class_="error")
        if error_div and "Invalid user" in error_div.text:
            return {
                "success": False,
                "error": "Invalid user or not logged in"
            }
        
        # Get profile info from the profile card
        profile_data = {}
        
        # Extract username and rank
        username_span = soup.find("span", class_="tbdrank")
        if username_span:
            profile_data["username"] = username_span.text.strip()
            profile_data["rank"] = username_span.get("class")[1] if len(username_span.get("class", [])) > 1 else "Unknown"
        
        # Find the small element with rank text (more reliable)
        rank_span = soup.find("small", class_="u-rank-text")
        if rank_span:
            profile_data["rank"] = rank_span.text.strip()
        
        # Extract avatar URL - find in card panel
        # profile_data["avatar"] = "https://i.ibb.co/HH1pG8T/wallpaperflare-com-wallpaper-4.jpg"
        
        # Try to extract the avatar from HTML if possible
        avatar_img = soup.find("img", class_="up-avatar")
        if avatar_img and avatar_img.get('data-src-og'):
            avatar_url = avatar_img.get('data-src-og', '')
            if avatar_url and avatar_url != "https://www.torrentbd.net/images/transparent-sq.png":
                profile_data["avatar"] = avatar_url
        
        # Extract values from crc-wrapper divs
        # Find all crc-wrapper divs and extract their data
        crc_wrappers = soup.find_all("div", class_="crc-wrapper")
        for wrapper in crc_wrappers:
            title = wrapper.get("title", "")
            value_div = wrapper.find("div", class_="cr-value")
            if not value_div:
                continue
                
            value = value_div.text.strip()
            
            if "Upload:" in title:
                profile_data["upload"] = value
            elif "Download:" in title:
                profile_data["download"] = value
            elif "Ratio:" in title:
                profile_data["ratio"] = value
            elif "Seedbonus:" in title:
                profile_data["seedbonus"] = value
            elif "Last Seen" in title:
                profile_data["last_seen"] = value
        
        # Extract short links info
        short_links = soup.find_all("div", class_="short-links")
        for link in short_links:
            text = link.text.strip()
            counter = link.find("span", class_="short-link-counter")
            if counter:
                value = counter.text.strip()
                if "Torrent Uploads" in text:
                    profile_data["torrent_uploads"] = value
                elif "Upload Rep" in text:
                    profile_data["upload_rep"] = value
                elif "Forum Rep" in text:
                    profile_data["forum_rep"] = value
        
        # Extract profile stats from table
        profile_info_table = soup.find("table", class_="profile-info-table")
        if profile_info_table:
            rows = profile_info_table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if len(cols) == 2:
                    key = cols[0].text.strip().lower()
                    value = cols[1].text.strip()
                    
                    # Clean up values that have links
                    if cols[1].find("a"):
                        value = cols[1].find("a").text.strip()
                    
                    profile_data[key] = value
        
        # Extract additional user information from card-reveal
        card_reveal = soup.find("div", class_="card-reveal")
        if card_reveal:
            p_tags = card_reveal.find_all("p")
            for p in p_tags:
                if ":" in p.text:
                    key, value = p.text.split(":", 1)
                    profile_data[key.strip().lower()] = value.strip()
        
        # Extract user details from .cr-wrapper divs
        cr_wrappers = soup.find_all("div", class_="cr-wrapper")
        for wrapper in cr_wrappers:
            label_div = wrapper.find("div", class_="cr-label")
            value_div = wrapper.find("div", class_="cr-value")
            
            if not label_div or not value_div:
                continue
                
            key = label_div.text.strip().lower()
            value = value_div.text.strip()
            
            # Clean colon from start of values
            if value.startswith(":"):
                value = value[1:].strip()
                
            # Clean up values that have links
            if value_div.find("a"):
                value = value_div.find("a").text.strip()
                
            profile_data[key] = value
        
        # Extract activity from JavaScript or profile table
        activity_row = soup.find(lambda tag: tag.name == "tr" and tag.find("td") and tag.find("td").text.strip() == "Activity")
        if activity_row:
            activity_td = activity_row.find_all("td")[1]
            if activity_td:
                # Try to extract seeding and leeching from spans
                seeding_span = activity_td.find("span", class_="uc-seeding")
                leeching_span = activity_td.find("span", class_="uc-leeching")
                if seeding_span and leeching_span:
                    # If spans contain ..., look for actual values elsewhere
                    seeding_text = seeding_span.text.strip()
                    leeching_text = leeching_span.text.strip()
                    
                    if seeding_text == "..." or not seeding_text:
                        # Try to find seeding count from elsewhere
                        seeding_a = soup.find(lambda tag: tag.name == "div" and tag.find("div", class_="cr-label") and 
                                             tag.find("div", class_="cr-label").text.strip() == "Seeding now")
                        if seeding_a:
                            seeding_value = seeding_a.find("div", class_="cr-value")
                            if seeding_value and seeding_value.find("a"):
                                seeding_text = seeding_value.find("a").text.strip()
                    
                    # Update the activity data
                    profile_data["seeding"] = seeding_text
                    profile_data["leeching"] = leeching_text
        
        # Formatted response
        formatted_data = {
            "success": True,
            "username": profile_data.get("username", "Unknown"),
            "rank": profile_data.get("rank", "Unknown"),
            "avatar": profile_data.get("avatar", ""),
            "stats": {
                "upload": profile_data.get("upload", "0 B"),
                "download": profile_data.get("download", "0 B"),
                "ratio": profile_data.get("ratio", "0"),
                "seedbonus": profile_data.get("seedbonus", "0"),
                "referrals": profile_data.get("referrals", "0"),
                "fl_tokens": profile_data.get("fl tokens", "0"),
                "last_seen": profile_data.get("last_seen", "Unknown"),
                "torrent_uploads": profile_data.get("torrent_uploads", "0"),
                "upload_rep": profile_data.get("upload_rep", "0"),
                "forum_rep": profile_data.get("forum_rep", "0"),
                "activity": {
                    "seeding": profile_data.get("seeding", "0"),
                    "leeching": profile_data.get("leeching", "0")
                }
            },
            "additional_info": {
                "privacy_level": profile_data.get("privacy level", "Unknown"),
                "ip_address": profile_data.get("ip address", "Unknown"),
                "invited_by": profile_data.get("invited by", "Unknown"),
                "client": profile_data.get("torrent clients", "Unknown"),
                "country": profile_data.get("country", "Unknown"),
                "joined": profile_data.get("joined", "Unknown"),
                "age": profile_data.get("age", "Unknown"),
                "gender": profile_data.get("gender", "Unknown")
            }
        }
        
        # Add seed to go if it exists
        if "seed to go" in profile_data:
            formatted_data["stats"]["seed_to_go"] = profile_data["seed to go"]
        
        # Add seeding now if it exists
        if "seeding now" in profile_data:
            formatted_data["stats"]["seeding_now"] = profile_data["seeding now"]
            
        return formatted_data
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Error parsing profile: {str(e)}"
        }

def extract_number(text, prefix):
    """Extract number after a prefix like ↑ or ↓."""
    try:
        parts = text.split(prefix)
        if len(parts) > 1:
            num_str = ''.join(filter(lambda x: x.isdigit() or x == '.', parts[1].split()[0]))
            return num_str
        return "0"
    except:
        return "0"

