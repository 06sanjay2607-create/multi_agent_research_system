
import os
import requests


def search_photos(query):
    key = os.getenv("UNSPLASH_ACCESS_KEY")

    if not key:
        return {
            "success": False,
            "photos": [],
            "message": "Photo search API key missing."
        }

    try:
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            headers={"Authorization": f"Client-ID {key}"},
            params={"query": query, "per_page": 6},
            timeout=15
        )
        response.raise_for_status()

        photos = []
        for item in response.json().get("results", []):
            photos.append({
                "image_url": item["urls"]["regular"],
                "photographer": item["user"]["name"],
                "photo_url": item["links"]["html"]
            })

        return {"success": True, "photos": photos}

    except requests.RequestException:
        return {
            "success": False,
            "photos": [],
            "message": "Photo search failed."
        }