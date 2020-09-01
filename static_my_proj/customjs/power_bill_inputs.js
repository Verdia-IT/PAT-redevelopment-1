

//------------------------------------ Energy Charges---------------------------------------------------

var $EnergyChargeForm = $('#form_energy_charges');
$EnergyChargeForm.submit(function (event) {
    event.preventDefault();
    saveEnergyCharge();
});
showEnergyCharges();
$(".btn-close-energy-charge-modal").click(closeEnergyChargeModal);

function saveEnergyCharge(){
    var url = '/powerbillinputs/save_energy_charge/'
    var $EnergyChargeForm = $('#form_energy_charges');
    var scenarioId = document.getElementById("hidden_scenario_id").value;
    var energyChargeId = document.getElementById("modal_hidden_energy_charge").value;
    var $formData = $EnergyChargeForm.serialize() + '&scenarioId=' + scenarioId + '&energyChargeId=' + energyChargeId;
    console.log($formData);
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    clearEnergyChargeErrors();
                    var data = JSON.parse(this.responseText);
                    console.log(data)
                    if (data.message == "Success") {
                        closeEnergyChargeModal();
                        showEnergyCharges();
                    }
                    else {
                        if ((typeof data.message) == "string") {
                            alert(data.message);
                        }
                        else {
                            if ("_all_" in data.message) {
                                createErrorMessage("error_energy_charge_tariff_name", data.message.tariff_name)
                            }
                            if ("tariff_name" in data.message) {
                                createErrorMessage("error_energy_charge_tariff_name", data.message.tariff_name)
                            }
                            if ("amount" in data.message) {
                                createErrorMessage("error_energy_charge_amount", data.message.amount)
                            }
                            if ("months" in data.message) {
                                createErrorMessage("error_energy_charge_months", data.message.months)
                            }                            
                         
                        }
                    }

                }
    }
    request.send($formData);
}

function clearEnergyChargeModal(){
    var $EnergyChargeForm = $('#form_energy_charges');
    document.getElementById('modal_hidden_energy_charge').value = "";
    $EnergyChargeForm[0].reset();
    clearEnergyChargeErrors();
}

function clearEnergyChargeErrors(){
    
    deleteErrorMessage("error_energy_charge_tariff_name");    
    deleteErrorMessage("error_energy_charge_amount");    
    deleteErrorMessage("error_energy_charge_months");
 
}

function closeEnergyChargeModal(){
    clearEnergyChargeModal();
    $('#modal-energy-charges').modal("hide");
}

function showEnergyCharges() {
    var url = '/powerbillinputs/show_energy_charges/'
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
                                        "<td>" + data.value[i].tariff_name + "</td>" +
                                        "<td>" + data.value[i].include + "</td>" +
                                        "<td>" + data.value[i].amount + "</td>" +
                                        "<td>" + data.value[i].tariff_type + "</td>" +
                                        "<td>" + data.value[i].weekday_start_time + "</td>" +
                                        "<td>" + data.value[i].weekday_end_time + "</td>" +
                                        "<td>" + data.value[i].weekend_start_time + "</td>" +
                                        "<td>" + data.value[i].weekend_end_time + "</td>" +
                                        "<td>" + data.value[i].months + "</td>" +
                                        "<td>" + data.value[i].category + "</td>" +
                                        "<td>" +
                                        "<a class='btn text-secondary px-0' onclick='editEnergyCharge(" + data.value[i].id + ")';><i class='far fa-edit fa-lg'></i></a>" +
                                        "<button class='btn d-inline' onclick='deleteEnergyCharge(" + data.value[i].id + ")';>" +
                                        "<i class='far fa-trash-alt fa-lg text-danger float-right'></i>" +
                                        "</button>" +
                                        "</td>" +
                                        "</tr>"
                                    )

                            }
                        }
                        document.getElementById("tbl_energy_charge_body").innerHTML = table_html
                        deleteErrorMessage("div_energy_charges_error")
                    }
                    else {
                        createErrorMessage("div_energy_charges_error", data.message)
                    }

                }
    }
    request.send(params);
}

