
var $LightingHourDetailForm = $('#form_lighting_hour_detail');
$LightingHourDetailForm.submit(function (event) {
    event.preventDefault();
    saveLightingHourDetail();
});

showLightingHourDetails();
$(".btn-close-lighting-hour-detail-modal").click(closeLightingHourDetailModal);

var $LightingInputForm = $('#form_lighting_inputs');
$LightingInputForm.submit(function (event) {
    event.preventDefault();
    saveLightingInput();
});

showLightingInputs();
calculateLightingOutputs();
$(".btn-close-lighting-input-modal").click(closeLightingInputModal);


function saveLightingHourDetail(){
    var url = '/lighting/save_lighting_hour_detail/'
    var $LightingHourDetailForm = $('#form_lighting_hour_detail');
    var scenarioId = document.getElementById("hidden_scenario_id").value;
    var lightingHourDetailId = document.getElementById("modal_hidden_lighting_hour_detail").value;
    var $formData = $LightingHourDetailForm.serialize() + '&scenarioId=' + scenarioId + '&lightingHourDetailId=' + lightingHourDetailId;
    console.log($formData);
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    clearLightingHourDetailErrors();
                    var data = JSON.parse(this.responseText);
                    console.log(data)
                    if (data.message == "Success") {
                        closeLightingHourDetailModal();                        
                        showLightingHourDetails();

                        // Fill Lighting Hour Detail choices
                        selected_lighting_hour_detail_id = document.getElementById("lighting_input_lighting_type").value
                        $("#lighting_input_lighting_type").empty();
                        var sel = document.getElementById('lighting_input_lighting_type');
                        // create new option element
                        console.log(data)
                        for (i=0;i<data.idList.length;i++){
                            var opt = document.createElement('option');
                            opt.appendChild( document.createTextNode(data.lightingTypeList[i]) );
                            opt.value = data.idList[i];
                            sel.appendChild(opt); 
                            if (opt.value == selected_lighting_hour_detail_id){
                                opt.setAttribute("selected", "selected");
                            }
                        }
                    }
                    else {
                        if ((typeof data.message) == "string") {
                            createErrorMessage("error_lighting_hour_detail_lighting_type", data.message)
                        }
                        else {
                            if ("lighting_type" in data.message) {
                                createErrorMessage("error_lighting_hour_detail_lighting_type", data.message.lighting_type)
                            }                                                       
                         
                        }
                    }

                }
    }
    request.send($formData);
}

function clearLightingHourDetailErrors(){
    deleteErrorMessage("error_lighting_hour_detail_lighting_type");  
}

function closeLightingHourDetailModal(){
    clearLightingHourDetailModal();
    $('#modal-lighting-hour-details').modal("hide");
}

function clearLightingHourDetailModal(){
    var $LightingHourDetailForm = $('#form_lighting_hour_detail');
    document.getElementById('modal_hidden_lighting_hour_detail').value = "";
    $LightingHourDetailForm[0].reset();
    clearLightingHourDetailErrors();
}

function showLightingHourDetails(){
    var url = '/lighting/show_lighting_hour_details/'
    var obj = new Object;
    obj.scenarioId = document.getElementById("hidden_scenario_id").value;
    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var data = JSON.parse(this.responseText);
                    console.log(data);
                    if (data.message == 'Success') {
                        table_html = []
                        if (data.value.length > 0) {
                            for (i = 0; i < data.value.length; i++) {
                                table_html = table_html +
                                    (                                        
                                        "<tr align='center'>" +
                                        "<td>" + (i + 1) + "</td>" +
                                        "<td>" + data.value[i].lighting_type + "</td>" +                                        
                                        "<td>" +
                                        "<a class='btn text-secondary px-0' onclick='editLightingHourDetail(" + data.value[i].id + ")';><i class='far fa-edit fa-lg'></i></a>" +
                                        "<button class='btn d-inline' onclick='deleteLightingHourDetail(" + data.value[i].id + ")';>" +
                                        "<i class='far fa-trash-alt fa-lg text-danger float-right'></i>" +
                                        "</button>" +
                                        "</td>" +
                                        "</tr>"
                                    )

                            }
                        }
                        document.getElementById("tbl_lighting_hour_detail_body").innerHTML = table_html
                        deleteErrorMessage("div_lighting_hour_detail_error")
                    }
                    else {
                        createErrorMessage("div_lighting_hour_detail_error", data.message)
                    }

                }
    }
    request.send(params);
}

