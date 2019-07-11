<template>
  <div class='editor'>
    <div class='sidebar'>
      <h1>PDF - Annotator</h1>
      <Uploader @addfile="addfile" :notify="newFile"></Uploader>
      <ZoneViewer :selections="selections" class='zone-viewer' :batchUpdateSelections="batchUpdateSelections" :originalFilename="name" v-if="src"></ZoneViewer>
      <PDFZoneViewer @updateob="updateobj" :dimensions="pdfDimensions" :selections="selections" class='zone-viewer' :batchUpdateSelections="batchUpdateSelections" :originalFilename="name" v-if="arrayBuffer"></PDFZoneViewer>
      <div v-if="fill === false">
        <div v-for="(o_i, o_ind) in old_obs" :key="o_ind">
          <div v-if="o_ind ===  o_editid">
            <input type="text" :value="o_i.zname" @keyup.13="o_edit(o_i,$event)">
          </div>
          <div v-else>
            {{ o_i.zname }}
            <div v-if="o_ind === change_an && change_st">
              {{ f_change_an(o_i) }}
            </div>
            <button @click="o_editid = o_ind">edit</button>
            <button @click="o_del(o_ind)">x</button>
            <button @click="change_an = o_ind">change</button>
          </div>
        </div>
        <div v-for="(i, ind) in obs" :key="old_obs.length + ind">
          <input type="text" :value="i.zname" @mouseleave="highlight=null" @mouseover="highlight=i.zname" @keyup.13="edit(i,$event)" :can="true">
          {{ }}
          <button @click="del(ind)">x</button>
        </div>
        <div>
          <button @click="poost">
            <center>submit</center>
          </button> 
        </div>
          <button @click="fill = true">
            <center>fill</center>
          </button> 
      </div>
      <div v-else>
        <button @click="fill = false">
            <center>back</center>
        </button> 
      </div>
    </div>
      <div class='content'>
        <Annotator :highlight="highlight" :getcan="getcan" :znamech="znamech" :entry="entry" :fill="fill" :old_obs="old_obs" :pageoffset="pageoffset" :dimensions="pdfDimensions" :obs="obs" :src="src" :setPdfSize="setPdfSize" :arrayBuffer="arrayBuffer" :name="name" :selections="selections" :addSelection="addSelection"></Annotator>
        <!--div v-for="st in style" :key="st.c">
        <select name="2" id="2" :style="st.s">
          <option value="af">sdsdg</option>
          <option value="a">fadfa</option>
        </select>
        <input type="text" value="box1" :style="{...st.s,position: absolute}">
        </div-->
      </div>
  </div>
</template>

<script>
import Uploader from '@/components/Uploader'
import Annotator from '@/components/Annotator'
import ZoneViewer from '@/components/ZoneViewer'
import PDFZoneViewer from '@/components/PDFZoneViewer'
import randomColor from 'randomcolor'

