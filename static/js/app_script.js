function find_city() {
      $zval = $('#zip_code').val();

      if($zval.length == 5){
         $jCSval = getCityState($zval);
      }
    };

function getCityState($zip) {
	 $.getJSON('https://maps.googleapis.com/maps/api/geocode/json?address=' + $zip + '&key=ENTERKEYHERE', function(response){
         //find the city and state
	 var address_components = response.results[0].address_components;

	 $.each(address_components, function(index, component){
		 var types = component.types;

		 $.each(types, function(index, type){

			if(type == 'locality') {
			  city = component.long_name;
			  hascity = 1;
			}
			if(type == 'administrative_area_level_1') {
			  state = component.short_name;
			}
		 });
	});

	//pre-fill the city and state
        if(hascity == 1){
			$('#add2').val(city + ', ' + state);
        }
    });
  };

app = new Vue({
  el:'#root',
  data:{
    zip: ''
  }
}
)
