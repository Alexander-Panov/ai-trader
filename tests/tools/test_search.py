from unittest.mock import patch

from tools.search import search, SearchResponse

MOCK_TAVILY_RESPONSE = {
    'answer': 'Fesco is a major intermodal transport operator in Russia.',
    'follow_up_questions': None,
    'images': [],
    'query': 'Fesco',
    'request_id': '429427c9-993f-4453-9acb-180f177603fa',
    'response_time': 0.91,
    'results': [
        {
            'content': '# Fesco Transport Group. **FESCO Transportation Group** is an intermodal transport operator in Russia...',
            'raw_content': None,
            'score': 0.99953806,
            'title': 'Fesco Transport Group',
            'url': 'https://en.wikipedia.org/wiki/Fesco_Transport_Group',
        }
    ],
}


def test_search_fesco():
    with patch('tools.search.tavily_client.search', return_value=MOCK_TAVILY_RESPONSE):
        result = search.invoke({'query': 'Fesco'})

    assert isinstance(result, SearchResponse)