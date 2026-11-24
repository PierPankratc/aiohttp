from datetime import datetime
from aiohttp import web

ads = {}
next_id = 1


def serialize_ad(ad: dict) -> dict:
    return {**ad, "created_at": ad["created_at"].isoformat()}


async def create_ad(request: web.Request):
    global next_id
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "Некорректный JSON"}, status=400)

    ad = {
        "id": next_id,
        "title": data.get("title"),
        "description": data.get("description"),
        "created_at": datetime.now(),
        "owner": data.get("owner"),
    }
    ads[next_id] = ad
    next_id += 1

    return web.json_response(serialize_ad(ad), status=201)


async def get_ads(request: web.Request):
    return web.json_response(
        [serialize_ad(ad) for ad in ads.values()], status=200
    )


async def get_ad(request: web.Request):
    ad_id = int(request.match_info["ad_id"])
    ad = ads.get(ad_id)
    if ad is None:
        return web.json_response({"error": "Объявление не найдено"}, status=404)
    return web.json_response(serialize_ad(ad), status=200)


async def update_ad(request: web.Request):
    ad_id = int(request.match_info["ad_id"])
    ad = ads.get(ad_id)
    if ad is None:
        return web.json_response({"error": "Объявление не найдено"}, status=404)

    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "Некорректный JSON"}, status=400)

    if "title" in data:
        ad["title"] = data["title"]
    if "description" in data:
        ad["description"] = data["description"]
    if "owner" in data:
        ad["owner"] = data["owner"]

    return web.json_response(serialize_ad(ad), status=200)


async def delete_ad(request: web.Request):
    ad_id = int(request.match_info["ad_id"])
    ad = ads.pop(ad_id, None)
    if ad is None:
        return web.json_response({"error": "Объявление не найдено"}, status=404)
    return web.json_response({"message": "Объявление удалено"}, status=200)


def create_app():
    app = web.Application()
    app.router.add_post("/ads", create_ad)
    app.router.add_get("/ads", get_ads)
    app.router.add_get("/ads/{ad_id:\\d+}", get_ad)
    app.router.add_route("PUT", "/ads/{ad_id:\\d+}", update_ad)
    app.router.add_route("PATCH", "/ads/{ad_id:\\d+}", update_ad)
    app.router.add_delete("/ads/{ad_id:\\d+}", delete_ad)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="127.0.0.1", port=8080)