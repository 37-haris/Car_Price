
const payload = {
      Fuel_Type: $("fuel").value,
      Transmission: $("gearbox").value,
      Brand: $("brand").value,
      Model: $("model").value,
      Year: Number($("year").value),
      Kilometers_Driven: Number($("mileage_km").value),
      Engine: Number($("engine").value),
      Consommation: Number($("consommation").value),
      Location: $("location").value,      
      Owner_Type: $("owner_type").value  
    };

    console.log("Payload:", payload);
