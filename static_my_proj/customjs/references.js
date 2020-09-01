

$(document).ready(function () {
    $("#btn-save-certificate-prices").click(saveCertificatePrices);
    $("#btn-save-tariff-escalations").click(saveTariffEscalations);
    $("#btn-save-peak-energy-rates").click(savePeakEnergyRates);
    $("#btn-save-offpeak-energy-rates").click(saveOffpeakEnergyRates);
    $("#btn-save-led").click(saveLED);
    $("#btn-save-existing").click(saveExisting);
    $("#btn-download-data").click(downloadData);
    var $SolarForm = $('#modal-form-solar-cost');
    $SolarForm.submit(function (event) {
        event.preventDefault();
        saveSolarCost();
    });
    $(".btn-close-solar-cost").click(closeSolarCost);
    $(".btn-close-pfc-cost").click(closePFCCost);

    var $PFCForm = $('#modal-form-pfc-cost');
    $PFCForm.submit(function (event) {
        event.preventDefault();
        savePFCCost();
    });
    showLedDatabase();
    showExistingDatabase();
    fillExistingLedReplacement();
    showSolarCost();
    showPFCCost();

})

// ---------------------------------------------Resource download ------------------------------------------------------------

function downloadData(){
    // alert("button clicked");
    var url = '/references/download_data/'
    var obj = new Object;
    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var data = JSON.parse(this.responseText);           
                    console.log(data);
                }
    }
    request.send(params);
}

//  --------------------------------------------- Renewable Certificates ---------------------------------------------------------

function saveCertificatePrices() {
    var url = '/references/save_certificate/'
    var obj = new Object;
    obj.stcPrice = document.getElementById("STC_price").value;
    obj.veecPrice = document.getElementById("VEEC_price").value;
    obj.escPrice = document.getElementById("ESC_price").value;
    obj.lgcPrice2019 = document.getElementById("LGC_price_2019").value;
    obj.lgcPrice2020 = document.getElementById("LGC_price_2020").value;
    obj.lgcPrice2021 = document.getElementById("LGC_price_2021").value;
    obj.lgcPrice2022 = document.getElementById("LGC_price_2022").value;
    obj.lgcPrice2023 = document.getElementById("LGC_price_2023").value;
    obj.lgcPrice2024 = document.getElementById("LGC_price_2024").value;
    obj.lgcPrice2025 = document.getElementById("LGC_price_2025").value;
    obj.lgcPrice2026 = document.getElementById("LGC_price_2026").value;
    obj.lgcPrice2027 = document.getElementById("LGC_price_2027").value;
    obj.lgcPrice2028 = document.getElementById("LGC_price_2028").value;
    obj.lgcPrice2029 = document.getElementById("LGC_price_2029").value;
    obj.lgcPrice2030 = document.getElementById("LGC_price_2030").value;

    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var data = JSON.parse(this.responseText);

                    // put values in respective places

                    document.getElementById("STC_price").value = data[0].STCprice;
                    document.getElementById("VEEC_price").value = data[0].VEECprice;
                    document.getElementById("ESC_price").value = data[0].ESCprice;
                    document.getElementById("LGC_price_2019").value = data[0].LGCprice2019;
                    document.getElementById("LGC_price_2020").value = data[0].LGCprice2020;
                    document.getElementById("LGC_price_2021").value = data[0].LGCprice2021;
                    document.getElementById("LGC_price_2022").value = data[0].LGCprice2022;
                    document.getElementById("LGC_price_2023").value = data[0].LGCprice2023;
                    document.getElementById("LGC_price_2024").value = data[0].LGCprice2024;
                    document.getElementById("LGC_price_2025").value = data[0].LGCprice2025;
                    document.getElementById("LGC_price_2026").value = data[0].LGCprice2026;
                    document.getElementById("LGC_price_2027").value = data[0].LGCprice2027;
                    document.getElementById("LGC_price_2028").value = data[0].LGCprice2028;
                    document.getElementById("LGC_price_2029").value = data[0].LGCprice2029;
                    document.getElementById("LGC_price_2030").value = data[0].LGCprice2030;

                }
    }
    request.send(params);
}

//  --------------------------------------------- Energy Rates and Escalations ---------------------------------------------------------

