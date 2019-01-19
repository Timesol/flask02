function save_status(id,status){


    $.ajax({
      url: '/save_status',
                        type: "get",
      data: {  id : id, status : status},
    
      success: function(response){
        console.log(response);
      },
      error: function(error){
        console.log(error);
      }
    });


  status=status.charAt(0).toUpperCase() + status.slice(1);

  document.getElementById("drop_button"+id).innerHTML=status
  }