function deleteEnergyCharge(energyChargeId){
    var url = '/powerbillinputs/delete_energy_charge/'
    var obj = new Object;
    obj.energyChargeId = energyChargeId;

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
                        showEnergyCharges();
                        deleteErrorMessage("div_energy_charges_error")
                    }
                    else {
                        createErrorMessage("div_energy_charges_error", data.message)
                    }

                }
    }
    request.send(params);
}

function editEnergyCharge(energyChargeId){
    var url = '/powerbillinputs/edit_energy_charge/'
    var obj = new Object;
    obj.energyChargeId = energyChargeId;

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
                        $('#modal-energy-charges').modal();
                        document.getElementById('modal_hidden_energy_charge').value = data.value.id;
                        document.getElementById("energy_charge_tariff_name").value = data.value['tariff_name'];
                        document.getElementById("energy_charge_include").value = data.value['include'];
                        document.getElementById("energy_charge_amount").value = data.value['amount'];
                        document.getElementById("energy_charge_tariff_type").value = data.value['tariff_type'];
                        document.getElementById("energy_charge_weekday_start_time").value = data.value['weekday_start_time'];
                        document.getElementById("energy_charge_weekday_end_time").value = data.value['weekday_end_time'];
                        document.getElementById("energy_charge_weekend_start_time").value = data.value['weekend_start_time'];
                        document.getElementById("energy_charge_weekend_end_time").value = data.value['weekend_end_time'];
                        document.getElementById("energy_charge_months").value = data.value['months'];
                        document.getElementById("energy_charge_category").value = data.value['category'];
                        

                        deleteErrorMessage("div_energy_charges_error")
                    }
                    else {
                        createErrorMessage("div_energy_charges_error", data.message)
                    }

                }
    }
    request.send(params);
}


//------------------------------------ Demand Charges ---------------------------------------------------

var $DemandChargeForm = $('#form_demand_charges');
$DemandChargeForm.submit(function (event) {
    event.preventDefault();
    saveDemandCharge();
});
showDemandCharges();
$(".btn-close-demand-charge-modal").click(closeDemandChargeModal);

function saveDemandCharge(){
    var url = '/powerbillinputs/save_demand_charge/'
    var $DemandChargeForm = $('#form_demand_charges');
    var scenarioId = document.getElementById("hidden_scenario_id").value;
    var demandChargeId = document.getElementById("modal_hidden_demand_charge").value;
    var $formData = $DemandChargeForm.serialize() + '&scenarioId=' + scenarioId + '&demandChargeId=' + demandChargeId;
    console.log($formData);
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    clearDemandChargeErrors();
                    var data = JSON.parse(this.responseText);
                    console.log(data)
                    if (data.message == "Success") {
                        closeDemandChargeModal();
                        showDemandCharges();
                    }
                    else {
                        if ((typeof data.message) == "string") {
                            alert(data.message);
                        }
                        else {
                            
                            if ("tariff_name" in data.message) {
                                createErrorMessage("error_demand_charge_tariff_name", data.message.tariff_name)
                            }
                            if ("chargeable_power" in data.message) {
                                createErrorMessage("error_demand_charge_chargeable_power", data.message.chargeable_power)
                            }
                            if ("amount" in data.message) {
                                createErrorMessage("error_demand_charge_amount", data.message.amount)
                            }
                            if ("months" in data.message) {
                                createErrorMessage("error_demand_charge_months", data.message.months)
                            } 
                            if ("threshold" in data.message) {
                                createErrorMessage("error_demand_charge_threshold", data.message.threshold)
                            }                            
                         
                        }
                    }

                }
    }
    request.send($formData);
}

function clearDemandChargeModal(){
    var $DemandChargeForm = $('#form_demand_charges');
    document.getElementById('modal_hidden_demand_charge').value = "";
    $DemandChargeForm[0].reset();
    clearDemandChargeErrors();
}

function clearDemandChargeErrors(){
    
    deleteErrorMessage("error_demand_charge_tariff_name");
    deleteErrorMessage("error_demand_charge_chargeable_power");  
    deleteErrorMessage("error_demand_charge_amount");    
    deleteErrorMessage("error_demand_charge_months");
    deleteErrorMessage("error_demand_charge_threshold");
 
}

function closeDemandChargeModal(){
    clearDemandChargeModal();
    $('#modal-demand-charges').modal("hide");
}

