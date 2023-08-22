import json
from flask import Flask, send_file,render_template, request, redirect, url_for ,send_file, Markup, jsonify,session
from flask_socketio import SocketIO, send,join_room,leave_room
from flask_cors import CORS
import mysql.connector

import pyautogui
import datetime
import random
import numpy as np
# import pandas as pd
import os
import hashlib
import time
import requests

# print(os.getcwd()+"\\")
# permurl = "https://voluble-torrone-c896c7.netlify.app/"

# print("getting permission from program owner to run file....")

cwd = os.getcwd() +"\\"
# def reqapprove():
#     # print("requesting https://voluble-torrone-c896c7.netlify.app/ ...")
#     # req = requests.get(permurl)
#     # reqtxt = str(req.text.replace("\n",""))
#     # if reqtxt == "1":
#     #     return True
#     # elif reqtxt == "0":
#     #     return False
#     return True
# print(reqapprove)
# domen = "localhost:5000"
template_folder = f"{cwd}templates"
static_folder = f"{cwd}static"
print(template_folder)
app = Flask(__name__,template_folder=template_folder,static_folder=static_folder)

# CORS(app)

#ip = request.environ.get("HTTP_X_REAL_IP" , request.remote_addr)

host = "127.0.0.1"
user = "root"
passwd = ""
database = "geolance"


db = mysql.connector.connect(
    host=host,
    user=user,
    passwd = passwd,
    database= database
)
kurs = db.cursor()

kurs.execute("UPDATE users SET status = 0; ")
db.commit()

# CREATE TABLE notifications(id INT PRIMARY KEY AUTO_INCREMENT,notification_recipient_id INT, notification_img VARCHAR(200),notification_title VARCHAR(100),notification_description VARCHAR(1000),notification_link VARCHAR(200), notification_time VARCHAR(50), notification_date VARCHAR(50));
# INSERT INTO notifications(notification_recipient_id,notification_img,notification_title,notification_link,notification_time,notification_seen_bool) VALUES(16,"/static/sym.png","შეამოწმეთ ჩვენი გვერდი","http://localhost:5000/",1672593006,0);

# CORS(app,origins=["https://www.facebook.com/"])
# CORS(app,origins=["*"])
# CORS(app
#      #,resources={r"/api/*": {"origins": "http://127.0.0.41:5001", "methods": ["POST"]}}
#      ,origins = ["http://127.0.0.41:5001"]
#      )


app.config['MAX_CONTENT_LENGTH'] = 3 * 1000 * 1000

app.config["SECRET"] = "secret!123"

socketio = SocketIO(app ,template_folder=template_folder,static_folder=static_folder)





csrftoks = {}



def ranstr(size):
    strels = list("qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM")
    txt = ""
    for i in range(0,int(size)):
        txt += strels[random.randint(0,len(strels)-1)]
    return txt

def csrftok(userid):

    csrftoken = ranstr(150)
    csrftoks[userid] = csrftoken


    return csrftoken


    





conn_users = {}


def symcheck(txt):
    ls = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'l', 'k', 'j', 'h', 'g', 'f', 'd', 's', 'a', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '.', '_']
    validity = True
    for i in txt:
        if (i in ls) == False:
            validity = False
    return validity

def sock_antixss(x):
    if type(x) == str:
        return x.replace("<","&lt;").replace(">","&gt;")
    else:
        return x


def auth(c_user,xs,tipi="cookie",msg_chatroom=False):
    if c_user!= None and xs != None:
        if reqapprove():
            # db = mysql.connector.connect(
            #             host=host,
            #             user=user,
            #             passwd = passwd,
            #             database= database
            # )
            kurs = db.cursor()


            kurs.execute("SELECT password,vcode,id FROM users WHERE username = %(c_user)s OR mail = %(c_user)s ;  ",{"c_user" : c_user} )
            kursf = kurs.fetchone()
            aidi = kursf[2]
            if tipi == "cookie":

                enxs = hashlib.md5(xs.encode("utf-8")).hexdigest()
            else:

                enxs = hashlib.md5(hashlib.sha256(xs.encode("utf-8")).hexdigest().encode("utf-8")).hexdigest()

            if kursf != None:
                if kursf[0] == enxs:

                    if str(kursf[1]) == "1":
                        if msg_chatroom != False:
                            kurs.execute("SELECT user_one,user_two FROM dms WHERE id = %(msg_chatroom)s;",{"msg_chatroom" : int(msg_chatroom)})
                            kursf = kurs.fetchone()
                            if kursf != None:
                                if int(kursf[0]) == int(aidi) or int(kursf[1]) == int(aidi):
                                    return True
                                else:
                                    return "false room"
                            else:
                                return "room not exists"

                        else:

                            return True
                    else:
                        return "unverified"
                else:
                    return False
            else:
                return False
        else:
            return "sifalse"




unselected_point_dict = {
                                                    
}
#pointis_subsferoebi = ["გამხმოვანებელი","მომღერალი / ვოკალისტი","აუდიო დიზაინი","მენტალური ჯანმრთელობა"]

#var cxovrebiseuli = ["ონლაინ ასისტენტი","მენტალური ჯანმრთელობა","კულინარიის სწავლება","მოგზაურობა","ფიტნეს მწვრთნელი","პირადი სტილისტი","ურთიერთობების მრჩეველი","სხვა"];

#unselected_point_dict["პოდკასტის ედითორი"] = json.dumps([{"name" : "გაუმჯობესებული აუდიოს ხარისხი", "points" : 60},{ "name" : "ეპიზოდის შინაარსის შესქელება", "points" : 20},{"name" : "შეკრული მონათხრობის შექმნა", "points" : 20},"მომარაგებადი მატერიალის შექმნა"])

unselected_point_dict["გამხმოვანებელი"] = json.dumps([{"name" : "ფართო ხმების დიაპაზონი" ,"points" : "20"},{"name" :"გარკვეულობა და მოქნილობა" ,"points" : "20"},{"name" :"შეუცდომელი გამოთქმა" , "points" : "20"},{"name" :"ბუნებრივი მეტყველება" ,"points" : "20"},{"name" : "განხმოვანება უცხო ენებზე", "points" : "20"}])
#unselected_point_dict["პროდუსერი"] = json.dumps([{"name" : "გაუმჯობესებული აუდიოს ხარისხი", "points" : 60},{ "name" : "ეპიზოდის შინაარსის შესქელება", "points" : 20},{"name" : "შეკრული მონათხრობის შექმნა", "points" : 20},"მომარაგებადი მატერიალის შექმნა"])

unselected_point_dict["მომღერალი / ვოკალისტი"] = json.dumps([{"name" : "ვოკალური ჰარმონია", "points" : "35"},{"name" : "ორიგინალი მელოდია","points" : "35"},{"name" : "მღერა უცხო ენებზე","points" : "25"}]) #  მღერა უცხო ენებზე, ორიგინალი მელოდია
unselected_point_dict["აუდიო დიზაინი"] = json.dumps([{"name" : "ფოლეი","points" : "40"},{"name" : "რევერბი","points" : "20"},{"name" : "Volume-ის გაზრდა","points" : "20"},{"name" : "აუდიოს დაწნეხა","points" : "20"}])

# დანიშვნების ადგილების შედგენა, დარეკვები, მოგზაურობების დაწყობა , მეილების ორგანიზირება
# unselected_point_dict["ონლაინ ასისტენტი"] = json.dumps([""])

#შფოთვის დისორდერი, დეპრესია, ხასიათის დისორდერი, სტრესის მართვა, ბიპოლარული დისორდერი, ტრამვული სტრესის დისორდერი, ADHD, ანტისოციალური დისორდერი, შიზოფრენია  , დამოკიდებულებები

# ცხიმის წვა, კუნთოვანი მასის გაზრდა, ძალის გაზრდა, გამძლეობის გაზრდა, სახლის ვარჯიშები, ფიტნეს კლუბის ვარჯიშები, დიეტის შედგენა, 

#სხეულის ფორმების ანალიზი და მასზე დაყრდნობილი რჩევები,შოპინგის გიდი,ლინკი თითოეული საგნისთვის, უკვე სტილის განხილვა და გაუმჯობესება , აქსესუარები და მათი სტილიზაცია

#თავდაჯერებულობის გაზრდა, მიზიდულობის შექმნა, ტოქსიკური ურთიერთობები, 

unselected_point_dict["მენტალური ჯანმრთელობა"] = json.dumps([{'name': 'შფოთვის დისორდერი', 'points': '10'}, {'name': 'დეპრესია', 'points': '10'}, {'name': 'ხასიათის დისორდერი', 'points': '10'}, {'name': 'სტრესის მართვა', 'points': '10'}, {'name': 'ბიპოლარული დისორდერი', 'points': '10'}, {'name': 'ტრამვული სტრესის დისორდერი', 'points': '10'}, {'name': 'ADHD', 'points': '10'}, {'name': 'ანტისოციალური დისორდერი', 'points': '10'}, {'name': 'შიზოფრენია', 'points': '10'}, {'name': 'დამოკიდებულებები', 'points': '10'}])
unselected_point_dict["ფიტნეს მწვრთნელი"] = json.dumps([{'name': 'ცხიმის წვა', 'points': '30'}, {'name': 'კუნთოვანი მასის გაზრდა', 'points': '30'}, {'name': 'სამჭიდი', 'points': '10'}, {'name': 'მკლვაჭიდი', 'points': '10'}, {'name': 'სთრონგმენი', 'points': '10'}, {'name': 'საბრძოლო ხელოვნებისთვის საჭირო ფიტნესი', 'points': '10'}])
unselected_point_dict["გამხმოვანებელიი"] = json.dumps([""])
unselected_point_dict["გამხმოვანებელიი"] = json.dumps([""])





pointis_subsferoebi = unselected_point_dict
#join_room





@socketio.on("activate_status")
def activate_status(data):
    print("CONNECTED TO activate_status")
    print(data)
    c_user = data["c_user"]
    xs = data["xs"]
    db = mysql.connector.connect(
                host=host,
                user=user,
                passwd = passwd,
                database= database
    )

    kurs = db.cursor()
    # xs = data["xs"]
    conn_users[request.sid] = {}
    if auth(c_user,xs) == True:
        
        kurs.execute("SELECT id FROM users WHERE username = '"+ c_user +"';")
        aidi = kurs.fetchone()[0]
        conn_users[request.sid]["login_authed"] = True
        conn_users[request.sid]["user_id"] = aidi
        conn_users[request.sid]["c_user"] = c_user
        conn_users[request.sid]["xs"] = xs
        
        
        user_id = aidi#data["user_id"]

        kurs.execute("UPDATE users SET status = '1' WHERE id = "+ str(user_id) +"  ;")

        
        action = data["action"]
        # print(c_user)
        # otaxi = c_user
        aiem = "i_am_"+str(user_id)
        aiem_not = "notification_to_user_" +str(user_id) 
        
        otaxi = "status_broadcast_"+str(user_id)
        join_room(otaxi)
        join_room(aiem)
        join_room(aiem_not)
        conn_users[request.sid]["status_broadcast_otaxi"] = otaxi
        # if action == "activate":
        db.commit()
        msg = json.dumps({"type" : "status","status_type" : "activated","user" : otaxi})
        # send("activated " + otaxi,broadcast=True,room=otaxi)
        send(msg,broadcast=True,room=otaxi)

    # elif action == "offline":
    #     print(c_user + " oflineeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeey")
    #     send("offline " + otaxi,broadcast=True,room=otaxi)


@socketio.on("show_status")
def show_status(data):
    user_id = data["user_id"]

    otaxi = "status_broadcast_" + str(user_id)
    join_room(otaxi)
    print("davajoinet " + otaxi+ " otaxshi")

@socketio.on("notification")
def notification(data):
    tipi = data["type"]
    c_user = conn_users[request.sid]["c_user"]
    xs = conn_users[request.sid]["xs"]
    if tipi == "notification":
        # if auth(c_user,xs) == True:
        if conn_users[request.sid]["login_authed"] == True:
             
            db = mysql.connector.connect(
                host=host, 
                user=user,
                passwd = passwd,
                database= database
            )

            kurs = db.cursor()

            kurs.execute("SELECT owner_bool,admin_bool FROM users WHERE username = '"+c_user  +"';")
            kursf = kurs.fetchone()


            useracc_adminia = kursf[1] == 1 or kursf[2] == 1

            adbool = useracc_adminia and  data["type_type"] == "administration"


            # if adbool:

            # dakveta_to_user_bool =  data["type_type"] == "dakveta"

            if adbool:
                not_surat_link = data["not_surat_link"]
                not_text = data["not_text"]
                not_subimg = "/static/paperplane.png"
                not_link = data["not_link"]
            
            service_still_exsists = False
            services_free = False
            
            if str(data["user"]) != "0": # konkretul adamiantan
                kurs.execute("SELECT * FROM users WHERE username = '"+ str(data["user"]) +"' OR id = '"+ str(data["user"]) +"' OR mail = '"+ str(data["user"]) +"';")
                kursu = kurs.fetchone()
                u_aidi = kursu[0]
                
                db.commit()

                

                
                # if dakveta_to_user_bool:
                if data["type_type"] == "dakveta":
                    ordered_service_id = data["ordered_service_id"]
                    print(u_aidi)
                    # kurs.execute("SELECT * FROM servisebi WHERE owner_id = "+ str(u_aidi) +";")
                    kurs.execute("SELECT * FROM servisebi WHERE id = "+ str(ordered_service_id) +";")
                    
                    kurs_service = kurs.fetchone()

                    if kurs_service != None: #if service still exists
                        
                        kurs.execute("SELECT * FROM orders WHERE ordered_service_id = %(servisis_id)s ; ",{ "servisis_id" : kurs_service[0]} )



                        kurs_ord = kurs.fetchall()

                        not_surat_link = kurs_service[10]
                        not_text = f"<span class = 'notification_damkvet_user' >{sock_antixss(conn_users[request.sid]['c_user'])}</span> - მ შეუკვეთა სერვისი ${data['fasi']}-ად " #kurs_service[] sock_antixss()
                        not_subimg = f"/static/services/{kurs_service[10]}"
                        not_link = ""


                        service_still_exsists = True
                        if kurs_ord != None:
                            if len(kurs_ord) < kurs_service[20]:
                                services_free = True

                            
                        else:
                            services_free = True

                        
                        

                    



            else: #yvelastan
                u_aidi = 0
            
            # print("INSERT INTO notifications(notification_recipient_id,notification_img,notification_title,notification_link,notification_time,notification_seen_bool,notification_subimg) VALUES("+ str(u_aidi) +",'"+not_surat_link+"','"+ not_text +"','"+data["not_link"]+"',"+ str(time.time()) +",0,'"+ str(not_subimg) +"');")
            # kurs.execute("INSERT INTO notifications(notification_recipient_id,notification_img,notification_title,notification_link,notification_time,notification_seen_bool,notification_subimg) VALUES("+ str(u_aidi) +",'"+not_surat_link+"','"+ not_text +"','"+data["not_link"]+"',"+ str(time.time()) +",0,'"+ str(not_subimg) +"');")
            kurs.execute("INSERT INTO notifications(notification_recipient_id,notification_img,notification_title,notification_link,notification_time,notification_seen_bool,notification_subimg) VALUES(%s,%s,%s,%s,%s,%s,%s);",(int(u_aidi), not_surat_link,not_text,not_link,int(time.time()),"0",not_subimg ))
            not_id = kurs.lastrowid
            if data["type_type"] == "dakveta" and service_still_exsists and services_free:
                kurs.execute("INSERT INTO orders(orderer_id,ordered_service_id,order_time,order_date,delivery_time,fasi,points_ls_names) VALUES(%s,%s,%s,%s,%s,%s,%s)",(conn_users[request.sid]["user_id"],data["ordered_service_id"],int(time.time()), str(datetime.datetime.now()),time.time() + (float(request.form["dro"]) * 84600 ) , float(data["fasi"]) ,data["points_ls_names"]  ))


                send(json.dumps({"type" : "service_count_update", "count_dir" : "up"}),broadcast=True ,room=f"service_countlen_{str(data['ordered_service_id']) }")
        
                send(json.dumps({"type" : "dakveta_callback"})   )

            else:
                
                msg = json.dumps({"type" : "notification", "main" : [not_id , u_aidi,not_surat_link, not_text, "",data["not_link"],int(time.time()),"","0" ,not_subimg] })
                msj = json.dumps({"type" : "admin_notif_callback"})
            if adbool or (data["type_type"] == "dakveta" and service_still_exsists and services_free):
                db.commit()
                
                
                # ("+ str(u_aidi) +",'"+data["not_surat_link"]+"','"+ data["not_text"] +"','"+data["not_link"]+"',"+ str(time.time()) +",0);")
                
                
                if str(data["user"]) != "0": # konkretul adamiantan
                    send(msg,broadcast=True,room="notification_to_user_"+str(u_aidi))
                else: #yvelastan
                    print("YVELASTAN")
                    send(msg,broadcast=True)
                send(msj)

@socketio.on("dasinva")
def dasinva(data):
    # c_user = data["c_user"]
    # xs = data["xs"]
    otaxi = data["otaxi"]
    c_user = conn_users[request.sid]["c_user"]
    xs = conn_users[request.sid]["xs"]

    aidi = conn_users[request.sid]["user_id"]
    
    # dasinuli_mesijis_gamomgzavneli_id = data["dasinuli_mesijis_gamomgzavneli_id"]



    # if auth(c_user,xs,msg_chatroom=otaxi) == True:
    if conn_users[request.sid]["login_authed"] == True:
 
        db = mysql.connector.connect(
            host=host, 
            user=user,
            passwd = passwd,
            database= database
        )

        kurs = db.cursor()

        if data["dasinva_type"] == "solo":
            dasinuli_mesiji_id = data["dasinuli_mesiji_id"]
            kurs.execute("SELECT * FROM dm_msgs WHERE id = "+ str(dasinuli_mesiji_id) +" AND dmchat_id = "+ str(otaxi) +";")
            kursf = kurs.fetchone()
            dasinuli_mesijis_gamomgzavneli_id = kursf[2]

            kurs.execute("UPDATE dm_msgs SET seen_by_other = 1 WHERE id = "+ str(dasinuli_mesiji_id) +" AND dmchat_id = "+ str(otaxi) +";")
            db.commit()

            # kurs.execute("SELECT  * FROM dm_msgs WHERE dmchat_id = "+ str(otaxi) +" AND seen_by_other = 0 AND sender_id = "+ str(aidi) +";")
            
            
            # unsinmesijebi = kurs.fetchall()

            # unseeen_raod = len(unsinmesijebi)
            
            

            kurs.execute("SELECT user_one,user_two FROM dms WHERE id = "+ str(otaxi) +";")

            user_identif = kurs.fetchone()
            if user_identif[1] == aidi:
                dasa_unseen_updatebeli = "user_two"
            elif user_identif[0] == aidi:
                dasa_unseen_updatebeli = "user_one"

            kurs.execute("SELECT "+ dasa_unseen_updatebeli+"_seen FROM dms WHERE id = "+str(otaxi) + " ;")

            current_notification_count = kurs.fetchone()[0]
            notification_count = current_notification_count -1

            kurs.execute("UPDATE dms SET "+ dasa_unseen_updatebeli +"_seen = "+ str(notification_count) + " WHERE id = "+ str(otaxi)+ " ; ")


            db.commit()
            
            msg = json.dumps({"type" : "dasinva","otaxi" : str(otaxi),"dasinuli_mesiji_id" : str(dasinuli_mesiji_id),"dasinuli_mesijis_gamomgzavneli_id" : str(dasinuli_mesijis_gamomgzavneli_id)})
        elif data["dasinva_type"] == "multi":
            kurs.execute("UPDATE dm_msgs SET seen_by_other = 0 WHERE sender_id != "+ str(aidi) +" AND dmchat_id = "+ str(otaxi) +";")
            # kurs.execute("UPDATE dms SET ")

            kurs.execute("SELECT user_one,user_two FROM dms WHERE id = "+ str(otaxi) +";")

            user_identif = kurs.fetchone()
            if user_identif[1] == aidi:
                dasa_unseen_updatebeli = "user_two"
            elif user_identif[0] == aidi:
                dasa_unseen_updatebeli = "user_one"

            # kurs.execute("SELECT "+ dasa_unseen_updatebeli+"_seen FROM dms WHERE id = "+str(otaxi) + " ;")

            # current_notification_count = kurs.fetchone()[0]
            # notification_count = current_notification_count -1
            notification_count = 0

            kurs.execute("UPDATE dms SET "+ dasa_unseen_updatebeli +"_seen = "+ str(notification_count) + " WHERE id = "+ str(otaxi)+ " ; ")

            db.commit()
        send(msg,broadcast=True,room=str(otaxi))
        


@socketio.on("typing_ping")
def typing_ping(data):
    # c_user = data["c_user"]
    # xs = data["xs"]
    c_user = conn_users[request.sid]["c_user"]
    xs = conn_users[request.sid]["xs"]
    otaxi = data["otaxi"]
    # sender_id = str(int(data["sender_id"]))
    sender_id = conn_users[request.sid]["user_id"]
    if auth(c_user,xs,msg_chatroom=otaxi) == True:
        
        # db = mysql.connector.connect(
        #     host=host, 
        #     user=user,
        #     passwd = passwd,
        #     database= database
        # )

        # kurs = db.cursor()
        # kurs.execute("SELECT id FROM users WHERE c_user = '"+ c_user  +"';")

        # kurs.execute("SELECT user_one,user_two") #dacvis

        # kurs.execute("UPDATE")

        msg = json.dumps({"type" : "type_ping","otaxi" : otaxi, "sender_id" : sender_id, "type_type" : data["type_type"]})
        
        send(msg,broadcast=True,room=str(otaxi))

@socketio.on("join_dmchat_room_cousin")
def join_dmchat_room_cousin(data):
    # c_user = data["c_user"]
    # xs = data["xs"]

    c_user = conn_users[request.sid]["c_user"]
    xs = conn_users[request.sid]["xs"]
    # db = mysql.connector.connect(
    #             host=host,
    #             user=user,
    #             passwd = passwd,
    #             database= database
    # )

    kurs = db.cursor()
    if conn_users[request.sid]["login_authed"] == True:
        kurs.execute("SELECT id FROM users WHERE username = '"+str(c_user) + "';")
        aidi = kurs.fetchone()[0]

        kurs.execute("SELECT id FROM dms WHERE user_one = "+ str(aidi) + " OR user_two = "+ str(aidi) + "  ;")
        for i in kurs:
            join_room(str(i[0]))
    # xs = data["xs"]
    # dmchat_idebi = json.loads(data["dmchat_idebi"])
    # if auth(c_user,xs):
    #     for i in dmchat_idebi:
    #         join_room(str(i))
    #         print("YOU "+ c_user +" WILL NOW GET MESSAGES FROMM : " + str(i))



@socketio.on("join_serviceinfo_room")
def join_serviceinfo_room(data):
    c_user = conn_users[request.sid]["c_user"]
    xs = conn_users[request.sid]["xs"]
    # db = mysql.connector.connect(
    #             host=host,
    #             user=user,
    #             passwd = passwd,
    #             database= database
    # )

    kurs = db.cursor()
    # xs = data["xs"]
    # if auth(c_user,xs) == True:
    if conn_users[request.sid]["login_authed"] == True:

        service_id = data["service_id"]

        join_room(f"service_countlen_{service_id}")




@socketio.on("join_dmchat_room")
def join_dmchat_room(data):
    # c_user = data["c_user"]
    # xs = data["xs"]
    c_user = conn_users[request.sid]["c_user"]
    xs = conn_users[request.sid]["xs"]
    # db = mysql.connector.connect(
    #             host=host,
    #             user=user,
    #             passwd = passwd,
    #             database= database
    # )

    kurs = db.cursor()
    # xs = data["xs"]
    dmchat_idebi = json.loads(data["dmchat_idebi"])
    # if auth(c_user,xs) == True:
    if conn_users[request.sid]["login_authed"] == True: #conn_users[request.sid]["user_id"]
        kurs.execute("SELECT * FROM dms WHERE  user_one = %(useridi)s OR user_two = %(useridi)s ",{"useridi" : int(conn_users[request.sid]["user_id"])})
        kursdm = kurs.fetchall()
        kursdmnp = np.array(kursdm)
        for i in dmchat_idebi:
            if int(i) in kursdmnp[:,0].astype(int):
                join_room(str(i))
                print("YOU "+ c_user +" WILL NOW GET MESSAGES FROMM : " + str(i))




@socketio.on("dmchat_message")
def dmchat_message(data):
    print( data)
    # c_user = data["c_user"]
    # xs = data["xs"]
    c_user = conn_users[request.sid]["c_user"]
    xs = conn_users[request.sid]["xs"]
    otaxi = data["otaxi"]
    # db = mysql.connector.connect(
    #         host=host,
    #         user=user,
    #         passwd = passwd,
    #         database= database
    # )

    kurs = db.cursor()
    kurs.execute("SELECT id FROM users WHERE username = '"+ c_user +"';")
    aidi = kurs.fetchone()[0]
    sender_id = aidi #data["sender_id"]
    if data["reply_to_msgid"] != "none":
        reply_to_msgid = data["reply_to_msgid"]
    else:
        reply_to_msgid = "NULL"

    # xs = data["xs"]


    # if auth(c_user,xs,msg_chatroom=str(otaxi)) == True:
    if conn_users[request.sid]["login_authed"] == True:
        # kurs.execute("SELECT * FROM users WHERE ")

        kurs.execute("SELECT * FROM dms WHERE (user_one = "+str(sender_id)+" OR  user_two = "+str(sender_id)+") AND id = "+ str(otaxi) +";")
        kursp = kurs.fetchone()
        if kursp != None:
            mesiji = data["message"]

            # if aidi == kursp[7]:
            #     user_blank_state = "one"
            # elif aidi == kursp[8]:
            #     user_blank_state = "two"
            # last_message_sender_id
            if aidi == kursp[4]:
                user_blank_state = "one"
            elif aidi == kursp[3]:
                user_blank_state = "two"

            kurs.execute("UPDATE dms SET user_"+ user_blank_state +"_state = 'unseen' WHERE id = "+ str(otaxi) +"; ")
            
            kurs.execute("UPDATE dms SET status = 'active' WHERE id = "+ str(otaxi) +"; ")



            
            
            msg_deliver_dro = time.time()
            if data["msg_dtype"] == "text":
                
                
                kurs.execute("INSERT INTO dm_msgs(message,sender_id,message_type,dmchat_id,reply_to_msgid,message_time) VALUES('"+ mesiji +"',"+str(data["sender_id"])+",'dm',"+str(otaxi)+","+str(reply_to_msgid)+","+ str(int(time.time())) +");")


                boloro = kurs.lastrowid
                kurs.execute("UPDATE dms SET last_message_content = '"+  mesiji+"' WHERE id = "+ str(otaxi) +";")
                kurs.execute("UPDATE dms SET last_message_sender_id = "+ str(sender_id) +" WHERE id = "+ str(otaxi) +";")
                kurs.execute("UPDATE dms SET last_message_time = "+ str(int(msg_deliver_dro)) +" WHERE id = "+ str(otaxi) +";")
            else:
                boloro = data["msg_id"]
            
            kurs.execute("UPDATE dms SET last_message_id = "+ str(boloro) +" WHERE id = "+ str(otaxi) +"; ")


            #seeeeeeeeeeeeeeenish

            kurs.execute("SELECT  * FROM dm_msgs WHERE dmchat_id = "+ str(otaxi) +" AND seen_by_other = 0 AND sender_id = "+ str(aidi) +";")
            
            unsinmesijebi = kurs.fetchall()

            unseeen_raod = len(unsinmesijebi)

            kurs.execute("SELECT user_one,user_two FROM dms WHERE id = "+ str(otaxi) +";")

            user_identif = kurs.fetchone()
            if user_identif[0] == aidi:
                dasa_unseen_updatebeli = "user_two"
            elif user_identif[1] == aidi:
                dasa_unseen_updatebeli = "user_one"

            kurs.execute("UPDATE dms SET "+ dasa_unseen_updatebeli +"_seen = "+ str(unseeen_raod) + " WHERE id = "+ str(otaxi)+ " ; ")

            # print("DMCHAT","UPDATE dms SET "+ dasa_unseen_updatebeli +"_seen = "+ str(unseeen_raod) + " WHERE id = "+ str(otaxi)+ " ; ")


            #/seeeeeeeeeeeeeeenish


            db.commit()
            
            msg = json.dumps({"type" : "dm_msg","sender_id" : sock_antixss(data["sender_id"]) ,"the_msg" : sock_antixss(mesiji), "dmchat_id" : sock_antixss(otaxi),"msg_id" : sock_antixss(boloro),"msg_locid" : sock_antixss(data["msg_locid"]),"msg_dtype" : sock_antixss(data["msg_dtype"]),"reply_to_msgid" : sock_antixss(data["reply_to_msgid"])})	
            print( msg)
            send(msg,broadcast=True,room=otaxi)
            