function editLightingHourDetail(lightingHourDetailId){
    var url = '/lighting/edit_lighting_hour_detail/'
    var obj = new Object;
    obj.lightingHourDetailId = lightingHourDetailId;

    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    console.log(this.responseText);
                    var data = JSON.parse(this.responseText);
                    if (data.message == "Success") {
                        clearLightingHourDetailModal();
                        $('#modal-lighting-hour-details').modal();
                        document.getElementById('modal_hidden_lighting_hour_detail').value = data.value.id;
                        document.getElementById("lighting_hour_detail_lighting_type").value = data.value.lighting_type
                        document.getElementById("lighting_hour_detail_monday_lighting_hour_1_start").value = data.value['monday_lighting_hour_1_start'];
                        document.getElementById("lighting_hour_detail_monday_lighting_hour_1_end").value = data.value['monday_lighting_hour_1_end'];
                        document.getElementById("lighting_hour_detail_monday_lighting_hour_2_start").value = data.value['monday_lighting_hour_2_start'];
                        document.getElementById("lighting_hour_detail_monday_lighting_hour_2_end").value = data.value['monday_lighting_hour_2_end'];
                        document.getElementById("lighting_hour_detail_tuesday_lighting_hour_1_start").value = data.value['tuesday_lighting_hour_1_start'];
                        document.getElementById("lighting_hour_detail_tuesday_lighting_hour_1_end").value = data.value['tuesday_lighting_hour_1_end'];
                        document.getElementById("lighting_hour_detail_tuesday_lighting_hour_2_start").value = data.value['tuesday_lighting_hour_2_start'];
                        document.getElementById("lighting_hour_detail_tuesday_lighting_hour_2_end").value = data.value['tuesday_lighting_hour_2_end'];
                        document.getElementById("lighting_hour_detail_wednesday_lighting_hour_1_start").value = data.value['wednesday_lighting_hour_1_start'];
                        document.getElementById("lighting_hour_detail_wednesday_lighting_hour_1_end").value = data.value['wednesday_lighting_hour_1_end'];
                        document.getElementById("lighting_hour_detail_wednesday_lighting_hour_2_start").value = data.value['wednesday_lighting_hour_2_start'];
                        document.getElementById("lighting_hour_detail_wednesday_lighting_hour_2_end").value = data.value['wednesday_lighting_hour_2_end'];
                        document.getElementById("lighting_hour_detail_thursday_lighting_hour_1_start").value = data.value['thursday_lighting_hour_1_start'];
                        document.getElementById("lighting_hour_detail_thursday_lighting_hour_1_end").value = data.value['thursday_lighting_hour_1_end'];
                        document.getElementById("lighting_hour_detail_thursday_lighting_hour_2_start").value = data.value['thursday_lighting_hour_2_start'];
                        document.getElementById("lighting_hour_detail_thursday_lighting_hour_2_end").value = data.value['thursday_lighting_hour_2_end'];
                        document.getElementById("lighting_hour_detail_friday_lighting_hour_1_start").value = data.value['friday_lighting_hour_1_start'];
                        document.getElementById("lighting_hour_detail_friday_lighting_hour_1_end").value = data.value['friday_lighting_hour_1_end'];
                        document.getElementById("lighting_hour_detail_friday_lighting_hour_2_start").value = data.value['friday_lighting_hour_2_start'];
                        document.getElementById("lighting_hour_detail_friday_lighting_hour_2_end").value = data.value['friday_lighting_hour_2_end'];
                        document.getElementById("lighting_hour_detail_saturday_lighting_hour_1_start").value = data.value['saturday_lighting_hour_1_start'];
                        document.getElementById("lighting_hour_detail_saturday_lighting_hour_1_end").value = data.value['saturday_lighting_hour_1_end'];
                        document.getElementById("lighting_hour_detail_saturday_lighting_hour_2_start").value = data.value['saturday_lighting_hour_2_start'];
                        document.getElementById("lighting_hour_detail_saturday_lighting_hour_2_end").value = data.value['saturday_lighting_hour_2_end'];
                        document.getElementById("lighting_hour_detail_sunday_lighting_hour_1_start").value = data.value['sunday_lighting_hour_1_start'];
                        document.getElementById("lighting_hour_detail_sunday_lighting_hour_1_end").value = data.value['sunday_lighting_hour_1_end'];
                        document.getElementById("lighting_hour_detail_sunday_lighting_hour_2_start").value = data.value['sunday_lighting_hour_2_start'];
                        document.getElementById("lighting_hour_detail_sunday_lighting_hour_2_end").value = data.value['sunday_lighting_hour_2_end'];                       
                        deleteErrorMessage("div_lighting_hour_detail_error");
                        
                    }
                    else{
                        createErrorMessage("div_lighting_hour_detail_error", data.message);
                    }
                    

                }
    }
    request.send(params);
}

