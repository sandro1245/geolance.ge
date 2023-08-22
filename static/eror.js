
var ranki = 20;

function erori(txt,posx=null,posy=null){

    var erorbox = document.createElement("div");
    var paragr = document.createElement("p");

    var erimg = document.createElement("img");

    erorbox.style.backgroundColor = "#DF4040";
    erorbox.style.position = "fixed";
    erorbox.style.zIndex = "2022"
        

        
    if(posy == null){
        erorbox.style.top = "20%";
    }
    else{

        erorbox.style.top = posy + "%";
    }
    
    //erorbox.style.left = "2%";
    if(posx == null){
        erorbox.style.left = "2%";
    }
    else{
        erorbox.style.left = posx + "%";
    }
    
    erorbox.style.borderRadius = "5px";
    erorbox.style.textAlign = "center";
    

    paragr.style.paddingTop = "40px";

    paragr.style.fontSize = "15px";
    

    erorbox.style.width = "15%";
    erorbox.style.height = "24%";


    erimg.src = "/static/erorsym.png";
    erimg.style.position = "absolute";
    erimg.style.width = "16%";
    erimg.style.borderRadius = "50% 50%";
    erimg.style.top = "5%";
    erimg.style.left = "42%";
    var c = 0.15;
    var x = -8;
    var z = -0.00025;

    var qrb = 1;

    //alert("yleror");erorsym.png
    function eranim(){

        
        x+=c;
    
        c+=z;
        
    
        erorbox.style.left = x + "%";
    
        if(c <=0){
            clearInterval(int);

            function gaqroba(){
                erorbox.style.opacity = qrb;
                qrb+=-0.01;
                if(qrb <= 0){
                    clearInterval(gaqrvr);
                    qrb = 1;
                    document.body.removeChild(erorbox)
                    
                }
            }

            var gaqrvr = setInterval(gaqroba,1);
        }
    
    
    
    
    }   

    paragr.innerHTML = txt;

    //erimg.style.posiion

    erorbox.appendChild(paragr);

    erorbox.appendChild(erimg);


    document.body.appendChild(erorbox);





    //anim

    erorbox.style.left = "-8%"

    var int = setInterval(eranim,1);
    

    
    c = 0.08;
    x = -8;
    z = -0.00025;
    qrb = 1;
    erorbox.style.opacity = qrb;



    
    
}