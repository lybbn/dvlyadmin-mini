import SvgIcon from './SvgIcon.vue'

const registerSvgIcon = (app) => {
  app.component('svg-icon', SvgIcon) // 注册全局组件

  const svgModules = import.meta.glob('/src/assets/lybbn/icons/svg/*.svg', { eager: true })
  Object.values(svgModules)
}

export default registerSvgIcon