function deleteLightingHourDetail(lightingHourDetailId){
    var url = '/lighting/delete_lighting_hour_detail/'
    var scenarioId = document.getElementById("hidden_scenario_id").value;
    var obj = new Object;
    obj.lightingHourDetailId = lightingHourDetailId;
    obj.scenarioId = scenarioId
    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var data = JSON.parse(this.responseText);
                    if (data.message == "Success") {
                        showLightingHourDetails();
                        showLightingInputs();
                        deleteErrorMessage("div_lighting_hour_detail_error")
                        // Fill Lighting Hour Detail choices
                        selected_lighting_hour_detail_id = document.getElementById("lighting_input_lighting_type").value
                        $("#lighting_input_lighting_type").empty();
                        var sel = document.getElementById('lighting_input_lighting_type');
                        // create new option element
                        console.log(data)
                        for (i=0;i<data.idList.length;i++){
                            var opt = document.createElement('option');
                            opt.appendChild( document.createTextNode(data.lightingTypeList[i]) );
                            opt.value = data.idList[i];
                            sel.appendChild(opt); 
                            if (opt.value == selected_lighting_hour_detail_id){
                                opt.setAttribute("selected", "selected");
                            }
                        }
                    }
                    else {
                        createErrorMessage("div_lighting_hour_detail_error", data.message)
                    }

                }
    }
    request.send(params);
}


// -------------------------------- Lighting Input -------------------------


