'use strict';

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
            `<tr class="border-top">
                <td class="name-order">
                <input type="hidden" class="tool-order" name="order" value="${NUM_TOOLS}" />
                <input type="hidden" class="tool-id" name="tool-id-${NUM_TOOLS}" value="NEW" />
                <label>New Tool: </label>
                <select class="tool-name custom-select" name="tool-name-${NUM_TOOLS}" required>
                <option value="">Please Select a Tool</option>
                ${str}
                <option value="other">Other (please specify)...</option>
                </select>
                <label for="tool-other-name">If other, please specify: </label>
                <input type="text" class="tool-other-name form-control" name="tool-other-name-${NUM_TOOLS}" />
                </td>
                <td class="img">
                <input type="hidden" class="tool-existing-img form-control" name="tool-existing-img-${NUM_TOOLS}" value="toolbox.png" />
                <label for="tool-img">If other, add image (optional): </label>
                <input type="file" class="tool-img form-control-file" name="tool-img-${NUM_TOOLS}" />
                </td>
                <td>
                <button class="remove-tool btn btn-primary">Remove Tool</button>
                </td>
            </tr>`
        );

        $('button.remove-tool').off();
        $('button.edit').off();
        $('button.del-img').off();
        $('select.tool-name').off();
        $('select.tool-name').on('change', requireOtherToolName);
        $('button.remove-tool').on('click', removeTool);
        $('button.edit').on('click', enableEditField);
        $('button.del-img').on('click', restoreDefaultImg);

    });

    $('#NUM_TOOLS').replaceWith(`<input name="NUM_TOOLS" id="NUM_TOOLS" 
                                    type="hidden" value="${NUM_TOOLS}" />`);
    
}

function requireOtherToolName (evt) {

    
    const thisSelect = evt.target;
    const otherName = $(thisSelect).siblings('input.tool-other-name');
    console.log(otherName);

    if ($(thisSelect).val() === 'other') {
        $(otherName).attr('required', true);
    } else {
        $(otherName).attr('required', false);
    };
}


function removeTool (evt) {

    evt.preventDefault();

    const thisButton = evt.target;
    const thisRow = $(thisButton).closest('tr');

    const nextLength = ($(thisRow).nextAll('tr')).length;

    for (let row = 0; row < nextLength; row += 1) {
        
        const nextRow = $(thisRow).nextAll('tr')[row];
        const nameOrderColumn = $(nextRow).children('td.name-order');
        const orderInput = $(nameOrderColumn).children('input.tool-order');
        const newOrder = Number($(orderInput).val()) - 1;
        $(orderInput).attr('value', newOrder);

        const toolInputID = $(nameOrderColumn).children('input.tool-id');
        $(toolInputID).attr('name', `tool-id-${newOrder}`);
        const toolInputName = $(nameOrderColumn).children('input.tool-name');
        $(toolInputName).attr('name', `tool-name-${newOrder}`);
        const toolSelectName = $(nameOrderColumn).children('select.tool-name');
        $(toolSelectName).attr('name', `tool-name-${newOrder}`);
        const toolInputOtherName = $(nameOrderColumn).children('input.tool-other-name');
        $(toolInputOtherName).attr('name', `tool-other-name-${newOrder}`);

        const imgColumn = $(nextRow).children('td.img');
        const toolInputExistingImg = $(imgColumn).children('input.tool-existing-img');
        $(toolInputExistingImg).attr('name', `tool-existing-img-${newOrder}`)
        const toolInputImg = $(imgColumn).children('input.tool-img');
        $(toolInputImg).attr('name', `tool-img-${newOrder}`);

    };

    $(thisRow).remove();

    let NUM_TOOLS = Number($('#NUM_TOOLS').val());
    NUM_TOOLS -= 1;

    $('#NUM_TOOLS').replaceWith(`<input name="NUM_TOOLS" id="NUM_TOOLS" 
                                    type="hidden" value="${NUM_TOOLS}" />`);
}


