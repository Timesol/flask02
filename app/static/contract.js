
$(document).ready(function() {
    // show the alert
    setTimeout(function() {
        $(".alert").alert('close');
    }, 2000);
});

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
 document.getElementById("delete_button"+no).style["display"]="inline-block";
	
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
  document.getElementById("delete_button"+no).style["display"]="none";




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




function send_id(id){




  document.getElementById('locid').value = id;
  document.getElementById('locid').readOnly = true;


var value_template= document.getElementById('bmodal').value;


if(value_template == 'Single-Static'){
$('label[for="gateway"]').hide();
$('label[for="fromip"]').hide();
$('label[for="toip"]').hide();
$('label[for="vip"]').hide();
$('label[for="subnet"]').hide();
$('label[for="cdir"]').hide();

document.getElementById('name').value=value_template;
document.getElementById('gateway').style["display"]="none";
document.getElementById('fromip').style["display"]="none";
document.getElementById('toip').style["display"]="none";
document.getElementById('vip').style["display"]="none";
document.getElementById('subnet').style["display"]="none";
document.getElementById('cdir').style["display"]="none";



}


}

function dec2bin(dec){
    return (dec >>> 0).toString(2);
}


function createNetmaskAddr(bitCount) {
  var mask=[];
  for(i=0;i<4;i++) {
    var n = Math.min(bitCount, 8);
    mask.push(256 - Math.pow(2, 8-n));
    bitCount -= n;
  }
  return mask.join('.');
}

function getIpRangeFromAddressAndNetmask(str) {
  var part = str.split("/"); // part[0] = base address, part[1] = netmask
  var ipaddress = part[0].split('.');
  var netmaskblocks = ["0","0","0","0"];
  if(!/\d+\.\d+\.\d+\.\d+/.test(part[1])) {
    // part[1] has to be between 0 and 32
    netmaskblocks = ("1".repeat(parseInt(part[1], 10)) + "0".repeat(32-parseInt(part[1], 10))).match(/.{1,8}/g);
    netmaskblocks = netmaskblocks.map(function(el) { return parseInt(el, 2); });
  } else {
    // xxx.xxx.xxx.xxx
    netmaskblocks = part[1].split('.').map(function(el) { return parseInt(el, 10) });
  }
  // invert for creating broadcast address (highest address)
  var invertedNetmaskblocks = netmaskblocks.map(function(el) { return el ^ 255; });
  var baseAddress = ipaddress.map(function(block, idx) { return block & netmaskblocks[idx]; });
  var broadcastaddress = baseAddress.map(function(block, idx) { return block | invertedNetmaskblocks[idx]; });
  return [baseAddress.join('.'), broadcastaddress.join('.')];
}


$(document).ready(function(){
    var $regexname=/(?=[/.]).*[?=1234567890]$/;
    $('#network').on('keypress keydown keyup',function(){
             if (!$(this).val().match($regexname)) {
              
                 $('.emsg').removeClass('hidden');
                 $('.emsg').show();
                 

             }
           else{
           	var network_calc=$(this).val();
            var calc= network_calc.split("/");
           	var calc_cdir= calc[1];
                // else, do not display message
                $('.emsg').addClass('hidden');
                if(!$('#cdir').is(":hidden")){ 
                $('#cdir').val(calc_cdir)}
                calc_cdir= calc[0];
                

                network_calc=network_calc.split("/");
                network_calc=network_calc[0]
                
                network_calc= network_calc.split(".");
               
                var oc1 = parseInt(network_calc[0]);
                var oc2 = parseInt(network_calc[1]);
                var oc3 = parseInt(network_calc[2]);
                var oc4 = parseInt(network_calc[3]);
                calc=parseInt(calc[1])
                if(!$('#subnet').is(":hidden")){ 
                $('#subnet').val(createNetmaskAddr(calc))}
                hosts=32-calc
                hosts=Math.pow(2, hosts)
                console.log(hosts)
                var ip=$(this).val();
                ip= getIpRangeFromAddressAndNetmask(ip)
                if(!$('#fromip').is(":hidden")){ 
                $('#fromip').val(ip[0])}
                if(!$('#toip').is(":hidden")){ 
                $('#toip').val(ip[1])}

                if(!$('#gateway').is(":hidden")){   
                oc4=oc4+1
                var gateway=[oc1,oc2,oc3,oc4].join(".")
                $('#gateway').val(gateway)}
 






               }
         });
});


function router_todo(no){

    $.ajax({
      url: '/router_todo',
                        type: "get",
      data: {  no : no},
    
      success: function(response){
        console.log(response);
      },
      error: function(error){
        console.log(error);
      }
    });
  







}



function hide_net_forms(){

var value_template= document.getElementById('bmodal').value;


if(value_template == 'ppp-static'){

$('label[for="gateway"]').hide();
document.getElementById('gateway').type="hidden";

}






}





/* alert("Hallo");
	var node = document.createElement("DIV");
	node.setAttribute("class", "flex-item");
	node.setAttribute("id", "flex-item-id"); 
	var textnode = document.createTextNode("Water"); 
    node.appendChild(textnode); 
    document.getElementById("flex_one").appendChild(node); 
    var pan = document.createElement("DIV");   */