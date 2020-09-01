var $SimulationParameterForm = $('#form_simulation_parameter');
$SimulationParameterForm.submit(function (event) {
    event.preventDefault();
    saveSimulationParameter();
});


function saveSimulationParameter(){
    var url = '/simulations/save_simulation_parameter/'
    var formData = new FormData(document.getElementById("form_simulation_parameter"));
    var scenarioId = document.getElementById("hidden_scenario_id").value;    
    console.log(document.getElementById("simulation_parameter_interval_data").value)
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
                    console.log(data)  
                    clearSimulationParameterErrors();
                    if (data.message=="Success"){
                        createErrorMessage("simulation_parameter_save_message","Saved")
                        calculateSolarPrice();
                        calculatePFCPrice();
                    }
                    else{
                        if ("interval_data" in data.message) {
                            createErrorMessage("error_simulation_parameter_interval_data", data.message.interval_data)
                        }
                        if ("include_lighting" in data.message) {
                            createErrorMessage("error_simulation_parameter_include_lighting", data.message.include_lighting)
                        }
                        if ("solar_size" in data.message) {
                            createErrorMessage("error_simulation_parameter_solar_size", data.message.solar_size)
                        }
                        if ("pfc_size" in data.message) {
                            createErrorMessage("error_simulation_parameter_pfc_size", data.message.pfc_size)
                        }
                        if ("target_pf" in data.message) {
                            createErrorMessage("error_simulation_parameter_target_pf", data.message.target_pf)
                        } 
                    }             

                }
    }
    request.send(formData);
}

function clearSimulationParameterErrors(){
    deleteErrorMessage("simulation_parameter_save_message");
    deleteErrorMessage("error_simulation_parameter_interval_data");
    deleteErrorMessage("error_simulation_parameter_include_lighting");
    deleteErrorMessage("error_simulation_parameter_solar_size");
    deleteErrorMessage("error_simulation_parameter_pfc_size");
    deleteErrorMessage("error_simulation_parameter_target_pf");
}



var btnRunSimulation = document.getElementById("btn_run_simulation")
btnRunSimulation.addEventListener("click",RunSimulation);

