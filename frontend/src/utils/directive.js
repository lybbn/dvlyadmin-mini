import {useUserState} from "@/store/userState.js";

//自定义指令插件：用法前面加上v-
export default {
    install:(app,options)=>{
        //v-auth 支持 [菜单组件名,按钮编码] 或 菜单组件名:按钮编码 或 元组形式 或 直接 按钮编码
        // 推荐格式3 v-auth="Create" 和 格式2 v-auth="system:Create"  原因简单
        // 解释：菜单组件名相当于route 中的的name，需保持唯一性
        app.directive('auth', {
            mounted(el, binding) {
                // 1. 从binding对象中解构出value（指令的绑定值）
                const { value } = binding
                if (!value) return
                const userState = useUserState();
                if (Array.isArray(value)) {
                    // 格式1: v-auth="['system', 'Create']"
                    const [menuName, buttonCode] = value
                    // 2. 检查：如果有绑定值 且 当前用户没有该权限
                    if (!userState.hasButtonPermission(menuName, buttonCode)) {
                        // 3. 从父节点移除当前元素
                        el.parentNode?.removeChild(el)
                    }
                } else if (typeof value === 'string') {
                    let menuName, buttonCode
                    if (value.includes(':')) {
                        // 格式2: v-auth="system:Create"
                        const parts = value.split(':');
                         // 确保分割后有且只有两部分
                        if (parts.length !== 2) {
                            return
                        }
                        menuName = parts[0] // 取前一部分作为组件名
                        buttonCode = parts[1]
                    } else {
                        // 格式3: v-auth="Create" - 自动使用当前路由route.name作为菜单名
                        menuName = app.config.globalProperties.$router?.currentRoute.value.name || "";
                        buttonCode = value
                    }
                    if (!userState.hasButtonPermission(menuName, buttonCode)) {
                        // 3. 从父节点移除当前元素
                        el.parentNode?.removeChild(el)
                    }
                    
                }else if (typeof value === 'object' && value.length === 2) {
                    // 格式4: v-auth="('system', 'Create')" (元组/类数组对象)
                    menuName = value[0]
                    buttonCode = value[1]
                    if (!userState.hasButtonPermission(menuName, buttonCode)) {
                        // 3. 从父节点移除当前元素
                        el.parentNode?.removeChild(el)
                    }
                }else {
                    console.error(`无效的权限指令格式: ${value}`)
                    return
                }
            
            }
        })
        //只能输入正数(包含小数)和0
        app.directive('limitPositiveNumber', {
            mounted(el, binding) {
                el.oninput=(e)=>{
                    let value=e.target.value;
                    //先把非数字的都替换掉，除了数字和.
                    value = value.replace(/[^\d\.]/g, '');
                    //保证只有出现一个.而没有多个
                    value = value.replace(/\.{2,}/g, '.');
                    //保证.只出现一次，而不能出现两次以上
                    value = value.replace('.', '$#$').replace(/\./g, '').replace('$#$', '.');
                    //必须保证第一个为数字而不是.
                    value = value.replace(/^\./g, '');
                    e.target.value=value;
                    //手动触发input事件使v-model绑定的值更新
                    e.target.dispatchEvent(new Event("input"));
                }
            }
        })
        //只能输入正整数和0
        app.directive('limitPositiveInt', {
            mounted(el, binding) {
                el.oninput=(e)=>{
                    let value=e.target.value;
                    value = value.replace(/\D/g, '');
                    e.target.value=value;
                    //手动触发input事件使v-model绑定的值更新
                    e.target.dispatchEvent(new Event("input"));
                }
            }
        })
        //只能输入正整数和不含0
        app.directive('limitPositiveIntNo0', {
            mounted(el, binding) {
                el.oninput=(e)=>{
                    let value=e.target.value;
                    value = value.replace(/\D/g, '');
            // 只保留大于0的正整数
            value = value.replace(/^0+/, ''); // 移除开头的零
            if (value === '' || parseInt(value) === 0) {
                value = ''; // 如果结果为空或是0，则置为空
            }
                    e.target.value=value;
                    //手动触发input事件使v-model绑定的值更新
                    e.target.dispatchEvent(new Event("input"));
                }
            }
        })
        //只能输入正数(最多两位小数)和0
        app.directive('limitPositiveNumberFixed2', {
            mounted(el, binding) {
                el.oninput=(e)=>{
                    let value=e.target.value;
                    var t = value.charAt(0);
                    //先把非数字的都替换掉，除了数字和.
                    value = value.replace(/[^\d\.]/g, '');
                    //保证只有出现一个.而没有多个
                    value = value.replace(/\.{2,}/g, '.');
                    //保证.只出现一次，而不能出现两次以上
                    value = value.replace('.', '$#$').replace(/\./g, '').replace('$#$', '.');
                    //必须保证第一个为数字而不是.
                    value = value.replace(/^\./g, '');
                    value = value.replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3');
                    e.target.value=value;
                    //手动触发input事件使v-model绑定的值更新
                    e.target.dispatchEvent(new Event("input"));
                }
            }
        })

        app.directive('drag', {
            mounted(el, binding) {
                el.style.cursor = 'move';
                el.style.userSelect = 'none'; // 防止拖动时选中文本
                el.style.touchAction = 'none'; // 禁用浏览器默认触摸行为
                
                let startX = 0, startY = 0;
                let initialLeft = 0, initialTop = 0;
                let isDragging = false;
                let clickStartTime = 0;
                let moved = false;

                // 边界限制配置
                const boundary = binding.value?.boundary ?? true;
                const withinParent = binding.value?.withinParent ?? false;

                el.__dragHandlers__ = {
                    startDrag: function(e) {
                        // 记录点击开始时间
                        clickStartTime = Date.now();
                        moved = false;
                        
                        // 获取初始位置
                        const clientX = e.clientX ?? e.touches[0].clientX;
                        const clientY = e.clientY ?? e.touches[0].clientY;
                        startX = clientX;
                        startY = clientY;
                        
                        // 获取当前元素位置
                        const rect = el.getBoundingClientRect();
                        initialLeft = rect.left;
                        initialTop = rect.top;
                        
                        // 添加样式
                        el.style.transition = 'none'; // 拖动时禁用过渡效果
                        document.addEventListener('mousemove', el.__dragHandlers__.onDrag);
                        document.addEventListener('touchmove', el.__dragHandlers__.onDrag, { passive: false });
                        document.addEventListener('mouseup', el.__dragHandlers__.endDrag);
                        document.addEventListener('touchend', el.__dragHandlers__.endDrag);
                    },

                    onDrag: function(e) {
                        // 标记已经开始移动
                        moved = true;
                        
                        e.preventDefault();
                        
                        const clientX = e.clientX ?? e.touches[0].clientX;
                        const clientY = e.clientY ?? e.touches[0].clientY;
                        
                        // 计算移动距离
                        const dx = clientX - startX;
                        const dy = clientY - startY;
                        
                        // 只有移动超过阈值才认为是拖拽
                        if (Math.abs(dx) > 5 || Math.abs(dy) > 5) {
                            isDragging = true;
                            el.style.cursor = 'grabbing';
                        }
                        
                        // 应用新位置
                        let newLeft = initialLeft + dx;
                        let newTop = initialTop + dy;
                        
                        // 边界检查
                        if ((boundary || withinParent) && isDragging) {
                            const boundaryRect = withinParent 
                            ? el.parentElement.getBoundingClientRect()
                            : {
                                left: 0,
                                top: 0,
                                right: window.innerWidth,
                                bottom: window.innerHeight,
                                width: window.innerWidth,
                                height: window.innerHeight
                                };
                            
                            newLeft = Math.max(0, Math.min(newLeft, boundaryRect.width - el.offsetWidth));
                            newTop = Math.max(0, Math.min(newTop, boundaryRect.height - el.offsetHeight));
                            
                            if (withinParent) {
                            newLeft = Math.max(boundaryRect.left, Math.min(newLeft, boundaryRect.right - el.offsetWidth));
                            newTop = Math.max(boundaryRect.top, Math.min(newTop, boundaryRect.bottom - el.offsetHeight));
                            }
                        }
                        
                        if (isDragging) {
                            el.style.left = `${newLeft}px`;
                            el.style.top = `${newTop}px`;
                        }
                    },

                    endDrag: function(e) {
                        // 判断是否为点击事件
                        const clickDuration = Date.now() - clickStartTime;
                        const isClick = !moved && clickDuration < 20;
                        
                        if (isClick) {
                            // 如果是点击，触发原始点击事件
                            const clickEvent = new MouseEvent('click', {
                                bubbles: true,
                                cancelable: true,
                                view: window
                            });
                            el.dispatchEvent(clickEvent);
                        }
                        
                        isDragging = false;
                        el.style.cursor = 'move';
                        
                        // 恢复过渡效果
                        el.style.transition = 'all 0.3s ease';
                        
                        // 移除事件监听
                        document.removeEventListener('mousemove', el.__dragHandlers__.onDrag);
                        document.removeEventListener('touchmove', el.__dragHandlers__.onDrag);
                        document.removeEventListener('mouseup', el.__dragHandlers__.endDrag);
                        document.removeEventListener('touchend', el.__dragHandlers__.endDrag);
                    }
                };

                // 添加事件监听
                el.addEventListener('mousedown', el.__dragHandlers__.startDrag);
                el.addEventListener('touchstart', el.__dragHandlers__.startDrag, { passive: false });
                
                // 确保元素有定位样式
                if (!['fixed', 'absolute', 'relative'].includes(getComputedStyle(el).position)) {
                    el.style.position = 'fixed';
                }
            },
            
            unmounted(el) {
                // 清理事件监听
                if (el.__dragHandlers__) {
                    el.removeEventListener('mousedown', el.__dragHandlers__.startDrag);
                    el.removeEventListener('touchstart', el.__dragHandlers__.startDrag);
                    document.removeEventListener('mousemove', el.__dragHandlers__.onDrag);
                    document.removeEventListener('touchmove', el.__dragHandlers__.onDrag);
                    document.removeEventListener('mouseup', el.__dragHandlers__.endDrag);
                    document.removeEventListener('touchend', el.__dragHandlers__.endDrag);
                    delete el.__dragHandlers__;
                }
            }
        })
        
    }

}