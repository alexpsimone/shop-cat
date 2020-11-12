"use strict";

function Title() {

    return (
        <React.Fragment>
            <h1>Let's write a procedure!</h1>

        </React.Fragment>
    );
}


function Procedures() {

    return (<div></div>);
}


ReactDOM.render(<Title />, document.querySelector('#app-title'));
ReactDOM.render(<Procedures />, document.querySelector('#app-procedures'));