function saveLightingInput(){
    var url = '/lighting/save_lighting_input/'
    var $LightingInputForm = $('#form_lighting_inputs');
    var scenarioId = document.getElementById("hidden_scenario_id").value;
    var lightingInputId = document.getElementById("modal_hidden_lighting_input").value;
    var $formData = $LightingInputForm.serialize() + '&scenarioId=' + scenarioId + '&lightingInputId=' + lightingInputId;
    console.log($formData);
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    clearLightingInputErrors();
                    var data = JSON.parse(this.responseText);
                    console.log(data)
                    if (data.message == "Success") {
                        closeLightingInputModal();
                        showLightingInputs();
                        calculateLightingOutputs();
                    }
                    else {
                        if ((typeof data.message) == "string") {
                            createErrorMessage("error_lighting_input_lighting_type", data.message)
                        }
                        else {
                            if ("lighting_type" in data.message) {
                                createErrorMessage("error_lighting_input_lighting_type", data.message.lighting_type)
                            } 
                            if ("number_of_existing_luminaire" in data.message) {
                            createErrorMessage("error_lighting_input_number_of_existing_luminaire", data.message.number_of_existing_luminaire);
                            }
                            if ("existing_luminaire" in data.message) {
                                createErrorMessage("error_lighting_input_existing_luminaire", data.message.existing_luminaire);
                            }
                            if ("existing_luminaire_power" in data.message) {
                                createErrorMessage("error_lighting_input_existing_luminaire_power", data.message.existing_luminaire_power);
                            } 
                            if ("number_of_replaced_luminaire" in data.message) {
                                createErrorMessage("error_lighting_input_number_of_replaced_luminaire", data.message.number_of_replaced_luminaire);
                            }
                            if ("replacement_luminaire" in data.message) {
                                createErrorMessage("error_lighting_input_replacement_luminaire", data.message.replacement_luminaire);
                            }
                            if ("replacement_luminaire_power" in data.message) {
                                createErrorMessage("error_lighting_input_replacement_luminaire_power", data.message.replacement_luminaire_power);
                            }
                            if ("power_reduction" in data.message) {
                                createErrorMessage("error_lighting_input_power_reduction", data.message.power_reduction); 
                             }
                            if ("estimated_operating_hours" in data.message) {
                                createErrorMessage("error_lighting_input_estimated_operating_hours", data.message.estimated_operating_hours);
                            }
                            if ("total_estimated_savings_kwhs" in data.message) {
                                createErrorMessage("error_lighting_input_total_estimated_savings_kwhs", data.message.total_estimated_savings_kwhs);
                            }
                            if ("veec_discount" in data.message) {
                                createErrorMessage("error_lighting_input_veec_discount", data.message.veec_discount);
                            }
                            if ("esc_discount" in data.message) {
                                createErrorMessage("error_lighting_input_esc_discount", data.message.esc_discount);
                            }
                            if ("discount_adjustment" in data.message) {
                                createErrorMessage("error_lighting_input_discount_adjustment", data.message.discount_adjustment);
                            }
                            if ("total_discount" in data.message) {
                                createErrorMessage("error_lighting_input_total_discount", data.message.total_discount);
                            }
                            if ("maintenance_savings" in data.message) {
                                createErrorMessage("error_lighting_input_maintenance_savings", data.message.maintenance_savings);
                            }
                            if ("dollar_per_fixture" in data.message) {
                                createErrorMessage("error_lighting_input_dollar_per_fixture", data.message.dollar_per_fixture);
                            }
                            if ("labour_per_hour" in data.message) {
                                createErrorMessage("error_lighting_input_labour_per_hour", data.message.labour_per_hour);
                            }
                            if ("fixtures_per_hour" in data.message) {
                                createErrorMessage("error_lighting_input_fixtures_per_hour", data.message.fixtures_per_hour);
                            }
                            if ("total_cost" in data.message) {
                                createErrorMessage("error_lighting_input_total_cost", data.message.total_cost);
                            }
                            if ("led_life_in_months" in data.message) {
                                createErrorMessage("error_lighting_input_led_life_in_months", data.message.led_life_in_months);
                            }
                            if ("existing_lamp_replacement_costs" in data.message) {
                                createErrorMessage("error_lighting_input_existing_lamp_replacement_costs", data.message.existing_lamp_replacement_costs);
                            }
                            if ("existing_luminaire_life_in_months" in data.message) {
                                createErrorMessage("error_lighting_input_existing_luminaire_life_in_months", data.message.existing_luminaire_life_in_months);
                            }                                                      
                         
                        }
                    }

                }
    }
    request.send($formData);
}


function showLightingInputs(){
    var url = '/lighting/show_lighting_inputs/'
    var obj = new Object;
    obj.scenarioId = document.getElementById("hidden_scenario_id").value;
    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var data = JSON.parse(this.responseText);
                    console.log(data);
                    if (data.message == 'Success') {
                        table_html = []
                        if (data.value.length > 0) {
                            for (i = 0; i < data.value.length; i++) {
                                table_html = table_html +
                                    (                                        
                                        "<tr align='center'>" +
                                        "<td>" + (i + 1) + "</td>" +
                                        "<td>" + nullValidation(data.value[i].area) + "</td>" +
                                        "<td>" + data.value[i].lighting_type + "</td>" +
                                        "<td>" + data.value[i].number_of_existing_luminaire + "</td>" +
                                        "<td>" + data.value[i].existing_luminaire + "</td>" +
                                        "<td>" + data.value[i].existing_luminaire_power + "</td>" +
                                        "<td>" + data.value[i].number_of_replaced_luminaire + "</td>" +
                                        "<td>" + data.value[i].replacement_luminaire + "</td>" +
                                        "<td>" + data.value[i].replacement_luminaire_power + "</td>" +
                                        "<td>" + data.value[i].power_reduction + "</td>" +
                                        "<td>" + data.value[i].estimated_operating_hours + "</td>" +
                                        "<td>" + data.value[i].total_estimated_savings_kwhs + "</td>" +
                                        "<td>" + data.value[i].veec_discount + "</td>" +
                                        "<td>" + data.value[i].esc_discount + "</td>" +
                                        "<td>" + data.value[i].discount_adjustment + "</td>" +                                        
                                        "<td>" + data.value[i].total_discount + "</td>" +
                                        "<td>" + data.value[i].maintenance_savings + "</td>" +
                                        "<td>" + data.value[i].dollar_per_fixture + "</td>" +
                                        "<td>" + data.value[i].labour_per_hour + "</td>" +
                                        "<td>" + data.value[i].fixtures_per_hour + "</td>" +
                                        "<td>" + data.value[i].total_cost + "</td>" +
                                        "<td>" + data.value[i].led_life_in_months + "</td>" +
                                        "<td>" + data.value[i].existing_lamp_replacement_costs + "</td>" +
                                        "<td>" + data.value[i].existing_luminaire_life_in_months + "</td>" +                                        
                                        "<td>" +
                                        "<a class='btn text-secondary px-0' onclick='editLightingInput(" + data.value[i].id + ")';><i class='far fa-edit fa-lg'></i></a>" +
                                        "<button class='btn d-inline' onclick='deleteLightingInput(" + data.value[i].id + ")';>" +
                                        "<i class='far fa-trash-alt fa-lg text-danger float-right'></i>" +
                                        "</button>" +
                                        "</td>" +
                                        "</tr>"
                                    )

                            }
                        }
                        document.getElementById("tbl_lighting_input_body").innerHTML = table_html
                        deleteErrorMessage("div_lighting_input_error")
                    }
                    else {
                        createErrorMessage("div_lighting_input_error", data.message)
                    }

                }
    }
    request.send(params);
}


