<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'

export interface PhotoItem {
  src: string
  alt: string
  title?: string
  caption?: string
}

const props = defineProps<{
  photos?: PhotoItem[]
  autoplay?: boolean
  interval?: number
  title?: string
}>()

const defaultPhotos: PhotoItem[] = [
  {
    src: '/images/photo-1.jpg',
    alt: 'Shaded wooded trail with pine trees and green ground cover',
    title: 'Wooded Trail System',
    caption: 'Quiet walking paths winding through the forest behind the pool'
  },
  {
    src: '/images/photo-2.jpg',
    alt: 'Newly built wooden footbridge over a small creek in the woods',
    title: 'New Creek Footbridge',
    caption: 'Recently constructed wooden bridge providing safe crossing across the stream'
  },
  {
    src: '/images/photo-3.jpg',
    alt: 'Dirt path leading through trees toward an open grassy field',
    title: 'Path to the Open Field',
    caption: 'Scenic trail connecting the woodland areas to the future multi-use field'
  },
  {
    src: '/images/photo-4.jpg',
    alt: 'Two volunteers working to clean out creek bed drainage',
    title: 'Community Volunteer Work',
    caption: 'Neighbors getting hands-on to clear brush and repair trail drainage'
  },
  {
    src: '/images/photo-5.jpg',
    alt: 'Wooded trail marked with pink flags winding through ivy-covered trees',
    title: 'Trail Marking & Ivy Clearing',
    caption: 'Trail blazes marking newly cleared paths through mature hardwoods'
  },
  {
    src: '/images/photo-6.jpg',
    alt: 'Rocky creek bed with historic stone culvert and dog exploring',
    title: 'Historic Stone Culvert & Creek',
    caption: 'Natural stream corridor running past the historic stone culvert'
  },
  {
    src: '/images/photo-7.jpg',
    alt: 'Wooded dirt trail leading toward neighborhood homes with dog walking',
    title: 'Dog-Friendly Walking Trails',
    caption: 'Shaded dirt trails connecting Woodmont neighborhoods and green space'
  },
  {
    src: '/images/photo-8.jpg',
    alt: 'Sunlit grassy field surrounded by dense green forest with dog',
    title: 'Sunlit Community Meadow',
    caption: 'Open field area planned for community gatherings and sports'
  }
]

const items = computed(() => (props.photos && props.photos.length > 0) ? props.photos : defaultPhotos)

const currentIndex = ref(0)
const isPlaying = ref(props.autoplay !== false)
const isFullscreen = ref(false)
let timer: ReturnType<typeof setInterval> | null = null

const currentPhoto = computed(() => items.value[currentIndex.value])

const nextSlide = () => {
  currentIndex.value = (currentIndex.value + 1) % items.value.length
}

const prevSlide = () => {
  currentIndex.value = (currentIndex.value - 1 + items.value.length) % items.value.length
}

const goToSlide = (index: number) => {
  currentIndex.value = index
}

const togglePlay = () => {
  isPlaying.value = !isPlaying.value
  if (isPlaying.value) {
    startTimer()
  } else {
    stopTimer()
  }
}

const startTimer = () => {
  stopTimer()
  if (isPlaying.value && items.value.length > 1) {
    timer = setInterval(() => {
      nextSlide()
    }, props.interval || 5000)
  }
}

const stopTimer = () => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}

const handleMouseEnter = () => {
  stopTimer()
}

const handleMouseLeave = () => {
  if (isPlaying.value) {
    startTimer()
  }
}

// Touch swipe support
const touchStartX = ref(0)
const touchEndX = ref(0)

const handleTouchStart = (e: TouchEvent) => {
  touchStartX.value = e.changedTouches[0].screenX
  stopTimer()
}

const handleTouchEnd = (e: TouchEvent) => {
  touchEndX.value = e.changedTouches[0].screenX
  handleSwipe()
  if (isPlaying.value) {
    startTimer()
  }
}

const handleSwipe = () => {
  const diff = touchStartX.value - touchEndX.value
  if (Math.abs(diff) > 40) {
    if (diff > 0) {
      nextSlide()
    } else {
      prevSlide()
    }
  }
}

// Lightbox full screen modal
const openFullscreen = () => {
  isFullscreen.value = true
  stopTimer()
}

const closeFullscreen = () => {
  isFullscreen.value = false
  if (isPlaying.value) {
    startTimer()
  }
}

