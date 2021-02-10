    game_choice = request.form.get("game_choice")
    searchdb = list(mongo.db.game.find_one({"$text": {"$search":  game_choice }}))
    id = searchdb.appid
    r = requests.get("https://store.steampowered.com/api/appdetails?appids={{id}}")
    return render_template("game.html", data=json.loads(r.text)['{{id}}']['data']['pc_requirements']['minimum'])


     r = requests.get("https://store.steampowered.com/api/appdetails?appids={{ game_id }}")
    return render_template("cpu.html", game=json.loads(r.text)['{{ game_id }}']['data']['pc_requirements']['minimum'])