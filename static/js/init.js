(function($){
  $(function(){

    $('.sidenav').sidenav();
    $('.parallax').parallax();
    $('.fixed-action-btn').floatingActionButton();
    $('.collapsible').collapsible();    
    $('textarea#message').characterCounter();
    $("select").formSelect();
    $('.modal').modal();
    $(".datepicker").datepicker({
      format: "dd/mm/yyyy",
      yearRange: 3,
      showClearBtn: true,        
      i18n: {
        done: "Select"
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

// Country dropdown API

const xhttp = new XMLHttpRequest();
const select = document.getElementById("company_country_name");

let countries;

xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    countries = JSON.parse(xhttp.responseText);
    assignValues();
    handleCountryChange();
  }
};
xhttp.open("GET", "https://restcountries.eu/rest/v2/all", true);
xhttp.send();

function assignValues() {
  countries.forEach(country => {
    const option = document.createElement("option");
    option.textContent = country.name;
    select.appendChild(option);
  });
}

function handleCountryChange() {
  const countryData = countries.find(
    country => select.value === country.alpha2Code
  );
}

select.addEventListener("change", handleCountryChange.bind(this));
