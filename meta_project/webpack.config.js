const path = require("path");
const webpack = require("webpack");

module.exports = {
  entry: {
    'index': path.resolve('public/', 'index.js')
  },
  mode: "development", // development or production
  devtool: "cheap-source-map",
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        loader: "babel-loader",
        options: {
          presets: [
            ["@babel/env", {"targets": "last 2 major versions"}],
            "@babel/preset-react"
          ],
          plugins: [
            ["@babel/plugin-proposal-class-properties", {loose: true}],
            ["@babel/plugin-proposal-object-rest-spread", {useBuiltIns: true}],
            "@babel/plugin-proposal-optional-chaining",
          ]
        }
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"]
      }
    ]
  },
  resolve: {extensions: ["*", ".js", ".jsx"]},
  output: {
    path: path.resolve(__dirname, "app/static/dist"),

    // the filename template for entry chunks
    publicPath: "/static/dist/",

    // the target directory for all output files
    filename: "[name].bundle.js",
  }
};