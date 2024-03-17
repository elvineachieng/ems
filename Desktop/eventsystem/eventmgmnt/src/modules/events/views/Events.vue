<template>
  <v-container fluid style="width: 90%">
    <v-row>
      <v-col cols="12" md="5" id="display1">
        <v-card
          flat
          class="d-flex align-center justify-center"
          :min-height="$vuetify.breakpoint.mdAndUp ? '250' : '100'"
        >
          <v-card-title class="text--primary">
            <span
              class="text-md-h4 font-weight-bold mb-3"
              style="word-break: break-word"
            >
              Events and Packages
            </span>

            <span
              class="text-body-1 font-weight-bolder"
              style="word-break: break-word"
            >
              {{ front_excerpt }}
            </span>
          </v-card-title>
        </v-card>
      </v-col>

      <v-col cols="12" md="7" id="display2">
        <v-carousel
          cycle
          height="250"
          hide-delimiter-background
          hide-delimiters
          show-arrows-on-hover
        >
          <v-carousel-item v-for="(item, i) in carouselEvents" :key="i">
            <v-card height="100%" rounded>
              <v-row
                class="fill-height"
                align="center"
                justify="center"
                :style="`background-image: url(${
                  url + item.base64Logo
                }); background-size: cover; background-position: center; border-radius: 10px;`"
              >
                <div>
                  <v-card flat tile class="pa-2 mt-auto carousel--card">
                    <div class="d-flex justify-end flex-column">
                      <div
                        class="text-lg-h5 primary--text font-weight-bold text-truncate align-self-end"
                      >
                        {{ item.description }}
                      </div>

                      <div
                        class="text-body-2 primary--text font-weight-bold text-truncate align-self-end"
                      >
                        {{ getFormattedDate(item.startDate) }} to
                        {{ getFormattedDate(item.endDate) }}
                      </div>
                    </div>
                  </v-card>
                </div>
              </v-row>
            </v-card>
          </v-carousel-item>
        </v-carousel>
      </v-col>
    </v-row>

    <v-row>
      <v-divider></v-divider>
    </v-row>

    <v-row>
      <v-col cols="12" md="8">
        <div style="overflow-y: scroll; max-width: 100%;">
          <v-btn-toggle color="primary" dense v-model="term">
            <v-btn small value=" "> All </v-btn>

            <v-btn
              small
              v-for="(item, i) in eventTypes"
              :key="i"
              :value="item.code"
            >
              <span>{{ item.code | capitalize }}</span>
            </v-btn>
          </v-btn-toggle>
        </div>
      </v-col>

      <v-col cols="12" md="4">
        <v-text-field
          outlined
          v-model="term"
          placeholder="Search Events ..."
          dense
        >
          <template v-slot:append>
            <v-icon left>search</v-icon>
          </template>
        </v-text-field>
      </v-col>
    </v-row>

    <v-card flat class="mt-n5">
      <v-card-title class="">
        <span class="ml-n4">Active Events</span>
        <v-spacer />
        <v-btn-toggle
          color="primary"
          v-model="displayType"
          mandatory
          class="mr-4"
          borderless
          active-class="primary--text"
        >
          <v-tooltip bottom v-for="(item, i) in displayTypes" :key="i">
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                text
                v-on="on"
                v-bind="attrs"
                :value="item.value"
                :title="item.text"
              >
                {{ $vuetify.breakpoint.mdAndUp ? "" : item.text }}
                <v-icon>{{ item.icon }}</v-icon>
              </v-btn>
            </template>
            <span>{{ item.text }}</span>
          </v-tooltip>
        </v-btn-toggle>
      </v-card-title>

      <EventCards v-if="displayType === 'grid'" :events="events" />
      <EventList v-if="displayType === 'list'" :events="events" />
    </v-card>
  </v-container>
</template>
<script>
import eventMixin from "../eventMixin";
import EventCards from "./EventCards";
import EventList from "./EventList.vue";
import { eventListing } from "@/environment/environment";
export default {
  name: "Events",
  mixins: [eventMixin],
  components: {
    EventCards,
    EventList,
  },
  data: function () {
    return {
      term: "",
      selectedType: "",
      type: "week",
      focus: "",
      typeToLabel: {
        week: "Week",
        month: "Month",
        day: "Day",
        year: "year",
      },
      displayType: eventListing,
      displayTypes: [
        { text: "List", value: "list", icon: "format_list_bulleted" },
        { text: "Grid", value: "grid", icon: "grid_view" },
      ],
    };
  },

  beforeRouteEnter: function (to, from, next) {
    next((v) => {
      v.$store.dispatch("Events/getEvents");
      v.$store.dispatch("Events/getEventTypes");
      v.$store.dispatch("Events/getAllMeta");
    });
  },

  computed: {
    events() {
      return (
        this.$store.getters["Events/events"]
          .filter((e) => {
            if (this.term === undefined) return true;

            return (
              e.eventType.toLowerCase().indexOf(this.term.toLowerCase()) > -1 ||
              e.description.toLowerCase().indexOf(this.term.toLowerCase()) >
                -1 ||
              e.location.toLowerCase().indexOf(this.term.toLowerCase()) > -1 ||
              e.startDate.indexOf(this.term) > -1
            );
          })
          .filter((e) => {
            return this.eventTypes.find((type) => type.code === e.eventType);
          }) || []
      ).sort((a, b) => new Date(a.startDate) - new Date(b.startDate));
    },
    carouselEvents() {
      return this.events ? this.events.filter((item) => item.featured) : [];
    },
    eventTypes() {
      return this.$store.getters["Events/eventsTypes"].filter((type) => {
        return !type.internalEvent;
      });
    },
    metadata() {
      return this.$store.getters["Events/metadata"];
    },
    front_excerpt() {
      return process.env.VUE_APP_FRONT_EXCERPT ?? "...";
    },
  },

  methods: {
    setToday: function () {
      this.focus = "";
    },

    calendarNavigate: function (direction) {
      Event.$emit("calender-navigate", direction);
    },

    images(number) {
      return require(`@/assets/images/picture${number}.jpg`);
    },

    meta(number) {
      if (this.metadata) {
        const data = this.metadata
          .filter((item) => item.eventNo === number)
          .shift();
        return data ? data.image : null;
      }
    },
  },
};
</script>
<style>
@media (max-width: 768px) {
  #display1 {
    order: 2;
  }
  #display2 {
    order: 1;
  }
}
.cpd--chip {
  position: absolute !important;
  top: 10px !important;
  right: 10px !important;
}

.carousel--card {
  position: absolute;
  bottom: 0%;
  width: 75%;
  right: 0;
}
</style>