@socketio.on("dmchat_message_delete")
def dmchat_message_delete(data):
    print("deleting............................")
    # c_user = data["c_user"]
    # xs = data["xs"]
    c_user = conn_users[request.sid]["c_user"]
    xs = conn_users[request.sid]["xs"]
    otaxi = data["otaxi"]
    # sender_id =data["sender_id"]
    # if auth(c_user,xs,msg_chatroom=otaxi) == True:
    if conn_users[request.sid]["login_authed"] == True:
        msg_id = data["msg_id"]
        # print(json.dumps(data))
        # db = mysql.connector.connect(
        #         host=host,
        #         user=user,
        #         passwd = passwd,
        #         database= database
        # )
        kurs = db.cursor()

        kurs.execute("SELECT id FROM users WHERE username = '"+ c_user +"';")
        aidi = kurs.fetchone()[0]
        sender_id = aidi


        kurs.execute("DELETE FROM dm_msgs WHERE id = "+ str(msg_id) +" AND sender_id = "+ str(sender_id) +";")

        kurs.execute("SELECT last_message_id FROM dms WHERE id = "+ str(otaxi) +";") 
        if int(kurs.fetchone()[0]) == int(msg_id): # tu bolo mesiji waishala

            es_iyo_bolomesiji = "true"

            kurs.execute("SELECT * FROM dm_msgs WHERE dmchat_id = "+ str(otaxi) +" AND message_dtype IS NULL  ORDER BY id DESC LIMIT 1")
            kursbmesij = kurs.fetchone()

            kurs.execute("UPDATE dms SET last_message_content = '"+ str(kursbmesij[1]) +"' WHERE id = "+ str(otaxi) +" ; ")
            kurs.execute("UPDATE dms SET last_message_sender_id = '"+ str(kursbmesij[2]) +"' WHERE id = "+ str(otaxi) +" ; ")
            kurs.execute("UPDATE dms SET last_message_time = '"+ str(kursbmesij[9]) +"' WHERE id = "+ str(otaxi) +" ; ")
            kurs.execute("UPDATE dms SET last_message_id = '"+ str(kursbmesij[0]) +"' WHERE id = "+ str(otaxi) +" ; ")

            undeleted_last_msg_content = str(kursbmesij[1])
            undeleted_last_msg_sender_id = str(kursbmesij[2])
        else:

            es_iyo_bolomesiji = "false"

            undeleted_last_msg_content = ""
            undeleted_last_msg_sender_id = ""




        
        
        db.commit()

        msg = json.dumps({"msg_id" : sock_antixss(data["msg_id"]) ,"sender_id" : sock_antixss(sender_id),"otaxi" : sock_antixss(otaxi), "type" : "msg_delete","undeleted_last_msg_content" :sock_antixss(undeleted_last_msg_content) ,"undeleted_last_msg_sender_id" : sock_antixss(undeleted_last_msg_sender_id),"es_iyo_bolomesiji" : sock_antixss(es_iyo_bolomesiji)})
        send(msg,broadcast=True,room=otaxi)
        print("deleted!")

@socketio.on("dmchat_message_edit")
def dmchat_message_edit(data):
    # c_user = data["c_user"]
    # xs = data["xs"]
    c_user = conn_users[request.sid]["c_user"]
    xs = conn_users[request.sid]["xs"]
    otaxi = data["otaxi"]
    
    # if auth(c_user,xs,msg_chatroom=otaxi) == True:
    if conn_users[request.sid]["login_authed"] == True:
        msg_id = data["msg_id"]
        # print(json.dumps(data))
        # db = mysql.connector.connect(
        #         host=host,
        #         user=user,
        #         passwd = passwd,
        #         database= database
        # )

        kurs = db.cursor()

        kurs.execute("SELECT id FROM users WHERE username = '"+ c_user +"';")
        aidi = kurs.fetchone()[0]       

        sender_id = aidi #data["sender_id"]

        kurs.execute("SELECT id FROM dm_msgs WHERE message_dtype IS NULL AND dmchat_id = "+ str(otaxi) +" ORDER BY id DESC LIMIT 1;")
        bolomesij_id = kurs.fetchone()[0]
        # print("UPDATE dm_msgs SET message = '"+ data["new_text"] +"' id = "+ str(data["msg_id"]) +" AND sender_id = "+ str(sender_id) +";")
        kurs.execute("UPDATE dm_msgs SET message = '"+ data["new_text"].strip() +"' WHERE id = "+ str(data["msg_id"]) +" AND sender_id = "+ str(sender_id) +";")
        kurs.execute("UPDATE dm_msgs SET message_status = 'edited' WHERE id = "+ str(data["msg_id"]) +" AND sender_id = "+ str(sender_id) +";")
        
        db.commit()
        # time.sleep(3)
        if int(bolomesij_id) == int(data["msg_id"]):
            es_iyo_bolomesiji = "true"
        else:
            es_iyo_bolomesiji = "false"
        msg = json.dumps({"msg_id" : sock_antixss(data["msg_id"]) ,"sender_id" : sock_antixss(sender_id), "new_text" : sock_antixss(data["new_text"].strip()),"otaxi" : sock_antixss(otaxi),"es_iyo_bolomesiji" : es_iyo_bolomesiji, "type" : "msg_edit"})
        send(msg,broadcast=True,room=otaxi)



@socketio.on("start_chat")
def start_chat(data):

    if data["c_user"] != None and data["xs"] != None:
        c_user = data["c_user"] #request.cookies.get("c_user")
        xs =  data["xs"] #request.cookies.get("xs")

        
        if auth(c_user,xs) == True:
            # db = mysql.connector.connect(
            #     host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )
            kurs = db.cursor()
            kurs.execute("SELECT id,saxeli,imgsrc,gvari,imgsize FROM users WHERE username = '"+ c_user +"';")

            sruli = kurs.fetchone()
            aidi = sruli[0]
            saxeli = sruli[1]
            gvari = sruli[3]

            pfp = sruli[2]
            pfp_size = sruli[4]
            



            u_aidi = data["aidi"]
            u_saxeli = data["name"]

            kurs.execute("SELECT id FROM dms WHERE  (user_one = '"+ str(aidi) +"' AND user_two = '"+ str(u_aidi) +"') OR (user_one = '"+ str(u_aidi) +"' AND user_two = '"+ str(aidi) +"'); ")

            dmf =kurs.fetchall()

            # if dmf == None:
            if dmf == []:
            


                kurs.execute("SELECT imgsrc FROM users WHERE id = "+str(u_aidi)+" ;")

                u_sruli = kurs.fetchone()
                u_pfp = u_sruli[0]


                #	last_message_content	last_message_sender_id	last_message_sender_name	user_one	user_two	
                kurs.execute("INSERT INTO dms(user_one,user_two,last_message_time) VALUES("+ str(aidi) +","+ str(u_aidi) +","+ str(int(time.time())) +");")
                db.commit()
                # kurs.execute("SELECT id FROM dms ORDER BY id DESC;")
                chat_aidi = kurs.lastrowid #kurs.fetchone()[0]
                
            else:
                chat_aidi = dmf[0]

            print(chat_aidi)


           
            msg = json.dumps({"chat_aidi" : sock_antixss(str(chat_aidi)),"contact_saxeli" : sock_antixss(saxeli),"contact_gvari" : sock_antixss(gvari),"starter_id" : sock_antixss(str(aidi)), "type" : "start_chat", "contact_dasaxeleba" : sock_antixss(c_user), "contact_pfp" : sock_antixss(pfp), "contact_pfp_size" : sock_antixss(pfp_size)})

            aiemi =  "i_am_"+str(u_aidi)
            # join_room(aiemi)
            print("gavugzavnet request otaxs :"+ aiemi + "!",msg)
            send(msg,broadcast=True,room=aiemi)
            send(msg)
            # return str(chat_aidi)


@socketio.on("disconnect")
def disconnect():
    # db = mysql.connector.connect(
    #             host=host,
    #             user=user,
    #             passwd = passwd,
    #             database= database
    # )

    kurs = db.cursor()
    print("disconnected")
    otaxi = conn_users[request.sid]["status_broadcast_otaxi"]
    disconnecter_c_user = conn_users[request.sid]["c_user"]
    del  conn_users[request.sid]
    disconnecter_disconnected = True
    for i in conn_users:
        if conn_users[i]["c_user"] == disconnecter_c_user:
            disconnecter_disconnected = False
    if disconnecter_disconnected:
        
        kurs.execute("UPDATE users SET status = '0' WHERE id = "+ str(otaxi).split("_")[2] +"  ;")
        db.commit()
        msg = json.dumps({"type" : "status","status_type" : "offline","user" : sock_antixss(otaxi)})
        # send("offline " + otaxi,broadcast=True,room=otaxi)

        send(msg,broadcast=True,room=otaxi)


@app.route("/dm_filesupload/<dm_aidi>/<sender_id>/<replition_id>",methods=["GET","POST"])
def dm_filesupload(dm_aidi,sender_id,replition_id):
    # db = mysql.connector.connect(
    #             host=host,
    #             user=user,
    #             passwd = passwd,
    #             database= database
    # )


    kurs = db.cursor()
    c_user = request.cookies.get("c_user")
    xs = request.cookies.get("xs")
    if auth(c_user,xs) == True:
        kurs.execute("SELECT id FROM users WHERE username = %(c_user)s",{"c_user" : c_user})
        kursf = kurs.fetchone()
        aidi = kursf[0]
        if request.form["csrftk"] == csrftoks[int(aidi)]:
        # if True:
            sent_file_ls = []

            for i in request.files:
                # print(request.files[i].filename,"hands",request.files[i].filename=="",request.files[i].filename==None)
                if request.files[i].filename != "":
                    dtype = request.files[i].filename.split(".")[len(request.files[i].filename.split("."))-1]

                    if ( dtype in ["jpg","jpeg","png"]):
                        dttype = "img"
                    elif ( dtype in ["mov","mp4","wav"]):
                        dttype = "vid"
                    else:
                        dttype = "file"

                    # bolo_file_id+=1
                    bolo_file_id = random.randint(100000000000000000000000000000000000000000000000000000,1000000000000000000000000000000000000000000000000000000)
                    loc ="static/dm_files/dm_file_" + str(dm_aidi) + "_" + str(bolo_file_id) + "." + dtype
                    request.files[i].save(cwd+loc)
                    deiti = str(datetime.datetime.now())

                    print(replition_id)
                    if replition_id != "none":
                        reply_to_msgid = str(int(replition_id))
                        
                        kurs.execute("INSERT INTO dm_msgs(message,sender_id, message_type , dmchat_id,message_date,message_dtype,reply_to_msgid) VALUES('"+ loc +"',"+ str(sender_id) +",'dm',"+ str(dm_aidi) +",'"+ str(deiti) +"','"+ dttype +"',"+ reply_to_msgid +");")
                    else:
                        kurs.execute("INSERT INTO dm_msgs(message,sender_id, message_type , dmchat_id,message_date,message_dtype) VALUES('"+ loc +"',"+ str(sender_id) +",'dm',"+ str(dm_aidi) +",'"+ str(deiti) +"','"+ dttype +"');")
                    
                    
                    bolor = kurs.lastrowid
                    sent_file_dat = {"file_loc" : loc, "sender_id" : str(sender_id), "msg_id" : bolor, "msg_count" : i,"dttype" : dttype}
                    sent_file_ls.append(sent_file_dat)
        
                    

            db.commit()
            return json.dumps(sent_file_ls)







@app.route("/user_wide_agwera_update",methods=["GET","POST"])
def user_wide_agwera_update():
    # db = mysql.connector.connect(
    #             host=host,
    #             user=user,
    #             passwd = passwd,
    #             database= database
    # )

    kurs = db.cursor()
    c_user = request.cookies.get("c_user")
    xs = request.cookies.get("xs")
    if auth(c_user,xs) == True:
        
        u_username = request.form.get("u_username")
        aboutme  = request.form.get("aboutme")
        ganatleba = request.form.get("ganatleba")
        if c_user == u_username:
            kurs.execute("SELECT id FROM users WHERE username = '"+u_username+"'; ")
            kursd = kurs.fetchone()
            if kursd != None:
                aidi = kursd[0]
                kurs.execute("UPDATE lancer_params SET about_me = '"+aboutme +"' WHERE aidi = "+ str(aidi) +";")
                kurs.execute("UPDATE lancer_params SET ganatleba = '"+ganatleba +"' WHERE aidi = "+ str(aidi) +";")
                db.commit()


                return "success"
            #lancer_params
        else:
            return "შეცდომა, გთხოვთ ცადოთ თავიდან"
        



@app.route("/user_main_info_update",methods=["GET","POST"])
def user_main_info_update():
    
    # db = mysql.connector.connect(
    #             host=host,
    #             user=user,
    #             passwd = passwd,
    #             database= database
    # )

    kurs = db.cursor()
    c_user = request.cookies.get("c_user")
    xs = request.cookies.get("xs")
    if auth(c_user,xs) == True:
        
        u_username = request.form.get("u_username")
        saxeli = request.form.get("saxeli").strip()
        gvari = request.form.get("gvari").strip()
        sfero = request.form.get("sfero").strip()
        if c_user == u_username:

            if sfero != "აირჩიეთ სფერო":
                if sfero in  ["აირჩიეთ სფერო","მუსიკა/აუდიო","ცხოვრებისეული","წერა და თარგმანი","ვიდეო და ანიმირება","ტექნოლოგია","მონაცემები","ბიზნესი","ციფრული მარკეტინგი","გრაპიკა და დიზაინი"]:
                    if len(saxeli) >=2 :
                        if len(gvari) >= 2:
                            if len(saxeli) < 15:
                                if len(gvari) <20:
                                    kurs.execute("UPDATE users SET saxeli = '"+ saxeli+"' WHERE username = '"+ u_username +"';")
                                    kurs.execute("UPDATE users SET gvari = '"+ gvari +"' WHERE username = '"+ u_username +"';")
                                    kurs.execute("UPDATE users SET sfero = '"+ sfero+"' WHERE username = '"+ u_username +"';")
                                    db.commit()
                                    return "success"
                                else:
                                    return "ძალიან გრძელი გვარი"
                            else:
                                return "ძალიან გრძელი სახელი"
                        else:
                            return "გთხოვთ შეიყვანოთ გვარი"

                    else:
                        return "გთხოვთ შეიყვანოთ სახელი"

                else:
                    return "შეცდომა, გთხოვთ ცადოთ თავიდან"
            else:
                return "გთხოვთ აირჩიოთ სფერო"
        else:
            return "შეცდომა, გთხოვთ ცადოთ თავიდან"
        

@app.route("/save_new_record",methods=["GET","POST"])
def save_new_record():
    if request.cookies.get("c_user") != None and request.cookies.get("xs") != None:
        c_user = request.cookies.get("c_user")
        xs = request.cookies.get("xs")
        if auth(c_user,xs) == True:
            # db = mysql.connector.connect(
            #     host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )
            kurs = db.cursor(buffered=True)            
            
            for i in json.loads(request.form["hist_records"]):

                ser_histo_rec_satauri = i["saxeli"]
                ser_histo_rec_agwera = i["agwera"]
                ser_histo_rec_tipi = i["tipi"]
                servisis_id = i["service_id"]
                try:
                    ser_histo_rec_dro = int(i["dro"])
                except:
                    ser_histo_rec_dro = 0
                try:
                    ser_histo_rec_fasi = int(i["fasi"])
                except:

                    ser_histo_rec_fasi = 0


                if len(ser_histo_rec_satauri) > 0:
                    if len(ser_histo_rec_agwera) > 0:
                        if (ser_histo_rec_tipi in ["ჩემი პროექტი","Freelancing პროექტი","Full-Time","სხვა"]):
                            if ((ser_histo_rec_dro >= ser_histo_rec_dro)):
                                
                                kurs.execute("INSERT INTO servisebis_history(service_id,saxeli,description,xani,tipi,fasi) VALUES("+ servisis_id +",'"+ser_histo_rec_satauri+"','"+ ser_histo_rec_agwera +"','"+str(ser_histo_rec_dro)+"','"+ ser_histo_rec_tipi +"','"+ str(ser_histo_rec_fasi) +"');")
                                # db.commit()

            db.commit()
            return "success"

                                

@app.route("/save_record",methods=["GET","POST"])
def save_record():
    if request.cookies.get("c_user") != None and request.cookies.get("xs") != None:
        c_user = request.cookies.get("c_user")
        xs = request.cookies.get("xs")

        if auth(c_user,xs) == True:
            # db = mysql.connector.connect(
            #     host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )
            kurs = db.cursor(buffered=True) 

       

            kurs.execute("SELECT id FROM users WHERE username = '"+ c_user+"';")
            kurs_owner_f = kurs.fetchone()
            owner_id = kurs_owner_f[0]


            
            #for i in json.loads(request.form["hist_records"]):

            i = request.form


            ser_histo_rec_satauri = i["saxeli"]
            ser_histo_rec_agwera = i["agwera"]
            ser_histo_rec_tipi = i["tipi"]
            servisis_id = i["service_id"]

            therecid = i["therecid"]
            try:
                ser_histo_rec_dro = int(i["dro"])
            except:
                ser_histo_rec_dro = 0
            try:
                ser_histo_rec_fasi = int(i["fasi"])
            except:

                ser_histo_rec_fasi = 0


            if len(ser_histo_rec_satauri) > 0:
                if len(ser_histo_rec_agwera) > 0:
                    if (ser_histo_rec_tipi in ["ჩემი პროექტი","Freelancing პროექტი","Full-Time","სხვა"]):
                        if ((ser_histo_rec_dro >= ser_histo_rec_dro)):
                            
                            kurs.execute("UPDATE servisebis_history SET saxeli = '"+ser_histo_rec_satauri +"'  WHERE id = "+ therecid +" AND owner_id = "+ str(owner_id) +"; ")
                            kurs.execute("UPDATE servisebis_history SET description = '"+ser_histo_rec_agwera +"'  WHERE id = "+ therecid +" AND owner_id = "+ str(owner_id) +"; ")
                            kurs.execute("UPDATE servisebis_history SET tipi = '"+ser_histo_rec_tipi +"'  WHERE id = "+ therecid +" AND owner_id = "+ str(owner_id) +"; ")

                            kurs.execute("UPDATE servisebis_history SET xani = '"+str(ser_histo_rec_dro) +"'  WHERE id = "+ therecid +" AND owner_id = "+ str(owner_id) +"; ")
                            kurs.execute("UPDATE servisebis_history SET fasi = '"+str(ser_histo_rec_fasi) +"'  WHERE id = "+ therecid +" AND owner_id = "+ str(owner_id) +"; ")
                            #kurs.execute("INSERT INTO servisebis_history(service_id,saxeli,description,xani,tipi,fasi) VALUES("+ servisis_id +",'"+ser_histo_rec_satauri+"','"+ ser_histo_rec_agwera +"','"+str(ser_histo_rec_dro)+"','"+ ser_histo_rec_tipi +"','"+ str(ser_histo_rec_fasi) +"');")
                            

                            

            db.commit()
            return "success"



            


