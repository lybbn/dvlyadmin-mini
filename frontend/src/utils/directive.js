//自定义指令插件：用法前面加上v-
export default {
  install:(app,options)=>{
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