function showDemandCharges() {
    var url = '/powerbillinputs/show_demand_charges/'
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
                                        "<td>" + data.value[i].tariff_name + "</td>" +
                                        "<td>" + data.value[i].include + "</td>" +
                                        "<td>" + data.value[i].chargeable_power + "</td>" +
                                        "<td>" + data.value[i].amount + "</td>" +
                                        "<td>" + data.value[i].tariff_type + "</td>" +
                                        "<td>" + data.value[i].weekday_start_time + "</td>" +
                                        "<td>" + data.value[i].weekday_end_time + "</td>" +
                                        "<td>" + data.value[i].weekend_start_time + "</td>" +
                                        "<td>" + data.value[i].weekend_end_time + "</td>" +
                                        "<td>" + data.value[i].chargeable_power_type + "</td>" +
                                        "<td>" + data.value[i].months + "</td>" +
                                        "<td>" + data.value[i].threshold + "</td>" +
                                        "<td>" + data.value[i].category + "</td>" +
                                        "<td>" +
                                        "<a class='btn text-secondary px-0' onclick='editDemandCharge(" + data.value[i].id + ")';><i class='far fa-edit fa-lg'></i></a>" +
                                        "<button class='btn d-inline' onclick='deleteDemandCharge(" + data.value[i].id + ")';>" +
                                        "<i class='far fa-trash-alt fa-lg text-danger float-right'></i>" +
                                        "</button>" +
                                        "</td>" +
                                        "</tr>"
                                    )

                            }
                        }
                        document.getElementById("tbl_demand_charge_body").innerHTML = table_html
                        deleteErrorMessage("div_demand_charges_error")
                    }
                    else {
                        createErrorMessage("div_demand_charges_error", data.message)
                    }

                }
    }
    request.send(params);
}

function deleteDemandCharge(demandChargeId){
    var url = '/powerbillinputs/delete_demand_charge/'
    var obj = new Object;
    obj.demandChargeId = demandChargeId;

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
                        showDemandCharges();
                        deleteErrorMessage("div_demand_charges_error")
                    }
                    else {
                        createErrorMessage("div_demand_charges_error", data.message)
                    }

                }
    }
    request.send(params);
}

function editDemandCharge(demandChargeId){
    var url = '/powerbillinputs/edit_demand_charge/'
    var obj = new Object;
    obj.demandChargeId = demandChargeId;

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
                        $('#modal-demand-charges').modal();
                        document.getElementById('modal_hidden_demand_charge').value = data.value.id;
                        document.getElementById("demand_charge_tariff_name").value = data.value['tariff_name'];
                        document.getElementById("demand_charge_include").value = data.value['include'];
                        document.getElementById("demand_charge_chargeable_power").value = data.value['chargeable_power'];
                        document.getElementById("demand_charge_amount").value = data.value['amount'];
                        document.getElementById("demand_charge_tariff_type").value = data.value['tariff_type'];
                        document.getElementById("demand_charge_weekday_start_time").value = data.value['weekday_start_time'];
                        document.getElementById("demand_charge_weekday_end_time").value = data.value['weekday_end_time'];
                        document.getElementById("demand_charge_weekend_start_time").value = data.value['weekend_start_time'];
                        document.getElementById("demand_charge_weekend_end_time").value = data.value['weekend_end_time'];
                        document.getElementById("demand_charge_chargeable_power_type").value = data.value['chargeable_power_type'];
                        document.getElementById("demand_charge_months").value = data.value['months'];
                        document.getElementById("demand_charge_threshold").value = data.value['threshold'];
                        document.getElementById("demand_charge_category").value = data.value['category'];                        

                        deleteErrorMessage("div_demand_charges_error")
                    }
                    else {
                        createErrorMessage("div_demand_charges_error", data.message)
                    }

                }
    }
    request.send(params);
}



//------------------------------------ Fixed Charges ---------------------------------------------------

var $FixedChargeForm = $('#form_fixed_charges');
$FixedChargeForm.submit(function (event) {
    event.preventDefault();
    saveFixedCharge();
});
showFixedCharges();
$(".btn-close-fixed-charge-modal").click(closeFixedChargeModal);

