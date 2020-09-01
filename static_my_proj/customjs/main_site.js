
 $(document).ready(function () {

    var $SiteDetailsForm = $('#form_site_details');
    $SiteDetailsForm.submit(function (event) {
        event.preventDefault();
        saveSiteDetails();
    });

    var $NewScenarioModalForm = $('#modal_form_new_scenario');
    $NewScenarioModalForm.submit(function (event) {
        event.preventDefault();
        saveNewScenario();
    });

    showScenarios();

    $('.btn-close-new-scenario').click(closeNewScenarioModal);
});

function submitProgramForm() {
    var Form = document.getElementById("form_program")
    Form.submit();
}

function saveSiteDetails() {
    var $SiteDetailsForm = $('#form_site_details');
    var url = '/sites/save_new_site/';
    var programId = document.getElementById("hidden_program_id").value;
    var siteId = document.getElementById("hidden_site_id").value;
    var $formData = $SiteDetailsForm.serialize() + '&siteId=' + siteId + '&programId=' + programId;
    console.log($formData);
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    console.log(this.responseText);
                    var data = JSON.parse(this.responseText);
                    if (data.message == "Success") {
                        clearSiteDetailsErrors();
                        createErrorMessage("site_details_save_message", "Saved");
                    }
                    else {
                        clearSiteDetailsErrors();
                        if ((typeof data.message) == "string") {
                            createErrorMessage("site_details_save_message", data.message)
                        }
                        else {
                            if ("site_name" in data.message) {
                                createErrorMessage("error_site_details_site_name", data.message.site_name)
                            }

                            if ("NMI" in data.message) {
                                createErrorMessage("error_site_details_NMI", data.message.NMI)
                            }

                            if ("street_address" in data.message) {
                                createErrorMessage("error_site_details_street_address", data.message.street_address)
                            }

                            if ("city" in data.message) {
                                createErrorMessage("error_site_details_city", data.message.city)
                            }

                            if ("state" in data.message) {
                                createErrorMessage("error_site_details_state", data.message.state)
                            }
                            if ("postcode" in data.message) {
                                createErrorMessage("error_site_details_postcode", data.message.postcode)
                            }
                            if ("industry_type" in data.message) {
                                createErrorMessage("error_site_industry_type", data.message.industry_type)
                            }
                            if ("DNSP" in data.message) {
                                createErrorMessage("error_site_details_DNSP", data.message.DNSP)
                            }
                            if ("default_solar_data" in data.message) {
                                createErrorMessage("error_site_details_default_solar_data", data.message.default_solar_data)
                            }

                        }

                    }

                }
    }
    request.send($formData);
}

function clearSiteDetailsErrors() {
    deleteErrorMessage("error_site_details_site_name")
    deleteErrorMessage("error_site_details_NMI")
    deleteErrorMessage("error_site_details_street_address")
    deleteErrorMessage("error_site_details_city")
    deleteErrorMessage("error_site_details_state")
    deleteErrorMessage("error_site_details_postcode")
    deleteErrorMessage("error_site_details_industry_type")
    deleteErrorMessage("error_site_details_DNSP")
    deleteErrorMessage("error_site_details_default_solar_data")
}

function closeNewScenarioModal() {
    clearNewScenarioModal();
    $('#modal-new-scenario').modal("hide");
}

function clearNewScenarioModal() {
    document.getElementById("scenario_details_scenario_name").value = "";
    document.getElementById("scenario_details_notes").value = "";
    clearNewScenarioModalErrors();
}

function clearNewScenarioModalErrors() {
    deleteErrorMessage("new_scenario_modal_save_message");
    deleteErrorMessage("error_new_scenario_modal_scenario_name");
    deleteErrorMessage("error_new_scenario_modal_notes");

}

function saveNewScenario() {
    var url = '/scenarios/save_new_scenario/'
    var $NewScenarioModalForm = $('#modal_form_new_scenario');
    var programId = document.getElementById("hidden_program_id").value;
    var siteId = document.getElementById("hidden_site_id").value;
    var scenarioId = "";
    var $formData = $NewScenarioModalForm.serialize() + '&siteId=' + siteId + '&programId=' + programId + '&scenarioId=' + scenarioId;
    console.log($formData);
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    clearNewScenarioModalErrors();
                    var data = JSON.parse(this.responseText);
                    if (data.message == "Success") {
                        clearNewScenarioModal();
                        $('#modal-new-scenario').modal("hide");
                        showScenarios();
                    }
                    else {

                        if ((typeof data.message) == "string") {
                            createErrorMessage("new_scenario_modal_save_message", data.message)
                        }
                        else {
                            if ("scenario_name" in data.message) {
                                createErrorMessage("error_new_scenario_modal_scenario_name", data.message.scenario_name)
                            }
                            if ("notes" in data.message) {
                                createErrorMessage("error_new_scenario_modal_notes", data.message.notes)
                            }

                        }


                    }

                }
    }
    request.send($formData);

}

function showScenarios() {
    var url = '/scenarios/show_scenarios/'
    var obj = new Object;
    obj.programId = document.getElementById("hidden_program_id").value;
    obj.siteId = document.getElementById("hidden_site_id").value;

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
                    if (data.message == 'Success') {
                        table_html = []
                        if (data.value.length > 0) {
                            for (i = 0; i < data.value.length; i++) {
                                table_html = table_html +
                                    (
                                        "<tr align='center'>" +
                                        "<td>" + (i + 1) + "</td>" +
                                        "<td>" + data.value[i].scenario_name + "</td>" +                                                                                  
                                        "<td>" + data.value[i].summary + "</td>" +
                                        "<td>" + data.value[i].notes + "</td>" +  
                                        "<td>" +
                                        "<div class='row'>" +
                                        "<div class='col-4'>" +
                                        "<form method='post' action='/scenarios/main_scenario/'>" +
                                        "<input type='hidden' name='hidden_scenario_id' value='" + data.value[i].id + "'>" +
                                        "<input type='hidden' name='csrfmiddlewaretoken' value='" + csrfcookie() + "'>" +
                                        "<button type='submit' class='btn text-secondary px-0 d-inline'><i class='far fa-edit fa-lg'></i></button>" +
                                        "</form>" +
                                        "</div>" +
                                        "<div class='col-4'>" +
                                        "<button class='btn text-secondary px-0 d-inline' onclick='deleteScenario(" + data.value[i].id + ")';>" +
                                        "<i class='far fa-trash-alt fa-lg text-danger'></i></button>" +

                                        "</div>" +
                                        "</div>" +
                                        "</td>" +
                                        "</tr>"
                                    )

                            }
                        }
                        document.getElementById("tbl_scenarios_body").innerHTML = table_html
                        deleteErrorMessage("div_scenarios_error")
                    }
                    else {
                        createErrorMessage("div_scenarios_error", data.message)
                    }



                }
    }
    request.send(params);
}

function deleteScenario(scenarioId){
    var url = '/scenarios/delete_scenario/'
    var obj = new Object;
    obj.scenarioId = scenarioId;

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
                        showScenarios();
                        deleteErrorMessage("div_scenarios_error")
                    }
                    else {
                        createErrorMessage("div_scenarios_error", data.message)
                    }

                }
    }
    request.send(params);
}