const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'ArrowRight') {
    nextSlide()
  } else if (e.key === 'ArrowLeft') {
    prevSlide()
  } else if (e.key === 'Escape' && isFullscreen.value) {
    closeFullscreen()
  }
}

onMounted(() => {
  startTimer()
  window.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  stopTimer()
  window.removeEventListener('keydown', handleKeyDown)
})
</script>

<template>
  <div class="slideshow-wrapper">
    <h3 v-if="title" class="slideshow-heading">{{ title }}</h3>
    
    <div 
      class="slideshow-container"
      @mouseenter="handleMouseEnter"
      @mouseleave="handleMouseLeave"
      @touchstart="handleTouchStart"
      @touchend="handleTouchEnd"
      role="region"
      aria-label="Park photos slideshow"
    >
      <!-- Slides -->
      <div class="slides-frame" @click="openFullscreen">
        <transition-group name="fade">
          <div 
            v-for="(photo, index) in items" 
            :key="photo.src"
            v-show="index === currentIndex"
            class="slide-item"
          >
            <img 
              :src="photo.src" 
              :alt="photo.alt" 
              class="slide-image"
              loading="lazy"
            />
            
            <div class="slide-overlay">
              <div class="caption-content">
                <span class="slide-badge">{{ index + 1 }} / {{ items.length }}</span>
                <h4 v-if="photo.title" class="slide-title">{{ photo.title }}</h4>
                <p v-if="photo.caption" class="slide-caption">{{ photo.caption }}</p>
              </div>
            </div>
          </div>
        </transition-group>

        <!-- Click to expand hint -->
        <div class="zoom-hint" title="Click for fullscreen view">
          <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none">
            <path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/>
          </svg>
        </div>
      </div>

      <!-- Arrow Controls -->
      <button 
        class="nav-btn prev-btn" 
        @click.stop="prevSlide" 
        aria-label="Previous photo"
      >
        <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2.5" fill="none">
          <path d="M15 18l-6-6 6-6"/>
        </svg>
      </button>

      <button 
        class="nav-btn next-btn" 
        @click.stop="nextSlide" 
        aria-label="Next photo"
      >
        <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2.5" fill="none">
          <path d="M9 18l6-6-6-6"/>
        </svg>
      </button>

      <!-- Bottom Toolbar (Dots & Play/Pause) -->
      <div class="toolbar">
        <div class="dots-list">
          <button 
            v-for="(_, index) in items" 
            :key="index"
            class="dot-btn"
            :class="{ active: index === currentIndex }"
            @click.stop="goToSlide(index)"
            :aria-label="`Go to photo ${index + 1}`"
          />
        </div>

        <button 
          class="play-toggle-btn" 
          @click.stop="togglePlay"
          :aria-label="isPlaying ? 'Pause slideshow' : 'Play slideshow'"
          :title="isPlaying ? 'Pause slideshow' : 'Play slideshow'"
        >
          <svg v-if="isPlaying" viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
            <rect x="6" y="4" width="4" height="16" rx="1"/>
            <rect x="14" y="4" width="4" height="16" rx="1"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
            <polygon points="5 3 19 12 5 21 5 3"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Lightbox Modal -->
    <ClientOnly>
      <Teleport to="body">
        <transition name="lightbox-fade">
          <div 
            v-if="isFullscreen" 
            class="lightbox-backdrop"
            @click.self="closeFullscreen"
            role="dialog"
            aria-modal="true"
          >
            <button 
              class="lightbox-close" 
              @click="closeFullscreen" 
              aria-label="Close fullscreen view"
            >
              &times;
            </button>

            <button 
              class="lightbox-nav lightbox-prev" 
              @click="prevSlide" 
              aria-label="Previous photo"
            >
              ‹
            </button>

            <div class="lightbox-content">
              <img 
                :src="currentPhoto.src" 
                :alt="currentPhoto.alt" 
                class="lightbox-img"
              />
              <div class="lightbox-caption">
                <h4>{{ currentPhoto.title }}</h4>
                <p>{{ currentPhoto.caption }}</p>
              </div>
            </div>

            <button 
              class="lightbox-nav lightbox-next" 
              @click="nextSlide" 
              aria-label="Next photo"
            >
              ›
            </button>
          </div>
        </transition>
      </Teleport>
    </ClientOnly>
  </div>
</template>

<style scoped>
.slideshow-wrapper {
  margin: 2rem 0;
  width: 100%;
}

.slideshow-heading {
  margin: 0 0 1rem;
  font-size: 1.5rem;
  color: var(--hemlock);
}

