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

// Smart image buffer: only load active, next, and previous photos in memory to maximize mobile GPU performance
const isPhotoLoaded = (index: number) => {
  const total = items.value.length
  if (total <= 3) return true
  const prev = (currentIndex.value - 1 + total) % total
  const next = (currentIndex.value + 1) % total
  return index === currentIndex.value || index === prev || index === next
}

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

// Mobile touch swipe handling with vertical scroll protection
const touchStartX = ref(0)
const touchStartY = ref(0)

const handleTouchStart = (e: TouchEvent) => {
  if (!e.changedTouches || e.changedTouches.length === 0) return
  touchStartX.value = e.changedTouches[0].clientX
  touchStartY.value = e.changedTouches[0].clientY
  stopTimer()
}

const handleTouchEnd = (e: TouchEvent) => {
  if (!e.changedTouches || e.changedTouches.length === 0) return
  const touchEndX = e.changedTouches[0].clientX
  const touchEndY = e.changedTouches[0].clientY
  
  const diffX = touchStartX.value - touchEndX
  const diffY = touchStartY.value - touchEndY

  // Only trigger horizontal swipe if horizontal movement > vertical movement (protect vertical scrolling on mobile)
  if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 35) {
    if (diffX > 0) {
      nextSlide()
    } else {
      prevSlide()
    }
  }

  if (isPlaying.value) {
    startTimer()
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
      @touchstart.passive="handleTouchStart"
      @touchend.passive="handleTouchEnd"
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
              v-if="isPhotoLoaded(index)"
              :src="photo.src" 
              :alt="photo.alt" 
              class="slide-image"
              decoding="async"
              :loading="index === currentIndex ? 'eager' : 'lazy'"
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
          <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none">
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
        <svg viewBox="0 0 24 24" width="22" height="22" stroke="currentColor" stroke-width="2.5" fill="none">
          <path d="M15 18l-6-6 6-6"/>
        </svg>
      </button>

      <button 
        class="nav-btn next-btn" 
        @click.stop="nextSlide" 
        aria-label="Next photo"
      >
        <svg viewBox="0 0 24 24" width="22" height="22" stroke="currentColor" stroke-width="2.5" fill="none">
          <path d="M9 18l6-6-6-6"/>
        </svg>
      </button>

      <!-- Bottom Toolbar (Dots & Play/Pause) -->
      <div class="toolbar">
        <div class="dots-list">
          <button 
            v-for="(_, index) in items" 
            :key="index"
            class="dot-btn-wrapper"
            @click.stop="goToSlide(index)"
            :aria-label="`Go to photo ${index + 1}`"
          >
            <span class="dot-btn" :class="{ active: index === currentIndex }" />
          </button>
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
                decoding="async"
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
  margin: 1.5rem 0;
  width: 100%;
}

.slideshow-heading {
  margin: 0 0 1rem;
  font-size: 1.4rem;
  color: var(--hemlock);
}

.slideshow-container {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  background: var(--hemlock-deep);
  box-shadow: 0 8px 24px rgba(31, 58, 46, 0.16);
  user-select: none;
  touch-action: pan-y;
  will-change: transform;
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
  will-change: opacity;
  transform: translateZ(0);
  backface-visibility: hidden;
}

.slide-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transform: translateZ(0);
}

.slide-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 2.2rem 1.25rem 1rem;
  background: linear-gradient(to top, rgba(16, 32, 25, 0.95) 0%, rgba(16, 32, 25, 0.65) 65%, transparent 100%);
  color: var(--on-dark);
  will-change: opacity;
}

.caption-content {
  max-width: 42rem;
}

.slide-badge {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  background: var(--blaze);
  color: var(--hemlock-deep);
  margin-bottom: 0.35rem;
}

.slide-title {
  margin: 0 0 0.2rem;
  font-family: var(--font-display);
  font-size: clamp(1.1rem, 2.5vw, 1.5rem);
  font-weight: 600;
  color: var(--on-dark);
  line-height: 1.2;
}

.slide-caption {
  margin: 0;
  font-size: clamp(0.85rem, 1.8vw, 0.95rem);
  color: var(--on-dark-soft);
  line-height: 1.35;
}

.zoom-hint {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  background: rgba(22, 43, 34, 0.82);
  color: var(--on-dark);
  padding: 0.4rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.9;
  transition: opacity 0.2s, transform 0.2s;
  z-index: 2;
}

@media (hover: hover) {
  .slides-frame:hover .zoom-hint {
    opacity: 1;
    transform: scale(1.08);
  }
}

/* Nav Buttons optimized for mobile touch */
.nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(22, 43, 34, 0.82);
  color: var(--on-dark);
  border: 1px solid rgba(255, 255, 255, 0.2);
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.15s, color 0.15s;
  z-index: 3;
  touch-action: manipulation;
}

@media (hover: hover) {
  .nav-btn:hover {
    background: var(--hemlock);
    border-color: var(--blaze);
    color: var(--blaze);
  }
}

.prev-btn {
  left: 0.6rem;
}

.next-btn {
  right: 0.6rem;
}

/* Bottom Toolbar */
.toolbar {
  position: absolute;
  bottom: 0.6rem;
  right: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  z-index: 3;
  background: rgba(16, 32, 25, 0.88);
  padding: 0.3rem 0.65rem;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.18);
}

.dots-list {
  display: flex;
  align-items: center;
  gap: 0.15rem;
}

/* Large ~32px touch target area for mobile tap, compact 7px visual dot */
.dot-btn-wrapper {
  background: transparent;
  border: none;
  padding: 0.75rem 0.35rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  touch-action: manipulation;
}

.dot-btn {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.45);
  display: block;
  transition: background-color 0.2s, transform 0.2s;
}

.dot-btn.active {
  background: var(--blaze);
  transform: scale(1.4);
}

.play-toggle-btn {
  background: transparent;
  border: none;
  color: var(--on-dark);
  cursor: pointer;
  padding: 0.2rem;
  min-width: 2rem;
  min-height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.15s;
  touch-action: manipulation;
}

.play-toggle-btn:hover {
  color: var(--blaze);
}

/* Hardware Accelerated Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease-in-out;
  will-change: opacity;
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
  background: rgba(10, 20, 16, 0.96);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.lightbox-content {
  max-width: 92vw;
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
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
}

.lightbox-caption {
  margin-top: 0.85rem;
  text-align: center;
  color: var(--on-dark);
}

.lightbox-caption h4 {
  margin: 0 0 0.2rem;
  color: var(--blaze);
  font-family: var(--font-display);
  font-size: 1.3rem;
}

.lightbox-caption p {
  margin: 0;
  font-size: 0.95rem;
  color: var(--on-dark-soft);
}

.lightbox-close {
  position: absolute;
  top: 1rem;
  right: 1.25rem;
  background: transparent;
  border: none;
  color: var(--on-dark);
  font-size: 2.5rem;
  line-height: 1;
  cursor: pointer;
  transition: color 0.15s;
  touch-action: manipulation;
}

.lightbox-close:hover {
  color: var(--blaze);
}

.lightbox-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--on-dark);
  font-size: 2.5rem;
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.15s, color 0.15s;
  touch-action: manipulation;
}

.lightbox-nav:hover {
  background: var(--blaze);
  color: var(--hemlock-deep);
}

.lightbox-prev {
  left: 1rem;
}

.lightbox-next {
  right: 1rem;
}

.lightbox-fade-enter-active,
.lightbox-fade-leave-active {
  transition: opacity 0.25s ease;
}

.lightbox-fade-enter-from,
.lightbox-fade-leave-to {
  opacity: 0;
}
</style>
