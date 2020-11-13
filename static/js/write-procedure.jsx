'use strict';

let NUM_TOOLS = 0;
let NUM_PARTS = 0;
let NUM_STEPS = 0;


function getTools (evt) {

    evt.preventDefault();
    NUM_TOOLS += 1;

    $.get('/get-tools.json', (res) => { 
        
        let str = '';
        for (const tool of res) {
            str = str + `<option value="${tool}">${tool}</option>`;
        }

        $('#tool-list').append(
            `<br />
            <label>Tool #${NUM_TOOLS}: </label>
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
            type="number" value="${NUM_TOOLS}" style="display: none;"/>`);
    
}


function getParts (evt) {
    
    evt.preventDefault();

    $.get('/get-parts.json', (res) => { 
        
        NUM_PARTS += 1;
        let str = '';

        for (const part of res) {
            str = str + `<option value="${part}">${part}</option>`;
        }

        $('#part-list').append(
            `<br />
            <label>Part #${NUM_PARTS}: </label>
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

        $('#NUM_PARTS').replaceWith(`<input name ="NUM_PARTS" id="NUM_PARTS" 
            type="number" value="${NUM_PARTS}" style="display: none;"/>`);

    });   
}


function addStep (evt) {
    
    evt.preventDefault();
        
    NUM_STEPS += 1;

    $('#step-list').append(`<p>Step ${NUM_STEPS}: </p>
                            <textarea name="step_text_${NUM_STEPS}"></textarea>
                            <br />
                            <input type="checkbox" id="ref_${NUM_STEPS}"
                            name="ref_${NUM_STEPS}" />
                            <label for="ref_${NUM_STEPS}">Reference?</label>
                            <br />
                            <label for="ref_text_${NUM_STEPS}">
                            Copy reference URL here: </label>
                            <input type="text" name="ref_text_${NUM_STEPS}" />`
                            );

    $('#NUM_STEPS').replaceWith(`<input name ="NUM_STEPS" id="NUM_STEPS" 
        type="number" value="${NUM_STEPS}" style="display: none;"/>`);
 
}

$('#tool-adder').on('click', getTools);
$('#part-adder').on('click', getParts);
$('#step-adder').on('click', addStep);