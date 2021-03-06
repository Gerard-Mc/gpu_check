import os
import requests
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
    game = list(mongo.db.game.find(
        {"$text": {"$search": "\"" + query + "\""}}))
    return render_template("search.html", game=game)


@app.route("/search_gpu", methods=["GET", "POST"])
def search_gpu():
    query_gpu = request.form.get("query-gpu")
    gpu = list(mongo.db.gpu.find(
        {"$text": {"$search": "\"" + query_gpu + "\""}}))
    return render_template("search.html", gpu=gpu)


@app.route('/submit', methods=["GET", "POST"])
def submit():
    user_gpu_name = request.form.get("text-gpu-model")
    game_id = format(request.form['text-game'])
    r = requests.get(
        "https://store.steampowered.com/api/appdetails?appids=" + game_id + "")
    steam = json.loads(r.text)[game_id]['data']['pc_requirements']['minimum'] 
    #steam = "512mb vram +32mb+ vram 128mb graphics card+256 mb video card Graphics 32mb 4 MB Video Card 256MB graphics card 256MB graphics card intel hd 3000 intel hd 4000 intel uhd 620 geforce 750gtx geforce 630gt nvidia 200gt Mobility Radeon HD 4250 Mobility Radeon HD 2400 XT Mobility Radeon X2300 GeForce MX110 GeForce MX45 Nvidia GeForce 7800 GT Nvidia GeForce 7800 GTx Nvidia GeForce 6666 GT Nvidia GeForce 6666 GTx NVIDIA 9990 GT GeForce3 Ti200 GeForce 256 GeForce4 Ti4200 GeForce FX GeForce 6800 GT GeForce 7800 GTX GeForce 7300 SE GeForce 8800 Ultra GeForce 9400 mGPU gtx 1070 M270X GT Radeon GT M470 NVIDIA Titan RTX  Ti GTX 640 nvidia GT 740 nvidia GT 640m RTX 2050 ti (notebook) GTX 2090 ti notebook RTX 2080 ti boost RTX 2070 notebook RTX 2010 (notebook) RTX 2070 ti boost Max GTS 160M GTS 250 GTX 560 SE M120 GTX 850M GT 520MX RTX 2070 Max-Q gtx 5000 ti gt 300 super MB MX 8 RTX 2070 Super Max-Q GT 120 GT 140 NVIDIA Titan Xp Collector's Edition NVIDIA Titan Xp NVIDIA Titan X (Pascal) nvidia titan x Radeon X1050 AGP Radeon X300 LE Radeon X300 SE Radeon X600 SE Radeon X600 Pro Radeon X600 XT Radeon X800 Pro Radeon X800 XL Radeon X800 GTO Radeon x800 xt Radeon 8500 LE Radeon 9000 Pro Radeon 9250 SE Radeon 9600 Pro Radeon 9600 XT Radeon 9800 XL Radeon 9800 XXL Radeon Xpress X200 Radeon Xpress 1100 Radeon HD 2350 Radeon HD 2400 PRO Radeon HD 2400 XT Radeon HD 2600 PRO Radeon HD 2900 Radeon HD 3450 Radeon HD 3850 X2 Radeon hd 2350 Radeon hd 2900 Radeon hd 3400 Radeon X1900 256 Radeon RX 5500M Radeon RX 540 Radeon RX 540d Radeon RX Vega Radeon RX Vega Radeon RX 5500 Radeon RX 5300 Radeon RX 5300M Radeon RX 560X Radeon RX 6800 Radeon RX 6900 Radeon RX Vega Radeon RX Vega Radeon RX 550X Radeon RX 470D Radeon HD 7690M XT Radeon HD 6630M Radeon HD 6380G Radeon HD 4350 Radeon HD 5850 Radeon HD 6970 Radeon HD 6370D Radeon R9 295X2 Radeon R7 250E Radeon R5 235X Radeon R7 250 Radeon HD 7560D Radeon HD 4870 X2 Radeon HD 7870 XT Radeon HD 7950 Boost Radeon R9 Fury Radeon R9 Fury x Radeon R9 nano Radeon R9 pro duo Radeon VII xt Radeon HD 8850M Radeon HD 7520G Radeon HD 7770M Radeon Radeon HD 550v X Radeon R9 380X Radeon R9 Fury X Radeon HD 8570 Radeon hd 4300 Radeon hd 4250 Radeon hd 5400 Radeon hd 6750 Radeon hd 6600 Radeon hd"    
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
            "(?i)(?:series\s|or\s|better\s)", "", shorten_requirements[0])
        gpu_requirements = remove_words

    else:
        gpu_requirements = steam

    # Find old gpus under 1GB
    message=""
    old_gpu = re.findall("\d+MB|\d+\sMB", gpu_requirements)
    if old_gpu:
        message = "Your GPU supports this game"
        for i in find_mb_gpu:
            mb_gpu.append(i)
            remove=i
            deleted += remove
            gpu_requirements = re.sub(remove,  "", gpu_requirements) 

    # Fix intel integrated graphics cards
    #eg intel hd 3000 and Intel hd 620
    find_intel_gpu =re.findall('(?i)intel\su?hd\s\d+[a-zA-Z]{0,2}', gpu_requirements)
    elif find_intel_gpu:
        for i in find_intel_gpu:
                remove=i
                deleted += remove
                i = re.sub("^\s",  "", i)
                i = re.sub("\s\s$",  "", i)
                i = re.sub("\s$",  "", i)
                i = re.sub("  ",  " ", i)
                if i:
                        i = mongo.db.weaker_gpu.find_one({"$text": {"$search": "\"" + i + "\""}})
                        intel_gpu.append(i)
                        gpu_requirements = re.sub(remove,  "", gpu_requirements) 



   # Fix Steam Nvidia naming inconsistencies to align with the app's database
   # Eg. Geforce 7800GTX -> Geforce 7800 GTX || Nvidia 7800GT -> Geforce 7800 GT
    find_gtx_gt_fix =re.findall('(?i)(?:nvidia\sgeforce|nvidia|geforce)\s\d+gt[xX]?\s', gpu_requirements)
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


    #Find mobile Amd gpus that are less powerful than all gpus on user gpu list
    find_old_amd_mobile_gpu = re.findall("(?i)(?:mobility\sradeon|mobility)\s(?:hd|x)*\s*(?:[1-3][0-9]\d+|4[0-5]\d+)\s*(?:x2|xt)*", gpu_requirements)
    for i in find_old_amd_mobile_gpu:
            remove=i
            deleted += remove
            i = re.sub("\s\s$",  "", i)
            i = re.sub("\s$",  "", i)
            i = re.sub("  ",  " ", i)
            #old_amd_mobile_gpu.append(i)
            if i:
                    i = mongo.db.weaker_gpu.find_one({"$text": {"$search": "\"" + i + "\""}})
                    old_amd_mobile_gpu.append(i)            
                    gpu_requirements = re.sub(remove,  "", gpu_requirements)      


    #Find old geforce gpus. Geforce 256, geforce2, geforce3, geforce4. geforce fx, geforce 6000, geforce 7000, geforce 8000, geforce 9000 series 
    find_old_geforce_gpu = re.findall("(?i)(?:nvidia\sgeforce|NVIDIA|geforce\d*)\s(?:(?:ti|mx|pcx)\d+|fx|pcx|\d+|\d+\s\+|\d+a|\d+pv)\s*(?:\d+gtx\+|gtx|gso|gt|gx2|ge|gs|le|se|mgpu|ultra|TurboCache|nForce\s4[1-3]0)*\s(?:ultra)*", gpu_requirements)
    for i in find_old_geforce_gpu:
            remove=i
            deleted += remove
            i = re.sub("(?i)nvidia\sgeforce",  " ", i)
            i = re.sub("(?i)nvidia",  " ", i)
            i = re.sub("(?i)geforce\s",  " ", i)
            i = re.sub("^\s",  "GeForce ", i)
            i = re.sub("\s\s$",  "", i)
            i = re.sub("\s$",  "", i)
            i = re.sub("  ",  " ", i)
            if i:
                    i = mongo.db.weaker_gpu.find_one({"$text": {"$search": "\"" + i + "\""}})
                    old_geforce_gpu.append(i) 
                    gpu_requirements = re.sub(remove,  "", gpu_requirements)

    # Find Regular all Nvidia gpus from above 9000 series exept for titan series
    # eg.  'Geforce GT 740', 'Geforce RTX 2050 ti (notebook)', 'Geforce GTX 2090 ti mobile', 'Geforce RTX 2080 ti boost', 'Geforce RTX 2070', 'Geforce GTS 160', 'Geforce GTX 560 SE', 'Geforce MX110', 'Geforce M120', 'Geforce GTX 850', 'Geforce GT 520', 'Geforce RTX 2070 Max-Q', 'Geforce MX45', 'Geforce gtx 5000 ti', 'Geforce gt 300 super', 'Geforce GT 256'
    find_newer_gtx_gpu =re.findall('(?i)\s(?:gtx\s|gt\s|rtx\s|gts\s|mx|m)\d*[a-zA-Z]*\s*\d*\s*(?:GB|ti\sboost|ti\s\(?notebook\)*|ti|le|max-q|super\smax-q|se|super|\d+m|\(?mobile\)*|\(?notebook\)?)*', gpu_requirements)
    for i in find_newer_gtx_gpu:
             remove=i
             deleted += remove
             i = re.sub("(?i)\d+GB",  "", i)
             i = re.sub("(?i)nvidia\sgeforce",  " ", i)
             i = re.sub("(?i)nvidia",  " ", i)
             i = re.sub("(?i)geforce\s",  " ", i)
             i = re.sub("^\s",  "GeForce ", i)
             i = re.sub("\s\s$",  "", i)
             i = re.sub("\s$",  "", i)
             i = re.sub("  ",  " ", i)
             if i:
                i = mongo.db.gpu.find_one({"$text": {"$search": "\"" + i + "\""}})
                newer_gtx_gpu.append(i) 
                gpu_requirements = re.sub(remove,  "", gpu_requirements)


    # find all Nvidia titan gpus in user gpu database 
    # eg "NVIDIA Titan Xp Collector's Edition", 'NVIDIA Titan Xp', 'NVIDIA Titan X (Pascal)', 'NVIDIA GTX TITAN X', 'NVIDIA GTX Titan Black', 'NVIDIA Titan RTX', 'NVIDIA Titan V', 'nvidia titan x'
    find_nvidia_titan =re.findall('(?i)\s(?:geforce\sgtx\stitan|nvidia\sgtx\stitan|nvidia\stitan|titan)\s(?:rtx|gtx|X\s\(?Pascal\)?|Xp\sCollector\'s\sEdition|xp|x|V|5|black)', gpu_requirements)
    for i in find_nvidia_titan:
            remove=i
            deleted += remove
            i = re.sub("Geforce",  "", i)
            i = re.sub("^\s",  "", i)
            i = re.sub("\s\s$",  "", i)
            i = re.sub("\s$",  "", i)
            i = re.sub("  ",  " ", i)
            if i:
                    i = mongo.db.gpu.find_one({"$text": {"$search": "\"" + i + "\""}})
                    nvidia_titan.append(i)
                    gpu_requirements = re.sub(remove,  "", gpu_requirements)

    #Find old AMD gpus.
    #Radeon 7000, 8000, 9000, x1000, x2000, x300, x500, x600, x700, x800, x1000, x1200, 2100, hd 2000, hd 3000, hd 4000, hd 5000, hd 6000 series
    #(?i)(?:radeon|ati|amd)\s(?:ve|le|sdr|ddr|7500|3[2-4]0|8500|9[0-5][0-2]0|9\d+|x\d+\s|xpress|hd\s2\d+|hd\s3\d+|hd\s4\d+|hd\s5\d+|hd\s6[5-6]\d+)[a-zA-z]*", gpu_requirements)
    # Radeon 8500 LE   Radeon 9000 Pro    Radeon 9250 SE  Radeon 9600 Pro Radeon 9600 XT Radeon 9800 XL Radeon 9800 XXL  
    #  Radeon X1050 AGP  Radeon X300 LE Radeon X300 SE  Radeon X550   Radeon X600 SE Radeon X600 Pro  Radeon X1050  Radeon X600 XT 
    # Radeon Xpress X200  Radeon Xpress 1100 Radeon X800 GT 
    # #Radeon X800 GTO Radeon X800 Pro  Radeon X800 XL  Radeon X800 GTO  Radeon HD 2350  Radeon HD 2400 PRO Radeon HD 2400 XT  
    # Radeon HD 2600 PRO Radeon HD 2900 GT    Radeon HD 3450 Radeon HD 3850 X2 

    find_x_amd_gpu = re.findall("(?i)(?:radeon|ati|amd)\sx\d+\s(?:le|pro|se|xt|xxl|xl|agp|gto|gt|x)", gpu_requirements)
    for i in find_x_amd_gpu:
        remove=i
        deleted += remove
        i = re.sub("(?i)ati",  "radeon", i)
        i = re.sub("(?i)amd",  "radeon", i)
        i = re.sub("^\s",  "", i)
        i = re.sub("\s\s$",  "", i)
        i = re.sub("\s$",  "", i)
        if i:
                i = mongo.db.weaker_gpu.find_one({"$text": {"$search": "\"" + i + "\""}})
                x_amd_gpu.append(i)
                gpu_requirements = re.sub(remove,  "", gpu_requirements)

    
    find_old_amd_gpu = re.findall("(?i)(?:radeon|ati|amd)\s(?:hd|x\d+|xpress\s\d+|xpress|8\d+|9\d+)\s(?:[2-3]\d+\s(?:pro|xt|gt|x2|\d+)*|[1-2]\d+|x\d+|le|pro|se|xt|xxl|xl|agp|gto|gt|x)", gpu_requirements)
    for i in find_old_amd_gpu:
        remove=i
        deleted += remove
        i = re.sub("(?i)ati",  "radeon", i)
        i = re.sub("(?i)amd",  "radeon", i)
        i = re.sub("^\s",  "", i)
        i = re.sub("\s\s$",  "", i)
        i = re.sub("\s$",  "", i)
        if i:   
                i = mongo.db.weaker_gpu.find_one({"$text": {"$search": "\"" + i + "\""}})
                old_amd_gpu.append(i)
                gpu_requirements = re.sub(remove,  "", gpu_requirements)


    find_new_amd_rx__gpu = re.findall("(?i)(?:radeon|ati|amd)\srx\s\d*[a-zA-Z]*\s*", gpu_requirements)
    for i in find_new_amd_rx__gpu:
        remove=i
        deleted += remove
        i = re.sub("(?i)ati",  "radeon", i)
        i = re.sub("(?i)amd",  "radeon", i)
        i = re.sub("^\s",  "", i)
        i = re.sub("\s\s$",  "", i)
        i = re.sub("\s$",  "", i)
        if i:
                i = mongo.db.gpu.find_one({"$text": {"$search": "\"" + i + "\""}})
                new_amd_rx__gpu.append(i)
                gpu_requirements = re.sub(remove,  "", gpu_requirements)


