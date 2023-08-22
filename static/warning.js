class GeoWarning{
    constructor(question,ara,ki,maini=[],state="auto"){
        this.maini = maini;
        for(let i of this.maini){
            
            document.getElementById(i).style.opacity = "0.2";
        }
        
        document.getElementById("navbar").style.opacity = "0.2";
        document.getElementById("nav_params_bar").style.opacity = "0";

        // document.getElementById("navbar").removeChild(document.getElementById("nav_params_bar"));

        this.rec_washla_gafrtxileba_div = document.createElement("div");
        document.body.append(this.rec_washla_gafrtxileba_div);
        this.rec_washla_gafrtxileba_div.className = "rec_washla_gafrtxileba_div";

        this.shekitxva = document.createElement("p");
        this.shekitxva.innerHTML = question;
        this.shekitxva.className = "rec_washla_gafrtxileba_shekitxva";

        this.rec_washla_gafrtxileba_div.append(this.shekitxva);

        this.rec_washla_gafrtxileba_buttonsdiv = document.createElement("div");
        this.rec_washla_gafrtxileba_buttonsdiv.className = "rec_washla_gafrtxileba_buttonsdiv";

        this.rec_washla_gafrtxileba_div.append(this.rec_washla_gafrtxileba_buttonsdiv);

        this.rec_washla_kibutton = document.createElement("div");
        this.rec_washla_arabutton = document.createElement("div");

        this.rec_washla_kibutton.innerHTML = "კი";
        this.rec_washla_arabutton.innerHTML = "არა";

        this.rec_washla_kibutton.className = "rec_washla_kibutton rec_washla_button";
        this.rec_washla_arabutton.className = "rec_washla_arabutton rec_washla_button";


        this.rec_washla_gafrtxileba_buttonsdiv.append(this.rec_washla_arabutton);
        this.rec_washla_gafrtxileba_buttonsdiv.append(this.rec_washla_kibutton);

        
        if(state == "auto"){
            this.rec_washla_arabutton.addEventListener("click",ara);
            this.rec_washla_arabutton.addEventListener("click",() => {
                this.window_gauqmeba()
            });

            this.rec_washla_kibutton.addEventListener("click",ki);
            this.rec_washla_kibutton.addEventListener("click",() => {
                this.window_gauqmeba()
            });

        }
        
        
        
        


    }
    window_gauqmeba(){
        // console.log(this.maini)
        for(let i of this.maini){
            document.getElementById(i).style.opacity = "1";
        }
        
        document.getElementById("navbar").style.opacity = "1";
        document.getElementById("nav_params_bar").style.opacity = "1";
        document.body.removeChild(this.rec_washla_gafrtxileba_div);
        
    }

}
