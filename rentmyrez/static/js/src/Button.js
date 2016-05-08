import React, {Component, PropTypes} from 'react';

// All this component does is display a button with a title based
// on its `title` prop, and call a callback function when it is
// clicked. This sort of simple, stateless, component is what we
// want the majority of our components to look like.
export default class Button extends Component {
	static displayName = "Button";

	static propTypes = {
		color: PropTypes.string,
		onClick: PropTypes.func,
		title: PropTypes.string
	};
	render () {
		const {color, onClick, title} = this.props;

		return (
			<button onClick={this._handleClick}>
				{title}
			</button>
		);
	}

	_handleClick = () => {
		this.props.onClick(this.props.color);
	}
}
