const path = require("path");
const webpack = require("webpack");

module.exports = {
  entry: {
    'index': path.resolve('src/', 'index.js')
  },
  mode: "development", // or production
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        loader: "babel-loader",
        options: {
          presets: ["@babel/env"], plugins: ["@babel/plugin-proposal-class-properties"]
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
    filename: "[name].bundle.js"
  }
};