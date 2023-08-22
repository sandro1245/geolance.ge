// var static_filter_el_label_shesadzleblobebi = document.getElementById("static_filter_el_label_shesadzleblobebi")
// var static_filter_dropdown_btn_shesadzleblobebi = document.getElementById("static_filter_dropdown_btn_shesadzleblobebi")


// var shesadzleblobebi_seleqcia_div_userinpdata = [];


var points_ls = [];

var points_ls_names = [];



var shesadzleblobebi_seleqcia_div = document.createElement("div");
shesadzleblobebi_seleqcia_div.className = "shesadzleblobebi_seleqcia_div";

var shesadzleblobebi_seleqcia_div_gauqmeba_btn = document.createElement("div");
shesadzleblobebi_seleqcia_div_gauqmeba_btn.className = "shesadzleblobebi_seleqcia_div_gauqmeba_btn gauqmeba_btn";


// var shesadzleblobebi_seleqcia_div




shesadzleblobebi_seleqcia_div_satauri = document.createElement("h2")
shesadzleblobebi_seleqcia_div_satauri.innerText = "შესაძლებლობები";
shesadzleblobebi_seleqcia_div_satauri.style.color = "blue"
shesadzleblobebi_seleqcia_div_satauri.className = "detaluri_dzebna_div_satauri"


// shesadzleblobebi_seleqcia_div_unselected_points_div_innerHTML  

var shesadzleblobebi_seleqcia_div_unselected_points_div = document.createElement("div");
var shesadzleblobebi_seleqcia_div_selected_points_div = document.createElement("div");





shesadzleblobebi_seleqcia_div.append(shesadzleblobebi_seleqcia_div_gauqmeba_btn)
shesadzleblobebi_seleqcia_div.append(shesadzleblobebi_seleqcia_div_satauri)

// 
    shesadzleblobebi_seleqcia_div_selected_points_div.id = "selected_points";
    shesadzleblobebi_seleqcia_div_selected_points_div.className = "selected_points";
    shesadzleblobebi_seleqcia_div.append(shesadzleblobebi_seleqcia_div_unselected_points_div)
    shesadzleblobebi_seleqcia_div.append(shesadzleblobebi_seleqcia_div_selected_points_div)


    let reject_label = document.createElement("div");
    reject_label.id = "reject_label";
    shesadzleblobebi_seleqcia_div.append(reject_label)
if(subsfero_selected){
    shesadzleblobebi_seleqcia_div_unselected_points_div.innerHTML = shesadzleblobebi_seleqcia_div_unselected_points_div_innerHTML;
    
    shesadzleblobebi_seleqcia_div_unselected_points_div.style.display = "grid";
    shesadzleblobebi_seleqcia_div_selected_points_div.style.display = "grid";

    reject_label.style.display = "none";

}
else{
    reject_label.innerHTML = shesadzleblobebi_seleqcia_div_unselected_points_div_innerHTML;
    
    shesadzleblobebi_seleqcia_div_unselected_points_div.style.display = "none";
    shesadzleblobebi_seleqcia_div_selected_points_div.style.display = "none";


    reject_label.style.display = "inline";
}

shesadzleblobebi_seleqcia_div_unselected_points_div.id = "unselected_points";
shesadzleblobebi_seleqcia_div_unselected_points_div.className = "unselected_points";














var shesadzleblobebi_seleqcia_div_anim_int;


var shesadzleblobebi_seleqcia_div_anim_y = -80;

var shesadzleblobebi_seleqcia_div_anim_velo = 1.87

var shesadzleblobebi_seleqcia_div_anim_accel = -0.00145;

var shesadzleblobebi_seleqcia_div_bgopac = "0.5"

var shesadzleblobebi_seleqcia_div_gauqmebulia = true;


document.body.append(shesadzleblobebi_seleqcia_div)


static_filter_el_label_shesadzleblobebi.onclick = shesadzleblobebi_seleqcia_div_anim_intsawyisi;
static_filter_dropdown_btn_shesadzleblobebi.onclick = shesadzleblobebi_seleqcia_div_anim_intsawyisi;



function shesadzleblobebi_seleqcia_div_anim_intsawyisi(){
    shesadzleblobebi_seleqcia_div_anim_int = setInterval(shesadzleblobebi_seleqcia_div_anim,1)


}


