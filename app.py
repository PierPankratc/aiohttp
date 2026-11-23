from datetime import datetime
from flask import Flask, jsonify, request



app = Flask(__name__)

ads = {}
next_id = 1


@app.route("/ads", methods=["POST"])
def create_ad():
    global next_id
    data = request.get_json()
    ad = {
        "id": next_id,
        "title": data.get("title"),
        "description": data.get("description"),
        "created_at": datetime.now(),
        "owner": data.get("owner"),
    }
    ads[next_id] = ad
    next_id += 1

    return jsonify(ad), 201


@app.route("/ads", methods=["GET"])
def get_ads():
    return jsonify(list(ads.values())), 200


@app.route("/ads/<int:ad_id>", methods=["GET"])
def get_ad(ad_id):
    ad = ads.get(ad_id)
    if ad is None:
        return jsonify({"error": "Объявление не найдено"}), 404
    return jsonify(ad), 200


@app.route("/ads/<int:ad_id>", methods=["PUT", "PATCH"])
def update_ad(ad_id):
    ad = ads.get(ad_id)
    if ad is None:
        return jsonify({"error": "Объявление не найдено"}), 404

    data = request.get_json()
    if "title" in data:
        ad["title"] = data["title"]
    if "description" in data:
        ad["description"] = data["description"]
    if "owner" in data:
        ad["owner"] = data["owner"]

    return jsonify(ad), 200


@app.route("/ads/<int:ad_id>", methods=["DELETE"])
def delete_ad(ad_id):
    ad = ads.pop(ad_id, None)
    if ad is None:
        return jsonify({"error": "Объявление не найдено"}), 404
    return jsonify({"message": "Объявление удалено"}), 200


if __name__ == "__main__":
    app.run(debug=True)
