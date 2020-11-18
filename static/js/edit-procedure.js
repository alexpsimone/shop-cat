'use strict';

// Toggle the label change field to active/inactive for changes based on
// checkbox selection. Checked box means the user wishes to delete the label,
// so make the label unavailable for edits.
$('#label-remove').on('change', () => {
    if ($('#label-remove').is(':checked')) {
        $('#label').prop('disabled', true);
    } else {
        $('#label').prop('disabled', false);
    };
});


function removeTool (evt) {

    evt.preventDefault();

    const toolButton = evt.target;
    const toolName = toolButton['value'];

    $(`#row-${toolName}`).remove();

    let NUM_TOOLS = Number($('#NUM_TOOLS').val());
    NUM_TOOLS -= 1;

    $('#NUM_TOOLS').replaceWith(`<input name="NUM_TOOLS" id="NUM_TOOLS" 
                                    type="hidden" value="${NUM_TOOLS}" />`);
}


function addTool (evt) {

    evt.preventDefault();
    
    let NUM_TOOLS = Number($('#NUM_TOOLS').val());
    NUM_TOOLS += 1;

    $.get('/get-tools.json', (res) => { 
        
        let str = '';
        for (const tool of res) {
            str = str + `<option value="${tool}">${tool}</option>`;
        }

        $('#tools').append(
            `<br />
            <label>New Tool: </label>
            <select name="tool_req_${NUM_TOOLS}" class="tool-req" id="tool${NUM_TOOLS}">
            <option value="">--Please select a tool--</option>
            ${str}
            <option value="other">Other (please specify)...</option>
            </select>
            <br /><label>If other, please specify: </label>
            <input type="text" name="tool_other_${NUM_TOOLS}" />
            <br />`
        );

    });

    $('#NUM_TOOLS').replaceWith(`<input name="NUM_TOOLS" id="NUM_TOOLS" 
                                    type="hidden" value="${NUM_TOOLS}" />`);
    
}

function removePart (evt) {

    evt.preventDefault();

    const partButton = evt.target;
    const partName = partButton['value'];

    $(`#row-${partName}`).remove();

    let NUM_PARTS = Number($('#NUM_PARTS').val());
    NUM_PARTS -= 1;

    $('#NUM_PARTS').replaceWith(`<input name="NUM_PARTS" id="NUM_PARTS" 
                                    type="hidden" value="${NUM_PARTS}" />`);
}


function addPart (evt) {

    evt.preventDefault();
    
    let NUM_PARTS = Number($('#NUM_PARTS').val());
    NUM_PARTS += 1;

    $.get('/get-parts.json', (res) => { 
        
        let str = '';
        for (const part of res) {
            str = str + `<option value="${part}">${part}</option>`;
        }

        $('#parts').append(
            `<br />
            <label>New Part: </label>
            <select name="part_req_${NUM_PARTS}" class="part-req" id="part${NUM_PARTS}">
            <option value="">--Please select a part--</option>
            ${str}
            <option value="other">Other (please specify)...</option>
            </select>
            <br /><label>If other, please specify name: </label>
            <input type="text" name="part_${NUM_PARTS}_other_name" />
            <br /><label>If other, please specify P/N: </label>
            <input type="text" name="part_${NUM_PARTS}_other_num" />
            <br /><label>If other, please specify manuf: </label>
            <input type="text" name="part_${NUM_PARTS}_other_manuf" />
            <br /><label>If other, please specify if OEM: </label>
            <input type="radio" name="oem_${NUM_PARTS}" value="True" />
            <label for="is_oem_1">OEM</label>
            <input type="radio" name="oem1" value="False" />
            <label for="not_oem_1">Aftermarket</label>
            <input type="radio" name="oem1" value="False" />
            <label for="unsure_if_oem_1">Not Sure</label>
            <br />`
        );

    });

    $('#NUM_PARTS').replaceWith(`<input name="NUM_PARTS" id="NUM_PARTS" 
                                    type="hidden" value="${NUM_PARTS}" />`);
}


function addVehicle (evt) {

    evt.preventDefault();
    $('#car-add-form').show()

}


function getModels (evt) {

    evt.preventDefault();

    const formData = {
        make: $('#make').val(),
        modelYear: $('#model-year').val()
    };

    console.log(formData.make);
    console.log(formData.modelYear);

    $.get('/get-models.json', formData, (res) => {

        let str = '';
        for (const model of res) {
            str = str + `<option value="${model}">${model}</option>`;
        }
        $('#model-select').replaceWith(
            `<select id="model-select" name="model">
            <option value="">--Please select a Model--</option>
            ${str}
            <option value="other">Other (please specify)...</option>
            </select>`
        );
    })

    $('#model-select').attr('disabled', false);
    $('#vehicle-submit').attr('disabled', false);
}


function selectAddlVehicle (evt) {

    evt.preventDefault();

    let numCars = Number($('#NUM_CARS').val());
    numCars += 1;

    const formData = {
        make: $('#make').val(),
        modelYear: $('#model-year').val(),
        model: $('#model-select').val()
    };

    $.post('/vehicle-select.json', formData, (res) => {
        $('#all-cars').append(`<li id="item-${res['model_year']}-${res['make']}-${res['model']}">
                                ${res['model_year']}
                                ${res['make']}
                                ${res['model']}
                                <input type="checkbox"
                                    class="car-remove"
                                    id="remove-${res['model_year']}-${res['make']}-${res['model']}"
                                    name="remove-${res['model_year']}-${res['make']}-${res['model']}" />
                                <label for="remove-${res['model_year']}-${res['make']}-${res['model']}">
                                    Remove This Vehicle
                                </label>
                                </li>`)
    });

    $('#NUM_CARS').replaceWith(`<input name="NUM_CARS" 
                                id="NUM_CARS" type="number" 
                                value="${numCars}" 
                                style="display: none;"/>`);

    $('checkbox.car-remove').attr('disabled', false);
    $('#car-add-form').hide();
}


// function moveStepUp (evt) {

//     evt.preventDefault();

//     const stepButton = evt.target;
//     const stepID = stepButton['value'];
//     const NUM_STEPS = Number($('#NUM_STEPS').val());

//     const currentStepOrder = Number($(`#order-${stepID}`).val());
//     console.log(currentStepOrder);
    
//     if (currentStepOrder > 1) {
//         console.log(stepID);
//         for (NUM_STEP in NUM_STEPS) {

//         }

//     }

// }

$('#car-add').on('click', addVehicle);
$('#make').on('change', getModels);
$('#vehicle-submit').on('click', selectAddlVehicle);

$('button.remove-tool').on('click', removeTool);
$('#tool-add').on('click', addTool);

$('button.remove-part').on('click', removePart);
$('#part-add').on('click', addPart);

// $('button.move-up').on('click', moveStepUp);
