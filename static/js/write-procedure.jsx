'use strict';

document.querySelector('#tool-adder').addEventListener('click', (evt) => {
    document.querySelector('#tool-list').insertAdjacentHTML('beforeend', 
        '<br /><label>Tool Required: </label>'
        + '<select name="tool_req">'
        + '<option value="">--Please select a tool--</option>'
        + '{% for tool in tools %}'
        + '<option value="{{ tool.name }}">{{ tool.name }}</option>'
        + '{% endfor %}'
        + '<option value="other">Other (please specify)...</option>'
        + '</select>'
        + '<br /><label>If other, please specify: </label>'
        + '<input type="text" name="tool_other" /><br />');
});