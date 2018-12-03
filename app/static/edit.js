function scraper(){

contract=document.getElementById('contract').value


                $.ajax({
                        url: '/scraper',
                        type: "get",
                        data: {  contract : contract},
                
                        success: function(response){
                                console.log(response);
                                var json = JSON.parse(response);
                                document.getElementById('residence').value =json['match'];
                                document.getElementById('project').value =json['project'];
                                document.getElementById('technology').value =json['technology'];
                                document.getElementById('hardware').value =json['hardware'];
                                document.getElementById('customer').value =json['customer'];
                        },
                        error: function(error){
                                console.log(error);
                        }
                });
        







}





function edit_row(no){


 

 document.getElementById("edit_button"+no);
 document.getElementById("save_button"+no);

 $("#edit_button"+no).addClass('disabled')
 $("#save_button"+no).removeClass('disabled')
	
 var residence=document.getElementById("residence_row"+no);
 var project=document.getElementById("project_row"+no);
 var projectmanager=document.getElementById("projectmanager_row"+no);
 var hardware=document.getElementById("hardware_row"+no);
 var technology=document.getElementById("technology_row"+no);
 var contract=document.getElementById("contract_row"+no);
 
	
 var residence_data=residence.innerHTML;
 var project_data=project.innerHTML;
 var projectmanager_data=projectmanager.innerHTML;
 var hardware_data=hardware.innerHTML;
 var technology_data=technology.innerHTML;
 var contract_data=contract.innerHTML;

	
 residence.innerHTML="<input type='text' id='residence_text"+no+"' value='"+residence_data+"'>";
 project.innerHTML="<input type='text' id='project_text"+no+"' value='"+project_data+"'>";
 projectmanager.innerHTML="<input type='text' id='projectmanager_text"+no+"' value='"+projectmanager_data+"'>";
 hardware.innerHTML="<input type='text' id='hardware_text"+no+"' value='"+hardware_data+"'>";
 technology.innerHTML="<input type='text' id='technology_text"+no+"' value='"+technology_data+"'>";
 contract.innerHTML="<input type='text' id='contract_text"+no+"' value='"+contract_data+"'>";
}



function save_row(no)
{
 var residence_val=document.getElementById("residence_text"+no).value;
 var project_val=document.getElementById("project_text"+no).value;
 var projectmanager_val=document.getElementById("projectmanager_text"+no).value;
 var hardware_val=document.getElementById("hardware_text"+no).value;
 var technology_val=document.getElementById("technology_text"+no).value;
 var contract_val=document.getElementById("contract_text"+no).value;

 document.getElementById("residence_row"+no).innerHTML=residence_val;
 document.getElementById("project_row"+no).innerHTML=project_val;
 document.getElementById("projectmanager_row"+no).innerHTML=projectmanager_val;
 document.getElementById("hardware_row"+no).innerHTML=hardware_val;
 document.getElementById("technology_row"+no).innerHTML=technology_val;
 document.getElementById("contract_row"+no).innerHTML=contract_val;

 document.getElementById("edit_button"+no)
 document.getElementById("save_button"+no)


$("#edit_button"+no).removeClass('disabled')
$("#save_button"+no).addClass('disabled')




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






function get_id(id){




  document.getElementById('locid').value = id;
  document.getElementById('locid').readOnly = true;




}


function get_data(technology, hardware,user,contract,customer){




  
  document.getElementById('technology').value = technology;
  document.getElementById('hardware').value = hardware;
  document.getElementById('customer').value = customer;
  document.getElementById('user').value = user;
  document.getElementById('contract').value = contract;
  
  

   

}




function show_net() {
    var x = document.getElementById("nets");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

function collapse_data(list){





$.ajax({

          data : {list : list},
                

             type : 'get',
             url : window.location.pathname,
            	success: function(response){
				console.log(response);
				var myData = JSON.parse(response);
				document.getElementById("test").innerHTML=myData.id

			},
			error: function(error){
				console.log(error);
			}



            })


}
















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











/*
$(document).ready(function() {


var modal = document.getElementById('rowi');
var id = modal.dataset.lid


/*
     $('form').on('submit', function(event) {
      
       $.ajax({

          data: {id: id},
                

             type : 'get',
             //contentType: 'application/json;charset=UTF-8',
             //dataType: "json",
             url : window.location.pathname,
            	success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}



            })
       
       
        
      });
      
      });

/*
$(document).ready(function() {

var modal = document.getElementById('rowi');
var id = modal.dataset.lid

$('#myModal').on('show.bs.modal', function() {


	

  document.getElementById('locid').value = id;
  document.getElementById('locid').readOnly = true;



});
     });


/*
$(document).ready(function() {

var modal = document.getElementById('myModal');
var id = modal.dataset.lid

$('#myModal').on('hidden.bs.modal', function() {
    // do something when the modal is shown


$.ajax({

          data : {id: id},
                

             type : 'get',
             url : window.location.pathname,
            	success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}



            })



});
     });



$(document).ready(function() {


var modal = document.getElementById('myModal');
var id = modal.dataset.lid



     $('form').on('submit', function(event) {

       $.ajax({

          data : {id: id},
                

             type : 'get',
             url : window.location.pathname,
            	success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}



            })
        
      });
      
      });



*/	
