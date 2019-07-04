<template>
  <div>
    <!--select name="" id="myselect" :style="styleContainer">
      <option value="">Option 1</option>
      <option value="">Option 2</option>
    </select-->
    <div class='selection-box' :style="styleObject">
      <span>{{ name }}</span>
      <!--input type="text" :value="name"-->
    </div>
  </div>
</template>

<script>
export default {
  name: 'area-select',
  props: ['coordinates', 'color', 'name', 'active', 'dimensions', 'pageoffset'],
  data () {
    return {
      styleContainer: null
    }
  },
  created () {
    console.log('AreaSelect created')
    // console.log({offset: this.pageoffset})
    // console.log(this.coordinates.lx)
    // console.log(this.coordinates.zname)
  },
  computed: {
    styleObject: function () {
      if (this.coordinates.ly - this.coordinates.ry === 0 || this.coordinates.rx - this.coordinates.lx === 0) {
        this.styleContainer = {
          display: 'none'
        }
      } else {
        this.styleContainer = {
          left: this.coordinates.lx + this.pageoffset.left + 'px',
          top: this.dimensions.height - this.coordinates.ly + this.pageoffset.top + 'px',
          width: this.coordinates.rx - this.coordinates.lx + 'px',
          height: this.coordinates.ly - this.coordinates.ry + 'px',
          border: 'solid ' + this.color + ' 1px',
          background: this.color.replace(/\)$/, ', 0.05)').replace('rgb(', 'rgba(')
        }
      }
      return this.styleContainer
    }
  }
}
</script>

<style scoped>
.selection-box {
  position: absolute;
  pointer-events: none;
  text-align: center;
  z-index: 1000;
  overflow:visible;
}

input {
 position: absolute;
 z-index: 2000;
}

span {
  overflow: visible;
  color: black;
  display: inline;
  font-weight: bold;
  font-size: 12px;
  text-shadow: white 0px 0px 2px, white 0px 0px 2px, white 0px 0px 5px, white 0px 0px 5px, white 0px 0px 30px, white 0px 0px 30px, white 0px 0px 30px, white 0px 0px 30px, white 0px 0px 30px, white 0px 0px 60px, white 0px 0px 60px, white 0px 0px 60px;
}

</style>