function saveTariffEscalations() {

    var url = '/references/save_tariff_escalations/'
    var obj = new Object;
    obj.qld2019 = document.getElementById("esc_2019_qld").value;
    obj.nsw2019 = document.getElementById("esc_2019_nsw").value;
    obj.vic2019 = document.getElementById("esc_2019_vic").value;
    obj.sa2019 = document.getElementById("esc_2019_sa").value;
    obj.wa2019 = document.getElementById("esc_2019_wa").value;
    obj.act2019 = document.getElementById("esc_2019_act").value;
    obj.tas2019 = document.getElementById("esc_2019_tas").value;
    obj.nt2019 = document.getElementById("esc_2019_nt").value;
    obj.qld2020 = document.getElementById("esc_2020_qld").value;
    obj.nsw2020 = document.getElementById("esc_2020_nsw").value;
    obj.vic2020 = document.getElementById("esc_2020_vic").value;
    obj.sa2020 = document.getElementById("esc_2020_sa").value;
    obj.wa2020 = document.getElementById("esc_2020_wa").value;
    obj.act2020 = document.getElementById("esc_2020_act").value;
    obj.tas2020 = document.getElementById("esc_2020_tas").value;
    obj.nt2020 = document.getElementById("esc_2020_nt").value;
    obj.qld2021 = document.getElementById("esc_2021_qld").value;
    obj.nsw2021 = document.getElementById("esc_2021_nsw").value;
    obj.vic2021 = document.getElementById("esc_2021_vic").value;
    obj.sa2021 = document.getElementById("esc_2021_sa").value;
    obj.wa2021 = document.getElementById("esc_2021_wa").value;
    obj.act2021 = document.getElementById("esc_2021_act").value;
    obj.tas2021 = document.getElementById("esc_2021_tas").value;
    obj.nt2021 = document.getElementById("esc_2021_nt").value;
    obj.qld2022 = document.getElementById("esc_2022_qld").value;
    obj.nsw2022 = document.getElementById("esc_2022_nsw").value;
    obj.vic2022 = document.getElementById("esc_2022_vic").value;
    obj.sa2022 = document.getElementById("esc_2022_sa").value;
    obj.wa2022 = document.getElementById("esc_2022_wa").value;
    obj.act2022 = document.getElementById("esc_2022_act").value;
    obj.tas2022 = document.getElementById("esc_2022_tas").value;
    obj.nt2022 = document.getElementById("esc_2022_nt").value;
    obj.qld2023 = document.getElementById("esc_2023_qld").value;
    obj.nsw2023 = document.getElementById("esc_2023_nsw").value;
    obj.vic2023 = document.getElementById("esc_2023_vic").value;
    obj.sa2023 = document.getElementById("esc_2023_sa").value;
    obj.wa2023 = document.getElementById("esc_2023_wa").value;
    obj.act2023 = document.getElementById("esc_2023_act").value;
    obj.tas2023 = document.getElementById("esc_2023_tas").value;
    obj.nt2023 = document.getElementById("esc_2023_nt").value;
    obj.qld2024 = document.getElementById("esc_2024_qld").value;
    obj.nsw2024 = document.getElementById("esc_2024_nsw").value;
    obj.vic2024 = document.getElementById("esc_2024_vic").value;
    obj.sa2024 = document.getElementById("esc_2024_sa").value;
    obj.wa2024 = document.getElementById("esc_2024_wa").value;
    obj.act2024 = document.getElementById("esc_2024_act").value;
    obj.tas2024 = document.getElementById("esc_2024_tas").value;
    obj.nt2024 = document.getElementById("esc_2024_nt").value;
    obj.qld2025 = document.getElementById("esc_2025_qld").value;
    obj.nsw2025 = document.getElementById("esc_2025_nsw").value;
    obj.vic2025 = document.getElementById("esc_2025_vic").value;
    obj.sa2025 = document.getElementById("esc_2025_sa").value;
    obj.wa2025 = document.getElementById("esc_2025_wa").value;
    obj.act2025 = document.getElementById("esc_2025_act").value;
    obj.tas2025 = document.getElementById("esc_2025_tas").value;
    obj.nt2025 = document.getElementById("esc_2025_nt").value;
    obj.qld2026 = document.getElementById("esc_2026_qld").value;
    obj.nsw2026 = document.getElementById("esc_2026_nsw").value;
    obj.vic2026 = document.getElementById("esc_2026_vic").value;
    obj.sa2026 = document.getElementById("esc_2026_sa").value;
    obj.wa2026 = document.getElementById("esc_2026_wa").value;
    obj.act2026 = document.getElementById("esc_2026_act").value;
    obj.tas2026 = document.getElementById("esc_2026_tas").value;
    obj.nt2026 = document.getElementById("esc_2026_nt").value;
    obj.qld2027 = document.getElementById("esc_2027_qld").value;
    obj.nsw2027 = document.getElementById("esc_2027_nsw").value;
    obj.vic2027 = document.getElementById("esc_2027_vic").value;
    obj.sa2027 = document.getElementById("esc_2027_sa").value;
    obj.wa2027 = document.getElementById("esc_2027_wa").value;
    obj.act2027 = document.getElementById("esc_2027_act").value;
    obj.tas2027 = document.getElementById("esc_2027_tas").value;
    obj.nt2027 = document.getElementById("esc_2027_nt").value;




    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var data = JSON.parse(this.responseText);

                    // put values in respective places
                    for (i = 0; i < data.length; i++) {
                        document.getElementById("esc_" + data[i].year + "_qld").value = data[i].queensland;
                        document.getElementById("esc_" + data[i].year + "_nsw").value = data[i].new_south_wales;
                        document.getElementById("esc_" + data[i].year + "_vic").value = data[i].victoria;
                        document.getElementById("esc_" + data[i].year + "_sa").value = data[i].south_australia;
                        document.getElementById("esc_" + data[i].year + "_wa").value = data[i].western_australia;
                        document.getElementById("esc_" + data[i].year + "_act").value = data[i].australian_capital_territory;
                        document.getElementById("esc_" + data[i].year + "_tas").value = data[i].tasmania;
                        document.getElementById("esc_" + data[i].year + "_nt").value = data[i].northern_territory;
                    }

                }
    }
    request.send(params);
}