#?  (:?\d+|\d+[a-zA-Z]+|\d+[a-zA-Z]+\d+)
    find_new_amd_gpu = re.findall("(?i)(?:mobility\sradeon|mobility|radeon|ati|amd)\s(?:hd|r[579x]|VII)\s\d*[a-zA-Z]*\d*\s*(?:xt|x2|boost|x|duo|56|64\sliquid|64)*", gpu_requirements)
    for i in find_new_amd_gpu:
        remove=i
        deleted += remove
        i = re.sub("(?i)ati",  "radeon", i)
        i = re.sub("(?i)amd",  "radeon", i)
        i = re.sub("^\s",  "", i)
        i = re.sub("\s\s$",  "", i)
        i = re.sub("\s$",  "", i)
        if i:
                i = mongo.db.gpu.find_one({"$text": {"$search": "\"" + i + "\""}})
                new_amd_gpu.append(i)
                gpu_requirements = re.sub(remove,  "", gpu_requirements)

    return render_template("result.html",user_gpu_name=user_gpu_name,old_geforce_gpu_2=old_geforce_gpu_2,new_amd_rx__gpu=new_amd_rx__gpu,x_amd_gpu=x_amd_gpu,deleted=deleted,old_amd_mobile_gpu=old_amd_mobile_gpu,switch=switch,gtx_gt_fix=gtx_gt_fix,remove=remove,new_amd_gpu=new_amd_gpu,nvidia_titan=nvidia_titan,old_amd_gpu=old_amd_gpu,old_geforce_gpu=old_geforce_gpu,mb_gpu=mb_gpu,newer_gtx_gpu=newer_gtx_gpu,intel_gpu=intel_gpu,old_gpu=old_gpu, message= message,gpu_requirements=gpu_requirements,steam=steam)


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


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
