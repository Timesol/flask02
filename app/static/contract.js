function edit_row(no){


 

 document.getElementById("edit_button"+no);
 document.getElementById("save_button"+no);

 document.getElementById("edit_button"+no).style["display"]="none";
 document.getElementById("save_button"+no).style["display"]="inline-block";
	
 var residence=document.getElementById("residence_contract");
 var project=document.getElementById("project_contract");
 var projectmanager=document.getElementById("projectmanager_contract");
 var hardware=document.getElementById("hardware_contract");
 var technology=document.getElementById("technology_contract");
 var contract=document.getElementById("contract_contract");
 
	
 var residence_data=residence.innerHTML;
 var project_data=project.innerHTML;
 var projectmanager_data=projectmanager.innerHTML;
 var hardware_data=hardware.innerHTML;
 var technology_data=technology.innerHTML;
 var contract_data=contract.innerHTML;

	
 residence.innerHTML="<input type='text' id='residence_text"+"' value='"+residence_data+"'>";
 project.innerHTML="<input type='text' id='project_text"+"' value='"+project_data+"'>";
 projectmanager.innerHTML="<input type='text' id='projectmanager_text"+"' value='"+projectmanager_data+"'>";
 hardware.innerHTML="<input type='text' id='hardware_text"+"' value='"+hardware_data+"'>";
 technology.innerHTML="<input type='text' id='technology_text"+"' value='"+technology_data+"'>";
 contract.innerHTML="<input type='text' id='contract_text"+"' value='"+contract_data+"'>";
}


function save_row(no)
{
 var residence_val=document.getElementById("residence_text").value;
 var project_val=document.getElementById("project_text").value;
 var projectmanager_val=document.getElementById("projectmanager_text").value;
 var hardware_val=document.getElementById("hardware_text").value;
 var technology_val=document.getElementById("technology_text").value;
 var contract_val=document.getElementById("contract_text").value;

 document.getElementById("residence_contract").innerHTML=residence_val;
 document.getElementById("project_contract").innerHTML=project_val;
 document.getElementById("projectmanager_contract").innerHTML=projectmanager_val;
 document.getElementById("hardware_contract").innerHTML=hardware_val;
 document.getElementById("technology_contract").innerHTML=technology_val;
 document.getElementById("contract_contract").innerHTML=contract_val;

 document.getElementById("edit_button"+no)
 document.getElementById("save_button"+no)


document.getElementById("edit_button"+no).style["display"]="inline-block";
 document.getElementById("save_button"+no).style["display"]="none";




		$.ajax({
			url: '/save',
                        type: "get",
			data: { residence_val : residence_val, no : no, project_val : project_val,
projectmanager_val : projectmanager_val, hardware_val : hardware_val, technology_val : technology_val, contract_val: contract_val},
		
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	







}



function edit_row_network(no, no_loc){


 

 document.getElementById("edit_button"+no);
 document.getElementById("save_button"+no);

 document.getElementById("edit_button"+no).style["display"]="none";
 document.getElementById("save_button"+no).style["display"]="inline-block";
	
 var network=document.getElementById("network_contract"+no);
 var gateway=document.getElementById("gateway_contract"+no);
 var subnet=document.getElementById("subnet_contract"+no);
 var cdir=document.getElementById("cdir_contract"+no);
 var vip=document.getElementById("vip_contract"+no);

 
	
 var network_data=network.innerHTML;
 var gateway_data=gateway.innerHTML;
 var subnet_data=subnet.innerHTML;
 var cdir_data=cdir.innerHTML;
 var vip_data=vip.innerHTML;


	
 network.innerHTML="<input type='text' id='network_text"+no+"' value='"+network_data+"'>";
 gateway.innerHTML="<input type='text' id='gateway_text"+no+"' value='"+gateway_data+"'>";
 subnet.innerHTML="<input type='text' id='subnet_text"+no+"' value='"+subnet_data+"'>";
 cdir.innerHTML="<input type='text' id='cdir_text"+no+"' value='"+cdir_data+"'>";
 vip.innerHTML="<input type='text' id='vip_text"+no+"' value='"+vip_data+"'>";
 
}




function save_row_network(no, no_loc)
{
 var network_val=document.getElementById("network_text"+no).value;
 var gateway_val=document.getElementById("gateway_text"+no).value;
 var subnet_val=document.getElementById("subnet_text"+no).value;
 var cdir_val=document.getElementById("cdir_text"+no).value;
 var vip_val=document.getElementById("vip_text"+no).value;
 

 document.getElementById("network_contract"+no).innerHTML=network_val;
 document.getElementById("gateway_contract"+no).innerHTML=gateway_val;
 document.getElementById("subnet_contract"+no).innerHTML=subnet_val;
 document.getElementById("cdir_contract"+no).innerHTML=cdir_val;
 document.getElementById("vip_contract"+no).innerHTML=vip_val;


 document.getElementById("edit_button"+no)
 document.getElementById("save_button"+no)


document.getElementById("edit_button"+no).style["display"]="inline-block";
 document.getElementById("save_button"+no).style["display"]="none";




		$.ajax({
			url: '/save_net',
                        type: "get",
			data: { network_val : network_val, no : no, gateway_val : gateway_val,
subnet_val : subnet_val, cdir_val : cdir_val, vip_val : vip_val, no_loc : no_loc },
		
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	







}

function panel(){

document.getElementById("container_add").style["display"]=null;



}


/* alert("Hallo");
	var node = document.createElement("DIV");
	node.setAttribute("class", "flex-item");
	node.setAttribute("id", "flex-item-id"); 
	var textnode = document.createTextNode("Water"); 
    node.appendChild(textnode); 
    document.getElementById("flex_one").appendChild(node); 
    var pan = document.createElement("DIV");   */