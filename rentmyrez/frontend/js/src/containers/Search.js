import {connect} from 'react-redux';
import Search from './../components/Search';
import {updateText} from './../actions/creators';

const mapStateToProps = state => ({text: state.text});

const mapDispatchToProps = dispatch => ({update: t => dispatch(updateText(t))});

const SearchContainer = connect(
	mapStateToProps,
	mapDispatchToProps
)(Search);

export default SearchContainer;
