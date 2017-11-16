<template>
  <!-- Three Line List with secondary info and action -->
  <div class="manifest-list mdl-list">
    <li class="mdl-list__item mdl-list__item--three-line">
    <span class="mdl-list__item-primary-content">
      <span>{{manifest["name"]}}</span>
      <span class="mdl-list__item-text-body">
        {{manifest["description"]}}
      </span>
    </span>
    </li>
    <li class="mdl-list__item mdl-list__item">
    <span class="mdl-list__item-primary-content">
      <span>Author : {{manifest["author"]}}</span>
    </span>
    </li>
    <li class="mdl-list__item mdl-list__item">
    <span class="mdl-list__item-primary-content">
        <table class="mdl-data-table mdl-js-data-table mdl-shadow--2dp">
            <thead>
              <tr>
                <th class="mdl-data-table__cell--non-numeric">Number</th>
                <th>Name</th>
                <th>Description</th>
                <th>Permission</th>
                <th>Type</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for='port in manifest["port"]' :port="port">
                <td class="mdl-data-table__cell--non-numeric">{{port["number"]}}</td>
                <td>{{port["name"]}}</td>
                <td>{{port["description"]}}</td>
                <td>{{port["permission"]}}</td>
                <td>{{port["type"]}}</td>
              </tr>
            </tbody>
        </table>
      </span>
    </li>
  </div>
</template>

<script>
  export default {
    props: {
      manifest: Object
    }
  }
</script>

<style>
  .manifest-list {
    padding: 0;
    background-color: #f6f6f6;
    margin: 30px auto;
    margin-bottom: 60px;
  }
</style>