function removePart (evt) {

    evt.preventDefault();

    const thisButton = evt.target;
    const thisRow = $(thisButton).closest('tr');

    const nextLength = ($(thisRow).nextAll('tr')).length;

    for (let row = 0; row < nextLength; row += 1) {
        
        const nextRow = $(thisRow).nextAll('tr')[row];
        const nameOrderColumn = $(nextRow).children('td.name-order');
        const orderInput = $(nameOrderColumn).children('input.part-order');
        const newOrder = Number($(orderInput).val()) - 1;    
        $(orderInput).attr('value', newOrder);

        const partInputID = $(nameOrderColumn).children('input.part-id');
        $(partInputID).attr('name', `part-id-${newOrder}`);
        const partInputName = $(nameOrderColumn).children('input.part-name');
        $(partInputName).attr('name', `part-name-${newOrder}`);
        const partSelectName = $(nameOrderColumn).children('select.part-name');
        $(partSelectName).attr('name', `part-name-${newOrder}`);
        const partInputOtherName = $(nameOrderColumn).children('input.part-other-name');
        $(partInputOtherName).attr('name', `part-other-name-${newOrder}`);

        const partInputOtherPN = $(nameOrderColumn).children('input.part-other-pn');
        $(partInputOtherPN).attr('name', `part-other-pn-${newOrder}`);
        const partInputOtherManuf = $(nameOrderColumn).children('input.part-other-manuf');
        $(partInputOtherManuf).attr('name', `part-other-manuf-${newOrder}`);
        const partInputOtherOEM = $(nameOrderColumn).children('input.part-other-oem');
        $(partInputOtherOEM).attr('name', `part-other-oem-${newOrder}`);

        const imgColumn = $(nextRow).children('td.img');
        const partInputExistingImg = $(imgColumn).children('input.part-existing-img');
        $(partInputExistingImg).attr('name', `part-existing-img-${newOrder}`)
        const partInputImg = $(imgColumn).children('input.part-img');
        $(partInputImg).attr('name', `part-img-${newOrder}`);

    };

    $(thisRow).remove();

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
            `<tr class="border-top">
                <td class="name-order">
                    <input type="hidden" class="part-order" name="order" value="${NUM_PARTS}" />
                    <input type="hidden" class="part-id" name="part-id-${NUM_PARTS}" value="NEW" />
                    <label for="part-name">New Part: </label>
                    <select class="part-name custom-select" name="part-name-${NUM_PARTS}" required>
                    <option value="">Please Select a Part</option>
                    ${str}
                    <option value="other">Other (please specify)...</option>
                    </select>
                    <div class="card sub-other">
                    <br /><label for="part-other-name">If other, please specify name: </label>
                    <input type="text" class="part-other-name form-control" name="part-other-name-${NUM_PARTS}" />
                    <br /><label for="part-other-pn">If other, please specify P/N: </label>
                    <input type="text" class="part-other-pn form-control" name="part-other-pn-${NUM_PARTS}" />
                    <br /><label for="part-other-manuf">If other, please specify manuf: </label>
                    <input type="text" class="part-other-manuf form-control" name="part-other-manuf-${NUM_PARTS}" />
                    <br /><label for="part-other-oem">If other, please specify if OEM: </label>
                    <br /><input type="radio" class="form-check part-check" name="part-other-oem-${NUM_PARTS}" value="True" />
                    <label for="is_oem_1">OEM</label>
                    <input type="radio" class="form-check part-check" name="oem1" value="False" />
                    <label for="not_oem_1">Aftermarket</label>
                    <input type="radio" class="form-check part-check" name="oem1" value="False" />
                    <label for="unsure_if_oem_1">Not Sure</label>
                    </div>
                </td>
                <td class="img">
                    <input type="hidden" class="part-existing-img form-control" name="part-existing-img-${NUM_PARTS}" value="toolbox.png" />
                    <label for="part-img">Part Image (optional):</label>
                    <input type="file" class="part-img form-control-file" name="part-img-${NUM_PARTS}" />
                    <button class="del-img btn btn-primary">Restore Default Img</button>
                </td>
                <td>
                    <button class="remove-part btn btn-primary">Remove Part</button>
                </td>
            </tr>`
        );
        $('button.remove-part').off();
        $('button.del-img').off();
        $('select.part-name').off();
        $('select.part-name').on('change', requireOtherPartName);
        $('button.remove-part').on('click', removePart);
        $('button.del-img').on('click', restoreDefaultImg);
    });

    $('#NUM_PARTS').replaceWith(`<input name="NUM_PARTS" id="NUM_PARTS" 
                                    type="hidden" value="${NUM_PARTS}" />`);
}


