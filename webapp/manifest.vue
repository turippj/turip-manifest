<template>
    <div>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/siimple@3.0.0/dist/siimple.min.css">
        <div class="siimple-content">Interface:<span v-for='item in manifest["interface"]'>{{ item }}</span>
        </div>
        <table class="siimple-table">
            <div class="siimple-table-header">
                <div class="siimple-table-row">
                    <div class="siimple-table-cell">Number</div>
                    <div class="siimple-table-cell">Name</div>
                    <div class="siimple-table-cell">Description</div>
                    <div class="siimple-table-cell">Permission</div>
                    <div class="siimple-table-cell">Type</div>
                </div>
            </div>
            <div class="siimple-table-body">
                <div v-for='port in manifest["port"]' :port="port" class="siimple-table-row">
                    <div class="siimple-table-cell">{{ port["number"] }}</div>
                    <div class="siimple-table-cell">{{ port["name"] }}</div>
                    <div class="siimple-table-cell">{{ port["description"] }}</div>
                    <div class="siimple-table-cell">{{ port["permission"] }}</div>
                    <div class="siimple-table-cell">{{ port["type"] }}</div>
                </div>
            </div>
        </table>
        <button class="siimple-btn siimple-btn--orange" @click="$emit('close')">Close</button>
    </div>
</template>

<script>
    export default {
        name: "manifest",
        props: ['manifest']
    }
</script>

<style scoped>
    li {
        list-style: none;
    }
    .siimple-table {
        width: 300px; height: 100px;
        box-sizing: border-box;
    }
</style>