function savePeakEnergyRates() {

    var url = '/references/save_peak_energy_rates/'
    var obj = new Object;
    obj.qld2020 = document.getElementById("per_2020_qld").value;
    obj.nsw2020 = document.getElementById("per_2020_nsw").value;
    obj.vic2020 = document.getElementById("per_2020_vic").value;
    obj.sa2020 = document.getElementById("per_2020_sa").value;
    obj.wa2020 = document.getElementById("per_2020_wa").value;
    obj.act2020 = document.getElementById("per_2020_act").value;
    obj.tas2020 = document.getElementById("per_2020_tas").value;
    obj.nt2020 = document.getElementById("per_2020_nt").value;
    obj.qld2021 = document.getElementById("per_2021_qld").value;
    obj.nsw2021 = document.getElementById("per_2021_nsw").value;
    obj.vic2021 = document.getElementById("per_2021_vic").value;
    obj.sa2021 = document.getElementById("per_2021_sa").value;
    obj.wa2021 = document.getElementById("per_2021_wa").value;
    obj.act2021 = document.getElementById("per_2021_act").value;
    obj.tas2021 = document.getElementById("per_2021_tas").value;
    obj.nt2021 = document.getElementById("per_2021_nt").value;
    obj.qld2022 = document.getElementById("per_2022_qld").value;
    obj.nsw2022 = document.getElementById("per_2022_nsw").value;
    obj.vic2022 = document.getElementById("per_2022_vic").value;
    obj.sa2022 = document.getElementById("per_2022_sa").value;
    obj.wa2022 = document.getElementById("per_2022_wa").value;
    obj.act2022 = document.getElementById("per_2022_act").value;
    obj.tas2022 = document.getElementById("per_2022_tas").value;
    obj.nt2022 = document.getElementById("per_2022_nt").value;


    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var data = JSON.parse(this.responseText);
                    // alert(this.responseText);
                    // put values in respective places
                    for (i = 0; i < data.length; i++) {
                        document.getElementById("per_" + data[i].year + "_qld").value = data[i].queensland;
                        document.getElementById("per_" + data[i].year + "_nsw").value = data[i].new_south_wales;
                        document.getElementById("per_" + data[i].year + "_vic").value = data[i].victoria;
                        document.getElementById("per_" + data[i].year + "_sa").value = data[i].south_australia;
                        document.getElementById("per_" + data[i].year + "_wa").value = data[i].western_australia;
                        document.getElementById("per_" + data[i].year + "_act").value = data[i].australian_capital_territory;
                        document.getElementById("per_" + data[i].year + "_tas").value = data[i].tasmania;
                        document.getElementById("per_" + data[i].year + "_nt").value = data[i].northern_territory;
                    }

                }
    }
    request.send(params);
}

function saveOffpeakEnergyRates() {
    var url = '/references/save_offpeak_energy_rates/'
    var obj = new Object;
    obj.qld2020 = document.getElementById("oer_2020_qld").value;
    obj.nsw2020 = document.getElementById("oer_2020_nsw").value;
    obj.vic2020 = document.getElementById("oer_2020_vic").value;
    obj.sa2020 = document.getElementById("oer_2020_sa").value;
    obj.wa2020 = document.getElementById("oer_2020_wa").value;
    obj.act2020 = document.getElementById("oer_2020_act").value;
    obj.tas2020 = document.getElementById("oer_2020_tas").value;
    obj.nt2020 = document.getElementById("oer_2020_nt").value;
    obj.qld2021 = document.getElementById("oer_2021_qld").value;
    obj.nsw2021 = document.getElementById("oer_2021_nsw").value;
    obj.vic2021 = document.getElementById("oer_2021_vic").value;
    obj.sa2021 = document.getElementById("oer_2021_sa").value;
    obj.wa2021 = document.getElementById("oer_2021_wa").value;
    obj.act2021 = document.getElementById("oer_2021_act").value;
    obj.tas2021 = document.getElementById("oer_2021_tas").value;
    obj.nt2021 = document.getElementById("oer_2021_nt").value;
    obj.qld2022 = document.getElementById("oer_2022_qld").value;
    obj.nsw2022 = document.getElementById("oer_2022_nsw").value;
    obj.vic2022 = document.getElementById("oer_2022_vic").value;
    obj.sa2022 = document.getElementById("oer_2022_sa").value;
    obj.wa2022 = document.getElementById("oer_2022_wa").value;
    obj.act2022 = document.getElementById("oer_2022_act").value;
    obj.tas2022 = document.getElementById("oer_2022_tas").value;
    obj.nt2022 = document.getElementById("oer_2022_nt").value;


    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var data = JSON.parse(this.responseText);
                    // alert(this.responseText);
                    // put values in respective places
                    for (i = 0; i < data.length; i++) {
                        document.getElementById("oer_" + data[i].year + "_qld").value = data[i].queensland;
                        document.getElementById("oer_" + data[i].year + "_nsw").value = data[i].new_south_wales;
                        document.getElementById("oer_" + data[i].year + "_vic").value = data[i].victoria;
                        document.getElementById("oer_" + data[i].year + "_sa").value = data[i].south_australia;
                        document.getElementById("oer_" + data[i].year + "_wa").value = data[i].western_australia;
                        document.getElementById("oer_" + data[i].year + "_act").value = data[i].australian_capital_territory;
                        document.getElementById("oer_" + data[i].year + "_tas").value = data[i].tasmania;
                        document.getElementById("oer_" + data[i].year + "_nt").value = data[i].northern_territory;
                    }

                }
    }
    request.send(params);

}


