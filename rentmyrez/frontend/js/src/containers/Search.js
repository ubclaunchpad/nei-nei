import {connect} from 'react-redux';
import Search from './../components/Search';
import {updateText} from './../actions/creators';

const mapStateToProps = (state) => ({text: state.get('text')});

const mapDispatchToProps = (dispatch) => (
	{update: event => dispatch(updateText(event.target.value))}
);

const SearchContainer = connect(
	mapStateToProps,
	mapDispatchToProps
)(Search);

export default SearchContainer;
