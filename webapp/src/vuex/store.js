import Vuex from 'vuex'
import Vue from 'vue'
import {
  CHANGE_KEYWORD,
  SEARCH
} from './mutation-types'

Vue.use(Vuex)

function getManifest (query) {
  const params = encodeURIComponent(query)
  return fetch('https://turip-manifest.appspot.com/api/manifest/search/' + params)
    .then( res => res.json())
}

const state = {
  keyword: '',
  manifest: Object
}

const actions = {
  [CHANGE_KEYWORD] ({ commit }, keyword) {
    commit(CHANGE_KEYWORD, keyword)
  },

  [SEARCH] ({ commit, state }) {
    getManifest(state.keyword)
      .then(data => {commit(SEARCH, data)})
  }
}

const mutations = {
  [CHANGE_KEYWORD] (state, keyword) {
    state.keyword = keyword
  },
  [SEARCH] (state, manifest) {
    state.manifest = manifest
  }
}

const getters = {
  manifest: state => state.manifest
}

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations
})
