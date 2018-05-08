<template>
    <div>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/siimple@3.0.0/dist/siimple.min.css">
        <div class="siimple-box-subtitle" align="center">{{ data.name }}</div>
        <div class="siimple-box-detail"align="center">
            {{ data.description }}
            <button v-on:click="flopManifestDetail(data.model)" class="siimple-btn siimple-btn--orange">More</button>
        </div>
        <manifest :manifest="model" v-if="showManifestDetail" @close="showManifestDetail = false"></manifest>
    </div>
</template>

<script>
    import manifest from './manifest.vue';
    const URL = 'https://manifest.turip.org//';
    export default {
        name: "ManifestDetail",
        props: ['data'],
        components: {
            'manifest': manifest
        },
        data: () => {
            return {
                showManifestDetail: false,
                model: ''
            }
        },
        methods: {
            flopManifestDetail: function(model) {
                fetch(URL + model)
                    .then(res => res.json())
                    .then(json => {
                        this.model = json;
                        this.showManifestDetail = true;
                    });
            },
        }

    }
</script>

<style scoped>

</style>