.slideshow-container {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  background: var(--hemlock-deep);
  box-shadow: 0 10px 30px rgba(31, 58, 46, 0.15);
  user-select: none;
}

.slides-frame {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 10;
  cursor: pointer;
  overflow: hidden;
}

@media (max-width: 640px) {
  .slides-frame {
    aspect-ratio: 4 / 3;
  }
}

.slide-item {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.slide-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.slide-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 2.5rem 1.5rem 1.25rem;
  background: linear-gradient(to top, rgba(22, 43, 34, 0.92) 0%, rgba(22, 43, 34, 0.6) 65%, transparent 100%);
  color: var(--on-dark);
  transition: opacity 0.3s ease;
}

.caption-content {
  max-width: 42rem;
}

.slide-badge {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  padding: 0.2rem 0.55rem;
  border-radius: 4px;
  background: var(--blaze);
  color: var(--hemlock-deep);
  margin-bottom: 0.4rem;
}

.slide-title {
  margin: 0 0 0.25rem;
  font-family: var(--font-display);
  font-size: clamp(1.2rem, 2.8vw, 1.6rem);
  font-weight: 600;
  color: var(--on-dark);
  line-height: 1.2;
}

.slide-caption {
  margin: 0;
  font-size: clamp(0.9rem, 2vw, 1rem);
  color: var(--on-dark-soft);
  line-height: 1.4;
}

.zoom-hint {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(31, 58, 46, 0.7);
  backdrop-filter: blur(4px);
  color: var(--on-dark);
  padding: 0.45rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.85;
  transition: opacity 0.2s, transform 0.2s;
  z-index: 2;
}

.slides-frame:hover .zoom-hint {
  opacity: 1;
  transform: scale(1.08);
}

/* Nav Buttons */
.nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(31, 58, 46, 0.75);
  backdrop-filter: blur(4px);
  color: var(--on-dark);
  border: 1px solid rgba(255, 255, 255, 0.2);
  width: 2.75rem;
  height: 2.75rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.2s, border-color 0.2s;
  z-index: 3;
}

.nav-btn:hover {
  background: var(--hemlock);
  border-color: var(--blaze);
  color: var(--blaze);
  transform: translateY(-50%) scale(1.08);
}

.prev-btn {
  left: 1rem;
}

.next-btn {
  right: 1rem;
}

/* Bottom Toolbar */
.toolbar {
  position: absolute;
  bottom: 0.75rem;
  right: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  z-index: 3;
  background: rgba(22, 43, 34, 0.75);
  backdrop-filter: blur(6px);
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.dots-list {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.dot-btn {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  border: none;
  padding: 0;
  cursor: pointer;
  transition: background-color 0.25s, transform 0.25s;
}

.dot-btn:hover {
  background: rgba(255, 255, 255, 0.8);
}

.dot-btn.active {
  background: var(--blaze);
  transform: scale(1.35);
}

.play-toggle-btn {
  background: transparent;
  border: none;
  color: var(--on-dark);
  cursor: pointer;
  padding: 0.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.play-toggle-btn:hover {
  color: var(--blaze);
}

/* Fade Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.6s ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Lightbox Modal */
.lightbox-backdrop {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(14, 27, 21, 0.94);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.lightbox-content {
  max-width: 90vw;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.lightbox-img {
  max-width: 100%;
  max-height: 75vh;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
}

.lightbox-caption {
  margin-top: 1rem;
  text-align: center;
  color: var(--on-dark);
}

.lightbox-caption h4 {
  margin: 0 0 0.25rem;
  color: var(--blaze);
  font-family: var(--font-display);
  font-size: 1.4rem;
}

.lightbox-caption p {
  margin: 0;
  font-size: 1rem;
  color: var(--on-dark-soft);
}

.lightbox-close {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  background: transparent;
  border: none;
  color: var(--on-dark);
  font-size: 2.5rem;
  line-height: 1;
  cursor: pointer;
  transition: color 0.2s;
}

.lightbox-close:hover {
  color: var(--blaze);
}

.lightbox-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--on-dark);
  font-size: 3rem;
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
}

.lightbox-nav:hover {
  background: var(--blaze);
  color: var(--hemlock-deep);
}

.lightbox-prev {
  left: 2rem;
}

.lightbox-next {
  right: 2rem;
}

.lightbox-fade-enter-active,
.lightbox-fade-leave-active {
  transition: opacity 0.3s ease;
}

.lightbox-fade-enter-from,
.lightbox-fade-leave-to {
  opacity: 0;
}
</style>