function clearLightingInputErrors(){
    deleteErrorMessage("error_lighting_input_lighting_type");
    deleteErrorMessage("error_lighting_input_number_of_existing_luminaire");
    deleteErrorMessage("error_lighting_input_existing_luminaire");
    deleteErrorMessage("error_lighting_input_existing_luminaire_power"); 
    deleteErrorMessage("error_lighting_input_number_of_replaced_luminaire");
    deleteErrorMessage("error_lighting_input_replacement_luminaire");
    deleteErrorMessage("error_lighting_input_replacement_luminaire_power");
    deleteErrorMessage("error_lighting_input_power_reduction");  
    deleteErrorMessage("error_lighting_input_estimated_operating_hours");
    deleteErrorMessage("error_lighting_input_total_estimated_savings_kwhs");
    deleteErrorMessage("error_lighting_input_veec_discount");
    deleteErrorMessage("error_lighting_input_esc_discount");
    deleteErrorMessage("error_lighting_input_discount_adjustment");
    deleteErrorMessage("error_lighting_input_total_discount");
    deleteErrorMessage("error_lighting_input_maintenance_savings");
    deleteErrorMessage("error_lighting_input_dollar_per_fixture");
    deleteErrorMessage("error_lighting_input_labour_per_hour");
    deleteErrorMessage("error_lighting_input_fixtures_per_hour");
    deleteErrorMessage("error_lighting_input_total_cost");
    deleteErrorMessage("error_lighting_input_led_life_in_months");
    deleteErrorMessage("error_lighting_input_existing_lamp_replacement_costs");
    deleteErrorMessage("error_lighting_input_existing_luminaire_life_in_months");
}

function closeLightingInputModal(){
    clearLightingInputModal();
    $('#modal-lighting-inputs').modal("hide");
}

function clearSuggestions(){

}

function clearLightingInputModal(){
    var $LightingInputForm = $('#form_lighting_inputs');
    document.getElementById('modal_hidden_lighting_input').value = "";
    $LightingInputForm[0].reset();
    clearLightingInputErrors();
    clearSuggestions();
}


function deleteLightingInput(lightingInputId){
    var url = '/lighting/delete_lighting_input/'
    var obj = new Object;
    obj.lightingInputId = lightingInputId;

    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var data = JSON.parse(this.responseText);
                    if (data.message == "Success") {
                        showLightingInputs();
                        deleteErrorMessage("div_lighting_input_error")
                        calculateLightingOutputs();
                    }
                    else {
                        createErrorMessage("div_lighting_input_error", data.message)
                    }

                }
    }
    request.send(params);
}

