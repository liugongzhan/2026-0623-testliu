<template>
  <div class="video-player-wrapper">
    <video
      ref="videoRef"
      class="video-js vjs-big-play-centered"
      :poster="poster"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import videojs from 'video.js'
import 'video.js/dist/video-js.css'

const props = defineProps({
  src: { type: String, default: '' },
  poster: { type: String, default: '' },
  autoplay: { type: [Boolean, String], default: false },
  controls: { type: Boolean, default: true },
  fluid: { type: Boolean, default: true },
  playbackRates: { type: Array, default: () => [0.5, 1, 1.5, 2] },
})

const emit = defineEmits(['ready', 'timeupdate', 'ended', 'play', 'pause'])

const videoRef = ref(null)
let player = null

function initPlayer() {
  if (!videoRef.value) return

  player = videojs(videoRef.value, {
    controls: props.controls,
    autoplay: props.autoplay,
    fluid: props.fluid,
    playbackRates: props.playbackRates,
    sources: props.src ? [{ src: props.src, type: 'video/mp4' }] : [],
  })

  player.ready(() => {
    emit('ready', player)
  })

  player.on('timeupdate', () => {
    emit('timeupdate', player.currentTime(), player.duration())
  })
  player.on('ended', () => emit('ended'))
  player.on('play', () => emit('play'))
  player.on('pause', () => emit('pause'))
}

function disposePlayer() {
  if (player) {
    player.dispose()
    player = null
  }
}

watch(
  () => props.src,
  (newSrc) => {
    if (player && newSrc) {
      player.src({ src: newSrc, type: 'video/mp4' })
    }
  }
)

onMounted(() => {
  initPlayer()
})

onBeforeUnmount(() => {
  disposePlayer()
})

defineExpose({
  getPlayer: () => player,
  currentTime: () => player?.currentTime(),
  duration: () => player?.duration(),
  play: () => player?.play(),
  pause: () => player?.pause(),
  seek: (time) => player?.currentTime(time),
})
</script>

<style scoped>
.video-player-wrapper {
  border-radius: 8px;
  overflow: hidden;
  background: #000;
}
</style>