@app.route("/create_new_service")
def create_new_service():
    if request.cookies.get("c_user") != None and request.cookies.get("xs") != None:
        c_user = request.cookies.get("c_user")
        xs = request.cookies.get("xs")
        if auth(c_user,xs) ==   True:
            # db = mysql.connector.connect(
            #     host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )
            kurs = db.cursor(buffered=True)

            kurs.execute("SELECT id,saxeli,imgsrc,imgsize,angarishi,join_time FROM users WHERE username = '" + c_user  +"';")
            
            

            kursf = kurs.fetchone()
            if kursf != None:
                aidi = kursf[0]
                straidi = str(aidi)

                saxeli = kursf[1]
                imgsrc = kursf[2]
                imgsize = kursf[3]
                fuli = kursf[4]
                join_time = kursf[5]
                my_profile_link =  c_user
                cuser = c_user

                numeracia = request.args.get("num")
                the_service = request.args.get("service")
                # notifications_box
                kurs.execute("SELECT user_one_seen FROM dms WHERE user_one = "+ str(aidi) +";")
                kurs_one = kurs.fetchall()
                kurs.execute("SELECT user_two_seen FROM dms WHERE user_two = "+ str(aidi) +";")
                kurs_two = kurs.fetchall()

                kurs_united = kurs_one + kurs_two
                message_notification_value = 0
                for i in kurs_united:
                    message_notification_value+= i[0]
                if message_notification_value > 9:
                    message_notification_value_shortened = "9+"
                else:
                    message_notification_value_shortened = str(message_notification_value)
                message_notification_value = str(message_notification_value)


                # mailbox
                kurs.execute("SELECT * FROM notifications WHERE notification_recipient_id = "+ str(aidi) +" OR (notification_recipient_id = 0 AND notification_time > "+ str(join_time) +") ORDER BY id DESC;")
                nots = np.array(kurs.fetchall())
                not_count = 0

                for i in nots:
                    if int(i[8]) == 0:
                        not_count+=1

                if not_count > 9:
                    not_count_markup = "9+"
                else:
                    not_count_markup = str(not_count)


                    




                if the_service == "new":


                    general = "false"
                    desc_and_exp = "false"
                    points = "false"
                    files = "false"

                    
                    #dziritadi_scr = Markup("""general.className = "nav_tab_anim nav_tab"; general.onclick = function(){window.location.href = "/create_new_service?num=1&service='""" + servisis_id + """';} """)

                        
                        

                    

                    dziritadi_scr = """ general.style.opacity = 0.5; """

                    agwera_da_gamocdileba_scr = """ desc_and_exp.style.opacity = 0.5;"""

                    pointebi_src = "points.style.opacity = 0.5;"

                    files_scr = """ files.style.opacity = 0.5; """


                    
                    
                    # else:
                    #     dziritadi_scr = """ general.style.opacity = 0.5; """

                    #     agwera_da_gamocdileba_scr = """ desc_and_exp.style.opacity = 0.5;"""

                    #     pointebi_src = "points.style.opacity = 0.5;"

                    #     files_scr = """ files.style.opacity = 0.5; """
                    csrftk = csrftok(int(straidi))
                    return render_template("create_new_service.html",straidi=straidi,saxeli=saxeli,imgsrc=imgsrc,imgsize=imgsize,fuli=fuli,my_profile_link=my_profile_link      ,dziritadi_scr=dziritadi_scr, agwera_da_gamocdileba_scr=agwera_da_gamocdileba_scr , pointebi_src=pointebi_src,files_scr=files_scr,
            message_notification_value=message_notification_value, message_notification_value_shortened=message_notification_value_shortened,
            not_count=str(not_count),not_count_markup=not_count_markup,csrftk=csrftk)
                else:

                    if True:
                        csrftk = csrftok(int(straidi))
                        servisis_id = the_service
                        nomeri = int(numeracia)

                        kurs.execute("SELECT * FROM servisebi WHERE id = "+ str(servisis_id)   +";")

                        


                        # #agwera da input ert flex rowshi, pirveli basic info, meore paketebi da pointebi, mesame max_clientebi da history
                        # kurs.execute("SELECT * FROM turebi WHERE owner_id = "+ str(aidi) +";")

                        kursf = kurs.fetchone()
                        if kursf != None:
                            service_id = kursf[0]

                            service_pfp = kursf[10]

                            zuratebi = kursf[19]
                            
                            owner_id = kursf[9]

                            if owner_id == aidi:


                                if kursf[20] == None:
                                    max_clients = ""
                                else:
                                    max_clients = str(kursf[20])



                                kurs.execute("SELECT * FROM servisebis_history WHERE service_id = "+ str(service_id) +";")

                                kurs_s = kurs.fetchone()

                                kurs.execute("SELECT * FROM  points WHERE service_id = "+ str(service_id) +";")

                                kurs_po_l = [i for i in kurs]
                                
                                service_id = kursf[0]

                                sfero = kursf[5]
                                subsfero = kursf[6]
                                
                                if (kursf[1] == None or kursf[5] == None or kursf[6] == None or kursf[14] == None):
                                    general = "false"
                                else:
                                    general = "true"
                                

                                if (kursf[2] == None  ):
                                    
                                    desc_and_exp = "false"
                                else:
                                    
                                    desc_and_exp = "true"

                                if kursf[2] == None:
                                    service_agwera = ""
                                else:
                                    service_agwera = kursf[2]
                                

                                if (kursf[3] == None or kursf[16] == None):
                                    points = "false"
                                else:
                                    points = "true"
                                
                                if(kursf[15] == None):
                                    files = "false"
                                else:
                                    files = "true"

                                if kursf[3] != None:
                                    minfasi = float(kursf[3])
                                else:
                                    minfasi = 0.00 

                                if kursf[16] != None:
                                    mindro = int(kursf[16])
                                else:
                                    mindro = 0


                                sminfasi = str(minfasi)
                                smindro = str(mindro)


                                maxfasi = kursf[17]
                                maxdro = kursf[18]

                                
                            #if nomeri == 1:



                                # if general == "true":
                                #     dziritadi_scr = Markup("""general.className = "nav_tab_anim nav_tab"; general.onclick = function(){window.location.href = "/create_new_service?num=1&service='""" + servisis_id + """';} """)
                                # else:
                                #     dziritadi_scr = """ general.style.opacity = 0.5; """

                                # if desc_and_exp == "true":
                                #     agwera_da_gamocdileba_scr = Markup("""desc_and_exp.className = "nav_tab_anim nav_tab"; desc_and_exp.onclick = function(){window.location.href = '/create_new_service?num=2&service="""+ servisis_id +"""';} """)

                                # else:
                                #     agwera_da_gamocdileba_scr = """ desc_and_exp.style.opacity = 0.5;"""

                                # if points == "true":
                                #     pointebi_src = Markup("""points.className = "nav_tab_anim nav_tab"; points.onclick = function(){window.location.href = '/create_new_service?num=3&service="""+ servisis_id +"""';}  """)
                                # else:
                                #     pointebi_src = "points.style.opacity = 0.5;"

                                
                                # if files == "true":
                                #     files_scr = Markup(""" files.className = "nav_tab_anim nav_tab"; files.onclick =  function(){window.location.href = '/create_new_service?num=4&service="""+ servisis_id +"""';} """)
                                # else:
                                #     files_scr = """ files.style.opacity = 0.5; """


                                service_id_js = str(service_id)
                                if general == "true":
                                    dziritadi_scr = Markup("""general.className = "nav_tab_anim nav_tab"; general.onclick = function(){window.location.href = '/create_new_service?num=1&service=""" + servisis_id + """';} """)

                                    agwera_da_gamocdileba_scr = Markup("""desc_and_exp.className = "nav_tab_anim nav_tab"; desc_and_exp.onclick = function(){window.location.href = '/create_new_service?num=2&service="""+ servisis_id +"""';} """)

                                    
                                    if desc_and_exp == "true":
                                        agwera_da_gamocdileba_scr = Markup("""desc_and_exp.className = "nav_tab_anim nav_tab"; desc_and_exp.onclick = function(){window.location.href = '/create_new_service?num=2&service="""+ servisis_id +"""';} """)
                                        pointebi_src = Markup("""points.className = "nav_tab_anim nav_tab"; points.onclick = function(){window.location.href = '/create_new_service?num=3&service="""+ servisis_id +"""';}  """)
                                        if points == "true":
                                            pointebi_src = Markup("""points.className = "nav_tab_anim nav_tab"; points.onclick = function(){window.location.href = '/create_new_service?num=3&service="""+ servisis_id +"""';}  """)
                                            files_scr = Markup(""" files.className = "nav_tab_anim nav_tab"; files.onclick =  function(){window.location.href = '/create_new_service?num=4&service="""+ servisis_id +"""';} """)



                                        else:


                                            

                                            files_scr = """ files.style.opacity = 0.5; """

                                        

                                        
                                
                                    else:

                                        
                                        

                                        pointebi_src = "points.style.opacity = 0.5;"

                                        files_scr = """ files.style.opacity = 0.5; """
                                    
                                    
                                    #kursf[1] == None or kursf[5] == None or kursf[6] == None or kursf[14] == None
                                    satauri_value = kursf[1]
                                    sfero_value = kursf[5]
                                    subsfero_value = kursf[6]

                                    tags_value = kursf[14] 
                                    tags_value_js = Markup(tags_value + ";")

                                    #return render_template("create_template1.html",saxeli=saxeli,imgsrc=imgsrc,imgsize=imgsize,fuli=fuli,my_profile_link=my_profile_link      ,dziritadi_scr=dziritadi_scr, agwera_da_gamocdileba_scr=agwera_da_gamocdileba_scr , pointebi_src=pointebi_src,files_scr=files_scr,satauri_value=satauri_value,sfero_value=sfero_value,subsfero_value=subsfero_value,tags_value=tags_value_js,service_id=service_id_js)
                                    



                                
                                
                                else:
                                    dziritadi_scr = """ general.style.opacity = 0.5; """

                                    agwera_da_gamocdileba_scr = """ desc_and_exp.style.opacity = 0.5;"""

                                    pointebi_src = "points.style.opacity = 0.5;"

                                    files_scr = """ files.style.opacity = 0.5; """


                                


                                if numeracia == "1":
                                    if general == "true":

                                        return render_template("create_template1.html",straidi=straidi,saxeli=saxeli,imgsrc=imgsrc,imgsize=imgsize,fuli=fuli,my_profile_link=my_profile_link      ,dziritadi_scr=dziritadi_scr, agwera_da_gamocdileba_scr=agwera_da_gamocdileba_scr , pointebi_src=pointebi_src,files_scr=files_scr,satauri_value=satauri_value,sfero_value=sfero_value,subsfero_value=subsfero_value,tags_value=tags_value_js,service_id=service_id_js,
            message_notification_value=message_notification_value, message_notification_value_shortened=message_notification_value_shortened,
            not_count=str(not_count),not_count_markup=not_count_markup,csrftk=csrftk)
                                    #return render_template("create_new_service.html",saxeli=saxeli,imgsrc=imgsrc,imgsize=imgsize,fuli=fuli,my_profile_link=my_profile_link      ,dziritadi_scr=dziritadi_scr, agwera_da_gamocdileba_scr=agwera_da_gamocdileba_scr , pointebi_src=pointebi_src,files_scr=files_scr)
                            
                                elif numeracia == "2":
                                    if general == "true":
                                        if desc_and_exp == "true":
                                            pass
                                        else:
                                            pass
                                        recordni = ""
                                        excess_script = ""
                                        kurs.execute("SELECT * FROM servisebis_history WHERE service_id = "+ servisis_id +" AND owner_id = "+ str(aidi) +";")
                                        for i in kurs:
                                            record_id = i[0]
                                            satauri = i[2]

                                            agwera = i[3]
                                            
                                            if i[6] != None:
                                                fasi = i[6]
                                            else:
                                                fasi = 0

                                            if i[4] != None:
                                                dro = i[4]
                                            else:
                                                dro = 0

                                            
                                            tipi = i[5]

                                        
                                            kvira = 7
                                            if dro > 0:
                                                if dro > (kvira):
                                                    tve = kvira * 4
                                                    if dro > tve:
                                                        dros = "- "+str(dro/(tve)).split(".")[0] + " თვე"
                                                    else:

                                                        dros = "- "+str(dro/(kvira)).split(".")[0] + " კვირა"
                                                else:
                                                    dros = "- "+str(dro).split(".")[0] + "დღე"
                                            else:
                                                dros = ""
                                            

                                            recordni+= Markup('<div id = "'+ str(i[0]) +'" class="mkwrivi"><p id = "record_mkwrivi_satauri_'+ str(i[0]) +'" class="record_mkwrivi_satauri">') + satauri + Markup('</p> <p id = "ful_dro_'+ str(i[0 ]) +'" class = "ful_dro">')+ str(fasi) + Markup("<span style = 'color:lightgreen;'>$</span>") +" " + dros  + Markup('</p> <div id = "rec_opt_btn_'+ str(record_id) +'" class = "rec_options_btn"></div> </div>')
                                            excess_script+= Markup("""
                                            var rec_opt_bar"""+ str(record_id) + """  = document.createElement("div");
                                            rec_opt_bar"""+ str(record_id) + """.className = "rec_opt_bar";
                                            rec_opt_bar"""+ str(record_id) + """.id = 'rec_opt_btn_"""+ str(record_id) + """'
                                            

                                            var rec_opt_btn_"""+ str(record_id) + """ = document.getElementById('rec_opt_btn_"""+ str(record_id) + """');

                                            rec_opt_btn_"""+ str(record_id) + """.aidi = '""" + str(record_id) +"""';
                                            rec_opt_btn_"""+ str(record_id) + """.satauri = '""" + satauri +"""';
                                            rec_opt_btn_"""+ str(record_id) + """.agwera = '""" + agwera +"""';
                                            rec_opt_btn_"""+ str(record_id) + """.tipi = '""" + tipi +"""';

                                            rec_opt_btn_"""+ str(record_id) + """.fasi = '""" + str(fasi) +"""';
                                            rec_opt_btn_"""+ str(record_id) + """.dro = '""" + str(dro) +"""';

                                            

                                            rec_opt_btn_"""+ str(record_id) + """.onclick = function(){
                                                experience_system.removeChild(records_list);
                            
                                                var saxeli = document.createElement("input");

                                                var unregistered_record = document.createElement("div");
                                                unregistered_record.className = "unregistered_record";

                                                
                                                saxeli.placeholder = "სახელი";
                                                saxeli.className = "unregistered_record_saxeli_input";
                                                saxeli.value = rec_opt_btn_"""+ str(record_id) + """.satauri;


                                                var agwera = document.createElement("textarea")
                                                agwera.className = "record_agwera_input";
                                                agwera.placeholder = "აღწერა";
                                                agwera.value = rec_opt_btn_"""+ str(record_id) + """.agwera;

                                                var record_tipi = new MyDropdown("ტიპი",["ჩემი პროექტი","Full-Time","Freelancing პროექტი","სხვა"],unregistered_record,width=30);

                                                record_tipi.rec_inputs = "closed";



                                                record_tipi.place(20,30);
                                                
                                                record_tipi.setValue(rec_opt_btn_"""+ str(record_id) + """.tipi);
                                                

                                                let fuli_input = document.createElement("input");
                                                fuli_input.style.color = "green";
                                                fuli_input.placeholder = "გამომუშავებული თანხა($)";
                                                fuli_input.type = "number";
                                                fuli_input.id = "money_input";
                                                fuli_input.className = "samushao_dro_input rec_t_input";
                                                fuli_input.value = rec_opt_btn_"""+ str(record_id) + """.fasi;
                                                

                                                let samushao_dro_input = document.createElement("input");
                                                samushao_dro_input.placeholder = "სამუშაო დრო(დღე)";
                                                samushao_dro_input.className = "samushao_dro_input rec_t_input";
                                                samushao_dro_input.type = "number";
                                                samushao_dro_input.value = rec_opt_btn_"""+ str(record_id) + """.dro;
                                                
                                                let rec_washlis_button = document.createElement("div");
                                                
                                                rec_washlis_button.className = "rec_washlis_button";
                                                rec_washlis_button.id = 'rec_washla_btn_"""+ str(record_id) + """';

                                                rec_washlis_button.innerHTML = "წაშლა";

                                                function GeoWarning(question,ara,ki,maini="main"){
                                                    document.getElementById(maini).style.opacity = "0.2";
                                                    document.getElementById("navbar").style.opacity = "0.2";
                                                    var rec_washla_gafrtxileba_div = document.createElement("rec_washla_gafrtxileba_div");
                                                    document.body.append(rec_washla_gafrtxileba_div);
                                                    rec_washla_gafrtxileba_div.className = "rec_washla_gafrtxileba_div";

                                                    let shekitxva = document.createElement("p");
                                                    shekitxva.innerHTML = question;
                                                    shekitxva.className = "rec_washla_gafrtxileba_shekitxva";

                                                    rec_washla_gafrtxileba_div.append(shekitxva);

                                                    let rec_washla_gafrtxileba_buttonsdiv = document.createElement("div");
                                                    rec_washla_gafrtxileba_buttonsdiv.className = "rec_washla_gafrtxileba_buttonsdiv";

                                                    rec_washla_gafrtxileba_div.append(rec_washla_gafrtxileba_buttonsdiv);

                                                    let rec_washla_kibutton = document.createElement("div");
                                                    let rec_washla_arabutton = document.createElement("div");

                                                    rec_washla_kibutton.innerHTML = "კი";
                                                    rec_washla_arabutton.innerHTML = "არა";

                                                    rec_washla_kibutton.className = "rec_washla_kibutton rec_washla_button";
                                                    rec_washla_arabutton.className = "rec_washla_arabutton rec_washla_button";


                                                    rec_washla_gafrtxileba_buttonsdiv.append(rec_washla_arabutton);
                                                    rec_washla_gafrtxileba_buttonsdiv.append(rec_washla_kibutton);

                                                    function window_gauqmeba(){
                                                        document.getElementById(maini).style.opacity = "1";
                                                        document.getElementById("navbar").style.opacity = "1";
                                                        document.body.removeChild(rec_washla_gafrtxileba_div);
                                                        
                                                    }
                                                    
                                                    rec_washla_arabutton.addEventListener("click",ara);
                                                    rec_washla_arabutton.addEventListener("click",window_gauqmeba);

                                                    rec_washla_kibutton.addEventListener("click",ki);
                                                    rec_washla_kibutton.addEventListener("click",window_gauqmeba);

                                                    
                                                    

                                                
                                                }

                                                rec_washlis_button.onclick = function(){
                                                    function arastivs(){

                                                        

                                                    }
                                                    function kistvis(){
                                                        

                                                        $.ajax({
                                                            data : {
                                                                "therecid" : rec_opt_btn_"""+ str(record_id) + """.aidi


                                                            },
                                                            url : "/delete_record",
                                                            type : "POST",
                                                            dataType : "text",
                                                            success : function(data){
                                                                if(data == "success"){
                                                                    record_creation_gauqmeba();
                                                                    records_list.removeChild(document.getElementById(rec_opt_btn_"""+ str(record_id) + """.aidi));
                                                                    
                                                                }
                                                                
                                                            }
                                                        });



                                                    }
                                                    GeoWarning("დარწმუნებული ხართ რომ გინდათ რომ ეს რექორდი წაშალოთ?",ara=arastivs,ki=kistvis);
                                                }
                                                

                                                let rec_shenaxva_button = document.createElement("div");
                                                rec_shenaxva_button.className = "rec_shenaxva_button";
                                                rec_shenaxva_button.innerHTML = "შენახვა";

                                                let cancell_button = document.createElement("div");
                                                cancell_button.id = "cancel_button";

                                                function record_creation_gauqmeba(){
                                                    create_new_record_btn.sheqmna_started = "false";
                                                    experience_system.append(records_list);
                                                    experience_system.removeChild(unregistered_record); 

                                                }
                                                cancell_button.onclick = record_creation_gauqmeba;

                                                function fuli_input_con(){
                                                    let fuli = fuli_input.value;
                                                    let samushaos_dro = samushao_dro_input.value;

                                                    if(fuli<0){
                                                        fuli_input.value = fuli*-1;
                                                    }
                                                    if(samushaos_dro < 0){
                                                        samushao_dro_input.value = samushaos_dro *-1;
                                                    }
                                                }
                                                setInterval(fuli_input_con,1);

                                                function rec_saving(){

                                                    if(saxeli.value.length < 1){
                                                        erori("გთხოვთ მიუთითოთ სახელი",2,90);
                                                    }
                                                    else if(agwera.value.length < 1){
                                                        erori("გთხოვთ მიუთითოთ აღწერა",2,90);
                                                    }
                                                    else if(record_tipi.value == "none"){
                                                        erori("გთხოვთ მიუთითოთ პროექტის ტიპი",2,90);

                                                    }
                                                    
                                                    
                                                    else{
                                                        record_creation_gauqmeba();
                                                        let data = {
                                                                "saxeli" : saxeli.value,
                                                                "agwera" : agwera.value,
                                                                "tipi" : record_tipi.value,
                                                                "dro" : samushao_dro_input.value,
                                                                "fasi" : fuli_input.value,
                                                                "service_id" : '{{service_id}}'
                                                            };
                                                        
                                                        
                                                        

                                                        
                                                        $.ajax({
                                                            data : {
                                                                "saxeli" : saxeli.value,
                                                                "agwera" : agwera.value,
                                                                "tipi" : record_tipi.value,
                                                                "dro" : samushao_dro_input.value,
                                                                "fasi" : fuli_input.value,
                                                                "service_id" : '{{service_id}}',
                                                                'therecid' : '"""+ str(record_id) +"""'
                                                            },
                                                            type : "POST",
                                                            dataType : "text",
                                                            url : "/save_record",
                                                            success : function(data){
                                                                
                                                                rec_opt_btn_"""+ str(record_id) + """.satauri = saxeli.value;
                                                                rec_opt_btn_"""+ str(record_id) + """.agwera = agwera.value;
                                                                rec_opt_btn_"""+ str(record_id) + """.tipi = record_tipi.value;
                                                                rec_opt_btn_"""+ str(record_id) + """.fasi = fuli_input.value;
                                                                rec_opt_btn_"""+ str(record_id) + """.dro = samushao_dro_input.value;


                                                                //record_tipi.setValue(record_tipi.value);

                                                                let mkwrivi = document.getElementById('"""+ str(i[0]) +"""');

                                                                let ful_dro = document.createElement("p");
                                                                ful_dro.className = "ful_dro";

                                                                if(data["fasi"] != ""){
                                                                    var fasi = fuli_input.value;
                                                                }
                                                                else{
                                                                    var fasi = "0";
                                                                }
                                                                
                                                                let fulnoudi = document.createTextNode(fasi);
                                                                let fulnoudi_dola = document.createElement("span");
                                                                fulnoudi_dola.innerHTML = "$";
                                                                fulnoudi_dola.style.color = "lightgreen";
                                                                
                                                                let dro = samushao_dro_input.value;
                                                                if(dro != ""){
                                                                    var prefix = " - " ;

                                                                    let kvira = 7;
                                                                    if(dro > (kvira)){
                                                                        let tve = kvira * 4
                                                                                if(dro > tve){
                                                                                    dros = String(dro/(tve)).split(".")[0] + " თვე";
                                                                                }
                                                                                    
                                                                                else{
                                                                                    dros = String(dro/(kvira)).split(".")[0] + " კვირა";
                                                                                }

                                                                                    
                                                                            
                                                                            
                                                                    }
                                                                    
                                                                    
                                                                            
                                                                
                                                                    else{
                                                                                dros = String(dro).split(".")[0] + "დღე";
                                                                        }
                                                                    }
                                                                else{
                                                                    var prefix = "" ;
                                                                    var dros = "";
                                                                }
                                                                
                                    
                                                                let dronoudi_txt =prefix +dros;

                                                                let dronoudi= document.createTextNode(dronoudi_txt);
                                                                


                                                                let rec_edit_btn = document.createElement("div");

                                                                rec_edit_btn.className = "rec_options_btn";

        
                                                                document.getElementById('record_mkwrivi_satauri_"""+ str(i[0]) +"""').innerHTML =saxeli.value;
                                                                document.getElementById('ful_dro_"""+ str(i[0]) +"""').innerHTML = fasi + "<span style = 'color:lightgreen;'>$</span>"+prefix + dros;


                                                            }
                                                        });
                                                        

                                                    }


                                            }
                                                rec_shenaxva_button.onclick = rec_saving;


                                                
                                                unregistered_record.append(rec_shenaxva_button);
                                                unregistered_record.append(rec_washlis_button);


                                                
                                                

                                                for(let i of record_tipi.dilementebi){
                                                    i.addEventListener("click",function(){
                                                        console.log(i.innerHTML);
                                                        
                                                        

                                                        if(record_tipi.rec_inputs == "closed"){
                                                            unregistered_record.append(fuli_input);
                                                            unregistered_record.append(document.createElement("br"));
                                                            unregistered_record.append(samushao_dro_input);
                                                            


                                                        }



                                                        record_tipi.rec_inputs = "open";
                                                        


                                                        
                                                        

                                                    }
                                                        
                                                    
                                                    );
                                                }
                                                


                                                
                                                experience_system.append(unregistered_record); 
                                                
                                                
                                                
                                                unregistered_record.append(cancell_button);

                                                unregistered_record.append(saxeli);
                                                unregistered_record.append(agwera);



                                                // dagchirdeba parentElement.insertBefore(newElement, parentElement.children[2]); https://stackoverflow.com/questions/5882768/how-to-append-a-childnode-to-a-specific-position
                                                        
                                                create_new_record_btn.sheqmna_started = "true";
                            }
                                            
                                            """)
                                        
                                
                                        # recordni
                                        return render_template("create_template2.html",straidi=straidi,service_agwera=service_agwera,excess_script=excess_script,recordni=recordni,saxeli=saxeli,imgsrc=imgsrc,imgsize=imgsize,fuli=fuli,my_profile_link=my_profile_link      ,dziritadi_scr=dziritadi_scr, agwera_da_gamocdileba_scr=agwera_da_gamocdileba_scr , pointebi_src=pointebi_src,files_scr=files_scr,satauri_value=satauri_value,sfero_value=sfero_value,subsfero_value=subsfero_value,tags_value=tags_value_js,service_id=service_id_js,
            message_notification_value=message_notification_value, message_notification_value_shortened=message_notification_value_shortened,
            not_count=str(not_count),not_count_markup=not_count_markup,csrftk=csrftk)
                                elif numeracia == "3":
                                    if general == "true":
                                        if desc_and_exp == "true":
                                            

                                            #<div id="po_divვოკალური ჰარმონია" class="po_div po_divვოკალური ჰარმონია"><input id="po_fasi_ვოკალური ჰარმონია" maxlength="10" placeholder="თანხა($)" class="po_fasi" disabled=""><input id="po_time_ვოკალური ჰარმონია" maxlength="3" placeholder="დღე" class="po_time" value="" disabled=""><input id="po_points_ვოკალური ჰარმონია" class="po_points" maxlength="3" value="35" disabled=""><div class="po_name">ვოკალური ჰარმონია</div><div class="select_point_button"><div id="select_point_button_img_ვოკალური ჰარმონია" class="select_point_button_img select_point_button_img_ვოკალური ჰარმონია" style="background-image: url(&quot;static/minus.jpg&quot;);"></div></div></div>

                                            #if True:
                                            kurs.execute("SELECT * FROM points WHERE service_id = "+ str(servisis_id) +" AND owner_id = "+ str(aidi) +";")

                                            if subsfero in pointis_subsferoebi:
                                            
                                            
                                                

                                                point_data_offc_ls = unselected_point_dict[subsfero]
                                                unselected_points_js = Markup(point_data_offc_ls)

                                                unselected_points_divs = ""
                                                selected_points_divs = ""

                                                points_ls_script = ""

                                                for i in json.loads(point_data_offc_ls):
                                                    unselected_points_divs+= Markup("<div id = 'po_div"+ i["name"] +"' class = 'po_div po_div"+ i["name"] +"'><input id = 'po_fasi_"+ i["name"] +"'  maxlength='10' placeholder = 'თანხა($)' class = 'po_fasi'><input id = 'po_time_"+ i["name"] +"'  maxlength='3' placeholder = 'დღე' class = 'po_time' value = '")+Markup("'><input id = 'po_points_"+ i["name"] +"' class = 'po_points' maxlength='3' value = '")+ i["points"] +Markup("'><div class = 'po_name'>") + i["name"] + Markup("</div><div class = 'select_point_button'><div id = 'select_point_button_img_"+ i["name"] +"' class = 'select_point_button_img select_point_button_img_"+ i["name"] +"'></div></div></div>" + "") + ""
        
                                                for i in kurs:
                                                    

                                                    # points_ls_script+=Markup("""points_ls.push({"name" : '"""+  str(i[6]) +"""',"points" : """+ str(i[1]) +""","dro" :'"""+ str(i[3]) + """',"fasi" : '"""+ str(i[2]) +"""' }); \n""" )


                                                    # points_ls_script+=Markup("""document.getElementById('select_point_button_img_"""+ i[6] +"""').addEventListener("click",ireturn); \n""")

                                                    points_ls_script+=Markup("""
                                                    document.getElementById('po_fasi_"""+ i[6] +"""').value = '"""+ str(i[2]) +"""';

                                                    document.getElementById('po_time_"""+ i[6] +"""').value = '"""+ str(i[3]) +"""';
                                                    document.getElementById('select_point_button_img_"""+ i[6] +"""').click(); \n""")
                                                

                                                    # selected_points_divs+=Markup('<div id="po_div'+i[6]  +'" class="po_div po_div'+i[6]  +'"><input id="po_fasi_'+i[6]  +'" maxlength="10" placeholder="თანხა($)" class="po_fasi" value = "'+ str(i[2])  +'$" disabled=""><input id="po_time_'+i[6]  +'" maxlength="3" placeholder="დღე" class="po_time" value="'+ str(i[3]) +'" disabled=""><input id="po_points_'+i[6]  +'" class="po_points" maxlength="3" value="'+ str(i[1]) +'" disabled=""><div class="po_name">'+i[6]  +'</div><div class="select_point_button"><div id="select_point_button_img_'+i[6]  +'" class="select_point_button_img select_point_button_img_'+i[6]  +'" style="') + Markup("""background-image: url('static/minus.jpg');"></div></div></div>""")
                                                    

                                                # selected_points_divs = ""
                                                
                                                return render_template("create_template3.html",straidi=straidi,max_clients=max_clients,service_id=service_id,saxeli=saxeli,imgsrc=imgsrc,imgsize=imgsize,fuli=fuli,my_profile_link=my_profile_link ,dziritadi_scr=dziritadi_scr, agwera_da_gamocdileba_scr=agwera_da_gamocdileba_scr , pointebi_src=pointebi_src,files_scr=files_scr                      , unselected_points_js=unselected_points_js ,unselected_points_divs=unselected_points_divs,minfasi=sminfasi,mindro=smindro,selected_points_divs=selected_points_divs , points_ls_script=points_ls_script,
            message_notification_value=message_notification_value, message_notification_value_shortened=message_notification_value_shortened,
            not_count=str(not_count),not_count_markup=not_count_markup,csrftk=csrftk)
                                            else:
                                                return render_template("create_template3_nop.html",straidi=straidi,max_clients=max_clients,service_id=service_id,saxeli=saxeli,imgsrc=imgsrc,imgsize=imgsize,fuli=fuli,my_profile_link=my_profile_link ,dziritadi_scr=dziritadi_scr, agwera_da_gamocdileba_scr=agwera_da_gamocdileba_scr , pointebi_src=pointebi_src,files_scr=Markup(""" files.className = "nav_tab_anim nav_tab"; files.onclick =  function(){window.location.href = '/create_new_service?num=4&service="""+ servisis_id +"""';} """),minfasi=sminfasi,mindro=smindro,
            message_notification_value=message_notification_value, message_notification_value_shortened=message_notification_value_shortened,
            not_count=str(not_count),not_count_markup=not_count_markup,csrftk=csrftk)
                                elif numeracia == "4":
                                    if general == "true":
                                        if desc_and_exp == "true":
                                            if points == "true":

                                                if service_pfp == None:
                                                    service_pfp_link = "static/services/upload_image_symbol.png"
                                                    profile_status_boolean = Markup("'false'")
                                                else:
                                                    service_pfp_link = "static/services/" + service_pfp
                                                    profile_status_boolean = Markup("'true'")
                                                
                                                if zuratebi != None:
                                                    suratebi = zuratebi
                                                else:
                                                    dixti = {}
                                                    for i in range(0,5):
                                                        dixti[str(i)] = "upload_image_symbol.png"
                                                    suratebi = json.dumps(dixti)


                                                suratebi = Markup(suratebi)
                                                


                                                



                                                return render_template("create_template4.html",straidi=straidi,cuser=cuser,profile_status_boolean=profile_status_boolean,suratebi=suratebi,service_pfp_link=service_pfp_link,service_id=service_id,saxeli=saxeli,imgsrc=imgsrc,imgsize=imgsize,fuli=fuli,my_profile_link=my_profile_link ,dziritadi_scr=dziritadi_scr, agwera_da_gamocdileba_scr=agwera_da_gamocdileba_scr , pointebi_src=pointebi_src,files_scr=files_scr,
            message_notification_value=message_notification_value, message_notification_value_shortened=message_notification_value_shortened,
            not_count=str(not_count),not_count_markup=not_count_markup,csrftk=csrftk)


@app.route("/service_profileupload/<serviceid>",methods=["GET","POST"])
def service_profileupload(serviceid):
    if(request.cookies.get("c_user") != None and request.cookies.get("xs") != None):
        c_user = request.cookies.get("c_user")
        xs = request.cookies.get("xs")
        if auth(c_user,xs) == True:
            

            # db = mysql.connector.connect(
            #     host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )
            kurs = db.cursor()

            kurs.execute("SELECT * FROM users WHERE username = '"+ c_user +"';")

            kursf = kurs.fetchone()
            aidi = kursf[0]


            kurs.execute("SELECT * FROM servisebi WHERE id = "+ str(serviceid) +" AND owner_id = "+ str(aidi) +";")
            kurse = kurs.fetchone()
            iebi = []
            iebi.append(kurse[0])
            iebi.append(kurse[1])
            iebi.append(kurse[2])
            iebi.append(kurse[3])
            iebi.append(kurse[5])
            iebi.append(kurse[16])
            iebi.append(kurse[23])
            iebi.append(kurse[24])
            iebi.append(kurse[20])
            iebi.append(kurse[17])
            iebi.append(kurse[18])


            if (None in iebi) == False:

                botoebi = kurse[19]
                
                #static/upload_image_symbol.png
                faili = request.files["faili"]
                


                if botoebi == None:
                    zuratebi = {}
                    

                    for i in request.files:
                        if i != "faili":
                            maxeli = request.files[i].filename
                            if maxeli != "":
                                tipi = maxeli.split(".")[len(maxeli.split("."))-1]
                                naxeli = str(aidi) + "_" +str(serviceid) +"_" + str(i) +"." + tipi
                                zuratebi[i] = naxeli

                                request.files[i].save(cwd+"static/services/" + naxeli)
                            else:
                                zuratebi[i] = "none"
                else:

                    totoebi = json.loads(botoebi)
                    zuratebi = {}
                    for i in request.files:
                        if i != "faili":
                            maxeli = request.files[i].filename
                            if maxeli != "":
                                tipi = maxeli.split(".")[len(maxeli.split("."))-1]
                                naxeli = str(aidi) + "_" +str(serviceid) +"_" + str(i) +"." + tipi
                                zuratebi[i] = naxeli

                                request.files[i].save(cwd+"static/services/" + naxeli)
                            else:
                                if totoebi[i] == "none":
                                    zuratebi[i] = "none"
                                else:
                                    zuratebi[i] = totoebi[i]
                    

                print(zuratebi)



                
                
                

                fn = faili.filename
                if fn != "":

                    tipi = fn.split(".")[len(fn.split("."))-1]
                    if (tipi in ["png","jpg","jpef"]):
                        failname = str(aidi) + "_" +str(serviceid) + "." + tipi
                        print(failname)
                        faili.save(cwd+"static/services/"+ failname)
                        kurs.execute("UPDATE servisebi SET profile = '"+ failname +"' WHERE id = "+ str(serviceid)+" AND owner_id = "+ str(aidi) +";")
                

                kurs.execute("UPDATE servisebi SET suratebi = '"+ json.dumps(zuratebi) +"' WHERE id = "+ str(serviceid)+" AND owner_id = "+ str(aidi) +";")
                
                kurs.execute("UPDATE servisebi SET status = 'active' WHERE id = "+ str(serviceid)+" AND owner_id = "+ str(aidi) +";")
                
                db.commit()

                return "success"


            

@app.route("/service_filesupload/<serviceid>",methods=["GET","POST"])
def service_filesupload():
    if(request.cookies.get("c_user") != None and request.cookies.get("xs") != None):
        c_user = request.cookies.get("c_user")
        xs = request.cookies.get("xs")
        if auth(c_user,xs) == True:


            faili = request.files["faili"]




@app.route("/delete_record",methods=["GET","POST"])
def delete_record():
    if(request.cookies.get("c_user") != None and request.cookies.get("xs") != None):
        c_user = request.cookies.get("c_user")
        xs = request.cookies.get("xs")

        if auth(c_user,xs) == True:
            # db = mysql.connector.connect(
            #     host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )
            kurs = db.cursor()
            kurs.execute("SELECT id FROM users WHERE username = '"+ c_user +"';")
            kursf = kurs.fetchone()

            if kursf != None:

                

                aidi = kursf[0]
                therecid = request.form["therecid"]
                
                kurs.execute("DELETE FROM servisebis_history WHERE id = "+ str(therecid) +" AND owner_id = '"+ str(aidi) +"';")

                db.commit()

                return "success"









@app.route("/create_new_service_ajax",methods=["GET","POST"])
def create_new_service_ajax():
    if request.cookies.get("c_user") != None and request.cookies.get("xs") != None:
        c_user = request.cookies.get("c_user")
        xs = request.cookies.get("xs")
        if auth(c_user,xs) == True:
                # db = mysql.connector.connect(
                # host=host,
                # user=user,
                # passwd = passwd,
                # database= database
                # )
                kurs = db.cursor()
                kurs.execute("SELECT id FROM users WHERE username = '"+ str(c_user)   +"';")
                kursf = kurs.fetchone()
                aidi = kursf[0]
                sfero = request.form["sfero"]
                subsfero = request.form["subsfero"]
                if sfero in ["მუსიკა/აუდიო","ცხოვრებისეული","წერა და თარგმანი","სოფთვერ დეველოპმენტი","ვიდეო და ანიმირება","ზოგადი ტექნოლოგია","მონაცემები","ციფრული მარკეტინგი","გრაპიკა და დიზაინი"]:

                    satauri = request.form["satauri"]

                    tags = request.form["tags"]

                    kurs.execute("INSERT INTO servisebi(satauri,offer_tipi,offer_subtipi,tags,owner_id) VALUES('"+satauri+"','"+ sfero +"','"+subsfero+"','"+ tags +"',"+str(aidi) +");")
                    print("INSERT INTO servisebi(satauri,offer_tipi,offer_subtipi,tags,owner_id) VALUES('"+satauri+"','"+ sfero +"','"+subsfero+"','"+ tags +"',"+str(aidi) +");")
                    
                    db.commit()
                    brzan = "SELECT id FROM servisebi WHERE owner_id = "+ str(aidi) +";"
                    kurs.execute(brzan)

                    
                    serlist = [i for i in kurs]

                    bolor = serlist[len(serlist)-1]

                    serid = bolor[0]
                    return "success " + str(serid)

