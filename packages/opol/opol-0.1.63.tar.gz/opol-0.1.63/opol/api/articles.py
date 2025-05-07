import json
from typing import Dict, List, Optional
from pydantic import BaseModel

from .client_base import BaseClient


class ContentsQueryParams(BaseModel):
    url: Optional[str] = None
    search_query: Optional[str] = None
    search_type: Optional[str] = None
    skip: Optional[int] = 0
    limit: int = 10
    sort_by: Optional[str] = None
    sort_order: str = "desc"
    filters: Optional[str] = None
    news_category: Optional[str] = None
    secondary_category: Optional[str] = None
    keyword: Optional[str] = None
    entities: Optional[str] = None
    locations: Optional[str] = None
    topics: Optional[str] = None
    classification_scores: Optional[str] = None
    keyword_weights: Optional[str] = None
    exclude_keywords: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None

class Articles(BaseClient):
    """
    Client to interact with the Articles API endpoints.
    """
    def __init__(self, mode: str, api_key: str = None, timeout: int = 60):
        # service-postgres at port 5434
        super().__init__(mode, api_key=api_key, timeout=timeout, service_name="service-postgres", port=5434)

    def __call__(self, *args, **kwargs):
        if args:
            kwargs['search_query'] = args[0]
            return self.get_articles(*args, **kwargs)
    
    class GetArticlesRequest(BaseModel):
        search_query: str
        limit: Optional[int] = 10
        from_date: Optional[str] = None
        to_date: Optional[str] = None
        search_type: Optional[str] = "semantic"

    class GetArticlesResponse(BaseModel):
        contents: List[Dict]


    def get_articles(self, *args, **kwargs) -> GetArticlesResponse:
        if args and 'search_query' not in kwargs:
            kwargs['search_query'] = args[0]
        endpoint = "api/v2/search/contents"  
        request = self.GetArticlesRequest(**kwargs)
        params = {k: v for k, v in request.model_dump().items() if v is not None}
        return self.get(endpoint, params)

    def by_entity(self, entity: str, date: Optional[str] = None, skip: Optional[int] = 0, limit: Optional[int] = 10) -> Dict:
        endpoint = f"api/v2/search/contents/by_entity/{entity}"
        params = {"skip": skip, "limit": limit}
        if date:
            params["date"] = date
        return self.get(endpoint, params)

    def by_id(self, article_id: str) -> Dict:
        """
        Retrieve a specific article by its ID.
        
        Args:
            article_id: The UUID of the article to retrieve
            
        Returns:
            Dict: The article data
        """
        endpoint = f"api/v2/search/contents/{article_id}"
        return self.get(endpoint)