//  ---------------------------------------------Lighting Database ---------------------------------------------------------

var $FormLightingData = $('#form_lighting_data')
$FormLightingData.submit(function (event) {
    event.preventDefault();
    saveLightingData();
});


function saveLightingData(){
    var url = '/references/save_lighting_data/'
    deleteErrorMessage("lighting_data_save_message")
    var obj = new Object;
    obj.lightingVerdiaFee = document.getElementById("lighting_verdia_fee").value
    if (obj.lightingVerdiaFee==""){
        createErrorMessage("lighting_data_save_message","Verdia Fee Cannot be empty.")
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
                    console.log(data)
                    if (data.message=="Success"){
                        createErrorMessage("lighting_data_save_message","Saved")
                    }
                    else{
                        createErrorMessage("lighting_data_save_message",data.message)
                    }
                }
    }   
    request.send(params);
}






function showLedDatabase() {
    var url = '/references/show_led_database/'
    var obj = new Object;
    obj.ledNew = "No"

    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var data = JSON.parse(this.responseText);
                    // alert(this.responseText);
                    // put values in respective places
                    table_html = []
                    for (i = 0; i < data.length; i++) {
                        table_html = table_html +
                            (
                                "<tr align='center'>" +
                                "<td>" + (i + 1) + "</td>" +
                                "<td>" + data[i].name + "</td>" +
                                "<td>" + data[i].fitting_type + "</td>" +
                                "<td>" + data[i].installation_type + "</td>" +
                                "<td>" + data[i].system_power + "</td>" +
                                "<td>" + data[i].led_life + "</td>" +
                                "<td>" + data[i].replacement_fitting_price + "</td>" +
                                "<td>" + data[i].replacement_fittings_per_hour + "</td>" +
                                "<td>" +
                                "<a class='btn text-secondary px-0' onclick='editLed(" + data[i].id + ")';><i class='far fa-edit fa-lg'></i></a>" +
                                "<button class='btn d-inline' onclick='deleteLed(" + data[i].id + ")';>" +
                                "<i class='far fa-trash-alt fa-lg text-danger float-right'></i>" +
                                "</button>" +
                                "</td>" +
                                "</tr>"
                            )


                    }
                    document.getElementById("tbl_led_database_body").innerHTML = table_html;


                }
    }
    request.send(params);
    fillExistingLedReplacement();
}

function saveLED() {
    var url = '/references/save_led/'
    var obj = new Object;
    obj.ledId = document.getElementById("hidden_led_id").value;
    obj.ledName = document.getElementById("led_name").value;
    obj.ledFittingType = document.getElementById("led_fitting_type").value;
    obj.ledInstallType = document.getElementById("led_install_type").value;
    obj.ledSystemPower = document.getElementById("led_system_power").value;
    obj.ledLife = document.getElementById("led_life").value;
    obj.ledReplacementFittingPrice = document.getElementById("led_replacement_fitting_price").value;
    obj.ledReplacementFittingsPerHour = document.getElementById("led_replacement_fittings_per_hour").value;

    console.log(obj)

    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var message = this.responseText;
                    if (message == "success") {
                        showLedDatabase();
                        clearLedModal();
                        $('#modal-led-lights').modal("hide");
                    }
                    else {
                        document.getElementById("led_modal_save_message").innerHTML = this.responseText;
                        document.getElementById("led_modal_save_message").classList.add("alert");
                        document.getElementById("led_modal_save_message").classList.add("alert-danger");
                    }
                }
    }
    request.send(params);


}

function deleteLed(ledId) {
    var url = '/references/delete_led/'
    var obj = new Object;
    obj.ledId = ledId;

    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    showLedDatabase();

                }
    }
    request.send(params);

}