function editLightingInput(lightingInputId){
    var url = '/lighting/edit_lighting_input/'
    var obj = new Object;
    obj.lightingInputId = lightingInputId;

    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    console.log(this.responseText);
                    var data = JSON.parse(this.responseText);
                    if (data.message == "Success") {
                        clearLightingInputModal();
                        $('#modal-lighting-inputs').modal();
                        document.getElementById('modal_hidden_lighting_input').value = data.value.id;
                        document.getElementById("lighting_input_area").value = data.value.area
                        document.getElementById("lighting_input_lighting_type").value = data.value.lighting_type_id
                        document.getElementById("lighting_input_number_of_existing_luminaire").value = data.value.number_of_existing_luminaire                        
                        document.getElementById("lighting_input_existing_luminaire").value = data.value.existing_luminaire_id
                        document.getElementById("lighting_input_existing_luminaire_power").value = data.value.existing_luminaire_power
                        document.getElementById("lighting_input_number_of_replaced_luminaire").value = data.value.number_of_replaced_luminaire
                        document.getElementById("lighting_input_replacement_luminaire").value = data.value.replacement_luminaire_id
                        document.getElementById("lighting_input_replacement_luminaire_power").value = data.value.replacement_luminaire_power
                        document.getElementById("lighting_input_power_reduction").value = data.value.power_reduction
                        document.getElementById("lighting_input_estimated_operating_hours").value = data.value.estimated_operating_hours
                        document.getElementById("lighting_input_total_estimated_savings_kwhs").value = data.value.total_estimated_savings_kwhs
                        document.getElementById("lighting_input_veec_discount").value = data.value.veec_discount
                        document.getElementById("lighting_input_esc_discount").value = data.value.esc_discount
                        document.getElementById("lighting_input_discount_adjustment").value = data.value.discount_adjustment
                        document.getElementById("lighting_input_total_discount").value = data.value.total_discount
                        document.getElementById("lighting_input_maintenance_savings").value = data.value.maintenance_savings
                        document.getElementById("lighting_input_dollar_per_fixture").value = data.value.dollar_per_fixture
                        document.getElementById("lighting_input_labour_per_hour").value = data.value.labour_per_hour
                        document.getElementById("lighting_input_fixtures_per_hour").value = data.value.fixtures_per_hour
                        document.getElementById("lighting_input_total_cost").value = data.value.total_cost
                        document.getElementById("lighting_input_led_life_in_months").value = data.value.led_life_in_months
                        document.getElementById("lighting_input_existing_lamp_replacement_costs").value = data.value.existing_lamp_replacement_costs
                        document.getElementById("lighting_input_existing_luminaire_life_in_months").value = data.value.existing_luminaire_life_in_months 
                                      
                        deleteErrorMessage("div_lighting_input_error");
                        
                    }
                    else{
                        createErrorMessage("div_lighting_input_error", data.message);
                    }
                    

                }
    }
    request.send(params);
}


// --------------------------- Lighting Suggestions ----------------------------------


// Lighting Type Change Function
// document.getElementById("lighting_input_lighting_type").addEventListener("change",lightingTypeChange);

// function lightingTypeChange(){
//     var url = '/lighting/lighting_type_change/'
//     var obj = new Object;
//     obj.scenarioId = document.getElementById("hidden_scenario_id").value;
//     obj.lightingType = document.getElementById("lighting_input_lighting_type").value;
//     var JSONobj = JSON.stringify(obj);
//     params = "JSONobj=" + JSONobj;
//     request = new ajaxRequest()
//     request.open("POST", url, true)
//     request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
//     request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
//     request.setRequestHeader('X-CSRFToken', csrfcookie());
//     request.onreadystatechange = function () {
//         if (this.readyState == 4)
//             if (this.status == 200)
//                 if (this.responseText != null) {                    
//                     var data = JSON.parse(this.responseText);    
//                     console.log(data) ;              
//                     if (data.message == "Success") {
//                         document.getElementById("lighting_input_estimated_operating_hours").value = data.operatingHours;
//                     }
//                     else {
                        
//                     }

//                 }
//     }
//     request.send(params);
// }


// # of existing lights change function
document.getElementById("lighting_input_number_of_existing_luminaire").addEventListener("change",numExistingLuminaireChange);

function numExistingLuminaireChange(){
    document.getElementById("suggestion_lighting_input_number_of_replaced_luminaire").innerHTML = document.getElementById("lighting_input_number_of_existing_luminaire").value
}


// existing lights change function
document.getElementById("lighting_input_existing_luminaire").addEventListener("change",existingLuminaireChange);

function existingLuminaireChange(){
    var url = '/lighting/existing_luminaire_change/'
    var obj = new Object;       
    obj.existingLuminaire = document.getElementById("lighting_input_existing_luminaire").value;
    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {                    
                    var data = JSON.parse(this.responseText);    
                    console.log(data) ;              
                    if (data.message == "Success") {
                        document.getElementById("suggestion_lighting_input_existing_luminaire_power").innerHTML = data.suggestedPower;
                        document.getElementById("suggestion_lighting_input_replacement_luminaire").innerHTML = data.suggestedReplacementLuminaire;                      
                    }
                    else {
                        
                    }

                }
    }
    request.send(params);
}


