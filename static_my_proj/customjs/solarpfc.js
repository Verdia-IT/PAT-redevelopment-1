
// solarCostSuggestion();
calculateSolarPrice();
// document.getElementById("solar_price_solar_size").addEventListener("change",calculateSolarPrice);
document.getElementById("solar_price_solar_unit_cost_override").addEventListener("change",calculateSolarPrice);
document.getElementById("solar_price_system_type_override").addEventListener("change",calculateSolarPrice);
document.getElementById("solar_price_verdia_fee").addEventListener("change",calculateSolarPrice);
document.getElementById("solar_price_other_adjustments_1").addEventListener("change",calculateSolarPrice);
document.getElementById("solar_price_other_adjustments_2").addEventListener("change",calculateSolarPrice);
document.getElementById("solar_price_include_solar_maintenance").addEventListener("change",calculateSolarPrice);
document.getElementById("solar_price_stc_deeming_period").addEventListener("change",calculateSolarPrice);


function calculateSolarPrice(){
    var url = '/solarpfc/solar_price_calculation/'
    var obj = new Object;
    obj.scenarioId = document.getElementById("hidden_scenario_id").value;
    obj.solarSize = document.getElementById("solar_price_solar_size").value;
    obj.solarUnitCost = document.getElementById("solar_price_solar_unit_cost").value;
    obj.solarUnitCostOverride = document.getElementById("solar_price_solar_unit_cost_override").value;
    obj.otherAdjustments1 = document.getElementById("solar_price_other_adjustments_1").value;
    obj.verdiaFee = document.getElementById("solar_price_verdia_fee").value;
    obj.otherAdjustments2 = document.getElementById("solar_price_other_adjustments_2").value;
    obj.systemType = document.getElementById("solar_price_system_type").value;
    obj.systemTypeOverride = document.getElementById("solar_price_system_type_override").value;
    obj.stcDeemingPeriod = document.getElementById("solar_price_stc_deeming_period").value;
    obj.includeSolarMaintenance = document.getElementById("solar_price_include_solar_maintenance").value;
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
                        document.getElementById("solar_price_solar_size").value = data.solar_size
                        document.getElementById("solar_price_solar_unit_cost").value = data.solar_unit_cost
                        document.getElementById("solar_price_solar_unit_cost_override").value = data.solar_unit_cost_override
                        document.getElementById("solar_price_gross_system_cost").value = data.gross_system_cost
                        document.getElementById("solar_price_other_adjustments_1").value = data.other_adjustments_1
                        document.getElementById("solar_price_verdia_fee").value = data.verdia_fee
                        document.getElementById("solar_price_verdia_fee_dollars").value = data.verdia_fee_dollars
                        document.getElementById("solar_price_other_adjustments_2").value = data.other_adjustments_2
                        document.getElementById("solar_price_system_type").value = data.system_type
                        document.getElementById("solar_price_system_type_override").value = data.system_type_override
                        document.getElementById("solar_price_stc_deeming_period").value = data.stc_deeming_period
                        document.getElementById("solar_price_stc_discount").value = data.stc_discount
                        document.getElementById("solar_price_system_cost").value = data.system_cost
                        document.getElementById("solar_price_system_unit_cost").value = data.system_unit_cost
                        document.getElementById("solar_price_maintenance_cost_per_annum").value = data.maintenance_cost_per_annum
                        document.getElementById("solar_price_include_solar_maintenance").value = data.include_solar_maintenance
                        saveSolarPrice();
                    }
                }
    }
    request.send(params);

}