function editLed(ledId) {
    var url = '/references/edit_led/'
    var obj = new Object;
    obj.ledId = ledId;

    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    // alert(this.responseText);
                    var data = JSON.parse(this.responseText);
                    $('#modal-led-lights').modal();
                    document.getElementById('hidden_led_id').value = data.id;
                    document.getElementById('led_name').value = data.name;
                    document.getElementById('led_fitting_type').value = data.fitting_type;
                    document.getElementById('led_install_type').value = data.installation_type;
                    document.getElementById('led_system_power').value = data.system_power;
                    document.getElementById('led_life').value = data.led_life;
                    document.getElementById('led_replacement_fitting_price').value = data.replacement_fitting_price;
                    document.getElementById('led_replacement_fittings_per_hour').value = data.replacement_fittings_per_hour;

                }
    }
    request.send(params);

}

function clearLedModal() {
    document.getElementById('hidden_led_id').value = "";
    document.getElementById('led_name').value = "";
    document.getElementById('led_fitting_type').value = "";
    document.getElementById('led_install_type').value = "";
    document.getElementById('led_system_power').value = "";
    document.getElementById('led_life').value = "";
    document.getElementById('led_replacement_fitting_price').value = "";
    document.getElementById('led_replacement_fittings_per_hour').value = "";
    document.getElementById("led_modal_save_message").innerHTML = "";
    document.getElementById("led_modal_save_message").classList.remove("alert");
    document.getElementById("led_modal_save_message").classList.remove("alert-danger");
}

function showExistingDatabase() {
    var url = '/references/show_existing_database/'
    var obj = new Object;
    obj.ledNew = "No"

    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var data = JSON.parse(this.responseText);
                    // alert(data.led_lights[2].name);
                    // put values in respective places
                    table_html = []
                    if (data.length > 0) {
                        for (i = 0; i < data.length; i++) {
                            table_html = table_html +
                                (
                                    "<tr align='center'>" +
                                    "<td>" + (i + 1) + "</td>" +
                                    "<td>" + data[i].name + "</td>" +
                                    "<td>" + nullValidation(data[i].other_names) + "</td>" +
                                    "<td>" + data[i].led_light + "</td>" +
                                    "<td>" + data[i].fitting_type + "</td>" +
                                    "<td>" + data[i].installation_type + "</td>" +
                                    "<td>" + data[i].lamp_quantity + "</td>" +
                                    "<td>" + data[i].lamp_wattage + "</td>" +
                                    "<td>" + data[i].system_power + "</td>" +
                                    "<td>" + data[i].lamp_life + "</td>" +
                                    "<td>" + data[i].replacement_lamp_price + "</td>" +
                                    "<td>" + data[i].replacement_lamp_fittings_per_hour + "</td>" +
                                    "<td>" + data[i].replacement_fitting_price + "</td>" +
                                    "<td>" + data[i].replacement_fittings_per_hour + "</td>" +
                                    "<td>" +
                                    "<a class='btn text-secondary px-0' onclick='editExisting(" + data[i].id + ")';><i class='far fa-edit fa-lg'></i></a>" +
                                    "<button class='btn d-inline' onclick='deleteExisting(" + data[i].id + ")';>" +
                                    "<i class='far fa-trash-alt fa-lg text-danger float-right'></i>" +
                                    "</button>" +
                                    "</td>" +
                                    "</tr>"
                                )

                        }
                    }
                    document.getElementById("tbl_existing_database_body").innerHTML = table_html


                }
    }
    request.send(params);
}

function saveExisting() {
    var url = '/references/save_existing/'
    var obj = new Object;
    obj.existingId = document.getElementById("hidden_existing_id").value;
    obj.existingName = document.getElementById("existing_name").value;
    obj.existingOtherNames = document.getElementById("existing_other_names").value;
    obj.existingLedReplacement = document.getElementById("existing_led_replacement").value;
    obj.existingFittingType = document.getElementById("existing_fitting_type").value;
    obj.existingInstallType = document.getElementById("existing_install_type").value;
    obj.existingLampQuantity = document.getElementById("existing_lamp_quantity").value;
    obj.existingLampWattage = document.getElementById("existing_lamp_wattage").value;
    obj.existingSystemPower = document.getElementById("existing_system_power").value;
    obj.existingLife = document.getElementById("existing_life").value;
    obj.existingReplacementLampPrice = document.getElementById("existing_replacement_lamp_price").value;
    obj.existingReplacementLampFittingsPerHour = document.getElementById("existing_replacement_lamp_fittings_per_hour").value;
    obj.existingReplacementFittingPrice = document.getElementById("existing_replacement_fitting_price").value;
    obj.existingReplacementFittingsPerHour = document.getElementById("existing_replacement_fittings_per_hour").value;

    console.log(obj)

    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var message = this.responseText;
                    if (message == "success") {
                        showExistingDatabase();
                        clearExistingModal();
                        $('#modal-existing-lights').modal("hide");
                    }
                    else {
                        document.getElementById("existing_modal_save_message").innerHTML = this.responseText;
                        document.getElementById("existing_modal_save_message").classList.add("alert");
                        document.getElementById("existing_modal_save_message").classList.add("alert-danger");
                    }
                }
    }
    request.send(params);


}

function deleteExisting(existingId) {
    var url = '/references/delete_existing/'
    var obj = new Object;
    obj.existingId = existingId;

    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    showExistingDatabase();

                }
    }
    request.send(params);

}

