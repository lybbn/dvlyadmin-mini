<template>
  <div class="icon-selector">
    <el-input
      v-model="searchText"
      placeholder="搜索图标"
      clearable
      prefix-icon="Search"
      class="search-input"
    />
    <div class="icon-grid">
      <div
        v-for="icon in filteredIcons"
        :key="icon"
        class="icon-item"
        :class="{ active: modelValue === icon }"
        @click="handleSelect(icon)"
      >
        <el-icon :size="20">
          <component :is="icon" />
        </el-icon>
        <span class="icon-name">{{ icon }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: String
})

const emit = defineEmits(['update:modelValue'])

const elementIcons = [
  'Menu',
  'Setting',
  'User',
  'UserFilled',
  'Monitor',
  'Document',
  'Folder',
  'FolderAdd',
  'FolderOpened',
  'Edit',
  'Delete',
  'Plus',
  'Search',
  'Refresh',
  'Upload',
  'Download',
  'Top',
  'Bottom',
  'Back',
  'ArrowRight',
  'Close',
  'Check',
  'Warning',
  'InfoFilled',
  'Bell',
  'Message',
  'Star',
  'StarFilled',
  'House',
  'Location',
  'Position',
  'Histogram',
  'PieChart',
  'DataBoard',
  'DataAnalysis',
  'Collection',
  'CollectionTag',
  'Printer',
  'Calendar',
  'Clock',
  'Connection',
  'Link',
  'Lock',
  'Unlock',
  'Key',
  'Tools',
  'Cpu',
  'Headset',
  'Microphone',
  'Camera',
  'VideoCamera',
  'Notification',
  'ChatDotRound',
  'ChatLineRound',
  'ChatSquare',
  'ChatRound',
  'Postcard',
  'PriceTag',
  'Sell',
  'Present',
  'Box',
  'Goods',
  'ShoppingCart',
  'ShoppingCartFull',
  'Truck',
  'Ship',
  'Discount',
  'Coin',
  'Wallet',
  'Money',
  'BankCard',
  'CreditCard',
  'Opportunity',
  'Flag',
  'Medal',
  'Trophy',
  'FirstAidKit',
  'Reading',
  'ReadingLamp',
  'Notebook',
  'School',
  'OfficeBuilding',
  'SetUp',
  'MagicStick',
  'Mouse',
  'Watch',
  'Magnet',
  'HelpFilled',
  'MoreFilled',
  'ArrowUp',
  'ArrowDown',
  'ArrowLeft',
  'ArrowRight',
  'CaretTop',
  'CaretBottom',
  'CaretLeft',
  'CaretRight',
  'DArrowRight',
  'DArrowLeft',
  'Sort',
  'SortUp',
  'SortDown',
  'Rank',
  'Loading',
  'View',
  'Hide',
  'More',
  'Share',
  'Right',
  'Left',
  'TopRight',
  'TopLeft',
  'BottomRight',
  'BottomLeft',
  'Back',
  'Bottom',
  'Top',
  'Upload',
  'Download',
  'FullScreen',
  'ExitFullScreen',
  'SwitchButton',
  'Aim',
  'Remove',
  'CircleClose',
  'CircleCheck',
  'CirclePlus',
  'Minus',
  'Check',
  'Close',
  'Plus',
  'Select',
  'SemiSelect',
  'ZoomIn',
  'ZoomOut',
  'BellFilled',
  'MuteNotification',
  'Mute',
  'CloseBold',
  'CheckBold',
  'ArrowUpBold',
  'ArrowDownBold',
  'ArrowLeftBold',
  'ArrowRightBold',
  'CaretLeft',
  'CaretRight',
  'CaretTop',
  'CaretBottom',
  'DArrowRight',
  'DArrowLeft',
  'DCaret',
  'Expand',
  'Fold'
]

const searchText = ref('')

const filteredIcons = computed(() => {
  return elementIcons.filter(icon =>
    icon.toLowerCase().includes(searchText.value.toLowerCase())
  )
})

const handleSelect = (icon) => {
  emit('update:modelValue', icon)
}
</script>

<style scoped>
.icon-selector {
  width: 100%;
}

.search-input {
  margin-bottom: 10px;
}

.icon-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
  max-height: 300px;
  overflow-y: auto;
}

.icon-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s;
}

.icon-item:hover {
  background-color: var(--el-color-primary-light-9);
}

.icon-item.active {
  background-color: var(--el-color-primary-light-8);
}

.icon-name {
  margin-top: 5px;
  font-size: 12px;
  text-align: center;
  word-break: break-all;
}
</style>