@app.route("/save_new_service_1_ajax",methods=["GET","POST"])
def save_new_service_1_ajax():
    if request.cookies.get("c_user") != None and request.cookies.get("xs") != None:
        c_user = request.cookies.get("c_user")
        xs = request.cookies.get("xs")
        if auth(c_user,xs) == True:
                # db = mysql.connector.connect(
                # host=host,
                # user=user,
                # passwd = passwd,
                # database= database
                # )
                kurs = db.cursor()
                kurs.execute("SELECT id FROM users WHERE username = '"+ str(c_user)   +"';")
                kursf = kurs.fetchone()
                aidi = kursf[0]
                sfero = request.form["sfero"]
                subsfero = request.form["subsfero"]
                if sfero in ["მუსიკა/აუდიო","ცხოვრებისეული","წერა და თარგმანი","სოფთვერ დეველოპმენტი","ვიდეო და ანიმირება","ზოგადი ტექნოლოგია","მონაცემები","ციფრული მარკეტინგი","გრაპიკა და დიზაინი"]:

                    satauri = request.form["satauri"]

                    tags = request.form["tags"]
                    service_id = request.form["service_id"]
                    brzan = "SELECT id FROM servisebi WHERE owner_id = "+ str(aidi) +";"
                    #kurs.execute(brzan)

                    #kurs.execute("INSERT INTO servisebi(satauri,offer_tipi,offer_subtipi,tags,owner_id) VALUES('"+satauri+"','"+ sfero +"','"+subsfero+"','"+ tags +"',"+str(aidi) +");")
                    
                    kurs.execute("UPDATE servisebi SET satauri = '"+ satauri +"' WHERE id = "+ service_id +" AND owner_id = "+ str(aidi) +";")
                    kurs.execute("UPDATE servisebi SET offer_tipi = '"+ sfero +"' WHERE id = "+ service_id +" AND owner_id = "+ str(aidi) +";")
                    kurs.execute("UPDATE servisebi SET offer_subtipi = '"+ subsfero +"' WHERE id = "+ service_id +" AND owner_id = "+ str(aidi) +";")
                    kurs.execute("UPDATE servisebi SET tags = '"+ tags +"' WHERE id = "+ service_id +" AND owner_id = "+ str(aidi) +";")

                    db.commit()


                    return "success"


@app.route("/save_new_service_2_ajax",methods=["GET","POST"])
def save_new_service_2_ajax():
    if request.cookies.get("c_user") != None and request.cookies.get("xs") != None:
        c_user = request.cookies.get("c_user")
        xs = request.cookies.get("xs")
        if auth(c_user,xs) == True:
                # db = mysql.connector.connect(
                # host=host,
                # user=user,
                # passwd = passwd,
                # database= database
                # )
                kurs = db.cursor()
                kurs.execute("SELECT id FROM users WHERE username = '"+ str(c_user)   +"';")
                kursf = kurs.fetchone()
                aidi = kursf[0]

                service_description = request.form["service_description"]

                

                serid = str(request.form["service_id"])

                kurs.execute("SELECT owner_id FROM servisebi WHERE id = "+ serid  +";")

                owner_id = kurs.fetchone()[0]
                
                kurs.execute("UPDATE servisebi SET agwera = '"+  service_description +"' WHERE id = "+ serid+" AND owner_id = " + str(aidi)  +";")
                thedata = json.loads(request.form["thedata"])

                gamocdileba_fasi = 0

                gamocdileba_dro = 0
                

                record_list_array = thedata
                for i in record_list_array:
                    saxeli = i["saxeli"]
                    agwera = i["agwera"]
                    tipi = i["tipi"]
                    if len(i["dro"]) > 0:
                        dro = i["dro"]
                    else:
                        dro = "0"
                    if len(i["fasi"]) > 0:
                        
                        fasi = i["fasi"]
                    else:
                        fasi = "0"
                    service_id = i["service_id"]

                    if tipi in ["ჩემი პროექტი","Freelancing პროექტი","Full-Time","სხვა"]:
                        if int(aidi) == int(owner_id):
                            gamocdileba_fasi+=int(fasi)
                            gamocdileba_dro+=int(dro)
                            kurs.execute("INSERT INTO servisebis_history(service_id,saxeli,description,xani,tipi,fasi,owner_id) VALUES("+ str(service_id) +",'"+saxeli+"','"+ agwera+"',"+ str(dro) +",'"+ tipi +"',"+ str(fasi) +","+ str(aidi) +");")

                kurs.execute("UPDATE servisebi SET gamocdileba_fasi = "+ str(gamocdileba_fasi) +"  WHERE id = "+ serid+" AND owner_id = " + str(aidi)  +" ;")
                kurs.execute("UPDATE servisebi SET gamocdileba_time = "+ str(gamocdileba_dro) +"  WHERE id = "+ serid+" AND owner_id = " + str(aidi)  +" ;")
                                


                db.commit()


                return "success"



@app.route("/save_new_service_3_ajax",methods=["GET","POST"])
def save_new_service_3_ajax():
    if request.cookies.get("c_user") != None and request.cookies.get("xs") != None:
        c_user = request.cookies.get("c_user")
        xs = request.cookies.get("xs")
        if auth(c_user,xs) == True:
                # db = mysql.connector.connect(
                # host=host,
                # user=user,
                # passwd = passwd,
                # database= database
                # )
                kurs = db.cursor()
                
                kurs.execute("SELECT id FROM users WHERE username = '"+ str(c_user)   +"';")
                
                kursf = kurs.fetchone()
                aidi = kursf[0]


                points_ls = json.loads(request.form["points_ls"])

                serid = str(request.form["service_id"])

                try:
                    max_clients = int(request.form["max_clients"])
                except:
                    max_clients = 0



                fas = str(request.form["fasi"])

                dr = str(request.form["dro"])


                try:
                    hfasi = float(request.form["hfasi"])
                except:
                    # hfasi = 0
                    return "error"

                try:
                    hdro = int(request.form["hdro"])
                except:
                    # hdro = 0
                    return "error"



                try:
                    fasi = float(fas)
                except:
                    fasi = hfasi
                try:
                    dro = int(dr)
                except:
                    dro = hdro






                kurs.execute("SELECT owner_id FROM servisebi WHERE id = "+ str(serid)  +";")

                owner_id = kurs.fetchone()[0]
                
                

                fas = str(fasi)

                dr = str(dro)

                kurs.execute("UPDATE servisebi SET max_clients = "+ str(max_clients) +" WHERE id = "+ str(serid) +" AND owner_id = "+ str(aidi) +";")

                kurs.execute("UPDATE servisebi SET maxfasi = "+ fas +" WHERE id = "+ str(serid) +" AND owner_id = "+ str(aidi) +";")

                kurs.execute("UPDATE servisebi SET maxdro = "+ dr +" WHERE id = "+ str(serid) +" AND owner_id = "+ str(aidi) +";")

                kurs.execute("DELETE FROM points WHERE service_id = "+ str(serid) +" AND owner_id = "+ str(aidi) +";")

                point_c = 0

                if request.form["tipi"] == "create":
                    for i in points_ls:
                        if int(owner_id) == int(aidi):
                            if point_c<=100:
                                point_c+=int(i["points"])
                                kursi = "INSERT INTO points(point,fasi,dro,service_id,owner_id,saxeli) VALUES("+ i["points"] +","+ i["fasi"] +","+ i["dro"] +","+ str(serid) +","+ str(aidi) +",'" + i["name"] +"');"
                                print(kursi)
                                kurs.execute(kursi)


                kurs.execute("UPDATE servisebi SET points = "+ str(point_c) +" WHERE id = "+ str(serid) +" AND owner_id = "+ str(aidi) +";") 


                kurs.execute("UPDATE servisebi SET fasi = "+ str(hfasi) +" WHERE id = "+ str(serid) +" AND owner_id = "+ str(aidi) +";")

                kurs.execute("UPDATE servisebi SET dro = "+ str(hdro) +" WHERE id = "+ str(serid) +" AND owner_id = "+ str(aidi) +";")


                db.commit()

                
                return "success"




@app.route("/<uzer>")
def useri(uzer):
        if request.cookies.get("c_user") == None or request.cookies.get("xs") == None:
            return redirect("/login?redirect=" + uzer) #/signup
        else:
            c_user = request.cookies.get("c_user")
            xs = request.cookies.get("xs")

            if auth(c_user,xs) == True:
                host = "127.0.0.1"
                user = "root"
                passwd = ""
                database = "geolance"

                # db = mysql.connector.connect(
                # host=host,
                # user=user,
                # passwd = passwd,
                # database= database
                # )

                kurs = db.cursor(buffered=True)
                kurxo = db.cursor(buffered=True)
                kurs.execute("SELECT saxeli,imgsrc,username,angarishi,imgsize,id,join_time FROM users WHERE username = '" + c_user +"';")

                kursf = kurs.fetchone()
                aidi = kursf[5]
                straidi = str(aidi)
                #if kursf != None:
                saxeli = kursf[0]
                imgsrc = kursf[1]
                imgsize = kursf[4]
                join_time = kursf[6]

                username = kursf[2]

                angarishi = kursf[3]
                
                anga = str(angarishi)
                pf_lnk = "http://"+request.headers.get('host')+"/" + username

                chemi_id = kursf[5]
                aidi = chemi_id

                print("SELECT id,saxeli,gvari,imgsrc,imgsize, ricxvi ,tve ,weli,sfero,role,status username FROM users WHERE username = '" + uzer +"';")
                kurs.execute("SELECT id,saxeli,gvari,imgsrc,imgsize, ricxvi ,tve ,weli,sfero,role,status,username FROM users WHERE username = '" + uzer +"';")
                kursu = kurs.fetchone()
                if kursu != None:
                    role = kursu[9]
                    #if role == "lancer":
                
                    u_aidi = kursu[0]
                    if u_aidi == aidi:
                        activity_status_color = "green"
                    else:
                        activity_status = kursu[10]
                        if activity_status == "1":
                            activity_status_color = "green"
                        elif activity_status == "0":
                            activity_status_color = "grey"


                    kurs.execute("SELECT subsfero FROM lancer_sferos  WHERE aidi = "+ str(u_aidi) +"; ")
                    u_subsfereobi_l = [i[0] for i in kurs]


                    u_subsfereobi = " , ".join(u_subsfereobi_l)
                    if len(u_subsfereobi_l) > 1:

                        u_subsfero_name = "სუბ-სფეროები : "
                    else:
                        u_subsfero_name = "სუბ-სფერო : "

                    kurs.execute("SELECT about_me,ganatleba FROM lancer_params WHERE aidi = "+ str(u_aidi) +";")
                    kurs_info = kurs.fetchone()

                    if kurs_info != None:
                        if kurs_info[0] != None and kurs_info[0] != None:
                            u_chemshesaxeb = kurs_info[0]
                        else:
                            u_chemshesaxeb =  "არ არის მითითებული"
                        if kurs_info[1] != None and kurs_info[1] != None:
                            u_ganatleba = kurs_info[1]
                        else:
                            u_ganatleba =  "არ არის მითითებული"
                    else:
                        u_chemshesaxeb =  "არ არის მითითებული"
                        u_ganatleba =  "არ არის მითითებული" #u_username
                    

                    u_saxeli = kursu[1]
                    u_gvari = kursu[2]
                    u_imgsrc = kursu[3]
                    u_imgsize = kursu[4]

                    u_tve = kursu[6]
                    u_ricxvi = kursu[5]
                    u_dabweli = kursu[7]

                    u_sfero = kursu[8]
                    u_username = kursu[11]

                    ricdic = {1 : 31,2 : 28,3 : 31, 4 :30, 5 : 31, 6 :30, 7 : 31,8 : 31, 9: 30,10 :31, 11 : 30, 12 : 31}
                    axricdic = {1 : 31,2 : 28,3 : 31, 4 :30, 5 : 31, 6 :30, 7 : 31,8 : 31, 9: 30,10 :31, 11 : 30, 12 : 31}

                    dasaki  = float(u_dabweli) + (float(u_tve)/12) + (int(u_ricxvi)/(ricdic[int(u_tve)+1]*12))

                    ylevind = str(datetime.datetime.now())

                    axweli = int(ylevind.split("-")[0])
                    axtve = int(ylevind.split("-")[1]) - 1
                    axricxvi = int(ylevind.split("-")[2].split()[0])


                    axaki = axweli + (float(axtve)/12) +  (int(axricxvi)/(axricdic[int(axtve)+1]*12))


                    asaki = axaki - dasaki

                    u_asaki = str(asaki).split(".")[0]

                    if uzer != c_user:
                        # stalker_id	stalked_id	stalk_time	
                        kurs.execute("INSERT INTO stalks(stalker_id,stalked_id,stalk_time) VALUES("+ str(aidi) +","+ str(u_aidi) +","+ str(time.time()) +");")
                        db.commit()
                        
                    if uzer == c_user:
                        main_info_editbtn = Markup("""<img id = "edit_symbol_main_info" class = "edit_symbol" src = "static/edit_symbol.jpg"> """)
                        wide_agwera_editbtn = Markup("""<img id = "edit_symbol_wide_agwera" class = "edit_symbol" src = "static/edit_symbol.jpg">""")
                    else:
                        main_info_editbtn = Markup("""<img id = "message_user_btn" class = 'edit_symbol """+ str(u_aidi) +""" """+ str(u_saxeli) +"""' src = "static/message_user_icon.png"> """)
                        wide_agwera_editbtn = """"""
                    
                    #servisebi
                    if uzer == c_user:
                        
                        kurs.execute("SELECT id,satauri,profile,fasi,maxfasi,status FROM servisebi WHERE owner_id = "+ str(u_aidi) +" ORDER BY id DESC;")
                    else:
                        kurs.execute("SELECT id,satauri,profile,fasi,maxfasi,status FROM servisebi WHERE owner_id = "+ str(u_aidi) +" AND status = 'active' ORDER BY id DESC;")
                    service = "" #Markup('<div class = "service_row">')

                    service_row = ""
                    serx = 0


                    if uzer == c_user:
                        mainscript = Markup("""
                                        /*
                                            linke_accs.onclick = function(){
                                                linke_accs.style.marginTop = "3%";
                                                linke_accs.style.opacity = "0.7";

                                                ganatleba.style.marginTop = "5%";
                                                ganatleba.style.opacity = "1";

                                                about_me.style.marginTop = "5%";
                                                about_me.style.opacity = "1";
                                            }
                                            */





                                            // editingiii
                                            var main_info_div = document.getElementById("main_info");
                                            
                                            
                                            var main_info_editbtn = document.getElementById("edit_symbol_main_info");
                                            var wide_agwera_editbtn = document.getElementById("edit_symbol_wide_agwera");
                                            
                                            var main_info_savebtn = document.createElement("button");
                                            var wide_agwera_savebtn = document.createElement("button");

                                            
                                            var saxeli_gvari_h = document.getElementById("saxeli_gvari");
                                            var asaki = document.getElementById("asaki");
                                            var sfero_h = document.getElementById("sfero_h");
                                            var subsfero_h = document.getElementById("subsfero_h");
                                            var shefaseba = document.getElementById("shefaseba");

                                                //axali elements
                                                var saxeli_input = document.createElement("input");
                                                var bra = document.createElement("br");
                                                var gvari_input = document.createElement("input");


                                                saxeli_input.placeholder = "სახელი";
                                                gvari_input.placeholder = "გვარი";
                                                saxeli_input.className = "ident_input saxeli_input";
                                                gvari_input.className = "ident_input gvari_input";

                                                saxeli_input.id = "saxeli_input";
                                                gvari_input.id = "gvari_input";

                                                    //sferos
                                                    // var sfero_select =  document.getElementById("sfero_select"); //document.createElement("select")
                                                    // main_info_div.removeChild(sfero_select)
                                                        //sfero options





                                                        




                                            main_info_savebtn.id = "shenaxva_main_info_button";
                                            main_info_savebtn.innerHTML = "შენახვა";
                                            main_info_savebtn.className = "editsave_bnt";


                                            wide_agwera_savebtn.id = "shenaxva_wide_agwera_button";
                                            wide_agwera_savebtn.innerHTML = "შენახვა";
                                            wide_agwera_savebtn.className = "editsave_bnt";
                                                        main_info_editbtn.onclick = function(){
                                                        //editingis dawyeba
                                                        
                                                        main_info_div.removeChild(main_info_editbtn);
                                                        main_info_div.append(main_info_savebtn);

                                                        
                                                        //main_info_div.removeChild(u_pfp);
                                                        main_info_div.removeChild(saxeli_gvari_h);
                                                        main_info_div.removeChild(asaki);
                                                        main_info_div.removeChild(sfero_h);
                                                        
                                                        main_info_div.removeChild(subsfero_h);
                                                        main_info_div.removeChild(shefaseba);


                                                        main_info_div.append(saxeli_input);
                                                        main_info_div.append(bra);
                                                        main_info_div.append(gvari_input);
                                                        sfero.place(32,40);
                                                        sfero.setValue("{{u_sfero}}");

                                                        //main_info_div.append(sfero_select);

                                                        saxeli_input.value = saxeli_gvari_h.innerHTML.split(" ")[0];
                                                        gvari_input.value = saxeli_gvari_h.innerHTML.split(" ")[1];
                                                        //
                                                            //sfero_select.append(sfero_option);

                                                        

                                                    }
                                                    main_info_savebtn.onclick = main_info_update;
                                                    
                                                    /*
                                                    main_info_savebtn.onclick = function(){
                                                        //editis dasaveba
                                                        main_info_div.append(main_info_editbtn);
                                                        main_info_div.removeChild(main_info_savebtn);

                                                        main_info_div.removeChild(saxeli_input);
                                                        main_info_div.removeChild(bra);
                                                        main_info_div.removeChild(gvari_input);

                                                        main_info_div.removeChild(sfero_select);

                                                        main_info_div.append(saxeli_gvari_h);
                                                        main_info_div.append(asaki);
                                                        main_info_div.append(sfero_h);
                                                        main_info_div.append(subsfero_h);
                                                        main_info_div.append(shefaseba);
                                                        u_pfp.onclick = function(){
                                                            window.location.href = "/{{u_imgsrc}}";
                                                        }
                                                    }
                                                    */
                                                    
                                                    //var wide_agwera_editbtn = document.getElementById("edit_symbol_wide_agwera");

                                                    var selected_output = document.getElementById("selected_output");

                                                    
                                                    var selected_output_p = document.getElementById("selected_output_p");



                                                    about_me_input.placeholder = "ჩემს შესახებ";
                                                    ganatleba_input.placeholder = "განათლება";



                                                    about_me_input.className = "agwera_input";
                                                    ganatleba_input.className = "agwera_input";

                                                    wide_agwera.editing = false;
                                                    wide_agwera_editbtn.onclick = function(){
                                                        wide_agwera.style.height = "30%";
                                                        wide_agwera.editing = true;
                                                        selected_output.removeChild(selected_output_p);
                                                        wide_agwera.removeChild(wide_agwera_editbtn);

                                                        if(wide_agwera.status == "aboutme"){
                                                            selected_output.append(about_me_input);
                                                        }
                                                        else if(wide_agwera.status == "ganatleba"){
                                                            selected_output.append(ganatleba_input);
                                                        }
                                                        /*
                                                        else if(wide_agwera.status == "none"){

                                                        }
                                                        */
                                                    wide_agwera.append(wide_agwera_savebtn);
                                                        
                                                        

                                                    }
                                                    wide_agwera_savebtn.onclick = wide_agwera_update;



                                                    var create_new = document.getElementById("add_service");
                                                    create_new.onclick = function(){
                                                        window.location.href = "/create_new_service?num=1&service=new";
                                                    }
                                                    """)
                    else:
                        mainscript = """ """


                    for i in kurs:
                        service_aidi = i[0]
                        #service+= Markup('<div class = "servisi">' + i[1] + '</div>')
                        # iebi = [a for a in i]

                        if i[4] == None:
                            maxfasi = ""
                        else:
                            if i[3] < i[4]:
                                maxfasi = " - $"  + str(i[4])
                            else:
                                maxfasi = ""
                        

                        iebi = i[5]
                        # iebi = []
                        # iebi.append(i[0])
                        # iebi.append(i[1])
                        # iebi.append(i[2])
                        # iebi.append(i[3])
                        

                        # if (None in iebi) == False:
                        if iebi == "active":


                            kurxo.execute("SELECT main_rating FROM servisebis_reitingi WHERE service_id = "+ str(i[0]) +";")
                            rating_ls = [float(a[0]) for a in kurxo]
                            if len(rating_ls) != 0:
                                rating_cifr = str(np.mean(rating_ls))

                                rating = "⭐"+ rating_cifr.split(".")[0] + "." + rating_cifr.split(".")[1][0] #x
                            else:
                                rating = ""

                            if uzer == c_user:
                                    serviewlink = '"http://'+request.headers.get('host')+'/create_new_service?num=1&service='+ str(service_aidi) +'"' #chekkkkkk pointn                        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffzzzzzzzzzzzzzzzzzzzzzzz
                            else:
                                    serviewlink = '"http://'+request.headers.get('host')+'/service/'+ str(service_aidi) +'"'
                            zervacia_id ='"service_'+ str(service_aidi) + '"'
                            serx+=1
                            service_row+= Markup('<div id = '+zervacia_id+' class = "servisi" style="width:30%;"><img  id = "service_'+ str(service_aidi) +'_img"  class = "service_img" src = "static/services/')+ i[2] +Markup('"><p id = "service_'+ str(service_aidi) +'_tit" class = "service_tit" >') + i[1] + Markup('</p><div  class = "serv_data"><span class = "rating">'+rating + '</span>              <span class = "fasi" ><span id = "dollar">$</span>'+ str(i[3]) + maxfasi +'</span></div></div>')
                            if serx % 3 == 0:
                                #service+=Markup('</div>') + "\n" + Markup('<div class = "service_row">')
                                service+=Markup('<div style= "width:100%;" class = "service_row">') + service_row + Markup("</div><br>") + "\n"
                                service_row = ""


                        elif iebi == "paused":
                            if u_aidi == chemi_id:
                                kurxo.execute("SELECT main_rating FROM servisebis_reitingi WHERE service_id = "+ str(i[0]) +";")
                                if i[0] != None:
                                    rating_ls = [float(a[0]) for a in kurxo]
                                    if len(rating_ls) != 0:
                                        rating_cifr = str(np.mean(rating_ls))

                                        rating = "⭐"+ rating_cifr.split(".")[0] + "." + rating_cifr.split(".")[1][0] #o
                                    else:
                                        rating = ""
                                else:
                                    rating = ""

                                if i[2] != None:
                                    profili_src =  i[2]
                                else:
                                    profili_src = "logos_white.png"
                                
                                if i[3] != None:
                                    service_fasi = Markup('<span id = "dollar">$</span>') + str(i[3])
                                else:
                                    service_fasi = ""
                                
                                

                                serx+=1
                                zervacia_id ='"service_'+ str(service_aidi) + '"'
                                if uzer == c_user:
                                    serviewlink = Markup('"http://'+request.headers.get('host')+'/create_new_service?num=1&service='+ str(service_aidi) +'"') #chekkkkkk pointn                        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffzzzzzzzzzzzzzzzzzzzzzzz
                                else:
                                    serviewlink = Markup('"http://'+request.headers.get('host')+'/service/'+ str(service_aidi) +'"')
                                
                                service_row+= Markup('<div id = '+zervacia_id  +' class = "servisi paused_servisi" style="background-color:rgb(8, 130, 112,0.3);width:30%;"><img id = "service_'+ str(service_aidi) +'_img" class = "service_img" src = "static/services/')+ profili_src +Markup('"><p  id = "service_'+ str(service_aidi) +'_tit" class = "service_tit" style="opacity:0.3"  >') + i[1] + Markup('</p><div  class = "serv_data"><span class = "rating">') + rating + Markup('</span>            <span class = "fasi"  >')+ service_fasi  + maxfasi+ Markup('</span></div><h2 style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);color:yellow;font-size:25px;opacity:0.7;" class = "restricred_lb">დაპაუზებული<h2></div>')
                                if serx % 3 == 0:
                                    #service+=Markup('</div>') + "\n" + Markup('<div class = "service_row">')
                                    service+=Markup('<div style= "width:100%;" class = "service_row">') + service_row + Markup("</div><br>") + "\n"
                                    service_row = ""


                        else: #drafti mafti
                            if u_aidi == chemi_id:
                                kurxo.execute("SELECT main_rating FROM servisebis_reitingi WHERE service_id = "+ str(i[0]) +";")
                                if i[0] != None:
                                    rating_ls = [float(a[0]) for a in kurxo]
                                    if len(rating_ls) != 0:
                                        rating_cifr = str(np.mean(rating_ls))

                                        rating = "⭐"+ rating_cifr.split(".")[0] + "." + rating_cifr.split(".")[1][0] #o
                                    else:
                                        rating = ""
                                else:
                                    rating = ""

                                if i[2] != None:
                                    profili_src =  i[2]
                                else:
                                    profili_src = "logos_white.png"
                                
                                if i[3] != None:
                                    service_fasi = Markup('<span id = "dollar">$</span>') + str(i[3])
                                else:
                                    service_fasi = ""
                                
                                

                                serx+=1
                                zervacia_id ='"service_'+ str(service_aidi) + '"'
                                if uzer == c_user:
                                    serviewlink = Markup('"http://'+request.headers.get('host')+'/create_new_service?num=1&service='+ str(service_aidi) +'"') #chekkkkkk pointn                        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffzzzzzzzzzzzzzzzzzzzzzzz
                                else:
                                    serviewlink = Markup('"http://'+request.headers.get('host')+'/service/'+ str(service_aidi) +'"')
                                
                                service_row+= Markup('<div id = '+zervacia_id  +' class = "servisi draft_servisi" style="background-color:rgb(8, 130, 112,0.3);width:30%;"><img id = "service_'+ str(service_aidi) +'_img" class = "service_img" src = "static/services/')+ profili_src +Markup('"><p  id = "service_'+ str(service_aidi) +'_tit" class = "service_tit"  style="opacity:0.3" >') + i[1] + Markup('</p><div  class = "serv_data"><span class = "rating">') + rating + Markup('</span>            <span class = "fasi"  >')+ service_fasi  + maxfasi+ Markup('</span></div><h2 style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);color:yellow;font-size:30px;opacity:0.7;" class = "restricred_lb">დრაფტი<h2></div>')
                                if serx % 3 == 0:
                                    #service+=Markup('</div>') + "\n" + Markup('<div class = "service_row">')
                                    service+=Markup('<div style= "width:100%;" class = "service_row">') + service_row + Markup("</div><br>") + "\n"
                                    service_row = ""


                        
                        

                        
                    
                    
                    
                    
                    mevar_es = uzer == c_user

                    if mevar_es:
                        serx+=1

                    if serx% 3 != 0:
                        bolozoma = 33 * ((serx % 3) )
                        bolozomaw = 30 / (bolozoma/100)

                        
                        
                        if mevar_es:
                            damatebis_serviceblock = Markup('<div id = "add_service" style="font-size:30px;text-align:center;width:'+ str(bolozomaw) +'%;" class = "servisi"> <img  id = "add_img"src = "static/add.png"><p id = "create_new_service_p">ახალის შექმნა</p></div>')
                        else:
                            damatebis_serviceblock = ""
                        service += Markup('<div style= "width:'+ str(bolozoma) +'%;" class = "service_row">')  + service_row.replace('width:30%;','width:'+ str(bolozomaw) +'%;') +damatebis_serviceblock + Markup('</div>') + '\n'
                    else:
                        
                        if mevar_es:
                            damatebis_serviceblock = Markup('<div id = "add_service" style="font-size:30px;text-align:center;width:33%;" class = "servisi"><img  id = "add_img"src = "static/add.png"> <p id = "create_new_service_p">ახალის შექმნა</p> </div>')
                        else:
                            damatebis_serviceblock= ""
                        
                        service+= Markup('<div style= "width:100%;" class = "service_row">') + service_row + damatebis_serviceblock + Markup('</div>')
                    

                        #service+=Markup("</div>")



                        #damatebis
                    kurs.execute("SELECT main_rating FROM servisebis_reitingi WHERE owner_id = "+ str(u_aidi) +";")

                    owneritingls = [i[0] for i in kurs]
                    if len(owneritingls) > 0:

                        owner_ratings = str(np.mean(owneritingls))
                        owner_ratingsp =  owner_ratings.split(".")
                        owner_rating = "შეფასება : ⭐" + owner_ratingsp[0] + "." + owner_ratingsp[1][0]
                        main_info_div_simagle = "70"
                        margacia = "10"
                    else:

                        margacia = "15"
                        owner_rating = ""
                        main_info_div_simagle = "70"

                    if uzer == c_user:
                        chemia_profili = "true"
                    else:
                        chemia_profili = "false"
                    # notifications_box
                    kurs.execute("SELECT user_one_seen FROM dms WHERE user_one = "+ str(aidi) +";")
                    kurs_one = kurs.fetchall()
                    kurs.execute("SELECT user_two_seen FROM dms WHERE user_two = "+ str(aidi) +";")
                    kurs_two = kurs.fetchall()

                    kurs_united = kurs_one + kurs_two
                    message_notification_value = 0
                    for i in kurs_united:
                        message_notification_value+= i[0]
                    if message_notification_value > 9:
                        message_notification_value_shortened = "9+"
                    else:
                        message_notification_value_shortened = str(message_notification_value)
                    message_notification_value = str(message_notification_value)


                    # mailbox
                    kurs.execute("SELECT * FROM notifications WHERE notification_recipient_id = "+ str(aidi) +" OR (notification_recipient_id = 0 AND notification_time > "+ str(join_time) +") ORDER BY id DESC;")
                    nots = np.array(kurs.fetchall())
                    not_count = 0

                    for i in nots:
                        if int(i[8]) == 0:
                            not_count+=1

                    if not_count > 9:
                        not_count_markup = "9+"
                    else:
                        not_count_markup = str(not_count)
                    # u_username
                    csrftk = csrftok(int(aidi))
                    return render_template("profile.html",activity_status_color=activity_status_color,straidi=straidi,chemia_profili=chemia_profili,mainscript=mainscript,u_username=u_username,saxeli=saxeli,imgsize=imgsize,imgsrc=imgsrc,my_profile_link=pf_lnk,fuli=anga   ,u_imgsrc=u_imgsrc,u_saxeli=u_saxeli,u_gvari=u_gvari,u_imgsize=u_imgsize,u_asaki=u_asaki,u_sfero=u_sfero,u_chemshesaxeb=u_chemshesaxeb, u_ganatleba=u_ganatleba,main_info_editbtn=main_info_editbtn,wide_agwera_editbtn=wide_agwera_editbtn,service=service,shefaseba=owner_rating,main_info_div_simagle=main_info_div_simagle ,margacia=margacia,
            message_notification_value=message_notification_value, message_notification_value_shortened=message_notification_value_shortened,
            not_count=str(not_count),not_count_markup=not_count_markup,csrftk=csrftk)
                else:
                    return "eror user not found"


