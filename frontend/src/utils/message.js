import { ElMessage } from 'element-plus';

let messageDom = null;
const messageTypeList = ['success', 'error', 'warning', 'info'];
const Message = (options) => {
    if (messageDom) messageDom.close();
    messageDom = ElMessage(options);
};
messageTypeList.forEach((type) => {
    Message[type] = (options) => {
        if (typeof options === 'string') options = { message: options };
        options.type = type;
        return Message(options);
    };
});

export const MsgOk = (message) => {
    Message.success({
        message: message,
        type: 'success',
        showClose: true,
        duration: 3000,
    });
};

export const MsgWarn = (message) => {
    Message.warning({
        message: message,
        type: 'warning',
        showClose: true,
        duration: 3000,
    });
};

export const MsgError = (message) => {
    Message.error({
        message: message,
        type: 'error',
        showClose: true,
        duration: 3000,
    });
};