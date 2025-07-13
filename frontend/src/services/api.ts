/**
 * API service for communicating with the FastAPI backend
 */

const API_BASE_URL = 'http://localhost:8000/api/v1';

export interface Article {
  id: number;
  title: string;
  subtitle?: string;
  article_url: string;
  date_published?: string;
  date_fetched: string;
  source_id: number;
  content?: string;
  source?: {
    id: number;
    label: string;
    url: string;
    type: string;
  };
}

export interface Source {
  id: number;
  label: string;
  url: string;
  type: string;
  last_scraped?: string;
}

export interface ArticleListResponse {
  articles: Article[];
  total: number;
  page: number;
  per_page: number;
}

export interface CountryData {
  id: string;
  name: string;
  flag: string;
  description: string;
  lastUpdate: string;
  bannerImage: string;
  updates: string[];
  tags: string[];
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Fetch recent articles for a specific source
   */
  async getRecentArticlesBySource(sourceId: number, limit: number = 3): Promise<Article[]> {
    try {
      const response = await fetch(
        `${this.baseUrl}/articles?source_id=${sourceId}&per_page=${limit}&page=1`
      );
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data: ArticleListResponse = await response.json();
      return data.articles;
    } catch (error) {
      console.error('Error fetching recent articles:', error);
      return [];
    }
  }

  /**
   * Fetch all sources
   */
  async getSources(): Promise<Source[]> {
    try {
      const response = await fetch(`${this.baseUrl}/articles/stats`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      // For now, we'll return a mock since we don't have a sources endpoint yet
      return this.getMockSources();
    } catch (error) {
      console.error('Error fetching sources:', error);
      return this.getMockSources();
    }
  }

  /**
   * Get country data with recent updates
   */
  async getCountryData(countryId: string): Promise<CountryData | null> {
    try {
      // For now, we'll use mock data since we only have UK sources
      // In the future, this could fetch from a countries endpoint
      if (countryId === 'uk') {
        return await this.getUKCountryData();
      }
      
      return null;
    } catch (error) {
      console.error('Error fetching country data:', error);
      return null;
    }
  }

  /**
   * Get UK country data with real articles
   */
  private async getUKCountryData(): Promise<CountryData> {
    try {
      // Get the most recent articles (we'll assume they're from UK sources)
      const response = await fetch(`${this.baseUrl}/articles/recent?limit=3`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const articles: Article[] = await response.json();
      
      // Extract updates from articles
      const updates = articles.map(article => article.title);
      
      // Generate tags from article content
      const tags = this.extractTagsFromArticles(articles);
      
      // Get the most recent date
      const lastUpdate = articles.length > 0 
        ? new Date(articles[0].date_fetched).toISOString().split('T')[0]
        : new Date().toISOString().split('T')[0];

      return {
        id: "uk",
        name: "United Kingdom",
        flag: "🇬🇧",
        description: "Latest immigration updates and policy changes",
        lastUpdate,
        bannerImage: "https://images.unsplash.com/photo-1512734099960-65a682cbfe2b?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8bG9uZG9ufGVufDB8MHwwfHx8Mg%3D%3D",
        updates: updates.length > 0 ? updates : [
          "No recent updates available",
          "Check back later for new immigration news",
          "System is monitoring for updates"
        ],
        tags: tags.length > 0 ? tags : ["Immigration", "Policy", "Updates"]
      };
    } catch (error) {
      console.error('Error fetching UK country data:', error);
      // Return fallback data
      return {
        id: "uk",
        name: "United Kingdom",
        flag: "🇬🇧",
        description: "Latest immigration updates and policy changes",
        lastUpdate: new Date().toISOString().split('T')[0],
        bannerImage: "https://images.unsplash.com/photo-1512734099960-65a682cbfe2b?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8bG9uZG9ufGVufDB8MHwwfHx8Mg%3D%3D",
        updates: [
          "Loading recent updates...",
          "Connecting to immigration news sources",
          "Preparing latest policy information"
        ],
        tags: ["Loading", "Updates", "Policy"]
      };
    }
  }

  /**
   * Extract tags from articles based on common immigration terms
   */
  private extractTagsFromArticles(articles: Article[]): string[] {
    const immigrationTerms = [
      'visa', 'immigration', 'policy', 'brexit', 'student', 'work', 'skilled',
      'family', 'tier', 'points', 'sponsor', 'application', 'processing',
      'requirements', 'changes', 'announcement', 'update', 'guidance'
    ];
    
    const allText = articles.map(article => 
      `${article.title} ${article.subtitle || ''} ${article.content || ''}`
    ).join(' ').toLowerCase();
    
    const foundTags = immigrationTerms.filter(term => 
      allText.includes(term)
    ).slice(0, 3); // Limit to 3 tags
    
    return foundTags.length > 0 ? foundTags : ['Immigration', 'Policy', 'Updates'];
  }

  /**
   * Mock sources for development
   */
  private getMockSources(): Source[] {
    return [
      {
        id: 1,
        label: "Gov UK News",
        url: "https://www.gov.uk/search/news-and-communications",
        type: "news"
      },
      {
        id: 2,
        label: "Immigration Rules Updates",
        url: "https://www.gov.uk/guidance/immigration-rules",
        type: "rules"
      },
      {
        id: 3,
        label: "Parliament Updates",
        url: "https://www.parliament.uk/business/news/",
        type: "parliament"
      }
    ];
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/health`);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }
}

// Export a singleton instance
export const apiService = new ApiService();
export default apiService; 