function requireOtherPartName (evt) {

    const thisSelect = evt.target;
    const otherName = $(thisSelect).siblings('input.part-other-name');
    console.log(otherName);
    console.log($(thisSelect).val());

    if ($(thisSelect).val() === 'other') {
        $(otherName).attr('required', true);
    } else {
        $(otherName).attr('required', false);
    };
}

function getModelYears (evt) {

    evt.preventDefault();

    const formData = {
        make: $('#make').val(),
    };

    $.get('/get-model-years.json', formData, (res) => {

        let str = '';
        for (const model_year of res) {
            str = str + `<option value="${model_year}">${model_year}</option>`;
        }
        $('#model-year').replaceWith(
            `<select id="model-year" class="custom-select" name="model-year" required>
            <option value="">Vehicle Model Year</option>
            ${str}
            </select>`
        );

        $('#model-year').on('change', getModels);
    });

    
}


function addVehicle (evt) {

    evt.preventDefault();

    $('#vehicle-modal').on('shown.bs.modal', function () {

        $('#car-add').trigger('focus');

    });

    // $('#make').on('change', getModelYears);
    // $('#vehicle-submit').on('click', selectAddlVehicle);
}


function removeVehicle (evt) {

    evt.preventDefault();

    let numCars = Number($('#NUM_CARS').val());
    numCars -= 1;
   
    const thisButton = evt.target;
    const thisRow = $(thisButton).closest('tr')
    $(thisRow).remove();

    $('#NUM_CARS').replaceWith(`<input name="NUM_CARS" 
                                id="NUM_CARS" type="number" 
                                value="${numCars}" 
                                style="display: none;"/>`);
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
            `<select id="model-select" class="custom-select" name="model" required>
            <option value="">Vehicle Model</option>
            ${str}
            </select>`
        );
    })

    $('#model-select').attr('disabled', false);
    $('#vehicle-submit').attr('disabled', false);
    $('#vehicle-submit').on('click', hideVehicleAdder);
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
    console.log(formData);

    if (!formData['model'] | !formData['modelYear'] | !formData['make']) {
        alert('Please fill out vehicle selection form completely.');
    } else {
    $.post('/vehicle-select.json', formData, (res) => {
        $('#cars').append(`<tr id="row-${res['model_year']}-${res['make']}-${res['model']}">
                                <td>
                                <input name="cars" class="form-control" value="${res['model_year']}-${res['make']}-${res['model']}" disabled />
                                </td>
                                <td>
                                    <button class="remove-vehicle btn btn-primary" value="${res['model_year']}-${res['make']}-${res['model']}">
                                    Remove Vehicle
                                    </button>
                                </td>
                            </tr>`)

        $('button.remove-vehicle').off();
        $('button.remove-vehicle').on('click', removeVehicle);
    });

    $('#NUM_CARS').replaceWith(`<input name="NUM_CARS" 
                                id="NUM_CARS" type="number" 
                                value="${numCars}" 
                                style="display: none;"/>`);

    $('checkbox.car-remove').attr('disabled', false);
    $('#car-add-form').hide();
    $('#model-year').attr('disabled', true);
    $('#model').attr('disabled', true);
    };
}


