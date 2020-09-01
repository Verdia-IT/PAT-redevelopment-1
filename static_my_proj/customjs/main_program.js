


$(document).ready(function () {

	var $ProgramContactDetailsForm = $('#form_program_contact_details');
	$ProgramContactDetailsForm.submit(function (event) {
		event.preventDefault();
		saveProgramContactDetails();
	});
	var $ProgramOverridesForm = $('#form_program_overrides');
	$ProgramOverridesForm.submit(function (event) {
		event.preventDefault();
		saveProgramOverrides();
	});

	var $NewSiteModalForm = $('#modal_form_new_site');
	$NewSiteModalForm.submit(function (event) {
		event.preventDefault();
		saveNewSite();
	});

	$('.btn-close-new-site').click(closeNewSiteModal);
	showSites();

	$('#btn_run_simulations').click(runSimulations);

});


function saveProgramContactDetails() {
	var $ProgramContactDetailsForm = $('#form_program_contact_details');
	var url = '/programs/save_new_program/'
	programId = document.getElementById("hidden_program_id").value;
	var $formData = $ProgramContactDetailsForm.serialize() + '&programId=' + programId;
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
						deleteErrorMessage("error_form_program_program_name")
						deleteErrorMessage("error_form_program_salesforce_id")
						deleteErrorMessage("error_form_program_contact_name")
						deleteErrorMessage("error_form_program_contact_title")
						deleteErrorMessage("error_form_program_contact_email")
						deleteErrorMessage("error_form_program_contact_phone")
					}
					else {

						if ("program_name" in data.message) {
							createErrorMessage("error_form_program_program_name", data.message.program_name)
						}
						else {
							deleteErrorMessage("error_form_program_program_name")
						}
						if ("salesforce_id" in data.message) {
							createErrorMessage("error_form_program_salesforce_id", data.message.salesforce_id)
						}
						else {
							deleteErrorMessage("error_form_program_salesforce_id")
						}
						if ("contact_name" in data.message) {
							createErrorMessage("error_form_program_contact_name", data.message.contact_name)
						}
						else {
							deleteErrorMessage("error_form_program_contact_name")
						}
						if ("contact_title" in data.message) {
							createErrorMessage("error_form_program_contact_title", data.message.contact_title)
						}
						else {
							deleteErrorMessage("error_form_program_contact_title")
						}
						if ("contact_email" in data.message) {
							createErrorMessage("error_form_program_contact_email", data.message.contact_email)
						}
						else {
							deleteErrorMessage("error_form_program_contact_email")
						}
						if ("contact_phone" in data.message) {
							createErrorMessage("error_form_program_contact_phone", data.message.contact_phone)
						}
						else {
							deleteErrorMessage("error_form_program_contact_phone")
						}
					}

				}
	}
	request.send($formData);
}

function saveProgramOverrides() {
	var $ProgramOverridesForm = $('#form_program_overrides');
	var url = '/programs/save_program_overrides/'
	programId = document.getElementById("hidden_program_id").value;
	var $formData = $ProgramOverridesForm.serialize() + '&programId=' + programId;
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
						deleteErrorMessage("error_form_program_overrides_cashflow_start_month")
						deleteErrorMessage("error_form_program_overrides_cashflow_start_year")
						deleteErrorMessage("error_form_program_overrides_discount_rate")						
					}
					else {

						if ("cashflow_start_month" in data.message) {
							createErrorMessage("error_form_program_overrides_cashflow_start_month", data.message.cashflow_start_month)
						}
						else {
							deleteErrorMessage("error_form_program_overrides_cashflow_start_month")
						}
						if ("cashflow_start_year" in data.message) {
							createErrorMessage("error_form_program_overrides_cashflow_start_year", data.message.cashflow_start_year)
						}
						else {
							deleteErrorMessage("error_form_program_overrides_cashflow_start_year")
						}
						if ("discount_rate" in data.message) {
							createErrorMessage("error_form_program_overrides_discount_rate", data.message.discount_rate)
						}
						else {
							deleteErrorMessage("error_form_program_overrides_discount_rate")
						}					
					}

				}
	}
	request.send($formData);
}