function saveSolarPrice(){
    var url = '/solarpfc/save_solar_price/'
    var $SolarPriceForm = $('#form_solar_price');
    var scenarioId = document.getElementById("hidden_scenario_id").value;    
    var $formData = $SolarPriceForm.serialize() + '&scenarioId=' + scenarioId;
    // console.log($formData);
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


//--------------------------------------------------------- Suggestions ------------------------------------------


// function solarCostSuggestion(){    
//     // deeming period calculation
//     var d = new Date();    
//     document.getElementById("solar_costs_stc_deeming_period").value = 2030 + 1 - d.getFullYear();
//     // System Type Override
//     if (document.getElementById("solar_costs_system_type_override").value == "No Override"){
//         if (document.getElementById("solar_costs_solar_size").value > 100){
//             document.getElementById("solar_costs_system_type").value = "LGC"
//         }
//         else{
//             document.getElementById("solar_costs_system_type").value = "STC"
//         }
//     }
//     else{
//         document.getElementById("solar_costs_system_type").value = "LGC"
//     }
//     // solar cost override
//     solarUnitCostOverride = document.getElementById("solar_costs_solar_unit_cost_override").value
//     if (solarUnitCostOverride != ""){
//         document.getElementById("solar_costs_solar_unit_cost").value = solarUnitCostOverride
//         calculateSolarCosts();
//     }
//     else{
//         calculateSolarUnitCost();
//     }
    
// }

// function calculateSolarUnitCost(){
//     var url = '/solarpfc/solar_unit_cost_calculation/'
//     var obj = new Object;
//     obj.scenarioId = document.getElementById("hidden_scenario_id").value;
//     obj.solarSize = document.getElementById("solar_costs_solar_size").value;    
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
//                     console.log(data);
//                     if (data.message == "Success") {  
//                         document.getElementById("solar_costs_solar_unit_cost").value = data.solar_unit_cost
//                         calculateSolarCosts();
                        
//                     }
//                 }
//     }
//     request.send(params);
// }




// ----------------------------------Solar Layout -----------------------------------------------------------


// Image browse and display

document.getElementById("solar_layout_form_solar_layout_file").addEventListener("change", function () {
    displaySolarLayout();
});

$(document).on('click', '.browse', function () {
    var file = $(this).parent().parent().parent().find('.file1');
    file.trigger('click');
});
$(document).on('change', '.file1', function () {
    $(this).parent().find('.form-control').val($(this).val().replace(/C:\\fakepath\\/i, ''));
});


function displaySolarLayout() {

    var fileSelect = document.getElementById('solar_layout_form_solar_layout_file');
    var files = fileSelect.files;
    var file = files[0];
    document.getElementById("solar-layout-display-div").innerHTML = "";
    document.getElementById("solar-layout-display-div").innerHTML = "<img src='" + URL.createObjectURL(file) + "' alt='No Image Found' style='max-width:100%; height:auto; '> ";
}

var $SolarLayoutForm = $('#form_solar_layout_upload');
$SolarLayoutForm.submit(function (event) {
    event.preventDefault();
    uploadSolarLayout();
});

function uploadSolarLayout(){
    var url = '/solarpfc/solar_layout_upload/'
    var formData = new FormData(document.getElementById("form_solar_layout_upload"));
    var scenarioId = document.getElementById("hidden_scenario_id").value;    
    var obj = new Object();
    obj.scenarioId = scenarioId
    var JSONobj = JSON.stringify(obj);
    formData.append('JSONobj', JSONobj);
    request = new ajaxRequest()
    request.open("POST", url, true)
    // request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var data = JSON.parse(this.responseText);
                    console.log(data.message)                  

                }
    }
    request.send(formData);
}



// ------------------------------PFC Costs -------------------------------------

// solarCostSuggestion();
calculatePFCPrice();
document.getElementById("pfc_price_pfc_unit_cost_override").addEventListener("change",calculatePFCPrice);
document.getElementById("pfc_price_verdia_fee").addEventListener("change",calculatePFCPrice);



function calculatePFCPrice(){
    var url = '/solarpfc/pfc_price_calculation/'
    var obj = new Object;
    obj.scenarioId = document.getElementById("hidden_scenario_id").value;
    obj.pfcSize = document.getElementById("pfc_price_pfc_size").value;
    obj.pfcUnitCost = document.getElementById("pfc_price_pfc_unit_cost").value;
    obj.pfcUnitCostOverride = document.getElementById("pfc_price_pfc_unit_cost_override").value;
    obj.verdiaFee = document.getElementById("pfc_price_verdia_fee").value;
    
    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var data = JSON.parse(this.responseText);
                    console.log(data)     
                    document.getElementById("pfc_price_pfc_size").value = data.pfc_size
                    document.getElementById("pfc_price_pfc_unit_cost").value = data.pfc_unit_cost
                    document.getElementById("pfc_price_pfc_unit_cost_override").value = data.pfc_unit_cost_override
                    document.getElementById("pfc_price_gross_system_cost").value = data.gross_system_cost
                    document.getElementById("pfc_price_verdia_fee").value = data.verdia_fee
                    document.getElementById("pfc_price_verdia_fee_dollars").value = data.verdia_fee_dollars
                    document.getElementById("pfc_price_system_cost").value = data.system_cost 
                    document.getElementById("pfc_price_system_unit_cost").value = data.system_unit_cost             
                    savePFCPrice();

                }
    }
    request.send(params);
}


function savePFCPrice(){
    var url = '/solarpfc/save_pfc_price/'
    var $PFCPriceForm = $('#form_pfc_price');
    var scenarioId = document.getElementById("hidden_scenario_id").value;    
    var $formData = $PFCPriceForm.serialize() + '&scenarioId=' + scenarioId;
    // console.log($formData);
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