function moveRow (evt) {

    evt.preventDefault();

    const thisButton = evt.target;

    // Find the order of the current row.
    const thisRow = $(thisButton).closest('tr');
    const thisOrderColumn = $(thisRow).children('td.name-order');
    const thisOrderInput = $(thisOrderColumn).children('input.step-order');
    const thisOrder = Number($(thisOrderInput).val());
    console.log(`thisOrder: ${thisOrder}`)

    if ($(thisButton).hasClass('up')) {

        if ($(thisRow).prevAll('tr').length > 0) {

            // Find the order of the row that just switched with current row.
            const prevRow = $(thisRow).prev('tr');
            const prevOrderColumn = $(prevRow).children('td.name-order');
            const prevOrderInput = $(prevOrderColumn).children('input.step-order');
            const prevOrder = Number($(prevOrderInput).val()); 
            console.log(`prevOrder: ${prevOrder}`)

            // Re-index everything in the current row.
            $(thisOrderInput).attr('name', `step-order-${prevOrder}`);
            $(thisOrderInput).attr('value', prevOrder);

            const stepInputID = $(thisOrderColumn).children('input.step-id');
            $(stepInputID).attr('name', `step-id-${prevOrder}`);
            const stepInputText = $(thisOrderColumn).children('input.step-text');
            $(stepInputText).attr('name', `step-text-${prevOrder}`);

            const refColumn = $(thisRow).children('td.ref');
            const stepInputRef = $(refColumn).children('input.step-ref');
            $(stepInputRef).attr('name', `step-ref-${prevOrder}`);

            const imgColumn = $(thisRow).children('td.img');
            const stepInputExistingImg = $(imgColumn).children('input.step-existing-img');
            $(stepInputExistingImg).attr('name', `step-existing-img-${prevOrder}`)
            const stepInputImg = $(imgColumn).children('input.step-img-edit');
            $(stepInputImg).attr('name', `step-img-${prevOrder}`);

            // Re-index everything in the switched row.
            $(prevOrderInput).attr('name', `step-order-${thisOrder}`);
            $(prevOrderInput).attr('value', thisOrder);

            const prevStepInputID = $(prevOrderColumn).children('input.step-id');
            $(prevStepInputID).attr('name', `step-id-${thisOrder}`);
            const prevStepInputText = $(prevOrderColumn).children('input.step-text');
            $(prevStepInputText).attr('name', `step-text-${thisOrder}`);

            const prevRefColumn = $(prevRow).children('td.ref');
            const prevStepInputRef = $(prevRefColumn).children('input.step-ref');
            $(prevStepInputRef).attr('name', `step-ref-${thisOrder}`);

            const prevImgColumn = $(prevRow).children('td.img');
            const prevInputExistingImg = $(prevImgColumn).children('input.step-existing-img');
            $(prevInputExistingImg).attr('name', `step-existing-img-${thisOrder}`);
            const prevStepInputImg = $(prevImgColumn).children('input.step-img-edit');
            $(prevStepInputImg).attr('name', `step-img-${thisOrder}`);
        };

        thisRow.prev().before(thisRow);

    } else {

        if ($(thisRow).nextAll('tr').length > 0) {
        
            // Find the order of the row that just switched with current row.
            const nextRow = $(thisRow).next('tr');
            const nextOrderColumn = $(nextRow).children('td.name-order');
            const nextOrderInput = $(nextOrderColumn).children('input.step-order');
            const nextOrder = Number($(nextOrderInput).val()); 
            console.log(`nextOrder: ${nextOrder}`)

            // Re-index everything in the current row.
            $(thisOrderInput).attr('name', `step-order-${nextOrder}`);
            $(thisOrderInput).attr('value', nextOrder);

            const stepInputID = $(thisOrderColumn).children('input.step-id');
            $(stepInputID).attr('name', `step-id-${nextOrder}`);
            const stepInputText = $(thisOrderColumn).children('input.step-text');
            $(stepInputText).attr('name', `step-text-${nextOrder}`);

            const refColumn = $(thisRow).children('td.ref');
            const stepInputRef = $(refColumn).children('input.step-ref');
            $(stepInputRef).attr('name', `step-ref-${nextOrder}`);

            const imgColumn = $(thisRow).children('td.img');
            const stepInputExistingImg = $(imgColumn).children('input.step-existing-img');
            $(stepInputExistingImg).attr('name', `step-existing-img-${nextOrder}`)
            const stepInputImg = $(imgColumn).children('input.step-img-edit');
            $(stepInputImg).attr('name', `step-img-${nextOrder}`);
            
            // Re-index everything in the switched row.
            $(nextOrderInput).attr('name', `step-order-${thisOrder}`);
            $(nextOrderInput).attr('value', thisOrder);

            const nextStepInputID = $(nextOrderColumn).children('input.step-id');
            $(nextStepInputID).attr('name', `step-id-${thisOrder}`);
            const nextStepInputText = $(nextOrderColumn).children('input.step-text');
            $(nextStepInputText).attr('name', `step-text-${thisOrder}`);

            const nextRefColumn = $(nextRow).children('td.ref');
            const nextStepInputRef = $(nextRefColumn).children('input.step-ref');
            $(nextStepInputRef).attr('name', `step-ref-${thisOrder}`);

            const nextImgColumn = $(nextRow).children('td.img');
            const nextInputExistingImg = $(nextImgColumn).children('input.step-existing-img');
            $(nextInputExistingImg).attr('name', `step-existing-img-${thisOrder}`);
            const nextStepInputImg = $(nextImgColumn).children('input.step-img-edit');
            $(nextStepInputImg).attr('name', `step-img-${thisOrder}`);
        };

        thisRow.next().after(thisRow);
    }
}