function shesadzleblobebi_seleqcia_div_anim(){
    // shesadzleblobebi_seleqcia_div
    // rgb(239, 232, 232);

    console.log(shesadzleblobebi_seleqcia_div.style.top)

    document.getElementById("navbar").style.opacity = shesadzleblobebi_seleqcia_div_bgopac;
    document.getElementById("nav_params_bar").style.opacity = "0";
    document.getElementById("full_search_input").style.opacity = shesadzleblobebi_seleqcia_div_bgopac;
    document.getElementById("search_big_button").style.opacity = shesadzleblobebi_seleqcia_div_bgopac;
    document.getElementById("detaluri_dzebna_label").style.opacity = shesadzleblobebi_seleqcia_div_bgopac;
    document.getElementById("shedegi_label").style.opacity = shesadzleblobebi_seleqcia_div_bgopac;
    // document.getElementById("stats_adjust_div").style.opacity = shesadzleblobebi_seleqcia_div_bgopac;
    document.getElementById("static_filter").style.opacity = shesadzleblobebi_seleqcia_div_bgopac;
    document.getElementById("servisebi").style.opacity = shesadzleblobebi_seleqcia_div_bgopac;
    

    if(shesadzleblobebi_seleqcia_div_anim_y < 50){
        shesadzleblobebi_seleqcia_div_anim_accel+=0.00037541982289555103;
        shesadzleblobebi_seleqcia_div_anim_velo+=-shesadzleblobebi_seleqcia_div_anim_accel;
        shesadzleblobebi_seleqcia_div_anim_y+=+shesadzleblobebi_seleqcia_div_anim_velo;
        shesadzleblobebi_seleqcia_div.style.top = shesadzleblobebi_seleqcia_div_anim_y + "%"; 
    }
    else{
        shesadzleblobebi_seleqcia_div_gauqmeba_btn.addEventListener("click",shesadzleblobebi_seleqcia_div_gauqmeba)
        document.body.addEventListener("click",shesadzleblobebi_seleqcia_div_gauqmeba)
        clearInterval(shesadzleblobebi_seleqcia_div_anim_int)
    }
    
}


function shesadzleblobebi_seleqcia_div_gauqmeba(e){
    if(shesadzleblobebi_seleqcia_div_gauqmebulia == true){
        // if( (e.target != shesadzleblobebi_seleqcia_div ) &&((e.target.parentNode != shesadzleblobebi_seleqcia_div && e.target.parentNode.parentNode!= shesadzleblobebi_seleqcia_div  ) || (e.target ==shesadzleblobebi_seleqcia_div_gauqmeba_btn || e.target == detailed_modzebna_btn) ) ){
        let shesadzleblobebi_seleqcia_div_parlist = [];
        let elemp = e.target.parentNode
        while(elemp){
            shesadzleblobebi_seleqcia_div_parlist.push(elemp)
            elemp = elemp.parentNode;
            
        }
        console.log(shesadzleblobebi_seleqcia_div_parlist);
        if((shesadzleblobebi_seleqcia_div_parlist.includes(shesadzleblobebi_seleqcia_div) || e.target == shesadzleblobebi_seleqcia_div) == false || e.target == shesadzleblobebi_seleqcia_div_gauqmeba_btn){
            shesadzleblobebi_seleqcia_div_bgopac = "1";
            document.getElementById("navbar").style.opacity = shesadzleblobebi_seleqcia_div_bgopac;
            document.getElementById("nav_params_bar").style.opacity = "1";
            document.getElementById("full_search_input").style.opacity = shesadzleblobebi_seleqcia_div_bgopac;
            document.getElementById("search_big_button").style.opacity = shesadzleblobebi_seleqcia_div_bgopac;
            document.getElementById("detaluri_dzebna_label").style.opacity = shesadzleblobebi_seleqcia_div_bgopac;
            document.getElementById("shedegi_label").style.opacity = shesadzleblobebi_seleqcia_div_bgopac;
            // document.getElementById("stats_adjust_div").style.opacity = shesadzleblobebi_seleqcia_div_bgopac;
            document.getElementById("servisebi").style.opacity = shesadzleblobebi_seleqcia_div_bgopac;
            document.getElementById("static_filter").style.opacity = shesadzleblobebi_seleqcia_div_bgopac;

            shesadzleblobebi_seleqcia_div_bgopac = "0.5"
            shesadzleblobebi_seleqcia_div_anim_y = -80;
            shesadzleblobebi_seleqcia_div_anim_velo = 1.87
            shesadzleblobebi_seleqcia_div_anim_accel = -0.00145;

            shesadzleblobebi_seleqcia_div.style.top = "-80%";
            document.body.removeEventListener("click",shesadzleblobebi_seleqcia_div_gauqmeba)
            shesadzleblobebi_seleqcia_div_gauqmeba_btn.removeEventListener("click",shesadzleblobebi_seleqcia_div_gauqmeba)

            shesadzleblobebi_seleqcia_div_gauqmebulia = true;
        }
        

    }

    
}





