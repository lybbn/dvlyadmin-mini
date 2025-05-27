const svgModules = import.meta.glob('/src/assets/lybbn/icons/svg/*.svg', { eager: true })

function getIconList() {
    let iconList = []
    for (const path in svgModules) {
        const fileName = path.split('/').pop()?.split('.')[0] // 根据路径截取name文件名（去除后缀和前面目录）
        if (fileName) {
            iconList.push("lyicon-" + fileName)
        }
    }
    return iconList
}

export {
    getIconList
}