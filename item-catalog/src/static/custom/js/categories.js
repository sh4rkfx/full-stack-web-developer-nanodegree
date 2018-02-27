$(document).ready(function() {
    var isdelete = IsDeleteAction();
    if(isdelete){
        var mytitle = 'Confirm Delete';
        var mytext = 'Confirm delete of the selected category?';
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
                runDeleteCat();
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
    if(window.location.href.indexOf("delete") >= 0)
        return true;
    else
        return false;
}

function runDeleteCat(){
    $("#upload_submit").remove();
    $.ajax ({
          url: $(location).attr('href'),
          data: { 'category_name' : $('#category_name').val(),
                  'category_description' : $('#category_description').val(),
                  'category_slug' : $('#category_slug').val(),
                  'csrf_token' : $('#csrf_token').val()},
          type: 'POST',
          success: function(response) {
              console.log('successful delete3');
              var base_url = window.location.protocol + "//" + window.location.host;
              var redirect_url = base_url + response.redirect_url;
              console.log(redirect_url);
              window.location.replace(redirect_url);
          },
          error: function(error){
              console.log(error);
          }
    });
}