function removeStep (evt) {

    evt.preventDefault();

    let NUM_STEPS = Number($('#NUM_STEPS').val());
    NUM_STEPS -= 1;

    const thisButton = evt.target;
    const thisRow = $(thisButton).closest('tr');
    const nextLength = ($(thisRow).nextAll('tr')).length;

    for (let row = 0; row < nextLength; row += 1) {
        
        const nextRow = $(thisRow).nextAll('tr')[row];
        const nameOrderColumn = $(nextRow).children('td.name-order');
        const orderInput = $(nameOrderColumn).children('input.step-order');
        const newOrder = Number($(orderInput).val()) - 1;  
        $(orderInput).attr('name', `step-order-${newOrder}`);
        $(orderInput).attr('value', newOrder);

        const stepInputID = $(nameOrderColumn).children('input.step-id');
        $(stepInputID).attr('name', `step-id-${newOrder}`);
        const stepInputText = $(nameOrderColumn).children('input.step-text');
        $(stepInputText).attr('name', `step-text-${newOrder}`);

        const refColumn = $(nextRow).children('td.ref');
        const stepInputRef = $(refColumn).children('input.step-ref');
        $(stepInputRef).attr('name', `step-ref-${newOrder}`);

        const imgColumn = $(nextRow).children('td.img');
        const stepInputExistingImg = $(imgColumn).children('input.step-existing-img');
        $(stepInputExistingImg).attr('name', `step-existing-img-${newOrder}`)
        const stepInputImg = $(imgColumn).children('input.step-img-edit');
        $(stepInputImg).attr('name', `step-img-${newOrder}`);

    };

    $(thisRow).remove();

    $('#NUM_STEPS').replaceWith(`<input name="NUM_STEPS" id="NUM_STEPS" 
                                    type="hidden" value="${NUM_STEPS}" />`);
   
}