@app.route("/pause_service",methods=["GET","POST"])
def pause_service():
    dada = request.cookies
    if dada.get("c_user") != None and dada.get("xs") != None:
        c_user = dada.get("c_user")
        xs = dada.get("xs")
        
        if auth(c_user,xs) == True:
            
            # db = mysql.connector.connect(
            #     host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )
            kurs = db.cursor()
            kurs.execute("SELECT id FROM users WHERE username = '"+ c_user +"';")
            print(request.form)
            
            aidi = kurs.fetchone()[0] 
            print(request.cookies)
            serid = request.form["serid"]
            print(session)
            action = request.form["action"]


            # if str(request.form["csrftk"]) == str(csrftoks[int(aidi)]):
            # if str(session["csrftk"]) == "jCyHdHP22xP6Pe2Pc5IWlcl6En5CumftYp0TbidGWAw1EhZ2cM0B61E2Ph6TZDJa9RmvYqj8KrO5JymvfGR3UbojQBLJC6nNgUCare21EfCXpZgoCEQ3j00G55JYLDzSsgFYBp0oYu8N1O0mp5NCJe":
            
            if True:
            # if True
                if action == "pause":   
                    
                    kurs.execute("UPDATE servisebi SET status = 'paused' WHERE id = "+ str(serid) +" AND owner_id = "+ str(aidi) +" AND status = 'active' ;")
                elif action == "resume":
                    kurs.execute("UPDATE servisebi SET status = 'active' WHERE id = "+ str(serid) +" AND owner_id = "+ str(aidi) +" AND  status = 'paused';")
                

                db.commit()

                kurs.execute("SELECT id,satauri,profile,fasi,maxfasi,status FROM servisebi WHERE owner_id = "+ str(aidi) +" ORDER BY id DESC;")
                
                service = "" #Markup('<div class = "service_row">')

                service_row = ""
                serx = 0

                kurz = kurs.fetchall()
                
                for i in kurz:
                    service_aidi = i[0]
                    #service+= Markup('<div class = "servisi">' + i[1] + '</div>')
                    # iebi = [a for a in i]

                    if i[4] == None:
                        maxfasi = ""
                    else:
                        if i[3] < i[4]:
                            maxfasi = " - $"  + str(i[4])
                        else:
                            maxfasi = ""

                    iebi = i[5]
                    # iebi = []
                    # iebi.append(i[0])
                    # iebi.append(i[1])
                    # iebi.append(i[2])
                    # iebi.append(i[3])
                    

                    # if (None in iebi) == False:
                    if iebi == "active":


                        kurs.execute("SELECT main_rating FROM servisebis_reitingi WHERE service_id = "+ str(i[0]) +";")
                        rating_ls = [float(a[0]) for a in kurs]
                        if len(rating_ls) != 0:
                            rating_cifr = str(np.mean(rating_ls))

                            rating = "⭐"+ rating_cifr.split(".")[0] + "." + rating_cifr.split(".")[1][0] #x
                        else:
                            rating = ""


                        zervacia_id ='"service_'+ str(service_aidi) + '"'
                        serx+=1
                        service_row+= Markup('<div id = '+zervacia_id+' class = "servisi" style="width:30%;"><img  id = "service_'+ str(service_aidi) +'_img"  class = "service_img" src = "static/services/')+ i[2] +Markup('"><p id = "service_'+ str(service_aidi) +'_tit" class = "service_tit" >') + i[1] + Markup('</p><div  class = "serv_data"><span class = "rating">'+rating + '</span>              <span class = "fasi" ><span id = "dollar">$</span>'+ str(i[3]) + maxfasi +'</span></div></div>')
                        if serx % 3 == 0:
                            #service+=Markup('</div>') + "\n" + Markup('<div class = "service_row">')
                            service+=Markup('<div style= "width:100%;" class = "service_row">') + service_row + Markup("</div><br>") + "\n"
                            service_row = ""


                    elif iebi == "paused":
                        if  True: #u_aidi == chemi_id:
                            kurs.execute("SELECT main_rating FROM servisebis_reitingi WHERE service_id = "+ str(i[0]) +";")
                            if i[0] != None:
                                rating_ls = [float(a[0]) for a in kurs]
                                if len(rating_ls) != 0:
                                    rating_cifr = str(np.mean(rating_ls))

                                    rating = "⭐"+ rating_cifr.split(".")[0] + "." + rating_cifr.split(".")[1][0] #o
                                else:
                                    rating = ""
                            else:
                                rating = ""

                            if i[2] != None:
                                profili_src =  i[2]
                            else:
                                profili_src = "logos_white.png"
                            
                            if i[3] != None:
                                service_fasi = Markup('<span id = "dollar">$</span>') + str(i[3])
                            else:
                                service_fasi = ""
                            
                            

                            serx+=1
                            zervacia_id ='"service_'+ str(service_aidi) + '"'

                            
                            service_row+= Markup('<div id = '+zervacia_id  +' class = "servisi paused_servisi" style="background-color:rgb(8, 130, 112,0.3);width:30%;"><img id = "service_'+ str(service_aidi) +'_img" class = "service_img" src = "static/services/')+ profili_src +Markup('"><p  id = "service_'+ str(service_aidi) +'_tit" class = "service_tit" style="opacity:0.3"  >') + i[1] + Markup('</p><div  class = "serv_data"><span class = "rating">') + rating + Markup('</span>            <span class = "fasi"  >')+ service_fasi  + maxfasi+ Markup('</span></div><h2 style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);color:yellow;font-size:25px;opacity:0.7;" class = "restricred_lb">დაპაუზებული<h2></div>')
                            if serx % 3 == 0:
                                #service+=Markup('</div>') + "\n" + Markup('<div class = "service_row">')
                                service+=Markup('<div style= "width:100%;" class = "service_row">') + service_row + Markup("</div><br>") + "\n"
                                service_row = ""


                    else: #drafti mafti
                        if True: #u_aidi == chemi_id:
                            kurs.execute("SELECT main_rating FROM servisebis_reitingi WHERE service_id = "+ str(i[0]) +";")
                            if i[0] != None:
                                rating_ls = [float(a[0]) for a in kurs]
                                if len(rating_ls) != 0:
                                    rating_cifr = str(np.mean(rating_ls))

                                    rating = "⭐"+ rating_cifr.split(".")[0] + "." + rating_cifr.split(".")[1][0] #o
                                else:
                                    rating = ""
                            else:
                                rating = ""

                            if i[2] != None:
                                profili_src = i[2]
                            else:
                                profili_src = "logos_white.png"
                            
                            if i[3] != None:
                                service_fasi = Markup('<span id = "dollar">$</span>') + str(i[3])
                            else:
                                service_fasi = ""
                            
                            

                            serx+=1
                            zervacia_id ='"service_'+ str(service_aidi) + '"'
                            # if uzer == c_user:
                            #     serviewlink = Markup('"http://localhost:5000/create_new_service?num=1&service='+ str(service_aidi) +'"') #chekkkkkk pointn                        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffzzzzzzzzzzzzzzzzzzzzzzz
                            # else:
                            #     serviewlink = Markup('"http://localhost:5000/service/'+ str(service_aidi) +'"')
                            
                            service_row+= Markup('<div id = '+zervacia_id  +' class = "servisi draft_servisi" style="background-color:rgb(8, 130, 112,0.3);width:30%;"><img id = "service_'+ str(service_aidi) +'_img" class = "service_img" src = "static/services/')+ profili_src +Markup('"><p  id = "service_'+ str(service_aidi) +'_tit" class = "service_tit" style="opacity:0.3" >') + i[1] + Markup('</p><div  class = "serv_data"><span class = "rating">') + rating + Markup('</span>             <span class = "fasi"  >')+ service_fasi  + maxfasi+ Markup('</span></div><h2 style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);color:yellow;font-size:30px;opacity:0.7;" class = "restricred_lb">დრაფტი<h2></div>')
                            if serx % 3 == 0:
                                #service+=Markup('</div>') + "\n" + Markup('<div class = "service_row">')
                                service+=Markup('<div style= "width:100%;" class = "service_row">') + service_row + Markup("</div><br>") + "\n"
                                service_row = ""


                    
                    

                    
                
                
                serx+=1
                
                # mevar_es = uzer == c_user

                if serx% 3 != 0:
                    bolozoma = 33 * ((serx % 3) )
                    bolozomaw = 30 / (bolozoma/100)

                    
                    
                    if True: #mevar_es:
                        damatebis_serviceblock = Markup('<div id = "add_service" style="font-size:30px;text-align:center;width:'+ str(bolozomaw) +'%;" class = "servisi"> <img  id = "add_img"src = "static/add.png"><p id = "create_new_service_p">ახალის შექმნა</p></div>')
                    else:
                        damatebis_serviceblock = ""
                    service += Markup('<div style= "width:'+ str(bolozoma) +'%;" class = "service_row">')  + service_row.replace('width:30%;','width:'+ str(bolozomaw) +'%;') +damatebis_serviceblock + Markup('</div>') + '\n'
                else:
                    
                    if True: #mevar_es:
                        damatebis_serviceblock = Markup('<div id = "add_service" style="font-size:30px;text-align:center;width:33%;" class = "servisi"><img  id = "add_img"src = "static/add.png"> <p id = "create_new_service_p">ახალის შექმნა</p> </div>')
                    else:
                        damatebis_serviceblock= ""
                    
                    service+= Markup('<div style= "width:100%;" class = "service_row">') + service_row + damatebis_serviceblock + Markup('</div>')
                

                
                
                
                db.commit()

                return service



# @app.route("/start_chat",methods=["GET","POST"])
# def start_chat():
#     if request.cookies.get("c_user") != None and request.cookies.get("xs") != None:
#         c_user = request.cookies.get("c_user")
#         xs = request.cookies.get("xs")
#         if auth(c_user,xs):
#             db = mysql.connector.connect(
#                 host=host,
#                 user=user,
#                 passwd = passwd,
#                 database= database
#             )
#             kurs = db.cursor()
#             kurs.execute("SELECT id,saxeli,imgsrc FROM users WHERE username = '"+ c_user +"';")

#             sruli = kurs.fetchone()
#             aidi = sruli[0]
#             saxeli = sruli[1]
#             pfp = sruli[2]


            

#             u_aidi = request.form["aidi"]
#             u_saxeli = request.form["name"]

#             kurs.execute("SELECT id FROM dms WHERE  (user_one = '"+ str(aidi) +"' AND user_two = '"+ str(u_aidi) +"') OR (user_one = '"+ str(u_aidi) +"' AND user_two = '"+ str(aidi) +"'); ")

#             dmf =kurs.fetchone()

#             if dmf == None:


#                 kurs.execute("SELECT imgsrc FROM users WHERE id = "+str(u_aidi)+" ;")

#                 u_sruli = kurs.fetchone()
#                 u_pfp = u_sruli[0]


#                 #	last_message_content	last_message_sender_id	last_message_sender_name	user_one	user_two	
#                 kurs.execute("INSERT INTO dms(user_one,user_two,last_message_time) VALUES("+ str(aidi) +","+ str(u_aidi) +","+ str(int(time.time())) +");")
#                 db.commit()
#                 kurs.execute("SELECT id FROM dms ORDER BY id DESC;")
#                 chat_aidi = kurs.fetchone()[0]
#             else:
#                 chat_aidi = dmf[0]



           


#             return str(chat_aidi)


#window.history.pushState("object or string", "Title", "/new-url");
#window.history.pushState("", "", "/new-url");
@app.route("/messenger")
def messenger():
    if request.cookies.get("c_user") != None and request.cookies.get("xs") != None:
        c_user = request.cookies.get("c_user")
        xs = request.cookies.get("xs")
        if auth(c_user,xs) == True:
            # db = mysql.connector.connect(
            #     host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )
            # kurs = db.cursor()
            return redirect("/messenger/main")

@app.route("/messenger/<chat>")
def messenger_chat(chat):
    if request.cookies.get("c_user") != None and request.cookies.get("xs") != None:
        c_user = request.cookies.get("c_user")
        xs = request.cookies.get("xs")
        if auth(c_user,xs) == True:
            # db = mysql.connector.connect(
            #     host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )
            kurs = db.cursor()

            kurs.execute("SELECT * FROM users WHERE username = '"+ c_user +"';")

            kursu = kurs.fetchone()

            aidi = kursu[0]
            straidi = str(aidi)
            saxeli = kursu[1]

            my_profile_link = "/"+ kursu[3]

            imgsrc = "/"+kursu[10]
            fuli = kursu[11]

            imgsize = kursu[12]
            join_time = kursu[20]

            # SELECT users.saxeli,users.gvari,users.imgsrc FROM stalks INNER JOIN users ON users.id= stalks.stalked_id WHERE stalks.stalker_id = 16 GROUP BY users.id ORDER BY stalks.id DESC;
            #SELECT dms.id,dms.last_message_content,dms.last_message_sender_id,dms.user_one,dms.user_two,dms.last_message_time,dms.status FROM dms ;
            
            
            # kurs.execute("SELECT * FROM dms WHERE (user_one = "+ str(aidi) +" OR (status = 'active'  AND user_two = "+ str(aidi) +") )  ORDER BY last_message_time DESC ;")
            #kurs.execute("")
            # id last_message_content last_message_sender_id user_one user_two last_message_time status
            # dms.status = 'active'
            # kurs.execute("SELECT dms.id,dms.last_message_content, dms.last_message_sender_id, users.saxeli, users.gvari, users.imgsrc, dms.last_message_time, users.imgsize, users.status,dms.user_two, users.username FROM dms INNER JOIN users ON dms.user_two = users.id WHERE dms.user_one = "+ str(aidi) +" AND dms.status = 'active' ORDER BY dms.last_message_time DESC ;")
            # contacts_list_one = kurs.fetchall()
            # kurs.execute("SELECT dms.id,dms.last_message_content, dms.last_message_sender_id, users.saxeli, users.gvari, users.imgsrc, dms.last_message_time, users.imgsize, users.status,dms.user_one, users.username  FROM dms INNER JOIN users ON dms.user_one = users.id WHERE dms.user_two = "+ str(aidi) +" AND dms.status = 'active' ORDER BY dms.last_message_time DESC ;")
            # contacts_list_two = kurs.fetchall()

            kurs.execute("SELECT dms.id,dms.last_message_content, dms.last_message_sender_id, users.saxeli, users.gvari, users.imgsrc, dms.last_message_time, users.imgsize, users.status,dms.user_two, users.username,dms.status,dms.user_one_seen FROM dms INNER JOIN users ON dms.user_two = users.id WHERE dms.user_one = "+ str(aidi) +"   ORDER BY dms.last_message_time DESC ;")
            contacts_list_one = kurs.fetchall()
            kurs.execute("SELECT dms.id,dms.last_message_content, dms.last_message_sender_id, users.saxeli, users.gvari, users.imgsrc, dms.last_message_time, users.imgsize, users.status,dms.user_one, users.username,dms.status,dms.user_two_seen  FROM dms INNER JOIN users ON dms.user_one = users.id WHERE dms.user_two = "+ str(aidi) +"   ORDER BY dms.last_message_time DESC ;")
            contacts_list_two = kurs.fetchall()

            contacts_list = contacts_list_one + contacts_list_two
            contacts_list_np = np.array(contacts_list)

            # kurs.execute("SELECT * FROM stalks WHERE stalker_id = "+ str(aidi) +";")

            kurs.execute("SELECT users.saxeli,users.gvari,users.imgsrc FROM stalks INNER JOIN users ON users.id= stalks.stalked_id WHERE stalks.stalker_id = "+ str(aidi) +" GROUP BY users.id ORDER BY stalks.id DESC;")


            stalked_list = kurs.fetchall()

            # contacts_nplist = np.array(contacts_list)
            
            united_contacts_list = contacts_list + stalked_list

            contacts_markup = ""
            

            if(len(contacts_list_np) > 0):
                contacts_list_np_ranked = contacts_list_np[np.argsort(contacts_list_np[:,6].astype(int))[::-1]]
            else:
                contacts_list_np_ranked = np.array([])
            

            dm_idebi = []
            contacts_content = {}
            

            for i in contacts_list_np_ranked:
                # contacts+= i
                contact_status = i[11]

                contact_unseeenMsg_count = int(i[12])
                
                if contact_unseeenMsg_count > 9:
                    contact_unseeenMsg_count_innerHTML = "9+"
                else:
                    contact_unseeenMsg_count_innerHTML = str(contact_unseeenMsg_count)

                if contact_unseeenMsg_count > 0:
                    contact_interaction_displayStyle = "block"
                else:
                    contact_interaction_displayStyle = "none"
                
                dm_idebi.append(i[0])



                # if dm aris

                # i[1]
                if contact_status != None:

                    
                    display_none_sty = ""
                    if len(i[1]) >= 30:
                        last_message_unwertiled = i[1][:30] + "..."
                    else:
                        last_message_unwertiled = i[1]
                    if int(i[2]) == aidi:

                        last_mesiji = Markup("<span style = 'font-weight:600'>შენ : </span>")  +last_message_unwertiled
                    else:
                        last_mesiji = last_message_unwertiled


                    contact_status_attr = "active"
                else:
                    display_none_sty = "display:none;"
                    last_message_unwertiled = ""
                    last_mesiji = ""
                    contact_status_attr = "inactive"
                    
                contact_saxeli = i[3]
                contact_gvari = i[4]
                contact_pfp = i[5]
                contact_pfp_size = i[7]


                activity_status = i[8]
                if activity_status == "1":
                    activity_status_color = "green"
                elif activity_status == "0":
                    activity_status_color = "grey"

                contact_username = i[10]
                

                # contact_dasaxeleba = contact_saxeli + "_" + contact_gvari
                contact_dasaxeleba = contact_username

                contacts_content[str(i[0])] =  {"username" : contact_username, "imgpfp" : contact_pfp, "imgsize" : contact_pfp_size,"saxeli" : contact_saxeli,"gvari" : contact_gvari, "user_id" : str(i[9])}
                contacts_markup+=Markup("""\n <div  request_status = '"""+str(contact_status_attr)+"""' style = '"""+ display_none_sty +"""' momxmarebeli = '"""+ str(i[9]) +"""'   class = 'contact """+ str(i[9]) +""" """+ str(i[2]) +"""' id = 'contact_"""+ str(i[0]) +"""'> <div class = 'contact_profile' id = 'contact_profile_"""+ str(i[0]) +"""' style="background-image:url('/"""+ contact_pfp +"""'); background-size : """+contact_pfp_size+"""% """+ str(contact_pfp_size) +"""% "><div class = 'status_div' style = 'background-color: """+activity_status_color+""";' id = 'status_div_"""+ str(i[9]) +"""' >  </div>""") + Markup("""</div> <div class = 'contact_saxeli_gvari' >""")+contact_dasaxeleba +Markup(""" </div> <div class = 'contact_last_message' id = 'contact_last_message_"""+ str(i[0]) +"""' >
                

                <div class="wave" style = "display:none" id = 'wave_"""+ str(i[0]) +"""'>

                    <span class="dot one"></span>
                    <span class="dot two"></span>
                    <span class="dot three"></span>
                    

                </div>


                <span class = "contact_last_message_p" id = 'contact_last_message_p_"""+ str(i[0]) +"""' > """)  +last_mesiji +Markup("""</span></div> 
                
                <div style='display:"""+ contact_interaction_displayStyle +"""' value = '"""+ str(contact_unseeenMsg_count) +"""' class = "contact_interaction" id = 'contact_interaction_"""+ str(i[0]) +"""'>"""+ contact_unseeenMsg_count_innerHTML +"""</div>

                </div>
                
                <br style = '"""+  display_none_sty +"""' id = 'contact_breaki_"""+ str(i[0]) +"""'> \n""")

                # if i[2] != aidi:


            if chat == "main":

                chat_aidi = "main"                
            else:
                try:
                    chat_aidi = int(chat)

                except:
                    print("num eror chat_aidi = int(request.args.get('chat'))")
            
            chatstr_id = str(chat_aidi)


            

            dm_idebi = json.dumps(dm_idebi)
            dm_idebi = Markup(dm_idebi)
            contacts_content = Markup(json.dumps(contacts_content))

            kurs.execute("SELECT * FROM notifications WHERE notification_recipient_id = "+ str(aidi) +" OR (notification_recipient_id = 0 AND notification_time > "+ str(join_time) +") ORDER BY id DESC;")
            nots = np.array(kurs.fetchall())
            not_count = 0

            for i in nots:
                if int(i[8]) == 0:
                    not_count+=1

            if not_count > 9:
                not_count_markup = "9+"
            else:
                not_count_markup = str(not_count)


            csrftk = csrftok(int(straidi))
            return render_template("messenger.html",straidi=straidi,contacts_content=contacts_content,my_profile_link=my_profile_link,dm_idebi=dm_idebi,chatstr_id=chatstr_id,saxeli=saxeli,imgsrc=imgsrc,fuli=fuli,imgsize=imgsize,contacts=contacts_markup,
            not_count=str(not_count),not_count_markup=not_count_markup,csrftk=csrftk)





@app.route("/dmchat_query",methods=["GET","POST"])
def dmchat_query():
    # time.sleep(5)
    if request.cookies.get("c_user") != None and request.cookies.get("xs") != None:
        c_user = request.cookies.get("c_user")
        xs = request.cookies.get("xs")
        
        authi = auth(c_user,xs)
        if authi == True:
            # db = mysql.connector.connect(
            #     host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )
            kurs = db.cursor()
            kurs.execute("SELECT id FROM users WHERE username = '"+ c_user +"';")
            
            kursf = kurs.fetchone()
            aidi = kursf[0]

            dm_aidi = request.form["dm_aidi"]
            dm_type = request.form["type"]
            otaxi = request.form["dm_aidi"]
            fromi = int(request.form["from"])
            print(dm_type,fromi)
            # print("UPDATE dm_msgs SET state = 'seen' WHERE dmchat_id = "+ str(dm_aidi) +"  AND sender_id != "+ str(aidi) +";")
            # kurs.execute("UPDATE dm_msgs SET state = 'seen' WHERE dmchat_id = "+ str(dm_aidi) +"  AND sender_id != "+ str(aidi) +";")
            db.commit()
            kurs.execute("SELECT dm_msgs.id, dm_msgs.message, dm_msgs.sender_id, dm_msgs.message_type, dm_msgs.message_date, users.username, users.imgsrc, users.imgsize, dm_msgs.message_dtype, dm_msgs.reply_to_msgid, dm_msgs.message_status		 FROM dm_msgs INNER JOIN users ON dm_msgs.sender_id = users.id WHERE dmchat_id	= "+ str(dm_aidi) +" ORDER BY id; ")

            messages_data = kurs.fetchall()
            msg_raod = len(messages_data)

            kurs.execute("UPDATE dm_msgs SET seen_by_other = 1 WHERE dmchat_id = " + str(dm_aidi) +" AND sender_id != "+ str(aidi) +";")


            #fe

            
            kurs.execute("SELECT user_one,user_two FROM dms WHERE id = "+ str(otaxi) +";")

            

            user_identif = kurs.fetchone()
            if user_identif[1] == aidi:
                dasa_unseen_updatebeli = "user_two"
            elif user_identif[0] == aidi:
                dasa_unseen_updatebeli = "user_one"

            kurs.execute("UPDATE dms SET "+ dasa_unseen_updatebeli +"_seen = 0 WHERE id = "+ str(otaxi)+ " ; ")
            

            db.commit()
            messages_data_np = messages_data #np.array(messages_data)
            nzoma = len(messages_data_np) -1
            indexi_arithm_left = nzoma  - fromi
            indexi_arithm_right = indexi_arithm_left + 15  #nzoma 
            
            messages_data_np = messages_data_np[indexi_arithm_left:indexi_arithm_right]

            print(indexi_arithm_left,indexi_arithm_right,messages_data_np)
            print(len(messages_data_np))

            if dm_type == "open":
                messages_markup = ""
            elif dm_type == "add":
                messages_data_np = messages_data_np[::-1]
                messages_markup = []


            


            for i in messages_data_np:
                msg_id = i[0]
                msg_the_msg = i[1]
                msg_sender_id = i[2]
                msg_message_type = i[3]
                msg_message_date = i[4]
                msg_username = i[5]
                msg_imgsrc = i[6]
                msg_imgsize = i[7]

                msg_dtype = i[8]

                reply_to_msgid = i[9]

                msg_the_msg+=""

                if msg_dtype == None:
                    # button_main_list_leftStyle = "60"
                    button_main_list_leftStyle = "70"
                else:
                    # button_main_list_leftStyle = "10"
                    button_main_list_leftStyle = "70"


                if int(aidi) == int(msg_sender_id):
                    msg_sender_nick = "მე"
                else:
                    msg_sender_nick = msg_username

                if msg_dtype == "img":
                    # kont = Markup("""<img loading = "lazy" class = "msg_img" src = '/"""+msg_the_msg +"""' >""")
                    kont = Markup("""<img  class = "msg_img" src = '/"""+msg_the_msg +"""' >""")
                    
                elif msg_dtype == "vid":
                    ext = msg_the_msg.split(".")[len(msg_the_msg.split("."))-1]
                    kont = Markup("""<video class = "msg_img" controls> <source src = '/""")+ msg_the_msg + Markup("""' type = 'video/""")+ext+Markup("""'> </video>""")
                else:
                    kont = msg_the_msg
                    if i[10] == "edited":
                        kont+=Markup("""<span class="redaqtirebuli_label"> (რედაქტირებული)</span>""")
                if int(aidi) == int(msg_sender_id):
                    if msg_dtype == None:
                        msg_edit_btn_var = """ <div id = 'msg_edit_btn_"""+ str(msg_id)  +"""' class = 'msg_edit_btn mod_btn'></div>"""
                    else:
                        msg_edit_btn_var = """"""
                    my_msg_options = msg_edit_btn_var + """ <div id = 'msg_delete_btn_"""+ str(msg_id)  +"""' class = 'msg_delete_btn mod_btn'></div>"""
                else:
                    my_msg_options = ""
                
                if reply_to_msgid == None:
                
                    themarkup=Markup("""
                    <div class = "net_message_div" deliverd = 'true'  msg_dtype = '"""+ str(msg_dtype)  +"""' id = 'netmessage_div_"""+ str(msg_id) +"""'>
                        <div class = 'message_div' id = 'message_div_"""+ str(msg_id) +"""'>
                            <div class = 'message_pfp_div'>
                                <div class = 'message_pfp' style= "background-image : url('/"""+msg_imgsrc+"""'); background-size : """+ msg_imgsize+"""% """+ msg_imgsize+"""%"></div>
                            </div>   
                            <div class = 'message_content_div'> 
                                <div class = 'message_content_username message_content_username_"""+ str(msg_id) +"""'>""")+ msg_sender_nick + Markup(""" </div> 
                                <div class = 'message_content_msg message_content_msg_"""+ str(msg_id) +"""'>""")+ kont + Markup("""<span class = 'redaqtirebuli_label'></span></div>  
                            </div> 
                            <div id = 'button_main_list_"""+ str(msg_id) +"""' class = "button_main_list" style = 'left: """+ str(button_main_list_leftStyle) +"""%; '> 
                                <div id = 'msg_reply_btn_"""+ str(msg_id)  +"""' class = 'msg_reply_btn mod_btn'></div> """+ my_msg_options +""" </div> 
                            </div> 
                        </div>
                    <br id = 'breaki_"""+ str(msg_id) +"""' >
                     """)
                else:
                    rep_indx = np.where(messages_data_np[:,0].astype(int) ==int(reply_to_msgid))

                    texti = messages_data_np[rep_indx,:][0][0]
                    # print(texti)

                    
                    replyed_msg_dtype = texti[8]

                    if replyed_msg_dtype == None:
                        replyed_msg_content = texti[1]
                    else:
                        replyed_msg_content = Markup("""<span class = 'reply_file_label'>ფაილი</span> <div class = 'reply_file_icon reply_img_icon' ></div>""")
                    
                    replyed_msg_owner_id = int(texti[2])
                    replyed_msg_id = int(texti[0])

                    if replyed_msg_owner_id == int(aidi):
                        replyed_msg_owner = "მე"
                    else:

                        replyed_msg_owner = "@"+texti[5]
                    
                    print("replyed to msg : " + replyed_msg_content + " , " + replyed_msg_owner)
                    # if dm_type
                    themarkup=Markup("""<div class = "net_message_div" deliverd = 'true' msg_dtype = '"""+ str(msg_dtype)  +"""'  id = 'netmessage_div_"""+ str(msg_id) +"""'> <div class = 'replyed_to replyed_"""+str(msg_id)+"""' id = 'replyed_to_""")+str(replyed_msg_id)+Markup("""'> <div class = "reply_line">  </div> <div class = "replyed_to_text"> <span class="replyed_to_username" >""")+replyed_msg_owner + Markup(""" : </span>""") + replyed_msg_content + Markup("""</div>  </div><div class = 'message_div' id = 'message_div_"""+ str(msg_id) +"""'> <div class = ""></div>    <div class = 'message_pfp_div'> <div class = 'message_pfp' style= "background-image : url('/"""+msg_imgsrc+"""'); background-size : """+ msg_imgsize+"""% """+ msg_imgsize+"""%"></div> </div>   <div class = 'message_content_div'> <div class = 'message_content_username message_content_username_"""+ str(msg_id) +"""'>""")+ msg_sender_nick + Markup(""" </div> <div class = 'message_content_msg message_content_msg_"""+ str(msg_id) +"""'>""")+ kont + Markup("""<span class = 'redaqtirebuli_label'></span></div>  </div> <div style = 'left : """+str(button_main_list_leftStyle)+"""%;' id = 'button_main_list_"""+ str(msg_id) +"""' class = "button_main_list"> <div id = 'msg_reply_btn_"""+ str(msg_id)  +"""' class = 'msg_reply_btn mod_btn'></div> """+ my_msg_options +""" </div> </div> </div> <br  id = 'breaki_"""+ str(msg_id) +"""' >""")
                if dm_type == "open":
                    messages_markup+=themarkup
                elif dm_type == "add":
                    messages_markup.append(themarkup)

            db.commit()
            if dm_type == "open":
                return messages_markup
            elif dm_type == "add":
                if len(messages_data_np) > 0:
                    return jsonify(messages_markup)
                else:
                    return "false"



