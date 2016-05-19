import React, {PropTypes} from 'react';

const Search = ({text, update}) => <input value={text} onChange={update} />;

Search.displayName = 'Search';

Search.propTypes = {
	text: PropTypes.string,
	update: PropTypes.func
};

export default Search;
