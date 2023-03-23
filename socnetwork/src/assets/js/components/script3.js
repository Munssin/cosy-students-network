$(document).ready(function(){

$(document).on('submit','#post-form',function(e){
    e.preventDefault();
    $.ajax({
      type:'POST',
      url:'/send/',
      data:{
          room_id:document.getElementById('room_id').value,
          under_room_id:document.getElementById('under_room_id').value,
          message:$('#message').val(),
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
      },
      success: function(data){
         //alert(data)
      }
    });
    document.getElementById('message').value = ''
});

$(document).on('submit','#post-form_url',function(e){
    e.preventDefault();
    $.ajax({
      type:'POST',
      url:'/send_url/',
      data:{
          room_id:document.getElementById('room_id').value,
          under_room_id:document.getElementById('under_room_id').value,
          message_url:$('#message_url').val(),
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
      },
      success: function(data){
         //alert(data)
      }
    });
    document.getElementById('message_url').value = ''
});

$.ajax({
    type: 'GET',
    url : "/getRooms/",
    data:{
    },
    success: function(response){
        $("#rooms_menu").empty();
        for (var key in response.room){
            if (response.room[key].members.includes(response.username_r)){
                var temp="<div class='group_btn'><div class='dropdown'><button type='buttonA' class='listA-button width-Asettings' data-bs-toggle='dropdown' aria-expanded='false'>"+response.room[key].name+"<p class='text-A'>error users</p></button></button><ul class='dropdown-menu'><li><a class='dropdown-item' href='../../../user_workplace_test/"+response.room[key].id+"/1/'>Дискретна</a></li><li><a class='dropdown-item' href='../../../user_workplace_test/"+response.room[key].id+"/2/'>Мат аналіз</a></li><li><a class='dropdown-item' href='../../../user_workplace_test/"+response.room[key].id+"/3/'>Фізика</a></li></ul></div>";
                $("#rooms_menu").append(temp);
            }
        }
    },
});


$.ajax({
    type: 'GET',
    url : "/getMessages/"+document.getElementById('room_id').value+"/"+document.getElementById('under_room_id').value+"/",
    data:{
        username:$('#username').val(),
    },
    success: function(response){
        $("#chat_box").empty();
        for (var key in response.messages){
            var temp="<div class='speakermess'><b class='nickuser'>"+response.messages[key].user+"</b><p class='text-mess'>"+response.messages[key].value+"</p> </div>";
            var temp2="<div class='usermess'><b class='nickusermess'>"+response.messages[key].user+"</b><p class='text-mess'>"+response.messages[key].value+"</p> </div>";
            $("#chat_box").append(temp);
        }
        var block = document.getElementById("chat_box");
        block.scrollTop = block.scrollHeight;
    },
});

$.ajax({
    type: 'GET',
    url : "/getMessages_url/"+document.getElementById('room_id').value+"/"+document.getElementById('under_room_id').value+"/",
    data:{
        username:$('#username').val(),
    },
    success: function(response){
        $("#chat_box_url").empty();
        for (var key in response.messages_url)
        {
            var temp="<div class='speakermess'><b class='nickuser'>"+response.messages_url[key].user+"</b><p class='text-mess'><a href="+response.messages_url[key].value+" target='_blank'>"+response.messages_url[key].value+"</a></p> </div>";
            var temp2="<div class='usermess'><b class='nickusermess'>"+response.messages_url[key].user+"</b><p class='text-mess'>"+response.messages_url[key].value+"</p> </div>";
            $("#chat_box_url").append(temp);
        }
        var block = document.getElementById("chat_box");
        block.scrollTop = block.scrollHeight;    
    },
});

$.ajax({
    type: 'GET',
    url : "/getFiles/"+document.getElementById('room_id').value+"/"+document.getElementById('under_room_id').value+"/",
    data:{
        files:$('#files').val(),
    },
    success: function(response){
        console.log(response);
        $("#refuge-group").empty();
        for (var key in response.files)
        {
            var temp="<ul class='for-ulRG'><li><a href='download/"+response.files[key].id+"/'><button type='buttonU' class='listR-button width-Usettings' data-toggle='modal' data-target='#staticBackdrop'><div class='square'>T</div><h2 class='text'>"+response.files[key].file_name+"</h2><p class='text-R'>mb</p><p class='text-R'>"+response.files[key].user+"</p></button></a></li></ul>";
            $("#refuge-group").append(temp);
        }
    },
    error: function(response){
        //alert('An error occured')
    }
});

setInterval(function(){

    $.ajax({
        type: 'GET',
        url : "/getMessages/"+document.getElementById('room_id').value+"/"+document.getElementById('under_room_id').value+"/",
        data:{
            username:$('#username').val(),
        },
        success: function(response){
            $("#chat_box").empty();
            for (var key in response.messages){
                var temp="<div class='speakermess'><b class='nickuser'>"+response.messages[key].user+"</b><p class='text-mess'>"+response.messages[key].value+"</p> </div>";
                var temp2="<div class='usermess'><b class='nickusermess'>"+response.messages[key].user+"</b><p class='text-mess'>"+response.messages[key].value+"</p> </div>";
                $("#chat_box").append(temp);
            }
        },
    });

    $.ajax({
        type: 'GET',
        url : "/getMessages_url/"+document.getElementById('room_id').value+"/"+document.getElementById('under_room_id').value+"/",
        data:{
            username:$('#username').val(),
        },
        success: function(response){
            $("#chat_box_url").empty();
            for (var key in response.messages_url)
            {
                var temp="<div class='speakermess'><b class='nickuser'>"+response.messages_url[key].user+"</b><p class='text-mess'><a href="+response.messages_url[key].value+" target='_blank'>"+response.messages_url[key].value+"</a></p> </div>";
                var temp2="<div class='usermess'><b class='nickusermess'>"+response.messages_url[key].user+"</b><p class='text-mess'>"+response.messages_url[key].value+"</p> </div>";
                $("#chat_box_url").append(temp);
            }
        },
    });

    $.ajax({
        type: 'GET',
        url : "/getFiles/"+document.getElementById('room_id').value+"/"+document.getElementById('under_room_id').value+"/",
        data:{
            files:$('#files').val(),
        },
        success: function(response){
            console.log(response);
            $("#refuge-group").empty();
            for (var key in response.files)
            {
                var temp="<ul class='for-ulRG'><li><a href='download/"+response.files[key].id+"/'><button type='buttonU' class='listR-button width-Usettings' data-toggle='modal' data-target='#staticBackdrop'><div class='square'>T</div><h2 class='text'>"+response.files[key].file_name+"</h2><p class='text-R'>mb</p><p class='text-R'>"+response.files[key].user+"</p></button></a></li></ul>";
                $("#refuge-group").append(temp);
            }
        },
        error: function(response){
            //alert('An error occured')
        }
    });


},1000);
})