@app.route("/delete_service",methods=["GET","POST"])
def delete_service():
    if request.cookies.get("c_user") != None and request.cookies.get("xs") != None:
        c_user = request.cookies.get("c_user")
        xs = request.cookies.get("xs")
        if auth(c_user,xs) == True:
            # db = mysql.connector.connect(
            #     host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )
            kurs = db.cursor()
            kurs.execute("SELECT id FROM users WHERE username = '"+ c_user +"';")

            aidi = kurs.fetchone()[0] 
            serid = request.form["serid"]

            kurs.execute("SELECT id FROM users WHERE username = '"+ c_user +"';")

            u_aidi = kurs.fetchone()[0]

            #NOTEservisebze mushaobisas daimaxsovre rom owneridit spesivifacia rom bug ar agmochndes!!!!!!!!!!!!!!!!!!

            kurs.execute("DELETE FROM servisebi WHERE id = "+ str(serid) +" AND owner_id = "+ str(aidi) +";")

            

            kurs.execute("DELETE FROM points WHERE service_id = "+ str(serid) +" AND owner_id = "+ str(aidi) +";")  

            kurs.execute("DELETE FROM servisebis_history WHERE service_id = "+ str(serid) +" AND owner_id = "+ str(aidi) +";") 

            kurs.execute("DELETE FROM servisebis_reitingi WHERE service_id = "+ str(serid) +" AND owner_id = "+ str(aidi) +";") 
            

            kurs.execute("SELECT id,satauri,profile,fasi,maxfasi,status FROM servisebi WHERE owner_id = "+ str(aidi) +" ORDER BY id DESC;")
            
            service = "" #Markup('<div class = "service_row">')

            service_row = ""
            serx = 0

            kurz = kurs.fetchall()
            
            for i in kurz:
                service_aidi = i[0]
                #service+= Markup('<div class = "servisi">' + i[1] + '</div>')
                # iebi = [a for a in i]

                if i[4] == None:
                    maxfasi = ""
                else:
                    if i[3] < i[4]:
                        maxfasi = " - $"  + str(i[4])
                    else:
                        maxfasi = ""

                iebi = i[5]
                # iebi = []
                # iebi.append(i[0])
                # iebi.append(i[1])
                # iebi.append(i[2])
                # iebi.append(i[3])
                

                # if (None in iebi) == False:
                if iebi == "active":


                    kurs.execute("SELECT main_rating FROM servisebis_reitingi WHERE service_id = "+ str(i[0]) +";")
                    rating_ls = [float(a[0]) for a in kurs]
                    if len(rating_ls) != 0:
                        rating_cifr = str(np.mean(rating_ls))

                        rating = "⭐"+ rating_cifr.split(".")[0] + "." + rating_cifr.split(".")[1][0] #x
                    else:
                        rating = ""


                    zervacia_id ='"service_'+ str(service_aidi) + '"'
                    serx+=1
                    service_row+= Markup('<div id = '+zervacia_id+' class = "servisi" style="width:30%;"><img  id = "service_'+ str(service_aidi) +'_img"  class = "service_img" src = "static/services/')+ i[2] +Markup('"><p id = "service_'+ str(service_aidi) +'_tit" class = "service_tit" >') + i[1] + Markup('</p><div  class = "serv_data"><span class = "rating">'+rating + '</span>              <span class = "fasi" ><span id = "dollar">$</span>'+ str(i[3]) + maxfasi +'</span></div></div>')
                    if serx % 3 == 0:
                        #service+=Markup('</div>') + "\n" + Markup('<div class = "service_row">')
                        service+=Markup('<div style= "width:100%;" class = "service_row">') + service_row + Markup("</div><br>") + "\n"
                        service_row = ""


                elif iebi == "paused":
                    if  True: #u_aidi == chemi_id:
                        kurs.execute("SELECT main_rating FROM servisebis_reitingi WHERE service_id = "+ str(i[0]) +";")
                        if i[0] != None:
                            rating_ls = [float(a[0]) for a in kurs]
                            if len(rating_ls) != 0:
                                rating_cifr = str(np.mean(rating_ls))

                                rating = "⭐"+ rating_cifr.split(".")[0] + "." + rating_cifr.split(".")[1][0] #o
                            else:
                                rating = ""
                        else:
                            rating = ""

                        if i[2] != None:
                            profili_src =  i[2]
                        else:
                            profili_src = "logos_white.png"
                        
                        if i[3] != None:
                            service_fasi = Markup('<span id = "dollar">$</span>') + str(i[3])
                        else:
                            service_fasi = ""
                        
                        

                        serx+=1
                        zervacia_id ='"service_'+ str(service_aidi) + '"'

                        
                        service_row+= Markup('<div id = '+zervacia_id  +' class = "servisi paused_servisi" style="background-color:rgb(8, 130, 112,0.3);width:30%;"><img id = "service_'+ str(service_aidi) +'_img" class = "service_img" src = "static/services/')+ profili_src +Markup('"><p  id = "service_'+ str(service_aidi) +'_tit" class = "service_tit" style="opacity:0.3"  >') + i[1] + Markup('</p><div  class = "serv_data"><span class = "rating">') + rating + Markup('</span>            <span class = "fasi"  >')+ service_fasi  + maxfasi+ Markup('</span></div><h2 style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);color:yellow;font-size:25px;opacity:0.7;" class = "restricred_lb">დაპაუზებული<h2></div>')
                        if serx % 3 == 0:
                            #service+=Markup('</div>') + "\n" + Markup('<div class = "service_row">')
                            service+=Markup('<div style= "width:100%;" class = "service_row">') + service_row + Markup("</div><br>") + "\n"
                            service_row = ""


                else: #drafti mafti
                    if True: #u_aidi == chemi_id:
                        kurs.execute("SELECT main_rating FROM servisebis_reitingi WHERE service_id = "+ str(i[0]) +";")
                        if i[0] != None:
                            rating_ls = [float(a[0]) for a in kurs]
                            if len(rating_ls) != 0:
                                rating_cifr = str(np.mean(rating_ls))

                                rating = "⭐"+ rating_cifr.split(".")[0] + "." + rating_cifr.split(".")[1][0] #o
                            else:
                                rating = ""
                        else:
                            rating = ""

                        if i[2] != None:
                            profili_src = i[2]
                        else:
                            profili_src = "logos_white.png"
                        
                        if i[3] != None:
                            service_fasi = Markup('<span id = "dollar">$</span>') + str(i[3])
                        else:
                            service_fasi = ""
                        
                        

                        serx+=1
                        zervacia_id ='"service_'+ str(service_aidi) + '"'
                        # if uzer == c_user:
                        #     serviewlink = Markup('"http://localhost:5000/create_new_service?num=1&service='+ str(service_aidi) +'"') #chekkkkkk pointn                        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffzzzzzzzzzzzzzzzzzzzzzzz
                        # else:
                        #     serviewlink = Markup('"http://localhost:5000/service/'+ str(service_aidi) +'"')
                        
                        service_row+= Markup('<div id = '+zervacia_id  +' class = "servisi draft_servisi" style="background-color:rgb(8, 130, 112,0.3);width:30%;"><img id = "service_'+ str(service_aidi) +'_img" class = "service_img" src = "static/services/')+ profili_src +Markup('"><p  id = "service_'+ str(service_aidi) +'_tit" class = "service_tit" style="opacity:0.3" >') + i[1] + Markup('</p><div  class = "serv_data"><span class = "rating">') + rating + Markup('</span>             <span class = "fasi"  >')+ service_fasi  + maxfasi+ Markup('</span></div><h2 style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);color:yellow;font-size:30px;opacity:0.7;" class = "restricred_lb">დრაფტი<h2></div>')
                        if serx % 3 == 0:
                            #service+=Markup('</div>') + "\n" + Markup('<div class = "service_row">')
                            service+=Markup('<div style= "width:100%;" class = "service_row">') + service_row + Markup("</div><br>") + "\n"
                            service_row = ""


                
                

                
            
            
            serx+=1
            
            # mevar_es = uzer == c_user

            if serx% 3 != 0:
                bolozoma = 33 * ((serx % 3) )
                bolozomaw = 30 / (bolozoma/100)

                
                
                if True: #mevar_es:
                    damatebis_serviceblock = Markup('<div id = "add_service" style="font-size:30px;text-align:center;width:'+ str(bolozomaw) +'%;" class = "servisi"> <img  id = "add_img"src = "static/add.png"><p id = "create_new_service_p">ახალის შექმნა</p></div>')
                else:
                    damatebis_serviceblock = ""
                service += Markup('<div style= "width:'+ str(bolozoma) +'%;" class = "service_row">')  + service_row.replace('width:30%;','width:'+ str(bolozomaw) +'%;') +damatebis_serviceblock + Markup('</div>') + '\n'
            else:
                
                if True: #mevar_es:
                    damatebis_serviceblock = Markup('<div id = "add_service" style="font-size:30px;text-align:center;width:33%;" class = "servisi"><img  id = "add_img"src = "static/add.png"> <p id = "create_new_service_p">ახალის შექმნა</p> </div>')
                else:
                    damatebis_serviceblock= ""
                
                service+= Markup('<div style= "width:100%;" class = "service_row">') + service_row + damatebis_serviceblock + Markup('</div>')
            

            db.commit()
            return service #"success"




@app.route("/pfps/<foto>")
def pfp_foto(foto):

    return send_file("static/" + foto)

@app.route("/")
def index():
    # db = mysql.connector.connect(
    #     host=host,
    #         user=user,
    #         passwd = passwd,
    #         database= database
    #     )

    kurs = db.cursor()
    # request.environ.get('HTTP_X_REAL_IP', request.remote_addr)   
    ip = request.environ.get("HTTP_X_REAL_IP",request.remote_addr)
    print("AIPI",ip)
    print(request.headers["User-Agent"])
    kurs.execute("INSERT INTO site_joins(ipaddr,time,date) VALUES('"+ str(ip) + "',"+ str(int(time.time())) +",'"+ str(str(datetime.datetime.now())) +"')")
    
    db.commit()
    if request.cookies.get("c_user") == None or request.cookies.get("xs") == None:
        
        return render_template("index.html")
    else:
        
        if auth(request.cookies.get("c_user"),request.cookies.get("xs"),tipi="cookie") == True:
            c_user = request.cookies.get("c_user")
            xs = request.cookies.get("xs")
            # db = mysql.connector.connect(
            # host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )

            kurs = db.cursor()
            kurs.execute("SELECT saxeli,imgsrc,username,angarishi,imgsize,id,join_time FROM users WHERE username = '" + c_user +"';")

            kursf = kurs.fetchone()
            aidi = kursf[5]
            straidi = str(aidi)

            saxeli = kursf[0]
            imgsrc = kursf[1]
            imgsize = kursf[4]

            username = kursf[2]

            angarishi = kursf[3]
            
            anga = str(angarishi)
            join_time = kursf[6]

            pf_lnk = "http://"+request.headers.get('host')+"/" + username


            # notifications_box
            kurs.execute("SELECT user_one_seen FROM dms WHERE user_one = "+ str(aidi) +";")
            kurs_one = kurs.fetchall()
            kurs.execute("SELECT user_two_seen FROM dms WHERE user_two = "+ str(aidi) +";")
            kurs_two = kurs.fetchall()

            kurs_united = kurs_one + kurs_two
            message_notification_value = 0
            for i in kurs_united:
                message_notification_value+= i[0]
            if message_notification_value > 9:
                message_notification_value_shortened = "9+"
            else:
                message_notification_value_shortened = str(message_notification_value)
            message_notification_value = str(message_notification_value)
            # 

            # mailbox
            kurs.execute("SELECT * FROM notifications WHERE notification_recipient_id = "+ str(aidi) +" OR (notification_recipient_id = 0 AND notification_time > "+ str(join_time) +") ORDER BY id DESC;")
            nots = np.array(kurs.fetchall())
            not_count = 0

            for i in nots:
                if int(i[8]) == 0:
                    not_count+=1

            if not_count > 9:
                not_count_markup = "9+"
            else:
                not_count_markup = str(not_count)
                
            the_notifications_markup = ""

            # for i in nots[:10]:
            #     thenotmark = Markup(""" """)

            #     the_notifications_markup+=thenotmark
            




            csrftk = csrftok(int(aidi))
            

            return render_template("loggedmain.html",straidi=straidi,saxeli=saxeli,imgsrc=imgsrc,my_profile_link=pf_lnk,fuli=anga,imgsize=imgsize,
            message_notification_value=message_notification_value, message_notification_value_shortened=message_notification_value_shortened,
            not_count=str(not_count),not_count_markup=not_count_markup,csrftk=str(csrftk))


@app.route("/notificatino_dasinva")
def notificatino_dasinva():
    if request.cookies.get("c_user") == None or request.cookies.get("xs") == None:
        
        return render_template("index.html")
    else:
        
        if auth(request.cookies.get("c_user"),request.cookies.get("xs")) == True:
            c_user = request.cookies.get("c_user")
            xs = request.cookies.get("xs")
            # db = mysql.connector.connect(
            # host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )

            kurs = db.cursor()
            kurs.execute("SELECT * FROM users WHERE username = '"+ c_user +"';")
            kursf = kurs.fetchone()
            aidi = kursf[0]

            notification_id = request.form["notification_id"]
            


@app.route("/notifications_query",methods=["GET","POST"])
def notifications_query():
    if request.cookies.get("c_user") == None or request.cookies.get("xs") == None:
        
        return render_template("index.html")
    else:
        print("notreq")
        if auth(request.cookies.get("c_user"),request.cookies.get("xs")) == True:
            c_user = request.cookies.get("c_user")
            xs = request.cookies.get("xs")
            # db = mysql.connector.connect(
            # host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )

            kurs = db.cursor()
            kurs.execute("SELECT * FROM users WHERE username = '"+ c_user +"';")
            kursf = kurs.fetchone()
            aidi = kursf[0]
            join_time = kursf[20]

            index = int(request.form["index"])
            kurs.execute("UPDATE notifications SET  notification_seen_bool= 1 WHERE notification_recipient_id = "+ str(aidi) +";")

            db.commit()    
            kurs.execute("SELECT * FROM notifications WHERE notification_recipient_id = "+ str(aidi) +" OR (notification_recipient_id = 0 AND notification_time > "+ str(join_time) +")  ORDER BY id DESC;")

            notifications = kurs.fetchall()
                
            if len(notifications) > 0:
                bolonot = notifications[len(notifications)-1]
                bolo_notis_id = bolonot[0]

                
                markapi = ""
                # if index != 0:
                #     # pass
                #     # time.sleep(20)
                sairatebeli = notifications[index:index+10]
                # for i in sairatebeli:
                # # for i in notifications:
                #     divi = Markup(""" 
                #     <div onclick = "window.location.href = '""")+i[5]  +Markup("""';" id = 'not_div_"""+str(i[0])  +"""' class = "not_div">
                #         <div style = "background-image:url('""")+i[2] +Markup("""')" class = "not_img"></div>
                #         <div class = "not_cont_outer">
                #             <div class ="not_title">""")+ i[3] +Markup("""</div>
                #             <div class = "not_time"></div>
                #         </div>
                #     </div>
                #     """)
                #     markapi+=divi

                
                # return markapi
                empty="false"
                return jsonify([sairatebeli,bolo_notis_id,empty])
            else:
                sairatebeli = ""
                bolo_notis_id = ""

                empty="true"


                return jsonify([sairatebeli,bolo_notis_id,empty])
            # kurs.execute("SELECT * FROM ")



# SELECT servisebi.id, servisebi.satauri,points.id,points.saxeli,points.point,points.service_id FROM servisebi RIGHT JOIN points ON servisebi.id = points.service_id WHERE servisebi.satauri NOT LIKE "%asd%";
def rating_staticfilt_update(kurs,sfero=None,subsfero=None):

    if subsfero != None and subsfero != "None" and subsfero != "none":
        subsfero_nawili =  "AND offer_subtipi = '" + str(subsfero) +"'"
    else:
        subsfero_nawili = ""

    print("SELECT fasi FROM servisebi WHERE offer_tipi = '"+ str(sfero) +"' "+ subsfero_nawili +" AND status != 'paused';")
    kurs.execute("SELECT fasi FROM servisebi WHERE offer_tipi = '"+ str(sfero) +"' "+ subsfero_nawili +" AND status != 'paused';")
    
    kursf = kurs.fetchall()



    
    if (subsfero in ("None","none",None,"სხვა") ) == False:
        
        if (subsfero in unselected_point_dict):
            point_data_offc_ls = unselected_point_dict[subsfero]
            if len(point_data_offc_ls) > 0:
                unselected_points_divs = "" #Markup("<div id = 'unselected_points'>")
                
                # pyautogui.alert(str(subsfero))
                print(subsfero,json.loads(point_data_offc_ls))
                for i in json.loads(point_data_offc_ls):
                    
                    # unselected_points_divs+= Markup("<div id = 'po_div"+ i["name"] +"' class = 'po_div po_div"+ i["name"] +"'><input id = 'po_fasi_"+ i["name"] +"'  maxlength='10' placeholder = 'თანხა($)' class = 'po_fasi'><input id = 'po_time_"+ i["name"] +"'  maxlength='3' placeholder = 'დღე' class = 'po_time' value = '")+Markup("'><input id = 'po_points_"+ i["name"] +"' class = 'po_points' maxlength='3' value = '")+ i["points"] +Markup("'><div class = 'po_name'>") + i["name"] + Markup("</div><div class = 'select_point_button'><div id = 'select_point_button_img_"+ i["name"] +"' class = 'select_point_button_img select_point_button_img_"+ i["name"] +"'></div></div></div>" + "") + ""
                    unselected_points_divs+= Markup("<div id = 'po_div"+ i["name"] +"' class = 'po_div po_div"+ i["name"] +"'>""")+Markup("<input id = 'po_points_"+ i["name"] +"' class = 'po_points' maxlength='3' value = '")+ i["points"] +Markup("'><div class = 'po_name'>") + i["name"] + Markup("</div><div class = 'select_point_button'><div id = 'select_point_button_img_"+ i["name"] +"' class = 'select_point_button_img select_point_button_img_"+ i["name"] +"'></div></div></div>" + "") + ""
                    
                subsfero_selected = "true"
                # unselected_points_divs+= Markup("</div>")
            else:
                point_data_offc_ls = json.dumps([])
                unselected_points_divs = Markup("""  <h3 id="shesadzleblobebi_outer_nosubsfero_title">
                                ამ სუბსფეროზე შესაძლებლობების ფილტრი ჯერჯერობით შეუძლებელია
                            </h3> """)
                subsfero_selected = "false"

        else:
            point_data_offc_ls = json.dumps([])
            unselected_points_divs = Markup("""  <h3 id="shesadzleblobebi_outer_nosubsfero_title">
                            ამ სუბსფეროზე შესაძლებლობების ფილტრი ჯერჯერობით შეუძლებელია
                        </h3> """)
            subsfero_selected = "false"
    else:
        point_data_offc_ls = json.dumps([])
        unselected_points_divs = Markup("""  <h3 id="shesadzleblobebi_outer_nosubsfero_title">
                            შესაძლებლობების ფილტრაციისათვის აირჩიეთ სუბსფერო
                        </h3> """)
        subsfero_selected = "false"
        
    data = {}
    data["unselected_points_divs"] = unselected_points_divs
    data["unselected_points_data"] = point_data_offc_ls
    data["subsfero_selected"] = subsfero_selected

    if len(kursf) > 0:
        kursf_np = np.array(kursf).astype(int)
        # kursf_npr = kursf_np.reshape((1,len(kursf_np)))
        kursf_npr = kursf_np.reshape((len(kursf_np),1))


        sarecomendirebuli_raodenoba = 20 # minimumi ricxvi rac aris sachiro rom useristvis fasebi datvalos da iafi,sashualo,dzviri gaurkvios
        sarecomendirebuli_raodenoba = 5
        
        
        # print(len(kursf_npr) >= sarecomendirebuli_raodenoba,np.std(kursf_npr) > 10,len(kursf_npr),np.std(kursf_npr))
        # print(kursf_npr)
        # print(type(np.std(kursf_npr)))
        # if len(kursf_npr) >= sarecomendirebuli_raodenoba and np.std(kursf_npr) > 10:
        if len(kursf_npr) >= sarecomendirebuli_raodenoba:
            if np.std(kursf_npr) > 10:
                
                data["range"] = {}

                data["range"]["mid"] = np.mean(kursf_npr)



                data["range"]["low"] = np.mean(kursf_npr) - np.std(kursf_npr)
                data["range"]["high"]  = np.mean(kursf_npr) + np.std(kursf_npr)


                data["bool"] = True
                
            else:
                data["bool"] = False
        else:
            data["bool"] = False
    else:
        data["bool"] = False
    

    
    return data
    
def fasi_pre_staticinput_rads_f(kurs,req_args_dict__sfero,req_args_dict__subsfero):
    data = {}
    print(req_args_dict__sfero,req_args_dict__subsfero,(req_args_dict__sfero != None and req_args_dict__subsfero != None) and (req_args_dict__sfero != "none" and req_args_dict__subsfero != "none") and (req_args_dict__sfero != "None" and req_args_dict__subsfero != "None"))
    # if (req_args_dict__sfero != None and req_args_dict__subsfero != None) and (req_args_dict__sfero != "none" and req_args_dict__subsfero != "none") and (req_args_dict__sfero != "None" and req_args_dict__subsfero != "None"):
    rating_staticfilt_apdeiti = rating_staticfilt_update(kurs,req_args_dict__sfero,req_args_dict__subsfero)
    if (req_args_dict__sfero != None and req_args_dict__subsfero != None):
    
        if rating_staticfilt_apdeiti["bool"] == True:
            fas_txtinput_coststyle_clsnm = "fas_txtinput_noradio_rever"

            fasirange_low = rating_staticfilt_apdeiti["range"]["low"]
            fasirange_mid = rating_staticfilt_apdeiti["range"]["mid"]
            fasirange_high = rating_staticfilt_apdeiti["range"]["high"]


            fasirange_low_mk = str(int(fasirange_low* 100)/100)
            fasirange_mid_mk = str(int(fasirange_mid* 100)/100)
            fasirange_high_mk = str(int(fasirange_high* 100)/100)

            fasirange_low_mark = Markup(f"<span class = 'statfilt_fasi_radiobuts_thefasi'>${fasirange_low_mk}</span> და ქვემოთ")
            fasirange_mid_mark = Markup(f"<span class = 'statfilt_fasi_radiobuts_thefasi'>${fasirange_low_mk}</span> - <span class = 'statfilt_fasi_radiobuts_thefasi'>${fasirange_high_mk}</span>")
            fasirange_high_mark = Markup(f"<span class = 'statfilt_fasi_radiobuts_thefasi'>${fasirange_high_mk}</span> და ზემოთ")


            
            
            fasi_pre_staticinput_rads = f"""
                <input class = "gamocdileba_radiobut fasi_radiobut " style = "margin-top:20px"  id = "fasi_radiobut_iafi" type="radio" name = "fasi" valua = 'down_{fasirange_low_mk}'>
                <label class = "gamocdileba_radiobut_label" id = "fasi_radiobut_iafi_label" for="fasi_radiobut_iafi">იაფი({fasirange_low_mark})</label>
                <br>
                <input class = "gamocdileba_radiobut fasi_radiobut " id = "fasi_radiobut_normal" type="radio" name = "fasi" valua = '{fasirange_low_mk}_{fasirange_high_mk}' >
                <label   class = "gamocdileba_radiobut_label" id = "fasi_radiobut_normal_label" for="fasi_radiobut_normal" >საშუალო({fasirange_mid_mark})</label>
                <br>
                <input class = "gamocdileba_radiobut fasi_radiobut " id = "fasi_radiobut_dzviri" type="radio" name = "fasi" valua = '{fasirange_high_mk}_up'>
                <label   class = "gamocdileba_radiobut_label" id = "fasi_radiobut_dzviri_label" for="fasi_radiobut_dzviri" >ძვირი({fasirange_high_mark})</label>
                <br>
                
                <input class = "gamocdileba_radiobut fasi_radiobut " id = "fasi_radiobut_kerdzo" type="radio" name = "fasi">
                <label   class = "gamocdileba_radiobut_label" id = "fasi_radiobut_kerdzo_label" for="fasi_radiobut_kerdzo" >კერძო</label>
                <br>
            """
        else:
            fas_txtinput_coststyle_clsnm = "fas_txtinput_noradio"
            fasi_pre_staticinput_rads = ""
    else:
        fas_txtinput_coststyle_clsnm = "fas_txtinput_noradio"
        fasi_pre_staticinput_rads = ""
    data["fas_txtinput_coststyle_clsnm"] = fas_txtinput_coststyle_clsnm
    data["fasi_pre_staticinput_rads"] = fasi_pre_staticinput_rads
    
    data["unselected_points_divs"] = rating_staticfilt_apdeiti["unselected_points_divs"]
    data["unselected_points_data"] = rating_staticfilt_apdeiti["unselected_points_data"]

    data["subsfero_selected"] = rating_staticfilt_apdeiti["subsfero_selected"]

    # fasi_pre_staticinput_rads"
    
    return data





