<template>
  <div class='editor'>
    <div class='sidebar'>
      <h1>PDF - Annotator</h1>
      <Uploader @addfile="addfile" :notify="newFile"></Uploader>
      <ZoneViewer :selections="selections" class='zone-viewer' :batchUpdateSelections="batchUpdateSelections" :originalFilename="name" v-if="src"></ZoneViewer>
      <PDFZoneViewer @updateob="updateobj" :dimensions="pdfDimensions" :selections="selections" class='zone-viewer' :batchUpdateSelections="batchUpdateSelections" :originalFilename="name" v-if="arrayBuffer"></PDFZoneViewer>
      <button @click="poost">
          <center>submit</center>
        </button>
    </div>
    <div class='content'>
      <Annotator :src="src" :setPdfSize="setPdfSize" :arrayBuffer="arrayBuffer" :name="name" :selections="selections" :addSelection="addSelection"></Annotator>
      <!--div v-for="ob in obs" :key='ob'>
      <select name="2" id="2">
        <option value="af">sdsdg</option>
        <option value="a">fadfa</option>
      </select>
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
  methods: {
    addfile (file) {
      this.file = file
    },
    post () {
      if (this.change) {
        this.req1_stat = true
        // console.log(this.name)
        this.$http.post('https://jsonplaceholder.typicode.com/posts', {
          'userId': 1,
          'id': 1,
          'title': 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit',
          'body': 'quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto'
        }).then(function (data) {
          console.log(data)
          console.log([{
            pdf: this.file,
            name: this.name
          }])
          /* for (let i = 0; i < 20; i++) {
            console.log('d')
          } */
          console.log('wait finished')
          // this.obs = data
          this.change = false
          this.req1_stat = false
          this.poost()
        })
      }
    },
    poost () {
      this.post()
      if (!this.req1_stat) {
        this.$http.post('https://jsonplaceholder.typicode.com/posts', {
          'userId': 1,
          'id': 1,
          'title': 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit',
          'body': 'quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto'
        }).then(function (data) {
          console.log(data)
          console.log(this.obs)
          console.log('finished')
          // for (data )
          // this.old_obs = data
          // this.obs = []
          this.selections = []
        })
      }
    },
    updateobj (data) {
      this.obs = data
    },
    batchUpdateSelections: function (selections) {
      this.selections = selections
    },
    setPdfSize: function (width, height) {
      this.pdfDimensions = {
        width: width,
        height: height
      }
    },
    addSelection: function (coords) {
      if (coords.height === 0 || coords.width === 0) {
        return
      }

      this.selections.push({
        id: +new Date(),
        coordinates: {
          top: coords.top,
          left: coords.left,
          height: coords.height,
          width: coords.width,
          page: coords.page,
          pageOffset: coords.pageOffset
        },
        color: randomColor({format: 'rgb'}),
        name: 'Box' + this.selections.length
      })
      // console.log(this.selections)
    },
    newFile: function (data) {
      if (this.name === data) {
        this.change = false
      } else {
        this.change = true
      }
      this.name = data.name
      this.src = data.src
      this.arrayBuffer = data.arrayBuffer
      this.selections = []
      this.obs = []
      this.style = []
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