function RunSimulation(){
    var url = '/simulations/run_simulation/'
    document.getElementById("id_simulation_status").innerHTML = "Calculating..."
    var obj = new Object;
    obj.scenarioId = document.getElementById("hidden_scenario_id").value;
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
                    capexMetricsDict = data.val.capex_metrics_dict
                    outputSummaryDict = data.val.output_summary_dict
                    document.getElementById("output_npv").value = numberFormat(capexMetricsDict.NPV, 0, "no")
                    document.getElementById("output_irr").value = numberFormat(capexMetricsDict.IRR*100, 2, "no")
                    document.getElementById("output_payback").value = numberFormat(capexMetricsDict.payback, 2, "no")
                    document.getElementById("output_lcoe").value = numberFormat(capexMetricsDict.LCOE, 4, "no")
                    document.getElementById("id_simulation_status").innerHTML = ""           
                    // var df = JSON.parse(data.value);           
                    
                    // Output Summary -----------------------------------------------------------------------------------------------------------------------
                    table_html = "<div class='row'>"
                    table_html +=  "<div class='col-10 col-md-5'>"
                    table_html += "<table class='table table-bordered'>"
                    table_html += "<tr align='center'><td colspan='2'><strong>Load Summary</strong></td></tr>"
                    table_html += "<tr><td>Load Consumption</td><td>"+ numberFormat(Math.round(outputSummaryDict.load_consumption),0,"no") + " MWh</td></tr>"
                    table_html += "<tr><td>Load After System</td><td>"+ numberFormat(Math.round(outputSummaryDict.load_after_system),0,"no") + " MWh</td></tr>"
                    table_html += "<tr><td>Load Reduction</td><td>"+ numberFormat(Math.round(outputSummaryDict.load_reduction),0,"no") + " MWh</td></tr>"
                    table_html += "<tr><td>Load Reduction (%)</td><td>"+ numberFormat(Math.round(outputSummaryDict.load_reduction_percent*10)/10,0,"no") + " %</td></tr>"
                    table_html += "<tr><td>Greenhouse reduction</td><td>"+ outputSummaryDict.greenhouse_reduction  + " tCO2@-e</td></tr>"
                    table_html += "<tr align='center'><td colspan='2'><strong>System Summary</strong></td></tr>"
                    table_html += "<tr><td># of Lights</td><td>" + numberFormat(outputSummaryDict.num_led_lights,0,"no") + "</td></tr>"
                    table_html += "<tr><td>Solar kW</td><td>"+ numberFormat(outputSummaryDict.solar_size,2,"no") + " kW</td></tr>"
                    table_html += "<tr><td>PFC kvar</td><td>"+ numberFormat(outputSummaryDict.pfc_size,0,"no") +" kvar</td></tr>"
                    table_html += "<tr><td>Lighting Cost</td><td>"+ numberFormat(outputSummaryDict.lighting_cost,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>Solar Cost</td><td>"+ numberFormat(outputSummaryDict.solar_cost,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>Solar STCs</td><td>"+ numberFormat(outputSummaryDict.stc_discount,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>PFC Cost</td><td>"+ numberFormat(outputSummaryDict.pfc_cost,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>Total Cost</td><td>"+ numberFormat(outputSummaryDict.total_cost,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>Verdia Lighting Fee</td><td>"+ numberFormat(outputSummaryDict.verdia_lighting_fee_dollars,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>Verdia Solar Fee</td><td>"+ numberFormat(outputSummaryDict.verdia_solar_fee_dollars,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>Verdia PFC Fee</td><td>"+ numberFormat(outputSummaryDict.verdia_pfc_fee_dollars,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>Regional Fee</td><td>$0</td></tr>"
                    table_html += "<tr><td>Total Verdia Fee</td><td>"+ numberFormat(outputSummaryDict.total_verdia_fee_dollars,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>1st year Bill Savings</td><td>"+ numberFormat(outputSummaryDict.bill_savings_1st_year,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>1st year LGCs</td><td>"+ numberFormat(outputSummaryDict.LGCs_1st_year,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>1st year Lighting Maintenance Savings</td><td>"+ numberFormat(outputSummaryDict.lighting_maintenance_savings_1st_year,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>Feed in income 1st year</td><td>"+ numberFormat(outputSummaryDict.feed_in_income_1st_year,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>Operational costs 1st year</td><td>$0</td></tr>"
                    table_html += "<tr><td>Net Savings 1st year</td><td>"+ numberFormat(outputSummaryDict.net_savings_1st_year,0,"yes")+"</td></tr>"
                    table_html += "<tr align='center'><td colspan='2'><strong>Capex Summary</strong></td></tr>"
                    table_html += "<tr><td>Payback</td><td>"+ numberFormat(capexMetricsDict.payback,2,"no")  +" years</td></tr>"
                    table_html += "<tr><td>NPV 20 years @ 8%</td><td style='color:red;'>"+ numberFormat(capexMetricsDict.NPV,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>IRR 20 years</td><td>"+ numberFormat(capexMetricsDict.IRR*100,1,"no") +"%</td></tr>"
                    table_html += "<tr><td>LCOE 20 years @ 8%</td><td>"+ numberFormat(capexMetricsDict.LCOE,4,"yes") +" /kWh</td></tr>"
                    table_html += "<tr><td>Simplified 20 year solar cost</td><td>"+ numberFormat(capexMetricsDict.Simplified_LCOE,4,"yes") +" /kWh</td></tr>"
                    table_html += "<tr align='center'><td colspan='2'><strong>Finance Summary</strong></td></tr>"
                    table_html += "<tr><td>Cashflow Positive</td><td>16.0 years</td></tr>"
                    table_html += "<tr><td>NPV 20 years @ 8%</td><td style='color:red;'>-$57,478</td></tr>"
                    table_html += "</table></div>"
                    table_html += "<div class='col-10 col-md-6'>"
                    table_html += "<table class='table table-bordered'>"
                    table_html += "<tr align='center'><td colspan='2'><strong>Electricity Bill Summary</strong></td></tr>"
                    table_html += "<tr><td>Electricity Current Bill</td><td>"+ numberFormat(outputSummaryDict.electricity_current_bill,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>Electricity Bill 1st year (based on cashflow)</td><td>"+ numberFormat(outputSummaryDict.electricity_bill_1st_year,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>Electricity Bill 1st year after system</td><td>"+ numberFormat(outputSummaryDict.electricity_bill_after_system_1st_year,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>Electricity Bill Reduction 1st year</td><td>"+ numberFormat(outputSummaryDict.electricity_bill_reduction_percent_1st_year*100,1,"no") +"%</td></tr>"
                    table_html += "<tr><td>Electricity Cost Reduction</td><td>"+ numberFormat(outputSummaryDict.electricity_cost_reduction_percent_1st_year*100,1,"no") +"%</td></tr>"
                    table_html += "<tr align='center'><td colspan='2'><strong>Lighting Summary</strong></td></tr>"
                    table_html += "<tr><td>Maintenance savings 1st year</td><td>"+ numberFormat(outputSummaryDict.lighting_maintenance_savings_1st_year,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>Lighting load reduction</td><td>"+ numberFormat(outputSummaryDict.lighting_load_reduction_1st_year,0,"no") +" kWh</td></tr>"
                    table_html += "<tr><td>Lighting load reduction (%)</td><td>"+ numberFormat(outputSummaryDict.lighting_load_reduction_percent_1st_year*100,1,"no") +"%</td></tr>"
                    table_html += "<tr><td>Bill savings 1st year</td><td>"+ numberFormat(outputSummaryDict.lighting_bill_savings_1st_year,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>Total savings 1st year</td><td>"+ numberFormat(outputSummaryDict.lighting_total_savings_1st_year,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>Lighting simple payback</td><td>"+ numberFormat(outputSummaryDict.lighting_simple_payback,1,"no") +" years</td></tr>"
                    table_html += "<tr align='center'><td colspan='2'><strong>Solar and PFC Summary</strong></td></tr>"
                    table_html += "<tr><td>Solar generation (Ideal)</td><td>"+ numberFormat(outputSummaryDict.solar_generation_ideal_1st_year,0,"no") +" kWh</td></tr>"
                    table_html += "<tr><td>Solar Utilised</td><td>"+ numberFormat(outputSummaryDict.solar_generation_utilised_1st_year,0,"no") +" kWh</td></tr>"
                    table_html += "<tr><td>Solar Utilised (%)</td><td>"+ numberFormat(outputSummaryDict.solar_utilisation_percent*100,1,"no") +"%</td></tr>"
                    table_html += "<tr><td>Load reduction</td><td>"+ numberFormat(outputSummaryDict.solar_load_reduction_1st_year,0,"no") +" kWh</td></tr>"
                    table_html += "<tr><td>Load reduction (%)</td><td>"+ numberFormat(outputSummaryDict.solar_load_reduction_percent_1st_year*100,1,"no") +"%</td></tr>"
                    table_html += "<tr><td>Solar exported</td><td>"+ numberFormat(outputSummaryDict.solar_exported_1st_year,0,"no") +" kWh</td></tr>"
                    table_html += "<tr><td>Bill savings 1st year</td><td>"+ numberFormat(outputSummaryDict.solar_bill_savings_1st_year,0,"yes") +"</td></tr>"
                    table_html += "<tr><td>Maintenance costs 1st year</td><td>$0</td></tr>"
                    table_html += "<tr><td>Peak power factor before</td><td>"+ numberFormat(outputSummaryDict.peak_power_factor_before*100,1,"no") +"%</td></tr>"
                    table_html += "<tr><td>Peak power factor after</td><td>"+ numberFormat(outputSummaryDict.peak_power_factor_after*100,1,"no") +"%</td></tr>"
                    table_html += "<tr><td>Solar and PFC simple payback</td><td>"+ numberFormat(outputSummaryDict.solarpfc_simple_payback,1,"no") +" years</td></tr>"
                    table_html += "<tr align='center'><td colspan='2'><strong>Rates</strong></td></tr>"
                    table_html += "<tr><td>Blended Rate</td><td>"+ numberFormat(outputSummaryDict.blended_rate,4,"yes") +" /kWh</td></tr>"
                    table_html += "<tr><td>Solar PFC savings rate (Savings per kWh of Solar utilisation)</td><td>"+ numberFormat(outputSummaryDict.solarpfc_savings_rate,4,"yes") +" /kWh</td></tr>"
                    table_html += "<tr><td>Lighting Energy savings proportion (%)</td><td>"+ numberFormat(outputSummaryDict.lighting_energy_savings_proportion*100,1,"no") +"%</td></tr>"
                    table_html += "<tr><td>Solar PFC Energy savings proportion (%)</td><td>"+ numberFormat(outputSummaryDict.solarpfc_energy_savings_proportion*100,1,"no") +"%</td></tr>"
                    table_html += "<tr><td>Total Energy savings proportion</td><td>"+ numberFormat(outputSummaryDict.total_energy_savings_proportion*100,1,"no") +"%</td></tr>"
                    table_html += "<tr><td>Solar Energy bundled rate</td><td>"+ numberFormat(outputSummaryDict.solarpfc_energy_savings_rate,4,"yes") +" /kWh</td></tr>"
                    table_html += "</table></div>"
                    table_html += "</div>"
                    document.getElementById("div_outputs_summary").innerHTML = table_html;
                    

                    MonthlyLoadSummary = data.val.monthly_load_summary_dict                
                    MonthlyLoadSummarySum = data.val.monthly_load_summary_sum_dict
                    MonthlyLoadSummaryAverage = data.val.monthly_load_summary_average_dict

                    // Monthly Load Summary ------------------------------------------------------------------------------------------------------------
                                           
                        
                    table_html = "<div class='row'>"
                        
                    // Original Load
                    table_html += "<div class='col-10 col-xl-6'>"
                    table_html += "<table class='table table-bordered'>"
                    table_html += "<tr align='center'><td colspan='6'><strong>Original Load</strong></td></tr>"
                    table_html += "<tr align='center'><td colspan='2'><strong>Months</strong></td><td><strong>Total kWh</strong></td>"
                    table_html += "<td><strong>Peak kW</strong></td><td><strong>Peak kVA</strong></td><td><strong>PF</strong></td></tr>"
                    for (i=0;i<12;i++){
                        current_month = MonthlyLoadSummary.months[i]
                        current_kwhs = MonthlyLoadSummary.original_kwhs[i]
                        current_kW = MonthlyLoadSummary.original_kw[i]
                        current_kVA = MonthlyLoadSummary.original_kva[i]
                        current_PF = current_kW / current_kVA
                        table_html += "<tr>"
                        table_html += "<td>"+ current_month + "</td>"
                        table_html += "<td>"+ monthName(i) +"</td>"
                        table_html += "<td>"+ numberFormat(current_kwhs,0,"no") +"</td>"
                        table_html += "<td>"+ numberFormat(current_kW,0,"no") +"</td>"
                        table_html += "<td>"+ numberFormat(current_kVA,0,"no") +"</td>"
                        table_html += "<td>"+ numberFormat(current_PF*100,1,"no") +"%</td>"
                        table_html += "</tr>"

                    }
                    table_html += "<tr>"
                    table_html += "<td colspan='2'><strong>Yearly Summary</strong></td>"
                    table_html += "<td>"+ numberFormat(MonthlyLoadSummarySum.original_kwhs,0,"no") +"</td>"
                    table_html += "<td>"+ numberFormat(MonthlyLoadSummaryAverage.original_kw,0,"no") +"</td>"
                    table_html += "<td>"+ numberFormat(MonthlyLoadSummaryAverage.original_kva,0,"no") +"</td>"
                    table_html += "<td>"+ numberFormat(MonthlyLoadSummaryAverage.original_kw*100/MonthlyLoadSummaryAverage.original_kva,1,"no") +"%</td>"
                    table_html += "</tr>"   
                    
                    table_html += "</table></div>"
                    

                    // Load after lighting
                    table_html += "<div class='col-10 col-xl-6'>"
                    table_html += "<table class='table table-bordered'>"
                    table_html += "<tr align='center'><td colspan='6'><strong>Load after Lighting</strong></td></tr>"
                    table_html += "<tr align='center'><td colspan='2'><strong>Months</strong></td><td><strong>Total kWh</strong></td>"
                    table_html += "<td><strong>Peak kW</strong></td><td><strong>Peak kVA</strong></td><td><strong>PF</strong></td></tr>"
                    
                    for (i=0;i<12;i++){
                        current_month = MonthlyLoadSummary.months[i]
                        current_kwhs = MonthlyLoadSummary.after_lighting_kwhs[i]
                        current_kW = MonthlyLoadSummary.after_lighting_kw[i]
                        current_kVA = MonthlyLoadSummary.after_lighting_kva[i]
                        current_PF = current_kW / current_kVA
                        table_html += "<tr>"
                        table_html += "<td>"+ current_month + "</td>"
                        table_html += "<td>"+ monthName(i) +"</td>"
                        table_html += "<td>"+ numberFormat(current_kwhs,0,"no") +"</td>"
                        table_html += "<td>"+ numberFormat(current_kW,0,"no") +"</td>"
                        table_html += "<td>"+ numberFormat(current_kVA,0,"no") +"</td>"
                        table_html += "<td>"+ numberFormat(current_PF*100,1,"no") +"%</td>"
                        table_html += "</tr>"

                    }
                    table_html += "<tr>"
                    table_html += "<td colspan='2'><strong>Yearly Summary</strong></td>"
                    table_html += "<td>"+ numberFormat(MonthlyLoadSummarySum.after_lighting_kwhs,0,"no") +"</td>"
                    table_html += "<td>"+ numberFormat(MonthlyLoadSummaryAverage.after_lighting_kw,0,"no") +"</td>"
                    table_html += "<td>"+ numberFormat(MonthlyLoadSummaryAverage.after_lighting_kva,0,"no") +"</td>"
                    table_html += "<td>"+ numberFormat(MonthlyLoadSummaryAverage.after_lighting_kw*100/MonthlyLoadSummaryAverage.after_lighting_kva,1,"no") +"%</td>"
                    table_html += "</tr>"   
                    
                    table_html += "</table></div>"
                    table_html += "</div>" // row ends

                    table_html += "<div class='row'>"
                    
                    // Load after Lighting, Solar and PFC
                    table_html += "<div class='col-10 col-xl-6'>"
                    table_html += "<table class='table table-bordered'>"
                    table_html += "<tr align='center'><td colspan='6'><strong>Load after Lighting, Solar and PFC</strong></td></tr>"
                    table_html += "<tr align='center'><td colspan='2'><strong>Months</strong></td><td><strong>Total kWh</strong></td>"
                    table_html += "<td><strong>Peak kW</strong></td><td><strong>Peak kVA</strong></td><td><strong>PF</strong></td></tr>"
                    for (i=0;i<12;i++){
                        current_month = MonthlyLoadSummary.months[i]
                        current_kwhs = MonthlyLoadSummary.after_slp_kwhs[i]
                        current_kW = MonthlyLoadSummary.after_slp_kw[i]
                        current_kVA = MonthlyLoadSummary.after_slp_kva[i]
                        current_PF = current_kW / current_kVA
                        table_html += "<tr>"
                        table_html += "<td>"+ current_month + "</td>"
                        table_html += "<td>"+ monthName(i) +"</td>"
                        table_html += "<td>"+ numberFormat(current_kwhs,0,"no") +"</td>"
                        table_html += "<td>"+ numberFormat(current_kW,0,"no") +"</td>"
                        table_html += "<td>"+ numberFormat(current_kVA,0,"no") +"</td>"
                        table_html += "<td>"+ numberFormat(current_PF*100,1,"no") +"%</td>"
                        table_html += "</tr>"

                    }
                    table_html += "<tr>"
                    table_html += "<td colspan='2'><strong>Yearly Summary</strong></td>"
                    table_html += "<td>"+ numberFormat(MonthlyLoadSummarySum.after_slp_kwhs,0,"no") +"</td>"
                    table_html += "<td>"+ numberFormat(MonthlyLoadSummaryAverage.after_slp_kw,0,"no") +"</td>"
                    table_html += "<td>"+ numberFormat(MonthlyLoadSummaryAverage.after_slp_kva,0,"no") +"</td>"
                    table_html += "<td>"+ numberFormat(MonthlyLoadSummaryAverage.after_slp_kw*100/MonthlyLoadSummaryAverage.after_slp_kva,1,"no") +"%</td>"
                    table_html += "</tr>"   
                    
                    table_html += "</table></div>"
                    

                    // Total Savings
                    table_html += "<div class='col-10 col-xl-6'>"
                    table_html += "<table class='table table-bordered'>"
                    table_html += "<tr align='center'><td colspan='6'><strong>Total Savings</strong></td></tr>"
                    table_html += "<tr align='center'><td colspan='2'><strong>Months</strong></td><td><strong>Total kWh</strong></td>"
                    table_html += "<td><strong>Peak kW</strong></td><td><strong>Peak kVA</strong></td><td><strong>PF</strong></td></tr>"
                    
                    for (i=0;i<12;i++){
                        current_month = MonthlyLoadSummary.months[i]
                        current_kwhs = (MonthlyLoadSummary.original_kwhs[i] - MonthlyLoadSummary.after_slp_kwhs[i])
                        current_kW = (MonthlyLoadSummary.original_kw[i]- MonthlyLoadSummary.after_slp_kw[i])
                        current_kVA = (MonthlyLoadSummary.original_kva[i] - MonthlyLoadSummary.after_slp_kva[i])
                        current_PF = current_kW / current_kVA
                        table_html += "<tr>"
                        table_html += "<td>"+ current_month + "</td>"
                        table_html += "<td>"+ monthName(i) +"</td>"
                        table_html += "<td>"+ numberFormat(current_kwhs,0,"no") +"</td>"
                        table_html += "<td>"+ numberFormat(current_kW,0,"no") +"</td>"
                        table_html += "<td>"+ numberFormat(current_kVA,0,"no") +"</td>"
                        table_html += "<td>"+ numberFormat(current_PF*100,1,"no") +"%</td>"
                        table_html += "</tr>"

                    }
                    table_html += "<tr>"
                    table_html += "<td colspan='2'><strong>Yearly Summary</strong></td>"
                    table_html += "<td>"+ numberFormat(MonthlyLoadSummarySum.original_kwhs - MonthlyLoadSummarySum.after_slp_kwhs,0,"no") +"</td>"
                    table_html += "<td>"+ numberFormat(MonthlyLoadSummarySum.original_kw - MonthlyLoadSummarySum.after_slp_kw,0,"no") +"</td>"
                    table_html += "<td>"+ numberFormat(MonthlyLoadSummarySum.original_kva - MonthlyLoadSummarySum.after_slp_kva,0,"no") +"</td>"
                    temp_pf = (MonthlyLoadSummarySum.original_kw - MonthlyLoadSummarySum.after_slp_kw)/(MonthlyLoadSummarySum.original_kva - MonthlyLoadSummarySum.after_slp_kva)
                    table_html += "<td>"+ numberFormat(temp_pf*100,1,"no") +"%</td>"
                    table_html += "</tr>"   
                    
                    table_html += "</table></div>"
                    table_html += "</div>" // row ends

                    document.getElementById("div_load_summary").innerHTML = table_html;

                    // Solar Generation Summary ------------------------------------------------------------------------------------------------------------
                                            
                    table_html = "<div class='row'>"
                        
                    // Solar Generation
                    table_html += "<div class='col-10 col-xl-6'>"
                    table_html += "<table class='table table-bordered'>"
                    table_html += "<tr align='center'><td colspan='5'><strong>Solar Generation</strong></td></tr>"
                    table_html += "<tr align='center'><td colspan='2'><strong>Months</strong></td><td><strong>Solar Ideal</strong></td>"
                    table_html += "<td><strong>Solar Utilised</strong></td><td><strong>Utilisation (%)</strong></td></tr>"
                    for (i=0;i<12;i++){
                        current_month = MonthlyLoadSummary.months[i]
                        solar_ideal = MonthlyLoadSummary.solar_ideal[i]
                        solar_actual = MonthlyLoadSummary.solar_actual[i]
                        solar_utilisation = MonthlyLoadSummary.solar_utilisation[i]                     
                        table_html += "<tr>"
                        table_html += "<td>"+ current_month + "</td>"
                        table_html += "<td>"+ monthName(i) +"</td>"
                        table_html += "<td>"+ numberFormat(solar_ideal,0,"no") +"</td>"
                        table_html += "<td>"+ numberFormat(solar_actual,0,"no") +"</td>"                        
                        table_html += "<td>"+ numberFormat(solar_utilisation*100,1,"no") +"%</td>"
                        table_html += "</tr>"

                    }
                    table_html += "<tr>"
                    table_html += "<td colspan='2'><strong>Yearly Summary</strong></td>"
                    table_html += "<td>"+ numberFormat(MonthlyLoadSummarySum.solar_ideal,0,"no") +"</td>"
                    table_html += "<td>"+ numberFormat(MonthlyLoadSummarySum.solar_actual,0,"no") +"</td>"                    
                    table_html += "<td>"+ numberFormat(MonthlyLoadSummarySum.solar_actual*100/MonthlyLoadSummarySum.solar_ideal,1,"no") +"%</td>"
                    table_html += "</tr>"   
                    
                    table_html += "</table></div>"
                    table_html += "</div>" // row ends
                    document.getElementById("div_solar_generation_summary").innerHTML = table_html;

                    // Monthly Bill Summary -------------------------------------------------------------------------------
                    MonthlyBillSummary = data.val.monthly_bill_summary_dict                    
                    MonthlyBillSummarySum = data.val.monthly_bill_summary_sum_dict
                    MonthlyBillSummaryAverage = data.val.monthly_bill_summary_average_dict
               
                    table_html = "<div class='row'>"
                    
                    // Original Charges
                    table_html += "<div class='col-10 col-xl-6'>"
                    table_html += "<table class='table table-bordered'>"
                    table_html += "<tr align='center'><td colspan='6'><strong>Original Bill</strong></td></tr>"
                    table_html += "<tr align='center'><td colspan='2'><strong>Months</strong></td><td><strong>Volume Charges</strong></td>"
                    table_html += "<td><strong>Demand Charges</strong></td><td><strong>Supply charges</strong></td><td><strong>Total Bill</strong></td></tr>"
                    for (i=0;i<12;i++){
                        current_month = MonthlyBillSummary.months[i]
                        current_volume_charge = MonthlyBillSummary.original_volume_charges[i]
                        current_demand_charge = MonthlyBillSummary.original_demand_charges[i]
                        current_supply_charge = MonthlyBillSummary.fixed_charges[i]
                        current_total_bill = current_volume_charge + current_demand_charge + current_supply_charge
                        table_html += "<tr>"
                        table_html += "<td>"+ current_month + "</td>"
                        table_html += "<td>"+ monthName(i) +"</td>"
                        table_html += "<td>"+ numberFormat(current_volume_charge,0,"yes") +"</td>"
                        table_html += "<td>"+ numberFormat(current_demand_charge,0,"yes") +"</td>"
                        table_html += "<td>"+ numberFormat(current_supply_charge,0,"yes") +"</td>"
                        table_html += "<td>"+ numberFormat(current_total_bill,0,"yes") +"</td>"
                        table_html += "</tr>"

                    }
                    table_html += "<tr>"
                    table_html += "<td colspan='2'><strong>Yearly Summary</strong></td>"
                    table_html += "<td>"+ numberFormat(MonthlyBillSummarySum.original_volume_charges,0,"yes") +"</td>"
                    table_html += "<td>"+ numberFormat(MonthlyBillSummarySum.original_demand_charges,0,"yes") +"</td>"
                    table_html += "<td>"+ numberFormat(MonthlyBillSummarySum.fixed_charges,0,"yes") +"</td>"
                    temp_total_bill = MonthlyBillSummarySum.original_volume_charges + MonthlyBillSummarySum.original_demand_charges + MonthlyBillSummarySum.fixed_charges
                    table_html += "<td>"+ numberFormat(temp_total_bill,0,"yes") +"</td>"
                    table_html += "</tr>"   
                    
                    table_html += "</table></div>"
                    

                    // Charges after lighting
                    table_html += "<div class='col-10 col-xl-6'>"
                    table_html += "<table class='table table-bordered'>"
                    table_html += "<tr align='center'><td colspan='6'><strong>Bill after Lighting</strong></td></tr>"
                    table_html += "<tr align='center'><td colspan='2'><strong>Months</strong></td><td><strong>Volume Charges</strong></td>"
                    table_html += "<td><strong>Demand Charges</strong></td><td><strong>Supply charges</strong></td><td><strong>Total Bill</strong></td></tr>"
                    for (i=0;i<12;i++){
                        current_month = MonthlyBillSummary.months[i]
                        current_volume_charge = MonthlyBillSummary.after_lighting_volume_charges[i]
                        current_demand_charge = MonthlyBillSummary.after_lighting_demand_charges[i]
                        current_supply_charge = MonthlyBillSummary.fixed_charges[i]
                        current_total_bill = current_volume_charge + current_demand_charge + current_supply_charge
                        table_html += "<tr>"
                        table_html += "<td>"+ current_month + "</td>"
                        table_html += "<td>"+ monthName(i) +"</td>"
                        table_html += "<td>"+ numberFormat(current_volume_charge,0,"yes") +"</td>"
                        table_html += "<td>"+ numberFormat(current_demand_charge,0,"yes") +"</td>"
                        table_html += "<td>"+ numberFormat(current_supply_charge,0,"yes") +"</td>"
                        table_html += "<td>"+ numberFormat(current_total_bill,0,"yes") +"</td>"
                        table_html += "</tr>"

                    }
                    table_html += "<tr>"
                    table_html += "<td colspan='2'><strong>Yearly Summary</strong></td>"
                    table_html += "<td>"+ numberFormat(MonthlyBillSummarySum.after_lighting_volume_charges,0,"yes") +"</td>"
                    table_html += "<td>"+ numberFormat(MonthlyBillSummarySum.after_lighting_demand_charges,0,"yes") +"</td>"
                    table_html += "<td>"+ numberFormat(MonthlyBillSummarySum.fixed_charges,0,"yes") +"</td>"
                    temp_total_bill = MonthlyBillSummarySum.after_lighting_volume_charges + MonthlyBillSummarySum.after_lighting_demand_charges + MonthlyBillSummarySum.fixed_charges
                    table_html += "<td>"+ numberFormat(temp_total_bill,0,"yes") +"</td>"
                    table_html += "</tr>" 
                    
                    table_html += "</table></div>"
                    table_html += "</div>" // row ends

                    table_html += "<div class='row'>"
                    
                    // Bill after Lighting, Solar and PFC
                    table_html += "<div class='col-10 col-xl-6'>"
                    table_html += "<table class='table table-bordered'>"
                    table_html += "<tr align='center'><td colspan='6'><strong>Bill after Lighting, Solar and PFC</strong></td></tr>"
                    table_html += "<tr align='center'><td colspan='2'><strong>Months</strong></td><td><strong>Volume Charges</strong></td>"
                    table_html += "<td><strong>Demand Charges</strong></td><td><strong>Supply charges</strong></td><td><strong>Total Bill</strong></td></tr>"
                    for (i=0;i<12;i++){
                        current_month = MonthlyBillSummary.months[i]
                        current_volume_charge = MonthlyBillSummary.after_slp_volume_charges[i]
                        current_demand_charge = MonthlyBillSummary.after_slp_demand_charges[i]
                        current_supply_charge = MonthlyBillSummary.fixed_charges[i]
                        current_total_bill = current_volume_charge + current_demand_charge + current_supply_charge
                        table_html += "<tr>"
                        table_html += "<td>"+ current_month + "</td>"
                        table_html += "<td>"+ monthName(i) +"</td>"
                        table_html += "<td>"+ numberFormat(current_volume_charge,0,"yes") +"</td>"
                        table_html += "<td>"+ numberFormat(current_demand_charge,0,"yes") +"</td>"
                        table_html += "<td>"+ numberFormat(current_supply_charge,0,"yes") +"</td>"
                        table_html += "<td>"+ numberFormat(current_total_bill,0,"yes") +"</td>"
                        table_html += "</tr>"

                    }
                    table_html += "<tr>"
                    table_html += "<td colspan='2'><strong>Yearly Summary</strong></td>"
                    table_html += "<td>"+ numberFormat(MonthlyBillSummarySum.after_slp_volume_charges,0,"yes") +"</td>"
                    table_html += "<td>"+ numberFormat(MonthlyBillSummarySum.after_slp_demand_charges,0,"yes") +"</td>"
                    table_html += "<td>"+ numberFormat(MonthlyBillSummarySum.fixed_charges,0,"yes") +"</td>"
                    temp_total_bill = MonthlyBillSummarySum.after_slp_volume_charges + MonthlyBillSummarySum.after_slp_demand_charges + MonthlyBillSummarySum.fixed_charges
                    table_html += "<td>"+ numberFormat(temp_total_bill,0,"yes") +"</td>"
                    table_html += "</tr>" 
                    
                    table_html += "</table></div>"
                    

                    // Total Savings
                    table_html += "<div class='col-10 col-xl-6'>"
                    table_html += "<table class='table table-bordered'>"
                    table_html += "<tr align='center'><td colspan='6'><strong>Total Bill Savings</strong></td></tr>"
                    table_html += "<tr align='center'><td colspan='2'><strong>Months</strong></td><td><strong>Volume Charges</strong></td>"
                    table_html += "<td><strong>Demand Charges</strong></td><td><strong>Supply charges</strong></td><td><strong>Total Bill</strong></td></tr>"
                    for (i=0;i<12;i++){
                        current_month = MonthlyBillSummary.months[i]
                        current_volume_charge = MonthlyBillSummary.original_volume_charges[i] - MonthlyBillSummary.after_slp_volume_charges[i]
                        current_demand_charge = MonthlyBillSummary.original_demand_charges[i] - MonthlyBillSummary.after_slp_demand_charges[i]
                        current_supply_charge = 0
                        current_total_bill = current_volume_charge + current_demand_charge + current_supply_charge
                        table_html += "<tr>"
                        table_html += "<td>"+ current_month + "</td>"
                        table_html += "<td>"+ monthName(i) +"</td>"
                        table_html += "<td>"+ numberFormat(current_volume_charge,0,"yes") +"</td>"
                        table_html += "<td>"+ numberFormat(current_demand_charge,0,"yes") +"</td>"
                        table_html += "<td>"+ numberFormat(current_supply_charge,0,"yes") +"</td>"
                        table_html += "<td>"+ numberFormat(current_total_bill,0,"yes") +"</td>"
                        table_html += "</tr>"

                    }
                    table_html += "<tr>"
                    table_html += "<td colspan='2'><strong>Yearly Summary</strong></td>"
                    table_html += "<td>"+ numberFormat(MonthlyBillSummarySum.original_volume_charges - MonthlyBillSummarySum.after_slp_volume_charges,0,"yes") +"</td>"
                    table_html += "<td>"+ numberFormat(MonthlyBillSummarySum.original_demand_charges - MonthlyBillSummarySum.after_slp_demand_charges,0,"yes") +"</td>"
                    table_html += "<td>"+ numberFormat(0,0,"yes") +"</td>"
                    temp_total_savings = MonthlyBillSummarySum.original_volume_charges - MonthlyBillSummarySum.after_slp_volume_charges + MonthlyBillSummarySum.original_demand_charges - MonthlyBillSummarySum.after_slp_demand_charges
                    table_html += "<td>"+ numberFormat(temp_total_savings,0,"yes") +"</td>"
                    table_html += "</tr>"
                    
                    table_html += "</table></div>"
                    table_html += "</div>" // row ends

                    document.getElementById("div_bill_summary").innerHTML = table_html;
                    
                    


                    




                }
    }
    request.send(params);
}