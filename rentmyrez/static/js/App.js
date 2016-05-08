// Import our Hello component
import Hello from './src/Hello.js';
// We don't explicitly use React here, but it needs to be in scope whenever we
// call ReactDOM.render() and mount something to the DOM.
import React from 'react';
// ReactDOM is used to mount React components to the DOM.
import ReactDOM from 'react-dom';

// An example of ES6 arrow functions. Parameters go in the parentheses.
const onClickHandler = () => {
	alert('You have clicked a React component!');
};
// `const` variables cannot be redeclared later, so this will throw a compile-error:
// const x = 5;
// x = 6;
// When writing ES6, there is almost never a reason to use `var`

// Here we actually instantiate an instance of the `Hello` component and give it
// some props. Try changing the props and see what happens!
const component = <Hello age={20} name="Jordan" onClick={onClickHandler} />

// Here we render it to the DOM so that it appears in the HTML. Great!
ReactDOM.render(component, document.getElementById('app'));
