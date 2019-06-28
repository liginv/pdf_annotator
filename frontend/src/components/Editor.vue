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
      c: 0,
      change: false,
      file: null,
      ob: [],
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
        console.log(this.name)
        this.change = false
      }
    },
    poost () {
      this.post()
      console.log([{
        pdf: this.file,
        name: this.name,
        details: this.ob
      }])
      this.$http.post('https://jsonplaceholder.typicode.com/posts/', {
        'userId': 1,
        'id': 1,
        'title': 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit',
        'body': 'quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto'
      }).then(function (data) {
        console.log(data)
      })
    },
    updateobj (data) {
      this.ob = data
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
      this.ob = []
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
</style>
