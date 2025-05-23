import { createPinia } from 'pinia'
import PiniaPluginPersistedstate from 'pinia-plugin-persistedstate';

const store = createPinia()
store.use(PiniaPluginPersistedstate);

export default store