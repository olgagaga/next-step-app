#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import json

with open('config/uk.json', 'r') as f:
    CONFIG = json.load(f)

def fetch_and_print():
    print("🚀 Starting scraper in test mode - printing data instead of saving to database")
    print("=" * 80)
    
    for i, src in enumerate(CONFIG["updates"], 1):
        src_id = i  # Generate ID since config doesn't have one
        url = src['url']
        sel = src['selector']
        link_sel = src['link_selector']
        title_sel = src['title_selector']
        sub_sel = src['subtitle_selector']
        date_sel = src['date_selector']
        
        print(f"\n🔍 Scraping source: {url}")
        print(f"   Label: {src.get('label', 'No label')}")
        print(f"   Selector: {sel}")
        print(f"   Link selector: {link_sel}")
        print(f"   Title selector: {title_sel}")
        print(f"   Subtitle selector: {sub_sel}")
        print(f"   Date selector: {date_sel}")
        print("-" * 60)
        
        # Skip if essential selectors are missing
        if not sel or not link_sel or not title_sel:
            print("⚠️  Skipping source - missing essential selectors")
            continue
        
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, 'html.parser')

            items = soup.select(sel)
            print(f"📊 Found {len(items)} items matching selector '{sel}'")
            
            scraped_count = 0
            for i, item in enumerate(items, 1):
                print(f"\n--- Item {i} ---")
                
                # Try to find link
                a_tag = item.select_one(link_sel)
                if not a_tag or not a_tag.get('href'):
                    print("❌ No link found, skipping...")
                    continue

                article_url = urljoin(url, a_tag['href'])
                print(f"🔗 URL: {article_url}")
                
                # Try to find title
                title_tag = item.select_one(title_sel)
                title = title_tag.get_text(strip=True) if title_tag else 'No title found'
                print(f"📰 Title: {title}")
                
                # Try to find subtitle
                subtitle_tag = item.select_one(sub_sel) if sub_sel else None
                subtitle = subtitle_tag.get_text(strip=True) if subtitle_tag else 'No subtitle'
                print(f"📝 Subtitle: {subtitle}")
                
                # Try to find date
                date_tag = item.select_one(date_sel) if date_sel else None
                date_str = date_tag.get_text(strip=True) if date_tag else 'No date'
                print(f"📅 Date: {date_str}")
                
                # Try to parse date
                try:
                    date_published = datetime.fromisoformat(date_str)
                    print(f"✅ Parsed date: {date_published}")
                except Exception as e:
                    print(f"❌ Could not parse date '{date_str}': {e}")
                    date_published = None
                
                scraped_count += 1
                print(f"✅ Successfully scraped article {scraped_count}")
                
                # Limit output for testing - remove this if you want to see all items
                if scraped_count >= 5:
                    print(f"\n⚠️  Limiting output to first 5 articles for testing...")
                    break
            
            print(f"\n📈 Summary for {url}:")
            print(f"   Total items found: {len(items)}")
            print(f"   Successfully scraped: {scraped_count}")
            
        except requests.RequestException as e:
            print(f"❌ Error fetching {url}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error processing {url}: {e}")
    
    print("\n" + "=" * 80)
    print("✅ Scraping test complete!")

if __name__ == "__main__":
    fetch_and_print()
