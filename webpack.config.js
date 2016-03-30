var path = require('path');
var webpack = require('webpack');
var autoprefixer = require('autoprefixer');
var lost = require('lost');
var responsiveType = require('postcss-responsive-type');
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
        new LiveReloadPlugin(),
        new webpack.ProvidePlugin({
            leaflet: "leaflet"
        })
    ],
    module: {
        loaders: [
            { test: /\.(scss|css)$/, loader: ExtractTextPlugin.extract("style-loader", ["css", "postcss", "sass"]) },
            { test: /\.js$/, loaders: ['babel'], include: path.join(__dirname, 'src') },
            { test: /\.png$/, loader: "url-loader" },
        ]
    },
    postcss: function() {
        return {
            defaults: [autoprefixer, lost, responsiveType]
        };
    },
    cssnext: {
        browsers: 'last 2 versions'
    }
};
