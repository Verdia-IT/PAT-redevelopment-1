

var $BillDetailForm = $('#form_bill_details');
$BillDetailForm.submit(function (event) {
    event.preventDefault();
    saveBillDetail();
});

var $OperatingHourDetailForm = $('#form_operating_hour_details');
$OperatingHourDetailForm.submit(function (event) {
    event.preventDefault();
    saveOperatingHourDetail();
});

var $HolidayDetailForm = $('#form_holiday_details');
$HolidayDetailForm.submit(function (event) {
    event.preventDefault();
    saveHolidayDetail();
});

var $PriceForecastOverrideForm = $('#form_price_forecast_override');
$PriceForecastOverrideForm.submit(function (event) {
    event.preventDefault();
    savePriceForecastOverride();
});

var $EscalationsOverrideForm = $('#form_escalations_override');
$EscalationsOverrideForm.submit(function (event) {
    event.preventDefault();
    saveEscalationsOverride();
});

var $SolarExportForm = $('#form_solar_export');
$SolarExportForm.submit(function (event) {
    event.preventDefault();
    saveSolarExport();
});




function saveBillDetail() {
    var url = '/inputs/save_bill_detail/'
    var $BillDetailForm = $('#form_bill_details');
    var scenarioId = document.getElementById("hidden_scenario_id").value;
    var $formData = $BillDetailForm.serialize() + '&scenarioId=' + scenarioId;
    console.log($formData);
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    clearBillDetailErrors();
                    var data = JSON.parse(this.responseText);
                    if (data.message == "Success") {
                        createErrorMessage("bill_details_save_message", "Saved");
                    }
                    else {
                        if ((typeof data.message) == "string") {
                            createErrorMessage("bill_details_save_message", data.message)
                        }
                        else {

                            if ("number_of_bills" in data.message) {
                                createErrorMessage("error_bill_details_number_of_bills", data.message.number_of_bills)
                            }
                            if ("bill_month" in data.message) {
                                createErrorMessage("error_bill_details_bill_month", data.message.bill_month)
                            }
                            if ("bill_year" in data.message) {
                                createErrorMessage("error_bill_details_bill_year", data.message.bill_year)
                            }
                            if ("bill_days" in data.message) {
                                createErrorMessage("error_bill_details_bill_days", data.message.bill_days)
                            }
                            if ("electricity_retailer" in data.message) {
                                createErrorMessage("error_bill_details_electricity_retailer", data.message.electricity_retailer)
                            }
                            if ("kwhs_consumed" in data.message) {
                                createErrorMessage("error_bill_details_kwhs_consumed", data.message.kwhs_consumed)
                            }
                        }
                    }

                }
    }
    request.send($formData);
}

function clearBillDetailErrors() {
    deleteErrorMessage("error_bill_details_number_of_bills")
    deleteErrorMessage("error_bill_details_bill_month")
    deleteErrorMessage("error_bill_details_bill_year")
    deleteErrorMessage("error_bill_details_bill_days")
    deleteErrorMessage("error_bill_details_electricity_retailer")
    deleteErrorMessage("error_bill_details_kwhs_consumed")
    deleteErrorMessage("bill_details_save_message", "Saved");
}

function saveOperatingHourDetail() {
    var url = '/inputs/save_operating_hour_detail/'
    var $OperatingHourDetailForm = $('#form_operating_hour_details');
    var scenarioId = document.getElementById("hidden_scenario_id").value;
    var $formData = $OperatingHourDetailForm.serialize() + '&scenarioId=' + scenarioId;
    console.log($formData);
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    clearOperatingHourDetailErrors();
                    var data = JSON.parse(this.responseText);
                    if (data.message == "Success") {
                        createErrorMessage("operating_hour_details_save_message", "Saved");
                    }
                    else {
                        if ((typeof data.message) == "string") {
                            createErrorMessage("operating_hour_details_save_message", data.message)
                        }
                           
                      
                    }

                }
    }
    request.send($formData);
}

function clearOperatingHourDetailErrors() {
    deleteErrorMessage("operating_hour_details_save_message");
    
}