// replacement lights change function
document.getElementById("lighting_input_replacement_luminaire").addEventListener("change",replacementLuminaireChange);

function replacementLuminaireChange(){
    var url = '/lighting/replacement_luminaire_change/'
    var obj = new Object;
    obj.scenarioId = document.getElementById("hidden_scenario_id").value;
    // obj.lightingType = document.getElementById("lighting_input_lighting_type").value;
    obj.numReplacementLuminaire = document.getElementById("lighting_input_number_of_replaced_luminaire").value;
    obj.replacementLuminaire = document.getElementById("lighting_input_replacement_luminaire").value;
    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {                    
                    var data = JSON.parse(this.responseText);    
                    console.log(data) ;              
                    if (data.message == "Success") {
                        document.getElementById("suggestion_lighting_input_replacement_luminaire_power").innerHTML = data.suggestedReplacementPower;                        
                    }
                    else {
                        
                    }

                }
    }
    request.send(params);
}






// ------------------------------------Lighting Input Calculation --------------------------------

// Trigger for lightingInputCalculation
document.getElementById("lighting_input_number_of_existing_luminaire").addEventListener("change",lightingInputCalculation);
document.getElementById("lighting_input_existing_luminaire_power").addEventListener("change",lightingInputCalculation);
document.getElementById("lighting_input_number_of_replaced_luminaire").addEventListener("change",lightingInputCalculation);
document.getElementById("lighting_input_replacement_luminaire_power").addEventListener("change",lightingInputCalculation);
document.getElementById("lighting_input_discount_adjustment").addEventListener("change",lightingInputCalculation);
document.getElementById("lighting_input_maintenance_savings").addEventListener("change",lightingInputCalculation);
document.getElementById("lighting_input_dollar_per_fixture").addEventListener("change",lightingInputCalculation);
document.getElementById("lighting_input_labour_per_hour").addEventListener("change",lightingInputCalculation);
document.getElementById("lighting_input_fixtures_per_hour").addEventListener("change",lightingInputCalculation);



function lightingInputCalculation(){
    var url = '/lighting/lighting_input_calculation/'
    var obj = new Object;
    obj.scenarioId = document.getElementById("hidden_scenario_id").value;
    obj.lightingType = document.getElementById("lighting_input_lighting_type").value;
    obj.numExistingLuminaire = document.getElementById("lighting_input_number_of_existing_luminaire").value;
    obj.existingLuminaire = document.getElementById("lighting_input_existing_luminaire").value;
    obj.existingLuminairePower = document.getElementById("lighting_input_existing_luminaire_power").value;
    obj.numReplacementLuminaire = document.getElementById("lighting_input_number_of_replaced_luminaire").value;
    obj.replacementLuminaire = document.getElementById("lighting_input_replacement_luminaire").value;
    obj.replacementLuminairePower = document.getElementById("lighting_input_replacement_luminaire_power").value;
    obj.discountAdjustment = document.getElementById("lighting_input_discount_adjustment").value; 
    
    obj.maintenanceSavings = document.getElementById("lighting_input_maintenance_savings").value; 
    obj.dollarPerFixture = document.getElementById("lighting_input_dollar_per_fixture").value; 
    obj.labourPerHour = document.getElementById("lighting_input_labour_per_hour").value; 
    obj.fixturesPerHour = document.getElementById("lighting_input_fixtures_per_hour").value; 

    if (obj.lightingType == "" || obj.numExistingLuminaire == "" || obj.existingLuminaire == "" || obj.existingLuminairePower == "" || obj.numReplacementLuminaire == "" || obj.replacementLuminaire == "" || obj.replacementLuminairePower == "" ){
        return;
    }
    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {                    
                    var data = JSON.parse(this.responseText);    
                    clearLightingInputErrors();
                    console.log(data) ;              
                    if (data.message == "Success") {                        
                        document.getElementById("lighting_input_power_reduction").value = data.powerReduction;
                        document.getElementById("lighting_input_estimated_operating_hours").value = data.operatingHours;
                        document.getElementById("lighting_input_total_estimated_savings_kwhs").value = data.totalEstimatedSavingskWhs;
                        document.getElementById("lighting_input_veec_discount").value = data.veecDiscount;
                        document.getElementById("lighting_input_esc_discount").value = data.escDiscount;
                        document.getElementById("lighting_input_discount_adjustment").value = data.discountAdjustment;
                        document.getElementById("lighting_input_total_discount").value = data.totalDiscount;
                        document.getElementById("lighting_input_maintenance_savings").value = data.maintenanceSavings;
                        document.getElementById("lighting_input_dollar_per_fixture").value = data.dollarPerFixture;
                        document.getElementById("lighting_input_labour_per_hour").value = data.labourPerHour;
                        document.getElementById("lighting_input_fixtures_per_hour").value = data.fixturesPerHour;
                        document.getElementById("lighting_input_total_cost").value = data.totalCost;
                        document.getElementById("lighting_input_led_life_in_months").value = data.replacementLuminaireLife;
                        document.getElementById("lighting_input_existing_lamp_replacement_costs").value = data.existingLampReplacementCost;
                        document.getElementById("lighting_input_existing_luminaire_life_in_months").value = data.existingLuminaireLife;


                                               
                    }
                    else {
                        
                    }

                }
    }
    request.send(params);
}