function editExisting(existingId) {
    var url = '/references/edit_existing/'
    var obj = new Object;
    obj.existingId = existingId;

    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    // alert(this.responseText);
                    var data = JSON.parse(this.responseText);
                    $('#modal-existing-lights').modal();
                    document.getElementById('hidden_existing_id').value = data.id;
                    document.getElementById('existing_name').value = data.name;
                    document.getElementById('existing_led_replacement').value = data.led_light;
                    document.getElementById('existing_other_names').value = data.other_names;
                    var s = document.getElementById('existing_led_replacement')
                    for (i = 0; i < s.options.length; i++) {
                        if (s.options[i].value == data.led_light_id) {
                            s.options[i].selected = true;
                        }
                        console.log(s.options[i].value);
                    }
                    document.getElementById('existing_fitting_type').value = data.fitting_type;
                    document.getElementById('existing_install_type').value = data.installation_type;
                    document.getElementById('existing_lamp_quantity').value = data.lamp_quantity;
                    document.getElementById('existing_lamp_wattage').value = data.lamp_wattage;
                    document.getElementById('existing_system_power').value = data.system_power;
                    document.getElementById('existing_life').value = data.lamp_life;
                    document.getElementById('existing_replacement_lamp_price').value = data.replacement_lamp_price;
                    document.getElementById('existing_replacement_lamp_fittings_per_hour').value = data.replacement_lamp_fittings_per_hour;
                    document.getElementById('existing_replacement_fitting_price').value = data.replacement_fitting_price;
                    document.getElementById('existing_replacement_fittings_per_hour').value = data.replacement_fittings_per_hour;
                    console.log(data.led_light)
                    console.log(data.led_light_id)
                }
    }
    request.send(params);
}

function clearExistingModal() {
    document.getElementById('hidden_existing_id').value = "";
    document.getElementById('existing_name').value = "";
    document.getElementById('existing_other_names').value = "";
    document.getElementById('existing_fitting_type').value = "";
    document.getElementById('existing_install_type').value = "";
    document.getElementById('existing_lamp_quantity').value = "";
    document.getElementById('existing_lamp_wattage').value = "";
    document.getElementById('existing_system_power').value = "";
    document.getElementById('existing_life').value = "";
    document.getElementById('existing_replacement_lamp_price').value = "";
    document.getElementById('existing_replacement_lamp_fittings_per_hour').value = "";
    document.getElementById('existing_replacement_fitting_price').value = "";
    document.getElementById('existing_replacement_fittings_per_hour').value = "";
    document.getElementById("existing_modal_save_message").innerHTML = "";
    document.getElementById("existing_modal_save_message").classList.remove("alert");
    document.getElementById("existing_modal_save_message").classList.remove("alert-danger");
}

function fillExistingLedReplacement() {
    var url = '/references/fill_existing_led_replacement/'
    var obj = new Object;
    obj.dummyValue = "Dummy"

    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var data = JSON.parse(this.responseText);
                    if (data.length > 0) {

                        select_html = []
                        for (i = 0; i < data.length; i++) {

                            select_html = select_html +
                                "<option value='" + data[i].id + "'>" + data[i].name + "</option>"

                        }
                        document.getElementById("existing_led_replacement").innerHTML = select_html;
                    }

                }
    }
    request.send(params);
}

//  --------------------------------------------- Solar & PFC Costs ---------------------------------------------------------

// Solar Costs Javascript

function showSolarCost() {
    var url = '/references/show_solar_cost/'
    var obj = new Object;
    obj.dummyVariable = "Dummy"

    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var data = JSON.parse(this.responseText);
                    if (data.message == 'Success') {
                        table_html = [];
                        if (data.value.length > 0) {
                            for (i = 0; i < data.value.length; i++) {
                                table_html = table_html +
                                    (
                                        "<tr align='center'>" +
                                        "<td>" + (i + 1) + "</td>" +
                                        "<td>" + data.value[i].system_size + "</td>" +
                                        "<td>" + data.value[i].single_site_dollar_per_watt + "</td>" +
                                        "<td>" + data.value[i].single_site_verdia_fee + "</td>" +
                                        "<td>" + data.value[i].multi_site_dollar_per_watt + "</td>" +
                                        "<td>" + data.value[i].multi_site_verdia_fee + "</td>" +
                                        "<td>" +
                                        "<a class='btn text-secondary px-0' onclick='editSolarCost(" + data.value[i].id + ")';><i class='far fa-edit fa-lg'></i></a>" +
                                        "<button class='btn d-inline' onclick='deleteSolarCost(" + data.value[i].id + ")';>" +
                                        "<i class='far fa-trash-alt fa-lg text-danger float-right'></i>" +
                                        "</button>" +
                                        "</td>" +
                                        "</tr>"
                                    )

                            }
                        }
                        document.getElementById("tbl_solar_cost_body").innerHTML = table_html;
                        deleteErrorMessage("div_solar_cost_error");
                    }
                    else {
                        createErrorMessage("div_solar_cost_error", data.message)
                    }
                }
    }
    request.send(params);
}

