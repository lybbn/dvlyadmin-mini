<template>
    <el-card shadow="hover" class="lyccontainer">
        <template #header>
            <div>
                <el-button icon="Plus" type="primary" @click="handleClick('addgroup')" v-auth="'CreateGroup'">
                    新增分组
                </el-button>
                <el-button icon="Plus" type="primary" @click="handleClick('addcontent')" v-auth="'CreateContent'">
                    新增配置项
                </el-button>
            </div>
        </template>
        <el-tabs type="border-card" v-model="activeTab" v-if="editableTabs.length>0">
            <el-tab-pane
                v-for="(item, index) in editableTabs"
                :key="index"
                :label="item.title"
                :name="item.key"
            >   
                <apiWhiteList :options="item" v-if="item.key == 'apiWhiteList'" @refreshData="getGroups"></apiWhiteList>
                <FormItem :ref="(el) => setItemRef(el, item)" :options="item" :activeTab="activeTab" v-else @updateConfig="handleUpdateConfig"></FormItem>
            </el-tab-pane>
        </el-tabs>
        <el-empty v-else></el-empty>
        <AddModuleGroup ref="addGroupFlag" @refreshData="getGroups"></AddModuleGroup>
        <AddModuleContent ref="addContentFlag" @refreshData="getContentRefresh"></AddModuleContent>
    </el-card>
</template>

<script setup name="systemConfig">
    import {ref, onMounted, onBeforeUnmount} from 'vue'
    import AddModuleGroup from "./components/addModuleGroup.vue";
    import Api from '@/api/api'
    import AddModuleContent from "./components/addModuleContent.vue";
    import FormItem from "./components/formItem.vue";
    import apiWhiteList from './components/apiWhiteList.vue';
    import {useUserState} from "@/store/userState";

	const userState = useUserState()

    let activeTab = ref("base")
    let editableTabs = ref([])

    let addContentFlag = ref(null);

    let addGroupFlag = ref(null);

    function handleClick(flag) {
        if(flag == 'addgroup'){
            addGroupFlag.value.addModuleFn('',"新增分组")
        }else if(flag == 'addcontent'){
            addContentFlag.value.addModuleFn('',"新增配置项")
        }
    }

    function getGroups() {
        Api.platformsettingsSysconfig({limit:999,parent__isnull:true}).then(res=>{
            if(res.code == 2000){
                editableTabs.value = res.data.data
            }
        })
    }
    const formItemRefs = ref([]); // 存储所有 ref
    // 动态设置 ref
    const setItemRef = (el, item) => {
        if (el) {
            formItemRefs.value[item.key] = el;
        }
    }

    // 获取指定 ref
    const getRefByKey = (key) => {
        return formItemRefs.value[key];
    }

    function getContentRefresh(item){
        if(item.key == activeTab.value){
            const targetRef = getRefByKey(item.key);
            if (targetRef) {
                targetRef.fetchData(); // 调用子组件方法
            }
        }
        if(activeTab.value == "base"){
            handleUpdateConfig()
        }
    }

    function handleUpdateConfig(){
        userState.getSystemConfig()
    }

    onMounted(() => {
        getGroups()
    })
    
    onBeforeUnmount(() => {
    })
</script>

<style scoped lang="scss">
.lyccontainer{
    margin: 10px;
}
.mobile-button {
    padding: 8px 12px;
    
    &-text {
        display: inline-block;
        margin-left: 4px;
    }
}

@media (max-width: 768px) {
    .mobile-button {
        width: 100%;
        justify-content: center;
    }
}
</style>