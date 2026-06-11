import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

class WebScraper:
    """Handles web scraping and content extraction"""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def get_page_content(self, url: str) -> dict:
        """
        Fetch and parse a web page
        
        Args:
            url: URL to scrape
            
        Returns:
            dict with status and page content
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.title.string if soup.title else "No title found"
            
            # Extract main content
            paragraphs = [p.get_text() for p in soup.find_all('p')]
            content = "\n".join(paragraphs[:10])  # First 10 paragraphs
            
            return {
                "status": "success",
                "title": title,
                "content": content,
                "url": url
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to scrape page: {str(e)}"
            }
    
    def extract_links(self, url: str) -> dict:
        """Extract all links from a page"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            links = [
                {
                    "text": link.get_text(),
                    "href": link.get("href")
                }
                for link in soup.find_all('a', href=True)
            ]
            
            return {
                "status": "success",
                "links": links,
                "total": len(links)
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to extract links: {str(e)}"
            }
    
    def get_video_info(self, url: str) -> dict:
        """
        Get information about a video (YouTube, etc.)
        
        Args:
            url: URL of the video
            
        Returns:
            dict with video info
        """
        try:
            import yt_dlp
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    "status": "success",
                    "title": info.get('title'),
                    "duration": info.get('duration'),
                    "uploader": info.get('uploader'),
                    "view_count": info.get('view_count'),
                    "description": info.get('description'),
                }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get video info: {str(e)}"
            }
    
    def summarize_content(self, content: str, max_sentences: int = 5) -> str:
        """
        Create a simple summary by extracting key sentences
        
        Args:
            content: Text content to summarize
            max_sentences: Maximum sentences in summary
            
        Returns:
            Summary text
        """
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', content)
        
        # Return first N sentences
        summary = " ".join(sentences[:max_sentences])
        return summary
    
    def search_web(self, query: str) -> dict:
        """
        Perform a basic web search (returns page snippets)
        
        Args:
            query: Search query
            
        Returns:
            dict with search results
        """
        try:
            # Using a simple approach with requests
            search_url = f"https://www.google.com/search?q={query}"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract search results
            results = []
            for g in soup.find_all('div', class_='g'):
                title = g.find('h3')
                link = g.find('a')
                snippet = g.find('span', class_='st')
                
                if title and link:
                    results.append({
                        "title": title.get_text(),
                        "link": link.get('href'),
                        "snippet": snippet.get_text() if snippet else "No snippet"
                    })
            
            return {
                "status": "success",
                "results": results[:5],  # Return top 5
                "query": query
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to perform search: {str(e)}"
            }