function saveSolarCost() {
    var url = '/references/save_solar_cost/'
    var $SolarForm = $('#modal-form-solar-cost');
    solarCostId = document.getElementById("hidden_solar_cost_id").value;
    var $formData = $SolarForm.serialize() + '&solarCostId=' + solarCostId;
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
                    console.log(this.responseText);
                    var data = JSON.parse(this.responseText);
                    if (data.message == "saved") {
                        // $SolarForm[0].reset();
                        clearSolarCostModal();
                        $('#modal-solar-cost').modal("hide");
                        showSolarCost();
                    }
                    else {

                        if ("system_size" in data.message) {
                            createErrorMessage("error_solar_cost_modal_system_size", data.message.system_size)
                        }
                        else {
                            deleteErrorMessage("error_solar_cost_modal_system_size")
                        }

                        if ("single_site_dollar_per_watt" in data.message) {
                            createErrorMessage("error_solar_cost_modal_single_site_dollar_per_watt", data.message.single_site_dollar_per_watt)
                        }
                        else {
                            deleteErrorMessage("error_solar_cost_modal_single_site_dollar_per_watt")
                        }
                        if ("single_site_verdia_fee" in data.message) {
                            createErrorMessage("error_solar_cost_modal_single_site_verdia_fee", data.message.single_site_verdia_fee)
                        }
                        else {
                            deleteErrorMessage("error_solar_cost_modal_single_site_verdia_fee")
                        }
                        if ("multi_site_dollar_per_watt" in data.message) {
                            createErrorMessage("error_solar_cost_modal_multi_site_dollar_per_watt", data.message.multi_site_dollar_per_watt)
                        }
                        else {
                            deleteErrorMessage("error_solar_cost_modal_multi_site_dollar_per_watt")
                        }
                        if ("multi_site_verdia_fee" in data.message) {
                            createErrorMessage("error_solar_cost_modal_multi_site_verdia_fee", data.message.multi_site_verdia_fee)
                        }
                        else {
                            deleteErrorMessage("error_solar_cost_modal_multi_site_verdia_fee")
                        }

                    }


                }
    }
    request.send($formData);
}

function clearSolarCostModal() {
    document.getElementById('hidden_solar_cost_id').value = "";
    document.getElementById('solar_cost_system_size').value = "";
    document.getElementById('solar_cost_single_site_dollar_per_watt').value = "";
    document.getElementById('solar_cost_single_site_verdia_fee').value = "";
    document.getElementById('solar_cost_multi_site_dollar_per_watt').value = "";
    document.getElementById('solar_cost_multi_site_verdia_fee').value = "";
    deleteErrorMessage("solar_cost_modal_save_message");
    deleteErrorMessage("error_solar_cost_modal_system_size");
    deleteErrorMessage("error_solar_cost_modal_single_site_dollar_per_watt");
    deleteErrorMessage("error_solar_cost_modal_single_site_verdia_fee");
    deleteErrorMessage("error_solar_cost_modal_multi_site_dollar_per_watt");
    deleteErrorMessage("error_solar_cost_modal_multi_site_verdia_fee");
}

function editSolarCost(solarCostId) {
    var url = '/references/edit_solar_cost/'
    var obj = new Object;
    obj.solarCostId = solarCostId;

    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    // alert(this.responseText);
                    var data = JSON.parse(this.responseText);
                    if (data.message == 'Success') {
                        $('#modal-solar-cost').modal();
                        document.getElementById('hidden_solar_cost_id').value = data.value.id;
                        document.getElementById('solar_cost_system_size').value = data.value.system_size;
                        document.getElementById('solar_cost_single_site_dollar_per_watt').value = data.value.single_site_dollar_per_watt;
                        document.getElementById('solar_cost_single_site_verdia_fee').value = data.value.single_site_verdia_fee;
                        document.getElementById('solar_cost_multi_site_dollar_per_watt').value = data.value.multi_site_dollar_per_watt;
                        document.getElementById('solar_cost_multi_site_verdia_fee').value = data.value.multi_site_verdia_fee;
                        deleteErrorMessage("div_solar_cost_error")
                    }
                    else {
                        createErrorMessage("div_solar_cost_error", data.message)
                    }
                }
    }
    request.send(params);
}

function deleteSolarCost(solarCostId) {
    var url = '/references/delete_solar_cost/'
    var obj = new Object;
    obj.solarCostId = solarCostId;

    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var data = JSON.parse(this.responseText);
                    if (data.message == "Success") {
                        showSolarCost();
                        deleteErrorMessage("div_solar_cost_error")
                    }
                    else {
                        createErrorMessage("div_solar_cost_error", data.message)
                    }

                }
    }
    request.send(params);
}

function closeSolarCost() {
    clearSolarCostModal();
    $('#modal-solar-cost').modal("hide");

}

// PFC Costs Javascript

