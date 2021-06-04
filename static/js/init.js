(function($){
  $(function(){

    $('.sidenav').sidenav();
    $('.parallax').parallax();
    $('.fixed-action-btn').floatingActionButton();
    $('.collapsible').collapsible();    
    $('textarea#message').characterCounter();

  }); // end of document ready
})(jQuery); // end of jQuery name space

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.chips');
  var instances = M.Chips.init(elems, options);
});

$('#message').val('');
M.textareaAutoResize($('#message'));
