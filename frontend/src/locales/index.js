import { createI18n } from 'vue-i18n'
import el_zh_cn from 'element-plus/dist/locale/zh-cn.mjs'
import el_en from 'element-plus/dist/locale/en.mjs'
import zh_cn from './lang/zh_cn.js'
import en from './lang/en.js'

const messages = {
  'zh-cn': {
		el: el_zh_cn,
		...zh_cn
	},
	'en': {
		el: el_en,
		...en
	}
}

const i18n = createI18n({
  legacy: false,
  locale: localStorage.getItem('language') || 'zh-cn',
  fallbackLocale: 'zh-cn',
  globalInjection: true,
  messages
})

export const {t} = i18n.global
export default i18n