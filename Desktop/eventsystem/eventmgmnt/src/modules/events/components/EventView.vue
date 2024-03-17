<template>
  <v-container
    fluid
    class="mx-auto"
    ref="eventViewContainer"
    :style="$vuetify.breakpoint.mdAndUp ? 'width: 75%' : 'width: 100%'"
  >
    <v-card v-if="event.no !== decryptedRoute.params.no" flat>
      <v-row>
        <v-col cols="12" md="6">
          <v-skeleton-loader
            type="card, list-item-three-line, card-heading, list-item-three-line"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-skeleton-loader
            type="list-item-three-line, list-item-avatar, card-heading"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="2" v-for="col in 5" :key="col">
          <v-skeleton-loader type="avatar" />
        </v-col>
        <v-col cols="12">
          <v-skeleton-loader type="image" />
        </v-col>
      </v-row>
    </v-card>

    <v-card v-if="event.no === decryptedRoute.params.no" flat class="mt-2">
      <v-row>
        <v-col cols="12" md="7">
          <v-card flat>
            <v-img
              :src="url + event.base64Logo"
              :lazy-src="require(`@/assets/images/picture4.jpg`)"
              :height="$vuetify.breakpoint.mdAndUp ? '454px' : '224px'"
              :width="$vuetify.breakpoint.mdAndUp ? '800px' : '320px'"
              style="border-radius: 5px"
              class="mx-auto"
            />

            <v-card-title> Event Information </v-card-title>

            <v-card-text v-html="event.excerpt" />

            <v-card-title> Event Attachments </v-card-title>

            <v-card-text>
              <v-row>
                <v-col
                  cols="4"
                  v-for="(attachment, i) in event.eventsDocuments"
                  :key="i"
                >
                  <v-sheet
                    :color="fileMeta(attachment.documentFormat).color"
                    dark
                    outlined
                    rounded
                  >
                    <v-list-item link @click="viewDoc(attachment)">
                      <v-list-item-icon>
                        <v-icon>
                          {{ fileMeta(attachment.documentFormat).icon }}
                        </v-icon>
                      </v-list-item-icon>

                      <v-list-item-content>
                        <v-list-item-title>
                          {{ attachment.documentDescription }}
                        </v-list-item-title>
                        <v-list-item-subtitle>
                          {{ attachment.description }}
                        </v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                  </v-sheet>
                </v-col>
              </v-row>
            </v-card-text>

            <v-card-text>
              <EventCountdown :start-date="getStartTime" />
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="5">
          <v-card flat class="mx-auto">
            <v-row no-gutters>
              <v-col cols="12" md="10">
                <!-- Description -->
                <div
                  class="text-capitalize text-wrap text-lg-h4 font-weight-bold"
                >
                  {{ event.description }}
                </div>
                <!-- Date and time -->
                <div>
                  <v-icon small>mdi-calendar-multiselect</v-icon>
                  <span> Upcoming: {{ formatDate(event.startDate, 6) }} </span>
                  <br />

                  <div v-if="event.location !== 'Online'">
                    <a
                      class="text-capitalize mt-2 text-body-1 font-weight-bold text-justify text-decoration-none"
                      @click="
                        $vuetify.goTo('#map', {
                          duration: 500,
                          easing: 'easeInOutCubic',
                        })
                      "
                    >
                      <v-icon color="primary">mdi-map-marker</v-icon>
                      {{ event.location }}
                    </a>
                  </div>

                  <span v-else class="font-weight-bold">{{
                    event.location
                  }}</span>
                </div>
              </v-col>
              <v-col cols="12" md="2">
                <div style="width: 120%">
                  <badge v-if="event.cPDTerms" :cpd-caption="event.cPDTerms" />
                  <CPDbadge v-else :cpd-points="event.cpdHours" />
                </div>
              </v-col>
            </v-row>
            <!-- slots -->
            <v-list dense class="mt-n2">
              <v-list-item dense class="pa-0">
                <v-list-item-content
                  class="stats"
                  v-if="parseInt(event.remainingSlots) !== 0"
                >
                  <v-list-item-subtitle>
                    <v-avatar
                      class="secondary lighten-5 text--darken-4 text-center mr-2"
                      size="30"
                    >
                      <span
                        class="secondary--text text--darken-4 text-center text-body-1 font-weight-bold"
                        >{{ event.remainingSlots }}</span
                      >
                    </v-avatar>
                    <span class="text-body-2 font-weight-bold"
                      >Slots Available</span
                    >
                  </v-list-item-subtitle>
                </v-list-item-content>

                <v-list-item-content class="stats" v-else>
                  <div class="textStyle">Slots Available</div>

                  <v-list-item-subtitle class="textStyle2">
                    {{ event.slots }}
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>

            <section
              v-if="orgName === 'IEK' && event.no === 'EV-23-000026'"
              class="eventCostSection"
            >
              <v-btn
                @click="
                  $root.routeTo({
                    name: 'booking',
                    params: { no: event.no },
                  })
                "
                color="primary"
                class="toggleButtons mx-2"
                style="float: right"
              >
                <v-icon left>book_online</v-icon>
                {{ settings.BookHere }}
              </v-btn>
              <div class="section-filters">
                <!-- <button
                  @click="setIEKPhysical(key)"
                  v-for="(att, key) in iekSpecificEvent"
                  :key="key"
                  :class="{ activeAttendance: key === firstButtonIndex }"
                >
                  {{ att }}
                </button> -->
                <h4 class="activeAttendance">Physical Attendance</h4>
              </div>
              <table class="table">
                <tHead>
                  <tr>
                    <th></th>
                    <th>
                      <p>Early Bird</p>
                      (before 1st Oct)
                    </th>
                    <th>
                      <p>Regular</p>
                      (after 1st Oct)
                    </th>
                  </tr>
                </tHead>
                <tBody>
                  <tr>
                    <td>IEK Member in good standing</td>
                    <td>40000 (KES)</td>
                    <td>45000 (KES)</td>
                  </tr>
                  <tr>
                    <td>IEK Member not in good standing</td>
                    <td>45000 (KES)</td>
                    <td>50000 (KES)</td>
                  </tr>
                  <tr>
                    <td>IEK Non-Member</td>
                    <td>45000 (KES)</td>
                    <td>50000 (KES)</td>
                  </tr>
                  <tr>
                    <td>Foreign Delegate</td>
                    <td>380 (USD)</td>
                    <td>380 (USD)</td>
                  </tr>
                </tBody>
              </table>
              <div class="section-filters">
                <h4 class="activeAttendance">Virtual Attendance</h4>
              </div>
              <table class="table">
                <tHead>
                  <tr>
                    <th></th>
                    <th>
                      <p>Early Bird</p>
                      (before 1st Oct)
                    </th>
                    <th>
                      <p>Regular</p>
                      (after 1st Oct)
                    </th>
                  </tr>
                </tHead>
                <tBody>
                  <tr>
                    <td>IEK Member in good standing</td>
                    <td>15000 (KES)</td>
                    <td>20000 (KES)</td>
                  </tr>
                  <tr>
                    <td>IEK Member not in good standing</td>
                    <td>20000 (KES)</td>
                    <td>25000 (KES)</td>
                  </tr>
                  <tr>
                    <td>IEK Non-Member</td>
                    <td>20000 (KES)</td>
                    <td>25000 (KES)</td>
                  </tr>
                  <tr>
                    <td>Foreign Delegate</td>
                    <td>150 (USD)</td>
                    <td>150 (USD)</td>
                  </tr>
                  <tr>
                    <td>Undergraduate Student</td>
                    <td>3000 (KES)</td>
                    <td>3000 (KES)</td>
                  </tr>
                </tBody>
              </table>
            </section>
            <template v-else>
              <!-- Buttons -->
              <v-row dense>
                <v-col cols="6" md6 sm6>
                  <v-btn
                    depressed
                    @click="
                      $root.routeTo({
                        name: 'booking',
                        params: { no: event.no },
                      })
                    "
                    color="primary"
                    class="toggleButtons mx-2"
                    block
                  >
                    <v-icon left>book_online</v-icon>
                    {{ settings.BookHere }}
                  </v-btn>
                </v-col>
                <!--Button for site Visit-->
                <v-col cols="6" md6 sm6>
                  <v-btn
                    depressed
                    v-if="event.hasRelatedEvent"
                    @click="showRelatedEventDialog()"
                    color="primary"
                    class="toggleButtons mx-2"
                    block
                  >
                    <v-icon left>event</v-icon>
                    {{ settings.SiteVisit }}
                  </v-btn>
                </v-col>
              </v-row>
              <!--Event costs-->
              <v-card-title
                v-if="filteredPackages.eventCosts.length !== 0"
                class="pb-0"
                >Event Costs</v-card-title
              >
              <v-card-text>
                <v-list dense class="pa-0">
                  <div
                    v-for="(cost, i) in filteredPackages.eventCosts
                      .slice()
                      .reverse()"
                    :key="i"
                  >
                    <v-list-item class="pa-0" dense ripple three-line>
                      <v-list-item-content>
                        <v-list-item-title class="text-button">
                          {{ cost.description }}
                          {{
                            cost.appliesType.trim() !== ""
                              ? `(${cost.appliesType})`
                              : ""
                          }}
                        </v-list-item-title>

                        <!-- Early bird -->
                        <div
                          class="d-flex flex-row"
                          v-if="cost.earlyBirdAmountInclVAT !== 0"
                        >
                          <div
                            class="text-subtitle-1 font-weight-light ml-2 mr-7"
                            style="width: 80px"
                          >
                            EarlyBird:
                          </div>
                          <div>
                            <!-- foreign -->
                            <v-list-item-subtitle
                              class="overline"
                              v-if="cost.currencyCode !== 'KES'"
                            >
                              <div class="d-flex">
                                <div class="mr-2" style="width: 90px">
                                  foreign:
                                </div>
                                <div class="green--text">
                                  {{ cost.currencyCode }}
                                  {{ cost.earlyBirdAmountInclVAT | currency }}
                                </div>
                              </div>
                            </v-list-item-subtitle>
                            <!-- lcy -->
                            <v-list-item-subtitle class="overline">
                              <div class="d-flex">
                                <div class="mr-2" style="width: 90px">LCY:</div>
                                <div class="green--text">
                                  KES
                                  {{ cost.earlyBirdAmountInclLCY | currency }}
                                </div>
                              </div>
                            </v-list-item-subtitle>
                          </div>
                        </div>

                        <v-divider v-if="cost.earlyBirdAmountInclVAT" inset />

                        <!-- Normal -->
                        <div class="d-flex flex-row">
                          <div
                            class="text-subtitle-1 font-weight-light ml-2 mr-7"
                            style="width: 80px"
                          >
                            Normal:
                          </div>
                          <div>
                            <!-- foreign -->
                            <v-list-item-subtitle
                              class="overline"
                              v-if="cost.currencyCode !== 'KES'"
                            >
                              <div class="d-flex flex-row">
                                <div class="mr-2">
                                  <div style="width: 90px">
                                    Foreign
                                    {{
                                      cost.appliesType.trim() === "" &&
                                      cost.membershipCategory.trim() === ""
                                        ? ""
                                        : ", "
                                    }}
                                    {{
                                      getDescription(cost.membershipCategory)
                                    }}
                                    :
                                  </div>
                                </div>
                                <div class="green--text">
                                  {{ cost.currencyCode }}
                                  {{ cost.amountIncludingVAT | currency }}
                                </div>
                              </div>
                            </v-list-item-subtitle>
                            <!-- lcy -->
                            <v-list-item-subtitle class="overline">
                              <div class="d-flex">
                                <div class="mr-2" style="width: 90px">
                                  LCY
                                  {{
                                    cost.appliesType.trim() === "" &&
                                    cost.membershipCategory.trim() === ""
                                      ? ""
                                      : ", "
                                  }}
                                  {{ getDescription(cost.membershipCategory) }}
                                  :
                                </div>
                                <div class="green--text">
                                  KES {{ cost.amountInclLCY | currency }}
                                </div>
                              </div>
                            </v-list-item-subtitle>
                          </div>
                        </div>
                      </v-list-item-content>
                    </v-list-item>
                  </div>
                </v-list>
              </v-card-text>

              <!--Packages-->
              <v-card-title v-if="filteredPackages.otherpackages.length !== 0"
                >Packages</v-card-title
              >

              <v-card-text>
                <v-list
                  dense
                  v-if="filteredPackages.otherpackages.length !== 0"
                >
                  <div
                    v-for="(cost, i) in filteredPackages.otherpackages
                      .slice()
                      .reverse()"
                    :key="i"
                  >
                    <v-list-item
                      dense
                      ripple
                      :two-line="cost.amountIncludingVAT !== 0"
                    >
                      <v-list-item-content>
                        <v-list-item-title>
                          {{ cost.description }}
                        </v-list-item-title>

                        <v-list-item-subtitle
                          class="green--text overline text-wrap"
                          v-if="cost.amountIncludingVAT !== 0"
                        >
                          KES{{ cost.amountInclLCY | currency }}
                        </v-list-item-subtitle>

                        <v-list-item-title
                          v-if="
                            cost.amountIncludingVAT !== 0 &&
                            cost.currencyCode !== 'KES'
                          "
                        >
                          Foreign Delegate
                        </v-list-item-title>

                        <v-list-item-subtitle
                          class="green--text overline text-wrap"
                          v-if="
                            cost.amountIncludingVAT !== 0 &&
                            cost.currencyCode !== 'KES'
                          "
                        >
                          {{ cost.currencyCode }}
                          {{ cost.amountIncludingVAT | currency }}
                        </v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                  </div>
                </v-list>
              </v-card-text>
            </template>
            <v-card-title> Contact information </v-card-title>

            <v-card-text>
              <h4>Contact Person</h4>
              <p>{{ event.contactPersonName }}</p>

              <h4>Phone</h4>
              <p>{{ event.contactPersonPhoneNo }}</p>

              <h4>Email</h4>
              <p>{{ event.contactPersonEmail }}</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row no-gutters class="mb-16">
        <v-col cols="12">
          <div class="d-flex justify-start">
            <v-img
              :height="$vuetify.breakpoint.mobile ? '100%' : '100'"
              v-for="(sponsor, i) in event.eventSponsor"
              :key="i"
              contain
              width="10%"
              class="align-self-start"
              :src="url + sponsor.base64Picture"
            />
          </div>
        </v-col>
        <v-col cols="12" style="position: relative; z-index: 1">
          <v-card class="my-4" id="map">
            <div style="height: 400px; width: 100%">
              <l-map
                :zoom="leafMap.zoom"
                :center="leafMap.center"
                :options="leafMap.mapOptions"
                style="height: 100%"
                @update:center="centerUpdate"
                @update:zoom="zoomUpdate"
              >
                <l-tile-layer
                  :url="leafMap.url"
                  :attribution="leafMap.attribution"
                />

                <l-marker :lat-lng="leafMap.withPopup">
                  <l-popup>
                    <div>I am a popup</div>
                  </l-popup>
                </l-marker>
              </l-map>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-card>

    <PreviewDialog
      :dialog="dialog"
      @close-dialog="closeDialog"
      :document="document"
    />
    <ChildEventsDialog
      :dialog="relatedEventDialog"
      :events="relatedEvent"
      @close-dialog="closeRelatedEventDialog"
    />
  </v-container>
