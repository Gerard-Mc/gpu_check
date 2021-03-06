import os
import json
import re
from re import search
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
mongo = PyMongo(app)


@app.route("/")
@app.route("/search")
def game():
    reset_gpu = "Search GPU"
    reset_game = "Search Games"
    return render_template("search.html", reset_gpu=reset_gpu, reset_game=reset_game)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    game_list = []
    game = list(mongo.db.game.find(
        {"$text": {"$search": "\"" + query + "\""}}))
    for i in game:
        if i["appid"] % 10 == 0:
            game_list.append(i)
    return render_template("search.html", game_list=game_list)


@app.route("/search_gpu", methods=["GET", "POST"])
def search_gpu():
    query_gpu = request.form.get("query-gpu")
    gpu = list(mongo.db.gpu.find(
        {"$text": {"$search": "\"" + query_gpu + "\""}}))
    return render_template("search.html", gpu=gpu)


@app.route('/submit', methods=["GET", "POST"])
def submit():
    result = bool('false')
    login_message = ""
    user_gpu_name = request.form.get("text-gpu-model")
    user_gpu_rating = 0
    user_gpu_id = ""
    user_gpu_find = mongo.db.gpu.find_one({ "model": { "$regex": '^'+user_gpu_name+'$', "$options" :'i' } })
    if user_gpu_find:
            user_gpu_rating = int(user_gpu_find['rating'])
            user_gpu_id =  user_gpu_find['_id']
    game_name = request.form.get("text-game-name")
    game_id = format(request.form['text-game'])
    message = ""
    message_success = "Your GPU supports this game"
    message_fail = "Your GPU does not support this game"
    message_not_found = "We can't find this configuration in our database"
    r = requests.get("https://store.steampowered.com/api/appdetails?appids=" + game_id + "")
    steam = json.loads(r.text)[game_id]['data']['pc_requirements']['minimum']
    if steam:
        pass

    find_title_is_graphics = re.search("(?<=Graphics:).+", steam)
    find_title_is_video = re.search("(?<=Video:).+", steam)
    find_title_is_graphics_card = re.search("(?<=Graphics Card:).+", steam)
    find_title_is_video_card = re.search("(?<=Video Card:).+", steam)
    find_title_is_russian = re.search("(?<=Видеокарта:).+", steam)
    long_requirements = []
    shorten_requirements = []
    old_geforce_gpu = []
    old_geforce_gpu_2 = []
    old_amd_gpu = []
    new_amd_gpu = []
    intel_gpu = []
    newer_gtx_gpu= []
    nvidia_titan= []
    gtx_gt_fix = []
    old_amd_mobile_gpu = []
    x_amd_gpu = []
    new_amd_rx__gpu = []
    find_mb_gpu= []
    mb_gpu=[]
    remove= ""
    switch = ""
    message = ""
    deleted = ""
    check = []
    rating = 0
    attr = []
    output = ""

    if find_title_is_graphics:
	    long_requirements = re.findall("(?<=Graphics:).+", steam)
    elif find_title_is_video:
	    long_requirements = re.findall("(?<=Video:).+", steam)
    elif find_title_is_video_card:
	    long_requirements = re.findall("(?<=Video Card:).+", steam)
    elif find_title_is_graphics_card:
	    long_requirements = re.findall("(?<=Graphics Card:).+", steam)
    elif find_title_is_russian:
	    long_requirements = re.findall("(?<=Видеокарта:).+", steam)
    else:
	    print("We don't have this game on our database.")
    # Tidy Steam requirements input
    if long_requirements:
        shorten_requirements = re.findall("(.*?)<\/li>", long_requirements[0])

    if shorten_requirements:
        remove_words = re.sub(
            "(?i)(?:series\s|or\s|better\s)", "  ", shorten_requirements[0])
        remove_words = re.sub(
            "(?i)(?:®|™)", "", remove_words)
        gpu_requirements = remove_words

    else:
        gpu_requirements = steam

    # Fix Steam Nvidia naming inconsistencies to align with the app's database
    # Eg. Geforce 7800GTX -> Geforce 7800 GTX || Nvidia 7800GT -> Geforce 7800 GT
    find_gtx_gt_fix = re.findall('(?i)(?:nvidia\sgeforce|nvidia|geforce)\s\d+gt[xX]?\s', gpu_requirements)
    for i in find_gtx_gt_fix:
                before= i
                i = re.sub("(?i)nvidia\sgeforce",  "", i)
                i = re.sub("(?i)nvidia",  "", i)
                i = re.sub("(?i)geforce\s",  " ", i)
                i = re.sub("^\s",  "Nvidia GeForce ", i)
                a = re.sub("(?i)(?:GTX|GT)", lambda ele: " " + ele[0] + " ", i) 
                switch = a
                gpu_requirements = re.sub(before,  switch, gpu_requirements)
                gtx_gt_fix.append(a)

    # Find old gpus under 1GB
    old_gpu = re.findall("\d+MB|\d+\sMB", gpu_requirements)
    for i in old_gpu:
                remove=i
                deleted += remove + ", "
    # Fix intel integrated graphics cards
    #eg intel hd 3000 and Intel hd 620
    find_intel_gpu =re.findall('(?i)intel\su?hd\s\d+[a-zA-Z]{0,2}', gpu_requirements)
    for i in find_intel_gpu:
                remove=i
                deleted += remove + ", "
    #Find mobile Amd gpus that are less powerful than all gpus on user gpu list
    find_old_amd_mobile_gpu = re.findall("(?i)(?:mobility\sradeon|mobility)\s(?:hd|x)*\s*(?:[1-3][0-9]\d+|4[0-5]\d+)\s*(?:x2|xt)*", gpu_requirements)
    for i in find_old_amd_mobile_gpu:
                remove=i
                deleted += remove + ", "
    #Find old geforce gpus. Geforce 256, geforce2, geforce3, geforce4. geforce fx, geforce 6000, geforce 7000, geforce 8000, geforce 9000 series 
    find_old_geforce_gpu = re.findall("(?i)(?:nvidia\sgeforce|NVIDIA|geforce\d*)\s(?:(?:ti|mx|pcx)\d+|fx|pcx|\d+|\d+\s\+|\d+a|\d+pv)\s*(?:\d+gtx\+|gtx|gso|gt|gx2|ge|gs|le|se|mgpu|ultra|TurboCache|nForce\s4[1-3]0)*\s(?:ultra)*", gpu_requirements)
    for i in find_old_geforce_gpu:
                remove=i
                deleted += remove + ", "
    find_x_amd_gpu = re.findall("(?i)(?:radeon|ati|amd)\sx\d+\s(?:le|pro|se|xt|xxl|xl|agp|gto|gt|x)", gpu_requirements)
    for i in find_x_amd_gpu:
                remove=i
                deleted += remove + ", "
    find_old_amd_gpu = re.findall("(?i)(?:radeon|ati|amd)\s(?:hd|x\d+|xpress\s\d+|xpress|8\d+|9\d+)\s(?:[2-3]\d+\s(?:pro|xt|gt|x2|\d+)*|[1-2]\d+|x\d+|le|pro|se|xt|xxl|xl|agp|gto|gt|x)", gpu_requirements)
    for i in find_old_amd_gpu:
                remove=i
                deleted += remove + ", "
    # Find Regular all Nvidia gpus from above 9000 series exept for titan series
    # eg.  'Geforce GT 740', 'Geforce RTX 2050 ti (notebook)', 'Geforce GTX 2090 ti mobile', 'Geforce RTX 2080 ti boost', 'Geforce RTX 2070', 'Geforce GTS 160', 'Geforce GTX 560 SE', 'Geforce MX110', 'Geforce M120', 'Geforce GTX 850', 'Geforce GT 520', 'Geforce RTX 2070 Max-Q', 'Geforce MX45', 'Geforce gtx 5000 ti', 'Geforce gt 300 super', 'Geforce GT 256'
    find_newer_gtx_gpu =re.findall('(?i)\s(?:gtx\s|gt\s|rtx\s|gts\s|mx|m)\d*[a-zA-Z]*\s*\d*\s*(?:GB|ti\sboost|ti\s\(?notebook\)*|ti|le|max-q|super\smax-q|se|super|\d+m|\(?mobile\)*|\(?notebook\)?)*', gpu_requirements)
    for i in find_newer_gtx_gpu:
                remove=i
                deleted += remove + ", "
    if old_gpu:
            message = message_success

    if find_intel_gpu:
        for i in find_intel_gpu:
                remove=i
                deleted += remove + ", "
                i = re.sub("^\s",  "", i)
                i = re.sub("\s\s$",  "", i)
                i = re.sub("\s$",  "", i)
                i = re.sub("  ",  " ", i)
                if i:
                        check = mongo.db.weaker_gpu.find_one({"$text": {"$search": "\"" + i + "\""}})
                        if check:
                            message = message_success
                        else:
                            pass

    elif find_old_amd_mobile_gpu:
        message = message_success

    elif find_old_geforce_gpu:
        message = message_success

    elif find_x_amd_gpu:
        message = message_success

    elif find_old_amd_gpu:
        message = message_success

    elif find_newer_gtx_gpu:
        print(find_newer_gtx_gpu)
        for i in find_newer_gtx_gpu:
             remove=i
             gpu_requirements = re.sub(remove,  "", gpu_requirements)
             deleted += remove + ", "
             i = re.sub("(?i)\d+GB",  "", i)
             i = re.sub("^",  "NVIDIA GeForce", i)
             i = re.sub("\s\s$",  "", i)
             a = re.sub("\s$",  "", i)
             if a:
                check = mongo.db.gpu.find_one({ "model": { "$regex": '^'+a+'$', "$options" :'i' } })
                if check:
                    rating = int(check['rating'])
                    attr = rating
                    if user_gpu_rating <= rating:
                        message = message_success
                    elif user_gpu_rating >= rating:
                        message = message_fail
                    else:
                        pass

    # find all Nvidia titan gpus in user gpu database 
    # eg "NVIDIA Titan Xp Collector's Edition", 'NVIDIA Titan Xp', 'NVIDIA Titan X (Pascal)', 'NVIDIA GTX TITAN X', 'NVIDIA GTX Titan Black', 'NVIDIA Titan RTX', 'NVIDIA Titan V', 'nvidia titan x'
    find_nvidia_titan =re.findall('(?i)\s(?:geforce\sgtx\stitan|nvidia\sgtx\stitan|nvidia\stitan|titan)\s(?:rtx|gtx|X\s\(?Pascal\)?|Xp\sCollector\'s\sEdition|xp|x|V|5|black)', gpu_requirements)
    for i in find_nvidia_titan:
            remove=i
            deleted += remove + ", "
            i = re.sub("Geforce",  "", i)
            i = re.sub("^\s",  "", i)
            i = re.sub("\s\s$",  "", i)
            i = re.sub("\s$",  "", i)
            i = re.sub("  ",  " ", i)
            if i:
                check = mongo.db.gpu.find_one({ "model": { "$regex": '^'+i+'$', "$options" :'i' } })
                if check:
                    rating = int(check['rating'])
                    attr = rating
                    if user_gpu_rating <= rating:
                        message = message_success
                    elif user_gpu_rating >= rating:
                        message = message_fail
                    else:
                        pass

    find_new_amd_rx__gpu = re.findall("(?i)(?:radeon|ati|amd)\srx\s\d*[a-zA-Z]*\s*", gpu_requirements)
    for i in find_new_amd_rx__gpu:
        remove=i
        deleted += remove + ", "
        i = re.sub("(?i)ati",  "radeon", i)
        i = re.sub("(?i)amd",  "radeon", i)
        i = re.sub("^\s",  "", i)
        i = re.sub("\s\s$",  "", i)
        i = re.sub("\s$",  "", i)
        if i:
            check = mongo.db.gpu.find_one({ "model": { "$regex": '^'+i+'$', "$options" :'i' } })
            if check:
                rating = int(check['rating'])
                attr = rating
                if user_gpu_rating <= rating:
                    message = message_success
                elif user_gpu_rating >= rating:
                    message = message_fail
                else:
                    pass


    #?  (:?\d+|\d+[a-zA-Z]+|\d+[a-zA-Z]+\d+)
    find_new_amd_gpu = re.findall("(?i)(?:mobility\sradeon|mobility|radeon|ati|amd)\s(?:hd|r[579x]|VII)\s\d*[a-zA-Z]*\d*\s*(?:xt|x2|boost|x|duo|56|64\sliquid|64)*", gpu_requirements)
    for i in find_new_amd_gpu:
        remove=i
        deleted += remove + ", "
        i = re.sub("(?i)ati",  "", i)
        i = re.sub("(?i)amd",  "", i)
        i = re.sub("(?i)radeon",  "", i)
        i = re.sub("^",  "AMD Radeon ", i)
        i = re.sub("\s\s",  " ", i)
        i = re.sub("\s\s$",  "", i)
        i = re.sub("\s$",  "", i)
        if i:
            check = mongo.db.gpu.find_one({ "model": { "$regex": '^'+i+'$', "$options" :'i' } })
            if check:
                rating = int(check['rating'])
                attr = rating
                if user_gpu_rating <= rating:
                    message = message_success
                elif user_gpu_rating >= rating:
                    message = message_fail
                else:
                    message = message_not_found

    if message == message_success:
        output = mongo.db.gpu.find_one( { "games": { "name": game_name } } )
        if output:
                pass
        else:
                mongo.db.gpu.update_one({ "_id": user_gpu_id },{ "$push": { 'games': { "name": game_name}}})
                output = mongo.db.gpu.find_one( { "games": { "name": game_name } } )


    return render_template("result.html",game_id=game_id,result=result,output=output,login_message=login_message,game_name=game_name,user_gpu_rating=user_gpu_rating, user_gpu_id=user_gpu_id,rating = rating,attr=attr,check=check,user_gpu_name=user_gpu_name,old_geforce_gpu_2=old_geforce_gpu_2,new_amd_rx__gpu=new_amd_rx__gpu,x_amd_gpu=x_amd_gpu,deleted=deleted,old_amd_mobile_gpu=old_amd_mobile_gpu,switch=switch,gtx_gt_fix=gtx_gt_fix,remove=remove,new_amd_gpu=new_amd_gpu,nvidia_titan=nvidia_titan,old_amd_gpu=old_amd_gpu,old_geforce_gpu=old_geforce_gpu,mb_gpu=mb_gpu,newer_gtx_gpu=newer_gtx_gpu,intel_gpu=intel_gpu,old_gpu=old_gpu, message= message,gpu_requirements=gpu_requirements,steam=steam)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")))
           
