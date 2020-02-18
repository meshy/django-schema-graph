var path = require("path")
var webpack = require('webpack')
const VueLoaderPlugin = require('vue-loader/lib/plugin')


module.exports = {
  context: __dirname,

  entry: './assets/entrypoints/index.js',

  output: {
      path: path.resolve('./schema_graph/static/schema_graph/'),
      filename: "[name].js",
  },

  module: {
    rules: [
      { test: /\.vue$/, loader: 'vue-loader' },
      { test: /\.js$/, loader: 'babel-loader', exclude: path.resolve(__dirname, 'node_modules/') },
      { test: /\.css$/, use: [ 'vue-style-loader', 'css-loader' ] }
    ],
  },

  plugins: [
    new VueLoaderPlugin()
  ],

  resolve: {
    modules: ['node_modules'],
    extensions: ['.js', '.vue']
  },
}
