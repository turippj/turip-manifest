<template>
  <div class="mdl-textfield mdl-js-textfield">
    <input @change="CHANGE_KEYWORD($event.target.value)" class="mdl-textfield__input" type="text" id="sample1">
    <i @click="SEARCH" class="material-icons">search</i>
  </div>
</template>

<script>
  import { mapActions } from 'vuex'
  import { CHANGE_KEYWORD, SEARCH } from '../vuex/mutation-types'
  export default {
    methods: {
      ...mapActions([
        CHANGE_KEYWORD, SEARCH
      ])
    }
  }
</script>

<style media="screen">
  .mdl-textfield {
    padding: 0;
    background-color: #f6f6f6;
    margin: 30px auto;
    width: 60%;
    display: flex;
    margin-bottom: 60px;
  }
</style>
