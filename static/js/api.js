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

$(function(){
  $('#company_country_name').on('click', function(){
    select.addEventListener("change", handleCountryChange.bind(this));
  });
});