"use strict";

function Title() {

    return (
        <React.Fragment>
            <p>Let's write a procedure!</p>
            <br />
            <form action="/procedure">
                <label>Procedure Name: </label>
                <input type="text" name="name" required/>
                <input type="submit" />
            </form>
            <br />
        </React.Fragment>
    );
}


function Tools() {

    return (
        <React.Fragment>
            <p>THIS IS A TOOLS TEST.</p>
        </React.Fragment>
    );
}


function Parts() {
    return (
        <p>THIS IS A PART TEST.</p>
    );
}


function Steps() {
    return (
        <p>THIS IS A STEP TEST.</p>
    );
}


ReactDOM.render(<Title />, document.querySelector('#app-title'));
ReactDOM.render(<Tools />, document.querySelector('#app-tools'));
ReactDOM.render(<Parts />, document.querySelector('#app-parts'));
ReactDOM.render(<Steps />, document.querySelector('#app-steps'));