</template>

<script>
import { helper } from "../../../utilities";
import eventMixin from "../eventMixin";
import { latLng, Icon } from "leaflet";
import { LMap, LTileLayer, LMarker, LPopup } from "vue2-leaflet";
import "leaflet/dist/leaflet.css";
import PreviewDialog from "./PreviewDialog.vue";
import CPDbadge from "../views/CPDbadge.vue";
import badge from "../views/badge.vue";
import EventCountdown from "./EventCountdown.vue";
import { company } from "../../../environment/environment";
import ChildEventsDialog from "./ChildEventsDialog.vue";

// Fix for icon Markers
delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});

export default {
  name: "EventView",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
    PreviewDialog,
    CPDbadge,
    badge,
    EventCountdown,
    ChildEventsDialog,
  },
  mixins: [eventMixin],
  data: function () {
    return {
      isPhysicalForIEK: true,
      firstButtonIndex: 0,
      iekSpecificEvent: ["Physical Attendance", "Virtual Attendance"],
      delegateCategory: "Member",
      map: {
        lat: "",
        long: "",
      },
      dialog: false,
      relatedEventDialog: false,
      document: null,
      orgName: company,
    };
  },

  beforeRouteEnter(to, from, next) {
    next((v) => {
      v.$store.dispatch(
        "Events/getEventMeta",
        v.$root.decryptRoute(to).params.no
      );
      v.$store.dispatch("Events/getEvent", v.$root.decryptRoute(to).params.no);
      v.$store.dispatch("Events/getMembershipCategories");
    });
  },

  mounted() {
    // scroll to top of page
    window.scrollTo(0, 0);
  },

  computed: {
    iekPricingTable() {
      return [
        {
          type: "Member",
          cost: 40000,
          currencyCode: "KES",
          ticketType: "earlyBird",
          physical: true,
        },
        {
          type: "Member-not-in-good-standing",
          cost: 45000,
          currencyCode: "KES",
          ticketType: "earlyBird",
          physical: true,
        },
        {
          type: "Non-Member",
          cost: 45000,
          currencyCode: "KES",
          ticketType: "earlyBird",
          physical: true,
        },
        {
          type: "Member",
          cost: 45000,
          currencyCode: "KES",
          ticketType: "regular",
          physical: true,
        },
        {
          type: "Member-not-in-good-standing",
          cost: 50000,
          currencyCode: "KES",
          ticketType: "regular",
          physical: true,
        },
        {
          type: "Non-Member",
          cost: 50000,
          currencyCode: "KES",
          ticketType: "regular",
          physical: true,
        },
        {
          type: "Member",
          cost: 15000,
          currencyCode: "KES",
          ticketType: "earlyBird",
          physical: false,
        },
        {
          type: "Member-not-in-good-standing",
          cost: 20000,
          currencyCode: "KES",
          ticketType: "earlyBird",
          physical: false,
        },
        {
          type: "Non-Member",
          cost: 20000,
          currencyCode: "KES",
          ticketType: "earlyBird",
          physical: false,
        },
        {
          type: "Member",
          cost: 20000,
          currencyCode: "KES",
          ticketType: "regular",
          physical: false,
        },
        {
          type: "Member-not-in-good-standing",
          cost: 25000,
          currencyCode: "KES",
          ticketType: "regular",
          physical: false,
        },
        {
          type: "Non-Member",
          cost: 25000,
          currencyCode: "KES",
          ticketType: "regular",
          physical: false,
        },
        {
          type: "foreign",
          cost: 380,
          currencyCode: "USD",
          ticketType: "earlyBird",
          physical: true,
        },
        {
          type: "foreign",
          cost: 380,
          currencyCode: "USD",
          ticketType: "regular",
          physical: true,
        },
        {
          type: "foreign",
          cost: 150,
          currencyCode: "USD",
          ticketType: "earlyBird",
          physical: false,
        },
        {
          type: "foreign",
          cost: 150,
          currencyCode: "USD",
          ticketType: "regular",
          physical: false,
        },
        {
          type: "student",
          cost: 3000,
          currencyCode: "KES",
          ticketType: "earlyBird",
          physical: false,
        },
        {
          type: "student",
          cost: 3000,
          currencyCode: "KES",
          ticketType: "regular",
          physical: false,
        },
      ];
    },
    cpd_caption() {
      return process.env.VUE_APP_CPD_CAPTION;
    },

    getStartTime() {
      // combine startDate and startTime
      return this.event
        ? new Date(this.event.startDate + " " + this.event.startTime)
        : new Date();
    },

    event() {
      return this.$store.getters["Events/event"];
    },
    //fn ()get related event
    relatedEvent() {
      if (this.event) {
        if (this.event.relatedEvent && this.event.relatedEvent.length > 0) {
          return this.event.relatedEvent;
        }
      }
      return {};
    },
    leafMap() {
      //-1.2832533,36.8172449

      let latLong = latLng(
        parseFloat(this.event.gPSLatitude),
        parseFloat(this.event.gPSLongitude)
      );

      return {
        zoom: 13,
        center: latLong,
        url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        attribution:
          '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        withPopup: latLong,
        withTooltip: latLong,
        currentZoom: 11.5,
        currentCenter: latLong,
        showParagraph: false,
        mapOptions: {
          zoomSnap: 0.5,
        },
        showMap: true,
      };
    },

    filteredPackages() {
      let eventpackages = {
        eventCosts: [],
        otherpackages: [],
      };

      if (this.event)
        this.event.eventPackageCost
          ? this.event.eventPackageCost.forEach((cost) => {
              if ((cost.defaultPackage || cost.mandatory) && !cost.hideCost) {
                eventpackages.eventCosts.push(cost);
              }

              if (!cost.mandatory && !cost.hideCost)
                eventpackages.otherpackages.push(cost);
            })
          : [];

      return eventpackages;
    },

    decryptedRoute() {
      return this.$root.decryptRoute(this.$route);
    },

    membershipCategories() {
      return this.$store.getters["Events/membershipCategories"];
    },
    settings() {
      return JSON.parse(window.localStorage.getItem("aquila_captions"));
    },
  },

  methods: {
    setIEKPhysical(id) {
      this.firstButtonIndex = id;
      if (this.isPhysicalForIEK && id !== 0) {
        this.isPhysicalForIEK = !this.isPhysicalForIEK;
        return;
      }
      if (!this.isPhysicalForIEK && id === 0) {
        this.isPhysicalForIEK = !this.isPhysicalForIEK;
        return;
      }
    },
    fileMeta: function (file) {
      return {
        icon: helper.getFileIcon(file),
        color: helper.getFileIconColor(file),
      };
    },

    isEarlyBird: function (eventPackage) {
      return new Date(eventPackage.earlyBirdCutoffDate) > new Date();
    },

    zoomUpdate(zoom) {
      this.currentZoom = zoom;
    },

    centerUpdate(center) {
      this.currentCenter = center;
    },

    images(number) {
      return require(`@/assets/images/picture${number}.jpg`);
    },

    closeDialog: function (val) {
      this.dialog = val;
    },

    getDescription(item) {
      const category = this.membershipCategories.filter(
        (category) => category.Code === item
      )[0];
      return category ? category.Description : "";
    },
    //fn ()-> add book for site-visit
    showRelatedEventDialog() {
      this.relatedEventDialog = true;
    },
    closeRelatedEventDialog() {
      this.relatedEventDialog = false;
    },
  },
  //fn -> watch for relatedEvent & dispatch action
  watch: {
    relatedEvent(newVal) {
      if (newVal) {
        const eve = newVal.map((item) => {
          return {
            no: item.childEventNo,
          };
        });
        this.$store.dispatch("Events/getRelatedEvent", eve);
      }
    },
  },
};
</script>
<style>
@import "../EventView.css";
</style>
