import {useUserState} from "@/store/userState.js";
import { useRoute } from 'vue-router'
//自定义指令插件：用法前面加上v-
export default {
    install:(app,options)=>{
        //v-hasBtn 支持 [菜单组件名,按钮编码] 或 菜单组件名:按钮编码 或 元组形式 或 直接 按钮编码
        // 推荐格式3 v-hasBtn="Create" 和 格式2 v-hasBtn="system:Create"  原因简单
        // 解释：菜单组件名相当于route 中的的name，需保持唯一性
        app.directive('hasBtn', {
            mounted(el, binding) {
                // 1. 从binding对象中解构出value（指令的绑定值）
                const { value } = binding
                if (!value) return
                const userState = useUserState();
                if (Array.isArray(value)) {
                    // 格式1: v-hasBtn="['system', 'Create']"
                    const [menuName, buttonCode] = value
                    // 2. 检查：如果有绑定值 且 当前用户没有该权限
                    if (!userState.hasButtonPermission(menuName, buttonCode)) {
                        // 3. 从父节点移除当前元素
                        el.parentNode?.removeChild(el)
                    }
                } else if (typeof value === 'string') {
                    let menuName, buttonCode
                     if (value.includes(':')) {
                        // 格式2: v-hasBtn="system:Create"
                        menuName = value.split(':')[0] // 取前一部分作为组件名
                        buttonCode = value
                    } else {
                        const route = useRoute()
                        // 格式3: v-hasBtn="Create" - 自动使用当前路由route.name作为菜单名
                        menuName = route.name
                        buttonCode = value
                    }
                    
                    if (!userState.hasButtonPermission(menuName, buttonCode)) {
                        // 3. 从父节点移除当前元素
                        el.parentNode?.removeChild(el)
                    }
                    
                }else if (typeof value === 'object' && value.length === 2) {
                    // 格式4: v-hasBtn="('system', 'Create')" (元组/类数组对象)
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

    }

}