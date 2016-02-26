var path = require('path');
var webpack = require('webpack');
var autoprefixer = require('autoprefixer');
var lost = require('lost');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var LiveReloadPlugin = require('webpack-livereload-plugin');

module.exports = {
    devtool: 'cheap-module-eval-source-map',
    entry: [
        './app/snowdoniadragons/static/index'
    ],
    output: {
        filename: 'app.js',
        path: path.join(__dirname, 'app/snowdoniadragons/static/'),
        publicPath: '/assets/'
    },
    plugins: [
        new webpack.NoErrorsPlugin(),
        new ExtractTextPlugin("css/index.css"),
        new LiveReloadPlugin()
    ],
    module: {
        loaders: [
            { test: /\.scss$/, loader: ExtractTextPlugin.extract("style-loader", ["css", "postcss", "sass"]) },
            { test: /\.js$/, loaders: ['babel'], include: path.join(__dirname, 'src') },
        ]
    },
    postcss: function() {
        return {
            defaults: [autoprefixer, lost]
        };
    },
    cssnext: {
        browsers: 'last 2 versions'
    }
};
