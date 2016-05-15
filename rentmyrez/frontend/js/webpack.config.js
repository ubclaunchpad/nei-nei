module.exports = {
	entry: './src/App.js',
	output: {
		path: __dirname,
		filename: 'dist/bundle.js'
	},
	module: {
		loaders: [
			{
				test: /.jsx?$/,
				loader: 'babel-loader',
				exclude: /node_modules/,
				query: {
					presets: [
						'es2015',
						'react'
					],
					plugins: [
						'transform-class-properties'
					]
				}
			}
		]
	}
};