function saveNewSite() {
	var url = '/sites/save_new_site/'
	var $NewSiteModalForm = $('#modal_form_new_site');
	var programId = document.getElementById("hidden_program_id").value;
	var siteId = "";
	var $formData = $NewSiteModalForm.serialize() + '&siteId=' + siteId + '&programId=' + programId;
	console.log($formData);
	request = new ajaxRequest()
	request.open("POST", url, true)
	request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
	request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
	request.onreadystatechange = function () {
		if (this.readyState == 4)
			if (this.status == 200)
				if (this.responseText != null) {
					clearNewSiteModalErrors();
					console.log(this.responseText);
					var data = JSON.parse(this.responseText);
					console.log(typeof data.message)
					if (data.message == "Success") {
						clearNewSiteModal();
						$('#modal-new-site').modal("hide");
						showSites();
					}
					else {

						if ((typeof data.message) == "string") {
							createErrorMessage("new_site_modal_save_message", data.message)
						}
						else {
							if ("site_name" in data.message) {
								createErrorMessage("error_new_site_modal_site_name", data.message.site_name)
							}
							if ("NMI" in data.message) {
								createErrorMessage("error_new_site_modal_NMI", data.message.NMI)
							}

							if ("street_address" in data.message) {
								createErrorMessage("error_new_site_modal_street_address", data.message.street_address)
							}

							if ("city" in data.message) {
								createErrorMessage("error_new_site_modal_city", data.message.city)
							}

							if ("state" in data.message) {
								createErrorMessage("error_new_site_modal_state", data.message.state)
							}

							if ("postcode" in data.message) {
								createErrorMessage("error_new_site_modal_postcode", data.message.postcode)
							}

							if ("DNSP" in data.message) {
								createErrorMessage("error_new_site_modal_DNSP", data.message.DNSP)
							}

							if ("industry_type" in data.message) {
								createErrorMessage("error_new_site_modal_industry_type", data.message.industry_type)
							}

							if ("default_solar_data" in data.message) {
								createErrorMessage("error_new_site_modal_default_solar_data", data.message.default_solar_data)
							}

						}


					}

				}
	}
	request.send($formData);

}


function clearNewSiteModal() {
	document.getElementById("modal_new_site_site_name").value = "";
	document.getElementById("modal_new_site_NMI").value = "";
	document.getElementById("modal_new_site_street_address").value = "";
	document.getElementById("modal_new_site_city").value = "";
	document.getElementById("modal_new_site_state").value = "";
	document.getElementById("modal_new_site_postcode").value = "";
	document.getElementById("modal_new_site_DNSP").value = "";
	document.getElementById("modal_new_site_industry_type").value = "";
	document.getElementById("modal_new_site_default_solar_data").value = "";
	clearNewSiteModalErrors();
}

function clearNewSiteModalErrors() {
	deleteErrorMessage("new_site_modal_save_message");
	deleteErrorMessage("error_new_site_modal_site_name");
	deleteErrorMessage("error_new_site_modal_NMI");
	deleteErrorMessage("error_new_site_modal_street_address");
	deleteErrorMessage("error_new_site_modal_city");
	deleteErrorMessage("error_new_site_modal_state");
	deleteErrorMessage("error_new_site_modal_postcode");
	deleteErrorMessage("error_new_site_modal_DNSP");
	deleteErrorMessage("error_new_site_modal_industry_type");
	deleteErrorMessage("error_new_site_modal_default_solar_data");
	deleteErrorMessage("new_site_modal_save_message");


}


function closeNewSiteModal() {
	clearNewSiteModal();
	$('#modal-new-site').modal("hide");
}


function showSites() {
	var url = '/sites/show_sites/'
	var obj = new Object;
	obj.programId = document.getElementById("hidden_program_id").value;
	console.log(obj.programId)

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
					// console.log(this.responseText);
					var data = JSON.parse(this.responseText);
					if (data.message == 'Success') {
						table_html = []
						if (data.site_value.length > 0) {
							for (i = 0; i < data.site_value.length; i++) {
								table_html = table_html +
									(
										"<tr align='center'>" +
										"<td>" + (i + 1) + "</td>" +
										"<td>" + data.site_value[i].site_name + "</td>"
									)
									table_html = table_html + "<td><select onchange='selectInclude(this,"+ data.site_value[i].id +")'>" 
									if(data.site_value[i].included == true){
										table_html = table_html +
										(												
											"<option selected>Yes</option>" +
											"<option>No</option>" 												
										)
									} 
									else{
										table_html = table_html +
											(												
											"<option>Yes</option>" +
											"<option selected>No</option>" 
											
										)
									}
									selected_j = -1;
									for (j=0; j < data.scenario_value.length; j++){
										if(data.site_value[i].site_name == data.scenario_value[j].site_name){	
											selected_j = 0
										}
									}
									if(selected_j == -1){
										table_html = table_html + "</select></td><td>No Scenarios"
									}
									else{
										table_html = table_html + "</select></td><td><select onchange='selectScenario(this)'>"
									}										
									// console.log('Scenario Value Length: ',data.scenario_value.length);
									selected_j = -1;	
									for (j=0; j < data.scenario_value.length; j++){
										// console.log(data.site_value[i].site_name,data.scenario_value.site_name)																					
										if(data.site_value[i].site_name == data.scenario_value[j].site_name){																									
											if (data.scenario_value[j].chosen == true){
												table_html = table_html + " <option selected value="+ data.scenario_value[j].id +">"+ data.scenario_value[j].scenario_name + "</option>"
												selected_j = j;
											}	
											else{
												if(selected_j == -1){
													selected_j = j;
												}
												table_html = table_html + " <option value="+ data.scenario_value[j].id +">"+ data.scenario_value[j].scenario_name + "</option>"
											}							 
											
										}
									}										
									if(selected_j == -1){
										table_html = table_html + "</td><td></td>"
									}
									else{
										table_html = table_html + "</select></td><td>"+ data.scenario_value[selected_j].summary +"</td>"
									}
									table_html = table_html + (																			
										"<td>" +
										"<div class='row'>" +
										"<div class='col-4'>" +
										"<form method='post' action='/sites/main_site/'>" +											
										"<input type='hidden' name='hidden_site_id' value='" + data.site_value[i].id + "'>" +
										"<input type='hidden' name='csrfmiddlewaretoken' value='" + csrfcookie() + "'>" +
										"<button type='submit' class='btn text-secondary px-0 d-inline'><i class='far fa-edit fa-lg'></i></button>" +

										"</form>" +
										"</div>" +
										"<div class='col-4'>" +
										"<button class='btn text-secondary px-0 d-inline' onclick='deleteSite(" + data.site_value[i].id + ")';>" +
										"<i class='far fa-trash-alt fa-lg text-danger'></i></button>" +

										"</div>" +
										"</div>" +
										"</td>" +
										"</tr>"
									)

							}
						}
						document.getElementById("tbl_sites_body").innerHTML = table_html
						deleteErrorMessage("div_sites_error")
					}
					else {
						createErrorMessage("div_sites_error", data.message)
					}



				}
	}
	request.send(params);


}


