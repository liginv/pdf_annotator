<template>
  <div class='preview' >
  {{ text }}
  </div>
</template>

<script>
export default {
  props: ['coordinates', 'znamech'],
  created () {
    console.log('selectionpreviewcreated')
  },
  data () {
    return {
      text: null
    }
  },
  updated () {
    // console.log(this.text)
    if (this.text === null) {
      this.text = ''
    }
    // this.$emit('zname', this.text)
    this.znamech(this.text)
  },
  watch: {
    coordinates () {
      this.highlightOverlaps()
      this.text = this.overlappingText()
      // console.log(this.text)
    }
  },
  methods: {
    hasCoordinates () {
      let coordinates = this.coordinates
      if (!coordinates || !coordinates.top || !coordinates.left || coordinates.height === 0 || coordinates.width === 0) {
        return false
      }
      return true
    },
    overlapping () {
      if (this.hasCoordinates()) {
        let allText = document.querySelectorAll('.page[data-page-number="1"] .textLayer div')
        return Array.prototype.filter.call(allText, this._overlaps)
      } else {
        return []
      }
    },
    overlappingText () {
      // console.log(this.overlapping().textContent)
      let content = this.overlapping().map((element) => element.textContent).join(' ')
      // console.log(content)
      return content
    },
    highlightOverlaps () {
      this.unhighlight()
      this.overlapping().forEach(this._highlight)
    },
    _highlight (element) {
      if (element.className.indexOf('selected-preview') === -1) {
        element.className += ' selected-preview'
      }
    },
    unhighlight (element) {
      var highlighted = document.querySelectorAll('.selected-preview')
      for (let h of highlighted) {
        h
        h.className = h.className.replace('selected-preview', '')
      }
    },
    _overlaps (element) {
      let coordinates = this.coordinates
      if (element.offsetLeft > (coordinates.left + coordinates.width) || (element.offsetLeft + element.offsetWidth) < coordinates.left) {
        return false
      }
      if (element.offsetTop > (coordinates.top + coordinates.height) || coordinates.top > (element.offsetTop + element.offsetHeight)) {
        return false
      }
      return true
    },
    _sorted (a, b) {
      if (a.offsetTop === b.offsetTop) {
        return (a.offsetLeft < b.offsetTop) ? -1 : 1
      }
      return (a.offsetTop < b.offsetTop) ? -1 : 1
    }
  }
}
</script>

<style>
.preview {
  display: none;
/*  position: absolute;
  pointer-events: none;
  opacity: 0.5;
  padding: 10px;
  max-width: 300px;
  z-index: 4000;
  background: white;*/
}

.selected-preview {
  background: red;
}
</style>
