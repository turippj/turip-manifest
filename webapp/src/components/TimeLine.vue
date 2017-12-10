<template>
  <main class="mdl-layout__content">
    <div class="page-content">
      <search></search>
      <card v-if="manifest != Object && manifest != 404" :manifest="manifest"></card>
      <p v-if="manifest == 404">Manifest is not found.</p>
    </div>
  </main>
</template>

<script>
  import Search from './Search'
  import Card from './Card'
  import { mapGetters } from 'vuex'
  export default {
    computed: {
      ...mapGetters(['manifest'])
    },
    components: {
      Search,
      Card
    }
  }
</script>

<style>
  main {
    background-color: #f6f6f6;
    width: 100%;
    margin: 0 auto;
  }
  .page-content {
    display: flex;
    flex-direction: column;
  }
  p {
    font-size: 20px;
    margin: 30px auto;
  }
</style>
