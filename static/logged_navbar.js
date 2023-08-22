if(status_update_socket == undefined){

    function logout(){
        document.cookie = "c_user=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        document.cookie = "xs=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        window.location.href = "/";
    }
    var pfp = document.getElementById("pfp");

    pfp.style.height = pfp.width + "px";

    var notifications_btn = document.getElementById("notifications_btn")
    var arr = document.getElementById("arr");

    var nav_params_bar = document.getElementById("nav_params_bar");
    //arr.src = "static/arr_open.png";
    //arr.src = "static/arr.png";
    var logout_btn = document.getElementById("logout_li");
    var statu = "up";

        function arclick(){

            
            if(statu == undefined || statu == "up"){
                arr.src = "/static/arr_open.png";
            var x = -14;
        var y = 0.0005;
        
            function anim(){
            nav_params_bar.style.top = x + "%";
            x+=y;
            y+=0.04;
            //console.log(x);
            if(x>=14){
                clearInterval(pirte);
            }
        }
        var pirte = setInterval(anim,0.1);
        statu = "down";
    }
    else{
        var x = 14;
        var y = -0.0005;
        arr.src = "/static/arr.png";
            function anim(){
            nav_params_bar.style.top = x + "%";
            x+=y;
            y+=-0.04;
            //console.log(x);
            if(x<=-12){
                clearInterval(pirte);
            }
        }
        var pirte = setInterval(anim,0.1);
        statu = "up";

    }
        
        //nav_params_bar.style.css = "300px";
        //nav_params_bar
    }

    arr.onclick = arclick;
    logout_btn.onclick = logout;


    var search_input = document.getElementById("search_input");
    var search_btn = document.getElementById("search_btn");

    search_btn.onclick = function(){
        window.location.href = "/query_services?srch="+search_input.value;
    }
    search_input.onkeyup = function(key){
        if(key.key == "Enter"){
            window.location.href = "/query_services?srch="+search_input.value;
        }
    }

    var kukis = document.cookie;
    var kuki = {}

    for(let i of kukis.split(";")){
        kuki[i.split("=")[0].trim()]  = i.split("=")[1].trim();

    }
    var inbox_audio = new Audio("/static/geolance_not.mp3");



    var status_update_socket =  io.connect("ws://localhost:5000") //io.connect("ws://localhost:5000");

    status_update_socket.on("connect",function(){

        status_update_socket.emit("activate_status",data={"user_id" : straidi,"c_user" : kuki.c_user,"xs" : kuki["xs"], "action" : "activate"})
        status_update_socket.emit("join_dmchat_room_cousin",data={})
    })

    var notification_queryied_ids = []
    var sock_recieved_ids = [];
    status_update_socket.on("message",function(dat){
        data = JSON.parse(dat)
        
        if(data["type"] == "dm_msg"){
            if(window.location.href.split("/")[3] != "messenger"){
                let inbox_btn_not_p = document.getElementsByClassName("inbox_btn_not_p")[0]
                let curnum = parseInt(inbox_btn_not_p.getAttribute("value")) //parseInt(inbox_btn_not_p.innerHTML.split("+")[0])
                let nextnum = curnum +1
                inbox_btn_not_p.setAttribute("value",curnum+"")
                if(nextnum>9){
                    inbox_btn_not_p.innerHTML = "9+"
                }
                else{
                    inbox_btn_not_p.innerHTML=nextnum

                }
                inbox_btn_not_p.setAttribute("value",nextnum+"")
                
            }
        }
        else if(data["type"] == "start_chat"){
            if(window.location.href.split("/")[3] != "messenger"){
                status_update_socket.emit("join_dmchat_room",data={"dmchat_idebi" : JSON.stringify([data["chat_aidi"]]),"c_user" : kuki.c_user,"xs" : kuki["xs"]})
            }
            
        }
        else if(data["type"] == "notification"){
            console.log("nodification")
            let dat = data["main"];

            // notifications_div.innerHTML = not_dive(dat)+ notifications_div.innerHTML
            // if(notification_queryied_ids.includes(dat[0]) == false){
            notifications_div.prepend(not_dive(dat))
            // }
            let inbox_btn_not_p = document.getElementsByClassName("notifications_btn_not_p")[0]

            inbox_btn_not_p.setAttribute("value",parseInt(inbox_btn_not_p.getAttribute("value"))+1)
            if(parseInt(inbox_btn_not_p.getAttribute("value")) > 9){
                inbox_btn_not_p.innerHTML = "9+";
            }
            else{
                inbox_btn_not_p.innerHTML = inbox_btn_not_p.getAttribute("value");
            }

            sock_recieved_ids.push(dat[0]+"")
            
        }

        if(data["type"] == "notification"){
            
            inbox_audio.play()

        }
        else if(data["type"] == "dm_msg" ){
            if((straidi+"")  != (data["sender_id"]+"")){
                inbox_audio.play()
            }
        }
    })

    var notifications_div = document.createElement("div");
    notifications_div.id = "notifications_div";
    if(window.location.href.split("/")[3] == "messenger"){
        notifications_div.style.left =  "61%"
    }

    notifications_btn.status = "closed";
    document.getElementById("navbar").append(notifications_div);

    var loading_html = document.createElement("div");
    loading_html.className = "burtula_outer_nv";
    loading_html.innerHTML = `<div class="lds-circle_nv"><div class = "burtula_nv"></div></div>`;
    // let loading_html = `
    // <div class = "burtula_outer_nv">
    //                                     <div class="lds-circle_nv"><div class = "burtula_nv"></div></div>
    //                                 </div>`;
    var indexi = 0;
    notifications_div.innerHTML = loading_html.outerHTML;


    function not_dive(i){


            
            // mark=`
            // <div onclick = "window.location.href = '${i[5]}';" id = 'not_div_${i[0]}' class = "not_div">
            //             <div style = "background-image:url('${i[2]}')" class = "not_img"></div>
            //             <div class = "not_cont_outer">
            //                 <div class ="not_title">${i[3]}</div>
            //                 <div class = "not_time"></div>
            //             </div>
            //         </div>
            // `;
            console.log("dupc")
            console.log(i)
            mark = document.createElement("div");
            mark.onclick = function(){
                window.location.href = `${i[5]}`;
                // $.ajax({
                //     data : {
                //         "notification_id" : i[0]
                //     },
                //     url : "/notificatino_dasinva",
                //     type :"POST",
                //     dataType : "text",
                //     success : function(data){
                //         window.location.href = `${i[5]}`;
                //     }
                // })
                
            }
            mark.id = `not_div_${i[0]}`;
            mark.className = "not_div";
            mark.innerHTML = `
            <div style = "background-image:url('${i[2]}')" class = "not_img"></div>
                        <div class = "not_cont_outer">
                            <div class ="not_title">${i[3]}</div>
                            <div class = "not_time"></div>
                            
                        </div>
                        <div class = "not_subimg" style = "background-image:url('${i[9]}')"'></div>
            `;
            
        

        return mark; 
    }
    function daa_not_dive(dat){
        // let data = JSON.parse(dat)
        let data = dat;
        let mark = "";
        // let mark = document.getElementById("notifica")
        
        


        for(let i of data){
            
            // mark+=`
            // <div onclick = "window.location.href = '${i[5]}';" id = 'not_div_${i[0]}' class = "not_div">
            //             <div style = "background-image:url('${i[2]}')" class = "not_img"></div>
            //             <div class = "not_cont_outer">
            //                 <div class ="not_title">${i[3]}</div>
            //                 <div class = "not_time"></div>
            //             </div>
            //         </div>
            // `;
            // mark+=not_dive(i)
            notdiv_ls = []
            for(let a of document.getElementsByClassName("not_div")){
                notdiv_ls.push(a);
                
            }
            
            // if(document.getElementsByClassName("not_div").length > 0){
            //     if(document.getElementsByClassName("not_div").includes(not_dive(i)) == false){
            //         notifications_div.append(not_dive(i))
            //     }
            // }
            // else{notifications_div.append(not_dive(i))

            // }
            if(notdiv_ls.length > 0){
                if(notdiv_ls.includes(not_dive(i)) == false){
                    if(sock_recieved_ids.includes(i[0]+"") == false){
                        notifications_div.append(not_dive(i))
                    }
                    
                }
            }
            else{
                if(sock_recieved_ids.includes(i[0]+"") == false){
                notifications_div.append(not_dive(i)) 
                }
                

            }
            
        }

        return mark;

    }
    var observer_nav = new IntersectionObserver(function(entries) {
        // isIntersecting is true when element and viewport are overlapping
        // isIntersecting is false when element and viewport don't overlap
        if(entries[0].isIntersecting === true){
            //console.log('Element has just become visible in screen');
            // console.log("vnaxe mesiji : " + entries[0].target.id)
            indexi+=10
            // console.log(`vamowmebt ${indexi}-dan ${indexi+10}-mde`)
            $.ajax({
                data : {
                    "index" : indexi
                },
                url : "/notifications_query",
                type : "POST",
                dataType : "text",
                success : function(dat){
                    for(let i of document.getElementsByClassName("burtula_outer_nv")){
                        notifications_div.removeChild(i);
                    }
                    let data = JSON.parse(dat)
                    // notifications_div.innerHTML= notifications_div.innerHTML.replace(loading_html,"")+(daa_not_dive(data[0])+loading_html);
                    console.log("tveni iears" + data[2])
                    if(data[2] == "false"){
                        daa_not_dive(data[0])
                        document.getElementById("notifications_div").append(loading_html)
                        observer_nav.unobserve(entries[0].target)
                        if(parseInt(document.getElementsByClassName("not_div")[document.getElementsByClassName("not_div").length-1].id.split("_")[2]) != parseInt(data[1])){
                            observer_nav.observe(document.getElementsByClassName("not_div")[document.getElementsByClassName("not_div").length-1])
                        }
                        else{
                            for(let i of document.getElementsByClassName("burtula_outer_nv")){
                                notifications_div.removeChild(i);
                            }
                        }
                    }
                }
                
            })
            

        }
        else{
            //gauchinarda
            
        }
            
    }, { threshold: [0] });

    // $.ajax({
    //     data : {
    //         "index" : indexi+""
    //     },
    //     url : "/notifications_query",
    //     type : "POST",
    //     dataType : "text",
    //     success : function(dat){
    //         let data = JSON.parse(dat)
    //         // notifications_div.innerHTML= notifications_div.innerHTML.replace(loading_html,"")+(daa_not_dive(data[0])+loading_html);
    //         daa_not_dive(data[0])
    //         document.getElementById("notifications_div").append(loading_html)
    //         observer_nav.observe(document.getElementsByClassName("not_div")[document.getElementsByClassName("not_div").length-1])
    //     }
        
    // })


    // notifications_btn.onclick = notclick;
    document.body.addEventListener("click",notclick_onlyclose)
    notifications_btn.addEventListener("click",notclick);




    function notclick(){
        if(notifications_btn.status == "closed"){
            notifications_div.style.display = "block";
            notifications_btn.status = "open";
            let inbox_btn_not_p = document.getElementsByClassName("notifications_btn_not_p")[0]
            inbox_btn_not_p.setAttribute("value","0")
            inbox_btn_not_p.innerHTML = "0";
            $.ajax({
                data : {
                    "index" : indexi+""
                },
                url : "/notifications_query",
                type : "POST",
                dataType : "text",
                success : function(dat){
                    let data = JSON.parse(dat)
                    // notifications_div.innerHTML= notifications_div.innerHTML.replace(loading_html,"")+(daa_not_dive(data[0])+loading_html);
                    if(data[2] == "false"){
                        daa_not_dive(data[0])
                        document.getElementById("notifications_div").append(loading_html)
                        observer_nav.observe(document.getElementsByClassName("not_div")[document.getElementsByClassName("not_div").length-1])
                        
                    } 
                    for(let i of document.getElementsByClassName("burtula_outer_nv")){
                        notifications_div.removeChild(i);
                    }
                    
                }
                
            })
            
        }
        else if(notifications_btn.status == "open"){
            notifications_div.style.display = "none";
            notifications_btn.status = "closed";
        }
        
            
    }
    function notclick_onlyclose(e){
        if(e.target != notifications_btn){
            if(notifications_btn.status == "open"){
                notifications_div.style.display = "none";
                notifications_btn.status = "closed";
            }
        }
    }
}