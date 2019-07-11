<template>
  <div>
    <h3 v-if="name">
      Currently working on: <span class="filename">{{ name }}</span>
      <span class="filetype">{{ arrayBuffer ? "PDF" : "image" }}</span>
    </h3>
    <!-- <p>If you want to zoom in/out, you'll need to use your browser zoom for the moment.</p> -->
    <div class='selection-area' @mousedown="start" @mouseup="end" @mousemove="drag" v-if="src || arrayBuffer" ref="selectionArea">
      <img :src="src" v-if="src">
      <PDF @get="getcan" :getcan="getcan" :setPdfSize="setPdfSize" :arrayBuffer="arrayBuffer" v-if="arrayBuffer"></PDF>
      <div class="area-select">
      <SelectionPreview :znamech="znamech" :coordinates="coordinates" v-if="arrayBuffer"></SelectionPreview>
      <AreaSelect :highliht="null" :fill="fill" :coordinates="coordinates" ref="activeSelector" color="rgb(0,255,0)" active="true"></AreaSelect>
      <div v-if="fill === false">
      <AreaSelect v-for="(ob,ind) in obs"
        :key="old_obs.length + ind"
        :coordinates="ob"
        :name="ob.zname"
        :pageOffset_top="ob.pageOffset_top"
        :pageOffset_left="ob.pageOffset_left"
        :dimensions="dimensions"
        :fill="false"
        :entry="entry"
        :highlight="highlight"
      ></AreaSelect>
      </div>
      <AreaSelect v-for="(old_ob,o_ind) in old_obs"
        :key="o_ind"
        :keyid="o_ind"
        :coordinates="old_ob"
        :name="old_ob.zname"
        :pageOffset_top="old_ob.pageOffset_top"
        :pageOffset_left="old_ob.pageOffset_left"
        :dimensions="dimensions"
        :fill="fill"
        :entry="entry"
        :highlight="highlight"
      >{{this.o_ind}}</AreaSelect>
      <!--div v-for="coordinate in coordinates" :key='coordinate'>
      <select name="2" id="2">
        <option value="af">sdsdg</option>
        <option value="a">fadfa</option>
      </select>
      </div-->
      </div>
    </div>
  </div>
</template>

<script>
import AreaSelect from '@/components/AreaSelect'
import PDF from '@/components/PDF'
import SelectionPreview from '@/components/SelectionPreview'
import randomColor from 'randomcolor'
// import * as JsPDF from 'jspdf'

export default {
  name: 'Annotator',
  components: {
    AreaSelect,
    PDF,
    SelectionPreview
  },
  created () {
    console.log('Annotator created')
    console.log(this.dimensions)
  },
  updated () {
    // var doc = new JsPDF()
    // var elementHandler = {
    //   '#ignorePDF': function (element, renderer) {
    //     return true
    //   }
    // }
    // var source = window.document.getElementsByTagName('span')[0]
    // doc.fromHTML(
    //   source,
    //   15,
    //   15,
    //   {
    //     'width': 180, 'elementHandlers': elementHandler
    //   })
    // doc.output('dataurlnewwindow')
  },
  props: ['src', 'name', 'selections', 'addSelection', 'arrayBuffer', 'setPdfSize', 'dimensions', 'pageoffset', 'obs', 'old_obs', 'fill', 'entry', 'znamech', 'getcan', 'highlight'],
  data () {
    return {
      pdfsize: 'setPdfSize',
      text: '',
      down: false,
      coords: {
        xa: null,
        ya: null,
        xb: null,
        yb: null
      },
      pageNumber: 1,
      pageOffset: {
        top: 0,
        left: 0
      }
    }
  },
  computed: {
    color () {
      return randomColor({format: 'rgb'})
    },
    coordinates () {
      return {
        left: Math.min(this.coords.xa, this.coords.xb),
        top: Math.min(this.coords.ya, this.coords.yb),
        width: Math.abs(this.coords.xa - this.coords.xb),
        height: Math.abs(this.coords.ya - this.coords.yb),
        page: this.pageNumber,
        pageOffset_top: this.pageOffset.top,
        pageOffset_left: this.pageOffset.left
      }
    }
  },
  methods: {
    // znamech (data) {
    //   this.$emit('zname', data)
    // },
    reset: function () {
      this.coords.xa = null
      this.coords.ya = null
      this.coords.xb = null
      this.coords.yb = null
    },
    start: function (event) {
      // event.stopPropagation()
      // event.preventDefault()
      this.down = true

      this.pageNumber = parseInt(event.target.getAttribute('data-page-number') || 1)
      this.pageOffset.top = event.target.offsetTop
      this.pageOffset.left = event.target.offsetLeft
      this.coords.xa = event.offsetX
      this.coords.ya = event.offsetY
      this.coords.xb = event.offsetX
      this.coords.yb = event.offsetY
    },
    end: function (event) {
      event.stopPropagation()
      event.preventDefault()
      this.down = false
      if (this.fill === false) {
        this.addSelection(this.coordinates)
        this.reset()
      }
      // console.log(this.text)
    },
    drag: function (event) {
      event.stopPropagation()
      event.preventDefault()
      if (this.down) {
        this.coords.xb = event.offsetX
        this.coords.yb = event.offsetY
        let text = window.getSelection()
        this.text = text.toString()
      }
    }
  }
}
</script>

<style scoped>
.selection-area {
  position: absolute;
  display: inline-block;
  outline: solid 1px black;
  overflow: hidden;
}

h3 span.filename {
  padding: 0px 15px;
  background: #FFF800;
}

h3 span.filetype {
  text-transform: lowercase;
  font-size: 0.75em;
  background: black;
  color: white;
  border-radius: 10px;
  padding: 2px 12px;
}

.area-select {
overflow: visible;
}

</style>
