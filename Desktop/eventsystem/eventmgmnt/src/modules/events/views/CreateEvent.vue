<template>
    <v-container fluid>
        <v-card>
            <v-card-title>
                <span class="heading"></span>
            </v-card-title>
            <v-card-tex>
                <v-form>
                    <v-row>
                        <v-col cols="6">
                            <v-text-field v-model="FormData.title" label="Title"></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            <v-textarea v-model="FormData.description" label="Event description"></v-textarea>
                        </v-col>
                        <v-col cols="6">
                            <v-text-field v-model="FormData.cost" label="Event cost"></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            <v-text-field v-model="FormData.venue" label="venue"></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            <v-text-field v-model="FormData.startDate" label="Start date"></v-text-field>
                        </v-col>
                        <v-col cols="6">
                            <v-text-field v-model="FormData.endDate" label="End date"></v-text-field>
                        </v-col>
                        <v-col cols="6">

                        </v-col>
                    </v-row>
                </v-form>
            </v-card-tex>
        </v-card>
    </v-container>
</template>
<script>
export default {
    name: "CreateEventComponent",
    data() {
        return {
            FormData: {
                title: "",
                description: "",
                cost: 0,
                venue: "",
                startDate: "",
                endDate: ""
            }
        }
    }
}
</script>
<style scoped></style>