/**
 * 自定义拖动指令
 */
export function dragDirective(app) {
	app.directive('drag', {
		mounted(el, binding) {
			let oDiv = el; //当前元素
            let firstTime=''
            let lastTime=''
            //禁止选择网页上的文字
            document.onselectstart = function() {
            	return false;
            };
            oDiv.onmousedown = function(e){
                //鼠标按下，计算当前元素距离可视区的距离
                let disX = e.clientX - oDiv.offsetLeft;
                let disY = e.clientY - oDiv.offsetTop;
                document.onmousemove = function(e){
                    oDiv.setAttribute('drag-flag', true);
                    firstTime = new Date().getTime();
                    //计算移动的距离
                    let l = e.clientX - disX;
                    let t = e.clientY - disY;

                    //移动当前元素

                    if(t > 0 && t < document.body.clientHeight - 50){
                        oDiv.style.top = t + "px";
                    }
                    if(l > 0 && l < document.body.clientWidth - 50){
                        oDiv.style.left = l + "px";
                    }


                }
                document.onmouseup = function(){
                    lastTime = new Date().getTime();
                    if( (lastTime - firstTime)>200 ){
                        oDiv.setAttribute('drag-flag', false);
                    }
                    document.onmousemove = null;
                    document.onmouseup = null;
                };
                //return false不加可能导致黏连，如拖到一个地方时div粘在鼠标上不下来，相当于onmouseup失效
                return false;
            };
		},
	});
}