function saveHolidayDetail(){
    var url = '/inputs/save_holiday_detail/'
    var $HolidayDetailForm = $('#form_holiday_details');
    var scenarioId = document.getElementById("hidden_scenario_id").value;
    var $formData = $HolidayDetailForm.serialize() + '&scenarioId=' + scenarioId;
    console.log($formData);
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    clearHolidayDetailErrors();
                    var data = JSON.parse(this.responseText);
                    if (data.message == "Success") {
                        createErrorMessage("holiday_details_save_message", "Saved");
                    }
                    else {
                        if ((typeof data.message) == "string") {
                            createErrorMessage("holiday_details_save_message", data.message)
                        }
                        else {

                            if ("holiday_period_1_start_date" in data.message) {
                                createErrorMessage("error_holiday_details_holiday_period_1_start_date", data.message.holiday_period_1_start_date)
                            }
                            if ("holiday_period_1_start_month" in data.message) {
                                createErrorMessage("error_holiday_details_holiday_period_1_start_month", data.message.holiday_period_1_start_month)
                            }
                            if ("holiday_period_1_end_date" in data.message) {
                                createErrorMessage("error_holiday_details_holiday_period_1_end_date", data.message.holiday_period_1_end_date)
                            }
                            if ("holiday_period_1_end_month" in data.message) {
                                createErrorMessage("error_holiday_details_holiday_period_1_end_month", data.message.holiday_period_1_end_month)
                            }
                            if ("holiday_period_2_start_date" in data.message) {
                                createErrorMessage("error_holiday_details_holiday_period_2_start_date", data.message.holiday_period_2_start_date)
                            }
                            if ("holiday_period_2_start_month" in data.message) {
                                createErrorMessage("error_holiday_details_holiday_period_2_start_month", data.message.holiday_period_2_start_month)
                            }
                            if ("holiday_period_2_end_date" in data.message) {
                                createErrorMessage("error_holiday_details_holiday_period_2_end_date", data.message.holiday_period_2_end_date)
                            }
                            if ("holiday_period_2_end_month" in data.message) {
                                createErrorMessage("error_holiday_details_holiday_period_2_end_month", data.message.holiday_period_2_end_month)
                            }
                            if ("holiday_period_3_start_date" in data.message) {
                                createErrorMessage("error_holiday_details_holiday_period_3_start_date", data.message.holiday_period_3_start_date)
                            }
                            if ("holiday_period_3_start_month" in data.message) {
                                createErrorMessage("error_holiday_details_holiday_period_3_start_month", data.message.holiday_period_3_start_month)
                            }
                            if ("holiday_period_3_end_date" in data.message) {
                                createErrorMessage("error_holiday_details_holiday_period_3_end_date", data.message.holiday_period_3_end_date)
                            }
                            if ("holiday_period_3_end_month" in data.message) {
                                createErrorMessage("error_holiday_details_holiday_period_3_end_month", data.message.holiday_period_3_end_month)
                            }
                            if ("holiday_period_4_start_date" in data.message) {
                                createErrorMessage("error_holiday_details_holiday_period_4_start_date", data.message.holiday_period_4_start_date)
                            }
                            if ("holiday_period_4_start_month" in data.message) {
                                createErrorMessage("error_holiday_details_holiday_period_4_start_month", data.message.holiday_period_4_start_month)
                            }
                            if ("holiday_period_4_end_date" in data.message) {
                                createErrorMessage("error_holiday_details_holiday_period_4_end_date", data.message.holiday_period_4_end_date)
                            }
                            if ("holiday_period_4_end_month" in data.message) {
                                createErrorMessage("error_holiday_details_holiday_period_4_end_month", data.message.holiday_period_4_end_month)
                            }
                            
                        }
                    }

                }
    }
    request.send($formData);
}

function clearHolidayDetailErrors(){
    deleteErrorMessage("holiday_details_save_message");
    deleteErrorMessage("error_holiday_details_holiday_period_1_start_date");
    deleteErrorMessage("error_holiday_details_holiday_period_1_start_month");
    deleteErrorMessage("error_holiday_details_holiday_period_1_end_date");
    deleteErrorMessage("error_holiday_details_holiday_period_1_end_month");       
    deleteErrorMessage("error_holiday_details_holiday_period_2_start_date");   
    deleteErrorMessage("error_holiday_details_holiday_period_2_start_month");  
    deleteErrorMessage("error_holiday_details_holiday_period_2_end_date");
    deleteErrorMessage("error_holiday_details_holiday_period_2_end_month");  
    deleteErrorMessage("error_holiday_details_holiday_period_3_start_date");
    deleteErrorMessage("error_holiday_details_holiday_period_3_start_month"); 
    deleteErrorMessage("error_holiday_details_holiday_period_3_end_date");   
    deleteErrorMessage("error_holiday_details_holiday_period_3_end_month");
    deleteErrorMessage("error_holiday_details_holiday_period_4_start_date");
    deleteErrorMessage("error_holiday_details_holiday_period_4_start_month");
    deleteErrorMessage("error_holiday_details_holiday_period_4_end_date");    
    deleteErrorMessage("error_holiday_details_holiday_period_4_end_month");
}

