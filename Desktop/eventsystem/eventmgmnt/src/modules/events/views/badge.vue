<template>
  <svg
    version="1.0"
    xmlns="http://www.w3.org/2000/svg"
    width="1020.000000pt"
    height="1020.000000pt"
    viewBox="0 0 65.000000 63.000000"
    preserveAspectRatio="xMidYMid meet"
    class="div--badge"
  >
    <g
      transform="translate(0.000000,63.000000) scale(0.100000,-0.100000)"
      :fill="$vuetify.theme.themes.light.secondary"
      stroke="none"
    >
      <path
        d="M205 548 c-68 -25 -113 -67 -146 -133 -28 -58 -31 -72 -27 -128 6 -68 21 -106 65 -157 65 -78 199 -103 298 -56 198 93 199 361 1 463 -38 20 -151 27 -191 11z m149 -22 c67 -20 114 -61 142 -120 30 -64 33 -154 7 -184 -29 -32 -231 -152 -255 -152 -40 1 -112 45 -145 89 -104 135 -40 321 127 372 39 12 73 10 124 -5z m95 -402 c-15 -19 -69 -47 -76 -41 -2 3 12 13 31 22 20 10 39 21 42 26 3 5 8 9 11 9 3 0 0 -7 -8 -16z"
      />
    </g>
    <foreignObject width="100%" height="100%" x="9.5" y="16.5">
      <div xmlns="http://www.w3.org/1999/xhtml" class="text--div">
        {{ cpdCaption }}
      </div>
    </foreignObject>
  </svg>
</template>

<script>
export default {
  name: "Badge",
  props: {
    cpdCaption: {
      type: String,
      default: "",
    },
  },
};
</script>
<style scoped>
.div--badge {
  width: 100%;
  height: 90%;
}
.text--div {
  font-weight: 900;
  font-family: Arial;
  font-size: 5px;
  line-height: 8px;
  letter-spacing: 0.15em;
  color: var(--v-secondary-base);
  text-align: center;
  width: 40px;
  height: 45px;
}
</style>
