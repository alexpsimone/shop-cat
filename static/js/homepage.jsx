"use strict";

function Title() {

    return (
        <React.Fragment>
            <h1>Let's write a procedure!</h1>

        </React.Fragment>
    );
}


function Procedures() {

    return (
        <React.Fragment>
            <h1>Browse all the available procedures:</h1>

        </React.Fragment>
    );
}


ReactDOM.render(<Title />, document.querySelector('#app-title'));
ReactDOM.render(<Procedures />, document.querySelector('#app-procedures'));