function savePriceForecastOverride(){
    var url = '/inputs/save_price_forecast_override/'
    var $PriceForecastOverrideForm = $('#form_price_forecast_override');
    var scenarioId = document.getElementById("hidden_scenario_id").value;
    var $formData = $PriceForecastOverrideForm.serialize() + '&scenarioId=' + scenarioId;
    console.log($formData);
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    clearPriceForecastOverrideErrors();
                    var data = JSON.parse(this.responseText);
                    if (data.message == "Success") {
                        createErrorMessage("price_forecast_override_save_message", "Saved");
                    }
                    else {
                        if ((typeof data.message) == "string") {
                            createErrorMessage("price_forecast_override_save_message", data.message)
                        }
                        else {

                            if ("year_2019" in data.message) {
                                createErrorMessage("error_price_forecast_override_year_2019", data.message.year_2019)
                            }
                            if ("year_2020" in data.message) {
                                createErrorMessage("error_price_forecast_override_year_2020", data.message.year_2020)
                            }
                            if ("year_2021" in data.message) {
                                createErrorMessage("error_price_forecast_override_year_2021", data.message.year_2021)
                            }
                            if ("year_2022" in data.message) {
                                createErrorMessage("error_price_forecast_override_year_2022", data.message.year_2022)
                            }
                            if ("year_2023" in data.message) {
                                createErrorMessage("error_price_forecast_override_year_2023", data.message.year_2023)
                            }
                            if ("year_2024" in data.message) {
                                createErrorMessage("error_price_forecast_override_year_2024", data.message.year_2024)
                            }
                            if ("year_2025" in data.message) {
                                createErrorMessage("error_price_forecast_override_year_2025", data.message.year_2025)
                            }
                            if ("year_2026" in data.message) {
                                createErrorMessage("error_price_forecast_override_year_2026", data.message.year_2026)
                            }
                            if ("year_2027" in data.message) {
                                createErrorMessage("error_price_forecast_override_year_2027", data.message.year_2027)
                            }                            
                            
                        }
                    }

                }
    }
    request.send($formData);
}

function clearPriceForecastOverrideErrors(){
        deleteErrorMessage("price_forecast_override_save_message");
        deleteErrorMessage("error_price_forecast_override_year_2019");
        deleteErrorMessage("error_price_forecast_override_year_2020");
        deleteErrorMessage("error_price_forecast_override_year_2021"); 
        deleteErrorMessage("error_price_forecast_override_year_2022"); 
        deleteErrorMessage("error_price_forecast_override_year_2023"); 
        deleteErrorMessage("error_price_forecast_override_year_2024"); 
        deleteErrorMessage("error_price_forecast_override_year_2025");  
        deleteErrorMessage("error_price_forecast_override_year_2026");  
        deleteErrorMessage("error_price_forecast_override_year_2027");                              
}

function saveEscalationsOverride(){
    var url = '/inputs/save_escalations_override/'
    var $EscalationsOverrideForm = $('#form_escalations_override');
    var scenarioId = document.getElementById("hidden_scenario_id").value;
    var $formData = $EscalationsOverrideForm.serialize() + '&scenarioId=' + scenarioId;
    console.log($formData);
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    clearEscalationsOverrideErrors();
                    var data = JSON.parse(this.responseText);
                    if (data.message == "Success") {
                        createErrorMessage("escalations_override_save_message", "Saved");
                    }
                    else {
                        if ((typeof data.message) == "string") {
                            createErrorMessage("escalations_override_save_message", data.message)
                        }
                        else {

                            if ("year_1" in data.message) {
                                createErrorMessage("error_escalations_override_year_1", data.message.year_1)
                            }
                            if ("override_1" in data.message) {
                                createErrorMessage("error_escalations_override_override_1", data.message.override_1)
                            }
                            if ("year_2" in data.message) {
                                createErrorMessage("error_escalations_override_year_2", data.message.year_2)
                            }
                            if ("override_2" in data.message) {
                                createErrorMessage("error_escalations_override_override_2", data.message.override_2)
                            }
                            if ("year_3" in data.message) {
                                createErrorMessage("error_escalations_override_year_3", data.message.year_3)
                            }
                            if ("override_3" in data.message) {
                                createErrorMessage("error_escalations_override_override_3", data.message.override_3)
                            }
                            if ("year_4" in data.message) {
                                createErrorMessage("error_escalations_override_year_4", data.message.year_4)
                            }
                            if ("override_4" in data.message) {
                                createErrorMessage("error_escalations_override_override_4", data.message.override_4)
                            }
                            if ("year_5" in data.message) {
                                createErrorMessage("error_escalations_override_year_5", data.message.year_5)
                            }
                            if ("override_5" in data.message) {
                                createErrorMessage("error_escalations_override_override_5", data.message.override_5)
                            }
                            if ("year_6" in data.message) {
                                createErrorMessage("error_escalations_override_year_6", data.message.year_6)
                            }
                            if ("override_6" in data.message) {
                                createErrorMessage("error_escalations_override_override_6", data.message.override_6)
                            }                                             
                            
                        }
                    }

                }
    }
    request.send($formData);
}