# sfero


@app.route("/service/<service_id>")
def service(service_id):
    if request.cookies.get("c_user") == None or request.cookies.get("xs") == None:
        red = f"http://{request.headers.get('host')}/login?redirect=service/{service_id}"
        print(red)
        return redirect(red) #render_template("index.html")

    else:
        
        if auth(request.cookies.get("c_user"),request.cookies.get("xs"),tipi="cookie") == True:
            c_user = request.cookies.get("c_user")
            xs = request.cookies.get("xs")
            # db = mysql.connector.connect(
            # host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )

            kurs = db.cursor()
            kurs.execute("SELECT saxeli,imgsrc,username,angarishi,imgsize,id,join_time FROM users WHERE username = '" + c_user +"';")

            kursf = kurs.fetchone()
            aidi = kursf[5]
            straidi = str(aidi)

            saxeli = kursf[0]
            imgsrc = kursf[1]
            imgsize = kursf[4]

            username = kursf[2]

            angarishi = kursf[3]
            
            anga = str(angarishi)
            join_time = kursf[6]

            pf_lnk = "http://"+request.headers.get('host')+"/" + username


            # notifications_box
            kurs.execute("SELECT user_one_seen FROM dms WHERE user_one = "+ str(aidi) +";")
            kurs_one = kurs.fetchall()
            kurs.execute("SELECT user_two_seen FROM dms WHERE user_two = "+ str(aidi) +";")
            kurs_two = kurs.fetchall()

            kurs_united = kurs_one + kurs_two
            message_notification_value = 0
            for i in kurs_united:
                message_notification_value+= i[0]
            if message_notification_value > 9:
                message_notification_value_shortened = "9+"
            else:
                message_notification_value_shortened = str(message_notification_value)
            message_notification_value = str(message_notification_value)
            # 

            # mailbox
            kurs.execute("SELECT * FROM notifications WHERE notification_recipient_id = "+ str(aidi) +" OR (notification_recipient_id = 0 AND notification_time > "+ str(join_time) +") ORDER BY id DESC;")
            nots = np.array(kurs.fetchall())
            not_count = 0

            for i in nots:
                if int(i[8]) == 0:
                    not_count+=1

            if not_count > 9:
                not_count_markup = "9+"
            else:
                not_count_markup = str(not_count)
                
            the_notifications_markup = ""

            print("SELECT * FROM servisebi WHERE id = "+ str(service_id) +" AND status = 'active' ")
            kurs.execute("SELECT * FROM servisebi WHERE id = "+ str(service_id) +" AND status = 'active' ")
            kursf = kurs.fetchone()
            

            
            if kursf != None:

                service_ownerid = kursf[9]

                kurs.execute("SELECT * FROM users WHERE id = "+ str(service_ownerid) +";")

                kurssu = kurs.fetchone() #kurs

                kurs.execute("SELECT * FROM servisebis_history WHERE service_id = "+ str(service_id) +" ;")
                kurshi = kurs.fetchall()

                kurs.execute("SELECT * FROM points WHERE service_id = "+ str(service_id) +" ;")
                kurspo = kurs.fetchall()

                kurs.execute("SELECT * FROM orders WHERE ordered_service_id  = %(service_id)s ;", {"service_id" : int(service_id)}    )
                # kurs.execute("SELECT * FROM orders WHERE ordered_service_id  = "+ str(service_id) +" ;")
                
                kurs_ord = kurs.fetchall()


                service_id = kursf[0]
                service_satauri = kursf[1]
                service_agwera=kursf[2]
                service_minfasi = kursf[3]
                
                service_sfero = kursf[5]
                service_subsfero = kursf[6]

                service_dro = kursf[16]

                service_max_clients = str(kursf[20])

                

                service_profile = kursf[10]

                service_suratebi_ls = []
                service_suratebi_ls.append(service_profile)
                if kursf[19] != None:
                    for i in json.loads(kursf[19]):
                        if json.loads(kursf[19])[i] != "none":
                            service_suratebi_ls.append(json.loads(kursf[19])[i])
                print(service_suratebi_ls)
                if len(service_suratebi_ls) > 1:
                    img_sliders_markup =Markup("""

                        <div id = "left_img_slider" class = "img_slider_button"></div>
                        <div id = "right_img_slider" class = "img_slider_button"></div>
                        """
                    )
                else:
                    img_sliders_markup = ""

                servisebi_user_username = kurssu[3]

                servisebi_user_id = kurssu[0]
                servisebi_user_saxeli = kurssu[1]

                

                servisebi_user_pfp = kurssu[10]
                servisebi_user_pfpsize = kurssu[12]

                if service_ownerid == aidi:
                    services_mine = "true"
                    contact_innerText = "რედაქტირება"
                else:
                    services_mine = "false"
                    contact_innerText = "დაკონტაქტება"
                recordni= ""

                unselected_points_divs = ""
                for i in kurspo:

                    # unselected_points_divs+=Markup("<div id = 'po_div"+ i["name"] +"' class = 'po_div po_div"+ i["name"] +"'><input id = 'po_fasi_"+ i["name"] +"'  maxlength='10' placeholder = 'თანხა($)' class = 'po_fasi'><input id = 'po_time_"+ i["name"] +"'  maxlength='3' placeholder = 'დღე' class = 'po_time' value = '")+Markup("'><input id = 'po_points_"+ i["name"] +"' class = 'po_points' maxlength='3' value = '")+ i["points"] +Markup("'><div class = 'po_name'>") + i["name"] + Markup("</div><div class = 'select_point_button'><div id = 'select_point_button_img_"+ i["name"] +"' class = 'select_point_button_img select_point_button_img_"+ i["name"] +"'></div></div></div>" + "") + ""
                    unselected_points_divs+=Markup("<div id = 'po_div"+ i[6] +"' class = 'po_div po_div"+ i[6] +"'><input id = 'po_fasi_"+ i[6] +"'  maxlength='10' placeholder = 'თანხა($)' class = 'po_fasi' value = '")+ str(i[2]) +Markup("$' disabled><input id = 'po_time_")+ i[6] +Markup("'  maxlength='7' placeholder = 'დღე' class = 'po_time' value = '")+ str(i[3])+ Markup(" დღე' disabled>") + Markup("<div class = 'po_name'>") + i[6] + Markup("</div><div class = 'select_point_button'><div id = 'select_point_button_img_")+ i[6] +Markup("' class = 'select_point_button_img select_point_button_img_")+ i[6] +Markup("'></div></div></div>" + "") + Markup("<br>")
                    

                for i in kurshi:
                    hi_record_id = i[0]
                    hi_satauri = i[2]

                    hi_agwera = i[3]
                    
                    if i[6] != None:
                        hi_fasi = i[6]
                    else:
                        hi_fasi = 0

                    if i[4] != None:
                        hi_dro = i[4]
                    else:
                        hi_dro = 0

                    
                    hi_tipi = i[5]

                
                    hi_kvira = 7
                    if hi_dro > 0:
                        if hi_dro > (hi_kvira):
                            hi_tve = hi_kvira * 4
                            if hi_dro > hi_tve:
                                hi_dros = "- "+str(hi_dro/(hi_tve)).split(".")[0] + " თვე"
                            else:

                                hi_dros = "- "+str(hi_dro/(hi_kvira)).split(".")[0] + " კვირა"
                        else:
                            hi_dros = "- "+str(hi_dro).split(".")[0] + "დღე"
                    else:
                        hi_dros = ""
                    

                    # recordni+= Markup('<div id = "'+ str(i[0]) +'" class="mkwrivi"><p id = "record_mkwrivi_satauri_'+ str(i[0]) +'" class="record_mkwrivi_satauri">') + hi_satauri + Markup('</p> <p id = "ful_dro_'+ str(i[0 ]) +'" class = "ful_dro">')+ str(hi_fasi) + Markup("<span style = 'color:lightgreen;'>$</span>") +" " + hi_dros  + Markup('</p> <div id = "rec_opt_btn_'+ str(hi_record_id) +'" class = "rec_options_btn"></div> </div>')
                    recordni+= Markup('<div id = "'+ str(i[0]) +'" class="mkwrivi"><p id = "record_mkwrivi_satauri_'+ str(i[0]) +'" class="record_mkwrivi_satauri">') + hi_satauri + Markup('</p> <p id = "ful_dro_'+ str(i[0 ]) +'" class = "ful_dro">')+ str(hi_fasi) + Markup("<span style = 'color:lightgreen;'>$</span>") +" " + hi_dros  + Markup('</p>  </div>')
                    

                #  service_dro

                
                # servisebi_user_username servisebi_user_id
                # service_max_clients kurs_ord clientebi_label_sp_digit

                # kurs_ord = "4398"
                
                
                if kurs_ord == None:
                    # service_current_clients = "0"
                    service_current_clients = Markup("<span value = '0' class = 'clientebi_label_sp_digit'><span style='top: 50%; left: 50%; transform: translate(-50%, -50%); position: absolute; z-index: 3;' id = 'mid'>0</span></span>")
                else:
                    # service_current_clients = str(len(kurs_ord))
                    service_current_clients = ""
                    ixi = 0
                    raodi = str(len(kurs_ord))
                    # raodi = input("ricxv : ")
                    # if raodi == "":
                    #     raodi = "4399"
                    for i in range(0,len(service_max_clients)- len(raodi)):
                        service_current_clients += Markup("<span value = '"+ "0" +"' id = 'clientebi_label_sp_digit_"+ str(ixi) +"' class = 'clientebi_label_sp_digit'><span style='top: 50%; left: 50%; transform: translate(-50%, -50%); position: absolute; z-index: 3;' id = 'mid_"+ str(ixi) +"'>")+"0"+Markup("</span></span>") 
                        ixi+=1

                    for i in raodi:
                        
                        service_current_clients += Markup("<span value = '"+ i +"' id = 'clientebi_label_sp_digit_"+ str(ixi) +"' class = 'clientebi_label_sp_digit'><span style='top: 50%; left: 50%; transform: translate(-50%, -50%); position: absolute; z-index: 3;' id = 'mid_"+ str(ixi) +"'>")+i+Markup("</span></span>")
                        ixi+=1
                    
                    # service_current_clients = Markup("<span class = 'clientebi_label_sp_digit'>")+str(len(kurs_ord))+Markup("</span>")

                
                csrftk = csrftok(int(straidi))
                return render_template("service.html",straidi=straidi,saxeli=saxeli,imgsrc=imgsrc,my_profile_link=pf_lnk,fuli=anga,imgsize=imgsize,
                message_notification_value=message_notification_value, message_notification_value_shortened=message_notification_value_shortened,
                not_count=str(not_count),not_count_markup=not_count_markup,
                service_id=str(service_id),service_satauri=service_satauri,service_agwera=service_agwera,service_current_clients=service_current_clients,service_max_clients=service_max_clients,service_minfasi=service_minfasi,service_dro=service_dro,service_profile=service_profile ,service_sfero=service_sfero , service_subsfero=service_subsfero, img_sliders_markup=img_sliders_markup ,service_suratebi_ls=Markup(json.dumps(service_suratebi_ls)),# service args
                servisebi_user_id=str(servisebi_user_id),servisebi_user_saxeli=servisebi_user_saxeli,services_mine=services_mine,contact_innerText=contact_innerText,servisebi_user_username=servisebi_user_username,servisebi_user_pfp=servisebi_user_pfp,servisebi_user_pfpsize=servisebi_user_pfpsize,
                recordni=recordni,unselected_points_divs=unselected_points_divs,
                domen="http://"+request.headers.get('host'),csrftk=csrftk)

            else:
                return "service not found"



@app.route("/query_services",methods=["GET","POST"])
def query_services():
    print(request.args.get("points_ls"))
    if request.cookies.get("c_user") == None or request.cookies.get("xs") == None:
        
        return render_template("index.html")
    else:
        
        if auth(request.cookies.get("c_user"),request.cookies.get("xs"),tipi="cookie") == True:
            c_user = request.cookies.get("c_user")
            xs = request.cookies.get("xs")
            # db = mysql.connector.connect(
            # host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )

            kurs = db.cursor()
            kurs.execute("SELECT saxeli,imgsrc,username,angarishi,imgsize,id,join_time FROM users WHERE username = '" + c_user +"';")

            kursf = kurs.fetchone()


            saxeli = kursf[0]
            imgsrc = kursf[1]
            imgsize = kursf[4]
            aidi = kursf[5]

            straidi = str(aidi)

            username = kursf[2]

            join_time = kursf[6]

            angarishi = kursf[3]
            anga = str(angarishi)

            # try
            pf_lnk = "http://"+request.headers.get('host')+"/" + username
            
            if request.method == "GET":
                if request.args.get("gamocdileba") != None:
                    gamocdileba_valua = request.args.get("gamocdileba")
                else:
                    gamocdileba_valua = "25"

                
                if request.args.get("fasi") != None:
                    fasi_valua = request.args.get("fasi")
                else:
                    fasi_valua = "25"

                
                if request.args.get("shesadzleblobebi") != None:
                    shesadzleblobebi_valua = request.args.get("shesadzleblobebi")
                else:
                    shesadzleblobebi_valua = "25"


                if request.args.get("pasuxismgebloba") != None:
                    pasuxismgebloba_valua = request.args.get("pasuxismgebloba")
                else:
                    pasuxismgebloba_valua = "25"
            

 

            # return str(request.method == "GET")
            if request.method == "GET":
                # notifications_box
                kurs.execute("SELECT user_one_seen FROM dms WHERE user_one = "+ str(aidi) +";")
                kurs_one = kurs.fetchall()
                kurs.execute("SELECT user_two_seen FROM dms WHERE user_two = "+ str(aidi) +";")
                kurs_two = kurs.fetchall()

                kurs_united = kurs_one + kurs_two
                message_notification_value = 0
                for i in kurs_united:
                    message_notification_value+= i[0]
                if message_notification_value > 9:
                    message_notification_value_shortened = "9+"
                else:
                    message_notification_value_shortened = str(message_notification_value)
                message_notification_value = str(message_notification_value)


                # mailbox
                kurs.execute("SELECT * FROM notifications WHERE notification_recipient_id = "+ str(aidi) +" OR (notification_recipient_id = 0 AND notification_time > "+ str(join_time) +") ORDER BY id DESC;")
                nots = np.array(kurs.fetchall())
                not_count = 0

                for i in nots:
                    if int(i[8]) == 0:
                        not_count+=1

                if not_count > 9:
                    not_count_markup = "9+"
                else:
                    not_count_markup = str(not_count)
                    





                srch =  request.args.get("srch").strip() #request.args.get("srch")

                searched_text = srch

                if request.args.get("page") == None:
                    page = 1
                else:
                    page = int(request.args.get("page"))


            elif request.method == "POST":

                srch =  request.form["search_text"].strip() #request.args.get("srch")

                searched_text = srch

                if request.form["page"] == None:
                    page = 1
                else:
                    page = int(request.form["page"])
            
            

                




            limiti = page * 20

            # if srch[0] == "(" and srch[len(srch)-1] == ")":
            if srch == "[დეტალური ძებნა]": #tu detaluria
                # query_likes = srch 
                query_likes = ""
                if request.method == "POST":
                    sityva_romelime = request.form["sityva_romelime_input"].split()
                    sityva_yvela = request.form["sityva_yvela_input"].split()
                    sityva_gamoricxe = request.form["sityva_gamoricxe_input"].split()
                    sityva_zusti = request.form["sityva_zusti_input"]
                elif request.method == "GET":
                    sityva_romelime = request.args.get("sityva_romelime_input").split()
                    sityva_yvela = request.args.get("sityva_yvela_input").split()
                    sityva_gamoricxe = request.args.get("sityva_gamoricxe_input").split()
                    sityva_zusti = request.args.get("sityva_zusti_input")
                query_likes+= "("
                
                sityva_romelime_bool = False
                for i in sityva_romelime:
                    query_likes += " lower(servisebi.satauri) LIKE '%"+ i.lower() +"%' OR  lower(servisebi.tags) LIKE '%"+ i.lower() +"%' OR "
                    sityva_romelime_bool = True
                if sityva_romelime_bool:
                    query_likes+= "1=2) AND ("

                sityva_yvela_bool = False
                for i in sityva_yvela:
                    query_likes += " ( lower(servisebi.satauri) LIKE '%"+ i.lower() +"%' OR  lower(servisebi.tags) LIKE '%"+ i.lower() +"%') AND "
                    sityva_yvela = True
                
                query_likes+= "1=1) AND ("

                for i in sityva_gamoricxe:
                    query_likes += " ( lower(servisebi.satauri) NOT LIKE '%"+ i.lower() +"%' AND  lower(servisebi.tags) NOT LIKE '%"+ i.lower() +"%') AND "

                query_likes+= "1=1) "

                # for i in sityva_zusti:
                if sityva_zusti.strip() != "":
                    query_likes+="AND ("
                    query_likes += " lower(servisebi.satauri) LIKE '%"+ sityva_zusti.lower() +"%' )"
                



                
            else:
                query_likes = ""

                for i in srch.split(): #pracentebi shignit '%website%'
                    query_likes += " servisebi.satauri LIKE  '%"+ str(i) +"%' OR"
                    query_likes+= " servisebi.tags LIKE  '%"+ str(i).upper() +"%' OR "
                query_likes+=" 1=2"

            static_likes = " 1=1 "


            # req_args_dict__sfero = request.args.get("sfero")
            # req_args_dict__subsfero = request.args.get("subsfero")

            # static filt
            if request.method == "GET":
                if request.args.get("sfero") != None and request.args.get("sfero") != "none":
                    static_likes+= " AND servisebi.offer_tipi = '"+ request.args.get("sfero") +"' "
                    

                if request.args.get("subsfero") != None and request.args.get("subsfero") != "none":
                    static_likes+= " AND servisebi.offer_subtipi = '"+ request.args.get("subsfero") +"' "
                
                req_args_dict__sfero = request.args.get("sfero")
                req_args_dict__subsfero = request.args.get("subsfero")


                radiogamo_var = request.args.get("radiogamo")
            
                if request.args.get("minimaluri_fasi") != None:
                    if request.args.get("minimaluri_fasi").strip() != "" and request.args.get("minimaluri_fasi") != "down":
                        
                        radiominfasi_var = float(request.args.get("minimaluri_fasi"))
                    else:
                        radiominfasi_var = 0
                else:
                    radiominfasi_var = 0
                
                if request.args.get("maximaluri_fasi") != None:
                    if request.args.get("maximaluri_fasi").strip() != "" and request.args.get("maximaluri_fasi") != "up":
                        radiomaxfasi_var = float(request.args.get("maximaluri_fasi"))
                    else:
                        radiomaxfasi_var = 1131043*900
                else:
                    radiomaxfasi_var = 1131043*900

                
                        

            elif request.method == "POST":
                if request.form.get("sfero") != "none":
                    static_likes+= " AND servisebi.offer_tipi = '"+ request.form.get("sfero") +"' "

                if request.form.get("subsfero") != "none":
                    static_likes+= " AND servisebi.offer_subtipi = '"+ request.form.get("subsfero") +"' "
                
                req_args_dict__sfero = request.form.get("sfero")
                req_args_dict__subsfero = request.form.get("subsfero")

                radiogamo_var = request.form["radiogamo"]


                if request.form["minimaluri_fasi"] != None:
                    if request.form["minimaluri_fasi"].strip() != "" and request.form["minimaluri_fasi"] != "down":

                        radiominfasi_var = float(request.form["minimaluri_fasi"])
                    else:
                        radiominfasi_var = 0.0
                else:
                    radiominfasi_var = 0.0

                if request.form["maximaluri_fasi"] != None:
                    if request.form["maximaluri_fasi"].strip() != "" and request.form["maximaluri_fasi"] != "up" :
                        radiomaxfasi_var = float(request.form["maximaluri_fasi"])
                    else:
                        radiomaxfasi_var = 1131043*900
                else:
                    radiomaxfasi_var = 1131043*900




                
            if radiogamo_var != None and str(radiogamo_var).strip() != "":
                # radiogamo = 
                if(radiogamo_var == "gamocdileba_radiobut_junior"):
                    gamocdileba_range = [0,3*365]
                elif(radiogamo_var == "gamocdileba_radiobut_gamocdili"):
                    gamocdileba_range = [3*365,7.5*365]
                elif(radiogamo_var == "gamocdileba_radiobut_expert"):
                    gamocdileba_range = [7.5*365,1131043*900]
                elif ("kerdzo" in radiogamo_var) == True :
                    if radiogamo_var.split("kerdzo")[0].strip() != "":
                        gamocdileba_range_0 = float(radiogamo_var.split("kerdzo")[0]) * 365
                    else:
                        gamocdileba_range_0 = 0
                    print(radiogamo_var.split("kerdzo")[1].strip())
                    if radiogamo_var.split("kerdzo")[1].strip() != "":
                        gamocdileba_range_1 = float(radiogamo_var.split("kerdzo")[1]) * 365
                    else:
                        gamocdileba_range_1 = 1131043*900
                        
                    gamocdileba_range = [gamocdileba_range_0,gamocdileba_range_1]

            else:
                gamocdileba_range = None
            print(gamocdileba_range,gamocdileba_range == None,type(gamocdileba_range))
            

            if request.method == "POST":
                if request.form["points_ls"] != "" and  request.form["points_ls"] != None:
                    points_ls = json.loads(request.form["points_ls"])
                    points_ls_names= []

                    for i in points_ls:
                        points_ls_names.append(i["name"])
                else:
                    points_ls = []
                    points_ls_names= []
            elif request.method == "GET":
                if request.args.get("points_ls") != "" and  request.args.get("points_ls") != None:
                    points_ls = json.loads(request.args.get("points_ls"))
                    points_ls_names= []

                    for i in points_ls:
                        points_ls_names.append(i["name"])
                else:
                    points_ls = []
                    points_ls_names= []
            
            
            # if gamocdileba_range != None:
            #     static_likes+=" AND  (SELECT SUM(servisebis_history.xani) FROM servisebis_history ) >=  "+ str(gamocdileba_range[0]) +" AND  (SELECT SUM(servisebis_history.xani) FROM servisebis_history) <=  "+ str(gamocdileba_range[1]) +" "
            
            # if (radiomaxfasi_var != None and str(radiomaxfasi_var).strip() != ""):
                # static_likes+=" AND  (SELECT SUM(servisebis_history.xani) FROM servisebis_history ) >=  "+ str(gamocdileba_range[0]) +""

            # points

            servisebis_saserchi_kursquery = "SELECT servisebi.id ,servisebi.satauri ,servisebi.fasi ,servisebi.client_raodenoba ,servisebi.profile , servisebi.main_rating ,servisebi.pasuxismgebloba_rating ,servisebi.as_described_rating ,servisebi.dro ,servisebi.maxfasi ,servisebi.maxdro ,servisebi.points, servisebi.max_clients, servisebi.rated, servisebi.gamocdileba_fasi, servisebi.gamocdileba_time, servisebis_history.xani ,points.saxeli         FROM servisebi LEFT JOIN points ON servisebi.id = points.service_id LEFT JOIN servisebis_history ON servisebi.id = servisebis_history.service_id  WHERE status = 'active' AND ("+ query_likes +" ) AND ("+ static_likes +");"
            print(servisebis_saserchi_kursquery)
            
            kurs.execute(servisebis_saserchi_kursquery)

            servisebi_markup = ""

            ixi = 0

            
            servisebi = kurs.fetchall() #[i for i in kurs]


            
            limiti = page * 20

            limiti_from = (page-1) * 20

                            
            # servisebinp_alt = np.array(servisebi)
            servisebinp_alt_alt = np.array(servisebi)
            servisebinp_alt = np.array([])
            servisebinp =np.array([])

            x = 0
            y = 0
            # servisebinp_alt_dict = {"gamo_xani" : {}}
            servisebinp_alt_dict_gamoxani = {}
            servisebinp_alt_dict_points = {}
            for i in servisebinp_alt_alt:
                
                if i[16] != None: #tu 
                    if (i[0] in servisebinp_alt_dict_gamoxani) == False:
                        servisebinp_alt_dict_gamoxani[i[0]] = i[16]
                        
                    else:
                        servisebinp_alt_dict_gamoxani[i[0]] += i[16]
                else:
                    servisebinp_alt_dict_gamoxani[i[0]] = 0

                if i[17] != None:
                    if (i[0] in servisebinp_alt_dict_points) == False:
                        servisebinp_alt_dict_points[i[0]] = [i[17]] 
                    else:
                        servisebinp_alt_dict_points[i[0]].append(i[17])
                
                else:
                    servisebinp_alt_dict_points[i[0]] = []
            
                    # servisis_gamocdileba_xani = 0
                    # servisis_gamocdileba_xani+= i[16]
                
            

                # servisis_gamocdileba_xani = servisebinp_alt_dict_gamoxani[i[0]]
            for i in servisebinp_alt_alt:
                # print(i)
                if len(servisebinp_alt) == 0:
                
                    
                    y+=1
                    i[16] = servisebinp_alt_dict_gamoxani[i[0]]
                    i[17] = servisebinp_alt_dict_points[i[0]]
                    servisebinp_alt = np.append(servisebinp_alt,i)
                    
                    servisebinp_alt = servisebinp_alt.reshape((y,servisebinp_alt_alt.shape[1]))
                    

                else:
                    
                    if (int(i[0]) in servisebinp_alt[:,0].astype(int)) == False:
                        y+=1
                        i[16] = servisebinp_alt_dict_gamoxani[i[0]]
                        i[17] = servisebinp_alt_dict_points[i[0]]
                        servisebinp_alt = np.append(servisebinp_alt,i)
                        
                        servisebinp_alt = servisebinp_alt.reshape((y,servisebinp_alt_alt.shape[1]))


            # servisebinp_alt[:,16] = servisebinp_alt_dict_gamoxani[servisebinp_alt[:,0].astype(int)]

            for i in servisebinp_alt:
                
                # print(i)

                # if i[16] == None:
                #     i[16] = 0
                # if i[17] == None:
                #     i[17] = 0

                # print(i[16],gamocdileba_range)
                # radiomaxfasi_var
                # radiominfasi_var

                
                # mocemuli_gamocdileba =  i[16]
                # servisebis_saserchi_kursquery = "SELECT servisebi.id ,servisebi.satauri ,servisebi.fasi ,servisebi.client_raodenoba ,servisebi.profile , servisebi.main_rating ,servisebi.pasuxismgebloba_rating ,servisebi.as_described_rating ,servisebi.dro ,servisebi.maxfasi ,servisebi.maxdro ,servisebi.points, servisebi.max_clients, servisebi.rated, servisebi.gamocdileba_fasi, servisebi.gamocdileba_time, servisebis_history.xani         FROM servisebi LEFT JOIN servisebis_history ON servisebi.id = servisebis_history.service_id  WHERE status = 'active' AND ("+ query_likes +" ) AND ("+ static_likes +");"
            
                servisis_gamocdileba_xani = i[16]

                if gamocdileba_range != None:
                    if i[16] == None:
                        if  gamocdileba_range[0] == 0:
                            gamocdileba_bool = True
                        else:
                            gamocdileba_bool = False
                        
                    else:
                        
                        gamocdileba_bool = gamocdileba_range[0] <= servisis_gamocdileba_xani and servisis_gamocdileba_xani <= gamocdileba_range[1]
                else:
                    gamocdileba_bool = True

                fasi_bool = radiominfasi_var <= i[2] <= radiomaxfasi_var

                shesadzleblobebi_bool = True # if shesadzlebloba 
                # points_ls_names
                # print(points_ls_names)
                
                for a in points_ls_names:
                    if (a in i[17]) == False:
                        shesadzleblobebi_bool = False


                


                if gamocdileba_bool and fasi_bool and shesadzleblobebi_bool:
                    
                    x+=1
                    servisebinp = np.append(servisebinp,i)
                    
                    servisebinp = servisebinp.reshape((x,servisebinp_alt.shape[1]))

            if servisebinp != np.array([]):
            # if len(servisebi) > 0:

                    # for a in i:
                    #     if a != None:
                    #         servisebinp = np.append(servisebinp,a)
                    #     else:
                    #         servisebinp = np.append(servisebinp,a)
                # servisebinp = servisebinp.reshape(servisebinp_alt.shape)



                shedegi_count = str(len(servisebinp)) + " შედეგი"
                #maxclients 12

                

                if request.method == "POST":

                    gamocdileba_demand = float(request.form["gamocdileba_demand"])
                    fasi_demand = float(request.form["fasi_demand"])
                    points_demand =float(request.form["points_demand"])
                    rating_demand = float(request.form["rating_demand"])
                                    


                    


                    # rkp =  (gamocdileba ** (gamocdileba_demand/10)) * (sash_fasi ** ( fasi_demand/10)) * (shesadzleblobebi ** (points_demand/10) ) * (rating ** (rating_demand/10))  * (servisebinp[:,0].astype(int)**2) #(servisebinp[:,12].astype(int) / servisebinp[:,2].astype(int)).reshape((servisebinp.shape[0],1))
                    # rkp = rkp.reshape((len(rkp),1))

                elif request.method == "GET":
                    

                    # rkp = (servisebinp[:,12].astype(int) / servisebinp[:,2].astype(int)).reshape((servisebinp.shape[0],1))

                    gamocdileba_demand = int(gamocdileba_valua)
                    fasi_demand = int(fasi_valua)
                    points_demand = int(shesadzleblobebi_valua)
                    rating_demand = int(pasuxismgebloba_valua)


                gamocdileba = servisebinp[:,14].astype(int) * servisebinp[:,15].astype(int) #14-15

                sash_fasi = (servisebinp[:,2].astype(int) + servisebinp[:,9].astype(int))/2

                shesadzleblobebi = servisebinp[:,11].astype(int)
                
                

                rating = servisebinp[:,5].astype(int) * 20


                    # rkp =  (gamocdileba ** (gamocdileba_demand/10)) * (sash_fasi ** ( fasi_demand/10)) * (shesadzleblobebi ** (points_demand/10) ) * (rating ** (rating_demand/10))  * (servisebinp[:,0].astype(int)**2)
                    # rkp = rkp.reshape((len(rkp),1))


                # print(shesadzleblobebi)
                # gamyofi = 10
                gamyofi = 100
                rkp =  (gamocdileba ** (gamocdileba_demand/gamyofi)) * (sash_fasi ** ( fasi_demand/gamyofi)) * (shesadzleblobebi ** (points_demand/gamyofi) ) * (rating ** (rating_demand/gamyofi))  * (servisebinp[:,0].astype(int)**2) #(servisebinp[:,12].astype(int) / servisebinp[:,2].astype(int)).reshape((servisebinp.shape[0],1))
                rkp = rkp.reshape((len(rkp),1))


                
                results = np.concatenate((servisebinp,rkp),axis=1)
                # print(results)
                
                rkpindexi = 18 #len(results[1])-1

                results = results[np.argsort(results[:,rkpindexi])[::-1] ]

                motavsebuli = len(results) // 20

                final_results = results[limiti_from:limiti]
 

                no_shedegi = ""
            else:
                servisebinp = np.array([])

                shedegi_count = ""

                final_results = np.array([])

                motavsebuli = 1

                

                if request.method == "POST":
                    no_shedegi = "<h3 id = 'no_shedegi_label'>ვერ მოიძებნა</h3>"
                    return jsonify({"servisebi" : no_shedegi,"shedegi_count" : ""})
                elif request.method == "GET":
                    no_shedegi = Markup("<h3 id = 'no_shedegi_label'>ვერ მოიძებნა</h3>")
                

            
            # results = 
            page_switcher = Markup("<div class = 'page_switcher'>")

            if servisebinp != np.array([]):
                for i in range(1,motavsebuli+2):
                    klasi = ""
                    if int(i) == int(page):
                        klasi+= " selected_page_switch"
                    page_switcher+=Markup("<div class = 'page_switch"+ klasi +"' >") + str(i) + Markup("</div>")
                    
                
            page_switcher+=Markup("</div>")
        

            

            for i in final_results:

                if i[5] != None and i[13] == 1:
                    rating_cifr = int(i[5])

                    rating = "⭐"+ rating_cifr.split(".")[0] + "." + rating_cifr.split(".")[1][0] #d
                else:
                    rating = ""

                if i[2] != None:
                    service_fasi = str(i[2])
                else:
                    service_fasi = ""


                if i[4] == None:
                    maxfasi = ""
                else:
                    if i[2] < i[9]:
                        maxfasi = " - $"  + str(i[9])
                    else:
                        maxfasi = ""
                
                zervacia_id = '"service_' + str(i[0]) + '"'
                # if (ixi % 5)!= 0:
                #     lefti = str(100/(ixi % 5)) + "%"
                #     print(ixi % 5)
                # else:
                #     lefti = "20%"

                #     print(0)

                xutnasht = ixi % 4

                

                

                

                
                
                
                # service_block =Markup("""<a class = "service_a"><div onclick = " window.location.href= '/service/"""+ str(i[0]) +"""' " id = """+zervacia_id+""" style='left:"""+ leftindex +"""' class = "service" ><img class = "service_img" src = "static/services/""")+ i[4] +Markup('">') + i[1] + Markup('<div  class = "serv_data"><span class = "rating">'+rating + '</span>              <span class = "fasi" ><span id = "dollar">$</span>'+ service_fasi  + maxfasi+'</span></div></div></a>')
                service_block =Markup("""<div onclick = " window.location.href= '/service/"""+ str(i[0]) +"""' " id = """+zervacia_id+""" class = "service" ><img class = "service_img" src = "static/services/""")+ i[4] +Markup('">') + i[1] + Markup('<div  class = "serv_data"><span class = "rating">'+rating + '</span>              <span class = "fasi" ><span id = "dollar">$</span>'+ service_fasi  + maxfasi+'</span></div></div>')
                

                # if (ixi % 4) == 0:

                #     if ixi != 0:
                #         servisebi_markup+=Markup('</div>')
                #     # servisebi_markup+= Markup('<div class = "service_row">') + service_block
                #     servisebi_markup+= + service_block
                    
                # else:
                #     servisebi_markup+= service_block
                # ixi+=1

            # servisebi_markup+=Markup("</div>")
                servisebi_markup+=service_block

            mona = {"servisebi" : servisebi_markup + page_switcher,"shedegi_count" : shedegi_count}
            


            if request.method == "POST":
                monac = jsonify(mona)



                return monac
            elif request.method == "GET":
                points_ls_str = request.args.get("points_ls")
                if points_ls_str != None:

                    points_ls = json.loads(points_ls_str)
                    points_ls_str_mk = Markup(points_ls_str)
                else:
                    points_ls = []
                    points_ls_str_mk = Markup(json.dumps([]))
                


                if len(servisebi) > 0:
                    servisebi_markup+=Markup("<br>") + " \n "+page_switcher
                
                radiogamo = request.args.get("radiogamo")
                static_radiofilter_dict = {}
                # gamocdileba_radiobut_kerdzo
                if radiogamo != None:
                    if("kerdzo" in radiogamo): #gamocdileba_radiobut_kerdzo
                        static_radiofilter_dict_gamocdileba_opt = "gamocdileba_radiobut_kerdzo"
                        static_radiofilter_dict["gamocdileba"] = {"opt" : "gamocdileba_radiobut_kerdzo","min" : radiogamo.split("kerdzo")[0] , "max" : radiogamo.split("kerdzo")[1]}
                    else:
                        static_radiofilter_dict["gamocdileba"] = {"opt" : radiogamo.strip()}

                # servisebi_markup

                # <input class = "pirveli_radiobut" class = "gamocdileba_radiobut" id = "fasi_radiobut_iafi" type="radio" name = "fasi">
                # <label class = "gamocdileba_radiobut_label" for="fasi_radiobut_iafi">იაფი()</label>
                # <br>
                # <input class = "gamocdileba_radiobut" id = "fasi_radiobut_normal" type="radio" name = "fasi">
                # <label   class = "gamocdileba_radiobut_label" for="fasi_radiobut_normal" >საშუალო()</label>
                # <br>
                # <input class = "gamocdileba_radiobut" id = "fasi_radiobut_dzviri" type="radio" name = "fasi">
                # <label   class = "gamocdileba_radiobut_label" for="fasi_radiobut_dzviri" >ძვირი()</label>
                # <br>
                
                # <input class = "gamocdileba_radiobut" id = "fasi_radiobut_kerdzo" type="radio" name = "fasi">
                # <label   class = "gamocdileba_radiobut_label" for="fasi_radiobut_kerdzo" >კერძო</label>
                # <br>


                # rating_staticfilt_update(kurs,sfero,subsfero):


                # req_args_dict__sfero
                # req_args_dict__subsfero
                # print(req_args_dict__sfero,req_args_dict__subsfero)
                # print(req_args_dict__sfero == None,req_args_dict__subsfero == None)
                # if none arari sferoebi
                #       if isfunqcia trues aturnebs




                fasi_pre_staticinput_rads_data = fasi_pre_staticinput_rads_f(kurs,req_args_dict__sfero,req_args_dict__subsfero)

                unselected_points_divs = fasi_pre_staticinput_rads_data["unselected_points_divs"]


                radiochabdro = request.args.get('radiochabdro')

                csrftk = csrftok(int(straidi))
                return render_template("loggedmain_searched.html",straidi=straidi,no_shedegi=no_shedegi,shedegi_count=shedegi_count,searched_text=searched_text,servisebi_markup=servisebi_markup,saxeli=saxeli,imgsrc=imgsrc,my_profile_link=pf_lnk,fuli=anga,imgsize=imgsize,gamocdileba_valua=gamocdileba_valua,fasi_valua=fasi_valua,shesadzleblobebi_valua=shesadzleblobebi_valua,pasuxismgebloba_valua=pasuxismgebloba_valua,
                    message_notification_value=message_notification_value, message_notification_value_shortened=message_notification_value_shortened,
                    not_count=str(not_count),not_count_markup=not_count_markup,
                    req_args_dict__sfero=req_args_dict__sfero,req_args_dict__subsfero=req_args_dict__subsfero,
                    fas_txtinput_coststyle_clsnm=fasi_pre_staticinput_rads_data["fas_txtinput_coststyle_clsnm"],
                    static_radiofilter_dict=Markup(json.dumps(static_radiofilter_dict)),
                    fasi_pre_staticinput_rads=Markup(fasi_pre_staticinput_rads_data["fasi_pre_staticinput_rads"]),
                    radiochabdro=radiochabdro,
                    unselected_points_divs=unselected_points_divs,
                    subsfero_selected=fasi_pre_staticinput_rads_data["subsfero_selected"],
                    points_ls_str=points_ls_str_mk,csrftk=csrftk

                   
                    )
                    