function addStep (evt) {

    evt.preventDefault();

    let NUM_STEPS = Number($('#NUM_STEPS').val());
    NUM_STEPS += 1;

    $('#steps').append(
                `<tr class="border-top">
                    <td class="name-order">
                        <input type="hidden" class="step-order" name="step-order-${NUM_STEPS}" value="${NUM_STEPS}" />
                        <input type="hidden" class="step-id" name="step-id-${NUM_STEPS}" value="NEW" />
                        <textarea class="step-text form-control" name="step-text-${NUM_STEPS}" required></textarea>
                    </td>
                    <td class="ref">
                        <input type="url" class="step-ref form-control" name="step-ref-${NUM_STEPS}"
                            placeholder="https://example.com" pattern="https://.*" disabled/>
                        <br />
                        <button class="edit ref btn btn-primary">Edit Ref</button>
                        <button class="del-ref btn btn-primary" disabled>Remove Ref</button>
                    </td>
                    <td class="img">
                        <input type="hidden" class="step-existing-img" name="step-existing-img-${NUM_STEPS}" value="toolbox.png" />
                        <input type="file" class="step-img-edit form-control-file" name="step-img-${NUM_STEPS}" disabled />
                        <br />
                        <button class="edit img btn btn-primary">Edit Img</button>
                        <button class="del-img btn btn-primary" disabled>Restore Default Img</button>
                    </td>
                    <td>
                        <button class="remove-step btn btn-primary">Remove Step</button>
                    </td>
                    <td>
                        <button class="move up btn btn-primary">UP</button>
                    </td>
                    <td>
                        <button class="move down btn btn-primary">DOWN</button>
                    </td>
                </tr>`);

    $('#NUM_STEPS').replaceWith(`<input name="NUM_STEPS" id="NUM_STEPS" 
                                    type="hidden" value="${NUM_STEPS}" />`);

    
    $('button.move').off();
    $('button.remove-step').off();
    $('button.edit').off();
    $('button.del-ref').off();
    $('button.del-img').off();
    $('button.move').on('click', moveRow);
    $('button.remove-step').on('click', removeStep);
    $('button.edit').on('click', enableEditField);
    $('button.del-ref').on('click', removeReference);
    $('button.del-img').on('click', restoreDefaultImg);
}


function enableEditField (evt) {

    evt.preventDefault();

    const thisButton = evt.target;
    const thisInput = $(thisButton).prevAll('input');
    const otherButton = $(thisButton).next('button');

    $(thisInput).attr('disabled', false);
    $(thisButton).attr('disabled', true);
    $(otherButton).attr('disabled', false);

}


function restoreDefaultImg (evt) {

    evt.preventDefault();

    const thisButton = evt.target;
    const thisInput = $(thisButton).prevAll('input');
    const otherButton = $(thisButton).prevAll('button');
    $(thisInput).val('');
    $(thisInput).attr('disabled', true);
    $(thisButton).attr('disabled', true);
    $(otherButton).attr('disabled', false);
}


function removeReference (evt) {

    evt.preventDefault();

    const thisButton = evt.target;
    const thisInput = $(thisButton).prevAll('input');
    $(thisInput).val('');
}





function requireStepAndCar (evt) {

    let NUM_STEPS = Number($('#NUM_STEPS').val());
    let NUM_CARS = Number($('#NUM_CARS').val());

    if (NUM_CARS === 0) {
        evt.preventDefault();
        alert('All procedures must have at least one car!');
    } else if (NUM_STEPS === 0) {
        evt.preventDefault();
        alert('All procedures must have at least one step!');
    };
    // needs refactoring, but gets the job done
    $('input', this).prop('disabled', false);
}


$('#car-add').on('click', addVehicle);
$('#make').on('change', getModelYears);
$('#vehicle-submit').on('click', selectAddlVehicle);
$('button.remove-vehicle').on('click', removeVehicle);

$('button.remove-tool').on('click', removeTool);
$('#tool-add').on('click', addTool);

$('button.remove-part').on('click', removePart);
$('#part-add').on('click', addPart);

$('button.move').on('click', moveRow);
$('button.remove-step').on('click', removeStep);
$('#step-add').on('click', addStep);

$('button.edit').on('click', enableEditField);
$('button.del-img').on('click', restoreDefaultImg);
$('button.del-ref').on('click', removeReference);

$('form').on('submit', requireStepAndCar);
