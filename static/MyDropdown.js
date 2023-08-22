
           // class MyDropdown{
            function MyDropdown(title="აირჩიეთ",elementebi=[],master=document.body,width=null,height=null){
                // constructor(){
                    this.title = title;
                    this.elementebi = elementebi;
                    this.master = master;
                    
                    this.avalability_status = "enabled";
                    
                   // var maini = document.createElement("span");

                   this.pos_status = "removed";

                    this.maini = document.createElement("div");
                    // this.maini.style.left = pos[0] + "%";
                    // this.maini.style.top = pos[1] + "%";

                    this.chamosashleli = document.createElement("div");
                    this.chamosashleli.className  = "chamoshashleli";

                    this.width = width;
                    this.height = height;
                    if(width != null){
                        this.maini.style.width = this.width + "%";
                        this.chamosashleli.style.width = this.width*1.0869565217391304347826086956522+ "%";
                    }
                    if(this.elementebi.length <= 5){
                        this.simsim = this.elementebi.length*50;

                    }
                    else{
                        this.simsim = 205;
                    }
                    

                    // this.chamosashleli.style.left = pos[0] + "%";
                    // this.chamosashleli.style.top = (pos[1]-5) + "%";


                    this.maini.className = "dropdown_main";

                    this.maini.innerHTML = this.title;
                    this.value = "none";

                    
                    // this.master.append(this.maini);
                    
                    this.status = "closed";



                    this.dilementebi = [];
                    
                    for(let i of this.elementebi){
                            
                            let elementi = document.createElement("div");
                            if(this.width != null){
                                elementi.style.width = "100%";
                            }
                            this.dilementebi.push(elementi);
                            elementi.innerHTML = i;
                            elementi.className = "drop_opt";
                            elementi.id = i;
                            this.chamosashleli.append(elementi);
                            

                            elementi.addEventListener("click", () => {
                               
                                
                                
                                this.maini.innerHTML = i;
                                this.value = i;
                                //this.status = "closed";
                                
                                var sim = 251;
                                var sim_y = -1;
                                var sim_ya = -0.045;
                                daxurva_f = () => {
                                    sim+=sim_y;
                                    sim_y+=sim_ya;
                                    sim_ya+=-0.002;
                                    
                                    
                                    this.chamosashleli.style.height = sim + "px";
                                    
                                    if(sim < 49){
                                        clearInterval(daxuravs);
                                        this.status = "closed";
                                        this.master.removeChild(this.chamosashleli);
                                    }
                                }
                                var daxuravs = setInterval(daxurva_f,1);

                                
                                
                               
                                var aian = 0;
                                for(let aiaa in this.dilementebi){
                                    
                                        let aia = this.dilementebi[aian];
                                        aia.style.color = "black";
                                        aia.onmouseenter = () => {

                                            aia.style.color = "blue";
                                        }
                                       
                                        
                                            aia.onmouseleave = () =>{
                                                if(this.maini.innerHTML != aia.innerHTML){
                                                    aia.style.color = "black";
                                                }
                                                else{
                                                    aia.style.color = "#088270";
                                                }
                                            }
                                        
                                       
                                        aian+=1;
                                }
                                
                                
                                
                            }
                            )
                            elementi.addEventListener("click",function(){
                                this.style.color = "#088270";
                                
                        })
                            
                            
                        }
                    
                    this.setValues = (elegentebi) => {
                        
                        for(let i of this.dilementebi){
                            
                            this.chamosashleli.removeChild(i);
                        }
                        if(this.elementebi.length <= 5){
                            this.simsim = this.elementebi.length*50;
    
                        }
                        else{
                            this.simsim = 205;
                        }
                        
                        
                        this.elementebi = elegentebi;
                        this.dilementebi = [];
                        
                    
                        for(let i of this.elementebi){
                                
                                let elementi = document.createElement("div");
                                if(this.width != null){
                                    elementi.style.width ="100%";
                                }
                                this.dilementebi.push(elementi);
                                elementi.innerHTML = i;
                                elementi.className = "drop_opt";
                                elementi.id = i;
                                this.chamosashleli.append(elementi);
                                
                                
                                elementi.addEventListener("click", () => {
                                
                                    
                                    
                                    this.maini.innerHTML = i;
                                    this.value = i;
                                    //this.status = "closed";
                                    
                                    var sim = 251;
                                    var sim_y = -1;
                                    var sim_ya = -0.045;
                                    daxurva_f = () => {
                                        sim+=sim_y;
                                        sim_y+=sim_ya;
                                        sim_ya+=-0.002;
                                        
                                        
                                        this.chamosashleli.style.height = sim + "px";
                                        
                                        if(sim < 49){
                                            clearInterval(daxuravs);
                                            this.status = "closed";
                                            this.master.removeChild(this.chamosashleli);
                                        }
                                    }
                                    var daxuravs = setInterval(daxurva_f,1);

                                    
                                    
                                    
                                    var aian = 0;  
                                    for(let aiaa in this.dilementebi){
                                            let aia = this.dilementebi[aian];
                                            aia.style.color = "black";
                                            aia.onmouseenter = () => {

                                                aia.style.color = "blue";
                                            }
                                        
                                            
                                                aia.onmouseleave = () =>{
                                                    if(this.maini.innerHTML != aia.innerHTML){
                                                        aia.style.color = "black";
                                                    }
                                                    else{
                                                        aia.style.color = "#088270";
                                                    }
                                                }
                                            
                                        
                                            aian+=1;
                                    }
                                    
                                    
                                    
                                }
                                )
                                elementi.addEventListener("click",function(){
                                    this.style.color = "#088270";
                                    
                            })
                                
                                
                            }

                    }
                        
                    this.kliki = () => {
                        if(this.avalability_status == "enabled"){
                            if(this.status == "closed"){
                                
                                this.master.append(this.chamosashleli);


                                //anim
                                this.status = "open";
                                var sim = 50;
                                var sim_y = 1;
                                var sim_ya = 0.045;
                                gaxsna_f = () => {
                                    sim+=sim_y;
                                    sim_y+=sim_ya;
                                    sim_ya+=0.002;
                                    
                                    this.chamosashleli.style.height = sim + "px";
                                    
                                    if(sim > this.simsim){
                                        clearInterval(gaxsnis);
                                    }
                                }
                                var gaxsnis = setInterval(gaxsna_f,1);
                                //</> anim
                                
                            }

                            else if(this.status == "open"){
                                this.status = "closed";
                                //this.maini.removeChild(this.chamosashleli);
                                // this.status = "closed";
                            }
                    }

                    }
                    

                    this.maini.addEventListener("click",this.kliki);


                    this.place = (posx="rel",posy="rel",type="front",position_indx="%",position_indy="%",margz=5) => {
                        if(posx != "rel" && posy != "rel"){

                            this.maini.style.left = posx + position_indx;
                            this.maini.style.top = posy + position_indy;
        
             
        
                            this.chamosashleli.style.left = posx + position_indx;
                            this.chamosashleli.style.top = (posy-margz) + position_indy;
                        }
                        else{
                            
                        }

         

                        if(type == "front"){
                            this.master.append(this.maini);

                        }
                        else if(type == "back"){
                            this.master.prepend(this.maini);
                        }
                        
                        if(this.status == "open"){
                            // this.master.append(this.chamosashleli);
                            if(type == "front"){
                                this.master.append(this.chamosashleli);
    
                            }
                            else if(type == "back"){
                                this.master.prepend(this.chamosashleli);
                            }
                        }
                        this.pos_status = "placed";

                    }

                    this.place_forget = () => {
                        this.master.removeChild(this.maini);

                        if(this.status == "open"){
                            this.master.removeChild(this.chamosashleli);
                        }
                        this.pos_status = "removed";
                    }

                    this.setValue = (saxeli) => {
                        if(this.elementebi.includes(saxeli)){
                            this.maini.innerHTML = saxeli; 
                            this.value = saxeli;

                            var elims = this.chamosashleli.getElementsByClassName("drop_opt");

                            for(let i of elims){

                                if(i.innerHTML == saxeli){
                                    i.style.color = "#088270";
                                }
                            }
                            //elim.style.color = "#088270";

                        }
                        
                    }


                    this.enable = () =>{
                        if(this.avalability_status == "disabled"){

                            this.maini.className = "dropdown_main";



                            this.avalability_status = "enabled";
                        }

                    }
                    this.disable = () =>{
                        if(this.avalability_status == "enabled"){

                            this.maini.className = "dropdown_main_disabled";






                            this.avalability_status = "disabled";
                        }
                    }

                    
                }
            // }
                
                
            
            //}
            
            
        