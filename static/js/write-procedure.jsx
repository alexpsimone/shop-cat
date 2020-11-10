'use strict';

let NUM_TOOLS = 0;
let NUM_PARTS = 0;

function getTools (evt) {

    evt.preventDefault();
    

    $.get('/get-tools.json', (res) => { 
        
        NUM_TOOLS += 1;
        let str = '';
        
        for (const tool of res) {
            str = str + `<option value="${tool}">${tool}</option>`;
        }

        $('#tool-list').append(
            `<br />
            <label>Tool #${NUM_TOOLS}: </label>
            <select name="tool_req" class="tool-req" id="tool${NUM_TOOLS}">
            <option value="">--Please select a tool--</option>
            ${str}
            <option value="other">Other (please specify)...</option>
            </select>
            <br /><label>If other, please specify: </label>
            <input type="text" name="tool_other" />
            <br />`
        );

        $('#NUM_TOOLS').replaceWith(`<input id="NUM_TOOLS" type="number" 
            value="${NUM_TOOLS}" style="display: none;"/>`);

    });
    
    
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
            <select name="part_req" class="part-req" id="part${NUM_PARTS}">
            <option value="">--Please select a part--</option>
            ${str}
            <option value="other">Other (please specify)...</option>
            </select>
            <br /><label>If other, please specify: </label>
            <input type="text" name="part_other" />
            <br />`
        );

        $('#NUM_PARTS').replaceWith(`<input id="NUM_PARTS" type="number" 
            value="${NUM_PARTS}" style="display: none;"/>`);

    });   
}

$('#tool-adder').on('click', getTools);
$('#part-adder').on('click', getParts);