function deleteSite(siteId) {
	var url = '/sites/delete_site/'
	var obj = new Object;
	obj.siteId = siteId;

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
						showSites();
						deleteErrorMessage("div_sites_error")
					}
					else {
						createErrorMessage("div_sites_error", data.message)
					}

				}
	}
	request.send(params);
}


function selectScenario(element){
	var url = '/scenarios/choose_scenario/'
	var obj = new Object;
	obj.scenarioId = element.value;
	JSONobj = JSON.stringify(obj);
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
					if(data.message == 'Success') {
						showSites();						
					}
					else {
						createErrorMessage("div_sites_error", data.message)
					}
				}
	}
	request.send(params);

	
}

function selectInclude(element, siteId){
	var url = '/sites/include_site/'
	var obj = new Object;
	obj.include = element.value;
	obj.siteId = siteId;
	JSONobj = JSON.stringify(obj);
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
					// console.log(this.responseText);
					var data = JSON.parse(this.responseText);
					if(data.message == 'Success') {
						showSites();						
					}
					else {
						createErrorMessage("div_sites_error", data.message)
					}
				}
	}
	request.send(params);
}


function runSimulations(){
	var url = '/programs/run_simulations/'
	var obj = new Object; 
	obj.programId = document.getElementById("hidden_program_id").value;
	JSONobj = JSON.stringify(obj);
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
					if(data.message == 'Success') {
						alert("Success")
						showSites();
						var test = 0
						if (test != 1){
							document.getElementById("id_program_output_solar_size").innerHTML = "<strong>" + numberFormat2(data.Program_Output.solar_size, 0, "no") + " kW</strong>"
							document.getElementById("id_program_output_solar_size_desc").innerHTML = "Solar PV installation across <br> " + data.Program_Output.num_sites + " sites"
							document.getElementById("id_program_output_led").innerHTML = "<strong>" + numberFormat2(data.Program_Output.num_led,0,"no") + "</strong>"
							document.getElementById("id_program_output_led_desc").innerHTML = "Lights upgraded across <br>" + data.Program_Output.num_sites + " sites"
							document.getElementById("id_program_output_savings_yr_1_dollar").innerHTML = "<strong>" + numberFormat2(data.Program_Output.savings_yr_1_dollar,0,"yes") + "</strong>"
							document.getElementById("id_program_output_savings_yr_1_dollar_desc").innerHTML = "Est. savings year 1 of "+ numberFormat2(data.Program_Output.electricity_current_bill,0,"yes")+" current spend"
							document.getElementById("id_program_output_savings_yr_1_energy").innerHTML = "<strong>" + numberFormat2(data.Program_Output.savings_yr_1_energy,0,"no") + " MWh</strong>"
							temp_var = (data.Program_Output.savings_yr_1_energy*1000 / data.Program_Output.base_load_kwh)*100
							document.getElementById("id_program_output_savings_yr_1_energy_desc").innerHTML = "Energy savings year 1.<br>"+ numberFormat2(temp_var,0,"no") + "% of "+ numberFormat2(data.Program_Output.base_load_kwh/1000,0,"no") +" MWh"
							document.getElementById("id_program_output_payback").innerHTML = "<strong>" + numberFormat2(data.Program_Output.payback,1,"No") + " years</strong>"
							document.getElementById("id_program_output_payback_desc").innerHTML = "Break Even Period.<br> Based on projected cashflow"
							document.getElementById("id_program_output_npv").innerHTML = "<strong>" + numberFormat2(data.Program_Output.npv,0,"yes") + "</strong>"
							document.getElementById("id_program_output_npv_desc").innerHTML = "NPV <br> 20 years <br>"
							document.getElementById("id_program_output_irr").innerHTML = "<strong>" + numberFormat2(data.Program_Output.irr*100,1,"no") + "%</strong>"
							document.getElementById("id_program_output_irr_desc").innerHTML = "Stand-alone program IRR <br> 20 years"
						}			
						
					}
					else {
						createErrorMessage("div_sites_error", data.message)
					}
				}
	}
	request.send(params);
}