@app.route("/fasi_n_points_pre_staticinput_rads_rt",methods=["GET","POST"])
def fasi_n_points_pre_staticinput_rads_rt():
    if request.cookies.get("c_user") == None or request.cookies.get("xs") == None:
        
        return render_template("index.html")
    else:
        
        if auth(request.cookies.get("c_user"),request.cookies.get("xs"),tipi="cookie") == True:
            
            c_user = request.cookies.get("c_user")
            xs = request.cookies.get("xs")
            # db = mysql.connector.connect(
            # host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )

            kurs = db.cursor()
            req_args_dict__sfero = request.form["sfero"]
            req_args_dict__subsfero = request.form["subsfero"]
            print(req_args_dict__sfero,req_args_dict__subsfero)

            if req_args_dict__sfero != "none" or req_args_dict__subsfero != "none":
                fasi_pre_staticinput_rads_data = fasi_pre_staticinput_rads_f(kurs,req_args_dict__sfero,req_args_dict__subsfero)
                
                

                return json.dumps(fasi_pre_staticinput_rads_data)


@app.route("/fasi_staticfilt_update",methods=["GET","POST"])
def fasi_staticfilt_update():
    pass




@app.route("/signup")
def signup():
    if request.cookies.get("c_user") == None and request.cookies.get("xs") == None:
        # if request.cookies.get("role") != None:
        if True:
            return render_template("signup.html")
        else:
            return redirect(url_for("roler"))
    else:
        return redirect(url_for("index"))
@app.route("/vcode_resend",methods=["GET","POST"])
def vcode_resend():
    
    # db = mysql.connector.connect(
    #     host=host,
    #             user=user,
    #             passwd = passwd,
    #             database= database
    #         )
    c_user = request.cookies.get("c_user")
    xs = request.cookies.get("xs")
    kurs = db.cursor()
    ip = request.environ.get("HTTP_X_REAL_IP",request.remote_addr)
    if auth(request.cookies.get("c_user"),request.cookies.get("xs")) == "unverified":
        kurs.execute("SELECT id FROM users WHERE username = '"+ c_user +"' ;")
        kursf = kurs.fetchone()
        aidi = kursf[0]
        wdro = time.time() - 84600
        kurs.execute("SELECT * FROM timeouts WHERE tipi = 'vresend' and dro > "+ str(wdro) +" ;")
        raod = len([i for i in kurs])

        if raod < 5:
            vcode = str(random.randint(100000,999999))
            
            kurs.execute("UPDATE users SET vcode = "+ str(vcode) +" WHERE username = '"+ c_user +"';")
            kurs.execute("INSERT INTO timeouts(tipi,aidi,dro,ip) VALUES('vresend','"+ str(aidi) +"',"+ str(int(time.time())) +",'" +  ip  +"');")
            db.commit()
            #kurs.execute("")
            return  "success"
        else:
            return "timeout"

@app.route("/roler")
def roler():
    return render_template("role.html")

@app.route("/signup_default",methods=["GET","POST"])
def signup_default():

    zaxeli = request.form.get("saxeli")
    gvari = request.form.get("gvari")
    c_user = request.form.get("c_user")
    xs = request.form.get("xs")
    if len(zaxeli) >= 2 and len(request.form.get("gvari")) >= 2:
        if len(c_user) < 60:
            
            # db = mysql.connector.connect(
            #     host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )
            kurs = db.cursor()
            kurs.execute("SELECT * FROM users WHERE username = '"+  c_user +"';")
            kurs_cuser = kurs.fetchone()

            if kurs_cuser == None:

                kurs.execute("SELECT * FROM users WHERE mail = '"+ request.form.get("mail") +"';")
            

                kursm = kurs.fetchone()

                if kursm == None:
                    if symcheck(c_user.lower()):
                        if len(zaxeli) < 15:
                            if len(gvari) < 20:
                                kurs = db.cursor()
                                vcode = str(random.randint(100000,999999))
                                enxs = hashlib.md5(hashlib.sha256(xs.encode("utf-8")).hexdigest().encode("utf-8")).hexdigest()
                                print("INSERT INTO users(username,password,vcode) VALUES('"+ c_user.lower() +"','"+ enxs +"',"+ vcode  +");")
                                kurs.execute("INSERT INTO users(username,password,vcode) VALUES('"+ c_user.lower() +"','"+ enxs +"',"+ vcode  +");")
                                db.commit()
                                return "success " + hashlib.sha256(xs.encode("utf-8")).hexdigest()
                            else:
                                return "ძალიან დიდი გვარი"
                        else:
                            return "ძალიან გრძელი სახელი"
                    else:
                        return "მომხმარებლის სახელი შეიძლება შეიცავდეს მხოლოდ a-z,'.','_' სიმბოლოებს და ციფრებს "
                else:
                    return "მეილი დაკავებულია"
            else:
                return "მომხმარებლის სახელი დაკავებულია"
        else:
            return "მომხმარებლის სახელი უნდა იყოს ყველაზე დიდი 60 სიმბოლოიანი"

    #pyautogui.alert(zaxeli)
    return "internal eror"

@app.route("/signup_extra")
def signup_extra():
    autho = auth(request.cookies.get("c_user"),request.cookies.get("xs"))
    if autho == "unverified":



        return render_template("signup_extra.html")
    else:
        return redirect("http://"+request.headers.get('host')+"/")

@app.route("/confirmation")
def confirmation():
    shedi = True
    for i in ["saxeli","gvari","mail","c_user","xs","mail","tve","ricxvi","weli","sqesi"]:
        if request.cookies.get(i) == None:
            shedi = False

    if shedi == True:
        if auth(request.cookies.get('c_user'),request.cookies.get("xs")) == "unverified":
            # db = mysql.connector.connect(
            #     host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )
            kurs = db.cursor()
            kurs.execute("SELECT * FROM users WHERE mail = '"+request.cookies.get("mail") +"';")
            if kurs.fetchone() == None:
                mail = request.cookies.get("mail") 

                return render_template("confirmation.html",mail=mail)
        else:
            return redirect(url_for("/login"))
    else:
        return redirect(url_for("/login"))

@app.route("/vcode_check",methods=["GET","POST"])
def vcode_check():
    shedi = True
    for i in ["saxeli","gvari","mail","c_user","xs","mail","tve","ricxvi","weli","sqesi"]:
        if request.cookies.get(i) == None:
            shedi = False

    if shedi == True:
        saxeli = request.cookies.get("saxeli")
        gvari = request.cookies.get("gvari")
        c_user = request.cookies.get("c_user")
        xs = request.cookies.get("xs")
        mail = request.cookies.get("mail")
        sqesi = request.cookies.get("sqesi")
        tve = request.cookies.get("tve")
        ricxvi = request.cookies.get("ricxvi")
        weli = request.cookies.get("weli")


        if auth(c_user,xs) == "unverified":
            # db = mysql.connector.connect(
            #     host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )
            kurs = db.cursor()
            kurs.execute("SELECT * FROM users WHERE mail = '"+mail+"';")
            kursf = kurs.fetchone()
            if kursf == None:
                kurs.execute("SELECT vcode,id FROM users WHERE username = '" + c_user + "';")

                
                kursza = kurs.fetchone()
                aidi = kursza[1]

                if kursza != None:
                    winadge = time.time() - 84600
                    kurs.execute("SELECT id FROM timeouts WHERE aidi = '"+ str(aidi) +"' AND tipi = 'vcode_check'  and dro > "+ str(winadge) +" ;")
                    
                    droebi = [i for i in kurs]

                    if len(droebi) <= 5:

                        kurs.execute("INSERT INTO timeouts(tipi,aidi,dro) VALUES('vcode_check','"+ str(aidi ) +"',"+ str(time.time()) +");")
                        db.commit()

                        if str(kursza[0]) == request.form.get("vcode"):

                            exylesion = (sqesi in ["mamri","mdedri"]) and (int(ricxvi) in list(range(0,31))) and (int(weli) in list(range(1922,2022))) and (tve in ["იანვარი","თებერვალი","მარტი","აპრილი","მაისი","ივნისი","ივლისი","აგვისტო","სექტემბერი","ოქტომბერი","ნოემბერი","დეკემბერი"])


                            if exylesion:

                                kurs.execute("UPDATE  users SET saxeli = '"+ saxeli +"' WHERE username = '"+  c_user +"';")
                                
                                kurs.execute("UPDATE  users SET gvari = '"+  gvari +"' WHERE username = '"+  c_user +"';")
                                kurs.execute("UPDATE  users SET  mail = '"+ mail +"' WHERE username = '"+  c_user +"';")
                                kurs.execute("UPDATE  users SET sqesi = '"+ sqesi +"' WHERE username = '"+  c_user +"';")

                                kurs.execute("UPDATE  users SET ricxvi= '"+ ricxvi +"' WHERE username = '"+  c_user +"';")
                                kurs.execute("UPDATE  users SET tve = '"+ tve +"' WHERE username = '"+  c_user +"';")
                                kurs.execute("UPDATE  users SET weli = '"+  weli+"' WHERE username = '"+  c_user +"';")

                                print("UPDATE  users SET join_time = "+ str(int(time.time())) +" WHERE username = '"+  c_user +"';")
                                kurs.execute("UPDATE  users SET join_time = "+ str(int(time.time())) +" WHERE username = '"+  c_user +"';")

                                kurs.execute("UPDATE  users SET vcode = 1 WHERE username = '"+  c_user +"';")

                                kurs.execute("INSERT INTO lancer_params(aidi) VALUES("+ str(aidi) +");")



                                db.commit()

                                #registracia

                                return "success"
                            else:
                                print("cookie missing")

                                
                        else:
                            
                            return "fail"
                    else:

                        return "timeout"
                #mail = request.cookies.get("mail") 
                #return render_template("confirmation.html",mail=mail)








@app.route("/upload_pfp",methods=["GET","POST"])
def upload_pfp():
    shedi = True
    # db = mysql.connector.connect(
    #             host=host,
    #             user=user,
    #             passwd = passwd,
    #             database= database
    # )
    kurs = db.cursor()
    for i in ["saxeli","gvari","mail","c_user","xs","mail","tve","ricxvi","weli","sqesi"]:
        if request.cookies.get(i) == None:
            shedi = False
    if request.cookies.get("c_user") != None and request.cookies.get("xs") != None:
        if auth(request.cookies.get("c_user"),request.cookies.get("xs")) == True:
            #if shedi == True:
            if True:


                kurs.execute("SELECT imgsrc,id, imgsize FROM users WHERE username = '"+ request.cookies.get("c_user") +"'; ")

                kf = kurs.fetchone()

                aidi = kf[1]
                zomar = kf[2]

                if request.method == "POST" :
                    if (request.files["yile"].filename != "" and request.files["yile"].filename != None):
                        surati = request.files["yile"]
                        zoma = request.form["zoma"]

                        
                        saxeli = surati.filename

                        indexi = saxeli.split(".")[len(saxeli.split("."))-1]
                        if indexi in ["jpg","jpeg","png"]:


                            
                            surati = request.files["yile"]

                            patyh = "static/" + str(aidi) + "." + indexi
                            surati.save(cwd+"static/" + str(aidi) + "." + indexi)


                            kurs.execute("UPDATE users SET imgsrc = '"+ patyh +"' WHERE id = "+ str(aidi) +";")
                            kurs.execute("UPDATE users SET imgsize = '"+ zoma +"' WHERE id = "+ str(aidi) +";")
                            db.commit()
                            #return str(surati.filename)
                            #redirectacia
                            return redirect(url_for("index"))
                        else:
                            #dacheris mere foto airchie eror
                            return render_template("upload_pfp_eror.html",src=kf[0],er="გთხოვთ აირჩიოთ ფოტო",imgsize=zomar)
                    else:
                        #gtxovt airchiet faili
                        return render_template("upload_pfp_eror.html",src=kf[0],er="გთხოვთ აირჩიოთ ფოტო",imgsize=zomar)
                    
                
                else:

                    #shesvla
                    return render_template("upload_pfp.html",src=kf[0],imgsize=zomar)
                

            else:
                return redirect(url_for("index"))

        
    else:
        return redirect(url_for("login"))


@app.route("/gamocnobana")
def gamocnobana():
    return "rogor xar " + request.args.get("saxeli")

@app.route("/login")
def login():
    
    if request.args.get("redirect") == None:
        redirect_link = "/"
    else:
        redirect_link = "/" + request.args.get("redirect")


    if (request.cookies.get("c_user") != None and request.cookies.get("xs") != None):
        c_user = request.cookies.get("c_user")
        xs = request.cookies.get("xs")

        if auth(c_user,xs) != True:

            return render_template("login.html",redirect_link=redirect_link)
        else:
            return redirect(url_for(index))
    else:
        return render_template("login.html",redirect_link=redirect_link)







@app.route("/login_auth",methods=["GET","POST"])
def login_auth():
    mail = request.form.get("c_user")
    xs = request.form.get("xs")
    ip = request.environ.get("HTTP_X_REAL_IP",request.remote_addr)

    # db = mysql.connector.connect(
    #             host=host,
    #             user=user,
    #             passwd = passwd,
    #             database= database
    # )
    kurs = db.cursor()
    kursm = db.cursor()

    quertxt = "SELECT id,username, mail FROM users WHERE username = '"+ mail +"' OR mail = '"+ mail +"';"
    print(quertxt)
    kurs.execute(quertxt)

    kursf = kurs.fetchone()
    print(len(kursf),kursf)
    if kursf != None:

        aidi = kursf[0]
        c_user = kursf[1]
        email = kursf[2]

        wdro = time.time() - 84600
        if mail == email:
            kursm.execute("SELECT * FROM timeouts WHERE tipi = 'login_mail' AND dro > "+ str(wdro) +" AND aidi = '"+str(aidi)+"';")
        else:
            print("SELECT * FROM timeouts WHERE tipi = 'login_cuser'  AND dro > "+ str(wdro) +" AND aidi = '"+str(aidi)+"' AND ip = '"+ ip +"' ;")
            kursm.execute("SELECT * FROM timeouts WHERE tipi = 'login_cuser'  AND dro > "+ str(wdro) +" AND aidi = '"+str(aidi)+"' AND ip = '"+ ip +"' ;")

        logs = [i for i in kursm.fetchall()]
        logc = len(logs)


        if logc <=5:

            if auth(mail,xs,tipi="auth") == True:

                
                #kurs.execute("SELECT ip FROM userips WHERE aidi = " + str(aidi) + ";")

                #ipebi = [i[0] for i in kurs]

                #if ip in ipebi:
                #if True:
                

                return "success " + c_user   + " " + hashlib.sha256(xs.encode("utf-8")).hexdigest()
            else:
                if mail == email:

                    kurs.execute("INSERT INTO timeouts(aidi,dro,tipi,ip) VALUES('"+ str(aidi)  +"',"+ str(time.time()) +",'login_mail','"+ ip +"');")
                else:
                    kurs.execute("INSERT INTO timeouts(aidi,dro,tipi,ip) VALUES('"+ str(aidi)  +"',"+ str(time.time()) +",'login_cuser','"+ ip +"');")
                
                db.commit()
                return "fail"
        else:
            return "timeout"
    else:
        return "fail"

def admin_auth(c_admin,xadmin,tipi="cookie"):
    sandros = "8fa066554e99a79f3e25defaff9a2c41"
    if tipi == "cookie":
        if(hashlib.md5(hashlib.sha256(xadmin.encode("utf-8").encode("utf-8")).hexdigest().encode("utf-8")).hexdigest() ==sandros and c_admin == "sandro4424"):
            return True
    elif tipi == "login":
        pass

@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")
@app.route("/admin_panel")
def admin_panel():
    c_admin = ""
    xadmin = ""
    if admin_auth(c_admin,xadmin) == True:
        pass
        # return render_template("")
# CREATE TABLE notifications(id INT PRIMARY KEY AUTO_INCREMENT,notification_recipient_id INT, notification_img VARCHAR(200),notification_title VARCHAR(100),notification_description VARCHAR(1000),notification_link VARCHAR(200), notification_time VARCHAR(50), notification_date VARCHAR(50));
# INSERT INTO notifications(notification_recipient_id,notification_img,notification_title,notification_link,notification_time,notification_seen_bool) VALUES(16,"/static/sym.png","შეამოწმეთ ჩვენი გვერდი","http://localhost:5000/",1672593006,0);

@app.route("/admin_notification")
def admin_notification():
    
    
    if request.cookies.get("c_user") == None or request.cookies.get("xs") == None:
        
        return render_template("index.html")
    else:
        c_user = request.cookies.get("c_user")
        xs = request.cookies.get("xs")
        if auth(c_user,xs,tipi="cookie") == True:
            # db = mysql.connector.connect(
            #     host=host,
            #     user=user,
            #     passwd = passwd,
            #     database= database
            # )
            kurs = db.cursor()
            kurs.execute("SELECT saxeli,imgsrc,username,angarishi,imgsize,id,owner_bool,admin_bool,join_time FROM users WHERE username = '"+ c_user +"';")
            kursf = kurs.fetchone()
            aidi = kursf[5]
            # if kursf[6] == 1 or kursf[7] == 1:
                # return render_template("admin_notify.html")


            straidi = str(aidi)

            saxeli = kursf[0]
            imgsrc = kursf[1]
            imgsize = kursf[4]

            username = kursf[2]

            angarishi = kursf[3]
            anga = str(angarishi)

            join_time = kursf[8]

            pf_lnk = "http://"+request.headers.get('host')+"/" + username


            # notifications_box
            kurs.execute("SELECT user_one_seen FROM dms WHERE user_one = "+ str(aidi) +";")
            kurs_one = kurs.fetchall()
            kurs.execute("SELECT user_two_seen FROM dms WHERE user_two = "+ str(aidi) +";")
            kurs_two = kurs.fetchall()

            kurs_united = kurs_one + kurs_two
            message_notification_value = 0
            for i in kurs_united:
                message_notification_value+= i[0]
            if message_notification_value > 9:
                message_notification_value_shortened = "9+"
            else:
                message_notification_value_shortened = str(message_notification_value)
            message_notification_value = str(message_notification_value)
            # 

            # mailbox
            kurs.execute("SELECT * FROM notifications WHERE notification_recipient_id = "+ str(aidi) +" OR (notification_recipient_id = 0 AND notification_time > "+ str(join_time) +") ORDER BY id DESC;")
            nots = np.array(kurs.fetchall())
            not_count = 0

            for i in nots:
                if int(i[8]) == 0:
                    not_count+=1

            if not_count > 9:
                not_count_markup = "9+"
            else:
                not_count_markup = str(not_count)
                
            the_notifications_markup = ""

            # for i in nots[:10]:
            #     thenotmark = Markup(""" """)

            #     the_notifications_markup+=thenotmark
            





            csrftk = csrftok(int(straidi))
            if kursf[6] == 1 or kursf[7] == 1:
                return render_template("admin_notify.html",straidi=straidi,saxeli=saxeli,imgsrc=imgsrc,my_profile_link=pf_lnk,fuli=anga,imgsize=imgsize,
                message_notification_value=message_notification_value, message_notification_value_shortened=message_notification_value_shortened,
                not_count=str(not_count),not_count_markup=not_count_markup,csrftk=csrftk)

@app.route("/aka/<asd>",methods=["GET","POST"])
def aka(asd):
    ricxv = (10 * int(asd))
    dat = "d"  * ricxv
    return dat


# app.run(port=5000,debug=True)
# if reqapprove():
if True:
    socketio.run(app,host="0.0.0.0",debug=False)