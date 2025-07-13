import { defineStore } from 'pinia';
import WebSocket from '@/utils/websocket';
import { ElNotification } from 'element-plus'

export const useLywebsocket = defineStore('lywebsocket', {
	state:() => {
        return {
            isWebSocketOpen: false,
			msgInfo:{
				msgNumber:0,//未读消息数
			},
        }
    },
	getters:{

    },
	actions: {
		setWebSocketState(socketState) {
			this.isWebSocketOpen = socketState
		},
		isWebsocket(){
			return WebSocket.websocket
		},
		wsReceive(message){
			const data = JSON.parse(message.data);
			const { unread } = data;
			this.setUnread(unread);
			if (data.msg_type === 'SYS') {
				ElNotification({
					title: '系统消息',
					message: data.content,
					type: 'success',
					position: 'bottom-right',
					duration: 5000,
				});
			}
		},
		async initWebSocket() {
			WebSocket.initWebSocket(this.wsReceive)
		},
		setUnread (number) {
            this.msgInfo.msgNumber = number
        }
	},persist: [
        {
            pick: ['isWebSocketOpen','msgInfo'],
            storage: sessionStorage,
        }
    ],
});
