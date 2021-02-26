    game_choice = request.form.get("game_choice")
    searchdb = list(mongo.db.game.find_one({"$text": {"$search":  game_choice }}))
    id = searchdb.appid
    r = requests.get("https://store.steampowered.com/api/appdetails?appids={{id}}")
    return render_template("game.html", data=json.loads(r.text)['{{id}}']['data']['pc_requirements']['minimum'])


     r = requests.get("https://store.steampowered.com/api/appdetails?appids={{ game_id }}")
    return render_template("cpu.html", game=json.loads(r.text)['{{ game_id }}']['data']['pc_requirements']['minimum'])


    r = requests.get("https://store.steampowered.com/api/appdetails?appids=" + game_id + "")
    game=json.loads(r.text)[ game_id ]['data']['pc_requirements']['minimum']


    @app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    game = list(mongo.db.game.find({"$text": {"$search": "\"" + query + "\""}}))
    if game != "":
        query_gpu = request.form.get("query")
        gpu = list(mongo.db.gpu.find({"$text": {"$search": "\"" + query-gpu + "\""}}))
        return render_template("game.html", game=game, gpu=gpu)


@app.route('/submit', methods=["GET", "POST"])
def submit():
    game_id = format(request.form['text'])
    return render_template("game.html", game=game)

@app.route('/submit', methods=["GET", "POST"])
def submit2():
    gpu = format(request.form['text-gpu'])
    return render_template("game.html", gpu=gpu)
     game=json.loads(r.text)[ game_id ]['data']['pc_requirements']['minimum']

    # Find old Geforce and ATI/Radeon GPUs and some Intel graphics
    for i in re.findall('(Intel?\s[A-Za-z]+\s\d{2,5}\s?[A-Za-z]{0,2}\s)', gpu_requirements):
        old_geforce_radeon_intel_gpu =  i


    # Find intel all integrated graphics
    for i in re.findall('(?i)intel\shd\s\d+[A-Za-z]{0,2}', gpu_requirements):
        intel_gpu = i


    # Find radeon hd
    for i in re.findall('(?i)amd\sradeon\shd\s\d+', gpu_requirements):
        radeon_hd = i
        if radeon_hd:
            find_old_gpu = mongo.db.rest_gpu.search({ "model": { "$regex": "(.*?)"+ radeon_hd + "", "$options" :'i' } })


    # Find other Radeon variants
    for i in re.findall('(?i)radeon\s[A-Za-z]{1,2}[0-9]{0,1}\s[0-9]+[A-za-z]{0,1}', gpu_requirements):
        other_radeon = i


 
    
    
    # Find nvidia gtx 
    for i in re.findall('(?i)nvidia\s[A-Za-z]+\s\d+', gpu_requirements):
        gtx_gpu = i


    return render_template("result.html",find_old_gpu=find_old_gpu,other_radeon=other_radeon, gpu_requirements=gpu_requirements,steam=steam, message=message, old_geforce_radeon_intel_gpu=old_geforce_radeon_intel_gpu, radeon_hd=radeon_hd, intel_gpu=intel_gpu, gtx_gpu=gtx_gpu)



       # Fix Steam Nvidia naming inconsistencies to align with the app's database
   # Eg. Geforce 7800GTX -> Geforce 7800 GTX || Nvidia 7800GT -> Geforce 7800 GT
    x =re.findall('(?i)nvidia\s\d+gt[xX]?', gpu_requirements)
    if x:
        length = len(x)
        for i in range(length):
                a = re.sub("[A-Za-z]+", lambda ele: " " + ele[0] + " ", x[i]) 
                b = re.sub("(?i)nvidia", "GeForce", a) 
                c = re.sub("^\s",  "", b)
                d = re.sub("\s\s$",  "", c)
                e = re.sub("\s$",  "", d)
                f = re.sub("  ",  " ", e)
                geforce_gt.append(f)

                """
    find_geforce_gt =re.findall('(?i)(nvidia\s\d+gt[xX]?|nvidia\s\d+\sgt[xX]?)', gpu_requirements)
    for i in find_geforce_gt:
            i = re.sub("[A-Za-z]+", lambda ele: " " + ele[0] + " ", i) 
            i = re.sub("(?i)nvidia", "GeForce", i) 
            i = re.sub("^\s",  "", i)
            i = re.sub("\s\s$",  "", i)
            i = re.sub("\s$",  "", i)
            i = re.sub("  ",  " ", i)
            geforce_gt.append(i)
"""  i = re.sub("(?i)nvidia",  "", i)
            i = re.sub("(?i)geforce\s",  "Nvidia Geforce", i)
            i = re.sub("^\s",  "", i)
            i = re.sub("\s\s$",  "", i)
            i = re.sub("\s$",  "", i)
            i = re.sub("  ",  " ", i)


               
    find_mb_gpu = re.findall("(?i)\d+\s*mb\+*\s(?:video card|graphics card|video|graphics|vram|video ram)*\s*\+*", steam)
    if find_mb_gpu:
        for i in find_mb_gpu:
            remove=i
            deleted += remove
            gpu_requirements = re.sub(remove,  "", gpu_requirements) 


            
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome, {}".format(
                            request.form.get("username")))
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    user_gpu_name = request.form.get("text-gpu-model")
    game_name = request.form.get("text-game-name")
    user_gpu_id = request.form.get("text-gpu-id")
 

    if session["user"]:
        return render_template("profile.html",user_gpu_id=user_gpu_id,user_gpu_name=user_gpu_name,game_name=game_name)
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/")
@app.route("/search")
def game():


    
@app.route("/return_back", methods=["GET", "POST"])
def return_back():
    quality = request.form.get("quality")
    fps = request.form.get("fps")
    result = bool('true')
    user_gpu_name = request.form.get("text-gpu-model")
    user_gpu_id = request.form.get("text-gpu-id")
    game_name = request.form.get("text-game-name")
    return render_template("fps.html",user_gpu_id=user_gpu_id, fps = fps, quality = quality, result=result,user_gpu_name=user_gpu_name,game_name=game_name)

    @app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)
        
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")




    
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    user_gpu_name = request.form.get("text-gpu-model")
    game_name = request.form.get("text-game-name")
    user_gpu_id = request.form.get("text-gpu-id")
 

    if session["user"]:
        return render_template("profile.html",user_gpu_id=user_gpu_id,user_gpu_name=user_gpu_name,game_name=game_name)
    return redirect(url_for("login"))


    @app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


    
@app.route("/benchmark", methods=["GET", "POST"])
def benchmark():
    if request.method == "POST":
        # check if username already exists in db
        game_gpu_combo = request.form.get(
            "name") + "_" + request.form.get("gpuName")
        existing_combo = mongo.db.gpu_game.find_one(
            {"gpu_game": (game_gpu_combo)})

        if existing_combo:
            flash("combo found")
            return redirect(url_for("benchmark"))

        gpu_game_combo = {
            "gpu_game": request.form.get("name") + "_" + request.form.get("gpuName")
        }
        mongo.db.gpu_game.insert_one(gpu_game_combo)

    return render_template("benchmark.html")

    
@app.route("/return_back", methods=["GET", "POST"])
def return_back():
    quality = request.form.get("quality")
    fps = request.form.get("fps")
    result = bool('true')
    user_gpu_name = request.form.get("text-gpu-model")
    user_gpu_id = request.form.get("text-gpu-id")
    game_name = request.form.get("text-game-name")
    return render_template("fps.html",user_gpu_id=user_gpu_id, fps = fps, quality = quality, result=result,user_gpu_name=user_gpu_name,game_name=game_name)