def clean_articles(data):

    cleaned = []

    for item in data:
        title = item["title"].strip()
        summary = item["summary"].strip()

        if summary == title:
            summary = ""

        cleaned.append({
            "title": title,
            "summary": summary,
            "url": item["url"].strip()
        })

    return cleaned