function clearEscalationsOverrideErrors(){
    deleteErrorMessage("escalations_override_save_message");   
    deleteErrorMessage("error_escalations_override_year_1");    
    deleteErrorMessage("error_escalations_override_override_1");   
    deleteErrorMessage("error_escalations_override_year_2");  
    deleteErrorMessage("error_escalations_override_override_2");   
    deleteErrorMessage("error_escalations_override_year_3");    
    deleteErrorMessage("error_escalations_override_override_3");    
    deleteErrorMessage("error_escalations_override_year_4");    
    deleteErrorMessage("error_escalations_override_override_4");    
    deleteErrorMessage("error_escalations_override_year_5");    
    deleteErrorMessage("error_escalations_override_override_5");    
    deleteErrorMessage("error_escalations_override_year_6");   
    deleteErrorMessage("error_escalations_override_override_6");
}


function saveSolarExport(){
    var url = '/inputs/save_solar_export/'
    var $SolarExportForm = $('#form_solar_export');
    var scenarioId = document.getElementById("hidden_scenario_id").value;
    var $formData = $SolarExportForm.serialize() + '&scenarioId=' + scenarioId;
    console.log($formData);
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    clearSolarExportErrors();
                    var data = JSON.parse(this.responseText);
                    if (data.message == "Success") {
                        createErrorMessage("solar_export_save_message", "Saved");
                    }
                    else {
                        if ((typeof data.message) == "string") {
                            createErrorMessage("solar_export_save_message", data.message)
                        }
                        else {

                            if ("year_2019" in data.message) {
                                createErrorMessage("error_solar_export_year_2019", data.message.year_2019)
                            }
                            if ("year_2020 " in data.message) {
                                createErrorMessage("error_solar_export_year_2020", data.message.year_2020)
                            }
                            if ("year_2021" in data.message) {
                                createErrorMessage("error_solar_export_year_2021", data.message.year_2021)
                            }
                            if ("year_2022" in data.message) {
                                createErrorMessage("error_solar_export_year_2022", data.message.year_2022)
                            }
                            if ("year_2023" in data.message) {
                                createErrorMessage("error_solar_export_year_2023", data.message.year_2023)
                            }
                            if ("year_2024" in data.message) {
                                createErrorMessage("error_solar_export_year_2024", data.message.year_2024)
                            }
                            if ("year_2025" in data.message) {
                                createErrorMessage("error_solar_export_year_2025", data.message.year_2025)
                            }
                            if ("year_2026" in data.message) {
                                createErrorMessage("error_solar_export_year_2026", data.message.year_2026)
                            }
                            if ("year_2027" in data.message) {
                                createErrorMessage("error_solar_export_year_2027", data.message.year_2027)
                            }
                            if ("year_2028" in data.message) {
                                createErrorMessage("error_solar_export_year_2028", data.message.year_2028)
                            }
                            if ("year_2029" in data.message) {
                                createErrorMessage("error_solar_export_year_2029", data.message.year_2029)
                            }
                            if ("year_2030" in data.message) {
                                createErrorMessage("error_solar_export_year_2030", data.message.year_2030)
                            }
                            if ("year_2031" in data.message) {
                                createErrorMessage("error_solar_export_year_2031", data.message.year_2031)
                            }                                              
                            
                        }
                    }

                }
    }
    request.send($formData);
}

function clearSolarExportErrors(){
    deleteErrorMessage("solar_export_save_message"); 
    deleteErrorMessage("error_solar_export_year_2019");   
    deleteErrorMessage("error_solar_export_year_2020");    
    deleteErrorMessage("error_solar_export_year_2021");   
    deleteErrorMessage("error_solar_export_year_2022");   
    deleteErrorMessage("error_solar_export_year_2023");   
    deleteErrorMessage("error_solar_export_year_2024");    
    deleteErrorMessage("error_solar_export_year_2025");    
    deleteErrorMessage("error_solar_export_year_2026");   
    deleteErrorMessage("error_solar_export_year_2027");   
    deleteErrorMessage("error_solar_export_year_2028");  
    deleteErrorMessage("error_solar_export_year_2029");  
    deleteErrorMessage("error_solar_export_year_2030");
    deleteErrorMessage("error_solar_export_year_2031");
          
}