// -------------------------------------- Lighting Outputs ---------------------------------------

$('#temp_button').click(calculateLightingOutputs);
document.getElementById("lighting_outputs_other_adjustments_1").addEventListener("change",calculateLightingOutputs);
document.getElementById("lighting_outputs_verdia_fee").addEventListener("change",calculateLightingOutputs);
document.getElementById("lighting_outputs_other_adjustments_2").addEventListener("change",calculateLightingOutputs);

function calculateLightingOutputs(){    
    var url = '/lighting/lighting_outputs_calculation/'
    var obj = new Object;
    obj.scenarioId = document.getElementById("hidden_scenario_id").value;
    obj.otherAdjustments1 = document.getElementById("lighting_outputs_other_adjustments_1").value;
    obj.verdiaFee = document.getElementById("lighting_outputs_verdia_fee").value;
    obj.otherAdjustments2 = document.getElementById("lighting_outputs_other_adjustments_2").value;
    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {                    
                    var data = JSON.parse(this.responseText);
                    console.log(data);
                    if (data.message == "Success") {  
                        document.getElementById("lighting_outputs_number_of_lights").value = data.num_lights;
                        document.getElementById("lighting_outputs_maintenance_savings").value = data.maintenance_savings;
                        document.getElementById("lighting_outputs_power_reduction").value = data.power_reduction;
                        document.getElementById("lighting_outputs_total_discount").value = data.total_discounts;
                        document.getElementById("lighting_outputs_installation_cost").value = data.installation_cost;               
                        document.getElementById("lighting_outputs_verdia_fee_dollars").value = data.verdia_fee_dollars;                       
                        document.getElementById("lighting_outputs_total_cost").value = data.total_cost;
                        document.getElementById("lighting_outputs_verdia_fee").value = data.verdia_fee;
                        document.getElementById("lighting_outputs_other_adjustments_1").value = data.other_adjustments_1;
                        document.getElementById("lighting_outputs_other_adjustments_2").value = data.other_adjustments_2;

                        saveLightingOutput();
                    }
                }
    }
    request.send(params);

}




function saveLightingOutput(){
    var url = '/lighting/save_lighting_output/'
    var $LightingOutputForm = $('#form_lighting_outputs');
    var scenarioId = document.getElementById("hidden_scenario_id").value;    
    var $formData = $LightingOutputForm.serialize() + '&scenarioId=' + scenarioId;
    console.log($formData);
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    // request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {                    
                    var data = JSON.parse(this.responseText);
                    console.log(data)
                    if (data.message == "Success") {
                        
                        
                    }                  
                    else {
                        if ((typeof data.message) == "string") {
                            // createErrorMessage("error_lighting_input_lighting_type", data.message)
                        }
                        else {
                            // if ("lighting_type" in data.message) {
                            //     createErrorMessage("error_lighting_input_lighting_type", data.message.lighting_type)
                            // } 
                            
                            
                            
                            
                            
                            
                            
                            
                                                                             
                         
                        }
                    }

                }
    }
    request.send($formData);
}