export default {
  name: 'editor',
  components: {
    Uploader,
    Annotator,
    ZoneViewer,
    PDFZoneViewer
  },
  data () {
    return {
      highlight: null,
      can: false,
      sdel: false,
      sed: false,
      scre: false,
      del_obs: [],
      ed_obs: [],
      zname: '',
      entry: ['mohamed zameel', 'ponnath [h]', 'pathazhakad', 'kodungallur', 'trissur'],
      fill: false,
      change_st: false,
      ch_cordinates: null,
      change_an: null,
      editid: null,
      o_editid: null,
      pageoffset: null,
      c: 0,
      pid: null,
      style: [],
      old_obs: [],
      req1_stat: false,
      change: false,
      file: null,
      obs: [],
      src: null,
      arrayBuffer: null,
      name: '',
      selections: [],
      pdfDimensions: {
        height: 0,
        width: 0
      }
    }
  },
  created () {
    console.log('Editor created')
    console.log(this.pdfDimensions)
  },
  methods: {
    getcan (data) {
      this.can = data
      console.log(data[0].height)
    },
    znamech (data) {
      this.zname = data
    },
    f_change_an (d) {
      // console.log(d)
      // this.ch_cordinates.zname = d.zname
      // this.ch_cordinates['zid'] = d.zid
      // console.log(this.ch_cordinates)
      d.left = this.ch_cordinates.left
      d.top = this.ch_cordinates.top
      d.width = this.ch_cordinates.width
      d.height = this.ch_cordinates.height
      d.pageOffset_left = this.ch_cordinates.pageOffset_left
      d.pageOffset_top = this.ch_cordinates.pageOffset_top
      d.pageno = this.ch_cordinates.pageno
      console.log(d)
      this.sed = true
      let n = this.ed_obs.find(x => x.id === d.id)
      if (!n) {
        this.ed_obs = [...this.ed_obs, d]
      }
      this.change_an = null
      this.ch_cordinates = null
      console.log(d)
      console.log(this.ed_obs)
      this.change_st = false
    },
    del (i) {
      this.obs.splice(i, 1)
      console.log(this.obs)
    },
    o_del (i) {
      let del = this.old_obs.splice(i, 1)
      this.del_obs = [...this.del_obs, del[0].zid]
      this.sdel = true
      console.log(this.del_obs)
    },
    o_edit (d, event) {
      console.log(event.target.value)
      d.zname = event.target.value
      this.sed = true
      let n = this.ed_obs.find(x => x.id === d.id)
      if (!n) {
        // n.cordinates.zname = event.target.value
        this.ed_obs = [...this.ed_obs, d]
      }
      console.log(this.ed_obs)
      this.o_editid = null
    },
    edit (d, event) {
      console.log(event.target.value)
      d.zname = event.target.value
    },
    addfile (file) {
      this.file = file
      console.log(file)
    },
    post () {
      let formData = new FormData()
      formData.append('pfile', this.file)
      if (this.change) {
        let data = new FormData()
        data.append('pfile', this.file)
        // let config = {
        //   header: {
        //     'Content-Type': 'application/pdf'
        //   }
        // }
        this.req1_stat = true
        // console.log(this.name)
        this.$http.post('http://127.0.0.1:8000/post_pdf',
        data,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          // parsedData: JSON.stringify({name: 'vyshnav'})
          }, function (data, status, request) {
            this.postResults = data
            this.ajaxRequest = false
          }).then(function (data) {
            console.log(data)
            // console.log(data.body)
            /* console.log([{
              pdf: this.file,
              name: this.name
            }]) */
            /* for (let i = 0; i < 20; i++) {
              console.log('d')
            } */
            console.log('wait finished')
            // this.obs = data
            this.pid = data.body.pid
            // console.log(data.pid)
            this.change = false
            this.req1_stat = false
            this.poost()
          }).catch(function (data) {
            console.log('From catch')
          })
      }
    },
    poost () {
      this.post()
      if (!this.req1_stat) {
        // let fd = new FormData()
        // fd.append('pid', this.pid)
        // fd.append('zones', this.obs.cordinates)
        // console.log(this.obs.cordinates)
        if (this.scre) {
          this.$http.post('http://127.0.0.1:8000/post_zones', {
            pid: this.pid,
            zones: this.obs
          }, {
            headers: {
              'content-type': 'application/json'
            }
          }).then(function (data) {
            console.log(data)
            // console.log(this.obs)
            console.log('finished')
            // for (data )
            // this.old_obs = data
            // this.obs = []
            console.log([...this.old_obs, ...this.obs])
            this.old_obs = [...this.old_obs, ...data.body]
            console.log(this.old_obs)
            this.obs = []
            this.scre = false
          })
        }
        if (this.sed) {
          this.$http.put('http://127.0.0.1:8000/put_zones', { zones: this.ed_obs }, {
            headers: {
              'content-type': 'application/json'
            }
          }).then(function (data) {
            console.log(data)
            console.log(this.obs)
            console.log('edit finished')
            // for (data )
            // this.old_obs = data
            // this.obs = []
            this.ed_obs = []
            this.sed = false
          })
        }
        if (this.sdel) {
          console.log(this.del_obs)
          this.$http.delete('http://127.0.0.1:8000/delete_zones', {body: { zids: this.del_obs }}).then(function (data) {
            console.log(data)
            console.log(this.obs)
            console.log('delete finished')
            // for (data )
            // this.old_obs = data
            // this.obs = []
            this.del_obs = []
            this.sdel = false
          })
        }
      }
    },
    updateobj (data) {
      this.obs = data
      // console.log(data)
    },
    batchUpdateSelections: function (selections) {
      this.selections = selections
    },
    setPdfSize: function (width, height) {
      this.pdfDimensions = {
        width: width,
        height: height
      }
      console.log(width, height)
    },
    addSelection: function (coords) {
      if (coords.height === 0 || coords.width === 0) {
        return
      }
      // console.log(coords.pageOffset)
      // let y0 = parseInt(this.pdfDimensions.height - coords.top)
      // let y1 = parseInt(this.pdfDimensions.height - coords.top - coords.height)
      if (this.change_an === null) {
        this.selections.push({
          id: +new Date(),
          coordinates: {
            top: coords.top,
            left: coords.left,
            height: coords.height,
            width: coords.width,
            page: coords.page,
            pageOffset_left: coords.pageOffset_left,
            pageOffset_top: coords.pageOffset_top
          },
          color: randomColor({format: 'rgb'}),
          name: 'Box' + this.selections.length
        })
        this.pageoffset = coords.pageOffset
        // console.log(coords.pageOffset)
        this.obs = [...this.obs, {
          zname: this.zname,
          // lx: coords.left,
          // ly: Math.max(y0, y1),
          // rx: coords.left + coords.width,
          // ry: Math.min(y0, y1)
          top: coords.top,
          left: coords.left,
          height: coords.height,
          width: coords.width,
          pageno: coords.page,
          pageOffset_top: coords.pageOffset_left,
          pageOffset_left: coords.pageOffset_top,
          canvas_width: this.can[coords.page - 1].width,
          canvas_height: this.can[coords.page - 1].height
          // color: randomColor({format: 'rgb'})
        }]
        console.log(this.obs)
        this.scre = true
        // console.log(this.obs[0].cordinates)
        this.c++
        this.style.push({
          id: this.c
          // s: {
          //   top: coords.top + coords.pageOffset.top + 'px',
          //   left: coords.left + coords.pageOffset.left + 'px',
          //   height: coords.height + 'px',
          //   width: coords.width + 'px'
          // }
        })
      } else {
        this.ch_cordinates = {
          zname: this.zname,
          // lx: coords.left,
          // ly: Math.max(y0, y1),
          // rx: coords.left + coords.width,
          // ry: Math.min(y0, y1)
          top: coords.top,
          left: coords.left,
          height: coords.height,
          width: coords.width,
          pageno: coords.page,
          pageOffset_left: coords.pageOffset_left,
          pageOffset_top: coords.pageOffset_top
        }
        this.change_st = true
      }
      // console.log(coords.pageOffset)
      // console.log(this.selections)
    },
    newFile: function (data) {
      if (this.name === data.name) {
        this.change = false
      } else {
        this.change = true
      }
      // console.log(typeof data.arrayBuffer)
      this.name = data.name
      this.src = data.src
      this.arrayBuffer = data.arrayBuffer
      // console.log(this.array)
      this.selections = []
      this.obs = []
      this.scre = false
      this.style = []
      this.c = 0
      /* const { convert, extract } = require("extract-pdf-by-coordinates")

      let totalConsumed = 0
      console.log(totalconsumed)
      convert("./resume (6).pdf")
        .then(pages => {
          for (const page of pages) {
            let monthConsumption = extract(
              page,
              { x: 300, y: 520 }, // Start position
              { x: 345, y: 540 } // End position
            )

            // Here we need to remove commas from the extracted value,
            monthConsumption = monthConsumption.split(",").join("")
            // and then convert the string to number.
            monthConsumption = parseFloat(monthConsumption)

            totalConsumed += monthConsumption
          }

          console.log(totalConsumed)
        })
        .catch(err => {
          console.log(err)
        }) */
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

.editor {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  margin-top: 60px;
}

.sidebar {
  position: absolute;
  width: 400px;
  top: 0;
  left: 0;
  padding: 10px;
  align-content: center
}

.content {
  position: absolute;
  width: auto;
  margin-left: 30px;
  top: 0px;
  left: 410px;
}

textarea {
  -webkit-box-sizing: border-box;
   -moz-box-sizing: border-box;
        box-sizing: border-box;
  font-size: 1em;
}

h2 {
  background: #FFF800;
  padding: 10px 25px;
}

h1 {
  background: #C50080;
  padding: 10px 25px;
  color: white;
}

select {
  position: relative;
  z-index: 100;
}
</style>
