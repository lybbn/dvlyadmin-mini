import { defineStore } from 'pinia'

export const cancelRequestState = defineStore('cancelRequest', {
    state:() => {
        return {
            cancelTokenList: []
        }
    },
    getters:{

    },
    actions: {
        addCancelToken(val) {
            if (!this.cancelTokenList) {
                this.cancelTokenList = []
            }
            if (val) {
                this.cancelTokenList.push(val)
            }
        },
        // 取消所有请求
        clearAllCancelToken() {
            this.cancelTokenList.forEach((cancel, index) => {
                if (cancel && !this.cancelTokenList[index].isCancelled) {
                    try {
                        cancel();  // 取消请求
                        this.cancelTokenList[index].isCancelled = true;  // 标记为已取消
                    } catch (err) {
                        if (err.name === 'CanceledError') {
                            // console.log('请求已经被取消');
                        } else {
                            // console.error('取消请求时发生错误:', err);
                        }
                    }
                }
            })
            this.cancelTokenList = []
        }
    },
})