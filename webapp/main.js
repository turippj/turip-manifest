'use strict';

import fetch from 'node-fetch';
import Vue from 'vue';
import manifestCard from './manifest-card.vue';

const URL = 'https://manifest.turip.org/';

let results = {
    result:'',
    model:'',
    validation: {
        valid: false
    }
};

const searchBox = new Vue({
    el: '#searchBox',
    data: {
        category: 'model',
        keyword: '',
        errorMessage: ''
    },
    methods: {
        search: function (event) {
            if(!this.keyword) {
                this.errorMessage = 'Keyword is Empty!'
            }else{
                this.errorMessage = '';
                fetch(URL+'api/manifest/search?category='+this.category+'&keyword='+this.keyword)
                    .then(res => res.json())
                    .then(json => results.result = json);
            }
        }
    }
});

const searchResult = new Vue({
    el: '#searchResult',
    data: results,
    components: {
        'manifest-card': manifestCard
    }
});