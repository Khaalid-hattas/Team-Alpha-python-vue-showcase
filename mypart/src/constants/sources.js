// Single source of truth for which news sources the backend can actually
// scrape. Only sources listed here should ever be selectable/visible in the
// Website Manager — this keeps the UI from offering sites that have no
// scraper behind them (e.g. the old hardcoded "BBC" entry).
export const SUPPORTED_SOURCES = [
  {
    name: 'EWN',
    url: 'https://ewn.co.za/rss',
    category: 'Local'
  },
  {
    name: 'News24',
    url: 'https://www.news24.com/rss/news24/topstories',
    category: 'Politics'
  },
  {
    name: 'SABC News',
    url: 'https://www.sabcnews.com/sabcnews/feed/',
    category: 'Local'
  }
]

export const AVAILABILITY_NOTE =
  'Only sources with a working scraper are listed here. Select a source below to activate it — the dashboard will only show articles from sources you\'ve added.'