function showPFCCost() {
    var url = '/references/show_pfc_cost/'
    var obj = new Object;
    obj.dummyVariable = "Dummy"

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
                    if (data.message == 'Success') {
                        table_html = []
                        if (data.value.length > 0) {
                            for (i = 0; i < data.value.length; i++) {
                                table_html = table_html +
                                    (
                                        "<tr align='center'>" +
                                        "<td>" + (i + 1) + "</td>" +
                                        "<td>" + data.value[i].pfc_rating + "</td>" +
                                        "<td>" + data.value[i].pfc_dollar_per_kvar + "</td>" +
                                        "<td>" +
                                        "<a class='btn text-secondary px-0' onclick='editPFCCost(" + data.value[i].id + ")';><i class='far fa-edit fa-lg'></i></a>" +
                                        "<button class='btn d-inline' onclick='deletePFCCost(" + data.value[i].id + ")';>" +
                                        "<i class='far fa-trash-alt fa-lg text-danger float-right'></i>" +
                                        "</button>" +
                                        "</td>" +
                                        "</tr>"
                                    )

                            }
                        }
                        document.getElementById("tbl_pfc_cost_body").innerHTML = table_html
                        deleteErrorMessage("div_pfc_cost_error")
                    }
                    else {
                        createErrorMessage("div_pfc_cost_error", data.message)
                    }



                }
    }
    request.send(params);
}

function savePFCCost() {
    var url = '/references/save_pfc_cost/'
    var $PFCForm = $('#modal-form-pfc-cost');
    pfcCostId = document.getElementById("hidden_pfc_cost_id").value;
    var $formData = $PFCForm.serialize() + '&pfcCostId=' + pfcCostId;
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
                    console.log(this.responseText);
                    var data = JSON.parse(this.responseText);
                    if (data.message == "Success") {
                        // $PFCForm[0].reset();
                        clearPFCCostModal();
                        $('#modal-pfc-cost').modal("hide");
                        showPFCCost();
                    }
                    else {

                        if ("pfc_rating" in data.message) {
                            createErrorMessage("error_pfc_cost_modal_pfc_rating", data.message.pfc_rating)
                        }
                        else {
                            deleteErrorMessage("error_pfc_cost_modal_pfc_rating")
                        }
                        if ("pfc_dollar_per_kvar" in data.message) {
                            createErrorMessage("error_pfc_cost_modal_pfc_dollar_per_kvar", data.message.pfc_dollar_per_kvar)
                        }
                        else {
                            deleteErrorMessage("error_pfc_cost_modal_pfc_dollar_per_kvar")
                        }
                    }

                }
    }
    request.send($formData);
}

function clearPFCCostModal() {
    document.getElementById('hidden_pfc_cost_id').value = "";
    document.getElementById('pfc_cost_pfc_rating').value = "";
    document.getElementById('pfc_cost_pfc_dollar_per_kvar').value = "";
    deleteErrorMessage("pfc_cost_modal_save_message");
    deleteErrorMessage("error_pfc_cost_modal_pfc_rating")
    deleteErrorMessage("error_pfc_cost_modal_pfc_dollar_per_kvar")

}

function editPFCCost(pfcCostId) {
    var url = '/references/edit_pfc_cost/'
    var obj = new Object;
    obj.pfcCostId = pfcCostId;

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
                        $('#modal-pfc-cost').modal();
                        document.getElementById('hidden_pfc_cost_id').value = data.value.id;
                        document.getElementById('pfc_cost_pfc_rating').value = data.value.pfc_rating;
                        document.getElementById('pfc_cost_pfc_dollar_per_kvar').value = data.value.pfc_dollar_per_kvar;
                        deleteErrorMessage("div_pfc_cost_error")
                    }
                    else {
                        createErrorMessage("div_pfc_cost_error", data.message)
                    }

                }
    }
    request.send(params);
}

function deletePFCCost(pfcCostId) {
    var url = '/references/delete_pfc_cost/'
    var obj = new Object;
    obj.pfcCostId = pfcCostId;

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
                        showPFCCost();
                        deleteErrorMessage("div_pfc_cost_error")
                    }
                    else {
                        createErrorMessage("div_pfc_cost_error", data.message)
                    }

                }
    }
    request.send(params);
}

function closePFCCost() {
    clearPFCCostModal();
    $('#modal-pfc-cost').modal("hide");
}



//--------------------------------------------------------- Solar Data --------------------------------------

$(document).on('click', '.browse', function () {
    var file = $(this).parent().parent().parent().find('.file1');
    file.trigger('click');
});

$(document).on('change', '.file1', function () {
    $(this).parent().find('.form-control').val($(this).val().replace(/C:\\fakepath\\/i, ''));
});

var $SolarDataForm = $('#form_solar_data_upload');
$SolarDataForm.submit(function (event) {
    event.preventDefault();
    uploadSolarData();
});


function uploadSolarData(){
    var url = '/references/solar_data_upload/'
    var formData = new FormData(document.getElementById("form_solar_data_upload"));     
    // var obj = new Object();
    // obj.scenarioId = scenarioId
    // var JSONobj = JSON.stringify(obj);
    // formData.append('JSONobj', JSONobj);
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