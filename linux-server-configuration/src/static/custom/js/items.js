$(document).ready(function() {
    var isdelete = IsDeleteAction();
    if(isdelete){
        var mytitle = 'Confirm Delete';
        var mytext = 'Confirm delete of the selected item?';
        ConfirmDelete(mytitle, mytext);
    }
});

function ConfirmDelete(mytitle, mytext){
    $.confirm({
        title: mytitle,
        content: mytext,
        buttons: {
            confirm: function () {
                // $.alert('Confirmed for delete!');
                runDeleteItem();
            },
            cancel: function () {
                // $.alert('Canceled!');
                var base_url = window.location.protocol + "//" + window.location.host;
                window.location.replace(base_url);
            }
        }
    });
}

function IsDeleteAction(){
    if(window.location.href.indexOf("delete") >= 0){
        return true;
    }
    else {
        return false;
    }

}

function runDeleteItem(){
    $("#upload_submit").remove();
    $.ajax ({
          url: $(location).attr('href'),
          data: { 'item_name' : $('#item_name').val(),
                  'item_description' : $('#item_description').val(),
                  'item_slug' : $('#item_slug').val(),
                  'category' : $('#category').val(),
                  'csrf_token' : $('#csrf_token').val()},
          type: 'POST',
          success: function(response) {
              var base_url = window.location.protocol + "//" + window.location.host;
              if (response.error_state == 1){
                  $.alert({
                        title: 'Error on Delete!',
                        content: response.error_msg,
                    });
                                  }
              if(response.redirect_url == undefined){
                  window.location.replace(base_url);
                  return;
              }
              var redirect_url = base_url + response.redirect_url;
              window.location.replace(redirect_url);
          },
          error: function(error){
              console.log(error);
          }
    });
}
