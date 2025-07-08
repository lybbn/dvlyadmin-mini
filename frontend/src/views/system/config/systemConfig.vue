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
                <FormItem :options="item" :editableTabsItem="item"></FormItem>
            </el-tab-pane>
            <el-tab-pane label="Api白名单" name="apiWhiteList">
                <el-table :data="ApiList" v-loading="loading" style="width: 100%">
                    <el-table-column min-width="120" label="名称" prop="label"></el-table-column>
                    <el-table-column min-width="150" label="Api地址" prop="value"></el-table-column>
                    <el-table-column label="操作" fixed="right" width="140">
                        <template #header>
                            <div class="lycaozuol">
                                <span>操作</span>
                                <el-button circle  size="small"  type="primary" icon="Plus"></el-button>
                            </div>
                        </template>
                        <template #default="{ row, $index }">
                            <div>
                                <el-popconfirm title="确定删除吗？" @confirm="handleApiDelete(row)">
                                    <template #reference>
                                        <el-button link type="danger" v-auth="'systemConfig:Delete'">删除</el-button>
                                    </template>
                                </el-popconfirm>
                            </div>
                        </template>
                </el-table-column>
                </el-table>
            </el-tab-pane>
        </el-tabs>
        <el-empty v-else></el-empty>
        <AddModuleGroup ref="addGroupFlag" @refreshData="getGroups"></AddModuleGroup>
        <AddModuleContent ref="addContentFlag" @refreshData="getGroups"></AddModuleContent>
    </el-card>
</template>

<script setup name="systemConfig">
    import {ref, onMounted, onBeforeUnmount} from 'vue'
    import AddModuleGroup from "./components/addModuleGroup.vue";
    import Api from '@/api/api'
    import AddModuleContent from "./components/addModuleContent.vue";
    import FormItem from "./components/formItem.vue";

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

    let loading = ref(false)
    let ApiList = ref([])

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
.lycaozuol{
    display: flex;
    align-items: center;
    justify-content: space-between;
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