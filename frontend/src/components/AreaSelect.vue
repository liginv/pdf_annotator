<template>
  <div>
    <!--select name="" id="myselect" :style="styleContainer">
      <option value="">Option 1</option>
      <option value="">Option 2</option>
    </select-->
    <div class='selection-box' :style="styleObject">
      <span v-if="fill === false">{{ name }}</span>
      <span v-if="fill === true">{{ entry[keyid] }}</span>
      <!--input type="text" :value="name"-->
    </div>
  </div>
</template>

<script>
import randomColor from 'randomcolor'

export default {
  name: 'area-select',
  props: ['coordinates', 'name', 'active', 'dimensions', 'pageoffset_top', 'pageoffset_left', 'fill', 'entry', 'keyid', 'highlight'],
  created () {
    // console.log(this.entry)
    // console.log(this.keyid)
    // textFit(document.getElementsByClassName('selection-box'))
    console.log('AreaSelect created')
    console.log(this.fill, this.coordinates, this.coordinates.left)
    console.log(this.coordinates.pageOffset_left)
    // console.log({offset: this.pageoffset})
    // console.log(this.coordinates.lx)
    // console.log(this.coordinates.zname)
  },
  updated () {
  //   if (this.fill === true) {
  //     this.name = this.entry[this.keyid]
  //     console.log(this.entry[this.keyid])
  //   }
  },
  data () {
    return {
      color: randomColor({format: 'rgb'})
    }
  },
  computed: {
    styleObject: function () {
      // if (this.coordinates.ly - this.coordinates.ry === 0 || this.coordinates.rx - this.coordinates.lx === 0) {
      //   return {
      //     display: 'none'
      //   }
      // }
      if (this.height === 0 || this.width === 0) {
        return {
          display: 'none'
        }
      }
      if (this.fill === false) {
        if (this.coordinates.zname === this.highlight) {
          return {
            // left: this.coordinates.lx + this.pageoffset.left + 'px',
            // top: this.dimensions.height - this.coordinates.ly + this.pageoffset.top - 3 + 'px',
            // width: this.coordinates.rx - this.coordinates.lx + 'px',
            // height: this.coordinates.ly - this.coordinates.ry + 'px',
            left: this.coordinates.left + this.coordinates.pageOffset_left - 1 + 'px',
            top: this.coordinates.top + this.coordinates.pageOffset_top - 4 + 'px',
            width: this.coordinates.width + 'px',
            height: this.coordinates.height + 'px',
            border: 'solid ' + this.color + ' 3px',
            background: this.color.replace(/\)$/, ', 0.05)').replace('rgb(', 'rgba(')
          }
        } else {
          return {
            // left: this.coordinates.lx + this.pageoffset.left + 'px',
            // top: this.dimensions.height - this.coordinates.ly + this.pageoffset.top - 3 + 'px',
            // width: this.coordinates.rx - this.coordinates.lx + 'px',
            // height: this.coordinates.ly - this.coordinates.ry + 'px',
            left: this.coordinates.left + this.coordinates.pageOffset_left + 'px',
            top: this.coordinates.top + this.coordinates.pageOffset_top - 3 + 'px',
            width: this.coordinates.width + 'px',
            height: this.coordinates.height + 'px',
            border: 'solid ' + this.color + ' 1px',
            background: this.color.replace(/\)$/, ', 0.05)').replace('rgb(', 'rgba(')
          }
        }
      } else {
        return {
          // left: this.coordinates.lx + this.pageoffset.left + 1 + 'px',
          // top: this.dimensions.height - this.coordinates.ly + this.pageoffset.top - 5 + 'px',
          // width: this.coordinates.rx - this.coordinates.lx + 'px',
          // height: this.coordinates.ly - this.coordinates.ry + 'px',
          left: this.coordinates.left + this.coordinates.pageOffset_left + 'px',
          top: this.coordinates.top + this.coordinates.pageOffset_top - 5 + 'px',
          width: this.coordinates.width + 'px',
          height: this.coordinates.height + 'px',
          opacity: 1
        }
      }
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
  word-break: break-all;
}

input {
 position: absolute;
 z-index: 2000;
}

span {
  top: 0em;
  overflow: visible;
  color: black;
  display: inline;
  /* font-weight: bold; */
  font-size: 10px;
  text-shadow: white 0px 0px 2px, white 0px 0px 2px, white 0px 0px 5px, white 0px 0px 5px, white 0px 0px 30px, white 0px 0px 30px, white 0px 0px 30px, white 0px 0px 30px, white 0px 0px 30px, white 0px 0px 60px, white 0px 0px 60px, white 0px 0px 60px;
}

</style>