var unselected_points = document.getElementById("unselected_points");
var selected_points = document.getElementById("selected_points");

var add_btns = document.getElementsByClassName("select_point_button_img");


function add_btns_func(){
    for(let i of add_btns){
        let mtavari = i.parentNode.parentNode;
        let saxeli = i.id.split("img_")[1];
        // let po_time = document.getElementById("po_time_" + saxeli);
        // let po_fasi = document.getElementById("po_fasi_" + saxeli);
        let po_points = document.getElementById("po_points_" + saxeli);

        po_points.setAttribute("disabled","");
        function ireturn(){
            
            // if(po_fasi.value != "0$"){
            //     po_fasi.value = po_fasi.value;
            // }
            // else{
            //     po_fasi.value = "";
            // }
            // if(po_time.value == "0"){
            //     po_time.value = "";
            // }
            
            
            // po_time.setAttribute("disabled",false);
            // po_fasi.setAttribute("disabled",false);
            // po_time.disabled = false;
            // po_fasi.disabled = false;

            selected_points.removeChild(mtavari);

            
            
            unselected_points.append(mtavari);
            // unselected_points.prepend(mtavari);
            
            
            
            // points_ls.splice(points_ls.indexOf({"name" :saxeli,"points" : po_points.value,"dro" :po_time.value,"fasi" : po_fasi.value.split("$")[0] }),1)
            
            // points_ls.splice(points_ls.indexOf({"name" :saxeli,"points" : po_points.value}),1)
            points_ls.splice(points_ls_names.indexOf(saxeli),1)
            points_ls_names.splice(points_ls_names.indexOf(saxeli),1)


            i.style.backgroundImage = "url('static/plus.jpg')";
            i.removeEventListener("click",ireturn);
            i.addEventListener("click",iclick);



            if(points_ls.length == 0){
                document.getElementById("selected_points").style.opacity = "0.5";
            }
            
            


        }
        function iclick(){
            document.getElementById("selected_points").style.opacity = "1";
                            
            // if(po_fasi.value != ""){
            //     po_fasi.value = po_fasi.value + "$";
            // }
            // else{
            //     po_fasi.value = "0$";
            // }
            // if(po_time.value == ""){
            //     po_time.value = "0";
            // }
            
            // po_time.setAttribute("disabled","");
            // po_fasi.setAttribute("disabled","");

            

            
            
            unselected_points.removeChild(mtavari);
            
            i.style.backgroundImage = "url('static/minus.jpg')";
            selected_points.append(mtavari);
            // selected_points.prepend(mtavari);

            console.log("clicked : " + saxeli)

            // points_ls.push({"name" :saxeli,"points" : po_points.value,"dro" :po_time.value,"fasi" : po_fasi.value.split("$")[0] }); 
            points_ls.push({"name" :saxeli,"points" : po_points.value});
            points_ls_names.push(saxeli) 


            i.removeEventListener("click",iclick);
            
            i.addEventListener("click",ireturn)
        
        }
        i.addEventListener("click",iclick);
    }
}

add_btns_func()



// What's point of  going to gym if you're not strongest or biggest guy at least in your country if not in whole world ( i don't want to discourage anyone from going to gym, i just want to hear other people's opinions), i'm 16 i've been going to gym since 14 years old, i live in very competitive and masculine country where every boy is judged by how strong he is, i loved wrestling and i got also in lot of fights in past so i started excercising at 13 till after bit of results and my calculation, i found out that i had pretty good genetics, idk why but small percentage of my self considered becoming MR.olympia or WSM(World's Strongest Man), and i got some compliments about my physique at my age too :)), but as time went i hit plateu and i started going to gym at 14 i still looked good for my age but after 2 years passed and i didn't gain much more muscle, my physique looks now very avarage for 16 years old, and my bench/deadlift PRs(100kg and 115kg) are half of what boys my age(other 16 year olds on TikTok) do, and i feel super inferior, my classmates made fun of me for wanting to be big and strong so hard that i go to gym 4 times a week and have specific routine and i don't get point why should i do that if someone with monster genetics can lift double i can at my age, and i've stopped going to gym and i decided i'll just won't eat junk food and do some pushups 2 times a week


// It feels super depressed


for(let i of points_ls_req){
    // document.getElementById(`select_point_button_img_კუნთოვანი მასის გაზრდა`)
    document.getElementById(`select_point_button_img_${i["name"]}`).click();
}