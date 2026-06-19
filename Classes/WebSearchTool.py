from ddgs import DDGS


class WebSearchTool:
    def __init__(self, max_results: int):
        self.max_results = max_results

    def search(self, query: str) -> list[dict]:
        results = []
        try:
            with DDGS() as search_engine:
                for result in search_engine.text(query, max_results=self.max_results):
                    results.append({
                        'title': result.get('title', ''),
                        'href': result.get('href', ''),
                        'body': result.get('body', '')
                    })
        except Exception as e:
            results.append({
                'title': 'Web search failed',
                'href': '',
                'body': str(e)
            })

        return results