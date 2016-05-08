// ES6 import-from syntax is equivalent to Node's require.
// But you can import (and export) multiple objects from a file.
// The 'react' package has a default export called React:
// import React from 'react';
// The 'react' package also has secondary named exports called Component
// and PropTypes that can be import using destructuring syntax.
// import {Component, PropTypes} from 'react';
// This can all be combined, as below:
import React, {Component, PropTypes} from 'react';
import Button from './Button.js';

// We export our Hello class so it accessible in App.js using the import syntax.
export default class Hello extends Component {
	// The `static` keyword associates the variable with the class, not any
	// particular instance of the class, sort of like Java
	// `displayName` is what the component appears as in the React debugger.
	// Every component should have a displayName property, usually the same
	// as the component name.
	static displayName = "Hello";

	// `propTypes` is a declaration of what props each component expects.
	// You declare the type of the prop, and whether it is required or not.
	static propTypes = {
		age: PropTypes.number,
		name: PropTypes.string.isRequired,
		onClick: PropTypes.func
	};

	// If a prop is not specified, `defaultProps` allows a way to provide a
	// default. If someone instantiates this Hello component without providing
	// a `name` prop, then the name will default to 'Arabelle'
	static defaultProps = {
		name: 'Arabelle'
	};

	// Constructors are used to instantiate an instance of each component.
	// If the component has state, this is where we setup the initial state values.
	constructor (props) {
		// Call the constructor on the superclass, in this case `React.Component`
		super(props);

		// Setup initial value(s) for the state.
		// Typically we avoid using state. Most components should only have props
		// with only a few top-level components having state.
		this.state = {
			backgroundColor: 'white'
		};
	}
	render () {
		// An example of ES6 destructuring.
		// This is equivalent to:
		// const age = this.props.age;
		// const name = this.props.name;
		// const onClick = this.props.onClick;
		const {age, name, onClick} = this.props;

		const {backgroundColor} = this.state;

		// `let` variables are block-scoped and CAN be reassigned, unlike `const`
		let ageStatement = null;
		if (age) {
			// You can put chunks of JSX into variables to use later
			// `ageStatement` will only have a value if the age prop is passed.
			ageStatement = <h2>You are {age} years old.</h2>;
		}

		// Another example of ES6 destructuring, this time in reverse.
		// This is equivalent to:
		// const colorStyle = {backgroundColor: backgroundColor};
		// If the name of the key is the same as the name of the variable,
		// you only need to write it once!
		const colorStyle = {backgroundColor};

		return (
			<div style={colorStyle}>
				<div onClick={onClick}>
					<h1>Hello, your name is {name}</h1>
					{/* You can directly add renderable variables into the JSX */}
					{ageStatement}
				</div>
				{/* You can also evaluate functions, and render the result */}
				{this._renderButtons()}
			</div>
		);
	}

	_renderButtons () {
		const colors = ['red', 'blue', 'orange', 'purple'];
		// If you aren't familiar with the map function, it just maps the values from
		// one array onto another, new array, applying some transform along the way.
		// It is commonly used to render lists of React components. But if you do this,
		// you must include a `key` prop so that React can keep track of which one is which.
		return colors.map((color) => {
			// Here we use a React component rather than a boring old <div>.
			// All the button does is call its `onClick` prop with its `color`
			// prop as the argument whenever it is clicked. This is a common design
			// pattern in React.
			return (
				<Button
					color={color}
					key={color}
					onClick={this._handleSelectColor}
					title={color} />
			);
		});
	}

	// A handler function for our buttons. When a button is pressed,
	// we update the internal state of the component, triggering a re-render.
	// NEVER modify `this.state` directly, always use `this.setState()`.
	_handleSelectColor = (color) => {
		this.setState({
			backgroundColor: color
		});
	}
}
