module.exports = {
	"extends": "airbnb",
	"ecmaFeatures": {
		"classes": true,
		"jsx": true
	},
	"parser": "babel-eslint",
	"plugins": [
		"react"
	],
	"rules": {
		"comma-dangle": ["error", "never"],
		"indent": ["error", "tab"],
		"new-cap": 0,
		"no-underscore-dangle": 0,
		"object-curly-spacing": 0,
		"react/jsx-closing-bracket-location": ["error", "after-props"],
		"react/jsx-indent": ["error", "tab"],
		"react/jsx-indent-props": ["error", "tab"],
		"react/sort-comp": 0,
		"space-before-function-paren": 0
	}
};
