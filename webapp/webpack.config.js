const VueLoaderPlugin = require('vue-loader/lib/plugin');
const VueCssLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = {
    entry: './main.js',
    mode: 'development',
    output: {
        path: `${__dirname}`,
        filename: 'renderer.js',
    },
    resolve: {
        extensions: ['.js', '.vue'],
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        }
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.css$/,
                use: [
                    'vue-style-loader',
                    'css-loader'
                ]
            }
         ]
    },
    plugins: [
        new VueLoaderPlugin()
    ]
};
