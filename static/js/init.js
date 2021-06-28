(function($){
  $(function(){

    $('.sidenav').sidenav();
    $('.parallax').parallax();
    $('.fixed-action-btn').floatingActionButton();
    $('.collapsible').collapsible();    
    $('textarea#message').characterCounter();
    $("select").formSelect();
    $('.modal').modal();
    $('#end_date').on('change', function () {
        var date1 = new Date($('#start_date').val());
        var date2 = new Date($('#end_date').val());
        if (date1 > date2) {
            $('#end_date').val(null)
            alert("Campaign end date must be after start date; please reselect");
        }
    });
    $('#start_date').on('change', function () {
        var date1 = new Date($('#start_date').val());
        var date2 = new Date($('#end_date').val());
        if (date1 > date2) {
            $('#start_date').val(null)
            alert("Campaign end date must be after start date; please reselect");
        }
    });
    validateMaterializeSelect();
    function validateMaterializeSelect() {
        let classValid = { "border-bottom": "1px solid #4caf50", "box-shadow": "0 1px 0 0 #4caf50" };
        let classInvalid = { "border-bottom": "1px solid #f44336", "box-shadow": "0 1px 0 0 #f44336" };
        if ($("select.validate").prop("required")) {
            $("select.validate").css({ "display": "block", "height": "0", "padding": "0", "width": "0", "position": "absolute" });
        }
        $(".select-wrapper input.select-dropdown").on("focusin", function () {
            $(this).parent(".select-wrapper").on("change", function () {
                if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () { })) {
                    $(this).children("input").css(classValid);
                }
            });
        }).on("click", function () {
            if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
                $(this).parent(".select-wrapper").children("input").css(classValid);
            } else {
                $(".select-wrapper input.select-dropdown").on("focusout", function () {
                    if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                        if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
                            $(this).parent(".select-wrapper").children("input").css(classInvalid);
                        }
                    }
                });
            }
        });
    }    
  });
})(jQuery); // end of jQuery name space