function saveFixedCharge(){
    var url = '/powerbillinputs/save_fixed_charge/'
    var $FixedChargeForm = $('#form_fixed_charges');
    var scenarioId = document.getElementById("hidden_scenario_id").value;
    var fixedChargeId = document.getElementById("modal_hidden_fixed_charge").value;
    var $formData = $FixedChargeForm.serialize() + '&scenarioId=' + scenarioId + '&fixedChargeId=' + fixedChargeId;
    console.log($formData);
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    clearFixedChargeErrors();
                    var data = JSON.parse(this.responseText);
                    console.log(data)
                    if (data.message == "Success") {
                        closeFixedChargeModal();
                        showFixedCharges();
                    }
                    else {
                        if ((typeof data.message) == "string") {
                            alert(data.message);
                        }
                        else {
                            
                            if ("tariff_name" in data.message) {
                                createErrorMessage("error_fixed_charge_tariff_name", data.message.tariff_name)
                            }                            
                            if ("amount" in data.message) {
                                createErrorMessage("error_fixed_charge_amount", data.message.amount)
                            }                                                   
                         
                        }
                    }

                }
    }
    request.send($formData);
}

function clearFixedChargeModal(){
    var $FixedChargeForm = $('#form_fixed_charges');
    document.getElementById('modal_hidden_fixed_charge').value = "";
    $FixedChargeForm[0].reset();
    clearFixedChargeErrors();
}

function clearFixedChargeErrors(){
    
    deleteErrorMessage("error_fixed_charge_tariff_name");   
    deleteErrorMessage("error_fixed_charge_amount");    
 
}

function closeFixedChargeModal(){
    clearFixedChargeModal();
    $('#modal-fixed-charges').modal("hide");
}

function showFixedCharges() {
    var url = '/powerbillinputs/show_fixed_charges/'
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
                                        "<td>" + data.value[i].tariff_name + "</td>" +
                                        "<td>" + data.value[i].include + "</td>" +                                       
                                        "<td>" + data.value[i].amount + "</td>" +
                                        "<td>" + data.value[i].frequency + "</td>" +                                       
                                        "<td>" + data.value[i].category + "</td>" +
                                        "<td>" +
                                        "<a class='btn text-secondary px-0' onclick='editFixedCharge(" + data.value[i].id + ")';><i class='far fa-edit fa-lg'></i></a>" +
                                        "<button class='btn d-inline' onclick='deleteFixedCharge(" + data.value[i].id + ")';>" +
                                        "<i class='far fa-trash-alt fa-lg text-danger float-right'></i>" +
                                        "</button>" +
                                        "</td>" +
                                        "</tr>"
                                    )

                            }
                        }
                        document.getElementById("tbl_fixed_charge_body").innerHTML = table_html
                        deleteErrorMessage("div_fixed_charges_error")
                    }
                    else {
                        createErrorMessage("div_fixed_charges_error", data.message)
                    }

                }
    }
    request.send(params);
}

function deleteFixedCharge(fixedChargeId){
    var url = '/powerbillinputs/delete_fixed_charge/'
    var obj = new Object;
    obj.fixedChargeId = fixedChargeId;

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
                        showFixedCharges();
                        deleteErrorMessage("div_fixed_charges_error")
                    }
                    else {
                        createErrorMessage("div_fixed_charges_error", data.message)
                    }

                }
    }
    request.send(params);
}

function editFixedCharge(fixedChargeId){
    var url = '/powerbillinputs/edit_fixed_charge/'
    var obj = new Object;
    obj.fixedChargeId = fixedChargeId;

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
                        $('#modal-fixed-charges').modal();
                        document.getElementById('modal_hidden_fixed_charge').value = data.value.id;
                        document.getElementById("fixed_charge_tariff_name").value = data.value['tariff_name'];
                        document.getElementById("fixed_charge_include").value = data.value['include']; 
                        document.getElementById("fixed_charge_amount").value = data.value['amount'];
                        document.getElementById("fixed_charge_frequency").value = data.value['frequency'];                      
                        document.getElementById("fixed_charge_category").value = data.value['category'];
                        deleteErrorMessage("div_fixed_charges_error")
                    }
                    else {
                        createErrorMessage("div_fixed_charges_error", data.message)
                    }

                }
    }
    request.send(params);
}
